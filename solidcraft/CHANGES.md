# SolidCraft — round 2026-11-14 changes

Re-pinned: v0.40.1 (`0c5292285a7e9331a780c11a2d55f22d8e1c9118`) -> v0.41.0
(`3c8efdb51952ed9a5f3ebc722c2bad1454fe6d80`, "Release 0.41.0" 2026-11-13; installed
`solidcraft 0.41.0` / `solidcraft-cli 0.41.0`).

## New in v0.41.0

- **Plugins (experimental).** Two new crates, `craft-plugin` (WIT contract, manifest, permissions,
  typed errors) and `craft-plugin-wasm` (Wasmtime, fuel/memory/stack limits, no WASI or network),
  run WebAssembly components through the same command registry (WIT `craft:plugin@0.1.0`,
  capability `commands@0.1`). Four commands: `plugin.inspect` (folder -> manifest + SHA-256 approval
  over manifest and component bytes, no code runs), `plugin.install` (zip, safe paths, size caps, no
  code runs), `plugin.list`, `plugin.run` (exact approval hash, one entry, params; one undo step,
  failed calls roll back). Plugin data lives in the design container under `plugins/<plugin-id>/`
  (<=1024 files, kept without the plugin; `storage` capability later). Over the running desktop,
  `plugin.run` is refused inside `engine.batch`/`engine.script`; MCP and control keep their file
  scopes, so a package folder needs `--allow-path`. Agent chat asks before executing external plugin
  code. New preferences `plugin_max_fuel` / `plugin_max_memory_mib`; new global CLI flag
  `--plugin-limits FILE.json` (user ceilings 100000000000 fuel / 128 MiB; per-invocation defaults
  10,000,000 / 64 MiB).
- **Kernel repair, not kernel change.** Fillet/chamfer on near-tangent sharp corners is mitred
  instead of failing (0.30.1 behaviour 0.40 lost); fillet/chamfer/shell/edge selection share one 2°
  tangent chain; STEP **export no longer writes solids inside out**; STEP import keeps faces that
  wrap a cone or sphere and tiny rounds; sheet-metal folds across tabs stay single faces; lofts with
  shared end sketches, thin-profile sweeps round sharp corners, skew-line revolves, Through All and
  tangent-profile merges build correctly. Failures now say why instead of "status 1001".
- **New model surface (no new area, +8 ids total):** `sketch.spline.handles`, `sketch.spline.reset_handles`,
  `model.mesh` (read-only evaluated mesh, tolerance default 0.05 mm, <=8192 vertices / 16384
  triangles), the four `plugin.*` commands, and `file.import_cache_clear`. `solid.move` takes
  `matrix` (rigid 3x4/4x4) and `origin`; `solid.split_face` takes `loops`; `solid.split_body` accepts
  a closed surface; `construct.*`/sketch/joint placement accept snap points; `file.export` takes
  `lay_on_print_faces`; GLB export keeps an assembly's named movable nodes; ISO thread sizes M3.5,
  M7, M33, M39, M45 are known; contour flanges accept tangent arcs; assemblies gain a Constrain
  dialog over the existing joint commands.
- **Defaults:** `agent_off_thread` flips `false -> true` (`crates/ui-egui/src/prefs.rs`; an existing
  saved off stays off, a pre-file follows the new default), so slow agent commands compute beside
  the window on new installs and each waiting command is its own cancellable operations row.
  Saves show progress and can be cancelled until the file is replaced. Design and Render share one
  docking system; saved layouts still work.
- **Packaging:** macOS still Developer ID + notarized; Windows builds now carry SignPath-provided
  signing, with a SmartScreen warning possible until the production certificate lands (`README.md`).

## Corrected / re-measured

- **Commands 634 -> 642** (+8, none removed): `plugin.inspect`, `plugin.install`, `plugin.list`,
  `plugin.run`, `model.mesh`, `file.import_cache_clear`, `sketch.spline.handles`,
  `sketch.spline.reset_handles`; `surface.fillet` is still the only planned id (CLI JSON
  `planned: "769"`). **`docs/features.md` is now stale**: it has 636 rows and lacks the six new
  non-sketch ids, where at v0.40.1 the page agreed with the registry row for row. The installed
  CLI's `commands` output remains the authority.
