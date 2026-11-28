"""Reproduce the post's figures from the stored files in data/. No model is called.

    uv run python analysis/reproduce.py

Scores for ranking are out of 100, where 100 is how well a second group of real
people ranks the same things. "Interval" is a 95% bootstrap interval for the
difference between two scores: if it excludes 0, the difference is beyond what
chance would explain.
"""

import csv
from collections import defaultdict
from pathlib import Path

import numpy as np

import ssr

DATA = Path(__file__).resolve().parent.parent / "data"


def read(name):
    with open(DATA / name) as f:
        return list(csv.DictReader(f))


def num(x):
    return float(x) if x != "" else np.nan


def score_diff(a, b, truth, ceiling):
    """95% interval of (score of a - score of b), resampling the items ranked."""
    lo, hi = ssr.bootstrap_ci(lambda i: ssr.pearson(a[i], truth[i]) - ssr.pearson(b[i], truth[i]), len(truth))
    return f"interval {100 * lo / ceiling:.0f} to {100 * hi / ceiling:.0f}"


def groceries():
    rows = read("groceries_people.csv")
    people = list(dict.fromkeys(r["person"] for r in rows))
    at = {p: i for i, p in enumerate(people)}
    bought, level, panel = np.full((len(people), 40), np.nan), np.zeros((len(people), 40), int), np.zeros(len(people), bool)
    for r in rows:
        i, k = at[r["person"]], int(r["product"]) - 1
        bought[i, k], level[i, k], panel[i] = num(r["bought"]), int(r["price_level"]), r["in_panel_of_100"] == "1"
    twins = defaultdict(lambda: np.full((len(people), 40), np.nan))
    for r in read("groceries_twins.csv"):
        twins[r["model"], r["arm"]][at[r["person"]], int(r["product"]) - 1] = num(r["value"])
    regular = np.array([float(r["regular_price"]) for r in read("groceries_products.csv")])

    rate = np.nanmean(bought, axis=0)
    ceiling = ssr.panel_ceiling(bought, 100)
    mean = lambda g, who: np.nanmean(g[who], axis=0)
    score = lambda s: 100 * ssr.pearson(s, rate) / ceiling
    arms = {"Haiku, paper's method": mean(twins["claude-haiku-5-5", "ssr"], panel),
            "Sonnet, paper's method": mean(twins["claude-sonnet-5-5", "ssr"], panel),
            "Sonnet, 1 to 5 score": mean(twins["claude-sonnet-5-5", "direct"], panel),
            "Haiku, yes or no": mean(twins["claude-haiku-5-5", "yesno"], panel),
            "Haiku, yes or no, all 2,058 twins": mean(twins["claude-haiku-5-5", "yesno"], slice(None)),
            "simple guess: cheapest first": -regular}
    print(f"Groceries: ranking 40 products ({len(people)} real people; a second group of 100 real people scores 100)")
    for name, s in arms.items():
        print(f"  {name:<36}{score(s):>4.0f}")
    print(f"  Sonnet 1 to 5 minus the guess: {score_diff(arms['Sonnet, 1 to 5 score'], arms['simple guess: cheapest first'], rate, ceiling)}")
    print(f"  Haiku paper's method minus the guess: {score_diff(arms["Haiku, paper's method"], arms['simple guess: cheapest first'], rate, ceiling)}")

    # A random group of k real people against all the others, 400 draws (as in the more-twins chart).
    rng = np.random.default_rng(0)
    orders = [rng.permutation(len(people)) for _ in range(400)]
    for k in (10, 20, 60):
        r = np.mean([ssr.pearson(np.nanmean(bought[o[:k]], axis=0), np.nanmean(bought[o[k:]], axis=0)) for o in orders])
        print(f"  {k} real people{'':<23}{100 * r / ceiling:>4.0f}")

    # One person at a time: does the twin give its own person's yes or no?
    twin = twins["claude-haiku-5-5", "yesno"]
    ok = ~np.isnan(twin) & ~np.isnan(bought)
    cell = np.zeros_like(bought)  # share of real people saying yes to that product at that price
    for k in range(40):
        for lv in np.unique(level[:, k]):
            cell[level[:, k] == lv, k] = np.nanmean(bought[level[:, k] == lv, k])
    print("Groceries: one person at a time, share of answers matching the real person")
    print(f"  {'Haiku twin, yes or no':<36}{100 * (twin == bought)[ok].mean():>4.0f}%")
    print(f"  {'simple guess: what most people did':<36}{100 * ((cell > 0.5) == bought)[ok].mean():>4.0f}%")


def food():
    photos = read("food_photos.csv")
    real, sd = np.array([float(p["mean_US"]) for p in photos]), np.array([float(p["sd_US"]) for p in photos])
    group = np.array([p["group"] for p in photos])
    n = len(photos)
    ceiling = 1 - (sd**2).mean() / (275 * 60 / n) / real.var()  # two real panels of about 34 raters per photo
    at = {p["photo"]: i for i, p in enumerate(photos)}
    got = defaultdict(list)
    for r in read("food_twins.csv"):
        got["number", at[r["photo"]]].append(num(r["gpt4o_number"]))
        got["ssr", at[r["photo"]]].append(num(r["gpt4o_ssr"]))
    arm = lambda a: np.array([np.nanmean(got[a, i]) for i in range(n)])
    arms = {"GPT-4o, paper's method": arm("ssr"), "GPT-4o, 1 to 5 score": arm("number"),
            "simple guess: average for that kind of food": np.array([real[(group == group[i]) & (np.arange(n) != i)].mean() for i in range(n)])}
    print(f"Food photos: ranking {n} photos (US raters)")
    for name, s in arms.items():
        print(f"  {name:<44}{100 * ssr.pearson(s, real) / ceiling:>4.0f}")
    print(f"  1 to 5 minus the guess: {score_diff(arms['GPT-4o, 1 to 5 score'], arms['simple guess: average for that kind of food'], real, ceiling)}")


def polls():
    by = defaultdict(lambda: ([], []))
    for r in read("polls.csv"):
        by[r["question"]][0].append(float(r["real_share"]))
        by[r["question"]][1].append(float(r["sonnet_ssr_share"]))
    real = [np.array(h) for h, _ in by.values()]
    arms = {"Sonnet, paper's method": [np.array(s) for _, s in by.values()],
            "simple guess: every answer equally popular": [np.full(len(h), 1 / len(h)) for h in real]}
    error = {name: np.array([100 * np.abs(p - h).mean() for p, h in zip(ps, real)]) for name, ps in arms.items()}
    print(f"Poll questions: {len(real)} Pew questions, average gap from the real share of each answer, in points (lower is better)")
    for name, e in error.items():
        print(f"  {name:<44}{e.mean():>5.1f}")
    d = error["Sonnet, paper's method"] - error["simple guess: every answer equally popular"]
    lo, hi = ssr.bootstrap_ci(lambda i: d[i].mean(), len(d))
    print(f"  paper's method minus the guess: interval {lo:.1f} to {hi:.1f}")


def coats():
    real = {(r["person"], r["coat"]): (int(r["rating"]), r["jacket_type"]) for r in read("coats_people.csv") if r["half"] == "test"}
    twins = read("coats_twins.csv")  # the held-back half only
    truth = np.eye(5)[[real[t["person"], t["coat"]][0] - 1 for t in twins]]
    kind = np.array([real[t["person"], t["coat"]][1] for t in twins])
    one_hot = lambda x: np.eye(5)[int(x) - 1] if x == x else np.full(5, np.nan)
    arms = {"Haiku, paper's method": np.array([[float(t[f"ssr_p{k}"]) for k in range(1, 6)] for t in twins]),
            "Haiku, all coats scored at once": np.array([one_hot(num(t["all_at_once_rating"])) for t in twins])}
    types = sorted(set(kind))
    dist = lambda x: np.nanmean(x, axis=0)
    ks = {name: np.array([ssr.ks_similarity(dist(truth[kind == t]), dist(x[kind == t])) for t in types]) for name, x in arms.items()}
    ks["simple guess: the average for the other coats"] = np.array([ssr.ks_similarity(dist(truth[kind == t]), dist(truth[kind != t])) for t in types])
    print(f"Coats: mix of 1 to 5 ratings, {len(twins)} answers from the held-back half of the raters, {len(types)} jacket types "
          "(100 = the same mix as real people)")
    for name, v in ks.items():
        print(f"  {name:<46}{100 * v.mean():>4.0f}")
    d = ks["simple guess: the average for the other coats"] - ks["Haiku, all coats scored at once"]
    lo, hi = ssr.bootstrap_ci(lambda i: d[i].mean(), len(d))
    print(f"  guess minus all at once: interval {100 * lo:.0f} to {100 * hi:.0f}")


def adverts():
    print("Adverts: summary figures only, because the ADS-16 licence forbids sharing its data (see DATA.md)")
    for r in read("adverts_summary.csv"):
        v = float(r["value"])
        print(f"  {r['measure']}, {r['who'] or 'value'}: {100 * v:.0f}" if "share" in r["measure"] else f"  {r['measure']}, {r['who'] or 'value'}: {v:.3f}")


def answers():
    total = sum(int(r["answers"]) for r in read("answer_counts.csv"))
    print(f"AI answers generated in all: {total:,}")


if __name__ == "__main__":
    print("The paper's own figures (90 and 82) are quoted from it; its data is not public.\n")
    for part in (groceries, food, polls, coats, adverts, answers):
        part()
        print()
