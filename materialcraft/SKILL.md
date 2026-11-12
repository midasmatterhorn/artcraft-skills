---
name: materialcraft
description: >
  MaterialCraft is the ArtCraft team's open-source, pure-Rust node-based procedural material designer —
  build tileable PBR materials from native primitives, functions and a 171-function SBS library in a node
  graph, watch them cook in 2D and on a displaced 3D model, and export the maps for any engine. Its native
  documents are SBS XML packages (`.sbs`) and self-contained MaterialCraft Project archives (`.mcraft`);
  portable `.mcmat` materials let TextureCraft paint with the result. Trigger this skill whenever the user
  mentions MaterialCraft — or an `.sbs`, `.mcraft` or `.mcmat` material — asks what it can or cannot do,
  which primitives or bundled functions exist, how to script, automate, batch or headlessly drive it
  (`materialcraft-cli`, MCP, the JSON control channel), wants a tileable PBR material built or exported,
  wants an SBS graph imported or a material handed to TextureCraft, needs exported maps or a project
  archive verified, or troubleshoots it. Also when the job is described without naming the app — "make me
  a tileable brick material", "export base color/normal/roughness maps", "build this material as a node
  graph", "open this SBS file", "package this project as one file", "share this material with my texturing
  app". Do not guess its node library, command ids or parameters — read this, then ask the app.
---

**Audit basis.** Re-pinned 2026-11-12 against tag **v0.4.1**, commit
**`65f7bfd3e5f40d695d03162285879f0f8079ff6c`** — `git rev-parse HEAD` in the pinned checkout
confirms — and the installed bundle matches (its binary prints
`MaterialCraft 0.4.1 (65f7bfd 2026-11-12)`; bundle `0.4.1`, id `ai.storyteller.materialcraft`).
This supersedes the v0.2.0 audit (`a1bbd4a83f62365d90f085e5f1ad61410f9cf11c`, 2026-11-07). Every
count below was re-measured from this tree (the method is in `evidence.md`); the app's docs are
cited only where the code agrees, and their drift is named.

**Delta v0.2.0 → v0.4.1** (measured from `git diff v0.2.0..HEAD`: 434 files, +28 465/−3 661; the
checkout carries both tags but a squashed history, so this is a tree diff). Five changes shape
this skill. (1) **The container story changed**: `.sbs` stays the main format, and `.mcraft` is
back — as a native *MaterialCraft Project* ZIP holding one root SBS plus `resources/`, with
`mcraft://` references and `.mcraft` autosaves, not the old package
(`crates/formats/src/project.rs`, `crates/engine/src/file_cmds.rs`; `docs/atomic-workflow.md` still
says support was removed — stale). (2) **Packages, folders and links**: several packages can be
open at once, Explorer edits SBS folder trees and resources, and `graph.instance.add` links a graph
from another open package
(`crates/engine/src/{package_commands,folder_commands,graph_instance_commands}.rs`).
(3) **A reusable function library landed**: 171 function graphs /
2 334 nodes in `assets/sbs/functions.sbs`, reachable through `library.functions`, `library.tree` and
`library.add` (`crates/engine/src/{function_library_commands,node_library_commands}.rs`).
(4) **The registry grew from 86 ids over 19 modules to 119 over 37**, adding `package.*`,
`folder.*`, `explorer.*` and five more `library.*` ids (`crates/engine/src/commands.rs`), while the
primitive catalog shrank 30 → 29 because `motion_blur` was deleted
(`crates/nodes/src/atomic/catalog.rs`). (5) **Export and the shell moved**: export lost TIFF (7
formats), gained `outputs`, `colorSpaces` and `[w,h]` size (`crates/engine/src/export_request.rs`),
the Export window has MaterialX/MCMAT stubs (`crates/ui-egui/src/export/`), the 3D view displaces
real geometry on the CPU (`crates/render/src/preview.rs`), undo has a configurable limit, the app
self-updates, and the macOS build is signed, notarized and stapled.

