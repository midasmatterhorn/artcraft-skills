# FigCraft — round 2026-11-04 changes

Re-pinned: v0.14.0 (`5fc2840`) -> v0.15.0 (`02c38a6`, installed `FigCraft 0.15.0 (02c38a6d959f0afd82e44d9d67d396266e6ab4a3)`).

## Corrected / re-measured

- CLI 9 → **10** verbs, MCP 18 → **19** tools, control 17 → **18** methods.
- SVG/.fig round-trip fidelity plus plugin-manifest validation.

## Method

- 105 files changed.
- Command/tool id sets diffed between `v0.14.0` and `v0.15.0` with the extraction the published skill's `evidence.md` names; the counts above are the new sets.
- Every repo path cited in `SKILL.md` was re-resolved against the new checkout; paths that moved were re-cited.

## Unchanged

- Sections of the skill whose code path and counts did not move. They were path-verified at this tag and carried forward; no claim was silently re-dated.

## Known gap in this round

- The prose was not re-derived from scratch for every capability; this is a pin-and-verify refresh, not a new deep audit of every feature.
