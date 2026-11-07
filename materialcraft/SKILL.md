---
name: materialcraft
description: >
  MaterialCraft is the ArtCraft team's open-source, pure-Rust node-based procedural material designer —
  build tileable PBR materials from native primitives, functions and patterns in a node graph, watch them
  update live in 2D and on a 3D model, and export the maps for any engine. Its native document is the SBS
  package (`.sbs`, XML); it also reads SBS graphs from the professional material workflow and ships portable
  `.mcmat` materials that TextureCraft applies without a graph engine. Trigger this skill whenever the user
  mentions MaterialCraft — or an `.sbs`/`.mcmat` material — asks what it can or cannot do, which primitives
  exist, how to script, automate, batch, or headlessly drive it (`materialcraft-cli`, MCP, the JSON control
  channel), wants a tileable PBR material built or exported, wants an SBS graph imported or a material handed
  to TextureCraft, needs exported maps verified, or troubleshoots it. Also when the job is described without
  naming the app — "make me a tileable brick material", "export base color/normal/roughness maps", "build
  this material as a node graph", "open this SBS file", "share this material with my texturing app". Do not
  guess its node library or parameters — read this, then ask the app.
---

**Audit basis.** Re-pinned 2026-11-07 against tag **v0.2.0**, commit
**`a1bbd4a83f62365d90f085e5f1ad61410f9cf11c`** — `git rev-parse HEAD` in the pinned checkout confirms — and
the installed bundle matches (its binary prints
`MaterialCraft 0.2.0 (a1bbd4a 2026-11-06)`). This supersedes the v0.1.0 audit
(`cedabf02030a3c662fda99b197ceb3ed12790ee7`, 2026-11-04). Every count below was measured from this tree
(the method is in `evidence.md`); the app's docs are cited only where the code agrees, and their drift is
named.

**Delta v0.1.0 → v0.2.0** (measured from `git diff v0.1.0..HEAD`; 493 files, +28 806/−13 724). The release
replaced the app's document and library foundations, so most of the v0.1.0 skill was rewritten. (1) **The
native document is now native SBS XML (`.sbs`)**: `crates/formats/src/sbs/sbs_reader.rs` and `sbs_writer.rs`
read and write filters, graph bridges, typed value ports, function and pattern nodes, parameters and
resources, and `.mcraft` package support is gone from the code (`docs/architecture.md` and
`docs/atomic-workflow.md` confirm; two other docs still mention it — stale, not code). (2) **The Rust
procedural node library was replaced by native primitives**: the catalog is **30 entries** —
25 `Atomic nodes` + 5 `Graph items` (`crates/nodes/src/atomic/catalog.rs::defs`) — driven by
**85 function operations** (`crates/nodes/src/function/catalog.rs::FUNCTIONS`) and **4 pattern nodes**
(Quadrant, Switch, Iterate, Dot; `crates/nodes/src/pattern/catalog.rs`); the old "227 nodes" and the ≈67 %
roadmap figure are retired by `ROADMAP.md`. (3) **`.mcmat` moved to manifest version 2** with `source.sbs`,
and version-1 archives are rejected (`crates/formats/src/material/archive.rs`). (4) **The sandboxed-MCP gap
closed**: a `material_export` tool (`crates/automation/src/server/material_craft_mcp.rs`) and a
`material.export` JSON-lines method (`crates/automation/src/rpc.rs` `METHODS`) can hand a material to
TextureCraft. (5) The command registry was split into **19 modules** and grew from 68 to **86 ids**
(`crates/engine/src/commands.rs`), adding wire editing (`graph.wire.insertDot`/`swap`/`delete`),
`file.newAtomicSample` and alignment/frame/annotation/comment/function/pattern/value-input commands.
(6) **3D view**: `transparency`, `alphaView`, `normalYFlip` (DirectX normal maps), `heightLevel` and
`target` (`crates/engine/src/view_cmds.rs`; `crates/render/src/preview.rs`); export gained a `size?`
parameter and rejects colliding filenames (`crates/engine/src/file_cmds.rs`); the control channel now uses
a random owner-only token file with one authentication attempt per connection
(`apps/materialcraft/src/control_server.rs`, `crates/automation/src/security.rs`); the UI ships **two
locales**, English and Arabic (`crates/ui-egui/src/i18n.rs`); templates shrank to three —
`empty`, `pbr`, `atomics` (`crates/engine/src/samples.rs`).

**Verify against your installed version** — the ArtCraft Launcher auto-updates, so a newer build may differ.
`materialcraft-cli commands`, `nodes` and `--help` are the live contract.

