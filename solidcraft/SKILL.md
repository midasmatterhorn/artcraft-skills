---
name: solidcraft
description: >-
  SolidCraft is an open-source parametric 3D CAD application in pure Rust (by Tangency Labs,
  independent clean-room; not an Autodesk/Dassault product): sketches with constraints and
  parameter-driven dimensions, a parametric feature timeline (extrude, revolve, sweep, loft,
  fillet, chamfer, shell, draft, holes, threads, patterns, mirror, split, combine), sheet metal,
  plastic enclosure features, assemblies with joints and motion studies, physical materials with
  mass properties, and STEP/IGES/3MF/STL/OBJ/GLB/URDF/DXF interchange. Desktop app, browser app,
  headless CLI and a 22-tool MCP server all run the same 634-command registry. Trigger this skill
  whenever the user mentions SolidCraft (or `.sc`, `solidcraft-cli`, "SolidCraft MCP", the control
  channel on 27878), asks what it can model or open/export, wants an agent to build or edit a
  parametric part (enclosure, bracket, plate, flange), drive the control channel, script a build,
  run the oracle, or troubleshoot it — and equally when they never name it but describe parametric
  CAD work ("model a case for this board", "sketch, constrain and extrude", "export a STEP of this
  bracket"). Do not assume Fusion/SolidWorks behaviour: read this first.
---

# SolidCraft

**Audit basis.** Refreshed **2026-11-12** against tag **v0.40.1**, commit **`0c5292285a7e9331a780c11a2d55f22d8e1c9118`** — `git rev-parse HEAD` in the pinned checkout confirms it. The installed bundle matches: its binaries print `solidcraft 0.40.1` and `solidcraft-cli 0.40.1`. The previous release this skill described was **v0.30.1** (`8e2b0cd60d14b4152b12b8f1fdb2bcfdcd8c52f4`).

**v0.30.1 → v0.40.1 delta.** The pinned diff touches 13,422 files. The kernel underneath the app changed: `Cargo.toml` drops `truck-modeling`/`truck-topology`/`truck-shapeops`/`truck-stepio` and builds `crates/kernel` on the vendored `solidcore/` (the safe-Rust port of NVIDIA's SMLib, Apache-2.0) through `crates/smlib`, with the mesher in `solidcore-tess` and the STEP reader in `solidcore-step`. The registry grew 570 → **634** ids (+64, none removed), including 25 `panel.*` and 5 `layout.*` commands (`crates/engine/src/cmd/panels.rs`), notes, `construct.axis/plane/point`, `selection.get`, `body.repair`, `sketch.move_points`, `sketch.point.divide`, `sketch.replace`, render coat/texture commands and `view.navigator`; `surface.fillet` is still the only planned id (`crates/engine/src/cmd/surface.rs`). MCP gained `cancel` (22 tools) and now builds on the new shared `mcp-server` crate. The control channel became **off by default** (`crates/ui-egui/src/prefs.rs`: `agent_control: bool = false`), takes effect at once when toggled (`crates/ui-egui/src/control_switch.rs`), and gained 36 documented methods/commands around panels, layout, `ui.operations`, `ui.recover` and `document.export/import/saved`. Design format 48 → **54** (`crates/doc/src/format/v49`…`v54`); GLB export now has its own format-registry row. The binary embeds five agent skills, not four (`crates/mcp/src/skill_reference.rs`).

**v0.29.0 → v0.30.1 delta.** 578 files changed; the registry grew to 570 rows in the v0.30.1 `docs/features.md`, MCP went 20 → 21 (`compare_picture`), `.scdwg` drawings and FreeCAD/Rhino import were added (per the previous audit), and glTF became import-only.

**Verify against your installed version** — the ArtCraft Launcher auto-updates, so a newer build may differ. Every count quoted here was re-measured at this tag; the method for each is in `evidence.md`.

## Overview

SolidCraft is an open-source parametric 3D CAD application in pure Rust by Tangency Labs (MIT OR Apache-2.0). Sketch, constrain and build solids on an editable feature timeline; change a dimension and the model rebuilds. It is **independent and clean-room**: behaviour is designed from public documentation and general CAD conventions, reference tests use analytic values and FreeCAD as an external oracle, and it is not affiliated with any CAD vendor (`README.md` Disclaimer; `NOTICE`). **Status: early but usable for simple parts** — the generated oracle reports **90/90** reference parts passing, while `README.md` and `docs/capabilities.md` still say "75 of 76" (trust `docs/oracle.md` and `solidcraft-cli oracle`). Since v0.40 the B-rep kernel is `solidcore`, a safe-Rust port of NVIDIA's SMLib (`solidcore/README.md`, `crates/smlib/src/lib.rs`). One command registry serves the desktop app (egui), the browser app, the CLI, the control channel and the MCP server.

## Capabilities (verified)

### The command registry is the API (start here)

- **634 engine commands**, dotted lower-case ids across `crates/engine/src/cmd/` (249 `.rs` files, tests included). Exactly one is planned: `surface.fillet` refuses with issue #769 (`crates/engine/src/cmd/surface.rs`; `docs/features.md` marks the row). The installed CLI's `commands` output is the authority; at this tag it agrees with `docs/features.md` row for row.
- **561 of 634 commands describe both typed input and output JSON Schemas** (2020-12); 73 describe neither, including the planned `surface.fillet` (`describe_command` for every id in one headless session). The repo's own coverage test currently only warns: `crates/engine/src/schema/coverage_tests.rs` has `SCHEMA_RULE_STRICT: bool = false`, and `crates/engine/src/schema/unconverted.txt` exempts 18 old commands. New commands are expected to ship both schemas.
- **Sketch commands return `created: {points, curves, constraints, dimensions}`** — stable, never-reused ids usable immediately in `sketch.dimension`, `sketch.constraint.*` and `sketch.delete` (71 command parameter docs carry the note; `created_doc!` in `crates/engine/src/cmd/mod.rs`). Lengths are mm; expressions take parameters and units (`crates/doc/src/expr.rs`).
- **Every surface runs the same ids**: toolbar, command palette, JSON scripts, `solidcraft-cli exec`, the control channel's `engine.execute`, and MCP's `execute`/`batch`. A command never opens a dialog; dialogs are UI on top of commands.

### Automation surfaces

- **MCP server — 22 tools**: `list_commands`, `describe_command`, `execute`, `batch`, `undo`, `redo`, `inspect_design`, `measure`, `body_topology`, `set_parameter`, `check_parameters`, `screenshot`, `compare_picture`, `export`, `new_design`, `open`, `save`, `crash_reports`, `running`, `pending`, `cancel`, `skill_reference` (`crates/mcp/src/tools.rs`). stdio JSON-RPC, protocol revisions 2025-06-18 / 2025-03-26 / 2024-11-05 (`crates/mcp-server/src/server.rs`). Headless it runs its own session (`--in part.sc` to start from a file); with `--connect HOST:PORT` it drives the running app so you can watch.
- **Control channel**: loopback-only, token-authenticated, 52 documented protocol methods plus the 30 `panel.*`/`layout.*` commands (`docs/control-protocol.md`). The token is 256-bit, written to `control/PORT.token`, with the port in `control/current.port`; 16 connections at once, 16 MiB per line, 60 s per request (3600 s for a batch) (`crates/control/src/auth.rs`; `docs/control-protocol.md` "Limits").
- **Real UI input, when a workflow has no command**: `ui.click`, `ui.drag`, `ui.move`, `ui.key`, `ui.text`, `ui.scroll`, `ui.menu`, `ui.pick`, `ui.handles`, `ui.at`, `ui.screenshot`, `ui.render`, `ui.documents`, `ui.operations`, `ui.prefs` (`docs/control-protocol.md` "UI"). `ui.agent_cursor` shows the agent gliding to each pick.
- **CLI — 24 verbs** (`apps/solidcraft-cli/src/main.rs`): 19 listed (`run`, `eval`, `script`, `bench-open`, `bench-agent`, `bench-assistant`, `snapshot`, `render`, `exec`, `commands`, `recipe`, `oracle`, `kernel-cases`, `fuzz`, `mcp`, `crashes`, `licences`, `gpu`, `icon`) and 5 unlisted (`inspect`, `fuzz-one`, `licenses`, `bench-edit`, `save-stress`). `mcp setup` (`mcp install`) registers the server with OpenCode, Claude Desktop, Claude Code or Cursor; `--allow-path DIR` widens what an agent may touch.
- **Scripts** are a JSON list of the same commands: `{"commands": [{"command": "sketch.create", "params": {"plane": "XY"}}, …]}` (`docs/scripts.md`). `script design.sc --out rebuild.json` extracts a design's history as such a script; `eval` returns measurements as JSON.

### Modelling (what it can actually build)

- **Sketches**: lines, rectangles, circles, arcs, polygons, slots, ellipses, fit/control splines, conics and text on origin planes, offset planes or planar faces; construction geometry, projection, trim/extend, corner fillets/chamfers (`docs/capabilities.md`; `sketch.*` 129 commands).
- **Constraints and dimensions**: coincident, point-on-curve, horizontal/vertical, parallel, perpendicular, tangent, curvature (G2), equal, concentric, collinear, midpoint, symmetry, fix; linear, aligned, horizontal, vertical, point-to-line, line-to-circle, point-to-circle, circle-to-circle, radius, diameter, angle, arc sweep, arc length and slot length, parameter-driven. Their own solver places fixed-relative points exactly and uses Levenberg–Marquardt for the rest, reporting remaining degrees of freedom; over-constraining edits are rejected (`docs/capabilities.md`).
- **Features**: extrude, revolve, sweep, loft, fillet/chamfer, shell, draft, holes (presets in `docs/hole-presets.md`), threads (`docs/threads.md`), patterns, mirror, split, combine, move, press/pull, offset face, replace face, rib, web, emboss, coil, pipe, boundary fill, bounding solid — on a parametric timeline with rollback and suppression (`solid.*` 36, `timeline.*` 22).
- **Parameters and configurations** with unit-aware expressions and rules (`parameters.*` 13, `config.*` 8); **assemblies** with components, occurrences, joints, motion links, motion studies, contact sets, interference and BOM (`joint.*` 19, `motion.*` 11, `contact.*` 7, `assembly.*` 4); **sheet metal** with flanges, contour flanges, hems, fold/unfold and flat pattern plus DXF and bend-table export (`sheet.*` 13, `docs/features.md`); **plastic enclosure** features (`plastic.*` 7); **physical materials** with mass in Properties (`material.*` 8, `appearance.*` 10, `docs/physical-material-cards.md`); **notes** (`note.*` 4); **point clouds** (`pointcloud.*` 5, `docs/point-clouds.md`); a **Render workspace** with GPU rendering, studio lighting and image export (`render.*` 65, `docs/render-workspace.md`).
- **Built-in agent skills**: the repo's `skills/` ships 19 Agent-Skills folders. Five are embedded in the binary and served by MCP `skill_reference`: `solidcraft-modeling`, `solidcraft-editing`, `solidcraft-checking`, `solidcraft-mechanisms` and `solidcraft-sheetmetal` (`crates/mcp/src/skill_reference.rs`). **Read `skill_reference` before a non-trivial model** — it is the project's own discipline for driving the engine, and it lists the traps.

### Files: open and save

- **Native design `.sc`** is a ZIP container: `container.json` (`solidcraft-container/1`), `document.json` (document format **54**) and content-addressed `blobs/<sha256>.<step|mesh|png|jpeg>` (`crates/format/src/container.rs`; `docs/design-container.md`). A `.json` path saves the plain JSON design; `.solidcraft` and `.solvecraft` still open and keep their names (`crates/io/src/lib.rs` `DESIGN_EXT`/`DESIGN_EXTS`; `docs/compatibility.md`).
- **Format registry, 19 rows** (`crates/io/src/formats.rs`): design (`.sc`/`.solidcraft`/`.solvecraft`/`.json`), STEP and IGES import+export, FreeCAD `.FCStd` and Rhino `.3dm` import, STL/3MF/OBJ import+export, glTF import only, GLB export only, PLY/XYZ/PTS point-cloud import, URDF export, DXF drawing import and current-view DXF export, SVG drawing import. Commercial codecs are not compiled in (`Cargo.toml`: cadmpeg without f3d/sldprt/inventor/catia/creo/nx/sat).
- **Commands**: `file.save` (`format: container|json`, `compression: fast|compact`, optional geometry `cache`, optional display `preview`), `file.export` (`step|stp|iges|igs|3mf|3mf-tagged|stl|stla|obj|glb|urdf|json`, with quality/mesh options), `file.export_step`, `file.export_stl`, `file.export_3mf`, `file.export_obj`, `file.export_urdf`, `file.save_mesh`, `file.export_view_dxf` (`curves: lines|arcs`, `zero: target|origin`), `file.send_to_slicer`/`file.slicers` for installed slicers.
- **Forward compatibility**: a file whose format number is newer than the build opens with a warning, reads what it can and keeps the rest on save (`crates/format/src/newer.rs`). Builds before 0.40 refuse such a file with "saved by a newer SolidCraft".
- **Drawings are groundwork only**: `.scdwg` has a document model and a container reader/writer (`crates/doc/src/drawing.rs`; `crates/io/src/design/drawing.rs`; `DRAWING_EXT` in `crates/io/src/lib.rs`), but nothing in the app or engine opens one — there is no caller of `read_drawing_file` outside the IO crate and tests, no `drawing.*` command, and the drawings milestone is still listed as unmerged in `ROADMAP.md`. The Insert Drawing dialog places SVG and DXF files on a sketch (`crates/ui-egui/src/dialogs_insert_drawing.rs`), not `.scdwg`.

### Platform and packaging

- Desktop app (egui) with multiple designs as tabs; the same engine runs as a WebAssembly browser app (`apps/solidcraft-web`, `docs/browser-api.md`), a headless CLI and an MCP server (`docs/architecture.md`).
- macOS is signed with a Developer ID and notarized; Windows installers are unsigned (SmartScreen) (`README.md` Download). ARM64 and 32-bit builds exist.
- Headless screenshots use a GPU device and fall back to a CPU rasterizer, saying which (`docs/mcp.md` `screenshot`).
- The desktop app also hosts an agent **Assistant** panel for ACP/API agents; desktop only (`docs/agent-chat.md`).

## Known limitations and not-implemented

- **Early but usable for simple parts** — the project's own words. The oracle covers 90 simple reference parts; complex multi-body workflows are not proven to that standard (`docs/oracle.md`; `docs/capabilities.md`).
- **One planned command**: `surface.fillet` refuses with issue #769. Any other tool you cannot find in `solidcraft-cli commands` / `describe_command` should be treated as absent.
- **Drawings are milestone work**: `.scdwg` has a document model and reader/writer, but no UI or command opens it; the Insert Drawing dialog places SVG/DXF on a sketch only (`ROADMAP.md`; `crates/ui-egui/src/dialogs_insert_drawing.rs`; `crates/io/src/design/drawing.rs`).
- **No CAM**: Send to Slicer exports to a slicer; it does not generate toolpaths (`ROADMAP.md` "Manufacturing / CAM").
- **Kernel limits**: G2 fillets only on straight edges between planar faces with planar ends; some coincident curved booleans can still fail; mass properties come from fine tessellation, not exact integration (`ROADMAP.md` "Known limitations").
- **Format 54 is forward-only**: 0.40.x opens a file from a newer build with a warning and preserves what it cannot read (`crates/format/src/newer.rs`), but builds before 0.40 refuse it; 0.40.0 draws a centre-placed box with its centre as the corner (`crates/doc/src/format/v54/box-centred.rs`).
- **The control channel is off on a new install**. A bridged `solidcraft-cli mcp` starts anyway but every call fails with `no SolidCraft app is listening at HOST:PORT` until the channel is enabled or the app is launched with `--control PORT` (`docs/mcp.md`; `crates/ui-egui/src/prefs.rs`).
- **MCP file access is fenced**: save/open/export/screenshot only inside the design's folder, folders the agent opened or saved in, the recovery folder, the server scratch folder, and `--allow-path` entries; hidden folders and files are out of reach. A `save` elsewhere is an error — ask the user to add `--allow-path`, do not route around it through the control port (`docs/mcp.md` "Which files the agent can reach").
- **Doc drift to discount**: `README.md`/`docs/capabilities.md` say "75 of 76" oracle parts; `docs/control-protocol.md` still says the channel is on by default; `docs/mcp.md` lists `solidcraft-reporting` among the embedded skills where the code embeds `-sheetmetal`; `docs/oracle.md` has a validation note that case 95 needs a replay after its reference was corrected.

## How to operate

- GUI: `open -a SolidCraft`; `solidcraft --sample` opens a sample part. App flags: `--control PORT`, `--theme-file FILE`, `--max-file-size SIZE`, `--safe-mode`, `--crash-log`, `--version`, `--help` (`apps/solidcraft/src/main.rs`).
- The CLI ships **inside the app bundle** at `Contents/MacOS/solidcraft-cli`; package installs and the app's Help ▸ Install solidcraft-cli put it on `PATH`, but a given Mac may not have it there — use the bundle-relative path when `command -v solidcraft-cli` is empty.
- First run of the control channel: Preferences ▸ Assistant ▸ Agents through MCP ▸ **Let AI agents connect** (default off). It takes effect immediately, closes/opens the port and rewrites the token file (`crates/ui-egui/src/control_switch.rs`). `--control PORT` and `SOLIDCRAFT_CONTROL_PORT` work regardless of the setting.
- Headless loop (verified flags):
  ```sh
  solidcraft-cli commands                                   # the registry as JSON
  solidcraft-cli exec solid.box '{"length":40,"width":30,"height":20}'
  solidcraft-cli run examples/bracket.json --out bracket.step
  solidcraft-cli eval part.sc                               # measurements as JSON
  solidcraft-cli script part.sc --out rebuild.json          # history as a script
  solidcraft-cli snapshot part.sc --out shot.png --view iso
  solidcraft-cli render part.sc --out render.png --samples 64
  solidcraft-cli oracle tests/oracle/01-box                 # needs case directories
  solidcraft-cli kernel-cases tests/kernel-cases/continuity/g0-box-edge-crease
  solidcraft-cli mcp --headless --in part.sc
  solidcraft-cli mcp setup                                  # register with your client
  ```
  `snapshot` takes `--out` (there is no `-o`). `oracle` and `kernel-cases` refuse with no case directory. `run` accepts a design or STEP as `--in` and writes `--out`/`--save`; a failed feature fails the run unless `--allow-errors`.
- Bridged MCP (watch the agent model): turn the control channel on (or `solidcraft --control 7878`), then `solidcraft-cli mcp` finds the app from `control/current.port`; or `solidcraft-cli mcp --connect 127.0.0.1:7878`. A bridged server starts before the app and retries on the first call.
- Token/discovery live in the platform data folder's `control/` directory, per the table in `docs/control-protocol.md` (macOS uses the Application Support family). `SOLIDCRAFT_CONTROL_DIR` moves it; `SOLIDCRAFT_CONTROL_TOKEN` supplies a known token.
- Web: `solidcraft.io/app` runs the same engine in the browser; pages drive it through the API in `docs/browser-api.md`.

## Working with an AI agent

- **Model like a person**: `list_commands` → `describe_command` for the typed contract → `execute` per step, or `batch` for a stage. Sketch ids from `created:` are stable, so `sketch.*` → `sketch.dimension` → `solid.extrude` → `solid.fillet` can chain without re-picking.
- **Read `skill_reference` first** for enclosures, brackets, plates, flanges and mechanisms. Its discipline (paraphrased): work the part out as numbers first; place it on the origin; use one `batch` per stage; verify every stage with `measure` against values you computed; keep risky steps in their own batch; pass `verbose: false` in large designs; edge picks snap to the nearest edge (compute exact midpoints); a cut that misses can still report success.
- **Use `check_parameters`** to try parameter values without keeping them (one checkpoint, one rebuild, restore); use `inspect.parameter_variants` to compare named value sets.
- **Prepare and verify files**: scripts are plain JSON — generate them, diff them, keep them in git. `script` extracts an existing design's history; `eval` and `inspect_design`/`measure` verify geometry; `compare_picture` checks a model outline against a reference image; `screenshot`/`ui.render` give visual evidence. To inspect or repair a `.sc`, use `file.save {format: "json"}` for the plain document or `script` for the history rather than editing the container's ZIP members by hand.
- **Undo is a tool**: `undo`/`redo` over MCP; `batch` rolls back completed steps on failure by default, and a failed command leaves the design unchanged — a failed `execute` needs no cleanup.
- **Respect the fences**: the MCP server's folder rules are a security boundary; ask the user to add `--allow-path DIR` rather than saving through another surface. Read the token file or use `SOLIDCRAFT_CONTROL_TOKEN`; never hard-code a token.
- **Prefer commands to pixels**: `ui.*` input injection exists for dialogs and picks that no command covers, and `ui.agent_cursor` makes it watchable, but pixel-driving is slower and more brittle than an id from `commands`.
- **What not to attempt**: assuming commercial-CAD parity (clean-room, independent); expecting proprietary formats (SolidWorks, CATIA, Creo, NX, Inventor, ACIS SAT are not compiled in); promising `surface.fillet`, a drawing workspace or CAM; driving the GUI before checking whether a command exists.

## Verification protocol

1. **Round-trip in a scratch design first**: new design → build → `save part.sc` → `open` it back → `export` STEP → re-import or `inspect_design`; compare volume, area and bbox with `measure` before trusting the chain.
2. **Use the oracle and kernel rig as harnesses**: `solidcraft-cli oracle tests/oracle/<case>` replays recipes with expected values; `kernel-cases` runs the kernel regression rig. Model your own checks the same way (recipe/script plus expected values in git).
3. **Never trust a silent export or a silent cut**: `export` says what it wrote — re-open and re-measure. A cut or hole that leaves the volume unchanged has missed even when it reports success (`skills/solidcraft-modeling/SKILL.md`).
4. **One design per session, save between phases**: `new_design`/`open`/`save`; keep scripts in git so any phase is replayable. `script` recovers a history you did not keep.
5. **Re-verify after updates**: compare `solidcraft --version` with this skill's pin (v0.40.1) and run `solidcraft-cli commands`; the registry is the contract, and design format 54 files will not open in 0.30.1.

## Sources & evidence

- Repo: https://github.com/tangency-labs/solidcraft — inspected at tag **v0.40.1**, commit **`0c5292285a7e9331a780c11a2d55f22d8e1c9118`** (commit dated 2026-11-11), inspection date **2026-11-12**. MIT OR Apache-2.0 (`LICENSE-MIT`/`LICENSE-APACHE`); independent clean-room per `NOTICE` and `DISCLAIMER.md`.
- Installed bundle at `/Applications/SolidCraft.app`: `CFBundleShortVersionString` 0.40.1, `CFBundleIdentifier` `io.tangencylabs.solidcraft`; binaries print `solidcraft 0.40.1` and `solidcraft-cli 0.40.1`. The GUI was never launched.
- Read: `README.md`, `ROADMAP.md`, `Cargo.toml`, `docs/{mcp,control-protocol,scripts,capabilities,features,oracle,compatibility,design-container,architecture,agent-chat,render-jobs,browser-api,view-dxf,hole-presets,threads,point-clouds,physical-material-cards,urdf,kernel-cases}.md`, `apps/solidcraft-cli/src/{main,oracle,kernel_cases}.rs`, `apps/solidcraft/src/{main,control_server}.rs`, `crates/engine/src/cmd/mod.rs` + `surface.rs` + module list, `crates/engine/src/schema/{coverage_tests.rs,unconverted.txt}`, `crates/mcp/src/{tools,skill_reference,options}.rs`, `crates/mcp-server/src/server.rs`, `crates/control/src/{auth,server}.rs`, `crates/ui-egui/src/{prefs,control,control_switch,export_name}.rs`, `crates/io/src/{lib,formats}.rs`, `crates/format/src/{container,newer}.rs`, `crates/doc/src/{format.rs,format/v54/box-centred.rs,drawing.rs,expr.rs}`, `crates/smlib/src/lib.rs`, `solidcore/README.md`, `skills/README.md` + skill folders, `tests/oracle/` and `tests/kernel-cases/` layouts.
- Counts recomputed from source and the installed CLI: **634 command ids (1 planned)**, **561 with both typed schemas**, **22 MCP tools**, **19 + 5 CLI verbs**, **82 control methods/commands**, **19 format rows**, **19 in-repo agent skills / 5 embedded**, **30 crates**, **137 docs pages**, oracle **90/90** (69 analytic / 21 FreeCAD; unchanged at v0.40.1), control port **27878** (→27893), design format **54**.
- Evidence ledger: `evidence.md` next to this file; round changes: `CHANGES.md`.