**Delta v0.1.0 → v0.2.0** (kept for history; 493 files then). That release made SBS XML the native
document and retired `.mcraft`; replaced the Rust procedural library with **30 catalog entries**
(25 atomic + 5 graph items), **85 function operations** and **4 pattern kinds**; moved `.mcmat` to
manifest version 2 with `source.sbs`; added the `material_export` MCP tool and `material.export`
method; split the command registry into 19 modules (68 → 86 ids); and added wire editing, export
`size?`, colliding-name rejection, the token-authenticated control channel and English + Arabic
locales (`crates/formats/src/sbs/`, `crates/nodes/`, `crates/engine/src/commands.rs`).

**Verify against your installed version** — the ArtCraft Launcher auto-updates, so a newer build may
differ. `materialcraft-cli commands`, `nodes` and `--help` are the live contract; if the CLI is not
installed, the registry in `crates/engine/src/commands.rs` is the source of truth.

# MaterialCraft

## Overview

MaterialCraft is an open-source (MIT OR Apache-2.0), pure-Rust **node-based material designer** for
procedural, tileable PBR materials — the ArtCraft suite's material-authoring app, built as a
clean-room answer to the professional node-graph material workflow. It is SBS-first: the document
is SBS XML (`.sbs`) or a self-contained MaterialCraft Project (`.mcraft`), and the Rust side
implements only native primitives, while SBS library graphs — including 171 reusable functions —
are loaded from the library folder. It is in active development: `ROADMAP.md` still states that
reference-application rendering parity and arbitrary SBS round trips are **not** established, and
that SBS import is not lossless for arbitrary files. It runs natively on macOS, Windows, Linux and
FreeBSD and in the browser through WebAssembly. Source: GitHub `storytold/materialcraft`.

The governing idea matches the rest of the suite: **every user-visible action is an engine command
with a stable id** (`graph.wire.insertDot`, `graph.instance.add`, `file.exportMaterial`, … —
`crates/engine/src/commands.rs`), and the UI, `materialcraft-cli`, the JSON control channel, the
JSON-lines server and the MCP server all run commands through that one registry (a few workspace
helpers such as `package.open` and `render` wrap it). A cook is content-addressed and cached, and
only the nodes downstream of an edit re-cook.

## Capabilities (verified)

### One command registry, five ways in

- **119 engine command ids over 37 registry modules** (`crates/engine/src/commands.rs`
  `command_specs()`): `graph.*` 65, `edit.*` 13, `file.*` 13, `view.*` 8, `library.*` 6,
  `folder.*` 5, `session.*` 3, `package.*` 3, `explorer.*` 3. The complete id list is in
  `references/commands.md`; `materialcraft-cli commands --filter <text>` prints params, menu paths,
  shortcuts and live enabled state.
- **CLI `materialcraft-cli` — 11 subcommands, unchanged at v0.4.1**
  (`apps/materialcraft-cli/src/main.rs` `SUBCOMMANDS`): `info`, `commands [--filter]`,
  `nodes [--filter] [--category]`, `run <input> <command-id> [params] [-o out]`,
  `batch <script.json>`, `new <template> <out> [--size --name]`,
  `cook [--graph] [--set k=v] [--full]`,
  `export <input> <dir> [--graph --set --format --depth --size --pattern]`,
  `render <input> <out.png> [--size --view 3d|2d --scene --node --yaw --pitch --graph --set
  --tiling --displacement --full --hq]`,
  `mcp [--bridge --token --read-root --write-root --automation-read-root --automation-write-root]`,
  `serve [--port --read-root --write-root …]`.
- **Control channel** `materialcraft --control <port>` — loopback TCP, one JSON object per line,
  `{"id","method","params"}` → `{"id","ok":true,"result"}`. **The first request must authenticate**:
  `auth` with the token from `MATERIALCRAFT_CONTROL_TOKEN` (16–1024 printable ASCII) or the
  per-launch token file `<temp>/materialcraft-control-<port>.token` — a fresh random 256-bit token
  written owner-only (0600) after bind. One attempt per connection within 10 s; a wrong token, any
  other first request or malformed JSON closes it; at most 16 connections and 8 MiB per request
  (`crates/automation/src/security.rs`, `apps/materialcraft/src/control_server.rs`). Whoever holds
  the token has full command authority, including host file access.
