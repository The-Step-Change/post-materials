# Data sources

One row per source. A file is included here only if its licence allows redistribution and it is small enough for GitHub (under 50 MB a file). Every file in `data/` is plain numbers and short labels: no model's written answers, no prompts and no advert.

## Public datasets

| Source | What it is | Licence | Included here? | Where to get it | Downloaded | SHA-256 of the file used |
|---|---|---|---|---|---|---|
| Twin-2K-500 (Toubia et al., 2025) | Groceries: 2,058 people said whether they would buy 40 products, each at a price, and gave their demographics | CC BY 4.0 | yes, reshaped: `data/groceries_products.csv` (product names and regular prices), `data/groceries_people.csv` (each person's answer and the price level they saw) | [huggingface.co/datasets/LLM-Digital-Twin/Twin-2K-500](https://huggingface.co/datasets/LLM-Digital-Twin/Twin-2K-500) | 2026-11-23 | `wave_3_numbers_anonymized.csv` d411654eb97f55858d07485df5d2a0794a3c03325050e6035ab4f08d5282ec93; `wave_4_numbers_anonymized.csv` 05cb67c89dd8e43f6878c0cd9b97275e83a793bfe25c5cb1d3b97483f98ba529; `wave1_3_response_label.csv` 4d735be9e5f00d072d17be25029cef524de9ec383911a4acc44f0b64a9c5818c |
| CROCUFID (Toet et al., 2019) | Food photos: 479 photos, each with the average and spread of US raters' desire to eat it | CC BY 4.0 | yes, reshaped: `data/food_photos.csv` (photo number, food group, US mean and standard deviation). The photos are not included. | [osf.io/5jtqx](https://osf.io/5jtqx/) | 2026-11-24 | `All_Foodpictures_information.xlsx` 1f6febb4aede28e4c942b96fa2670073096eb5bd10bfd15b5fd97fc7b3c5323a |
| Pew Research Center, comparison topline to "Can AI Stand In for Human Survey-Takers? Not Really" | Poll questions: the share of real adults choosing each answer | Pew's terms of use: excerpts may be reproduced with attribution; not in full | an excerpt: the real shares for the 40 questions used, in `data/polls.csv`, with Pew's wave and question code so each can be found in the topline. The topline itself is not included. | [the report](https://www.pewresearch.org/data-labs/2026/09/30/can-ai-stand-in-for-human-survey-takers-not-really/), which links the topline PDF | 2026-11-23 | `topline.pdf` 4a01ea601fd647f04cfda8c479bcc40cb22d98bebb1ea60acde39f51b68c6f05 |
| Coat Shopping (Schnabel et al., 2016) | Coats: 290 people each rated 16 randomly assigned coats from 1 to 5 | CC BY-NC 4.0 (non-commercial) | yes, reshaped: `data/coats_people.csv` (person, coat, jacket type, coat gender, rating) | [cs.cornell.edu/~schnabts/mnar](https://www.cs.cornell.edu/~schnabts/mnar/) | 2026-11-23 | `coat.zip` 6073d0b515ed1f6e830e4fead66dc76ad7991a7553eaa58e228b234a9d19daed; `test.ascii` de6714ab105a5e0be8166be7fd313901b29f9a09c3bea307901457d1d71847e6 |
| ADS-16 (Roffo and Vinciarelli, 2016) | Adverts: 120 people each rated 300 adverts from 1 to 5 | Release agreement: research use only; the database "will not be further distributed" | **no.** Only summary figures computed from it are here, in `data/adverts_summary.csv`. To recompute them, download the dataset yourself, under its agreement. | [kaggle.com/datasets/groffo/ads16-dataset](https://www.kaggle.com/datasets/groffo/ads16-dataset) (needs a Kaggle account) | 2026-11-24 | not recorded: the download was unpacked and the zip not kept |
| Amazon Reviews 2023 (McAuley Lab) | Product reviews: 1,000 reviews from the Subscription Boxes category, used to check the step that turns words into a rating. No figure in the post is computed from it. | none stated | **no** | [amazon-reviews-2023.github.io](https://amazon-reviews-2023.github.io/) | 2026-11-23 | `Subscription_Boxes.jsonl.gz` d62b81bd021ab6482e68605a97702f7c9df21314ff9657d3c1d0c34351d66ebd |

Changes made to the CC BY and CC BY-NC data: reshaped to one row per answer, with columns renamed; for Twin-2K-500, only the first pricing survey is kept, and `in_panel_of_100` marks the 100 people, drawn at random, whose AI twins answered every arm. In `coats_people.csv`, the `half` column is ours: the raters split at random into the half used to tune prompts and the half held back.

## Stored model outputs (ours)

Written by the working repository from its saved model answers, with no new model calls. They hold numbers only, released under CC BY 4.0 like the rest of this folder's text and charts.

| File | What it is |
|---|---|
| `data/groceries_twins.csv` | Each AI twin's answer to each grocery product: Claude Haiku 5.5 and Sonnet 5.5, the paper's method (`ssr`, the expected rating from 1 to 5), Sonnet's 1 to 5 score (`direct`), and Haiku's yes or no (`yesno`, 1 = yes) for all 2,058 people |
| `data/food_twins.csv` | GPT-4o's answer for each of 6 twins per photo: its 1 to 5 score, and the expected rating from the paper's method with OpenAI's `text-embedding-3-small` |
| `data/polls.csv` | Column `sonnet_ssr_share`: the share of Claude Sonnet 5.5 twins (150 personas) given to each answer by the paper's method |
| `data/coats_twins.csv` | For the held-back half of the coat raters: the paper's method as a probability for each rating 1 to 5 (Claude Haiku 5.5), and Haiku's rating when shown all 16 coats at once |
| `data/adverts_summary.csv` | Summary figures for the adverts: ranking scores and the share of each rating, for real people and for Haiku twins |
| `data/answer_counts.csv` | How many AI answers each part of the work produced |

The paper's method turns each written answer into a rating by comparing it with five reference sentences, using an embedding model (`analysis/ssr.py` has the arithmetic). The stored files hold the results of that step rather than the written answers, so the step itself is not rerun here.

## Required credit lines

- **ADS-16:** "The research in this paper use the ADS-16 database" and a citation to: G. Roffo, A. Vinciarelli, Personality in Computational Advertising: A Benchmark. ACM RecSys - ACM on Recommender Systems - International Workshop on Emotions and Personality in Personalized Systems (EMPIRE 2016).
- **Pew Research Center:** "Can AI Stand In for Human Survey-Takers? Not Really." Pew Research Center, Washington, D.C. (2026-09-30) https://www.pewresearch.org/data-labs/2026/09/30/can-ai-stand-in-for-human-survey-takers-not-really/. Pew Research Center bears no responsibility for the analyses or interpretations of the data presented here.
- **Twin-2K-500 (CC BY 4.0):** Toubia, O., Gui, G. Z., Peng, T., Merlau, D. J., Li, A. and Chen, H. (2025). Twin-2K-500: A Dataset for Building Digital Twins of 2,000 People. Hugging Face. https://arxiv.org/abs/2505.17479
- **CROCUFID (CC BY 4.0):** Toet, A. et al. (2019). CROCUFID: A Cross-Cultural Food Image Database for Research on Food Elicited Affective Responses. Frontiers in Psychology. https://osf.io/5jtqx/
- **Coat Shopping (CC BY-NC 4.0):** Schnabel, T., Swaminathan, A., Singh, A., Chandak, N. and Joachims, T. (2016). Recommendations as Treatments: Debiasing Learning and Evaluation. ICML 2016. https://www.cs.cornell.edu/~schnabts/mnar/
