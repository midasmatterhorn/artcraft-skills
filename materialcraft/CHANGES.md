# MaterialCraft — round 2026-11-12 changes

Re-pinned **v0.2.0** (`a1bbd4a83f62365d90f085e5f1ad61410f9cf11c`) → **v0.4.1**
(`65f7bfd3e5f40d695d03162285879f0f8079ff6c`); the installed bundle's own binary prints
`MaterialCraft 0.4.1 (65f7bfd 2026-11-12)` and `git rev-parse HEAD` in the pinned checkout
matches the tag commit. Delta measured from `git diff v0.2.0..HEAD` — **434 files, +28 465 /
−3 661**. The checkout carries both tags but a squashed history, so this is a tree diff, not a
replay of the commits between the releases.

## Corrected / re-measured

- **`.mcraft` is a native format again — and it is not the old package.** The v0.2.0 skill said
  `.mcraft` support was removed. v0.4.1 reads and writes a *MaterialCraft Project* ZIP that holds
  exactly one root SBS (`package.sbs`) plus `resources/`, with no manifest and no private graph
  payload (`crates/formats/src/project.rs`, `crates/formats/src/project/project_files.rs`; asserted
  in `crates/formats/tests/project_packages.rs`). `file.save` / `file.saveAs` / `file.saveCopyAs`
  pick the container from the path (`crates/engine/src/file_cmds.rs` `is_mcraft`,
  `write_package_at`), Save As offers "SBS XML Package (*.sbs)" and "MaterialCraft Project
  (*.mcraft)" separately (`crates/ui-egui/src/windows.test.rs`), and autosaves are `.mcraft`
  (`crates/ui-egui/src/material_craft_app.rs`). `docs/architecture.md` agrees with the code;
  `docs/atomic-workflow.md` still says support was removed — stale doc, recorded as drift.
- **Engine command registry: 86 → 119 ids over 37 modules (was 19).** New namespaces appear:
  `package.*` (3), `folder.*` (5), `explorer.*` (3); `library.*` grew 1 → 6, `graph.*` 53 → 65,
  `file.*` 10 → 13 (`crates/engine/src/commands.rs` `command_specs()`; ids by `cmd!` literals in
  exactly those modules). The full list moved to `references/commands.md`.
- **Node catalog: 30 → 29 entries** — 24 `Atomic nodes` + 5 `Graph items`
  (`crates/nodes/src/atomic/catalog.rs::defs()`); `motion_blur` was deleted
  (`git diff` shows `D crates/nodes/src/atomic/motion_blur.rs`). `ROADMAP.md` (26 + 4) and
  `docs/architecture.md` (30) both disagree with the code; the measured split is used here.
- **Map export: 8 → 7 formats.** TIFF is import-only now; `EXPORT_FORMATS` is png, jpg, tga, bmp,
  webp, exr, hdr (`crates/formats/src/lib.rs`; `encode` in `crates/formats/src/image.rs` rejects
  anything else). The CLI usage text still advertises `tif` (`apps/materialcraft-cli/src/main.rs`)
  — doc drift; the engine refuses it.
- **Image import widened to 17 extensions** (16 bitmap + `svg`): DDS, WebP, GIF, HDR, EXR,
  JPEG/JIF/JPE, PGM, PNG, TIFF, TGA/TARGA, BMP (`BITMAP_EXTENSIONS`), SVG vectors
  (`VECTOR_EXTENSIONS`), decoded in `crates/formats/src/image.rs` with DDS in
  `crates/formats/src/dds_image.rs` (first frame of a GIF, largest mip of a DDS).
- **Export gained output selection and colour spaces.** `file.export` takes `outputs` (identifiers)
  and `colorSpaces` (`srgb|linear|raw` per output) and a `size` that is either the larger side or
  `[width, height]` (`crates/engine/src/export_request.rs`, `crates/engine/src/color_space.rs`).
  The UI Export window has four tabs — From graph, Batch, MaterialX, MCMAT — where MaterialX and
  MCMAT report "not available yet" (`crates/ui-egui/src/export/`).
- **The 3D view displaces real geometry.** The v0.2.0 wording ("CPU renderer with parallax") was
  inaccurate: `Scene::displaced` subdivides the mesh up to a triangle budget and moves vertices along
  their normals by `height − level` (`crates/render/src/preview.rs`). It is still a CPU renderer;
  `crates/render` has no wgpu path.
- **Several packages can be open, and graphs can be linked across them.** `package.activate`,
  `package.close`, `package.closeAll`, `session.inspect.documents`, and `graph.instance.add` /
  `graph.instance.reference` for a graph in another open package (requires a source output,
  rejects dependency cycles) —
  `crates/engine/src/{package_commands,graph_instance_commands,linked_packages}.rs`.
- **Reusable SBS functions shipped.** `assets/sbs/functions.sbs` bundles **171 function graphs and
  2 334 function nodes**, asserted in `crates/formats/tests/function_library.rs`; agents list them
  with `library.functions` and insert them with `library.function.add` (default package
  `sbs://functions.sbs`, `crates/engine/src/function_library.rs`). `library.tree` / `library.add`
  expose the whole category tree, including entries that are `missing`.
- **Explorer became a package browser.** Folders, resources, clipboard and context menus:
  `folder.create/rename/remove/attributes/properties`, `explorer.copy/paste/move`, empty folders
  persisted as SBS groups (`crates/engine/src/{folder_commands,explorer_clipboard_commands}.rs`;
  `crates/formats/tests/explorer_folders.rs`).
