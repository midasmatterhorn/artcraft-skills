# EffectCraft — round 2026-11-04 changes

Re-pinned: v0.20.0 (`720c671`) -> v0.21.0 (`7870b59`, installed `effectcraft 0.21.0`).

## Corrected / re-measured

- Effects 307 → **308**; render formats 13 → **14**; 36 MCP tools (9 bridge-only), 24 control methods.
- Shortcut scopes are a new settings surface.

## Method

- 46 files changed; the command-id set is unchanged (608 ids).
- Command/tool id sets diffed between `v0.20.0` and `v0.21.0` with the extraction the published skill's `evidence.md` names; the counts above are the new sets.
- Every repo path cited in `SKILL.md` was re-resolved against the new checkout; paths that moved were re-cited.

## Unchanged

- Sections of the skill whose code path and counts did not move. They were path-verified at this tag and carried forward; no claim was silently re-dated.

## Known gap in this round

- The prose was not re-derived from scratch for every capability; this is a pin-and-verify refresh, not a new deep audit of every feature.
