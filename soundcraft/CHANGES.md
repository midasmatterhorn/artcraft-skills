# SoundCraft — round 2026-11-04 changes

Re-pinned: v0.16.0 (`db51dd1`) -> v0.17.0 (`b35dd0f`, installed `soundcraft 0.17.0 (macos aarch64)`).

## Corrected / re-measured

- UI menu commands 67 → **68** (`ui.new_tracks_dialog`); 17 MCP tools + 2 resources, 17 control methods + 2 aliases, 10 CLI subcommands.
- VST3 accepts 64 buses but activates only bus 0 per direction — no discrete multi-out.

## Method

- 18 files changed; the command-id set is unchanged (240 ids; the UI menu registry is **68** commands, not the 67 the previous skill carried).
- Command/tool id sets diffed between `v0.16.0` and `v0.17.0` with the extraction the published skill's `evidence.md` names; the counts above are the new sets.
- Every repo path cited in `SKILL.md` was re-resolved against the new checkout; paths that moved were re-cited.

## Unchanged

- Sections of the skill whose code path and counts did not move. They were path-verified at this tag and carried forward; no claim was silently re-dated.

## Known gap in this round

- The prose was not re-derived from scratch for every capability; this is a pin-and-verify refresh, not a new deep audit of every feature.
