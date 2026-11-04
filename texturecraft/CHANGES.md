# TextureCraft — round 2026-11-04 changes

Re-pinned: v0.2.0 (`e01dac2`) -> v0.3.0 (`8547514`, installed `TextureCraft 0.3.0 (8547514 2026-11-03)`).

## Corrected / re-measured

- Engine command extract 135 → **162** ids; menu parity 55/55; control channel hardened (owner-only token, 10 s auth deadline, 16-connection cap).
- 22 MCP tools (18 headless + 4 bridge), 17 JSON-lines methods, 13 control methods + auth.

## Method

- 168 files changed; the engine command extract grows from 135 to **162** ids (+27: `bake.
- Command/tool id sets diffed between `v0.2.0` and `v0.3.0` with the extraction the published skill's `evidence.md` names; the counts above are the new sets.
- Every repo path cited in `SKILL.md` was re-resolved against the new checkout; paths that moved were re-cited.

## Unchanged

- Sections of the skill whose code path and counts did not move. They were path-verified at this tag and carried forward; no claim was silently re-dated.

## Known gap in this round

- The prose was not re-derived from scratch for every capability; this is a pin-and-verify refresh, not a new deep audit of every feature.
