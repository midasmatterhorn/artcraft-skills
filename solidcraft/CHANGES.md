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
