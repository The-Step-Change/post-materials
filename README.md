# The Step Change: code and data behind the posts

[The Step Change](https://thestepchange.org/) tests what AI can and cannot do in real work. This repository holds the analysis, data and figures behind each post that rests on data or a model, so anyone can check the work or build on it.

## Posts

| Published | Post | Folder | What it tests |
|---|---|---|---|
| 2026-11-28 | [Can LLMs replace product research surveys?](https://thestepchange.org/p/can-llms-replace-product-research) | [2026-11-28-can-llms-replace-product-research](2026-11-28-can-llms-replace-product-research/) | Whether AI twins can stand in for survey panels, using a published method on six public datasets |

## How each folder is laid out

Every post has one folder, named `<date published>-<post slug>`, with the same five parts:

| Part | What it holds |
|---|---|
| `README.md` | The question, the finding, the limits, how to rerun it, and a link to the post |
| `analysis/` | Code that reproduces every figure and table in the post |
| `data/` | Data files small enough to keep here |
| `DATA.md` | Every source used: where to get it, its licence, the date downloaded and a checksum |
| `figures/` | The charts as published |

Data that is too large, or whose licence forbids sharing, is not in this repository. `DATA.md` says where to download it and where to put it.

## Corrections

If you find an error, open an issue. Corrections are recorded in the post's `README.md` with the date.

## Licence

- **Code** (everything under an `analysis/` folder, and any other script): MIT. See [LICENSE](LICENSE).
- **Text and charts** (the README files and everything under a `figures/` folder): [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/). Reuse them with credit to The Step Change and a link to the post.
- **Data from other publishers** keeps its own licence. Each post's `DATA.md` names it.