# MaterialCraft

## Overview

MaterialCraft is an open-source (MIT OR Apache-2.0), pure-Rust **node-based material designer** for
procedural, tileable PBR materials — the ArtCraft suite's material-authoring app, built as a clean-room
answer to the professional node-graph material workflow. Since v0.2.0 it is an **SBS-first** app: the native
document is SBS XML, and the Rust side implements only native primitives — SBS library nodes belong in SBS
graphs and have no Rust reimplementation (`crates/nodes/src/catalog.rs`, `docs/atomic-workflow.md`). It is
early software: v0.2.0 explicitly admits that reference-app rendering parity and arbitrary SBS round trips
have **not** been established (`ROADMAP.md`), and that SBS import is not lossless for arbitrary files. It runs
natively on macOS, Windows, Linux and FreeBSD, and in the browser through WebAssembly. Source: GitHub
`storytold/materialcraft`.

The governing idea matches the rest of the suite: **every user-visible action is an engine command with a
stable id** (`graph.wire.insertDot`, `graph.exposed.set`, `file.exportMaterial`, … —
`crates/engine/src/commands.rs`), and the UI, `materialcraft-cli`, the JSON control channel and the MCP
server all dispatch the same registry. A cook is content-addressed and cached, and cooking is scheduled only
for the nodes an input change actually reaches.

## Capabilities (verified)

### One command registry, four surfaces

- **86 engine command ids** — `cmd!(` registrations across the 19 modules aggregated by
  `command_specs()` (`crates/engine/src/commands.rs`), by namespace: `graph.*` 53, `edit.*` 13, `file.*` 10,
  `view.*` 8, `library.list`, `session.inspect`. `materialcraft-cli commands` lists them with params and
  enabled state.
- **CLI `materialcraft-cli` — 11 subcommands** (`apps/materialcraft-cli/src/main.rs` `SUBCOMMANDS`;
  unchanged at v0.2.0): `info`, `commands [--filter]`, `nodes [--filter] [--category]`,
  `run <input> <command-id> [params] [-o out.sbs]`, `batch <script.json>`, `new <template> <out.sbs> [--size]
  [--name]`, `cook [--graph] [--set k=v] [--full]`, `export <input> <dir> [--graph --set --format --depth
  --size --pattern]`, `render <input> <out.png> [--size --view 3d|2d --scene --node --yaw --pitch --graph
  --set --tiling --displacement --full --hq]`, `mcp [--bridge --token --read-root --write-root
  --automation-read-root --automation-write-root]`, `serve [--port --read-root --write-root …]`.
- **Control channel** `materialcraft --control <port>` — loopback TCP, one JSON object per line,
  `{"id","method","params"}` → `{"id","ok":true,"result"}`. **The first request must authenticate**: `auth`
  with the token from `MATERIALCRAFT_CONTROL_TOKEN` (16–1024 printable ASCII) or the per-launch token file
  `<temp>/materialcraft-control-<port>.token` — a fresh random 256-bit token written owner-only (0600) after
  the port is bound. One authentication attempt per connection within 10 s; a wrong token, another first
  request or malformed JSON closes it; at most 16 connections, 8 MiB per request
  (`crates/automation/src/security.rs`, `apps/materialcraft/src/control_server.rs`). Methods: `ping`,
  `methods`, `command.run`, `command.list`, `command.batch`, `session.inspect`, `package.open/save`,
  `bitmap.import`, `outputs.export`, `material.export`, `render`, plus the app-only `ui.inspect`,
  `ui.menu.list`, `ui.menu.invoke`, `ui.set`, `ui.input`, `view.screenshot`, `ui.screenshot`, `ui.resize`
  (`crates/ui-egui/src/control.rs`). `ui.input` sends synthetic mouse/keyboard events one frame at a time —
  the fallback when a command does not exist.
- **MCP server** `materialcraft-cli mcp` — **20 tools** (`crates/automation/src/server/material_craft_mcp.rs`):
  `session_inspect`, `command_list`, `command_run`, `command_batch`, `library_list`, `graph_new`, `node_add`,
  `node_connect`, `node_param`, `package_open`, `package_save`, `bitmap_import`, `outputs_export`,
  `material_export`, `view_render`, and the bridge-only `view_screenshot`, `ui_screenshot`, `ui_inspect`,
  `ui_menu_invoke`, `ui_input`. **Path confinement**: headless mode touches files only below
  `--read-root`/`--write-root`, and through `command_run` every path-taking `file.*` command is refused — use
  the workspace tools.
