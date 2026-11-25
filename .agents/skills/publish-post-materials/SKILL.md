---
name: publish-post-materials
description: Turn the working files behind a published Step Change post into a clean public folder in this repository. Use after a post that rests on data or a model has been published.
---

# Publish a post's materials

The working folders are private and may be messy. This repository is public and must be clean. Never copy a working folder wholesale: build the public folder file by file.

## Who does this

The session that did the analysis builds the folder, because it knows which code made each figure and what each dataset's licence allows. It does not approve its own folder: the publication's manager session checks it against the published post and this checklist, and the owner then says whether to push.

## Before you start

- The post is published and archived (`posts/index.md` in the publication's private project lists it).
- You know which working repository holds the analysis.

## Steps

1. **Make the folder.** Copy `_template/` to `<date published>-<post slug>/`, using the slug from the post's address.
2. **Code.** Copy only the code needed to reproduce the post's figures and tables into `analysis/`. Remove dead experiments, scratch scripts and absolute paths. Keep it runnable with `uv`.
3. **Data, one source at a time.** For each source, read its licence. Include a file only if the licence allows redistribution and the file is under 50 MB. Otherwise leave it out and write download instructions. Record every source in `DATA.md`, with the checksum of the file used.
4. **Stored model outputs.** Include them if they are small and contain nothing from a source that forbids redistribution, so readers can rerun the analysis without paying for model calls.
5. **Figures.** Copy the charts as published into `figures/`.
6. **README.** Fill in every section of the template. Copy each figure from the published post, not from memory or working notes.
7. **Check, in this order. Stop at the first failure.**
   - No secrets: search the folder for keys, tokens, `.env` files and personal details (names of private people, email addresses, home paths).
   - No forbidden data: every file under `data/` has a row in `DATA.md` marked as allowed.
   - Numbers match: every figure in `README.md` appears in the published post with the same value.
   - It runs: clone the repository into an empty folder and follow the README's "Reproduce it" steps exactly.
   - Size: no file over 50 MB.
8. **Index.** Add the post's row to the table in the top-level `README.md`.
9. **Commit locally. Do not push.** Pushing publishes. The owner approves each post's folder before it is pushed; the publication's manager session checks it first.

## Corrections after publishing

Fix the file, add a dated line under "Corrections" in the post's README saying what changed and why, and never rewrite history.
