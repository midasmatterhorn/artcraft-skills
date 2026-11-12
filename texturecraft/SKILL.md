---
name: texturecraft
description: >
  TextureCraft is the ArtCraft team's open-source, pure-Rust 3D texture-painting app — a clean-room
  reimplementation of the Adobe Substance 3D Painter texturing workflow (`ROADMAP.md`): paint PBR
  materials straight onto 3D models in layers with masks and generators, bake mesh maps (with a live
  bake preview that streams each map onto the model as it finishes), drive smart materials, and export
  texture sets for any engine (glTF, Unreal, Unity, Blender, Godot, OpenPBR). Trigger this skill
  whenever the user mentions TextureCraft — or a `.tcraft`, `.tcmat` file — asks what it can or cannot
  do, which mesh formats it opens, how to bake ambient occlusion / curvature / normal maps, how to
  script, automate, batch or headlessly drive it (texturecraft-cli, MCP, the JSON control channel),
  wants textures painted or exported for a game engine, needs baked maps verified (including maps
  baked in another app and imported by file name), or troubleshoots it. Also when the job is
  described without naming the app — "paint rust onto this model", "bake an AO map for this mesh",
  "export a glTF PBR texture set", "make a smart material from these layers", "reimport the mesh
  without losing my paint". Do not guess its capabilities from Substance Painter knowledge — read
  this first.
---

**Audit basis.** Refreshed 2026-11-12 against tag **v0.6.1**, commit
**`34a196190fe2daa2f43017a0f32b254cca4836f2`** — `git rev-parse HEAD` in the pinned checkout
confirms, and `git describe --tags` says v0.6.1. The installed bundle (see Sources & evidence)
prints `TextureCraft 0.6.1 (34a1961 2026-11-12)`. This skill previously described v0.4.0
(`16e9d21516434a63ac457f49ffd09005f649c02f`).

**v0.4.0 → v0.6.1 delta.** `git diff --stat v0.4.0..HEAD` shows **322 files changed,
+30,258/−4,287** (the shallow clone holds both trees; the range also spans the intermediate
releases, whose tags are not in it). The engine registry moves 172 → **177** ids with **nothing
removed**: `bake.preview`, `textureSet.meshMap.import`, `tool.fillSelection`, `tool.swapMaskValue`,
`effect.colorSelection.pick`. **Live bake preview** is the headline: `ui.bake.start` and
`ui.bake.cancel` on the control channel bake in the background one map at a time and stream each
finished map onto the model (`crates/engine/src/bake/streamed_bake.rs`,
`crates/engine/src/bake_preview.rs`); painting is refused while a preview shows, each set's bake
lands as one undo step, `ui.inspect` reports `baking`/`bakeStatus`/`bakePreview` and
`session.inspect` reports `bakePreview`. `bake.run`, the CLI `bake` and MCP `bake` still make every
map at once and never preview. **Bake mode draws its setup** — high poly, cage, UV seams, low poly
and where the transfer rays miss (`crates/render/src/bake_visualization.rs`,
`crates/render/src/{cage,high_poly}_gpu.rs`, `crates/bake/src/cage/high_poly_reach.rs`,
`crates/ui-egui/src/bake_mode/`). **Curvature** now
bakes from the mesh by default (`crates/core/src/bake/curvature_method.rs`); the normal-map path
follows the surface and gives one band per edge (`crates/bake/src/map/normal_curvature.rs`, test
`a_rounded_edge_is_one_convex_band`); curvature generators gained a mode and seven detail sizes
(`crates/core/src/layer/curvature_detail.rs`, `crates/compose/src/curvature_sizes.rs`). **Symmetry**
gets a movable plane (`symmetryOffset`), a selectable axis and an angle span for radial copies, and
a toolbar on/off that keeps the settings (`crates/paint/src/stamp_source.rs`,
`crates/ui-egui/src/symmetry/`, `tool.brush` params). The **path tool** previews a draft and its
points are editable in either view (`crates/engine/src/path_draft.rs`); **polygon fill** grows to a
whole source polygon as well as the triangle, UV island or mesh (`crates/engine/src/fill_mode.rs`),
takes a box with an intersection/contained-center hit test, can restrict a 3D box to what the camera
sees, and works from 2D-view points and boxes (`tool.fillSelection`, `tool.click`,
`crates/engine/src/fill_hit_test.rs`); Shift+click draws straight lines in the 2D view. **Effects**:
`effect.set` swaps a filter's type in place, levels edit input range, gamma and output range on the
histogram (`crates/ui-egui/src/levels_editor.rs`), the filter slot opens the picker
(`crates/ui-egui/src/filter_slot.rs`), and a color selection picks its ID colors from the ID map
(`effect.colorSelection.pick`). **Layers panel** thumbnails are asynchronous and never touch the
main composite (`crates/engine/src/thumbs.rs`, `crates/compose/src/thumb.rs`); the UI state (layout
and prefs) is stored as `ui.json` with a legacy RON fallback (`crates/ui-egui/src/ui_state_store.rs`);
smart materials preview on the orb (`crates/engine/src/orb_preview.rs`); a shelf image dropped on a
set can become a channel or a mask (`crates/ui-egui/src/decal_drop.rs`). **Saving** compresses
entries on several threads under a cores/RAM budget (`crates/formats/src/project_file/entries.rs`,
prefs `reserved_cores` and `save_ram_percent`), while **opening** enforces one decompressed-byte
budget — default 8 GiB, `prefs.project_open_limit_gib`, minimum 1 — and rejects overlapping ZIP
entries (`crates/formats/src/project_file/{load_budget,project_open_limit}.rs`). Help › Check for
Updates is the menu item that took parity to 59/59 and is skipped at start when `--control` drives
the app (`crates/ui-egui/src/updates_ui.rs`, `apps/texturecraft/src/main.rs`).

