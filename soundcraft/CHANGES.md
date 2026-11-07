# SoundCraft — round 2026-11-07 changes

Re-pinned: v0.17.0 (`b35dd0f`) -> v0.18.0 (`5ff012ab`, installed `soundcraft 0.18.0 (macos aarch64)`).

## Corrected / re-measured

- UI commands 68 → **70** (`ui.reduce_visual_effects`, `ui.undo_levels`; nothing removed), so a
  running app's `engine.commands` reply is **554** ids — 484 engine specs plus 70 UI ids, with no id
  in both lists.
- Engine command specs **484, unchanged** — the v0.17.0 tree was extracted and compared with the
  same extraction: 389 literal `cmd!` ids + 94 helper-macro ids (toggle 17 / flag 61 / radio 6 /
  option 10) + 1 direct `CommandSpec` on each side, none added or removed.
- Two registries the skill quotes were re-measured rather than carried: **34** channel formats and
  **512** menu-catalog leaves (parity report 397/512, 77.5 %).
- New at this tag, now documented: complete Grid/Nudge time scales (`clips_markers` for grid only,
  `{"timecode"}` / `{"feet_frames"}` increments, `follow_main`), the nine-page Preferences window
  with only three live controls, WAV bounces stamped with a BWF `bext` TimeReference (and `convert`
  keeping one), the 256 MiB session cap with duplicate-field and duplicate-payload refusals, and
  transient live input toggles.
- Rows whose evidence moved (1, 4, 9) were edited in place; five rows were added for the new
  surfaces. The carried rows (5–8, 10–11) were left exactly as written; none had to be deleted.

## Method

- `git rev-parse HEAD` = `5ff012ab88490cdfc635ee304c1019885e1b880d` (tag `v0.18.0`);
  `git diff v0.17.0..HEAD --stat` = 108 files changed, +6,468/−554. The shallow clone retains the
  v0.17.0 commit object, so the diff and the tag-tree extraction both run locally.
- Counts re-derived with the extraction named in `evidence.md` §5, run against HEAD and against
  `git archive v0.17.0`; the UI id lists were diffed (`comm`) to identify the two additions.
- Every repo path cited in `SKILL.md` was re-resolved against the clone; all exist, none moved.
- The installed bundle was read only through `--version` and `Info.plist` (`soundcraft 0.18.0
  (macos aarch64)`, `ai.storyteller.soundcraft`); the GUI was never launched.

## Unchanged

- 484 engine specs, 17 MCP tools + 2 resources, 17 control methods (+2 aliases), 10 CLI subcommands
  (the CLI gained `commands --json` inside the existing subcommand), 30 built-in plug-ins, 6 write
  extensions, and the craft-libs pin `c5a1cbfb…` for every crate.
- Sections whose code path and count did not move were path-verified at this tag and carried
  forward; the refreshed prose already marks them "unchanged at v0.18.0", and this round re-checked
  those counts rather than re-deriving the sections.

## Known gap in this round

- The 554 figure is arithmetic from the two registries plus an overlap check: `soundcraft-cli` is
  not installed on the authoring machine and the bundle ships only the GUI, so no live
  `engine.commands` reply was observed and no `commands --json` output was captured.
- This was a repair round — `SKILL.md` had already been refreshed by an earlier agent — so the prose
  was verified and re-pinned, not re-derived from scratch for every capability.
