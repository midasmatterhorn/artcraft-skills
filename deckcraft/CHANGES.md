# DeckCraft — round 2026-11-04 changes

Re-pinned: v0.14.1 (`ee39ff6`) -> v0.15.0 (`3e178d8`, installed `deckcraft 0.15.0`).

## Corrected / re-measured

- Command ids unchanged (234); 306 `cmd!(` sites; craft-libs pin now `c5a1cbfb…`.
- Presenter popout, H.264 motion vectors, PPTX tags parsing.

## Method

- 52 files changed; the command-id set is unchanged (234 ids; 306 `cmd!(` sites).
- Command/tool id sets diffed between `v0.14.1` and `v0.15.0` with the extraction the published skill's `evidence.md` names; the counts above are the new sets.
- Every repo path cited in `SKILL.md` was re-resolved against the new checkout; paths that moved were re-cited.

## Unchanged

- Sections of the skill whose code path and counts did not move. They were path-verified at this tag and carried forward; no claim was silently re-dated.

## Known gap in this round

- The prose was not re-derived from scratch for every capability; this is a pin-and-verify refresh, not a new deep audit of every feature.