- **JSON-lines server** `materialcraft-cli serve` — **12 methods, unchanged at v0.4.1**
  (`crates/automation/src/rpc.rs` `METHODS`): `ping`, `methods`, `session.inspect`, `command.list`,
  `command.run`, `command.batch`, `package.open`, `package.save`, `bitmap.import`,
  `outputs.export`, `material.export`, `render`.
- **App-only control methods — 8, unchanged at v0.4.1** (`crates/ui-egui/src/control.rs`):
  `ui.inspect`, `ui.menu.list`, `ui.menu.invoke`, `ui.set`, `ui.input`, `view.screenshot`,
  `ui.screenshot`, `ui.resize`. `ui.input` sends synthetic mouse/keyboard events one frame at a
  time — the fallback when no command fits.
- **MCP server** `materialcraft-cli mcp` — **20 tools, unchanged at v0.4.1**
  (`crates/automation/src/server/material_craft_mcp.rs`): `session_inspect`, `command_list`,
  `command_run`, `command_batch`, `library_list`, `graph_new`, `node_add`, `node_connect`,
  `node_param`, `package_open`, `package_save`, `bitmap_import`, `outputs_export`,
  `material_export`, `view_render`, plus the bridge-only `view_screenshot`, `ui_screenshot`,
  `ui_inspect`, `ui_menu_invoke`, `ui_input`. **Path confinement**: headless mode touches files
  only below `--read-root`/`--write-root`, and `command.run` refuses every path-taking `file.*`
  command (`crates/automation/src/workspace.rs` `authorize_command`) — use the workspace tools.

### Packages, Explorer, linked graphs

- **Native `.sbs`** — SBS XML with functions, pattern graphs, typed value ports, frames, comments,
  pins, parameters, and bitmaps/SVGs either embedded or under an adjacent `resources/` directory
  (`crates/formats/src/sbs/`). Saving to `.sbs` writes the XML plus resources atomically.
- **Native `.mcraft`** — a MaterialCraft Project ZIP: exactly one root SBS (`package.sbs`) and
  `resources/`, no manifest and no private graph payload; references to other packages become
  `mcraft://<identity>!/…` inside the archive. `file.save`/`saveAs`/`saveCopyAs` choose the
  container from the path; Save As offers "SBS XML Package (*.sbs)" and "MaterialCraft Project
  (*.mcraft)" separately; autosaves are `.mcraft` (`crates/formats/src/project.rs`,
  `crates/engine/src/file_cmds.rs`, `crates/ui-egui/src/material_craft_app.rs`). Archives validate
  path traversal, duplicate entries, symlinks and malformed data, and impose no fixed file-size,
  resource-count or linked-package ceiling (`docs/architecture.md` "Files").
- **Several packages open at once** — `package.activate` switches without losing selection, views
  or undo; `package.close` / `package.closeAll` refuse modified packages unless `discard: true`;
  `session.inspect` returns `documents` with each package's id, path, active/modified state and
  graphs (`crates/engine/src/{package_commands,session,inspect}.rs`).
- **Explorer** — a package browser with graph and folder trees, resources, and context menus:
  `folder.create/rename/remove/attributes/properties` and `explorer.copy/paste/move`. Empty folders
  persist as SBS groups; the root Resources name is reserved; copies retarget references between
  copied graphs (`crates/engine/src/{folder_commands,explorer_clipboard_commands}.rs`;
  `crates/formats/tests/explorer_folders.rs`).
- **Linked graph instances** — `graph.instance.add {document, graph, at?}` instances a compatible
  graph from another open package (it must have an output); dependency cycles are rejected and the
  target stores a file reference plus connector metadata, not a copy. `graph.instance.reference`
  resolves a source without editing. Missing source files keep cached connectors and report a cook
  error (`crates/engine/src/{graph_instance_commands,linked_packages}.rs`).
- **Undo is configurable** — `session.history {undoLimit?}` sets retained steps per package,
  1–10 000, default 200; `edit.undo` / `edit.redo` take `{document?}` so an agent can undo in an
  inactive package (`crates/engine/src/{history_prefs,document_history_commands}.rs`).

### Nodes, functions, patterns

