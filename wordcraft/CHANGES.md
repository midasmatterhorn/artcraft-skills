# WordCraft — round 2026-11-04 changes

Re-pinned: v0.14.0 (`5cd53f1`) -> v0.15.1 (`08afab5`, installed `wordcraft 0.15.1 (08afab50)`).

## Corrected / re-measured

- `CommandSpec::new(` sites 648 → **652** (`proof.installPack`, `proof.packs`, `proof.removePack`, `review.language.preferred`).
- Proofing moved to craft-libs `craft-proof`; `craft-i18n.rev` moved to `9d6d54d6…`.

## Method

- 316 files changed across two releases.
- Command/tool id sets diffed between `v0.14.0` and `v0.15.1` with the extraction the published skill's `evidence.md` names; the counts above are the new sets.
- Every repo path cited in `SKILL.md` was re-resolved against the new checkout; paths that moved were re-cited.

## Unchanged

- Sections of the skill whose code path and counts did not move. They were path-verified at this tag and carried forward; no claim was silently re-dated.

## Known gap in this round

- The prose was not re-derived from scratch for every capability; this is a pin-and-verify refresh, not a new deep audit of every feature.
