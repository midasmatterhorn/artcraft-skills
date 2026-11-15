# SolidCraft — round 2026-11-15 changes

Re-pinned: v0.41.0 (`3c8efdb51952ed9a5f3ebc722c2bad1454fe6d80`) -> **v0.42.0**
(`1b1e940cc48e4d1d5d01971a4be20e2e55647066`, "Merge main into release for 0.42.0", 2026-11-14), inspected 2026-11-15.
The installed bundle was auto-updated by the launcher and matches: `/Applications/SolidCraft.app`
is `CFBundleShortVersionString` 0.42.0, `CFBundleIdentifier` `io.tangencylabs.solidcraft`, and its
binaries print `solidcraft 0.42.0` and `solidcraft-cli 0.42.0`. The pin was verified with
`git rev-parse HEAD` in the read-only checkout; the checkout is the single commit of the tag.

## New in v0.42.0

- **Signed design provenance.** A design container may now carry one additive entry,
  `provenance/log.cbor`: a bounded chain of signed records over the design's authoritative
  content (`document.json`, `container.json`, every other non-derived entry), each record a
  CBOR manifest signed as a COSE_Sign1 message (Ed25519) or an OpenPGP detached signature with
  the signer's transferable public key (`crates/io/src/design/provenance.rs`;
  `docs/formats/cose-provenance.md`). Records chain by SHA-256 of the previous record's bytes, so
  removing, reordering or rewriting a record with a successor breaks the chain; the newest record
  names the oldest one, so truncation is a signed fact. Each signed save appends a record; the
  envelope is bounded (8 MiB, 64 records of 4 MiB, 10,000 signed parts, 4 KiB text fields) and
  drops the oldest records when full. Not signed: `cache/`, previews, thumbnails, the
  `provenance/` entry itself, the ZIP directory. Provenance is tamper-evidence, not identity.
- **Three new file commands and a sign path on save.** `file.verify` reports
  `unsigned`/`valid`/`not_covered`/`invalid`/`unsupported` with the chain
  (`crates/engine/src/cmd/file.rs`); `file.gpg_keys` lists the GnuPG secret keys a save can sign
  with, desktop only (`crates/engine/src/gpg.rs`); `file.save` takes `sign` and `signing_key`
  (container only, app's own Save only — a script or agent is refused, and the refusal was read
  live from the shipped CLI) and replies with `signature`. `doc.open` takes `verify` and reports
  the design's `signature`. Preferences ▸ Security carries the trust model (`crates/ui-egui/src/prefs.rs`,
  `crates/ui-egui/src/prefs/security.rs`; `docs/control-protocol.md` prefs list): `sign_saved_designs` (false),
  `signing_key` (empty: GnuPG's default), `trusted_signing_keys` (empty: only these show as verified, any
  other valid signature in grey with its fingerprint) and `verify_opened_designs` (false: verify on open
  instead of on request).
- **KiCad PCB import.** A twentieth format-registry row, `kicad` (`kicad_pcb`, `kicad_pro`;
  import only) with a reader written from KiCad's documented s-expression format
  (`crates/io/src/kicad_in.rs`; `docs/kicad-import.md`). The board substrate comes in as a B-rep
  solid by default, with drilled holes cut; footprint 3D models (STEP/VRML, colours kept), copper
  as a flat overlay or as 0.035 mm solids, silkscreen and text are options, and
  `doc.open` accepts `thickness`, `components`, `copper`, `silkscreen`, `color`, `representation`.
  The board is built once at import; the design stores solids and meshes, so it reopens without
  the board file.
- **Five new command ids (642 -> 647, none removed):** `file.verify`, `file.gpg_keys`,
  `sketch.insert_airfoil` (`crates/engine/src/cmd/sketch_import.rs`: Selig/Lednicer `.dat`
  coordinates to one fit-point spline, chord/pivot/angle/flip/tolerance, trailing-edge gap
  reported), `solid.cell_grid` (`crates/engine/src/cmd/cell_grid.rs`: hexagonal/square/triangle/
  circle/polygon cells cut as a field, at most 250 cells, `clip`, `direction`, keep-out loops;
  not for sheet metal), `view.origin_axes_across_view`.