- **JSON-lines server** `materialcraft-cli serve` — **12 methods** (`crates/automation/src/rpc.rs` `METHODS`),
  on stdio or on a loopback port behind the same token handshake.

### Materials, graphs, nodes

- **Native SBS package `.sbs`** — SBS XML read and written by `crates/formats/src/sbs/`: filters, graph
  bridges, typed value ports, function nodes, pattern nodes, parameters and embedded/linked resources. There
  is no private package comment or embedded JSON document. `.mcraft` packages are **not** supported any more
  (no `.mcraft` handling remains in `crates/`).
- **Primitive catalog** — **30 entries**: 25 nodes in the `Atomic nodes` category plus five `Graph items`
  (`crates/nodes/src/atomic/catalog.rs`), e.g. bitmap, SVG, text, FX-Map (`fx_map`), blend, blur, channels shuffle,
  curve, directional blur/warp, distance, emboss, gradients, HSL, levels, normal, motion blur, pixel/value
  processors, sharpen, transformation, uniform, warp, and the colour/value/grayscale inputs and output.
  Enumerate the live library with `materialcraft-cli nodes --filter <text>`.
- **Functions** — **85 operations** (`crates/nodes/src/function/catalog.rs`): constants and variables by
  type, arithmetic, logical/comparison, vector/swizzle and typed conversions. Function graphs are package
  items with a flat operation menu, editable constants and a designated output node
  (`crates/core/src/function_graph.rs`, evaluation in `crates/nodes/src/function/`).
- **Patterns (FX-Map)** — 4 nodes: Quadrant (`paramset`), Switch (`markov2`), Iterate (`addnode`), Dot
  (`passthrough`), with iterative traversal, cycle detection and node/execution budgets
  (`crates/nodes/src/pattern/`). New FX-Maps start with a Quadrant root.
- **Node graph** — wires, frames (groups), comments, navigation pins, node enable/disable, node base
  parameters (output size, format, seed, tiling), duplicate/paste with or without links, align, rename,
  selection helpers (`graph.selectUpstream`/`Downstream`), and wire editing: `graph.wire.insertDot` splits a
  wire with a reroute Dot, `graph.wire.swap` swaps/reverses sources, `graph.wire.delete`.
- **Exposed graph inputs** — typed inputs another app or an artist can set: `graph.exposed.add`/`set`/
  `delete`, `--set <input>=<value>` on `cook`/`export`/`render`, and `graph.input.bind`/`unbind` to feed an
  input from a mesh map or image.
- **Sub-graphs / instancing and presets** — `graph.createFromSelection` moves nodes into a sub-graph and
  replaces them with an instance; `graph.preset.save/apply/delete` store and restore input value sets.
- **2D and 3D views** — `view.2d` shows any node's output with channel, tiling and histogram options, and the
  Levels property panel carries a histogram editor with range handles (`crates/ui-egui/src/levels_editor.rs`,
  `crates/nodes/src/atomic/levels.rs`);
  `view.3d` renders the material on a mesh with scenes `rounded_cube`, `cube`, `sphere`, `cylinder`, `plane`,
  `torus`, `material_ball` — seven, unchanged at v0.2.0 — four environments (`studio`, `sunset`, `overcast`, `night`), exposure,
  `heightScale`/`heightLevel` displacement, `transparency`, `alphaView` and `normalYFlip` for DirectX normal
  maps, plus `view.3d.loadMesh` for an OBJ, glTF or GLB (`crates/render/src/preview.rs`,
  `crates/engine/src/view_cmds.rs`). **The 3D view is a CPU renderer** with parallax, not GPU tessellation.
  Preview resolution is selectable up to 4096 px (`crates/ui-egui/src/preview_resolution.rs`).

### Cook, export, portable materials

- **Cook** (`graph.cook`, the `cook` subcommand, `command.run`) with per-node timings and errors, a
  content-addressed cache across all CPU cores, scheduling only the nodes an input change reaches, and
  cancellation of stale cooks (`crates/eval/src/cache.rs`, `crates/engine/src/preview_cook.rs`).
- **Map export** — `outputs.export` / `file.export` cooks the graph at full size and writes every output:
  **PNG, JPEG, TGA, TIFF, BMP, WebP, EXR, HDR at 8/16/32 bit** (`crates/formats/src/lib.rs`
  `IMAGE_EXTENSIONS`; CLI `--format`, `--depth`, `--pattern`). v0.2.0 adds `size?` — the larger side in px,
  16..8192, rounded down to a power of two, keeping proportions — and refuses colliding output filenames
  (`crates/engine/src/file_cmds.rs`).