- **Undo is configurable.** `session.history {undoLimit?}` sets retained steps per package,
  1–10 000, default 200 (`crates/engine/src/history_prefs.rs`,
  `crates/engine/src/document_history_commands.rs`); `edit.undo` / `edit.redo` accept
  `{document?}`.
- **Self-update and a signed macOS build.** Help → Check for updates… (`ui.help.checkForUpdates`,
  `crates/ui-egui/src/updates_ui.rs`, `craft-update`). The installed bundle is Developer ID-signed,
  notarized and stapled, and `spctl` reports "accepted / Notarized Developer ID", so the old
  "no signed/notarized release" limitation is deleted.
- **Shared UI moved to craft-libs.** `craft-ui` (docking/widgets), `craft-keymap`, `craft-dialogs`,
  `craft-update`, `craft-quit`, `craft-window`, `craft-menu`, all pinned to one rev in
  `Cargo.toml`; the dock hosts eight panels including Console and History
  (`crates/ui-egui/src/docking.rs`). Still egui/eframe: no Tauri, Electron or webview.
- **MCP tools (20) and JSON-lines methods (12) are unchanged at v0.4.1** — now stated with the
  version instead of as an undated sentence. The eight app-only control methods are likewise
  unchanged at v0.4.1.
- **CLI subcommands unchanged at 11**, but the export/render/mcp/serve flags grew and root aliases
  were added (`apps/materialcraft-cli/src/main.rs` `SUBCOMMANDS`).

## Method

Read-only: `git show`, `git diff`, `git rev-parse`, code parses, and the installed bundle's
`--version` / `--help` only. No GUI launch, no build, no test run. Counts by source parse:

| Count | How |
|---|---|
| 119 engine commands | Perl `cmd!\(\s*"(id)"` over the 37 modules named in `commands.rs::command_specs()`, deduped (119 occurrences, 119 unique) |
| 20 MCP tools | `#[tool(...)]` immediately followed by `async fn` in `crates/automation/src/server/material_craft_mcp.rs` |
| 12 JSON-lines methods | literal entries of `METHODS` in `crates/automation/src/rpc.rs` |
| 11 CLI subcommands | `SUBCOMMANDS` slice in `apps/materialcraft-cli/src/main.rs` |
| 29 catalog entries | `atomic::defs()` list, categorised by the `ATOMIC` / `GRAPH_ITEMS` constant in each `node(...)` call |
| 85 function operations | entries of `FUNCTIONS` in `crates/nodes/src/function/catalog.rs` (85 unique ids) |
| 4 pattern kinds | `crates/nodes/src/pattern/catalog.rs` + `PatternNodeKind::ALL` |
| 171 functions / 2 334 nodes | `<function>` and `<paramNode` counts in `assets/sbs/functions.sbs`, matching the assertions in `crates/formats/tests/function_library.rs` |
| 3 templates, 7 scenes, 4 environments, 2 locales, 9 map usages | `crates/engine/src/samples.rs` `TEMPLATES`; `crates/engine/src/view_cmds.rs` `SCENES`; the `view.3d` environment ids; `crates/ui-egui/src/i18n.rs` language table; `crates/formats/src/material/map_entry.rs` usage doc |
| 7 export formats / 17 image extensions | `EXPORT_FORMATS`, `IMAGE_EXTENSIONS`, `BITMAP_EXTENSIONS`, `VECTOR_EXTENSIONS` in `crates/formats/src/lib.rs` |
| `.mcmat` version 2 | `crates/formats/src/material/archive.rs` `VERSION`, `SOURCE`, read-path version check |
| signed bundle | `codesign -dv` / `spctl -a -vv` on the installed app (read-only) |

## Unchanged

- 11 CLI subcommands — same 11 ids at v0.4.1 (`info`, `commands`, `nodes`, `run`, `batch`, `new`,
  `cook`, `export`, `render`, `mcp`, `serve`); only flags grew.
- 20 MCP tools, 12 JSON-lines methods, 8 app-only control methods, and the token handshake
  (one auth attempt in 10 s, 16 connections, 8 MiB requests, 256 batch steps).
- 9 `.mcmat` map usages; manifest version 2 with `source.sbs`; version-1 archives still rejected.
- 7 built-in 3D scenes and 4 environment ids (`studio`, `sunset`, `overcast`, `night`).
- 3 graph templates (`empty`, `pbr`, `atomics`); 85 function operations; 4 pattern kinds.
- 2 UI locales (English, Arabic RTL).
- Headless path confinement (`--read-root` / `--write-root`, aliases `--automation-*`),
  `MATERIALCRAFT_NO_PREFS=1`, the `.mcmat` ↔ TextureCraft contract, and the wasm build.

## Known gap in this round

No GUI and no build: the Explorer tree, docking layout, self-update prompt, Export window tabs,
undo-limit preference, function editor and RTL layout are verified by code paths only. The
`ui.screenshot` timeout (`docs/gaps.md` #7) was not retested and stays a repo claim. `.mcmat`
read/write was not exercised, only parsed. The installed bundle ships only the GUI binary — there
is no `materialcraft-cli` on this machine, so CLI counts come from source and only the GUI
binary's `--version` / `--help` were run.
