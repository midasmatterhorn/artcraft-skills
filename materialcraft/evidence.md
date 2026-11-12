# MaterialCraft — evidence map (v0.4.1, re-pinned audit)

Audit basis: tag `v0.4.1`, commit `65f7bfd3e5f40d695d03162285879f0f8079ff6c`, inspected
2026-11-12. `git rev-parse HEAD` confirms. Supersedes the v0.2.0 map
(`a1bbd4a83f62365d90f085e5f1ad61410f9cf11c`, 2026-11-07). Every count below names how it was
measured in this checkout; none is copied from the app's docs.

**Round 2026-11-12.** Delta measured from `git diff v0.2.0..HEAD` (434 files, +28 465/−3 661; the
checkout has both tags but a squashed history, so this is a tree diff). The container formats, the
command registry, the library, the export surface and the app shell moved, so most rows and the
whole count table were re-derived. Rows whose code path is the same file and the same shape are
carried forward and say so. Unexercised UI behaviour stays labelled, not upgraded.

| # | Claim | Evidence | Tier |
|---:|---|---|---|
| 1 | 119 engine command ids over 37 registry modules (was 86 over 19 at v0.2.0): graph 65, edit 13, file 13, view 8, library 6, folder 5, session 3, package 3, explorer 3 | `crates/engine/src/commands.rs` `command_specs()` aggregates the 37 modules; `cmd!` literal ids in exactly those modules (119 occurrences, 119 unique) | implemented |
| 2 | 11 CLI subcommands — unchanged at v0.4.1 | `apps/materialcraft-cli/src/main.rs` `SUBCOMMANDS`: info, commands, nodes, run, batch, new, cook, export, render, mcp, serve | implemented |
| 3 | 20 MCP tools — unchanged at v0.4.1 | `crates/automation/src/server/material_craft_mcp.rs`: `#[tool(...)]` followed by `async fn` (20) | implemented |
| 4 | 12 JSON-lines methods — unchanged at v0.4.1 | `crates/automation/src/rpc.rs` `METHODS` literal slice (12) | implemented |
| 5 | Control channel: `auth` first, token from env or owner-only token file, one attempt in 10 s, 16 connections, 8 MiB requests, 256 batch steps | `crates/automation/src/security.rs` `AUTH_TIMEOUT`, `MAX_CONNECTIONS`, `MAX_REQUEST_BYTES`, `MAX_BATCH_STEPS`; `apps/materialcraft/src/control_server.rs` | implemented |
| 6 | Native `.sbs` (XML + adjacent `resources/`) **and** native `.mcraft` ZIP (one root SBS `package.sbs` + `resources/`, no manifest) | `crates/formats/src/sbs/`, `crates/formats/src/project.rs` (`EXT`, `SBS_ENTRY`, `is_archive`, `read`), `crates/formats/src/project/project_files.rs`; `crates/formats/tests/project_packages.rs`; `file.save` doc in `crates/engine/src/file_cmds.rs` | implemented |
| 7 | Save picks the container from the path; Save As offers SBS and MaterialCraft Project separately; autosaves are `.mcraft` | `crates/engine/src/file_cmds.rs` `is_mcraft` / `write_package_at`; `crates/ui-egui/src/windows.test.rs` `package_filters`; `crates/ui-egui/src/material_craft_app.rs` autosave path | implemented |
| 8 | Cross-package references serialize as `mcraft://<identity>!/…`; archives validate traversal, duplicates and symlinks | `crates/formats/src/project.rs` `resolve`, `read`; `crates/formats/tests/project_packages.rs` | implemented |
| 9 | Multi-package sessions: activate/close/closeAll, per-package undo and selection, `session.inspect.documents` | `crates/engine/src/package_commands.rs`; `crates/engine/src/session.rs`; `crates/engine/src/inspect.rs` | implemented |
| 10 | Linked graph instances across open packages: requires a source output, rejects cycles, stores a file reference plus connector metadata | `crates/engine/src/graph_instance_commands.rs` (`graph.instance.add`, `reference`), `crates/engine/src/linked_packages.rs` | implemented |
| 11 | Explorer folders, resources and clipboard; empty folders persist as SBS groups; root Resources is reserved | `crates/engine/src/{folder_commands,folder_property_commands,explorer_clipboard_commands}.rs`; `crates/formats/tests/explorer_folders.rs`; `docs/architecture.md` "Files" | implemented |
| 12 | 29 catalog entries: 24 `Atomic nodes` + 5 `Graph items`, `motion_blur` removed | `crates/nodes/src/atomic/catalog.rs::defs()`; category constants `ATOMIC` / `GRAPH_ITEMS` in `crates/nodes/src/atomic/mod.rs` | implemented |
| 13 | 85 function operations (categories: Function 18, Vector 14, Variables 12, Constant 10, Operator 8, Cast 8, Comparison 6, Control 4, Logical 3, Samplers 2) — unchanged at v0.4.1 | `crates/nodes/src/function/catalog.rs` `FUNCTIONS` (85 entries, 85 unique ids) | implemented |
| 14 | 4 pattern nodes: Quadrant (`paramset`), Switch (`markov2`), Iterate (`addnode`), Dot (`passthrough`) — unchanged at v0.4.1 | `crates/nodes/src/pattern/catalog.rs`; `crates/core/src/pattern_node_kind.rs` `ALL` | implemented |
| 15 | 171 reusable SBS function graphs / 2 334 function nodes bundled; listed by `library.functions`, inserted by `library.function.add` | `assets/sbs/functions.sbs` (`<function>` = 171, `<paramNode` = 2 334), asserted in `crates/formats/tests/function_library.rs`; `crates/engine/src/function_library_commands.rs`; default package `sbs://functions.sbs` in `crates/engine/src/function_library.rs` | implemented |
| 16 | Library tree with `missing` entries and a destination canvas; `library.add` inserts native nodes, graph items, functions and patterns | `crates/engine/src/node_library_commands.rs`; `crates/engine/src/node_library.rs` `CATEGORIES`; `docs/control-protocol.md` "Node library" | implemented |
| 17 | Map export: 7 formats (png, jpg, tga, bmp, webp, exr, hdr), depths 8/16/32; TIFF is import-only | `crates/formats/src/lib.rs` `EXPORT_FORMATS`; `crates/formats/src/image.rs` `encode` match; `docs/file-format-parity.md` TIFF row | implemented |
| 18 | Import: 16 bitmap extensions (DDS, WebP, GIF, HDR, EXR, JPEG/JIF/JPE, PGM, PNG, TIFF, TGA/TARGA, BMP) plus SVG vectors | `BITMAP_EXTENSIONS`, `VECTOR_EXTENSIONS` in `crates/formats/src/lib.rs`; `crates/formats/src/image.rs` `decode`; `crates/formats/src/dds_image.rs`; `docs/architecture.md` "Files" (GIF first frame, DDS largest mip) | implemented |
| 19 | Export `outputs`, `colorSpaces` (srgb/linear/raw) and `size` as px or `[w,h]`; colliding names rejected | `crates/engine/src/export_request.rs`; `crates/engine/src/color_space.rs`; `file.export` param doc + duplicate-name error in `crates/engine/src/file_cmds.rs` | implemented |
| 20 | Export window has From graph / Batch / MaterialX / MCMAT tabs; MaterialX and MCMAT are explicitly unavailable; DDS is listed as planned | `crates/ui-egui/src/export/export_settings.rs` `ALL`; `crates/ui-egui/src/export/export_format.rs` `PLANNED`; `crates/ui-egui/src/export/mod.rs` toasts | partial |
| 21 | `.mcmat`: zip `material.json` (`craft-material`, **version 2**) + `maps/<usage>.png` + `source.sbs`; version-1 rejected; 9 usages | `crates/formats/src/material/archive.rs` (`FORMAT`, `VERSION = 2`, `SOURCE`), `crates/formats/src/material/map_entry.rs` usage doc; read path in `crates/engine/src/file_cmds.rs` loads the source package | implemented |
| 22 | 3D view: 7 scenes, 4 environment ids, CPU displacement of a subdivided mesh (not parallax), still no GPU path | `crates/engine/src/view_cmds.rs` `SCENES` and `view.3d` doc; `crates/render/src/preview.rs` `Scene::displaced`; `crates/render/src/ibl.rs` environment mapping; no wgpu use under `crates/render` | implemented |
| 23 | 3D material assignment: `view.3d.assign` / `view.3d.outputs` / `view.3d.clear` map any image output to a PBR channel | `crates/engine/src/material_preview_commands.rs`; `docs/architecture.md` "The UI" | implemented |
| 24 | Preview size: UI offers 256–4096 px or Full; `view.previewSize` clamps 64..8192 | `crates/ui-egui/src/preview_resolution.rs` `SIZES`; `crates/engine/src/view_cmds.rs` `preview_size` | implemented |
| 25 | Undo limit preference 1–10 000 (default 200) via `session.history`; `edit.undo/redo {document?}` | `crates/engine/src/history_prefs.rs`; `crates/engine/src/document_history_commands.rs` | implemented |
| 26 | Host evaluation values without touching the package (`session.environment`) and graph context metadata (`graph.context`) | `crates/engine/src/evaluation_environment_commands.rs`; `crates/engine/src/graph_property_commands.rs`; `docs/control-protocol.md` "Key commands" | implemented |
| 27 | 3 graph templates (`empty`, `pbr`, `atomics`) — unchanged at v0.4.1 | `crates/engine/src/samples.rs` `TEMPLATES` | implemented |
| 28 | 2 UI locales, English and Arabic (RTL) — unchanged at v0.4.1 | `crates/ui-egui/src/i18n.rs` `LANGUAGES`; `crates/ui-egui/src/i18n/ar.rs` | implemented |
| 29 | Self-update from Help → Check for updates…; installed bundle signed, notarized and stapled | `crates/ui-egui/src/menus.rs` `ui.help.checkForUpdates`; `crates/ui-egui/src/updates_ui.rs`; `crates/ui-egui/src/lib.rs` `UPDATE_APP`; `codesign -dv` / `spctl -a -vv` on the installed app | implemented |
| 30 | Headless path confinement: files only below the read/write roots; path-taking `file.*` refused through `command.run` | `crates/automation/src/workspace.rs` `authorize_command` and path validation; `crates/automation/src/filesystem.rs`; `crates/automation/src/rpc.rs` test at the `command.run` boundary | implemented |
| 31 | SBS import is not a lossless importer for arbitrary files; unsupported parameters warn and missing nodes stay placeholders | `docs/atomic-workflow.md` "Current limits"; `crates/core/src/missing_node.rs`; `crates/formats/src/sbs/sbs_reader.rs` | claimed |
| 32 | Reference-application reopen and numerical parity unverified | `ROADMAP.md`; `docs/atomic-workflow.md` "Current limits" | claimed |
| 33 | No mesh-based generators or bakers; no visibility conditions; no minimap, graph tabs or keymap editor | `docs/target-app-parity.md` gap rows; zero `minimap` / `visibility` hits under `crates/`; `ui.help.shortcuts` only | claimed |
| 34 | Text uses the built-in stroke font; external fonts error; SVG is vector geometry only | `docs/atomic-workflow.md` "Current limits"; `crates/nodes/src/atomic/{text,svg}.rs` | claimed |
| 35 | `ui.screenshot` may time out on the window-capture callback | `docs/gaps.md` #7 — not retested this round | claimed |
| 36 | Explorer has disabled dependency rows: `Link ▸ Bitmap/Vector graphics`, `Export with dependencies…`, `Dependency manager…` (empty command ids); `Open dependencies`, `Export material…` and `Show in folder…` work | `crates/ui-egui/src/menus.rs` `EXPLORER_LINK` / `EXPLORER_PACKAGE`; `docs/gaps.md` "Explorer" paragraph | implemented |