- **Portable materials `.mcmat`** — `file.exportMaterial` / `material.export` cooks the graph and packs a
  zip: `material.json` (`format: "craft-material"`, **version 2**), `maps/<usage>.png` (8-bit sRGB for colour
  usages, 16-bit linear otherwise, normals OpenGL-style) for the nine usages — unchanged at v0.2.0 —
  `baseColor`, `normal`, `roughness`, `metallic`,
  `height`, `ambientOcclusion`, `emissive`, `opacity`, `specular`, the exposed parameter values the maps were
  cooked with, the graph's image inputs, presets, and **`source.sbs`** so another app can re-cook
  (`crates/formats/src/material/{archive,manifest,map_entry}.rs`). Manifest version 1 archives are
  rejected. This is the cross-app contract with TextureCraft.
- **`file.sendToTextureCraft`** hands the material to a running TextureCraft; it is an app command, not a
  headless one.
- **Render for review** — `render --size 1024x1024 --view 3d --scene material_ball` writes a PNG with no GPU;
  `--hq` is a beauty render (displaced mesh, ray-traced AO, shadowed key light, 3×3 supersampling) and
  `--displacement` sets its depth in scene radii.
- **Templates** — 3 at v0.2.0: `empty`, `pbr`, `atomics` (`crates/engine/src/samples.rs` `TEMPLATES`). The
  atomic sample is also `file.newAtomicSample` and `examples/atomic_sample.sbs`.
- **Localisation** — 2 UI locales, English (`en`) and Arabic (`ar`, right-to-left), selected from the system
  locale (`crates/ui-egui/src/i18n.rs`).

## Known limitations and not-implemented

Do not assign these at v0.2.0:

- **No GPU 3D view**: the preview is a CPU renderer with parallax only; no tessellation, no GPU displacement
  preview, no custom light rigs (four fixed environments, exposure and rotation only).
- **No mesh-based generators or bakers** — you cannot start a material from a mesh or bake mesh maps inside
  the app.
- **SBS import is not a lossless importer for arbitrary files**: some native parameter variants and
  package/editor metadata are unsupported and reported as warnings; missing nodes stay as placeholders;
  function graphs and environment maps are not imported (`docs/atomic-workflow.md` "Current limits").
- **Parity with the reference application is unverified** — reopening generated SBS there has not been
  verified, and numerical parity (pattern shapes, blending, sampling, random sequences) is explicitly not
  established (`ROADMAP.md`, `docs/atomic-workflow.md`).
- **`.mcmat` is version 2 only** — a consumer that expects version 1 will reject these materials, and this
  build rejects version-1 archives.
- **No function loops or reusable functions** — function graphs live on one parameter or processor, and
  calling another SBS function graph is not implemented.
- **One graph at a time**, no minimap or multi-graph tabs; **fixed shortcuts**, no keymap editor.
- **Text uses the built-in stroke font**; external font references are an explicit error. SVG supports vector
  geometry only — no external images or font loading.
