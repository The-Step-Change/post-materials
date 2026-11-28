"""Semantic similarity rating (Maier et al., arXiv 2510.08338) and its metrics.

Written from the paper's equations, not copied from the authors' package, and
checked against their code (github.com/pymc-labs/semantic-similarity-rating):
the same inputs give the same probabilities.
"""

import numpy as np


def unit(x):
    x = np.asarray(x, dtype=float)
    return x / np.linalg.norm(x, axis=-1, keepdims=True)


def ssr_pmf(responses, anchor_sets, epsilon=0.0, temperature=1.0):
    """Map response embeddings to probabilities over the scale points.

    responses: (n, d). anchor_sets: (sets, points, d). Returns (n, points).

    Per anchor set: p(r) ∝ γ_r − min γ + ε·[r is the minimum], with γ the cosine
    similarity to anchor r; then p ∝ p^(1/T); then the mean over sets.
    """
    gamma = np.einsum("nd,spd->nsp", unit(responses), unit(anchor_sets))
    lowest = gamma.min(axis=-1, keepdims=True)
    p = gamma - lowest + epsilon * (gamma == lowest)
    total = p.sum(axis=-1, keepdims=True)
    # A response equally similar to every anchor carries no information: uniform.
    p = np.where(total > 0, p / np.where(total > 0, total, 1), 1 / p.shape[-1])
    if temperature != 1.0:
        p = p ** (1 / temperature)
        p = p / p.sum(axis=-1, keepdims=True)
    return p.mean(axis=1)


def expected_rating(pmf):
    return pmf @ np.arange(1, pmf.shape[-1] + 1)


def ks_similarity(p, q):
    """1 − the largest gap between two cumulative distributions over the scale."""
    return 1 - np.abs(np.cumsum(p) - np.cumsum(q)).max()


def pearson(x, y):
    return float(np.corrcoef(x, y)[0, 1])


def panel_ceiling(answers, panel_size, draws=2000, seed=0):
    """How well a real panel of `panel_size` people ranks the stimuli.

    answers: (respondents, stimuli), NaN where missing. Each draw correlates
    the stimulus means of a random panel with those of everyone else. With
    panel_size = half the respondents this is the paper's split-half R_xx.
    """
    rng = np.random.default_rng(seed)
    n = len(answers)
    r = []
    for _ in range(draws):
        order = rng.permutation(n)
        a, b = answers[order[:panel_size]], answers[order[panel_size:]]
        r.append(pearson(np.nanmean(a, axis=0), np.nanmean(b, axis=0)))
    return float(np.mean(r))


def bootstrap_ci(stat, n, draws=5000, seed=0):
    """95% interval of stat(index) when the n stimuli are resampled with replacement."""
    rng = np.random.default_rng(seed)
    values = [stat(rng.integers(0, n, n)) for _ in range(draws)]
    return tuple(float(v) for v in np.nanpercentile(values, [2.5, 97.5]))
