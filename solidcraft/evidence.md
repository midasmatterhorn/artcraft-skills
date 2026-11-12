# SolidCraft — evidence ledger (tag v0.40.1)

Audit basis: this checkout is tag **`v0.40.1`**, commit **`0c5292285a7e9331a780c11a2d55f22d8e1c9118`**
("Release 0.40.1", 2026-11-11; `git rev-parse HEAD` in the pinned checkout). Inspection date
**2026-11-12**. The installed bundle prints `solidcraft 0.40.1` and ships `solidcraft-cli 0.40.1`
(bundle id `io.tangencylabs.solidcraft`); the GUI was never launched.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | **634** engine commands, dotted ids, one planned (`surface.fillet`, #769) | `solidcraft-cli commands` = 634 unique ids; `docs/features.md` = 634 command rows; `crates/engine/src/cmd/surface.rs` `planned!`; `crates/engine/src/cmd/mod.rs` `command_specs()` | implemented |
| 2 | 561 commands describe both typed input and output JSON Schemas; 73 describe neither (one is the planned `surface.fillet`) | MCP `describe_command` called for all 634 ids in one headless session, counting non-null `input` and `output`; exemption list `crates/engine/src/schema/unconverted.txt` (18 ids); coverage test `crates/engine/src/schema/coverage_tests.rs` warns only (`SCHEMA_RULE_STRICT: bool = false`) | implemented (partial coverage) |
| 3 | Sketch commands return `created: {points, curves, constraints, dimensions}` | `created_doc!` in `crates/engine/src/cmd/mod.rs`; 71 command `params` entries in the registry carry the note (e.g. `sketch.line`) | implemented |
| 4 | **22** MCP tools, including `cancel`, `batch`, `check_parameters`, `skill_reference` | `crates/mcp/src/tools.rs` `tool_definitions_with` (22 `tool("…")` names); `docs/mcp.md` Tools table | implemented |
| 5 | MCP protocol revisions 2025-06-18 / 2025-03-26 / 2024-11-05 | `crates/mcp-server/src/server.rs` `PROTOCOL_VERSION` / `SUPPORTED_VERSIONS`; `docs/mcp.md` header | implemented |
| 6 | MCP file access is limited to the design folder, opened/saved folders, recovery, scratch and `--allow-path`; `--allow-any-path` removes the limit | `docs/mcp.md` "Which files the agent can reach"; `apps/solidcraft-cli/src/main.rs` usage; `crates/mcp/src/options.rs` | implemented |
| 7 | Compact output via app preference, `--compact` or `SOLIDCRAFT_MCP_COMPACT=1` | `crates/mcp/src/options.rs`; `docs/mcp.md` "Compact output" | implemented |
| 8 | **Control channel is off on a new install**; `--control PORT` / `SOLIDCRAFT_CONTROL_PORT` still open one | `crates/ui-egui/src/prefs.rs` `agent_control: bool = false` + test `agent_control_is_off_unless_saved_on`; `crates/ui-egui/src/control_switch.rs`; `apps/solidcraft/src/main.rs` `--control` | implemented |
| 9 | Token is 256-bit, in `control/PORT.token`; port in `control/current.port`; loopback only; 16 connections; 60 s (3600 s batch) timeout | `crates/control/src/auth.rs`; `docs/control-protocol.md` "Token", "Limits", "Finding the port" | implemented |
| 10 | **82** methods/commands documented on the control channel (52 protocol methods + 30 `panel.*`/`layout.*` engine commands) | tables in `docs/control-protocol.md`; dispatch in `crates/control/src/server.rs` and `crates/ui-egui/src/control.rs` | implemented |
| 11 | UI can be driven with real input events (`ui.click`, `ui.drag`, `ui.key`, `ui.text`, `ui.scroll`, `ui.menu`, `ui.pick`, `ui.screenshot`, `ui.render`) | `docs/control-protocol.md` "UI" table; `crates/ui-egui/src/scenario.rs`, `crates/ui-egui/src/control.rs` | implemented |
| 12 | Panel/layout commands (`panel.list/open/close/move/resize/…`, `layout.save/apply/reset/get/workspace.select`) are engine commands | `crates/engine/src/cmd/panels.rs`; `crates/control/src/server.rs`; `docs/control-protocol.md` first section | implemented |
| 13 | **24** CLI verbs: 19 listed + 5 unlisted (`inspect`, `fuzz-one`, `licenses`, `bench-edit`, `save-stress`) | `apps/solidcraft-cli/src/main.rs` `COMMANDS` table; installed `--help` | implemented |
| 14 | `solidcraft-cli mcp setup` adds a server to OpenCode, Claude Desktop, Claude Code or Cursor | `apps/solidcraft-cli/src/main.rs` (`USAGE_MCP`, "mcp setup"); installed `--help` | implemented |
| 15 | Scripts are a JSON list of commands; `script` turns a design's history back into one; `eval` measures as JSON | `docs/scripts.md`; `apps/solidcraft-cli/src/main.rs` `run`/`eval`/`script` usage | implemented |
| 16 | Native design is a ZIP container (`.sc`) holding `container.json` + `document.json` + `blobs/<sha256>.<ext>`; **document format 54** | `crates/format/src/container.rs`; `docs/design-container.md`; `crates/doc/src/format/v54/box-centred.rs` | implemented |
| 17 | Legacy `.solidcraft` / `.solvecraft` and plain `.json` designs still open; new saves are `.sc` | `crates/io/src/lib.rs` `DESIGN_EXT`, `LEGACY_DESIGN_EXTS`, `DESIGN_EXTS`; `docs/compatibility.md` | implemented |
| 18 | **19** format-registry rows; GLB export only, glTF import only, URDF export only, FreeCAD/Rhino import only, DXF/SVG sketch import | `crates/io/src/formats.rs` `FORMATS` (19 `id:` rows) | implemented |
| 19 | A file from a newer build opens with a warning and keeps what this build cannot read | `crates/format/src/newer.rs`; `docs/compatibility.md` | implemented |
| 20 | Send to Slicer / Installed Slicers commands exist | `file.send_to_slicer`, `file.slicers`, `file.open_in_easyprint` in `solidcraft-cli commands`; `crates/engine/src/cmd/file.rs` (`send_to_slicer`), `crates/engine/src/slicers.rs` | implemented |
| 21 | Async render jobs (`render.preflight/start/status/cancel/export`) | `docs/mcp.md` intro; `docs/render-jobs.md`; `render.*` ids in the registry (65) | implemented |
| 22 | **5** embedded agent skills served by `skill_reference` (modeling, editing, checking, mechanisms, sheet metal) and **19** in `skills/` | `crates/mcp/src/skill_reference.rs` `Skill` table; live `skill_reference` with an unknown name replies "Available skills: solidcraft-checking, solidcraft-editing, solidcraft-mechanisms, solidcraft-modeling, solidcraft-sheetmetal"; `skills/README.md` table; `skills/*/SKILL.md` | implemented |
| 23 | Kernel is the vendored `solidcore` (Rust port of NVIDIA SMLib, Apache-2.0) behind `crates/smlib`; `truck-*` is gone from the workspace | `crates/smlib/src/lib.rs`; `Cargo.toml` workspace deps; `solidcore/README.md`; v0.30.1 `Cargo.toml` had `truck-modeling`/`-topology`/`-shapeops`/`-stepio` | implemented |
| 24 | **30** crates under `crates/` (14 at v0.30.1), including shared UI/MCP/control/viewport crates | `crates/` listing; `docs/architecture.md` layer table; `Cargo.toml` | implemented |
| 25 | Assemblies with joints/motion/contact, sheet metal, plastic features, configurations, materials, BOM, notes, point clouds | `joint.*` 19, `motion.*` 11, `contact.*` 7, `sheet.*` 13, `plastic.*` 7, `config.*` 8, `material.*` 8, `assembly.bom`, `note.*` 4, `pointcloud.*` 5 in `solidcraft-cli commands`; `docs/capabilities.md` | implemented |
| 26 | Oracle reports **90/90** pass (69 analytic, 21 FreeCAD) | `docs/oracle.md` generated summary line; `tests/oracle/` (90 case folders) | implemented (doc-level; not replayed) |
| 27 | Independent clean-room; no CAD-vendor affiliation; MIT OR Apache-2.0 | `README.md` Disclaimer/Licence; `NOTICE`; `DISCLAIMER.md`; `LICENSE-MIT`, `LICENSE-APACHE` | policy |
| 28 | macOS bundle signed with a Developer ID and notarized; Windows unsigned | `README.md` Download; `spctl -a -vv` on the installed bundle answers "accepted, source=Notarized Developer ID" | implemented (packaging) |
| 29 | Web app runs the same engine in the browser (`solidcraft-web`, browser command API) | `apps/solidcraft-web/`; `docs/browser-api.md` | implemented (doc-level) |
| 30 | Agent chat panel hosts ACP/API agents, desktop only | `docs/agent-chat.md` ("Desktop app only."); `ui.agent_chat` in `docs/control-protocol.md` | implemented |

## 2. Counts, with the method used

| Surface | v0.40.1 (measured) | Method |
|---|---:|---|
| Engine commands | **634** (1 planned: `surface.fillet`) | `solidcraft-cli commands` parsed as JSON, unique `id`; cross-checked with `docs/features.md` rows (634) and source registries |
| Typed contracts | **561** of 634 (73 with neither schema) | MCP `describe_command` for every id in one headless session; `input` and `output` both non-null |
| MCP tools | **22** | first string argument of every `tool(...)` in `crates/mcp/src/tools.rs` |
| CLI verbs | **19 listed + 5 unlisted** | `Command { …, listed: … }` rows in `apps/solidcraft-cli/src/main.rs` |
| Control methods/commands | **82** (52 protocol + 30 panel/layout) | unique backticked ids in `docs/control-protocol.md` tables |
| In-repo agent skills | **19** | folders under `skills/` |
| Embedded skills | **5** | `Skill { name: … }` entries in `crates/mcp/src/skill_reference.rs` |
| Format-registry rows | **19** | `id:` entries inside `pub static FORMATS` in `crates/io/src/formats.rs` |
| Workspace crates | **30** | folders under `crates/` |
| docs pages | **137** | `ls docs/*.md` |
| Oracle cases | **90/90** (69 analytic / 21 FreeCAD) | summary line in `docs/oracle.md`; `tests/oracle/` case folders |
| Control port | **27878**, next free up to 27893 | `docs/control-protocol.md` "What listens"; `crates/control/src/auth.rs` (`default_port: 27878`) |
| Design format | **54** | `crates/doc/src/format/v54/`; `FORMAT = FORMATS.current()` in `crates/doc/src/format.rs` |

Deltas measured by diffing the same surfaces against `v0.30.1` with `git show`:
commands 570 -> 634 (+64, 0 removed), MCP 21 -> 22 (+`cancel`), control methods 46 -> 82 (+36,
0 removed), CLI 23 -> 24 rows (+`kernel-cases`), skills 17 -> 19, crates 14 -> 30, format 48 -> 54,
format rows 18 -> 19, docs 119 -> 137.

## 3. Drift between docs and code (code wins)

| Doc statement | Code / measured truth |
|---|---|
| `AGENTS.md` / `docs/book` imply every command has input and output schemas | `describe_command` reports 73 of 634 with neither; the coverage test's `SCHEMA_RULE_STRICT` is `false`, so it warns, and `unconverted.txt` exempts only 18 |
| `docs/control-protocol.md`: "Let AI agents connect" on "(the default)" | `crates/ui-egui/src/prefs.rs` `agent_control: bool = false`; test `agent_control_is_off_unless_saved_on`; `docs/mcp.md` agrees with the code |
| `README.md` and `docs/capabilities.md`: "75 of 76" reference parts | `docs/oracle.md`: 90/90 (69 analytic, 21 FreeCAD) |
| `docs/mcp.md` "Agent skills": five skills, listing `solidcraft-reporting` | `crates/mcp/src/skill_reference.rs` embeds modeling, editing, checking, mechanisms, **sheetmetal**; reporting is not embedded |
| `crates/mcp/src/tools.rs` `skill_reference` description lists four skills | table embeds five (sheetmetal missing from the text only) |
| `ROADMAP.md`: SMLib "not in releases yet"; drawings "not in the app yet" | `Cargo.toml` and `crates/kernel` build on the vendored solidcore, so the SMLib statement is stale. The drawings statement holds at the app level: `.scdwg` has a document model and reader/writer (`crates/doc/src/drawing.rs`, `crates/io/src/design/drawing.rs`) but no caller opens one and no `drawing.*` command exists; the Insert Drawing dialog is for SVG/DXF |
| `docs/mcp.md` `open` tool row: STEP/STP and 3MF/STL | tool description in `crates/mcp/src/tools.rs` also takes OBJ/GLB/glTF and names IGES/FreeCAD/Rhino |
| `docs/oracle.md`: 90/90 pass | same page's validation note says case 95's centre-of-mass reference was corrected after the run and needs a replay |
| Old skill: "the app listens by default" (true at v0.30.1) | false at v0.40.1 (see above) |
| Old skill: `snapshot … -o shot.png`; `solidcraft-cli oracle` with no arguments | `apps/solidcraft-cli/src/main.rs`: `--out` only; `apps/solidcraft-cli/src/oracle.rs` refuses with "give one or more case directories" |

## 4. Re-measured, carried forward, unverified

**Re-measured at v0.40.1:** command ids (634), typed-contract coverage (561), MCP tools (22), CLI
verbs (19 + 5), control methods/commands (82), format-registry rows (19), in-repo and embedded
skills (19 / 5), crates (30), docs pages (137), design format (54), oracle summary (90/90), and the
control-channel default (off). **Carried forward from the v0.30.1 audit after path re-resolution:**
the sketch `created:` contract, the CLI's long-standing flags, the design-container layout, the
render-job flow, and the licensing/clean-room statements.

- GUI appearance, dialogs and menu labels were not exercised; claims about them come from
  `docs/control-protocol.md`, `docs/agent-chat.md` and the command registry's toolbar placement.
- The browser build (`apps/solidcraft-web`) and `docs/browser-api.md` were read at doc level.
- Geometric capability lists (fillet/chamfer/boolean extents, sheet-metal options) are the
  project's own `docs/capabilities.md` and `ROADMAP.md` claims; no part was built in this round.
- The 0.40.0 kernel/mesher/STEP-reader replacement is evidenced by the dependency graph, crate
  layout and vendored `solidcore` tree; its accuracy was not tested against the old kernel.

## 5. Read-only verification commands

```sh
git rev-parse HEAD                                                     # 0c529228…
solidcraft-cli --version                                                # solidcraft-cli 0.40.1
solidcraft-cli commands | jq length                                     # 634 (or: … | jq -r '.[].id' | sort -u | wc -l)
perl -0777 -ne 'while (/\btool\(\s*"([a-z_0-9]+)"/g) { print "$1\n" }' \
  crates/mcp/src/tools.rs | sort -u | wc -l                            # 22
grep -cE 'Command \{ name: ".*listed: true' apps/solidcraft-cli/src/main.rs    # 19
grep -cE 'Command \{ name: ".*listed: false' apps/solidcraft-cli/src/main.rs   # 5
ls docs/*.md | wc -l                                                   # 137
ls -d skills/*/ | wc -l                                                # 19
ls -d crates/*/ | wc -l                                                # 30
grep -cE '^[a-z]' crates/engine/src/schema/unconverted.txt             # 18 exemptions
```
