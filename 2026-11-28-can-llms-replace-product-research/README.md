# Can LLMs replace product research surveys?

**Post:** https://thestepchange.org/p/can-llms-replace-product-research (published 2026-11-28)

## The question

A 2025 paper ([Maier et al., arXiv 2510.08338](https://arxiv.org/abs/2510.08338)) reports that "AI twins", a language model given a real survey taker's demographics, rank new products about 90% as well as a second group of real people, using its method of semantic similarity rating (SSR), against about 82% for asking for a 1 to 5 score. Its data is not public. The post tries the same method on six public datasets.

## What we found

- **The paper's method never beat a simple guess.** Each test had a simple guess that uses no AI. The simple guess won three tests, asking for a plain 1 to 5 score won two, and one was a tie.
- **The best results were on everyday products, as a crowd.** Asking for a 1 to 5 score ranked 40 groceries 86 out of 100 (Claude Sonnet 5.5) and 479 food photos 82 (GPT-4o), where 100 is a second group of real people. The paper's method scored 74 on the groceries with Claude Haiku 5.5 and 73 with Sonnet.
- **One person at a time, the twins did worse than the crowd.** A twin gave its own person's yes or no 68% of the time; guessing whatever most people answered got 74%.
- **More twins did not help.** 2,058 twins ranked the groceries no better than 100 (78 against 79 with Haiku), while real groups kept improving: 10 people 75, 20 people 86, 60 people 97.
- **Twins rarely say no.** On the adverts, real people gave the lowest rating 55% of the time; the twins, 3%. On 40 Pew poll questions, the twins did no better than assuming every answer is equally likely.

The six tests:

| Test | Paper's method | Our best AI | Simple guess |
|---|---|---|---|
| Groceries: ranking | 74 (Haiku) | **86** (Sonnet, 1 to 5 score) | 60 |
| Food photos: ranking | 75 (GPT-4o) | **82** (GPT-4o, 1 to 5 score) | 69 |
| Poll questions | 10.9 (Sonnet) | 10.9 (Sonnet, paper's method) | 11.5 |
| Coats: mix of ratings | 66 (Haiku) | 84 (Haiku, all coats scored at once) | **91** |
| Adverts: ranking | 59 (Haiku) | 59 (Haiku, paper's method) | **77** |
| Groceries: one person at a time | not tried | 68% (Haiku, yes or no) | **74%** |

Scores are out of 100, where 100 is a second group of real people (for the coats, the same mix of 1 to 5 ratings as real people). Polls are the average gap from the real result in points, lower is better. Bold: better than the other side beyond what chance would explain. The guesses, in order: cheapest first; the average for that kind of food; every answer equally popular; the average for the other coats; the average for that kind of advert; whatever most people answered.

## What this does not show

- **It does not disprove the paper.** We had no product-concept surveys, the paper's reference sentences were tuned on its own surveys and not published, and except for the food photos we used different models (Claude Haiku 5.5 and Sonnet 5.5 rather than GPT-4o).
- **Small numbers.** 40 products, 40 poll questions and 120 advert raters give wide intervals. `analysis/reproduce.py` prints the intervals behind the bold entries.
- **Only two tests showed pictures,** as the paper did: the food photos and the adverts. The others described the product in words.
- **The questions differ from the paper's.** Food photos measure desire to eat and adverts measure intent to click, not intent to buy.
- **The adverts cannot be rechecked from this folder.** The ADS-16 licence forbids sharing its data, so only summary figures are here.

## Reproduce it

```bash
uv sync
uv run python analysis/reproduce.py
```

It takes a few seconds and costs nothing. Every step runs from the stored files in `data/`: no model is called and no key is needed. It prints every figure in the table above and the post's other figures. The paper's own figures (90 and 82) are quoted from the paper. The adverts figures are read from `data/adverts_summary.csv`, not recomputed (see `DATA.md`).

About 410,000 AI answers went into the work; `data/answer_counts.csv` counts them by part.

## What is in this folder

| Path | What it is |
|---|---|
| `analysis/reproduce.py` | Computes the post's figures from `data/` |
| `analysis/ssr.py` | The paper's method (SSR) and the scores used to judge it |
| `data/` | The real people's answers, reshaped, and the AI twins' answers as numbers; one file per dataset |
| `DATA.md` | Sources, licences, checksums and download instructions |
| `figures/` | The five charts in the post, as published |
| `pyproject.toml`, `uv.lock`, `.python-version` | The Python environment for `uv` |

The figures, in the order they appear in the post: the paper's result, the datasets, the six tests, more twins against more people, and the share of each rating on the adverts.

## Corrections

None.