- **Primitive catalog — 29 entries**: 24 in the `Atomic nodes` category plus five `Graph items`
  (`crates/nodes/src/atomic/catalog.rs`; split verified from the `ATOMIC`/`GRAPH_ITEMS` constants).
  Atomic: bitmap, blend, blur, channels shuffle, curve, directional blur/warp, distance, emboss,
  FX-Map (`fx_map`), gradient (dynamic), gradient map, grayscale conversion, HSL, levels, normal,
  pixel processor, sharpen, SVG, text, transformation 2D, uniform color, value processor, warp.
  Graph items: Dot (reroute), input color, input grayscale, input value, output. `motion_blur` was
  deleted between v0.2.0 and v0.4.1. Enumerate the live catalog with
  `materialcraft-cli nodes --filter <text>`.
- **Functions — 85 operations** (`crates/nodes/src/function/catalog.rs`): constants and variables
  by type, vectors/swizzles, samplers, casts, operators, logical/comparison, 18 math functions, and
  control (`sequence`, `ifelse`, `while`, `passthrough`). Function graphs are package items with a
  flat operation menu, editable constants and a designated output node
  (`crates/core/src/function_graph.rs`, evaluation in `crates/nodes/src/function/`).
- **Reusable SBS functions — 171 bundled** — `assets/sbs/functions.sbs` holds 171 function graphs /
  2 334 function nodes (asserted in `crates/formats/tests/function_library.rs`). Discover with
  `library.functions {filter?}` or `library.tree {canvas?}`; insert with
  `library.function.add {graph, package?, function?, at?}` (default `sbs://functions.sbs`). Function
  instances are capped at 8 levels / 4 096 nodes (`crates/engine/src/function_library.rs`,
  `crates/nodes/src/function/resolve_instances.rs`).
- **Patterns (FX-Map) — 4 kinds**: Quadrant (`paramset`), Switch (`markov2`), Iterate (`addnode`),
  Dot (`passthrough`), with iterative traversal, cycle detection and node/execution budgets
  (`crates/nodes/src/pattern/`, `crates/core/src/pattern_node_kind.rs`). New FX-Maps start with a
  Quadrant root.
- **Graph editing** — wires, reroute dots, frames, comments, navigation pins, node
  enable/disable, base parameters (size, format, seed, tiling), duplicate/paste with or without
  links, align, rename, upstream/downstream selection, `graph.createFromSelection`, and graph
  presets (`crates/engine/src/{wire_cmds,frame_commands,comment_commands,pin_commands,graph_cmds,node_cmds}.rs`).
  Annotations are target-aware across material, Function and FX-Map canvases
  (`graph.annotation.select`, `crates/engine/src/annotation_target.rs`).
- **Exposed inputs and parameter functions** — `graph.exposed.add/set/delete` build and edit typed
  inputs, `graph.exposed.prepare` previews the settings without changing the graph;
  `graph.node.function` and `graph.node.bind` attach an owned function or a typed input driver to a
  parameter, and `graph.node.reset` removes it; `graph.function.variables` suggests typed system
  variables; `session.environment` supplies time, UV tile and normal-format values without editing
  the package; `graph.context` edits physical size, pixel ratio and tiling
  (`crates/engine/src/{exposed_input,parameter_function,evaluation_environment,graph_property}_commands.rs`).

### Cook, export, portable materials

- **Cook** (`graph.cook`, the `cook` subcommand, `command.run`) with per-node timings and errors, a
  content-addressed cache across all CPU cores, scheduling only downstream nodes, and cancellation
  of stale cooks (`crates/eval/src/cache.rs`, `crates/engine/src/preview_cook.rs`). The desktop UI
  cooks on a worker thread and keeps drawing the last results.
- **Map export** — `outputs.export` / `file.export` cooks at full size and writes the selected
  outputs: **7 formats** — PNG, JPEG, TGA, BMP, WebP, EXR, HDR — at **8/16/32 bit**
  (`crates/formats/src/lib.rs` `EXPORT_FORMATS`; `encode` in `crates/formats/src/image.rs`).
  TIFF is **import-only** since v0.4.1. `size` is the larger side in px or `[width, height]`
  (clamped 16..8192, floored to powers of two, proportions kept for the larger-side form);
  `outputs` picks identifiers; `colorSpaces` maps identifiers to `srgb`, `linear` or `raw`;
  colliding file names are rejected (`crates/engine/src/{export_request,color_space,file_cmds}.rs`).
