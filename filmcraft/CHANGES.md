# FilmCraft — round 2026-11-07 changes

Re-pinned: v0.17.0 (`eb59ec0`) -> v0.18.0 (`015d5b3`, installed `filmcraft 0.18.0`).

## Corrected / re-measured

- Export presets 42 -> **44**: the two new ones are `H.264 High 10 Master` and `H.264 High 10 Intra`
  (`crates/export/src/presets.rs`, counted as the `p(` entries of `builtin_presets`).
- Engine command registry: **+1 id, none removed** — `presets.scan` ("Scan Preset Library",
  `crates/engine/src/presets.rs`). The old "662 static ids" figure could not be reproduced with any
  method this round (the registry is assembled from ~15 modules that each build `CommandSpec`), so it
  is replaced by the measured id set delta plus the runtime authority (`filmcraft-cli commands`).
- CLI subcommand words **13**, not 12: `exec`, `run`, `commands`, `describe`, `inspect`, `import`,
  `export`, `render`, `probe`, `bench-decode`, `mcp`, `version`, `help` (`apps/filmcraft-cli/src/main.rs`
  HELP + dispatch). The body said 12 while the previous round's delta already said 13.
- Control methods **24** — the body's list omitted `ui.docking`, which exists in the dispatch
  (`crates/ui-egui/src/control.rs`). Unchanged at v0.18.0: that file is not in the diff.
- Built-in workspaces **10**, not 9 (`WORKSPACES: [&str; 10]`, `crates/ui-egui/src/dock.rs`; the tenth
  is Vertical). Unchanged at v0.18.0.
- Workspace shortcuts re-checked and confirmed: `Alt+Shift+1`–`Alt+Shift+8` select Editing, Assembly,
  Color, Effects, Audio, Captions and Graphics, Learning, Review; `Alt+Shift+0` resets; Vertical and All
  Panels have no chord (`crates/ui-egui/src/panels/keyboard.rs`, `crates/ui-egui/src/menus.rs`). The
  published `Alt+Shift+1..8` was right; the skill now names the mapping instead of only the range.
- UI languages **17** = 16 catalogues (`crates/ui-egui/src/i18n/*.tsv`) + English; the body said 12.
  Unchanged at v0.18.0 (existing catalogues were edited, none added).
- Project schema **17** (`assert_eq!(SCHEMA_VERSION, 17)`, `crates/format/src/lib.rs`); the body still
  said "15 at the previous pin". Unchanged at v0.18.0 (`crates/format` is not in the diff).
- craft-libs pin is **`c5a1cbfb…`**, one revision for `craft-docpath`, `craft-media`, `craft-ui`,
  `craft-update` (`Cargo.toml:76-91`). The body's `92d392cf…` was stale; `references/formats.md` said
  `f0ad6c1e…`, also stale.
- H.264 export is no longer 8-bit only: `H264Profile::High10` (10-bit 4:2:0) is wired through the
  built-in encoder, and MXF OP1a writes `profile_idc` 110 (`crates/export/src/settings.rs`,
  `crates/export/src/encoders.rs`, `crates/export/src/mxf_out.rs`). The limitations section now names
  what is still absent (High 4:2:2, High 4:4:4 Predictive, lossless H.264).

Counts that did **not** move at v0.18.0, stated as such in the skill: export formats 21, MCP tools
17 + 2 resources, caption formats 7, panels 28, blend modes 27, camera log curves 10, shortcut
presets 4, schema 17.

## Method

- Audit basis from `git rev-parse HEAD` = `015d5b3ea37e1202a529e6245d3cc021c8c16ffd` (tag `v0.18.0`);
  installed bundle prints `filmcraft 0.18.0` and its `Info.plist` says 0.18.0. The GUI was never
  launched; only `--version` and `Info.plist` reads were used.
- The checkout is a single squashed release commit (`git rev-list --count v0.17.0..HEAD` = 1), so the
  round is measured as a tree diff: `git diff --shortstat v0.17.0..HEAD` = **308 files, +14 708/−1 517**.
- Counts are code reads at this tag, not doc reads: `Format` enum in `crates/export/src/format.rs`
  (21 variants); `builtin_presets` `p(` calls (44); `grep -c '#\[tool('` in
  `crates/automation/src/server.rs` (17); control dispatch arms in `crates/ui-egui/src/control.rs` (24);
  CLI `HELP` + dispatch (`apps/filmcraft-cli/src/main.rs`, 13 words); `ls crates/ui-egui/src/i18n/*.tsv`
  (16) + English; `WORKSPACES: [&str; 10]`; `PanelKind::ALL: [PanelKind; 28]`; captions `Format::ALL:
  [Format; 7]`; `BLEND_MODES` (27); `LogCurve::ALL: [LogCurve; 10]`; `SCHEMA_VERSION` test (17).
- Command-id delta by the same extraction at both tags: first string literal after each `cmd!(`/
  `query!(` plus the first-argument literals in the modules that build `CommandSpec` (tests excluded).
  Set diff v0.17.0 -> v0.18.0: added `presets.scan`, removed nothing. (`json.unreadable` also appears
  as a new dotted literal, but it is a backup-file suffix in `crates/engine/src/presets.rs`, not a
  command.) `camera_keys!` still has one generation site (`crates/engine/src/multicam.rs:132`, 9
  cameras x 2 ids).
- Transitions re-counted as a sanity check: 112 `tr(` definitions = 84 current + 21 Legacy + 7
  Obsolete in 10 current folders (`crates/project/src/vtransition.rs`); the skill's "84 + 21 Legacy"
  wording still holds.
- Every repo path cited in `SKILL.md` and `evidence.md` was re-resolved against this checkout.

## Unchanged

- The import/export format tables, the automation surface (MCP, control, CLI), the project format,
  proxies/Project Manager, and the limitation list (no `.prproj`, no plug-ins, no AV1 encoder, DNG-only
  raw, no captions in the video stream, no Production model) — path-verified at this tag and carried
  forward, not re-dated.
- Effect catalogue totals (93 video / 16 folders, 53 audio, 84 + 21 transitions, 27 blend modes, 10 log
  curves) are carried: the modules that define them (`crates/project/src/effect.rs`,
  `crates/project/src/effect/`, `crates/project/src/vtransition.rs`, `crates/color/src/log.rs`) are not
  in the round's diff. Blend modes and transitions were re-counted as spot checks and match.

## Known gap in this round

- Pin-and-verify, not a fresh audit: deep feature prose was carried after path checks, not re-derived
  from code statement by statement.
- No runtime command enumeration: the macOS bundle ships only the GUI binary, so `filmcraft-cli
  commands` was not run and the registry total is a static measure. Effect/transition catalogue totals
  were spot-checked, not enumerated.
- The GUI was not launched, so panel/workspace behaviour is read from code, not observed.