**v0.3.0 → v0.4.0 delta (historical).** 216 files changed (+14,040/−5,788, 86 commits in the GitHub
compare). The engine registry moved 162 → 172: `camera.bookmark1`…`camera.bookmark9` (Ctrl+1…Ctrl+9),
`bake.tile.set`, `bake.cage.paint` and `bake.cage.reset` were added; `bake.autoRebake` and
`bake.autoRebake.run` were removed, so nothing re-bakes itself. Bake settings became a nested
per-map `BakeSettings` model (`crates/core/src/bake/`, `crates/engine/src/bake/`): `bake.settings`
takes `model`, `patch` and `preserveEnabled` and targets `ts`; `bake.run` takes the same parameters
and returns `{baked, tracer}`. The baked-map set shrank 12 → 10 (`ColorMap` and `WorldDirection`
removed, `crates/core/src/bake/baked_map.rs`); six smart masks took the set to 24; three new Views
entries took menu parity to 58/58. Old `.tcraft` files whose bake settings or baked maps no longer
parse are recovered field by field with defaults and a log warning
(`crates/formats/src/project_file/recovery.rs`). Masks and content evaluate **every** neighbourhood
filter in stack order (`crates/compose/src/eval.rs`); exports sample baked maps through the working
tile layout (`crates/formats/src/export/mod.rs`).

**Verify against your installed version** — the ArtCraft Launcher auto-updates, so a newer build may
differ; every count quoted here was re-measured at this tag with the method recorded in `evidence.md`.

# TextureCraft

## Overview