- **Bitmap and vector import** — 16 bitmap extensions (DDS, WebP, GIF, HDR, EXR, JPEG/JIF/JPE,
  PGM, PNG, TIFF, TGA/TARGA, BMP) plus SVG vectors (`BITMAP_EXTENSIONS`, `VECTOR_EXTENSIONS`;
  decoder in `crates/formats/src/image.rs`, DDS in `crates/formats/src/dds_image.rs`). GIF loads
  its first frame, DDS its first surface at the largest mip. Import creates a resource; dragging it
  onto the canvas creates the matching bitmap or SVG node (`file.importBitmap`, `file.importVector`).
- **Portable materials `.mcmat`** — `file.exportMaterial` / `material.export` cooks and packs a
  zip: `material.json` (`format: "craft-material"`, **version 2**), `maps/<usage>.png` (8-bit sRGB
  for colour usages, 16-bit linear otherwise, normals OpenGL-style) for the nine usages —
  unchanged at v0.4.1 — `baseColor`, `normal`, `roughness`, `metallic`, `height`,
  `ambientOcclusion`, `emissive`, `opacity`, `specular` — the exposed values it cooked with, the
  graph's image inputs, presets, and **`source.sbs`** so a consumer can re-cook
  (`crates/formats/src/material/{archive,manifest,map_entry}.rs`). Version-1 archives are
  rejected. Opening a `.mcmat` loads its source package and material preview
  (`crates/engine/src/file_cmds.rs`). `file.sendToTextureCraft` is an app command, not headless.
- **Render for review** — `render --size 1024x1024 --view 3d --scene material_ball` writes a PNG
  with no GPU; `--hq` is a beauty render (displaced mesh, ray-traced AO, shadowed key light, 3×3
  supersampling) and `--displacement` sets its depth in scene radii
  (`crates/automation/src/render_options.rs`).
- **3D view** — 7 built-in scenes (`cube`, `cylinder`, `plane`, `sphere`, `material_ball`,
  `rounded_cube`, `torus`, plus `custom` after `view.3d.loadMesh` for OBJ/glTF/GLB) and 4
  environment ids (`studio`, `sunset`, `overcast`, `night`), exposure/rotation, `heightScale` and
  `heightLevel` displacement, `transparency`, `alphaView`, `normalYFlip` for DirectX normals, and
  `view.3d.assign` / `view.3d.outputs` / `view.3d.clear` to map any image output to a PBR channel
  (`crates/engine/src/{view_cmds,material_preview_commands}.rs`). **It is a CPU renderer**: the
  height output subdivides the mesh up to a triangle budget and moves vertices along their normals
  (`crates/render/src/preview.rs` `Scene::displaced`) — real geometry, but no GPU tessellation.
  The preview cap is 256–4096 px or Full in the UI; `view.previewSize` clamps 64..8192
  (`crates/ui-egui/src/preview_resolution.rs`).
- **Templates and locales** — 3 graph templates, `empty`, `pbr`, `atomics`
  (`crates/engine/src/samples.rs`), unchanged at v0.4.1; 2 UI locales, English and Arabic RTL,
  unchanged at v0.4.1 (`crates/ui-egui/src/i18n.rs`).
- **App shell** — eight dockable panels (Graph, Explorer, Library, 3D, 2D, Properties, Console,
  History) on shared craft-libs crates, a Home screen, preferences, and Help → Check for updates…
  (`crates/ui-egui/src/{docking,menus,updates_ui}.rs`). The export window has four tabs:
  From graph, Batch, MaterialX and MCMAT, where the last two report "not available yet"
  (`crates/ui-egui/src/export/`).

## Known limitations and not-implemented

Do not assign these at v0.4.1:

- **No GPU renderer** — the 3D view is CPU-only (BVH ray casts, CPU displacement); no GPU
  tessellation, no path-traced render mode, no custom light rigs (four environment ids, exposure and
  rotation only).
- **No mesh-based generators or mesh-map bakers** inside the app; mesh import exists only for the
  3D view's `custom` scene. Mesh maps from TextureCraft arrive as input preview images.
- **SBS import is not a lossless importer for arbitrary files**: some native parameter variants and
  package/editor metadata are unsupported and reported as warnings; missing nodes stay as
  placeholders; environment maps are not imported (`docs/atomic-workflow.md` "Current limits").