## Headline count table

| Count | v0.1.0 | v0.2.0 | v0.4.1 | Method |
|---|---:|---:|---:|---|
| Engine command ids | 68 | 86 | **119** | `cmd!(` literal ids over the modules in `command_specs()` |
| Command registry modules | 6 | 19 | **37** | `crate::*::specs()` lines in `crates/engine/src/commands.rs` |
| CLI subcommands | 11 | 11 | **11** (unchanged) | `apps/materialcraft-cli/src/main.rs` `SUBCOMMANDS` |
| MCP tools | 19 | 20 | **20** (unchanged) | `#[tool(…)] async fn` in `crates/automation/src/server/material_craft_mcp.rs` |
| JSON-lines methods | 11 | 12 | **12** (unchanged) | `crates/automation/src/rpc.rs` `METHODS` |
| Catalog entries | — (227 "nodes" was a different, retired library) | 30 (25 + 5) | **29** (24 atomic + 5 graph items) | `crates/nodes/src/atomic/catalog.rs::defs()` + category constants |
| Function operations | — | 85 | **85** (unchanged) | `crates/nodes/src/function/catalog.rs::FUNCTIONS` |
| Pattern kinds | 1 | 4 | **4** (unchanged) | `crates/nodes/src/pattern/catalog.rs` / `PatternNodeKind::ALL` |
| Bundled reusable functions | — | 0 | **171** (2 334 nodes) | `assets/sbs/functions.sbs` + `crates/formats/tests/function_library.rs` |
| Templates | 12 | 3 | **3** (unchanged) | `crates/engine/src/samples.rs::TEMPLATES` |
| 3D scenes | 7 | 7 | **7** (unchanged) | `crates/engine/src/view_cmds.rs::SCENES` |
| 3D environments | 4 | 4 | **4** (unchanged) | `view.3d` environment ids |
| `.mcmat` map usages | 9 | 9 | **9** (unchanged) | `crates/formats/src/material/map_entry.rs` usage doc |
| `.mcmat` manifest version | 1 | 2 | **2** (unchanged) | `crates/formats/src/material/archive.rs::VERSION` |
| Export formats | 8 | 8 | **7** (TIFF import-only) | `crates/formats/src/lib.rs` `EXPORT_FORMATS` + `encode` |
| Image extensions (read) | 10 | 11 | **17** (16 bitmap + svg) | `crates/formats/src/lib.rs` `IMAGE_EXTENSIONS` / `BITMAP_EXTENSIONS` + `VECTOR_EXTENSIONS` |
| UI locales | 1 | 2 | **2** (unchanged) | `crates/ui-egui/src/i18n.rs` language table |
| Native project containers | `.sbs` | `.sbs` | **`.sbs` + `.mcraft`** | `crates/formats/src/project.rs`, `crates/engine/src/file_cmds.rs` |

