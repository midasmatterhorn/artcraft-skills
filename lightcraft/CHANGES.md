# LightCraft — round 2026-11-04 changes

Re-pinned: v0.17.0 (`5a09d07`) -> v0.18.0 (`32d569a`, installed `lightcraft 0.18.0`).

## Corrected / re-measured

- Re-measured the command registry at **380** `cmd!` specs (the previous skill carried a contradictory 375/379).
- The delta is correctness-only; no id was added.

## Method

- 13 files changed; the command set is unchanged (274 ids).
- Command/tool id sets diffed between `v0.17.0` and `v0.18.0` with the extraction the published skill's `evidence.md` names; the counts above are the new sets.
- Every repo path cited in `SKILL.md` was re-resolved against the new checkout; paths that moved were re-cited.

## Unchanged

- Sections of the skill whose code path and counts did not move. They were path-verified at this tag and carried forward; no claim was silently re-dated.

## Known gap in this round

- The prose was not re-derived from scratch for every capability; this is a pin-and-verify refresh, not a new deep audit of every feature.