- **Reference-application parity is unverified** — reopening generated SBS there has not been
  verified, and numerical parity (pattern shapes, blending, sampling, random sequences) is
  explicitly not established (`ROADMAP.md`).
- **`.mcmat` is version 2 only** — a consumer that expects version 1 will reject these materials,
  and this build rejects version-1 archives.
- **Export is narrower than import**: TIFF, DDS, GIF and PGM are import-only; the Export window
  lists DDS as planned, and its MaterialX and MCMAT tabs are stubs
  (`crates/ui-egui/src/export/export_format.rs`, `docs/atomic-workflow.md`).
- **No visibility conditions** on graph inputs; **one graph in the canvas at a time** (packages
  switch, graphs do not tab), no minimap, and fixed shortcuts with no keymap editor (the shortcut
  list is read-only: `ui.help.shortcuts`). `docs/target-app-parity.md` still lists these gaps.
- **Text uses the built-in stroke font**; external font references are an explicit error. SVG
  supports vector geometry only — no external images or font loading.
- **The Explorer's dependency tools are incomplete**: `Link ▸ Bitmap/Vector graphics`, `Export with
  dependencies…` and `Dependency manager…` are menu rows with no command behind them (disabled),
  while `Export material…`, `Send to TextureCraft`, `Open dependencies` and `Show in folder…` work
  (`crates/ui-egui/src/menus.rs` `EXPLORER_LINK` / `EXPLORER_PACKAGE`).
- **Function authoring is SBS-graph-bound**: reusable functions come from SBS graphs (Function
  Graphs, processor/parameter functions and library instances) rather than a separate function
  library editor; library aliases are read-only save destinations, an edited library must be saved
  to a local path, and the converted standard library's redistribution rights are not established
  (`ROADMAP.md`).
- **The CLI is a separate install** — the app bundle ships only the GUI binary; `materialcraft-cli`
  comes from the release's command-line archive.
- **`ui.screenshot` may time out**: the repo records that the window-capture callback never fires
  on its test machine (`docs/gaps.md` #7, claimed — not retested here). `view.screenshot` is the
  safer capture.
- **Doc drift to ignore**: `docs/atomic-workflow.md` says `.mcraft` support was removed (wrong),
  `ROADMAP.md`/`docs/architecture.md` say 30 catalog entries (code: 29), the CLI usage string lists
  `tif` export (engine: 7 formats, no TIFF), and `docs/control-protocol.md` lists retired
  `file.new` template ids. Code wins.
- **Programmatic calls never open dialogs**: every command runs with defaults; only
  `ui.menu.invoke` behaves like a menu click (and returns an error while a dialog is open).

## How to operate

- **Launch on macOS**: `open -a "MaterialCraft"` (GUI only — never from an agent that cannot see
  the screen). The binary accepts `[package.sbs] [--control <port>] [--empty]`; `--version` and
  `--help` print and exit (`apps/materialcraft/src/main.rs`).
- **One-shot headless build**:
  `materialcraft-cli new atomics out.sbs --size 2048` → `materialcraft-cli cook out.sbs` →
  `materialcraft-cli export out.sbs maps --format png --depth 8 --size 2048` →
  `materialcraft-cli render out.sbs preview.png --size 1024x1024 --hq`.
- **Save a container deliberately**: `file.save {"path":"out.sbs"}` writes SBS + adjacent
  `resources/`; `file.save {"path":"out.mcraft"}` writes the self-contained ZIP. A new package has
  no path, so `file.save` without `path` errors. Prefer `.mcraft` to hand one file to another
  machine or app; prefer `.sbs` when the resources should stay browsable/diffable.
- **Script a package**: `materialcraft-cli run out.sbs graph.exposed.set '{"id":"roughness","value":0.4}' -o out.sbs`
  (for a package that exposes `roughness`), or a batch: `materialcraft-cli batch steps.json` with
  `[{"id","params"}]` or `{"open": <input>, "steps": [...], "save": <out.sbs>}`.
- **Set exposed inputs without opening a graph**: `cook out.sbs --set roughness=0.4 --set tint="#aa7744"`
  (`--set` values are JSON, else strings). Per-output colour spaces are only available through
  `file.export`'s `colorSpaces` (CLI `run` or MCP), not a CLI flag.
- **Discover before scripting**: `materialcraft-cli nodes --category "Atomic nodes"`,
  `materialcraft-cli commands --filter material`, `library.functions`, `library.tree`, then `run`
  the id you found. `graph.node.info` describes a node and `graph.node.parameterInfo` reports a
  parameter's type, value, driver and warnings without editing. Parameters are typed — numbers,
  `[x,y]`, `"#rrggbb"`, enum index, curves `[[x,y],…]`, gradients `[[pos,color],…]`, and typed
  function values.
- **Work with several packages**: open both (`file.open`), then
  `package.activate {"document": <id>}`; `session.inspect` lists documents. Link a graph with
  `graph.instance.add {"document": <source id>, "graph": "<name>"}` — save the source first.
- **Use the bundled functions**: in a Function or processor canvas, copy `graph` and `package` from a
  `library.functions` entry and run `library.function.add {"package": "<package>", "graph": "<graph>"}`
  (the default package is `sbs://functions.sbs`); native nodes go through
  `library.add {"entry": "<id from library.tree>"}`.
