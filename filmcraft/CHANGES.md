# FilmCraft — round 2026-11-04 changes

Re-pinned: v0.16.0 (`77adc30`) -> v0.17.0 (`eb59ec0`, installed `filmcraft 0.17.0`).

## Corrected / re-measured

- Schema 15 → **17**, languages 12 → **17**, workspaces 9 → **10**, CLI 12 → **13**, control methods 23 → **24**, presets 39 → **42**.
- craft-libs pin `c5a1cbfb…`.

## Method

- 75 files changed; the dotted-id command set is unchanged (176 ids).
- Command/tool id sets diffed between `v0.16.0` and `v0.17.0` with the extraction the published skill's `evidence.md` names; the counts above are the new sets.
- Every repo path cited in `SKILL.md` was re-resolved against the new checkout; paths that moved were re-cited.

## Unchanged

- Sections of the skill whose code path and counts did not move. They were path-verified at this tag and carried forward; no claim was silently re-dated.

## Known gap in this round

- The prose was not re-derived from scratch for every capability; this is a pin-and-verify refresh, not a new deep audit of every feature.