TextureCraft is an open-source (MIT OR Apache-2.0), pure-Rust 3D texture-painting application — the
ArtCraft suite's clean-room answer to Adobe Substance 3D Painter, aiming at that texturing workflow
with better performance, a smaller footprint and every feature drivable by agents (`ROADMAP.md`).
Its own weighted estimate is **≈94%** done across 11 areas (`ROADMAP.md` "Honest parity estimate
(2026-11-04)"); that estimate predates v0.6.1 and has not been refreshed. It runs natively on macOS
(universal, signed, notarized), Windows, Linux, FreeBSD and in the browser via
WebAssembly/WebGPU-or-WebGL2 (`README.md`, `ROADMAP.md` Platforms). Source: GitHub
`storytold/texturecraft`. The workspace is 11 crates (`automation`, `bake`, `compose`, `core`,
`engine`, `formats`, `geom`, `paint`, `render`, `texel`, `ui-egui`) plus three apps
(`apps/texturecraft`, `apps/texturecraft-cli`, `apps/texturecraft-web`).

The one governing idea: **everything is an engine command with a stable id** (`layer.add.fill`,
`bake.run`, `edit.undo`, … — `docs/control-protocol.md`), and the UI, `texturecraft-cli`, the JSON
control channel and the MCP server all run the same registry (**177 unique command ids** at v0.6.1;
the generated menu doc counts **59 of 59 menu items live**, `docs/parity.md`, regenerated by
`TC_UPDATE_PARITY=1 cargo test -p texturecraft-ui-egui parity`). Programmatic calls never open
dialogs; `session.inspect` reports every layer, mask, effect, fill source, generator detail, per-tile
`bakeEnabled` flag, painted tile count and the bake preview state, so an agent can verify work
without screenshots.

## Capabilities (verified)

**Count status at v0.6.1** (method in `evidence.md`). Changed since v0.4.0: engine ids **177** (172),
menu items **59/59** (58/58), control methods **15** (13). Unchanged at v0.6.1: CLI 10 subcommands,
MCP 22 tools, serve 17 methods, 31 filters, 24 smart masks, 72 procedural + 21 smart materials, 23
procedurals, 6 environments, 67 brush alphas, 18 brush presets, 21 channels, 32 blend modes, 10 baked
maps, 10 export presets, 8 texture formats, 12 mesh import / 5 mesh export formats, 9 built-in
meshes, 10 UI languages, project `format_version` 2.

### One command registry, four surfaces

- **Engine registry: 177 unique command ids** (every `cmd!`/`query!` registration with a string id
  across `crates/engine/src`, tests excluded; `texturecraft-cli commands [--filter]` prints the live
  set for the build in front of you). All **59/59** target menu items are wired (`docs/parity.md`).
- **CLI** `texturecraft-cli` — **10 subcommands** (`apps/texturecraft-cli/src/main.rs`
  `SUBCOMMANDS`): `info`, `commands [--filter]`, `run <input> <command-id> [params-json] [-o
  out.tcraft]`, `batch <script.json>`, `bake <input> [-o out] [--resolution px] [--maps id,id]`,
  `export <input> <dir> [--preset --format --padding --size]`, `render <input> <out.png> [--size
  WxH --view 3d|2d --camera name --yaw --pitch --samples --bounces] [--cpu]`, `new <input>
  <out.tcraft> [--resolution] [--sample]`, `mcp [--bridge --token --read-root --write-root
  --automation-read-root --automation-write-root]`, `serve [--port --read-root --write-root
  --automation-read-root --automation-write-root]`; plus `--version`/`--help` (hand-rolled parser,
  not clap).
- **Control channel** — `texturecraft --control <port>`, loopback TCP, one JSON object per line,
  8 MiB request cap. **Token-authenticated**: the first request on every connection must be
  `{"id":0,"method":"auth","params":{"token":"…"}}`; the token is `TEXTURECRAFT_CONTROL_TOKEN`
  (16–1024 printable ASCII characters) or a fresh random token the app writes to
  `<temp>/texturecraft-control-<port>.token` (owner-only) and prints to stderr. One auth attempt,
  10 s deadline, 16 connections, 600 s idle (`docs/control-protocol.md`,
  `crates/automation/src/security.rs`, `apps/texturecraft/src/control_server.rs`). **15 methods**:
  `ping`, `command.run`, `command.list`, `session.inspect`, `ui.inspect` (now with `baking`,
  `bakeStatus` and `bakePreview`), `ui.menu.list`, `ui.menu.invoke`, `ui.bake.start`, `ui.bake.cancel`,
  `ui.set` (layout/dock/prefs/keymap — `prefs` covers `language`, `brightness` (4 levels), `accent`
  (7 colours), `system_title_bar`, `project_open_limit_gib`, `reserved_cores`, `save_ram_percent`),
  `viewport.screenshot {view: 3d|2d}`, `ui.screenshot`, `ui.resize` (640–7680 points),
  `debug.paintTest {from,to,frames}` (a real per-frame scripted stroke), `debug.frames` (frame timing
  breakdown). Scripted runs can set `TEXTURECRAFT_NO_PREFS` to start from defaults in a throwaway
  state.
- **MCP server** `texturecraft-cli mcp` — **22 tools** (`crates/automation/src/server.rs` `#[tool]`
  entries; unchanged at v0.6.1): `session_inspect`, `command_list`, `command_run`, `command_batch`
  (stops at first error, ≤256 steps), `project_new` (9 built-in meshes: material_ball, sphere, cube,
  rounded_cube, cylinder, torus, plane, crate, udim_plane; templates), `project_open`, `project_save`,
  `mesh_import` (glTF/GLB, FBX binary+ASCII, COLLADA, USD usda/usdc/usdz, Alembic, OBJ, PLY, STL),
  `mesh_reimport` (**`preserveStrokes: true` re-projects paint where UVs changed**; off by default),
  `mesh_export` (obj, glb, usda, usdc, usdz), `bake_mesh_add` (high-poly + cage), `resource_import`,
  `material_save`/`material_load` (`.tcmat` smart materials; load also takes MaterialCraft
  `.mcmat`/`.mcraft`), `textures_export` (preset-driven), `bake`, `paint_stroke` (points in viewport
  pixels, sharing one space with `viewport_render`), `viewport_render` (headless PNG ≤2048 px,
  optional path-traced `samples` 1–4096 on GPU or CPU), bridge-only
  `viewport_screenshot`/`ui_screenshot`/`ui_inspect`/`ui_menu_invoke`. **No MCP tool starts the live
  preview bake** — bridged tools call fixed methods only; use the control channel for
  `ui.bake.start`. **Path confinement**: headless mode touches files only below
  `--read-root`/`--write-root` (forward-slash relative paths; `..`, absolute paths, drive letters,
  device names, symlink/junction escapes refused); through `command_run`, every `file.*` command is
  refused except `file.close`, `file.removeUnused` and `file.reimportMesh` without a `path`, and so
  is any command given a `path`/`dir` at the top level **or in a `files` entry** — use the workspace
  tools. Replies capped at 8 MiB JSON / 5 MiB PNG / 256 batch steps.
- **Headless JSON-lines server** `texturecraft-cli serve` — **17 methods** (`crates/automation/src/rpc.rs`
  `METHODS`, unchanged at v0.6.1): `ping`, `methods`, `session.inspect`, `command.list`,
  `command.run`, `command.batch`, `project.open`, `project.save`, `mesh.import`, `mesh.reimport`,
  `mesh.export`, `bake.mesh.add`, `resource.import`, `material.save`, `material.load`,
  `textures.export`, `render`.

### Painting, layers and materials

- **Paint on the 3D mesh or the 2D UV view**: brush (size/flow/stroke-opacity/spacing/hardness/angle/
  follow-path, jitters, tangent or camera alignment, angle fade, backface culling, lazy mouse, X/Y/Z
  mirror + radial symmetry with a movable plane, selectable axis and angle span, pen pressure),
  eraser, **projection with image stencils** (hold S), polygon fill (triangle/source polygon/UV
  island/mesh, box selection with an intersection or contained-center hit test, visible-only in 3D,
  points and boxes in 2D), **path and lasso fill**, **particle brush**, smudge, clone (V + click sets
  source), colour picker, Shift+click straight lines in both views, **quick mask** (Y), **geometry
  decals** and **text** (`docs/features.md` §Paint in 3D). **67 procedural brush alphas** (31
  generated shapes + 36 stencil glyphs, `crates/paint/src/alphas.rs`) plus any imported image; **18
  brush presets** in three groups, with user presets saved as `.tcbrush`
  (`crates/paint/src/presets.rs`, `crates/engine/src/brush_preset_cmds.rs`).
- **Layer stack**: paint, fill, folder and **instance** layers; **32 blend modes per channel** with
  per-channel opacity; white/black/painted masks, **mask with height**, smart masks, generators;
  **31 library filters** (`crates/engine/src/filter_lib.rs` `FILTERS`: adjustments, blur/sharpen/
  high-pass, bevel, glow, edge detect, warps, mosaic, baked lighting, four material finishes);
  **geometry masks**; anchor points; copy/paste across texture sets, flatten, save layers/folders as
  `.tcmat` smart materials; **levels** edited on a live histogram (input range, gamma, output range);
  a filter slot that swaps a filter's type in place via `effect.set` while keeping its stack
  position, blend and opacity; **24 smart masks** that all expose their preset id (`mask.smart.list`
  to enumerate, `mask.smart.apply {name, layer?}` to replace a layer's mask;
  `crates/engine/src/smart_masks.rs`). X flips the mask paint value while painting a mask
  (`tool.swapMaskValue`). The Layers panel shows live content, mask and per-effect thumbnails
  rendered off the UI thread (`crates/engine/src/thumbs.rs`, `crates/compose/src/thumb.rs`).
- **Bundled library**: **72 procedural materials and 21 smart materials** (93 shelf entries), **24
  smart masks**, **23 procedurals**, **6 procedural environments** plus imported HDR/EXR panoramas
  (`crates/engine/src/materials.rs` `MATERIALS`, `crates/core/src/layer.rs` `ProceduralKind`,
  `crates/core/src/project.rs` `ENVIRONMENTS`). Seven generator kinds (`GeneratorKind::ALL`);
  curvature generators carry a mode and seven detail sizes (`crates/core/src/layer/curvature_detail.rs`).
  A shelf material can be dropped on the texture set under the cursor (as a channel or a mask), and
  hover shows a large preview (`crates/ui-egui/src/shelf.rs`, `crates/ui-egui/src/decal_drop.rs`).
  **MaterialCraft materials**: `material.load` accepts a `.mcmat` portable material or `.mcraft`
  package as a fill layer, re-cooked through MaterialCraft's command line with the set's baked mesh
  maps (`docs/control-protocol.md` §MaterialCraft materials, `crates/engine/src/link_cmds.rs`).
- **Channels**: 21 `Channel` variants per texture set — base color, metallic, roughness, height,
  normal, emissive, opacity, AO, specular level, specular, glossiness, clear coat weight/roughness/
  normal, sheen weight/colour/roughness, anisotropy level/angle, subsurface scattering weight,
  transmission (`crates/core/src/channel.rs` `pub enum Channel`). Texture sets 128–8192 px,
  **UDIM/UV tiles** with per-tile working resolution and `$udim` export.
- **Viewport**: PBR with IBL, ACES/linear tone mapping (a dropdown in the Display panel), depth of
  field, displacement, 4× MSAA + idle temporal accumulation, channel/mesh-map/mask/UV-checker views,
  saved cameras (also imported from glTF/FBX/COLLADA/USD) with **Ctrl+1…9 bookmarks**
  (`camera.bookmark1`…`9`), top-bar layout and perspective/orthographic dropdowns, a draggable 3D/2D
  divider, a right-click Properties popup at the cursor (`crates/ui-egui/src/properties_popup.rs`),
  and **Rendering mode (F10)** — a progressive path tracer on GPU compute (the repo claims ~25× CPU)
  or CPU, with environment importance sampling and an edge-aware denoiser.

### Bake and export

- **Bake mesh maps** — **10 baked maps** (unchanged at v0.6.1): normal, world-space normal, ID,
  ambient occlusion, curvature (from the mesh by default, or from the normal map), position,
  thickness, height, bent normal, opacity (`crates/core/src/bake/baked_map.rs` `BakedMap::ALL`). GPU
  ray tracing (the repo claims ~12× the CPU path) or all CPU cores; high-poly meshes with cage,
  frontal/rear distances, average normals, match by mesh name; 2D cage and skew paint
  (`bake.cage.paint`/`bake.cage.reset`, `bake.skew.*`); mesh maps can be baked or imported as images
  (`textureSet.meshMap.set`). Fresh settings default to 64 AO rays, cosine distribution, 180° spread
  and linear AO attenuation (`crates/core/src/bake/ray_settings.rs`,
  `crates/core/src/bake/ambient_occlusion_attenuation.rs`). In the app, Bake mode draws the high
  poly, cage, UV seams and low poly, and where the transfer rays miss
  (`crates/render/src/bake_visualization.rs`, `crates/ui-egui/src/bake_mode/`).
- **Live bake preview (app/control channel only)**: `ui.bake.start {ts?}` opens Bake mode and bakes
  the selected sets in the background, one map at a time, showing each finished map raw on the model
  (`crates/engine/src/bake/streamed_bake.rs`, `crates/engine/src/bake_preview.rs`); `bake.preview
  {show?: follow|material|map:<id>}` reads or pins what the view shows; `ui.bake.cancel` stops;
  painting is refused while a preview shows; each set's bake applies as one undo step. A cancelled
  bake leaves the set it was baking unchanged and keeps sets already finished. `bake.run`, the CLI
  `bake` and the MCP `bake` tool make every map in one pass and never preview.
- **Per-set bake settings**: each texture set owns a nested `BakeSettings` (common
  resolution/antialiasing/dilation plus per-map parameters). `bake.settings` reads or edits it:
  `model` replaces the whole settings object, `patch` changes only the named fields (nested
  `maps.ao.parameters.rays.rays`, …; `null` clears optional fields), `preserveEnabled` keeps the
  set's Include-in-Bake flag, and flat parameters (`resolution`, `antialiasing`, `dilation`, `ao`,
  `thickness`, `bentNormal`, `rays`, `maxDistance`, `curvatureMethod`, `positionMode`, `maps`,
  `enabled`, …) apply last. It returns `[{ts, settings, model}]` per targeted set
  (`crates/engine/src/bake/mesh_map_command.rs`). `bake.run` takes the same parameters plus
  `ts`/`cpu` and returns `{baked, tracer}`; **there is still no auto-rebake at v0.6.1**.