- **Edit the Explorer tree**: `folder.create {"parent": "", "name": "Materials"}`,
  `explorer.copy {"graph": 0}`, `explorer.paste {"folder": "Materials"}`,
  `folder.rename {"folder": "Materials", "name": "Surfaces"}`.
- **Drive the live app**: launch `materialcraft --control <port>`, authenticate with the token from
  the environment or the token file, then `command.run` / `session.inspect` / `view.screenshot`.
  Set `MATERIALCRAFT_NO_PREFS=1` for scripted runs so the user's layout is untouched.
- **Agent flow**: `claude mcp add materialcraft -- materialcraft-cli mcp --read-root . --write-root .`;
  then `library_list` → `graph_new` → `node_add`/`node_connect`/`node_param` → `view_render` →
  `outputs_export` → `material_export` → `package_save`. Bridge to a running app with
  `--bridge <port>`.

## Working with an AI agent

- Treat `command_list`, `library_list`, `library.tree`/`library.functions` and `nodes` as the
  discovery contract; never invent a node id, primitive name, command id or parameter name. Every
  command reports whether it is enabled in the current session.
- **Verify a cook, don't assume it**: `session.inspect` returns node cook errors, output sizes and
  mean values; `cook` prints per-node timings and errors; `render` gives a PNG you can inspect
  without a GUI. Linked instances whose source is missing report a cook error — do not read that as
  an empty material.
- **Choose the container on purpose**: `.mcraft` is one file (best for transfer, including linked
  dependencies); `.sbs` is XML plus a `resources/` folder (best for review and version control).
  Both round-trip the same package; do not claim a lossless round trip for a file you did not save
  and reopen.
- **A `.mcmat` is a build artifact plus a recipe**: it holds cooked maps, exposed values, presets,
  input images and `source.sbs`. If parameters may change later, keep the `.sbs`/`.mcraft` and
  re-cook; opening the `.mcmat` recovers the source package, not the cooked values.
- When importing SBS, read the import warnings: unsupported parameters and missing nodes become
  warnings and placeholders, not silent value changes. The same applies to `library.tree` entries
  marked `missing` — they refuse to insert with a reason.
- Do not attempt to drive the GUI blind; there is no stable window automation beyond `ui.input`,
  and it is bridge-only. If a command does not exist, say so rather than scripting a click
  sequence.
- Mind the sandbox: headless MCP/JSON-lines access is confined to the read/write roots, and
  `command.run` refuses path-taking `file.*` commands. Use `package_open`, `package_save`,
  `bitmap_import`, `outputs_export` and `material_export`.
- The control token grants full command authority, including host files — treat it as a secret and
  never print it into a shared log.

## Verification protocol

- **Round-trip both containers**: `new` → edit → `cook` → `export` → `render` → save as `.sbs`,
  reopen in a fresh `info`, then save the same package as `.mcraft` and reopen that. Confirm the
  node graph, wire types, folders, resources and outputs survived, and re-cook to the same means.
  A `.mcraft` must contain `package.sbs` and `resources/` only.
