# Craft Anything — round 2026-11-04 changes

Re-pinned: v0.2.0 (`b09b99a`) -> v0.3.0 (`e6280b5`, installed `craft-anything 0.3.0`).

## Corrected / re-measured

- Engine tools 298 → **299** (`projects` 18 → 19). The macOS bundle does ship `craft-anything-cli` — corrected.
- CLI: `--build-with`, `--generate-assets`; `--resume` needs `--continue-in`; `--rounds` defaults to 2.

## Method

- 135 files changed.
- Command/tool id sets diffed between `v0.2.0` and `v0.3.0` with the extraction the published skill's `evidence.md` names; the counts above are the new sets.
- Every repo path cited in `SKILL.md` was re-resolved against the new checkout; paths that moved were re-cited.

## Unchanged

- Sections of the skill whose code path and counts did not move. They were path-verified at this tag and carried forward; no claim was silently re-dated.

## Known gap in this round

- The prose was not re-derived from scratch for every capability; this is a pin-and-verify refresh, not a new deep audit of every feature.