- **Per-tile bake selection**: `bake.tile.set {ts?, tile: 1002, enabled: false}` excludes one UV
  tile; `session.inspect` reports each tile's `bakeEnabled`; excluded tiles keep their previous baked
  pixels (`crates/engine/src/bake/tile_command.rs`).
- **Batch mesh-map import**: `textureSet.meshMap.import {files: [{path, map?}]}` places up to 512
  images by file name — `Body_ao.png`, `Body_world_normal.png`, `Body_ao.1001.png` for a UV-tiled
  set — into the set and slot the name names, and lists what it could not match
  (`crates/engine/src/meshmap_import_cmds.rs`, `crates/engine/src/meshmap_file_name.rs`). New
  Project can import baked maps at creation (`crates/ui-egui/src/new_project_advanced.rs`). The
  command takes host paths, so `command_run` refuses it through MCP; import each file with
  `resource_import` + `textureSet.meshMap.set` there.
- **Export presets**: `Document channels + Normal + AO`, `glTF PBR Metal Roughness`, `Unreal Engine
  (Packed)`, `Unity HDRP (Mask Map)`, `Unity Standard (Metallic Smoothness)`, `Blender (Principled
  BSDF)`, `Godot 4 (ORM)`, `OpenPBR (separate maps)` (coat/fuzz/anisotropy/transmission/subsurface
  maps), `Separate maps`, `Mesh maps` — **10 built-ins** plus **user output templates** (per-channel
  packing, converted maps, JSON shareable) (`crates/formats/src/presets.rs`). Texture formats: PNG,
  JPEG, TGA, TIFF, BMP, WEBP, EXR, HDR — **depth is per format** (PNG/TIFF 8 or 16, EXR 16 or 32
  float, HDR 32, the rest 8), plus UV padding, size override, OpenGL/DirectX normals, colour-space
  conversion of colour maps and `$udim` tiles (`crates/formats/src/export/mod.rs`). Mesh export to
  OBJ (+MTL and maps), textured GLB (clear coat + sheen) and USD (clear coat), **5 formats**
  (`crates/engine/src/file_cmds.rs` `MESH_EXPORT_FORMATS`).