- **Design format 55 -> 57.** Format 56 is folded from five change files
  (`crates/doc/src/format/v56/cell-grid-feature.rs`, `frame-member-locate.rs`,
  `frame-standard-sizes.rs`, `occurrence-move-expressions.rs`, `pattern-names-by-source.rs`), and
  57 is those plus two pending changes (`extrude-to-object-keeps-picked-placements`,
  `plane-at-angle-follows-named-axis`). A probe save writes `"format": "solidcraft/57"` with a
  `format_pending` list naming both.
- **Measurements are exact for B-rep bodies.** Volume, area, centre of mass and box now come from
  SMLib's mass properties (`crates/kernel/src/measure.rs` `measure_mass`; the probe replies
  `measured_by: "smlib"`), where v0.41.0 measured them from a tessellation at a chord tolerance
  (`crates/kernel/src/body.rs` `volume_at` took a tolerance and meshed). Mesh bodies still measure
  from their triangles. This retires the previous skill's "mass properties come from fine
  tessellation" limitation.
- **Agent-surface changes.** MCP tool schemas no longer use JSON-Schema `type` unions; they are
  `anyOf`, because Moonshot refused every tool whose argument had two types and Gemini refused
  the list form (`crates/mcp/src/tools.rs`; the 22 tool names are unchanged).
  `view.pick` is documented as a control-channel method handled by the app: it is not a registry
  command and is unavailable in headless MCP. Two CLI flags are new: `--require-allow-path`
  (with `mcp`: refuse to start when every `--allow-path` folder is missing or unusable) and
  `--script-relative` (with `run`: command file paths come from the positional script's folder).
  A `--allow-path` folder that cannot be used is now reported instead of dropped.
- **Library and docs:** new dependency-free crate `display-units` (mm/cm/m/in/ft formatting,
  `crates/display-units/src/lib.rs`) takes the workspace from 32 to 33 crates, and
  `docs/kicad-import.md` takes the docs pages from 139 to 140.

## Corrected / re-measured

- **Commands 642 -> 647** (+5, none removed; the five ids above). `surface.fillet` is still the
  only planned id (`planned: "769"` in the CLI's JSON; it also reports
  `disabled_reason: "not supported yet (issue #769)"`). **`docs/features.md` is now one row
  behind** instead of six: it lists 646 ids and lacks only `sketch.insert_airfoil` (v0.41.0: 636
  rows, six missing). The installed CLI's `commands` output remains the authority.
- **Typed schemas 572/642 -> 612/647.** 612 commands describe both input and output JSON Schema;
  35 describe neither (was 70), one of them the planned `surface.fillet`. The exemption list
  `crates/engine/src/schema/unconverted.txt` is down to 16 ids (17 at v0.41.0; `sheet.export_dxf`
  gained its contract) — the previous round's "21 exempted ids" was a miscount. The coverage test
  still only warns (`SCHEMA_RULE_STRICT: bool = false`, `crates/engine/src/schema/coverage_tests.rs`).
- **Design format 55 -> 57**, verified by saving a probe design with the shipped CLI and reading
  `document.json` (`format`, `format_pending`). Reading a newer file still warns and keeps what
  the build cannot read (`crates/format/src/newer.rs`).
- **Format registry 19 -> 20 rows** (`kicad`); IGES still exports through `file.export` (the row
  carries the export, the command's `format` enum does not name it — export by `.igs`/`.iges`
  extension). **Crates 32 -> 33**, **docs pages 139 -> 140**.
- **Unchanged counts, re-measured:** MCP tools 22 (identical name set), MCP protocol revisions
  2025-06-18 / 2025-03-26 / 2024-11-05, CLI verbs 19 listed + 5 unlisted, control-channel
  documented methods/commands 82 (identical name set), in-repo agent skills 19 / embedded 5,
  oracle 90/90 (69 analytic, 21 FreeCAD), control port 27878 (next free up to 27893) with the
  channel off on a new install, `agent_off_thread: true`, plugin surface (four `plugin.*`
  commands, WIT `craft:plugin@0.1.0`).
- **Drift still standing at v0.42.0:** `README.md` and `docs/capabilities.md` say "75 of 76"
  reference parts where `docs/oracle.md` says 90/90 and still carries the case-95 replay note;
  `docs/control-protocol.md`'s launch table still calls the control channel "on (the default)"
  while its own prose and `crates/ui-egui/src/prefs.rs` say off; `docs/mcp.md` still lists
  `solidcraft-reporting` where the embedded set has `solidcraft-sheetmetal` (and now also documents
  `view.pick`, which is not a command); `docs/rfcs/0002-plugins.md` still says "No plugin runs"
  while the plugin runtime ships.

## Method

- Pinned the read-only checkout with `git rev-parse HEAD` (equals the release commit) and read the
  installed bundle's `--version` strings; the GUI was never launched, nothing in the checkout was
  modified.
- Counted commands from the installed `solidcraft-cli 0.42.0` (`commands` parsed as JSON: 647
  unique ids, one with a `planned` field). Derived the delta by extracting dotted id literals from
  `crates/engine/src/**/*.rs` in both tags: the extraction reproduces exactly 642 ids in the
  v0.41.0 tree (the v0.41.0 live count) and 647 in the v0.42.0 tree, so the five new ids are the
  whole delta and none was removed.
- Counted typed contracts by calling MCP `describe_command` for all 647 ids in one headless
  `solidcraft-cli mcp --headless` session (612 with both `input` and `output`, 35 with neither);
  counted the tool list from the same session's `tools/list` and from `crates/mcp/src/tools.rs`.
- Diffed the two source trees (v0.41.0 fetched as a tarball, not into the checkout) for: command
  ids, MCP tool names and schemas, CLI verbs and flags, control-protocol method tables, format
  registry rows, skills, crates, docs pages, preferences defaults, kernel measurement code,
  workspace members and the plugin WIT contract.
- Probed the shipped CLI for behaviour that prose cannot settle: `commands`, `--help`, `exec`,
  `run --save` (container + format number), `run --out` (plain JSON), `eval` (measured volume and
  area with `measured_by`), `file.verify` on an unsigned design, and a scripted `file.save` with
  `sign: true` (refused, quoted in `evidence.md`).

## Unchanged

- One command registry is still the API for the desktop app, browser app, CLI, control channel,
  MCP and plugins; sketch commands still return stable `created:` ids; expressions still accept
  parameters and units; the native design is still a `.sc` ZIP container with
  `container.json` + `document.json` + content-addressed `blobs/`, and `.solidcraft`/`.solvecraft`
  still open under their own names; render jobs still run through
  `render.preflight/start/status/cancel/export`; the artefact format set is the same rows plus
  `kicad`; the kernel is still the vendored `solidcore`; independent clean-room status and
  MIT OR Apache-2.0 licensing are unchanged.
- Drawings still have no app or command path (`.scdwg` reader/writer only, the drawings milestone
  still unmerged), and there is still no CAM.
- This skill ships no `references/` directory, because v0.41.0 shipped none: there was nothing to
  preserve and no new automation surface that needed its own file.

## Known gap in this round

- No GUI run and no part built end-to-end beyond the format/measurement probes: capability prose
  comes from the source diff, the shipped CLI's own registry and command replies, and the repo's
  documentation. The oracle report was read, not replayed.
- KiCad import is source- and doc-derived: this tree carries no `.kicad_pcb` fixture, so no board
  was imported. Signing was verified only from the refusing side (an agent cannot sign); no
  signed design was produced, so the verification path (`valid`, `not_covered`, `truncated`) is
  read from `crates/io/src/design/provenance.rs` and `docs/formats/cose-provenance.md`.
- No plugin package was installed or run; the plugin section is unchanged from v0.41.0 after
  re-reading `docs/plugins.md`, `docs/plugin-runtime.md` and the engine's plugin modules.

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
