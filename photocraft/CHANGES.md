# PhotoCraft — round 2026-11-04 changes

Re-pinned: v0.19.0 (`2df9f80`) -> v0.20.1 (`327c4cc`, installed `photocraft 0.20.1 (327c4cc82, 2026-11-03)`).

## Corrected / re-measured

- 78 engine command ids at both tags; `actions.*` is now 17 ids (`actions.newSet`), and `.atn` I/O gained `actions.record {set}`, `actions.load {encoding}`, `actions.save {skipUnsupported}`.
- Actions/.atn import-export matrix and the editable Line-tool arrowheads are the release's feature surface.

## Method

- 276 files changed; the engine command set is unchanged (78 ids at both tags).
- Command/tool id sets diffed between `v0.19.0` and `v0.20.1` with the extraction the published skill's `evidence.md` names; the counts above are the new sets.
- Every repo path cited in `SKILL.md` was re-resolved against the new checkout; paths that moved were re-cited.

## Unchanged

- Sections of the skill whose code path and counts did not move. They were path-verified at this tag and carried forward; no claim was silently re-dated.

## Known gap in this round

- The prose was not re-derived from scratch for every capability; this is a pin-and-verify refresh, not a new deep audit of every feature.