- **No signed/notarized public release yet** (`docs/gaps.md` #10 is still open).
- `ui.menu.invoke` is the only method that behaves like a click; every command runs with defaults and never
  opens a dialog.
- **`ui.screenshot` may time out**: the repo records that the window-capture callback never fires on its test
  machine (`docs/gaps.md` #7, claimed — not retested here). `view.screenshot` is the safer capture.

## How to operate

- One-shot build: `materialcraft-cli new atomics out.sbs --size 2048` → `materialcraft-cli cook out.sbs` →
  `materialcraft-cli export out.sbs maps --format png --depth 8 --size 2048` →
  `materialcraft-cli render out.sbs preview.png --size 1024x1024 --hq`.
- Script a package: `materialcraft-cli run out.sbs graph.exposed.set '{"id":"roughness","value":0.4}' -o out.sbs`
  (for a package that exposes `roughness`), or a batch: `materialcraft-cli batch steps.json` with `[{"id","params"}]` or
  `{"open": <input>, "steps": [...], "save": <out.sbs>}`.
- Set exposed inputs without opening a graph: `cook out.sbs --set roughness=0.4 --set tint="#aa7744"`
  (`--set` values are JSON, else strings).
- Discover before scripting: `materialcraft-cli nodes --category "Atomic nodes"`, `materialcraft-cli commands --filter
  material`, then `run` the id you found. Parameters are typed — numbers, `[x,y]`, `"#rrggbb"`, enum index,
  curves `[[x,y],…]`, gradients `[[pos,color],…]`, and typed function values.
- Drive the live app: launch `materialcraft --control <port>`, authenticate with the token from the
  environment or the token file, then `command.run` / `session.inspect` / `view.screenshot`. Set
  `MATERIALCRAFT_NO_PREFS=1` for scripted runs so the user's layout is untouched.
- Agent flow: `claude mcp add materialcraft -- materialcraft-cli mcp --read-root . --write-root .`; then
  `library_list` → `graph_new` → `node_add`/`node_connect`/`node_param` → `view_render` → `outputs_export` →
  `material_export` → `package_save`. Bridge to a running app with `--bridge <port>`.
- Launch on macOS: `open -a "MaterialCraft"` (GUI only — never do this from an agent that cannot see the
  screen). The bundle ships the GUI binary; the headless CLI is a separate install.

## Working with an AI agent

- Treat `command_list`, `library_list` and `nodes` as the discovery contract; never invent a node id,
  primitive name or parameter name. Every command reports whether it is enabled in the current session.
- Verify a cook, don't assume it: `session.inspect` returns node cook errors, output sizes and mean values;
  `cook` prints per-node timings and errors; `render` gives a PNG you can inspect without a GUI.
- A `.mcmat` is a build artifact plus a recipe: if you need different parameters later, keep the
  `source.sbs`/the `.sbs` package and re-cook rather than editing maps.
- When importing SBS, read the import warnings: unsupported parameters and missing nodes become warnings and
  placeholders, not silent value changes. Do not claim a lossless round trip for a file you did not save.
- Do not attempt to drive the GUI blind; there is no stable window automation beyond `ui.input`, and it is
  bridge-only.

## Verification protocol

- Round-trip everything: `new` → edit → `cook` → `export` → `render` → reopen the `.sbs` in a fresh `info`,
  confirm the node graph, wire types and outputs survived, and re-cook to the same means.
- Never trust a silent export: check the output directory for the expected map usages and sizes, and open one
  map.
- `.mcmat` is versioned (`material.json` `version: 2`, `source.sbs`); a consumer that does not know version 2
  will reject it. Record the version you shipped.
- Alpha software: back up `.sbs` files per session, and update the app only between projects.

## Sources & evidence

- Repo: `https://github.com/storytold/materialcraft` (MIT OR Apache-2.0), tag **v0.2.0**, commit
  **`a1bbd4a83f62365d90f085e5f1ad61410f9cf11c`**, inspected 2026-11-07. Previous audit: v0.1.0
  (`cedabf02030a3c662fda99b197ceb3ed12790ee7`).
- Files read: `README.md`, `ROADMAP.md`, `docs/atomic-workflow.md`, `docs/gaps.md`,
  `docs/control-protocol.md`, `docs/architecture.md`, `docs/file-format-parity.md`, `Cargo.toml`,
  `apps/materialcraft-cli/src/main.rs`, `apps/materialcraft/src/{main.rs,control_server.rs}`,
  `crates/engine/src/commands.rs` and its 19 `*_cmds.rs`/`*_commands.rs` registry modules,
  `crates/engine/src/{file_cmds.rs,samples.rs,view_cmds.rs,atomic_sample_commands.rs}`,
  `crates/formats/src/lib.rs` and `crates/formats/src/material/{archive,manifest,map_entry}.rs`,
  `crates/formats/src/sbs/{sbs_reader.rs,sbs_writer.rs}`, `crates/automation/src/rpc.rs`,
  `crates/automation/src/server/material_craft_mcp.rs`, `crates/automation/src/security.rs`,
  `crates/nodes/src/{catalog.rs,atomic/catalog.rs,function/catalog.rs,pattern/catalog.rs}`,
  `crates/render/src/preview.rs`, `crates/ui-egui/src/{i18n.rs,control.rs}`.
- Counts: 86 command ids (`cmd!(` literals over the 19 registry modules), 20 MCP tools (`#[tool(…) async fn`),
  12 JSON-lines methods (`METHODS`), 11 CLI subcommands (`SUBCOMMANDS`), 30 catalog entries
  (`atomic::defs`), 85 function operations (`FUNCTIONS`), 4 pattern nodes, 3 templates, 7 3D scenes, 9
  `.mcmat` map usages, 8 export formats (11 image extensions), 2 UI locales.
- Installed bundle: `/Applications/MaterialCraft.app` — `CFBundleShortVersionString 0.2.0`,
  `CFBundleIdentifier ai.storyteller.materialcraft`, binary prints `MaterialCraft 0.2.0 (a1bbd4a
  2026-11-06)`; `--version`/`--help` only, the GUI was never launched.
