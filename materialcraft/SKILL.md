---
name: materialcraft
description: >
  MaterialCraft is the ArtCraft team's open-source, pure-Rust node-based procedural material designer —
  build tileable PBR materials from noises, patterns and filters in a node graph, watch them update live
  in 2D and on a 3D model, and export the maps for any engine. It reads and writes the native `.mcraft`
  package and ships portable `.mcmat` materials that TextureCraft applies without a graph engine. Trigger
  this skill whenever the user mentions MaterialCraft — or a `.mcraft`, `.mcmat` file — asks what it can
  or cannot do, which nodes exist, how to script, automate, batch, or headlessly drive it
  (`materialcraft-cli`, MCP, the JSON control channel), wants a tileable PBR material built or exported,
  wants a material handed to TextureCraft, needs exported maps verified, or troubleshoots it. Also when
  the job is described without naming the app — "make me a tileable brick material", "export base
  color/normal/roughness maps", "build this material as a node graph", "share this material with my
  texturing app". Do not guess its node library or parameters — read this, then ask the app.
---

**Audit basis.** First audit, refreshed 2026-11-04 against tag **v0.1.0**, commit
**`cedabf02030a3c662fda99b197ceb3ed12790ee7`** — `git rev-parse HEAD` in the pinned checkout
confirms, and the installed `/Applications/MaterialCraft.app` matches (its binary prints
`MaterialCraft 0.1.0 (cedabf0 2026-11-02)`). This is a v0.1.0 app: three days old at audit
time, with a large surface and an explicitly incomplete node library. Every count below was
measured from this tree (the method is in `evidence.md`); the app's own numbers are quoted only
where they are generated from code, and their drift is named.

**Verify against your installed version** — the ArtCraft Launcher auto-updates, so a newer build
may differ. `materialcraft-cli commands`, `nodes` and `--help` are the live contract.

# MaterialCraft

## Overview

