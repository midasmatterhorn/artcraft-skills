---
name: solidcraft
description: >-
  SolidCraft is an open-source parametric 3D CAD application in pure Rust (by Tangency Labs,
  independent clean-room; not an Autodesk/Dassault product): sketches with constraints and
  parameter-driven dimensions, a parametric feature timeline (extrude, revolve, sweep, loft,
  fillet, chamfer, shell, draft, holes, threads, patterns, mirror, split, combine), sheet metal,
  plastic enclosure features, assemblies with joints and motion studies, physical materials with
  mass properties, and STEP/IGES/3MF/STL/OBJ/glTF/URDF/DXF interchange. Desktop app, browser app,
  headless CLI and a 20-tool MCP server all run the same 539-command registry. Trigger this skill
  whenever the user mentions SolidCraft (or `.sc`, `solidcraft-cli`, "SolidCraft MCP", the
  control channel on 27878), asks what it can model or open/export, wants an agent to build or
  edit a parametric part (enclosure, bracket, plate, flange), drive the control channel, script a
  build, run the oracle, or troubleshoot it — and equally when they never name it but describe
  parametric CAD work ("model a case for this board", "sketch, constrain and extrude", "export a
  STEP of this bracket"). Do not assume Fusion/SolidWorks behaviour: read this first.
---

# SolidCraft

**Audit basis.** Refreshed 2026-11-04 against tag **v0.30.1**, commit **`8e2b0cd60d14b4152b12b8f1fdb2bcfdcd8c52f4`** — `git rev-parse HEAD` in the pinned checkout confirms, and the installed `/Applications/SolidCraft.app` matches (its binary prints `solidcraft 0.30.1`). The previous release this skill described was v0.29.0 (`3a5195b`).

**v0.29.0 → v0.30.1 delta.** 578 files changed; 15 new command ids, none removed — **554** ids measured in code, while the CI-regenerated `docs/features.md` lists 571 rows (the doc is the stronger source where it is test-enforced). Additions include `file.export_3mf/obj/step/stl/urdf`, `render.batch`, `render.compare`, `render.compare.divider`, `render.result.select/discard`, `component.show_history/hide_history`, `construct.plane.axis_point` and squashed-spline editing. `.scdwg` drawing files are new, FreeCAD/Rhino import lands through cadmpeg, and glTF is import-only. `surface.fillet` remains planned-only (the single `planned` row).

**Verify against your installed version** — the ArtCraft Launcher auto-updates, so a newer build may differ; every count quoted here was re-measured at this tag, and code paths that moved were re-cited. The measurement method for each count is in `evidence.md`.

## Overview

SolidCraft is "an open-source parametric 3D CAD application built in pure Rust" by Tangency Labs (`README.md`; MIT OR Apache-2.0). Sketch, constrain and build solids on an editable parametric feature timeline; change a dimension and the model rebuilds. It is **independent and clean-room**: behaviour is designed from public documentation and general CAD conventions, reference tests use analytic values and FreeCAD as an external oracle, and it is not affiliated with any CAD vendor (`README.md` Disclaimer; `NOTICE`). **Status: early but usable for simple parts** — the generated oracle report counts **90/90 reference parts passing** against analytic or FreeCAD-computed volume/area/centre-of-mass/bounding-box (`docs/oracle.md`; the README and `docs/capabilities.md` still say "75 of 76" — the generated oracle table is newer, trust it and `solidcraft-cli oracle`). One command registry serves the desktop app (egui), the browser app, the headless CLI and the MCP server. Source: GitHub `tangency-labs/solidcraft`; docs at `docs.solidcraft.io`.

## Capabilities (verified)

### The command registry is the API (start here)

- **539 engine commands** registered with `CommandSpec::new("dotted.id", …)` across ~210 modules under `crates/engine/src/cmd/` (re-grepped at this tag; one **`planned!`** id, `surface.fillet`, refuses with its issue number). Ids are dotted and lower-case: `sketch.rectangle.two_point`, `solid.extrude`, `solid.fillet`, `timeline.rollback`. The same commands run from the toolbar, scripts, `solidcraft-cli exec`, the control channel and MCP (`docs/features.md` header; `crates/engine/src/cmd/mod.rs`).
- **MCP server** (`solidcraft-cli mcp`): stdio JSON-RPC, protocol revisions 2025-06-18 (2025-03-26 and 2024-11-05 accepted). **21 tools**: `list_commands` (catalog with enablement), `describe_command` (typed JSON-Schema contracts for input/output on converted commands), `execute`, `batch`, `undo`, `redo`, `inspect_design`, `measure`, `body_topology`, `set_parameter`, `check_parameters`, `screenshot`, `export`, `new_design`, `open`, `save`, `crash_reports`, `running`, `pending`, and **`skill_reference`** (returns SolidCraft's built-in modelling skills) (`crates/mcp/src/tools.rs` `tool_definitions`). Headless it runs its own session (`--in part.sc` to start from a file); with `--connect HOST:PORT` it drives the running app so you can watch.
- **The app listens by default**: control channel on `127.0.0.1:27878` (next free port up to 27893), loopback only, token-authenticated — the app writes a 256-bit token to a `control/PORT.token` file in its data folder and the port to `control/current.port` for discovery; `solidcraft-cli mcp` with no arguments finds it. Preferences ▸ Assistant ▸ "Let AI agents connect" turns the default listener off (`docs/control-protocol.md`; `docs/mcp.md`).
- **Sketch commands return `created: {points, curves, constraints, dimensions}`** — stable ids you can use immediately in `sketch.dimension`, `sketch.constraint.*`, `sketch.delete` (`crates/engine/src/cmd/mod.rs` `created_doc!`). Lengths are mm; expressions accept parameters and units (`"width / 2"`, `"30 deg"`).
- **CLI verbs** (`apps/solidcraft-cli/src/main.rs`): listed — `run`, `eval`, `script`, `bench-open`, `bench-agent`, `bench-assistant`, `snapshot`, `render`, `exec`, `commands`, `recipe`, `oracle`, `fuzz`, `mcp`, `crashes`, `licences`/`licenses`; also present (unlisted) — `inspect`, `fuzz-one`, `gpu`, `icon`, `bench-edit`, `save-stress`. **`run script.json --out part.step`** executes a JSON script and exports.
- **Scripts** are a JSON list of the same commands: `{"commands": [{"command": "sketch.create", "params": {"plane": "XY"}}, …]}` (`docs/scripts.md`).
- **Async render jobs** through plain `execute`: `render.preflight`, `render.start`, `render.status`, `render.cancel`, `render.export`; keep the returned job ID; image bytes stay in the session until PNG export (`docs/mcp.md`; `docs/render-jobs.md`). The renderer is deep — dozens of render docs (PBR, path tracing, CPU/GPU backends, denoise, HDR, studio lighting, GGX anisotropic…).

### Modelling (what it can actually build)

- **Sketches**: lines, rectangles, circles, arcs, polygons, slots, ellipses, fit/control splines, conics and text on origin/offset planes or planar faces; construction geometry, projection, trim/extend, corner fillets/chamfers; face attachments (`docs/capabilities.md`).
- **Constraints and dimensions**: coincident, point-on-curve, horizontal/vertical, parallel, perpendicular, tangent, curvature (G2), equal, concentric, collinear, midpoint, symmetry, fix; ~15 dimension kinds driven by parameters; solved by their own solver (exact loci intersections + Levenberg–Marquardt with rank/DOF reporting); over-constraining edits rejected; drag solves every frame and rebuilds once at the end.
- **Features**: extrude, revolve, sweep, loft, fillet, chamfer, shell, draft, holes (with presets, `docs/hole-presets.md`), threads, patterns, mirror, split, combine — on an editable parametric timeline with rollback (`timeline.rollback`).
- **Parameters and configurations** with unit-aware expressions; **assemblies** with joints, motion studies, contact sets, interference and mass properties; **sheet metal** (flanges, hems, fold/unfold, flat patterns) and plastic enclosure features; **physical material cards** with mass in Properties; BOM commands (`crates/engine/src/cmd/bom.rs`); point clouds (`docs/point-clouds.md`); drawing foundations/HLR docs exist (`docs/drawing-*.md`).
- Built-in agent skills: the repo's `skills/` folder ships 17 Agent-Skills-format folders; the four modelling ones (`solidcraft-modeling`, `-editing`, `-checking`, `-mechanisms`, `-reporting`) are embedded in the binary and served through the MCP `skill_reference` tool — **read `skill_reference` before a non-trivial model**; it encodes the project's own ground rules for driving the engine.

### Files: open and save

- **Native design `.sc`** (also opens `.solidcraft`, `.solvecraft`, and JSON designs; older `.solidcraft` files still open) — `crates/io/src/lib.rs` `DESIGN_EXT = "sc"`, `DESIGN_EXTS = ["sc", "solidcraft", "solvecraft"]`; a native CAD kernel (`crates/io/src/native_cad/`, `docs/native-brep.md`).
- **Import/export**: STEP/`.stp`, IGES/`.igs`, 3MF, STL, OBJ, glTF/GLB, PLY, DXF (2-D drawing sketch import and current-view DXF export with hidden-edge modes), URDF export — "in and out where supported" (`README.md` What works; `crates/io/src/` modules `formats.rs`, `dxf.rs`, `gltf_in.rs`, `obj.rs`; `docs/view-dxf.md`).
- **Oracle/reference tests**: `cargo xtask oracle` generates `tests/oracle/` cases; every rebuilt part is also exported as STEP, validated and read back (`docs/oracle.md`).

## Known limitations and not-implemented

Do not assign these at v0.29.0:

- **Early but usable for simple parts** — the project's own words. The oracle covers 90 simple reference parts; complex multi-body workflows are not proven to that standard (`docs/oracle.md`; `docs/capabilities.md`).
- **One planned command**: `surface.fillet` refuses with its tracking issue (`planned!` in `crates/engine/src/cmd/mod.rs`).
- The README/capabilities "75 of 76" oracle count is stale against the generated 90/90 table (`docs/oracle.md`).
- Windows downloads are unsigned (SmartScreen); macOS is signed and notarized (`README.md` Download).
- Tool, feature or check you cannot find in `solidcraft-cli commands` / `describe_command` should be treated as absent — the registry is the contract, and disabled commands report why.

## How to operate

- GUI: `open -a SolidCraft`, binary `/Applications/SolidCraft.app/Contents/MacOS/SolidCraft`; **the CLI is inside the bundle**: `/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli` (also on PATH on most installs). `solidcraft --sample` opens a sample part. The control channel is on by default (Preferences ▸ Assistant to disable; takes effect at next start).
- Model headlessly:
  ```sh
  solidcraft-cli commands                       # the registry, id + label + enablement
  solidcraft-cli exec solid.box '{"length":40,"width":30,"height":20}'
  solidcraft-cli run examples/bracket.json --out bracket.step
  solidcraft-cli oracle                         # replay the reference parts
  solidcraft-cli snapshot design.sc -o shot.png
  claude mcp add solidcraft -- solidcraft-cli mcp
  ```
- Bridged MCP (watch the agent model): `solidcraft &` then `solidcraft-cli mcp` (it finds the port/token file), or `--connect 127.0.0.1:7878` after `solidcraft --control 7878`. A bridged server starts even before the app and errors with "no SolidCraft app is listening at HOST:PORT" until it is; pass `SOLIDCRAFT_CONTROL_TOKEN` when the app runs sandboxed.
- Data folders: token/discovery files under the platform data dir (macOS `~/Library/Application Support`-family per `docs/control-protocol.md` token table; Linux `$XDG_DATA_HOME/solidcraft/control/PORT.token`).
- Web: `solidcraft.io/app` runs the same engine in the browser; the browser command API is `docs/browser-api.md`.

## Working with an AI agent

- **Model like a person**: `list_commands` → `describe_command` for the typed contract → `execute` per step. Sketch ids from `created:` are stable; chain `sketch.*` → `sketch.dimension` → `solid.extrude` → `solid.fillet` without re-picking. `batch` runs several commands in order.
- **Read `skill_reference` first** for enclosures/brackets/plates/flanges and for mechanisms (joints, contact sets, motion studies) — SolidCraft's own modelling discipline, including parameter-range checking (`check_parameters`, `docs/configurations.md`).
- **Prepare and verify files**: scripts are plain JSON (generate them, diff them, keep them in git — `docs/scripts.md` says designs kept in git are expected practice); verify exports by re-opening the STEP (`oracle` does exactly this) or with `inspect_design`/`measure`/`body_topology` and compare mass properties.
- **Undo is a tool**: `undo`/`redo` over MCP; failures leave the design unchanged, so a failed `execute` needs no cleanup.
- **What not to attempt:** assuming commercial-CAD parity (clean-room, independent); driving dialogs (MCP tools never open dialogs — use commands); hard-coding the control token (read the token file or the env var); trusting `describe_command` coverage for every old command (typed contracts land progressively); promising `surface.fillet`.

## Verification protocol

1. **Round-trip first**: build the part → `save design.sc` → `open` it back → `export` STEP → re-import or `inspect_design`; compare volume/area/bbox with `measure` before trusting the chain.
2. **Use the oracle as your harness**: `solidcraft-cli oracle` replays reference parts with expected values; model your checks the same way (recipe.json + expected values in git).
3. **Never trust a silent export**: `export` returns what it wrote; re-open and re-measure.
4. **One design per session, save between phases**: `new_design`/`open`/`save`; keep scripts in git so any phase is replayable.
5. **Re-verify after updates** (`solidcraft --version` vs this skill's pin v0.29.0): the command registry moves fast; `list_commands` on your build is the contract.

## Sources & evidence

- Repo: https://github.com/tangency-labs/solidcraft — inspected at tag **v0.29.0**, commit `8e2b0cd60d14b4152b12b8f1fdb2bcfdcd8c52f4`, release dated 2026-11-01, inspection date **2026-11-01**. MIT OR Apache-2.0 (`LICENSE-MIT`/`LICENSE-APACHE`); independent clean-room per `NOTICE` and `DISCLAIMER.md`.
- Installed `/Applications/SolidCraft.app`: `CFBundleShortVersionString` 0.29.0, `CFBundleIdentifier` `io.tangencylabs.solidcraft`; binaries print `solidcraft 0.29.0` and `solidcraft-cli 0.29.0` — **both are in the bundle**.
- Read: `README.md`, `ROADMAP.md`, `Cargo.toml`, `docs/{mcp,control-protocol,scripts,capabilities,features,oracle,render-jobs,building,downloads,native-brep,hole-presets,point-clouds,physical-material-cards,view-dxf,browser-api}.md`, `apps/solidcraft-cli/src/main.rs`, `apps/solidcraft/src/`, `crates/engine/src/cmd/mod.rs` and the `cmd/` module list, `crates/engine/src/{control_auth,control_pending}.rs`, `crates/mcp/src/{lib,server,tools}.rs`, `crates/io/src/{lib,formats,dxf,gltf_in,obj,catalog}.rs`, `crates/{kernel,geom,sketch,render,gpu,derive,doc}/` (layouts), `skills/README.md` + skill folder list, `tests/oracle/` layout, `tools/oracle-analytic/`, `tools/freecad-oracle/`.
- Counts recomputed from source: **539 `CommandSpec::new` ids (1 `planned!`: `surface.fillet`)**, **21 MCP tools**, 16 listed + 6 unlisted CLI verbs, 3 design extensions (`sc`, `solidcraft`, `solvecraft`), 12+ interchange formats, 17 in-repo agent skills, 118 docs pages, oracle 90/90 (69 analytic / 21 FreeCAD), control port 27878–27893.
- Evidence table: `evidence.md` next to this file.