- **Typed schemas 561/634 -> 572/642**; 70 commands describe neither (was 73), one planned. The
  repo's coverage test still only warns (`SCHEMA_RULE_STRICT: bool = false`).
- **Design format 54 -> 55** (`crates/doc/src/format/v55`; probe: build a box, `run --save box.sc`,
  `document.json` says `"format": "solidcraft/55"`). Format 55 records rounds by definition,
  snap-point construction geometry, a Move rotation origin, dragged spline tangent handles, Split
  Face loops, projected-vertex names and plugin data. 0.40.x opens it with a warning; 0.30.1 refuses
  it. `--out x.sc` on `run` writes plain JSON (`file.export`), not the container — use `--save` for
  a `.sc`.
- **Crates 30 -> 32** (`craft-plugin`, `craft-plugin-wasm`); **docs pages 137 -> 139**
  (`plugin-runtime.md`, `plugin-test-guide.md`).
- **Unchanged counts, re-measured:** MCP tools 22, CLI verbs 19 + 5, control methods/commands 82
  (identical name set; doc diff is wording), format-registry rows 19, in-repo agent skills 19 /
  embedded 5, oracle 90/90 (69 analytic, 21 FreeCAD). Control channel still off by default (port
  27878, next free up to 27893). `README.md`/`docs/capabilities.md` still say "75 of 76".
- **New drift recorded:** `docs/features.md` six behind; the control-protocol launch table still
  says the channel is "on (the default)" and that old preference files load it on (the test says
  otherwise); `docs/mcp.md` still lists `solidcraft-reporting`; the `skill_reference` description
  still lists four skills; `docs/oracle.md` still carries the case-95 replay note.

## Method

- The local clone was stale at v0.29.0 and `git fetch` hung, so the audit used the GitHub
  release tarballs for both tags
  (`codeload` at `3c8efdb…` and `0c529228…`), plus the installed bundle. Tag -> commit came from
  the GitHub ref API and the release notes' `target_commitish`.
- Counted commands and read the new command contracts from the installed
  `solidcraft-cli 0.41.0` (`commands`, `exec`, `--help`); compared id sets against the v0.40.1
  `docs/features.md`.
- Counted typed contracts by calling MCP `describe_command` for all 642 ids in one headless
  `solidcraft-cli mcp --headless` session; counted MCP tools from live `tools/list` and from
  `crates/mcp/src/tools.rs`.
- Verified the design format by saving a probe design (`--save`) and reading `document.json`.
- Diffed the two source trees for commands, MCP tools, CLI verbs, control method tables, format
  rows, skills, crates, docs pages, prefs defaults, plugin docs and the release notes' fixed/new
  list. Per-surface method and the drift table are in `evidence.md`.

## Unchanged

- One command registry remains the API for every surface; sketch commands still return stable
  `created:` ids; expressions still accept parameters and units; the native design is still `.sc`
  (legacy `.solidcraft`/`.solvecraft`, plain `.json` still read/written); render jobs still run
  through `render.preflight/start/status/cancel/export`; the artefact format set is the same 19
  registry rows; the kernel is still the vendored `solidcore`; independent clean-room status and
  MIT OR Apache-2.0 licensing are unchanged.

## Known gap in this round

- No GUI or kernel run: capability prose comes from source, the installed CLI's registry output,
  release notes and repo docs. No part was built end-to-end beyond the format probe, and the
  oracle report was read, not replayed.
- No plugin package was installed or run; the plugin section is derived from `docs/plugins.md`,
  `docs/plugin-runtime.md`, the engine's `plugin` modules and the CLI's `commands` output.
- Drawings and CAM are still not implemented; `.scdwg` has a reader/writer but no app/command path.
- `docs/` stale statements are recorded as drift in `evidence.md` rather than treated as fact.

# SolidCraft — round 2026-11-12 changes