## Drift notes

- `docs/atomic-workflow.md` "Files and execution" still says `.mcraft` read/write support has been
  removed. The code, `docs/architecture.md` and the Save As dialog say otherwise; code wins.
- `docs/atomic-workflow.md` "Catalog" says 26 native primitives + 4 input/output items;
  `ROADMAP.md` says the same; `docs/architecture.md` says 30 main-graph entries. Measured:
  **24 + 5 = 29** (motion blur deleted). The totals disagree; the measured split is used.
- `apps/materialcraft-cli/src/main.rs` `USAGE` lists `tif` among export formats; `EXPORT_FORMATS`
  and `image::encode` do not accept it. Import-only since v0.4.1.
- `docs/control-protocol.md` `file.new` still lists the retired template ids (`bricks`,
  `stone_tiles`, `wood`, `rusty_metal`, `fabric`, `ground`); `TEMPLATES` is `empty`, `pbr`,
  `atomics`.
- `docs/gaps.md` and `docs/target-app-parity.md` carry their own historical headers (they predate
  the 2026-11-05 primitive rewrite). Their gap #1 (227 nodes), #4 (missing `material_export`),
  #5 (function loops / reusable functions) and #10 (first signed release) no longer describe the
  code; #2, #3, #6, #7, #8 and #9 still roughly do. `docs/gaps.md` #7 is not retested here.
- `docs/file-format-parity.md` describes the older `.mcraft` as `package.json` + `resources/`;
  the current archive is one root SBS (`package.sbs`) + `resources/`, per
  `crates/formats/src/project.rs`.
- `ROADMAP.md` retires all earlier percentage estimates; the skill quotes no parity percentage.
- `docs/control-protocol.md` header still says "Last updated 2026-11-03" while describing commands
  added later (`session.history`, `folder.*`, `graph.instance.add`); the code is the contract.

## Not measured

- Runtime behaviour: cook times, render quality, the Explorer tree, docking, self-update prompt,
  Export tabs, undo-limit preference, function editor, RTL layout, `.mcmat` read/write — no GUI,
  no build and no test run. Only the installed GUI binary's `--version` and `--help` were executed.
- The installed bundle ships no separate `materialcraft-cli`, so CLI counts and help text come
  from source.
- The SBS library package was counted structurally (`<function>` 171, `<paramNode` 2 334), not
  evaluated in the reference application.
