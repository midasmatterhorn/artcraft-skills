---
name: effectcraft
description: >-
  EffectCraft is an open-source, pure-Rust motion-graphics, compositing and VFX app for macOS,
  Windows, Linux and the web — a clean-room, After Effects-shaped studio with compositions,
  layers, keyframes, 307 effects, expressions, Classic/Advanced 3D, tracking, roto, a render queue
  and Lottie, driven by a CLI, an MCP server, a localhost JSON control channel and JavaScript
  scripting. Trigger this skill whenever the user mentions EffectCraft, `.ecproj`/`.ecprojx`/
  `.ectemplate`/`.ecpreset`, `effectcraft-cli`, its MCP tools or control channel; asks what it can
  or cannot do, which formats/shortcuts it has, or how to script, batch, render, verify, repair or
  troubleshoot it; or describes the job without naming the app ("make a title card", "animate this
  logo", "key this green screen", "render a ProRes", "export Lottie", "open this .aep"). Also use
  it when choosing between EffectCraft and FilmCraft, or preparing/verifying assets for it. Do not
  assume After Effects project files open: they do not.
---

# EffectCraft

Audit basis: this checkout is tag `v0.18.0`, commit `c3600f9b59b109da97871a43a6898683a0163cb1`. The installed `/Applications/EffectCraft.app` reports version `0.18.0` and its binary prints `effectcraft 0.18.0`, so the bundle matches this source exactly. **Verify against your installed version** if the ArtCraft Launcher has auto-updated since. No `references/` directory ships with this skill: every claim is cited inline to the repository.

## Overview

EffectCraft is a free, open-source, clean-room reimplementation of Adobe After Effects 2026 for motion graphics and visual effects: compositions, layers, keyframes, 307 effects, layer styles, expressions, Classic and Advanced 3D, tracking, roto/paint, a render queue and Lottie/timeline interchange. It is pure Rust with no FFmpeg; media codecs come from the sibling FilmCraft project, pinned by revision (`Cargo.toml`). It is **alpha**: the repo self-rates ≈91% feature breadth but ≈45% "ready for real work" (`docs/gaps.md`, `docs/target-app-parity.md`). FilmCraft is the editing/NLE sibling; EffectCraft is the compositor. Source: GitHub `storytold/effectcraft`, MIT OR Apache-2.0.

`v0.18.0` is a maintenance release: the **effect registry is unchanged** (307 effects / 3032 parameters / 280 GPU / 21 categories stand) and the engine command registry gains exactly one id, **`text.deleteSurrounding`**, over v0.17.0's 672. What is new for agents: **each open composition is a tab in the timeline group's tab row, with an overflow menu** (PR #2458); **export pipelines now encode while the next batch renders and skip transparent pixels when compositing** (PR #2518); **Edit-menu keys edit a focused text field**, docked and in panel windows (PR #2459); a workarea-selector hover cursor fix; software-GPU median timeouts fixed; panels moved onto craft-ui's shared docking (PR #2432); the UI migrated to egui 0.37; a startup update prompt with direct self-updating (PR #2420); and Windows installs per-user by default (PR #2493). The shared-module refactor consolidated the `cmd!`/`query!` call sites (697 → 678 occurrences) without changing the registry.

## Capabilities (verified)

### Project and document model

- **Native `.ecproj`** is versioned, pretty-printed JSON headed by `savedBy` and `schema` (currently 2), with `activeComp`/`openComps`/`compTimes`, `settings`, `items`, `nextId`, `renderQueue`, render templates and preferences (`crates/project/src/lib.rs`). Saving re-reads the text before writing and writes atomically; a project whose `savedBy` is a newer version still opens, with a warning.
- **XML project copy `.ecprojx`** is the same data as `EffectCraftProject` XML (lossless); Save a Copy As XML writes it, `file.open` reads it back.
- **Autosave, crash recovery and MCP checkpoints**; `mcp --autosave` writes a checkpoint after each mutating call (`crates/engine/src/autosave.rs`, `docs/agents.md`). Out-of-range values are repaired on open and reported in the result's `repaired` list, not rejected (`crates/project/src/limits.rs`).
- **One project per app process**, with compositions open as tabs restored from `openComps` — **now one tab per open comp in the timeline group's tab row, with an overflow menu**; **36 panel kinds** and **15 named workspaces**, and any panel can move to its own native window (`crates/ui-egui/src/dock.rs`, `docs/architecture.md`).

### Composition, animation, expressions

- **Compositions** use exact integer `Tick` time at 254,016,000,000 ticks/s; `comp.new` defaults to 1920×1080, 29.97 fps, 10 s, and accepts `renderer: classic3D|advanced3D`. Layer kinds cover footage, precomp, solid, text, shape, null, camera, light, 3D model and parametric primitive; adjustment layers are solids with the adjustment switch.
- **Parenting, track mattes, all 38 blend modes and motion blur** are in the document model (`crates/color/src/blend.rs`).
- **Keyframes**: linear/Bezier/hold, per-side speed and influence (Easy Ease), auto/continuous Bezier, roving keys, Keyframe Velocity/Interpolation, and a Graph Editor with value and speed graphs. Time remap/stretch/reverse/freeze are `layer.*` commands.
- **Expressions** run on `boa` with the AE object model (`thisComp`, `thisLayer`, `thisProperty`, `valueAtTime`, `velocityAtTime`, `wiggle`, `temporalWiggle`, `smooth`, `loopIn/Out`, `sampleImage`, `sourceRectAtTime`, `nearestKey`, `propertyGroup`, text style API) and AE legacy array maths (`crates/expr/src/lib.rs`).

### Effects, text, shapes, masks

- **307 registered effects, 3032 parameters, 280 GPU-capable, all 32-bit float, 21 categories, 0 marked partial**, plus 9 Layer Styles with Global Light (`docs/effects.md`, generated from `crates/effects/src/catalog.rs` and checked by the `effects_doc_is_current` test). The README's "306" is one behind the registry. Effects are addressed by id (`ec.<category>.<name>`) or display name.
- **54 built-in animation presets** (8 text animators, 23 backgrounds, 23 transitions) and `.ecpreset` save/apply.
- **Text, shapes and masks**: point/paragraph text with style runs, variable fonts, text animators; shape operators (trim, repeater, round corners, offset, zig zag, twist, wiggle, merge, gradient stroke); masks with **7 modes**, feather, expansion, vertex editing and Mask Interpolation. **New:** `text.deleteSurrounding` deletes characters around the caret (the only registry addition this release).

### 3D, tracking, roto and paint

- **Classic 3D and Advanced 3D**: 3D layers, one/two-node cameras with depth of field, Parallel/Spot/Point/Ambient/Environment lights, ray-cast shadows; Advanced 3D adds PBR materials, six primitives, imported models and environment lighting.
- **Tracking**: point/transform tracking, stabilize, affine/perspective corner-pin tracks, mask tracking including face outline/detailed features, Warp Stabilizer, and a 3D Camera Tracker that creates cameras, solids, nulls, text and shadow catchers.
- **Roto Brush and Object Matte**: stroke/propagate/freeze with optional MobileSAM or classical fallback; face tracking with optional MediaPipe Face Landmarker. Paint strokes/clone source, Liquify and all five puppet pin kinds are commands. **Content-Aware Fill and Scene Edit Detection** run as background jobs with `wait`; **Auto-trace** is synchronous.
- **Cryptomatte picking**: `effect.pickCryptomatte` replaces/edits the effect's Selection with the ID under a point, in one undo step; `effect.cryptomatteAt` only reports.
- **Replace Source**: `layer.replaceSource {layers?, item: id|name}` swaps a footage/precomp/solid layer's source while keeping everything; `layer.revealSource` opens the Project panel on the item.

### Import formats (only what the code registers)

| Kind | Extensions / route | Evidence |
|---|---|---|
| Stills | `png jpg jpeg gif webp tif tiff bmp exr tga hdr psd psb svg pdf ai eps` (17; animated WebP as footage) | `crates/media/src/lib.rs` |
| Film scans | `dpx cin` (8/10/12/16-bit; log shown as stored) | `crates/media/src/dpx.rs` |
| Video | `mp4 m4v mov mkv webm mxf`; H.264, HEVC, VP9, AV1, ProRes, DNxHD, MPEG-2, MJPEG; MXF OP1a/OP-Atom | `crates/media/src/lib.rs`, `docs/file-format-parity.md` |
| Audio | `wav wave bwf aif aiff mp3 mp2 m4a aac flac ogg opus` | `crates/media/src/lib.rs` |
| 3D models | `gltf glb obj stl fbx` (glTF: meshes/PBR/skins/animations; FBX 7.x: meshes/materials only) | `crates/media/src/lib.rs`, `crates/model/src/fbx.rs` |
| Data | `json csv tsv` as data footage (plain `file.import`; Lottie needs `file.importLottie`) | `crates/engine/src/cmd/` |
| Lottie | `.json`, `.lottie` via `file.importLottie`; export `file.exportLottie` | `crates/lottie/` |
| Timelines | `.xml` (FCP7), `.fcpxml`, `.otio`, `.edl`, `.aaf`, `.omf` | `crates/interchange/src/lib.rs` |
| Color / fonts | LUTs `.cube .3dl .csp .spi1d/.spi3d`, CDL; bundled + installed fonts, `EFFECTCRAFT_FONT_DIRS` | `docs/file-format-parity.md`, `crates/text/src/font_dirs.rs` |

`.json` through plain `file.import` is **data footage**, not Lottie. PSD/PDF/AI/EPS import as footage or as a composition (`importAs`).

### Export formats

The Render Queue writes **13 formats** (`crates/project/src/render_queue.rs`):

| Family | Formats |
|---|---|
| Video | H.264 MP4 (+AAC), HEVC MP4 (`hvc1`), AV1 MP4 (`av01`), ProRes MOV (Proxy→4444 XQ; 4444 with alpha), uncompressed 8-bit MOV, WebM (VP9 or AV1 + Opus) |
| Stills | PNG, JPEG, TIFF, OpenEXR (32-bit float) sequences; animated GIF |
| Audio | WAV, AIFF (16-bit PCM) |

Render Settings/Output Modules cover quality, resolution, time span (**Work Area by default**), frame rate, proxy use, overrides, colour depth, field rendering, motion blur, frame blending, skip existing frames, crop/ROI/resize, extra outputs, post-render actions and logs. **New:** export now **encodes while the next batch renders** and **skips transparent pixels when compositing** (faster exports, PR #2518).

- **Single frames** also export as a layered PSD or a multi-layer OpenEXR.
- **Lottie** `.json`/`.lottie` with a `warnings` list.
- **Timeline interchange** `.xml` (FCP7 default), `.fcpxml`, `.otio`, `.edl`, `.aaf`, `.omf`.
- **Essential Graphics template `.ectemplate`** and **animation preset `.ecpreset`**.

### Automation and platform (counts re-measured at this tag)

| Surface | Count at v0.18.0 | vs v0.17.0 | Evidence |
|---|---:|---|---|
| Engine command ids | **672 +1** = registry unchanged except +`text.deleteSurrounding` | `cmd!`/`query!` call sites consolidated 697 → 678 by the shared-module refactor; id sets otherwise identical | `crates/engine/src/cmd.rs` `command_specs()` wires 83 `specs()` modules |
| UI-only command ids | 111 | unchanged (no adds/removes; table moved to `crates/ui-egui/src/commands.rs`) | `crates/ui-egui/src/menus.rs` `pub use commands::UI_COMMANDS` |
| MCP tools | 36 (27 headless + 9 bridge-only) | unchanged, identical tool names | `crates/automation/src/tools.rs` `static TOOLS` (36 `ToolDef` entries; 9 `bridge_only: true`) |
| Control-channel methods | 24 (21 dispatch arms) | unchanged, identical set | `crates/ui-egui/src/control.rs` |
| CLI subcommands | 12 | unchanged; `run --args-file` flag carried | `apps/effectcraft-cli/src/main.rs` |
| Render Queue formats | 13 | unchanged | `crates/project/src/render_queue.rs` |
| Effects / params / GPU / categories / partial | 307 / 3032 / 280 / 21 / 0 | unchanged | `docs/effects.md` |
| Blend modes | 38 | unchanged | `crates/color/src/blend.rs` |
| Layer Styles | 9 | unchanged | `crates/project/src/styles.rs` |
| Menu languages / panel catalogs | 11 / 8 | unchanged | `crates/ui-egui/src/i18n.rs` |

- **CLI** `effectcraft-cli`: the 12 subcommands are `info commands exec run props get set render-frame render bench script mcp`, with `--json`, `--project`, `--demo`, `--empty`, `--save`, `--save-as`, `--bridge`, `--gpu`, per-codec render flags, `--queue` and `--progress`; `run --args-file F` reads one argument per line.
- **MCP** over stdio: **36 tools** — 27 headless and 9 bridge-only (`screenshot`, `ui_inspect`, `ui_elements`, `ui_click`, `ui_drag`, `ui_key`, `ui_type`, `ui_set`, `control`) — plus resources `effectcraft://document` and `effectcraft://commands`.
- **Control channel**: `effectcraft --control <port>` (or `EFFECTCRAFT_CONTROL_PORT`) speaks newline JSON on `127.0.0.1`: **24 methods** — `engine.execute`, `ui.menu.invoke`, `engine.commands`, `ui.menu.list`, `render.frame`, `ui.inspect/elements/set/screenshot/click/move/drag/scroll/key/type`, `ui.panel.show/close`, `ui.playback`, `ui.resize`, `ui.focus`, `ui.viewer.locate/hit`, `ui.timeline.locate`, `app.quit`.
- **Two command tiers**: engine ids run headless (CLI/MCP/`engine.execute`); UI-only ids dispatch only in the live app. No command is a disabled stub.
- **Scripts/ScriptUI**: `.jsx`/`.js` with the AE object model, dockable ScriptUI panels; `script.run`, `file.runScript`, CLI `script FILE.jsx`.
- **WebAssembly effect plug-ins**: `.wasm`/`.wat`, API v1, sandboxed in `wasmi` with no imports.
- **Web build** (`apps/effectcraft-web`) runs the same engine/UI as WASM with OPFS/IndexedDB storage and `window.effectcraft`; it is not the installed macOS app.
- **GPU**: a wgpu compute compositor for Metal/Vulkan/Direct3D 12/WebGPU; CPU is the reference; headless CLI/MCP render on the CPU and say so unless started with `--gpu`. Software-GPU median timeouts were fixed this release.
- **Localization**: menus in **11** languages; panel/tooltip catalogs in **8**. Korean and Italian remain absent.

## Known limitations and not-implemented

- **After Effects projects will not open.** No `.aep`/`.aepx` reader, no `.ffx` presets, no `.mogrt` templates, no AE SDK plug-ins. Only `.ecproj`/`.ecprojx`, `.ecpreset` and `.ectemplate` are native.
- **Fidelity against After Effects is mostly unmeasured.** The live comparisons (scalar ease plus Tint, Tritone, Black & White, Exposure, Levels (Individual Controls), Curves, Luma Key, Extract, 4-Color Gradient and Fill) match After Effects 2026 renders within 1–3/255, Brightness & Contrast up to 6.2/255. Everything else is self-graded — never promise AE-identical renders (`docs/fidelity/README.md`).
- **Alpha stability.** `docs/gaps.md` still lists open crash reports; re-check the tracker rather than quoting this skill.
- **No hardware video decode/encode** (VideoToolbox, NVENC, Quick Sync, VA-API). HEVC/AV1 have no B-frames, multi-reference or SAO/CDEF; Opus has no FEC/DTX.
- **Output/import gaps**: no 16-bpc uncompressed, AVI, MXF output, DNxHR, DPX/Targa/Photoshop sequences or ProRes RAW; no USD/USDZ, Substance `.sbsar`, camera raw, HEIF/AVIF, BRAW/R3D/ARRIRAW.
- **FBX/DPX/PDF caveats**: FBX is 7.x only, with no animation, skinning, cameras or lights; DPX/Cineon log values are shown as stored; PDF/AI/EPS import lacks JPX/JBIG2 and Illustrator procset EPS.
- **Scripting gaps**: no `.jsxbin`, no Startup/Shutdown script folders, no script shortcuts, no Legacy ExtendScript engine mode, no BridgeTalk.
- **The macOS `.app` contains no CLI** — get the universal `effectcraft-cli` from its separate release zip or build it. **The control channel has no authentication**, binds `127.0.0.1`, serves at most 16 connections, times out at 60 s and rejects lines over 4 MiB.
- **Docs drift — trust code/runtime.** Several docs still say 306 effects and 411 commands; the registries say 307/3032 and 672+1 ids. `docs/gaps.md` gap 3's "no PR CI gate" is stale.
- **`.prproj` is not read or written** — convert to FCP7 XML in Premiere first.

## How to operate

### Launch (macOS)

```sh
open -a EffectCraft                                  # empty Untitled Project (not the demo)
open -a EffectCraft Project.ecproj                   # open a project
open -a EffectCraft --args --control 9877 --demo     # agent-driven window + demo project
/Applications/EffectCraft.app/Contents/MacOS/EffectCraft --control 9877 --demo
```

Flags: `--control <1-65535>` (or `EFFECTCRAFT_CONTROL_PORT`), `--demo`, `--empty`, `--home`, `--version`; after `--` every argument is a file. Unknown options exit 1 before the window opens. The app starts **empty** by default, unlike most one-shot CLI commands, which start with the demo.

### CLI

`effectcraft-cli` is a separate macOS release zip (signed/notarized) or `cargo build --release -p effectcraft-cli`; it is **not** inside the `.app`. `<comp>` is an id, name or `-` (active comp); `<layer>` is an id, `#n` or name; values are JSON or bare strings.

| Subcommand | What it does |
|---|---|
| `info` | version, mode (headless/bridge), command and effect counts, project and active comp |
| `commands` / `exec --list` | list engine commands; `--filter TEXT`, `--enabled`, `--schemas` |
| `exec <id> [json]` | run one command |
| `run <id> [json] …` | run several in order, stopping at the first error; `--args-file F` |
| `props <comp> <layer>` | property tree with paths; `--flat`, `--time S`, `--depth N` |
| `get` / `set <comp> <layer> <path> [value]` | read/write one property |
| `render-frame` | PNG frame; `--time/--frame`, `--max-side/--scale`, `--transparent` |
| `render` | one comp (`--comp`, `--out`, codec flags) or the project queue (`--queue`); `--progress` |
| `bench` | render timings, GPU vs CPU, or `--ops` everyday-operation timings |
| `script FILE.jsx` | run AE-style JavaScript; `--eval CODE` |
| `mcp` | MCP server on stdio; `--autosave`, `--bridge PORT`, `--automation-read-root`, `--automation-write-root` |

- **Most commands open the demo project** unless you pass `--project F.ecproj`, a positional `*.ecproj`, or `--empty`. `commands`, `script` and `mcp` start empty.
- `--save` writes back to the opened project, `--save-as F` writes a copy. `--gpu` attaches the GPU compositor; CPU is the default.
- `render` needs `--out` (or `--queue`); `render --comp …` renders exactly one item; `--progress` prints progress lines on stderr.
- `render-frame` accepts `--time`, `--frame`, `--max-side`, `--scale`, `--transparent`; `--template T.ectemplate --values values.json` renders one Essential Graphics instance.
- `mcp --automation-read-root DIR / --automation-write-root DIR` (repeatable) confine agent file access.

### MCP

`effectcraft-cli mcp` serves JSON-RPC 2.0 over stdio, one message per line. It has **36 tools**:

| Group | Tools |
|---|---|
| Commands | `list_commands`, `describe_command`, `execute_command`, `command_list`, `command_run`, `batch`, `command_batch` |
| Project / properties | `get_project`, `doc_inspect`, `get_comp`, `get_layer`, `get_property`, `set_property`, `add_keyframe`, `add_effect`, `list_effects`, `list_fonts`, `get_state` |
| Files / history / scripting | `open_project`, `save_project`, `undo`, `redo`, `history`, `run_script`, `script_ui` |
| Render | `render_frame`, `render_preview` |
| Bridge-only (9) | `screenshot`, `ui_inspect`, `ui_elements`, `ui_click`, `ui_drag`, `ui_key`, `ui_type`, `ui_set`, `control` |

Resources `effectcraft://document` and `effectcraft://commands`. `batch` is atomic (`$N.key` references); `command_batch` stops at the first error by default. A `renderQueue.render` call with `_meta.progressToken` emits progress notifications and can be cancelled.

### Control channel

`effectcraft --control 9877` accepts one JSON object per line and replies per line. **24 methods**: engine/menus (`engine.execute`, `ui.menu.invoke`, `engine.commands`, `ui.menu.list`), render (`render.frame`), inspect (`ui.inspect`, `ui.elements`, `ui.set`, `ui.screenshot`), input (`ui.click`, `ui.move`, `ui.drag`, `ui.scroll`, `ui.key`, `ui.type`), panels/playback (`ui.panel.show`, `ui.panel.close`, `ui.playback`, `ui.resize`, `ui.focus`), viewer/timeline (`ui.viewer.locate`, `ui.viewer.hit`, `ui.timeline.locate`) and `app.quit`. `ui.elements` lists widgets drawn in the last frame `{id,label,rect}`; `ui.screenshot` returns a PNG. **Edit-menu keys now edit a focused text field** (docked or in a panel window).

### Document model and workflow

One project per app process in one main window; each open composition is a tab in the timeline group's tab row. Panels follow After Effects, dock/float on craft-ui's shared docking, and any panel can move to its own native window. Each layer carries a property tree addressed by paths such as `transform/position`, `effects/#1/blurriness` or `@<uid>`.

1. Create a composition (`comp.new`) and add layers (`layer.new*`, `file.import`, `layer.replaceSource`).
2. Animate (`prop.set`/`prop.addKey`) and ease (`keys.select` + `keys.easyEase`).
3. Apply effects (`effect.apply`), edit `effects/#1/...`, preview and save.
4. Export via `renderQueue.add` + `renderQueue.render`, or Lottie/timeline/template commands.

```sh
effectcraft-cli exec comp.new '{"name":"Main","width":1920,"height":1080,"frameRate":30,"duration":3}' --empty --save-as main.ecproj
effectcraft-cli exec layer.newText '{"text":"Hello","name":"Title","size":160,"fill":"#ffffff"}' main.ecproj --save
effectcraft-cli run main.ecproj \
  prop.addKey '{"layer":"Title","path":"transform/position","time":0,"value":[-400,540]}' \
  prop.addKey '{"layer":"Title","path":"transform/position","time":1,"value":[960,540]}' \
  keys.select '{"keys":[{"layer":"Title","path":"transform/position","time":0},{"layer":"Title","path":"transform/position","time":1}]}' \
  keys.easyEase '{"which":"both"}' --save
effectcraft-cli render main.ecproj --comp Main --out title.mp4 --format h264 --progress
```

Each headless CLI invocation is a new session: edits survive only if saved; group selection-dependent steps in one `run` (or one MCP session).

### Open / save / export, exact formats

- **Open** `.ecproj`, `.ecprojx`, or `.xml` whose root is `EffectCraftProject`; `file.importProject` merges another project. **Save** `.ecproj`, or XML when the path is `.ecprojx`/`.xml`; Save a Copy, Save a Copy As XML and Increment and Save exist.
- **Export** the 13 Render Queue formats, single-frame layered PSD or ProEXR, Lottie, timeline formats, `.ectemplate`, `.ecpreset`. A `.xml` path is ambiguous: `file.open` expects an EffectCraft XML project, `file.importTimeline` expects FCP7 XML — use `.ecprojx` for projects.
- **Rejected**: `.prproj` and every AE-native format above.

### Keyboard shortcuts (only verified ones)

`Cmd+N` New Composition, `Cmd+K` Composition Settings, `Cmd+Shift+X` Trim Comp to Work Area, `Cmd+Alt+N` New Project, `Cmd+O` Open, `Cmd+S` Save, `Cmd+Alt+Shift+S` Increment and Save, `Cmd+Shift+S` Save As, `Cmd+I` Import, `Cmd+M` Add to Render Queue, `F9` Easy Ease, `Cmd+Alt+K` Keyframe Interpolation, `Cmd+Shift+K` Keyframe Velocity, `Cmd+Alt+H` Toggle Hold, `Cmd+Alt+T` Enable Time Remapping, `Cmd+G`/`Cmd+Shift+G` Group/Ungroup Shapes, `Cmd+Opt+/` Replace Source. Property reveals `A/P/S/R/T/M/F/E/L/U` are in `docs/agents.md` §Timeline. Shortcuts are command data; for anything else read `effectcraft-cli commands --json` — do not invent shortcuts.

## Working with an AI agent

### Choose the surface

- **Headless (preferred)**: `effectcraft-cli exec/run` for one-shots or `effectcraft-cli mcp` for a persistent session; `mcp --autosave` checkpoints dirty work after each mutating call.
- **Live app**: start `effectcraft --control 9877`, then `mcp --bridge 9877` or the raw control channel. **Web**: no TCP channel; use `window.effectcraft`.

### Prepare inputs

- Convert unsupported sources: camera raw/AVI/BRAW/R3D/USDZ/Substance → H.264/ProRes/WebM or PNG/EXR/TIFF sequences; 3D → glTF/GLB/OBJ/STL/FBX 7.x; audio → WAV/AIFF; data → JSON/CSV/TSV.
- Image sequences: pass one numbered file with `sequence: true` (or import the folder); keep media next to the project (relative paths resolve against the project folder on open).
- Query `list_fonts`/`text.fonts` first; extra fonts come from `EFFECTCRAFT_FONT_DIRS`.

### Inspect and repair project files

- `.ecproj` is documented by the code: `savedBy`, `schema`, `activeComp`, `openComps`, `settings`, `items`, `nextId`, `renderQueue`. Item, layer and property ids share one counter; keep `nextId` above every id. Never bump `schema`.
- Prefer commands over JSON surgery; after a hand edit, reopen and check the `repaired` list in `file.open`'s result.
- For moved media: `footage.missing`, `footage.relink {item, path}` or `file.relinkFootage {folder, dryRun}`.
- `layer.revealSource` is the safe way to find a layer's Project item in the UI.

### Scripting

- Scripts run against the AE object model; `run_script`/`script` keep edits (wrap in `app.beginUndoGroup()`/`endUndoGroup()`). The CLI `script` exits 1 with `file:line:col`.
- Reads are allowed under the script's own folder and the project folder; writes and network require Settings ▸ Scripting & Expressions.
- Setting an array property to the wrong length throws `Array is not of the correct dimension` — pad or trim arrays in generated scripts.

### Verify exports

- Read the result: `renderQueue.render` returns per-item statuses; CLI `render` exits 1 if any item failed.
- Re-import the output and render a frame to prove it decodes; use `--transparent` for alpha.
- Lottie: inspect `warnings`; timeline: inspect `warnings`, `missing` and `prerendered`.
- Odd comp sizes: H.264/HEVC dimensions round down to even.

### Do not

- Try to open `.aep`/`.aepx`/`.aex`/`.ffx`/`.mogrt`/`.prproj`; there is no reader.
- Drive the GUI without `--control` (discover widgets with `ui.elements`), edit a `.ecproj` the app has open, or expose the control port (no authentication).

### Concurrency and safety

- Save early; `open_project`/`file.newProject` replaces a dirty project without a prompt. Without `--autosave`, MCP work is memory-only.
- After a broken bridge connection, mutating calls have an **unknown outcome**; inspect before retrying.
- Scripts may read files only in their own or the project's folder; confine agent file access with `--automation-read-root` / `--automation-write-root`.

## Verification protocol

Alpha-software discipline; run this for every delegated task.

1. **Copy first.** Work on a scratch `.ecproj` (`--save-as` / Save a Copy), never the only copy; update the app only between projects.
2. **Round-trip in a fresh process.** New → comp/layers/keyframes/effects → save → reopen via `info --project` → render a frame and a short movie.
3. **Check both artifacts.** A `render-frame` PNG at a known time and the final MP4/MOV/sequence; confirm dimensions, duration, audio and alpha.
4. **Check the time span.** Queued items default to **Work Area**; CLI `render` defaults to the whole comp unless `--work-area`.
5. **Check format constraints.** H.264/HEVC even dimensions; ProRes 4444 for alpha; WebM VP9 for VP9 alpha; WAV/AIFF are 16-bit PCM; EXR is 32-bit float.
6. **Interchange and Lottie:** inspect warnings/missing/prerendered, re-import the result.
7. **Report, don't hide.** Give the exact command, version, file and observed result. Fidelity differences against After Effects are expected and are the most useful report.

## Sources & evidence

- Repository: `https://github.com/storytold/effectcraft`; inspected tag `v0.18.0`, commit `c3600f9b59b109da97871a43a6898683a0163cb1` (`git rev-parse HEAD`, 2026-10-29). Fast-moving alpha — verify against your installed version.
- Installed app at this pin: version 0.18.0, bundle `ai.storyteller.effectcraft`; `Contents/MacOS` holds only the app binary (no CLI). No GUI was launched; only `--version` was run.
- Read: `README.md`, `Cargo.toml`, `docs/` (`agents`, `mcp`, `control-protocol`, `architecture`, `file-format-parity`, `gaps`, `effects`, `effects-parity`, `fidelity/README`, `footage`, `plugins`, `scripting-parity`, `web`); `apps/effectcraft-cli/src/main.rs`, `apps/effectcraft/src/{main,control_server}.rs`; `crates/project/src/{lib,render_queue,styles,limits}.rs`; `crates/engine/src/cmd.rs` (registry) and `crates/engine/src/cmd/`; `crates/{media,interchange,lottie,expr,keyframe,plugin,automation,script}/src`; `crates/effects/src/{lib,catalog}.rs`; `crates/color/src/blend.rs`; `crates/ui-egui/src/{control,commands,dock,menus}.rs`. Counts were re-measured from code and diffed against a fetched `v0.17.0` ref; no build, test or render was run.
- Delta method: `cmd!`/`query!` call sites 697 (v0.17.0) → 678 (v0.18.0) after the shared-module refactor; unique literal ids 563 → 564 (+`text.deleteSurrounding`, nothing removed); `static TOOLS` `ToolDef` entries 36 → 36; `docs/effects.md` 307/3032 unchanged (test-enforced).