- **Never trust a silent export**: check the output directory for the expected usages and sizes,
  open one map, and confirm the chosen `colorSpaces` (sRGB data in a normal map is a silent bug).
  Export refuses colliding names — if it errors, fix the pattern or `outputs` list rather than
  deleting files blindly.
- **Check `.mcmat` before shipping**: `material.json` must say `format: "craft-material"` and
  `version: 2`, carry `source.sbs`, and contain the usages you expect (9 are defined). A consumer
  that does not know version 2 will reject it.
- **Read warnings**: SBS import, linked packages and library entries all report warnings/errors
  instead of silently repairing. Treat a warning list as part of the result.
- **Alpha discipline**: back up `.sbs`/`.mcraft` files per session, keep the undo limit in mind
  (default 200 steps), and update the app only between projects.
- **Version the evidence**: record the app version you used (`MaterialCraft --version` prints
  `MaterialCraft <version> (<sha> <date>)`) and the `.mcmat`/SBS versions you shipped.

## Sources & evidence

- Repo: `https://github.com/storytold/materialcraft` (MIT OR Apache-2.0), tag **v0.4.1**, commit
  **`65f7bfd3e5f40d695d03162285879f0f8079ff6c`**, inspected **2026-11-12**. Previous audit: v0.2.0
  (`a1bbd4a83f62365d90f085e5f1ad61410f9cf11c`).
- Files read: `README.md`, `ROADMAP.md`, `AGENTS.md`, `Cargo.toml`, `docs/architecture.md`,
  `docs/atomic-workflow.md`, `docs/control-protocol.md`, `docs/gaps.md`,
  `docs/target-app-parity.md`, `docs/file-format-parity.md`,
  `apps/materialcraft/src/main.rs`, `apps/materialcraft-cli/src/main.rs`,
  `crates/engine/src/commands.rs` and its 37 `*_cmds.rs`/`*_commands.rs` registry modules,
  `crates/engine/src/{file_cmds,export_request,color_space,history_prefs,package_commands,
  package_file_commands,folder_commands,explorer_clipboard_commands,graph_instance_commands,
  function_library_commands,node_library_commands,material_preview_commands,view_cmds,
  document_history_commands,inspect}.rs`,
  `crates/formats/src/{lib,project,image,dds_image}.rs`, `crates/formats/src/project/project_files.rs`,
  `crates/formats/src/sbs/`, `crates/formats/src/material/{archive,manifest,map_entry}.rs`,
  `crates/formats/tests/{project_packages,function_library,explorer_folders}.rs`,
  `crates/nodes/src/{catalog,atomic/catalog,function/catalog,pattern/catalog}.rs`,
  `crates/render/src/{preview,ibl}.rs`, `crates/automation/src/{rpc,security,workspace}.rs`,
  `crates/automation/src/server/material_craft_mcp.rs`,
  `crates/ui-egui/src/{control,docking,menus,updates_ui,i18n,preview_resolution}.rs`,
  `crates/ui-egui/src/export/`, `crates/ui-egui/src/material_craft_app.rs`.
- Counts: 119 command ids over 37 modules (`cmd!` literals in `command_specs()` modules), 11 CLI
  subcommands (`SUBCOMMANDS`), 20 MCP tools (`#[tool]` + `async fn`), 12 JSON-lines methods
  (`METHODS`), 29 catalog entries (`atomic::defs()` + category constants), 85 function operations
  (`FUNCTIONS`), 4 pattern kinds, 171 bundled functions / 2 334 nodes (`<function>`/`<paramNode` and
  the test assertions), 3 templates, 7 scenes, 4 environments, 9 map usages, 7 export formats,
  17 image extensions, 2 locales. Full tables: `references/commands.md`, `references/library.md`.
- Installed bundle: `/Applications/MaterialCraft.app` — `CFBundleShortVersionString 0.4.1`,
  `CFBundleVersion 0.4.1`, `CFBundleIdentifier ai.storyteller.materialcraft`, binary prints
  `MaterialCraft 0.4.1 (65f7bfd 2026-11-12)`, Developer ID-signed, notarized and stapled
  (`codesign`/`spctl` read-only). Only `--version`/`--help` were run; the GUI was never launched.
  The bundle ships no `materialcraft-cli`.