## Known limitations and not-implemented

At v0.6.1, do not assign these:

- **No auto-rebake.** After changing `bake.settings`, the mesh, high polys or the skew/cage paint,
  run `bake.run` (or start the app's bake) yourself; nothing bakes in the background.
- **The live preview is app/control-channel only.** There is no MCP tool for `ui.bake.start`, and
  `bake.preview` reports `{active: false}` when no bake is running. Headless `bake`, MCP `bake` and
  the CLI `bake` make every map at once with no preview. Painting is refused while a preview shows.
- **`textureSet.meshMap.import` is desktop-only and refused through `command_run`** because it takes
  host paths; in automation import one image per map with `resource_import` then
  `textureSet.meshMap.set`, or use the command from `texturecraft-cli run` on desktop.
- **Old projects are recovered, not converted.** v0.6.1 still writes `format_version: 2`; older files
  load, newer files are refused (`crates/core/src/project.rs` `FORMAT_VERSION`,
  `crates/formats/src/project_file/mod.rs`). A `.tcraft` whose bake settings or baked map entries no
  longer deserialize opens with defaults for the unreadable fields (and drops unreadable maps) under
  a log warning (`crates/formats/src/project_file/recovery.rs`); re-bake to restore those maps.
  Baked pixels of older UDIM projects keep their old layout — the app does not convert baked pixels.
- **Opening a project has a decompressed-size budget**: 8 GiB by default, raised with
  `ui.set {"prefs":{"project_open_limit_gib":16}}` (1 GiB minimum). The limit applies to new loads;
  per-entry caps and the overlap check still apply. `ui.set`'s `prefs` object replaces the whole
  prefs object and omitted fields take their defaults, so send every pref you need to keep. A save is
  parallel on native targets (one core left to the UI, 50 % of available RAM as the in-flight entry
  budget by default) and single-threaded in the browser.
- **`mesh_reimport` does not preserve paint by default.** Pass `preserveStrokes: true` (MCP/command)
  to re-project painted pixels where UVs changed; without it the mesh is replaced with no
  re-projection.
- **The macOS app bundle contains only `TextureCraft`** — no `texturecraft-cli`. Get the CLI from the
  release's separate macOS CLI zip (`packaging/macos/package.sh`), or build it. `Contents/MacOS`
  verified.
- **Pen tilt is not exposed** by the windowing layer, and pen pressure is unavailable on Linux, macOS
  and desktop browsers (`ROADMAP.md` M2).
- **HDF5 Alembic is unsupported** (Ogawa only) and Alembic animation reads the first sample only
  (`ROADMAP.md` Project and files gaps).
- **Sheen and anisotropy do not export through USD** (UsdPreviewSurface has no such inputs; GLB and
  OpenPBR maps carry them) (`ROADMAP.md` Export gaps).
- **There is no 3D cage-editing overlay** — Bake mode draws the cage and 2D cage/skew can be painted,
  but the roadmap still lists 3D cage editing as a gap (`ROADMAP.md` Baking).
- **The bundled asset library is smaller than the reference app's**, and translations have had no
  native-speaker review (`ROADMAP.md` Materials/UI gaps).
- **Hardware ray tracing is not used** (compute shaders only; wgpu's ray queries need `unsafe`,
  which the workspace forbids) (`ROADMAP.md` Viewport gaps).
- The CLI/control/MCP surfaces run commands with defaults and never open dialogs; only
  `ui.menu.invoke` behaves like a click (`docs/control-protocol.md`). Bridge mode cannot touch files
  itself — the app does — so path tools are unavailable there and `project_save` without a path
  becomes File › Save.

## How to operate

- Headless one-shot (positional order: input first; `run` takes the command id then optional JSON
  params, with `-o` last):
  `texturecraft-cli new builtin:material_ball out.tcraft` → `texturecraft-cli bake out.tcraft
  --resolution 1024 --maps ambientOcclusion,curvature` → `texturecraft-cli export out.tcraft
  textures/ --preset "glTF PBR Metal Roughness" --format png` → `texturecraft-cli render out.tcraft
  preview.png --size 1024x1024` (`apps/texturecraft-cli/src/main.rs`; `docs/features.md` §Built for
  agents).
- Script a session: `texturecraft-cli run project.tcraft layer.add.fill '{"color":"#336699","roughness":0.2}'
  -o result.tcraft` — commands are the same ids `commands --filter` lists. A batch script is a step
  list or `{"open", "steps", "save"}` with paths relative to the current directory.
- Edit bake settings precisely: `texturecraft-cli run out.tcraft bake.settings
  '{"ts":"all","patch":{"maps":{"ao":{"parameters":{"rays":{"rays":128}}}}}'`; bake with overrides via
  `texturecraft-cli run out.tcraft bake.run '{"ts":"all","maps":["ambientOcclusion","curvature"],"resolution":2048}'`.
  Curvature reads the mesh by default; pass `"curvatureMethod":"normalMap"` for the normal-map path.
  Exclude a tile with `bake.tile.set {"tile":1002,"enabled":false}`.
- Import baked maps baked elsewhere: `texturecraft-cli run out.tcraft textureSet.meshMap.import
  '{"files":[{"path":"Body_ao.png"},{"path":"Body_curvature.png"}]}'` — each file lands in the set
  and slot its name names; check `assigned` and `unmatched` in the reply.
- Paint with symmetry: `tool.brush {"symmetryOn":true,"symmetryOffset":[0,0.5,0],"symmetryAxis":"y",
  "symmetryAngleSpan":180}`; box-fill a region with `tool.fillMode {"mode":"polygon"}` then
  `tool.click {"x0":420,"y0":300,"x1":700,"y1":560,"viewport":[1280,800]}` (or `{uv0,uv1}` in the
  2D view); draw a path with `tool.path {"points":[[…]],"closed":false}` and commit it.
- Swap a filter in place: `effect.set {"effect":12,"filter":"blur","radius":5}` — the stack position,
  blend and opacity stay; naming the current filter edits it without resetting omitted parameters.
- Cameras: `camera.add {"name":"Hero"}` saves the current view; `camera.bookmark1`…`9` (or
  `camera.select {name}`) jump to it; `texturecraft-cli render scene.tcraft hero.png --camera Hero`
  renders through it.
- Watch a bake land (needs the app): launch it with `--control 7878` (`open -a TextureCraft
  --args --control 7878`; `--args` apply on a fresh launch, so quit a running copy first, or run the
  `TextureCraft` binary inside the bundle directly), read the token from stderr or
  `<temp>/texturecraft-control-7878.token` (or set `TEXTURECRAFT_CONTROL_TOKEN`), send
  `{"id":0,"method":"auth","params":{"token":"…"}}`, then
  `{"id":1,"method":"ui.bake.start","params":{"ts":0}}`; poll `ui.inspect` (`baking`, `bakeStatus`,
  `bakePreview`) and `viewport.screenshot` until `baking` is `null`; pin a map with
  `command.run {"id":"bake.preview","params":{"show":"map:curvature"}}`; stop with
  `{"id":2,"method":"ui.bake.cancel"}`.
- Agent flows: `claude mcp add texturecraft -- texturecraft-cli mcp --read-root . --write-root .` (or
  a `.mcp.json`); bridge to the running app with `--bridge 7878`. Typical run: `project_new` →
  `command_run layer.add.fill` → `bake` → `command_run mask.add.black` → `command_run
  effect.add.generator {"generator":"edgeWear"}` → `session_inspect` → `viewport_render` →
  `project_save` → `textures_export` (`docs/control-protocol.md`).
- Verify without screenshots: `session.inspect` / `session_inspect` return project, mesh, texture
  sets (including each tile's `bakeEnabled`), layer stack with each generator's curvature mode and
  detail weights and each color selection's colors/tolerance, tool, camera, display, history and
  `bakePreview`; `bake.settings` returns the effective settings per set; `debug.frames` reports frame
  timing after a scripted stroke.
- `TEXTURECRAFT_NO_PREFS=1` isolates a scripted run from the user's saved layout/settings (and the
  startup update check is skipped whenever `--control` is given).

## Working with an AI agent

- Register the MCP server per `docs/control-protocol.md` (headless with roots, or bridged). In bridge
  mode the app reads and writes its own files, so path tools are unavailable and `project_save`
  without a path performs File › Save.
- Every tool call maps to one control method; `command_run` accepts any engine command id except the
  refused `file.*` set and path-taking commands (including a `files` entry with a `path`).
  `command_list {filter}` is the discovery contract.
- Use the control channel, not MCP, when you need the app's live bake: `ui.bake.start`, then poll
  `ui.inspect`, then `viewport.screenshot`. Use MCP `bake` for unattended bakes — it returns when all
  maps are done and shows nothing.
- Painted strokes and renders share one pixel space: coordinates for `paint_stroke` can be read off a
  `viewport_render` image at the default 1280×800. `tool.strokeUv` paints in UV space when the 2D
  layout is what you have.
- Baking is GPU-first with `cpu: true` fallback; use `bake.settings` `patch` for one parameter instead
  of hand-building a whole model, and always pass `ts` when more than one texture set must change.
  Curvature changed default: at v0.6.1 it bakes from the mesh unless you ask for `normalMap`.
- Import maps baked in another app by file name (`textureSet.meshMap.import` from the CLI or the app),
  then verify `assigned`/`unmatched`; through MCP, import one image per map with `resource_import` +
  `textureSet.meshMap.set`.
- For reusable material libraries use the `.tcmat` round trip (`material_save`, then `material_load`
  above the selection); `material_load` also ingests MaterialCraft `.mcmat`/`.mcraft` packages.
- Treat a recovered project as untrusted until re-baked: check the log for the recovery warning, run
  `session.inspect`, re-bake the affected sets, then re-export.
- Reimport a changed mesh with `mesh_reimport {"path":"model.glb","preserveStrokes":true}` and confirm
  `session_inspect` reports `modified: true` before saving.

## Verification protocol

1. `texturecraft-cli commands --filter <text>` — the live registry for the build in front of you;
   never trust any static number in this skill over it.
2. `session.inspect` after each mutation — layer stack, mask targets, fill sources, generator detail,
   tile `bakeEnabled`, baked maps, `modified` flag, painted tile counts and `bakePreview`.
3. Bake: `bake.settings` for the effective per-set model, `bake.run` for its `{baked, tracer}` result;
   `session.inspect` confirms the baked maps per texture set. In the app, `ui.bake.start` plus
   `ui.inspect` confirms the streamed stage, and `bakePreview` names the map on screen.
4. Imported maps: the reply's `assigned` and `unmatched` lists are the receipt; a file that matches no
   set or map, a duplicate slot or tile, and a UV-tiled set missing a tile are all listed, not
   silently dropped.
5. Exports: `textures_export` returns the written files; check names, packing, per-format bit depth
   and UDIM tiles against the preset.
6. Frame-loop work (recordings, perf): `debug.frames` before/after; `strokeEnd` in its result names
   the frame a scripted stroke committed.
7. Re-derive counts at v0.6.1: engine registry **177**, MCP `tools/list` **22**, serve `methods` **17**,
   control methods **15**, CLI `--help` **10 subcommands**, menu parity **59/59** (`docs/parity.md`).

## Sources & evidence

- Repo: https://github.com/storytold/texturecraft — inspected at tag **v0.6.1**, commit
  **`34a196190fe2daa2f43017a0f32b254cca4836f2`** (2026-11-12), inspection date **2026-11-12**, shallow
  checkout pinned to the tag; `git rev-parse HEAD` and `git describe --tags` both confirm v0.6.1.
  MIT OR Apache-2.0; workspace version 0.6.1 (`Cargo.toml`).
- Installed app: `/Applications/TextureCraft.app` — `TextureCraft 0.6.1 (34a1961 2026-11-12)`, bundle
  `ai.storyteller.texturecraft`, `CFBundleShortVersionString` 0.6.1; `Contents/MacOS` holds only
  `TextureCraft` (no CLI); GUI never launched (`--version`/`--help` only).
- Read: `README.md`, `ROADMAP.md`, `AGENTS.md`, `Cargo.toml`, `docs/{control-protocol,features,parity,
  architecture,localization-parity}.md`, `apps/texturecraft-cli/src/main.rs`,
  `apps/texturecraft/src/{main,control_server}.rs`, `crates/automation/src/{server,rpc,workspace,
  security,budgets}.rs`, `crates/engine/src/{commands,inspect,filter_lib,smart_masks,file_cmds,
  tool_cmds,color_selection_cmds,meshmap_import_cmds,meshmap_file_name,fill_mode,fill_hit_test,
  path_draft,thumbs,orb_preview,bake_preview}.rs`, `crates/engine/src/bake/{mesh_map_command,
  tile_command,bake_task,streamed_bake}.rs`, `crates/core/src/{channel,blend,project,layer}.rs`,
  `crates/core/src/bake/{baked_map,curvature_method,curvature_settings,ray_settings}.rs`,
  `crates/core/src/layer/{curvature_detail,curvature_mode}.rs`, `crates/bake/src/map/
  {curvature,normal_curvature}.rs`, `crates/bake/src/cage/{high_poly_reach,cage_shell}.rs`,
  `crates/formats/src/{presets.rs,export/mod.rs,mesh_import/mod.rs,project_file/{mod,recovery,
  entries,load_budget,project_open_limit}.rs}`, `crates/compose/src/{eval,thumb,curvature_sizes}.rs`,
  `crates/paint/src/{alphas,presets,stamp_source}.rs`, `crates/geom/src/primitives.rs`,
  `crates/render/src/bake_visualization.rs`, `crates/ui-egui/src/{control,menus,i18n,state,levels_editor,
  filter_slot,decal_drop,properties_popup,new_project_advanced,updates_ui,ui_state_store}.rs`,
  `crates/ui-egui/src/symmetry/`, `crates/ui-egui/src/bake_mode/`.
- Counts measured from code, not docs: 177 engine command ids (full `cmd!`/`query!` extract), 22 MCP
  `#[tool]` entries, 17 serve `METHODS`, 15 control methods (+`auth`), 10 CLI subcommands, 59/59 menu
  items (`docs/parity.md`, generated + test-enforced), 31 `FILTERS` defs, 24 `SMART_MASKS`, 72 `m(` +
  21 `sm(` materials, 23 `ProceduralKind`, 7 `GeneratorKind`, 6 `ENVIRONMENTS`, 67 alpha-library
  entries (31 shapes + 36 glyphs), 18 brush presets, 21 `Channel` variants, 32 `BlendMode` variants,
  10 `BakedMap`s, 10 built-in export presets, 9 built-in meshes, 10 UI languages, `FORMAT_VERSION` 2.
- Where repo docs disagree, the code counts win and the drift is noted in `evidence.md` §3:
  `ROADMAP.md` says 63 procedural materials, 30 filters and 19 channels (code: 72 / 31 / 21) and its
  parity estimate and current-focus list predate this release; `docs/features.md` lags polygon fill
  modes and symmetry controls; `README.md`'s "8, 16 or 32 bits" shorthand is per-format;
  `docs/control-protocol.md`'s CLI `--version` sample still shows an old 0.1.0 string.
- Per-claim tiering and the count method: `evidence.md` next to this file, plus
  `references/automation-surfaces.md` for the full control/MCP/serve/CLI surface tables.