MaterialCraft is an open-source (MIT OR Apache-2.0), pure-Rust **node-based material designer**
for procedural, tileable PBR materials — the ArtCraft suite's material-authoring app, built as a
clean-room answer to the professional node-graph material workflow (`ROADMAP.md`: "aims for full
parity with the professional node-based procedural material workflow, with better performance,
every feature drivable by agents"). The repo's own honest estimate is **≈67 %** over an 11-area
weighted table (`ROADMAP.md` "By area": graph editing 75 %, atomic nodes 95 %, node library 45 %,
function graphs 70 %, 3D view 55 %, files 70 %). It runs natively on macOS, Windows, Linux and
FreeBSD, and in the browser through WebAssembly. Source: GitHub `storytold/materialcraft`.

The governing idea matches the rest of the suite: **every user-visible action is an engine
command with a stable id** (`graph.node.add`, `graph.exposed.set`, `file.exportMaterial`, … —
`crates/engine/src/commands.rs`), and the UI, `materialcraft-cli`, the JSON control channel and
the MCP server all dispatch the same registry. A cook is content-addressed and cached, so
re-cooking an unchanged graph is cheap.

## Capabilities (verified)

### One command registry, four surfaces

- **68 engine command ids** (`cmd!(` registrations across `crates/engine/src/{file,material,edit,graph,node,view}_cmds.rs`; `materialcraft-cli commands` lists them with params and enabled state). Ids are namespaced `file.*`, `edit.*`, `graph.*`, `view.*`, `library.*`, `session.*`.
- **CLI `materialcraft-cli` — 11 subcommands** (`apps/materialcraft-cli/src/main.rs` `SUBCOMMANDS`): `info`, `commands [--filter]`, `nodes [--filter] [--category]`, `run <input> <command-id> [params] [-o out.mcraft]`, `batch <script.json>`, `new <template> <out.mcraft> [--size] [--name]`, `cook [--graph] [--set k=v] [--full]`, `export <input> <dir> [--format --depth --pattern --graph --set]`, `render <input> <out.png> [--size --view 3d|2d --scene --node --yaw --pitch --tiling --hq --displacement]`, `mcp [--bridge --token --read-root --write-root]`, `serve [--port --read-root --write-root]`.
- **Control channel** `materialcraft --control <port>` — loopback TCP, one JSON object per line, `{"id","method","params"}` → `{"id","ok":true,"result"}`. **The first request must authenticate**: `auth` with the token from `MATERIALCRAFT_CONTROL_TOKEN` or the per-launch token file `<temp>/materialcraft-control-<port>.token` (`docs/control-protocol.md`). Methods: `ping`, `command.run`, `command.list`, `session.inspect`, `package.open/save`, `bitmap.import`, `outputs.export`, `render`, plus app-only `ui.inspect`, `ui.menu.list`, `ui.menu.invoke`, `ui.set`, `ui.input`, `view.screenshot`, `ui.screenshot`, `ui.resize`. `ui.input` sends synthetic mouse/keyboard events one frame at a time — the fallback when a command does not exist.
- **MCP server** `materialcraft-cli mcp` — **21 tools** (`crates/automation/src/server.rs`): `session_inspect`, `command_list`, `command_run`, `command_batch`, `library_list`, `graph_new`, `node_add`, `node_connect`, `node_param`, `package_open`, `package_save`, `bitmap_import`, `outputs_export`, `view_render`, and the bridge-only `view_screenshot`, `ui_screenshot`, `ui_inspect`, `ui_menu_invoke`, `ui_input`. **Path confinement**: headless mode touches files only below `--read-root`/`--write-root`, and through `command_run` every `file.*` command that takes a path is refused — use the workspace tools.
- **JSON-lines server** `materialcraft-cli serve` — **11 methods** (`crates/automation/src/rpc.rs` `METHODS`), on stdio or on a loopback port behind the same token handshake.

### Materials, graphs, nodes

- **Node graph** with wires, frames (groups), comments, pins, node enable/disable, node base parameters (output size, format, seed, tiling), duplicate/align, and selection helpers (`graph.selectUpstream`/`Downstream`).
- **Exposed graph inputs** — typed inputs an artist or another app can set: `graph.exposed.add`/`set`/`delete`, `file`-level `--set <input>=<value>` on `cook`/`export`/`render`, and `graph.input.bind`/`unbind` to feed an input from a mesh map or image.
- **Dynamic parameters and function graphs** — `graph.node.function` drives a parameter from a function graph of the graph's inputs (`crates/core/src/function.rs`, `docs/control-protocol.md` §Function graphs). Ops include constants, `get_pos`/`get_size`/`get_var`, and samplers.
- **Sub-graphs / instancing** — `graph.createFromSelection` moves nodes into a sub-graph and replaces them with an instance; presets (`graph.preset.save/apply/delete`) store and restore input value sets.
- **Node library** — **227 nodes**, all tileable (`ROADMAP.md` "Headline numbers"; enumerate the live library with `materialcraft-cli nodes --filter <text>`): generators (noises, patterns, bricks, tiles, weathering), filters, flood fill, FX-Map, SVG, Text, 3D noises, material blending, and image inputs.
- **2D and 3D views** — `view.2d` shows any node's output with channel, tiling and histogram options; `view.3d` renders the material on a mesh, with scenes `rounded_cube`, `cube`, `sphere`, `cylinder`, `plane`, `torus`, `material_ball`, plus `view.3d.loadMesh` for an OBJ, glTF or GLB. The 3D view is a **CPU renderer** with parallax, not a GPU tessellated view.

### Cook, export, portable materials

- **Cook** (`graph.cook`, `cook`, `command_run`) with per-node timings and errors, a content-addressed cache across all CPU cores, preview-size caps (`view.previewSize`) and full-size cook (`--full`).
- **Map export** — `outputs.export` / `file.export` writes every output of the graph at full size: **PNG, JPEG, TGA, TIFF, BMP, WebP, EXR, HDR at 8/16/32 bit** (`crates/formats/src/lib.rs` `IMAGE_EXTENSIONS`; CLI `--format`, `--depth`, `--pattern`).
- **Portable materials `.mcmat`** — `file.exportMaterial` cooks the graph and packs a zip: `material.json` (`format: "craft-material"`, version **1**), `maps/<usage>.png` (8-bit sRGB for colour usages, 16-bit linear otherwise, normals OpenGL-style) for `baseColor`, `normal`, `roughness`, `metallic`, `height`, `ambientOcclusion`, `emissive`, `opacity`, `specular`, the exposed parameter values the maps were cooked with, the graph's image inputs, presets, and `source.mcraft` so another app can re-cook (`crates/formats/src/material.rs`). This is the cross-app contract with TextureCraft.
- **`file.sendToTextureCraft`** hands the material to a running TextureCraft; it is an app command, not a headless one.
- **Native package `.mcraft`** — a zip holding `package.json` and embedded resources/images (`crates/formats/src/lib.rs`), byte-based read/write so the same code runs natively and in the browser.
- **Render for review** — `render --size 1024x1024 --view 3d --scene material_ball` writes a PNG with no GPU; `--hq` is a beauty render (real displacement from the height output, ray-traced AO, shadowed key light, 3×3 supersampling).
- **Templates** — `new` builds a package from `empty`, `pbr`, `bricks`, `stone_tiles`, `wood`, `metal_plates`, `rusty_metal`, `lava`, `marble`, `wicker`, `fabric`, `ground` (`crates/engine/src/samples.rs`).

## Known limitations and not-implemented

Do not assign these at v0.1.0:

- **The node library is 227 nodes against ~400 in the reference library** — no scan processing, few grunges, no spline tools or SDF shapes yet (`docs/gaps.md` #1).
- **No GPU 3D view**: the 3D preview is CPU with parallax only; no tessellation, displacement preview or light setups (`docs/gaps.md` #2). `--hq` renders displacement offline, it does not preview it.
- **No mesh-based generators or bakers** — you cannot start a material from a mesh or bake mesh maps inside the app (`docs/gaps.md` #3).
- **Portable materials over MCP**: `.mcmat` export runs from the app and the CLI, but the MCP sandbox refuses path-taking `file.*` commands and exposes no `material_export` tool, so a sandboxed agent cannot hand a material to TextureCraft (`docs/gaps.md` #4). Use the CLI, or an agent with filesystem access.
- **No function loops or reusable functions** — function graphs live on one parameter/node (`docs/gaps.md` #5).
- **One graph at a time**, no minimap or multi-graph tabs (`docs/gaps.md` #9); English-only UI and fixed shortcuts (`docs/gaps.md` #8).
- **No signed/notarized public release yet**; workflows are copied, not run (`docs/gaps.md` #10).
- `ui.menu.invoke` is the only method that behaves like a click; every command runs with defaults and never opens a dialog.

## How to operate

- One-shot build: `materialcraft-cli new bricks out.mcraft --size 2048` → `materialcraft-cli cook out.mcraft` → `materialcraft-cli export out.mcraft maps --format png --depth 8` → `materialcraft-cli render out.mcraft preview.png --size 1024x1024 --hq`.
- Script a package: `materialcraft-cli run out.mcraft graph.node.param '{"param":"scale","value":8}' -o out.mcraft`, or a batch: `materialcraft-cli batch steps.json` with `[{"id","params"}]` or `{"open": <input>, "steps": [...], "save": <out>}`.
- Set exposed inputs without opening a graph: `cook out.mcraft --set roughness=0.4 --set tint="#aa7744"` (`--set` values are JSON, else strings).
- Discover before scripting: `materialcraft-cli nodes --category filter`, `materialcraft-cli commands --filter material`, then `run` the id you found. Parameters are typed — numbers, `[x,y]`, `"#rrggbb"`, enum index, curves `[[x,y],…]`, gradients `[[pos,color],…]`, and typed function values.
- Drive the live app: launch `materialcraft --control <port>`, authenticate with the token from the environment or the token file, then `command.run` / `session.inspect` / `view.screenshot`. Use `MATERIALCRAFT_NO_PREFS=1` for scripted runs so the user's layout is untouched.
- Agent flow: `claude mcp add materialcraft -- materialcraft-cli mcp --read-root . --write-root .`; then `library_list` → `graph_new` → `node_add`/`node_connect`/`node_param` → `view_render` → `outputs_export` → `package_save`. Bridge to a running app with `--bridge <port>`.

## Working with an AI agent

- Treat `command_list`, `library_list` and `nodes` as the discovery contract; never invent a node id or a parameter name. Every command reports whether it is enabled in the current session.
- Verify a cook, don't assume it: `session.inspect` returns node cook errors, output sizes and mean values; `cook` prints per-node timings and errors; `render` gives a PNG you can inspect without a GUI.
- A `.mcmat` is a build artifact plus a recipe: if you need different parameters later, keep the `source.mcraft` and re-cook rather than editing maps.
- Do not attempt to drive the GUI blind; there is no stable window automation beyond `ui.input`, and it is bridge-only.

## Verification protocol

- Round-trip everything: `new` → edit → `cook` → `export` → `render` → reopen the `.mcraft` in a fresh `info` and confirm the node graph and outputs survived.
- Never trust a silent export: check the output directory for the expected map usages and sizes, and open one map.
- `.mcmat` is versioned (`material.json` `version: 1`); a consumer that does not know the version may ignore maps. Record the version you shipped.
- Alpha software: back up `.mcraft` files per session, and update the app only between projects.

## Sources & evidence

- Repo: `https://github.com/storytold/materialcraft` (MIT OR Apache-2.0), tag **v0.1.0**, commit **`cedabf02030a3c662fda99b197ceb3ed12790ee7`**, inspected 2026-11-04.
- Files read: `README.md`, `ROADMAP.md`, `docs/gaps.md`, `docs/control-protocol.md`, `docs/architecture.md`, `Cargo.toml`, `apps/materialcraft-cli/src/main.rs`, `crates/engine/src/commands.rs` and the `*_cmds.rs` registry files, `crates/formats/src/lib.rs`, `crates/formats/src/material.rs`, `crates/automation/src/server.rs`, `crates/automation/src/rpc.rs`, `crates/nodes/src/catalog.rs`, `crates/render/src/preview.rs`, `crates/engine/src/samples.rs`.
- Counts: 68 command ids (`cmd!(` literal ids, non-test), 21 MCP tools (`#[tool` in `server.rs`), 11 JSON-lines methods (`METHODS`), 11 CLI subcommands (`SUBCOMMANDS`), 227 nodes (the repo's generated headline), 12 templates, 7 3D scenes, 9 map usages (`.mcmat` manifest).
- Installed bundle: `/Applications/MaterialCraft.app` prints `MaterialCraft 0.1.0 (cedabf0 2026-11-02)`.