Re-pinned: v0.30.1 (`8e2b0cd60d14b4152b12b8f1fdb2bcfdcd8c52f4`) -> v0.40.1
(`0c5292285a7e9331a780c11a2d55f22d8e1c9118`, installed `solidcraft 0.40.1`).

## Corrected / re-measured

- **Commands 570 -> 634** (64 new ids, none removed). The old skill mixed two methods and quoted
  554 (string literals in code) against 571 rows in `docs/features.md` (the v0.30.1 file actually
  has 570); at this tag the installed CLI's `commands` output, `docs/features.md` and the registry
  all agree on **634 ids**, of which exactly one is planned (`surface.fillet`, issue #769). 30 of
  the new ids are `panel.*`/`layout.*`.
- **MCP tools 21 -> 22**: `cancel` is the only addition. Typed input/output contracts are described
  for 561 of 634 commands; 73 describe neither, including the one planned command. The repo's
  coverage test only warns (`SCHEMA_RULE_STRICT: bool = false`) and exempts 18 old commands in
  `crates/engine/src/schema/unconverted.txt`.
- **The control channel is no longer on by default.** At v0.30.1 the preference was
  `agent_control: bool = true` with the test `agent_control_is_on_unless_saved_off`; at v0.40.1 it
  is `false` with `agent_control_is_off_unless_saved_on` (`crates/ui-egui/src/prefs.rs`). A new
  install listens on nothing until the user turns on Preferences ▸ Assistant ▸ Agents through MCP ▸
  "Let AI agents connect", or the app is launched with `--control PORT`. `docs/control-protocol.md`
  still says "on (the default)" — stale against code and against `docs/mcp.md`.
- **Control protocol 46 -> 82** documented methods/commands (+36, none removed): 25 `panel.*`,
  5 `layout.*`, `ui.operations`, `ui.recover`, `document.export`, `document.import`,
  `document.saved`, `mcp.options`, etc.
- **CLI verbs: 18 listed + 5 unlisted -> 19 + 5.** `kernel-cases` is the only new verb. The old
  skill's "16 listed + 6 unlisted" was wrong at both tags. Two bad examples in the old skill are
  fixed: `snapshot` accepts `--out`, not `-o`; `oracle` needs explicit case directories and does
  not replay anything with no arguments.
- **Design format 48 -> 54** (`crates/doc/src/format/v49` … `v54`; the last saves a box placed by
  its centre). Drawings keep their own family at format 1.
- **Format registry 18 -> 19 rows**: GLB export now has its own row (`glb`), separate from the
  import-only glTF row.
- **In-repo agent skills 17 -> 19**: `solidcraft-layers` and `solidcraft-sheetmetal` are new. The
  binary embeds **five** (`modeling`, `editing`, `checking`, `mechanisms`, `sheetmetal`), not four;
  `docs/mcp.md` lists `reporting` instead of `sheetmetal`, and the `skill_reference` tool
  description lists only four — both are text drift, the table in
  `crates/mcp/src/skill_reference.rs` is authoritative.
- **Workspace crates 14 -> 30.** The kernel is now the vendored `solidcore` (the Rust port of
  NVIDIA's SMLib, Apache-2.0) behind `crates/smlib`; `truck-*` left the dependency graph. Shared
  front-end crates (`ui-kit`, `look`, `theme`, `viewport*`, `mcp-server`, `control*`, `color`,
  `format`, `dynamics`, `profile`) are new.
- **Docs pages 119 -> 137.** Oracle stays **90/90** (69 analytic, 21 FreeCAD) but `docs/oracle.md`
  now carries a validation note that case 95's centre-of-mass reference was corrected after the
  run and needs a replay. `README.md` and `docs/capabilities.md` still say "75 of 76".
- **Baseline errors removed:** the old Sources section pinned tag v0.30.1 while the installed
  bundle was 0.29.0; the audit basis now names one tag, one commit and one installed version.

## Method

- Pinned the checkout with `git rev-parse HEAD` (equals the release commit) and read the installed
  bundle's `--version` strings (`solidcraft 0.40.1`, `solidcraft-cli 0.40.1`); the GUI was never
  launched.
- Counted commands from the installed CLI: `solidcraft-cli commands` parsed as JSON gives 634
  unique ids, cross-checked against 634 table rows in `docs/features.md` and against the source
  registries in `crates/engine/src/cmd/` (588 literal `CommandSpec::new("…")` ids plus 46 ids built
  by `variant!`, `planned!` and table-driven constructors).
- Counted MCP tools by extracting the first string argument of every `tool(...)` entry in
  `crates/mcp/src/tools.rs` (22 unique names), and confirmed the same set against `docs/mcp.md`.
- Counted typed command contracts by calling MCP `describe_command` for all 634 ids in one headless
  session and counting non-null `input` and `output`: 561 have both, 73 have neither (one is the
  planned command).
- Counted control methods/commands from the tables in `docs/control-protocol.md` (82 unique
  backticked ids; 36 more than the v0.30.1 copy of the same file).
- Counted CLI verbs from the `COMMANDS` table in `apps/solidcraft-cli/src/main.rs` (19 `listed:
  true`, 5 `listed: false`).
- Counted format rows by parsing the `FORMATS` static in `crates/io/src/formats.rs` (19 `id:`
  entries) and read each row's import/export capabilities from the same table.
- Counted skills from the folders under `skills/` (19) and from the `Skill` table in
  `crates/mcp/src/skill_reference.rs` (5 embedded).
- Counted crates from the folders under `crates/` (30) and from the workspace dependency list in
  `Cargo.toml`.
- Diffed id sets between `v0.30.1` and `HEAD` with `git show`/`git diff` (the shallow checkout
  holds both commits): 64 command ids added, 0 removed; 1 MCP tool added, 0 removed; 36 control
  methods/commands added, 0 removed; 2 skills added; 1 CLI verb added.

## Unchanged

- The command registry is still the API for the desktop app, web app, CLI, control channel and MCP;
  every command still has one dotted id, and the same ids run everywhere.
- Sketch commands still return `created: {points, curves, constraints, dimensions}` with stable,
  never-reused ids (71 command parameter docs carry the note; the `created_doc!` macro in
  `crates/engine/src/cmd/mod.rs`).
- The native design extension is still `.sc`, with `.solidcraft` and `.solvecraft` accepted as
  legacy names and plain `.json` designs still read and written.
- Rendering still runs through asynchronous `render.preflight/start/status/cancel/export` jobs.
- The oracle set is unchanged at v0.40.1: 90 reference parts with 69 analytic and 21 FreeCAD-derived
  expectations.
- The artefact format set is unchanged at v0.40.1 apart from GLB gaining its own export row:
  STEP/IGES import and export, FreeCAD and Rhino import, STL/3MF/OBJ/GLB export and
  STL/3MF/OBJ/glTF import, PLY/XYZ/PTS point clouds, URDF export, DXF sketch import and
  current-view DXF export, SVG sketch import.
- Independent clean-room status, MIT OR Apache-2.0 licensing, and the macOS signed/notarized vs
  Windows unsigned packaging split are unchanged (`README.md`, `NOTICE`, `DISCLAIMER.md`).

## Known gap in this round

- No GUI or kernel run: the capability prose is re-derived from code, the installed CLI's own
  registry output and the repo's documentation, but no part was built end-to-end in this round,
  and the oracle report was read, not replayed.
- The 0.40.0 kernel/mesher/STEP-reader replacement is described from the dependency graph, crate
  layout and vendored `solidcore` tree; its geometric consequences are not independently tested
  here.
- The drawings surface is not usable: `.scdwg` has a document model and reader/writer, but no app
  or command path opens one; the Insert Drawing dialog places SVG and DXF on a sketch, not
  `.scdwg`. `ROADMAP.md` still lists the drawings milestone as unmerged.
- `docs/` contains several stale statements (control default, skill list, "75 of 76" oracle,
  drawings, SMLib "not in releases"); they are recorded as drift in `evidence.md` rather than
  treated as fact.
