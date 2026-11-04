# PdfCraft — round 2026-11-04 changes

Re-pinned: v0.17.0 (`7d78f3e`) -> v0.18.1 (`8bb0528`, installed `pdfcraft 0.18.1`).

## Corrected / re-measured

- Tools 183 → **184** (`doc_bates_multi`); registry commands 205 → **210**.
- Dropped the unmeasurable "35 languages" claim; the `.tsv` catalogs are gone.

## Method

- 260 files changed.
- Command/tool id sets diffed between `v0.17.0` and `v0.18.1` with the extraction the published skill's `evidence.md` names; the counts above are the new sets.
- Every repo path cited in `SKILL.md` was re-resolved against the new checkout; paths that moved were re-cited.

## Unchanged

- Sections of the skill whose code path and counts did not move. They were path-verified at this tag and carried forward; no claim was silently re-dated.

## Known gap in this round

- The prose was not re-derived from scratch for every capability; this is a pin-and-verify refresh, not a new deep audit of every feature.
