# VectorCraft — evidence ledger (tag v0.18.0)

Audit basis: this checkout is tag **`v0.18.0`**, commit **`68b68a30acad9b3d8a72802b35f43b82e2bd7d3a`** ("Release
0.18.0", shallow clone). Inspection date **2026-10-29**. Installed `/Applications/VectorCraft.app` reports 0.18.0
(`CFBundleIdentifier ai.storyteller.vectorcraft`), binary prints `vectorcraft 0.18.0`; the GUI was never launched.
No `references/` directory.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 801 engine `cmd!` entries | `grep -rho 'cmd!' crates/engine/src/ \| wc -l` = 801 (was 789 at v0.17.0) | implemented |
| 2 | 374 UI commands, unique ids | `crates/ui-egui/src/menus/ui_commands.rs` (`pub use ui_commands::UI_COMMANDS` at `menus.rs:80`); 374 rows counted; set diff vs v0.17.0 not taken row-by-row — +31 net (saved views, brush libraries, artboard lock/unlock, Transform panel, docking) | implemented |
| 3 | 33 MCP tools; `answer_dialog` new; undo/redo single-line defs | `crates/mcp/src/tools/definitions.rs`: 31 `"name",` rows + `tool("undo"…)`/`tool("redo"…)` at `:509-510`; `answer_dialog` at `:303` (tests `crates/mcp/src/tests.rs:764`) | implemented |
| 4 | 5 prompts (poster, brief, palette, text, subject); 3 fixed resources + 5 URI templates (+`object/{lid}`) | `crates/mcp/src/prompts.rs` `PROMPTS` (5 `PromptDef`); `crates/mcp/src/resources.rs` URIs | implemented |
| 5 | 29 control methods (30 with `command` alias); `ui.docking` new; `ui.dialog.set` errors on unknown field | `crates/ui-egui/src/control.rs` match arms — 29 distinct; `ui.docking` arm present; PR #4049 | implemented |
| 6 | 9 browser API calls | `apps/vectorcraft-web/src/api.rs` `install` | implemented |
| 7 | 31 `OPEN_EXTS`; Place +`.txt/.rtf/.docx` | `crates/engine/src/cmd/fileio/formats.rs:473` (31 quoted entries; moved from `fileio/mod.rs` in the shared-module refactor) | implemented |
| 8 | 6 `SAVE_FORMATS`; `TEMPLATE_FORMATS` = template, ait; native v4 | `crates/engine/src/cmd/fileio/save.rs`; `crates/format/src/lib.rs:53` `VERSION: u32 = 4` | implemented |
| 9 | Effect catalogue 116 = 86 literal + 15 warps + 12 Pathfinder + Trap + Crop Marks + Rasterize | `crates/effects/src/catalog.rs:144` `effect_catalog()` (86 `g(`/`r(` entries), `WARP_STYLES` `[(&str,&str); 15]` at `:125`, `crates/effects/src/group.rs:24` `PATHFINDER_EFFECTS: 12` | implemented |
| 10 | 57 Photoshop-style raster filters | `crates/effects/src/pixel/mod.rs` `PIXEL_EFFECTS` (56) + `blur.gaussian` | implemented |
| 11 | 94 tool ids | `crates/tools/src/catalog.rs` `t(` entries = 94 (was 92) | implemented |
| 12 | Panels on craft-ui docking; 36 `ICON_PANELS` entries | `crates/ui-egui/src/state.rs:160`; `crates/ui-egui/src/panel_docking.rs` | implemented |
| 13 | 25 languages (24 tsv + English) | `ls crates/ui-egui/src/i18n/` = 24 `.tsv` | implemented |
| 14 | `.ai` blends import live; editing data ≤512 MiB on 64-bit; convert-to-PDF omits editing data by default | PRs #4127/#4234, #4177, #4147; `crates/engine/src/cmd/fileio/` readers | implemented |
| 15 | Type auto lists; Convert to Text; PDF list markers selectable; ruby round-trips | PRs #4192, #4093, #4098; `crates/engine/src/cmd/typecmd.rs` | implemented |
| 16 | Pen/path.join compound-path join/close; Ctrl+J two-path join | PR #3283 (M2.1), #4187 | implemented |
| 17 | Brush Libraries window; New Brush from art; pressure width; eraser tip | PRs #4020, #4195, #4181, #4180 | implemented |
| 18 | Grid Repeat on-canvas handles; artboard lock/unlock + Delete Empty Artboards; 25 saved views listed | PRs #4166, #2532, #4142, #4247 | implemented |
| 19 | Startup update prompt + self-update (craft-update); Windows per-user policy | PRs #4138, #4295; `Cargo.toml` craft pins | implemented |
| 20 | No reference-app scripting; `.jsx` static check only; no generative AI | `crates/scriptcheck/`; `docs/gaps.md` G18 | not implemented (verified absent) |

## 2. Automation-surface counts: v0.17.0 → v0.18.0

| Surface | v0.17.0 | v0.18.0 (measured) | Change |
|---|---:|---:|---|
| Engine `cmd!` entries | 789 | **801** | +12 |
| UI commands | 343 | **374** | +31 |
| MCP tools | 32 | **33** | +`answer_dialog` |
| MCP prompts | 5 | **5** | unchanged |
| MCP resources | 3 fixed + 4 templates | **3 + 5** | +`vectorcraft://object/{lid}` |
| Control methods | 28 (29 w/ alias) | **29 (30 w/ alias)** | +`ui.docking` |
| CLI subcommands | 7 | **7** | unchanged |
| Browser API | 9 | **9** | unchanged |
| Open extensions | 31 (+3 Place) | **31 (+3)** | unchanged |
| Save formats | 6 | **6** | unchanged |
| Writable formats | 20/19 + plug-ins; catalogue 24 (22 readable) | **same** | unchanged |
| Photoshop-style filters | 57 | **57** | unchanged |
| Effect catalogue | 116 | **116** | unchanged |
| Tools | 92 | **94** | +2 |
| Panels | 42 modules (old dock) | **36 `ICON_PANELS` + dock tabs** | reorganized onto craft-ui docking |
| Languages | 25 | **25** | unchanged |
| Native format version | 4 | **4** | unchanged |

## 3. Uncertain / not verified

- The exact 31 added UI-command ids were not individually enumerated (net count measured); the live registry
  (`vectorcraft-cli commands`) is the authority.
- GUI behaviour not launched; registry + docs + packaging are the evidence.
- Parity percentages remain project self-assessments.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `ROADMAP.md` 348/375 menus, 46/50 effects, 74% localization | `docs/target-app-parity.md` 353/375, `docs/effects-parity.md` conflicting totals, measured ~82% localization |
| `docs/file-format-parity.md` "PS missing" | `.ps` in `OPEN_EXTS` |
| `README.md` "What's missing" lists Variables image/graph + 3D beyond Revolve | `dataset.import`, all 4 `VariableKind`s, Extrude & Bevel/Inflate/Rotate ship (materials do not) |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # 68b68a30acad9b3d8a72802b35f43b82e2bd7d3a
grep -rho 'cmd!' crates/engine/src/ | wc -l                     # 801
awk '/pub (static|const) UI_COMMANDS/,/^];/' crates/ui-egui/src/menus/ui_commands.rs | grep -cE '^\s+(UiCommand|\()'   # 374
grep -cE '^\s+"[a-z_]+",$' crates/mcp/src/tools/definitions.rs  # 31 (multi-line tool names)
grep -c 'tool("' crates/mcp/src/tools/definitions.rs            # single-line defs (undo, redo, …) → 33 total
awk '/pub static PROMPTS/,/^];/' crates/mcp/src/prompts.rs | grep -c 'PromptDef {'   # 5
grep -oE '^\s+"[a-z]+\.[a-zA-Z.]+".*=>' crates/ui-egui/src/control.rs | grep -oE '"[^"]+"' | sort -u | wc -l  # 29
grep -oE 't\("' crates/tools/src/catalog.rs | wc -l             # 94
sed -n '473,505p' crates/engine/src/cmd/fileio/formats.rs | grep -oE '"[a-z0-9]+"' | wc -l  # 31
awk '/pub fn effect_catalog/,0' crates/effects/src/catalog.rs | grep -cE '^\s+(g|r)\('      # 86 (+15 warps +12 pathfinder)
ls crates/ui-egui/src/i18n/ | grep -c tsv                       # 24 (+English)
```
