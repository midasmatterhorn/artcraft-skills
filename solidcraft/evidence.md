# SolidCraft — evidence ledger (tag v0.41.0)

Audit basis: the source is tag **`v0.41.0`**, commit **`3c8efdb51952ed9a5f3ebc722c2bad1454fe6d80`**
("Release 0.41.0", 2026-11-13; the GitHub ref `tags/v0.41.0` resolves to it and the release notes
name it as `target_commitish`). Inspection date **2026-11-14**. The installed bundle prints
`solidcraft 0.41.0` and ships `solidcraft-cli 0.41.0` (bundle id `io.tangencylabs.solidcraft`,
notarized); the GUI was never launched. The previous round audited v0.40.1
(`0c5292285a7e9331a780c11a2d55f22d8e1c9118`).

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | **642** engine commands, dotted ids, one planned (`surface.fillet`, #769) | `solidcraft-cli commands` = 642 unique ids; `crates/engine/src/cmd/surface.rs` `planned!`; the CLI JSON carries `planned: "769"` for that id only; `docs/features.md` has only 636 rows (stale by six: four `plugin.*`, `model.mesh`, `file.import_cache_clear`) | implemented |
| 2 | 572 commands describe both typed input and output JSON Schemas; 70 describe neither (one is the planned `surface.fillet`) | MCP `describe_command` called for all 642 ids in one headless session, counting non-null `input` and `output`; exemption list `crates/engine/src/schema/unconverted.txt`; coverage test `crates/engine/src/schema/coverage_tests.rs` warns only (`SCHEMA_RULE_STRICT: bool = false`) | implemented (partial coverage) |
| 3 | Sketch commands return `created: {points, curves, constraints, dimensions}` | `created_doc!` in `crates/engine/src/cmd/mod.rs`; 71 command `params` entries in the registry carry the note (e.g. `sketch.line`) | implemented |
| 4 | **22** MCP tools, including `cancel`, `batch`, `check_parameters`, `skill_reference` | `crates/mcp/src/tools.rs` `tool_definitions_with` (22 `tool(...)` names); live `tools/list` over a headless session returned the same 22 | implemented |
| 5 | MCP protocol revisions 2025-06-18 / 2025-03-26 / 2024-11-05 | `crates/mcp-server/src/server.rs` `PROTOCOL_VERSION` / `SUPPORTED_VERSIONS` (unchanged from v0.40.1); `docs/mcp.md` header | implemented |
| 6 | MCP file access is limited to the design folder, opened/saved folders, recovery, scratch and `--allow-path`; `--allow-any-path` removes the limit | `docs/mcp.md` "Which files the agent can reach" (unchanged this round); `apps/solidcraft-cli/src/main.rs` usage; `crates/mcp/src/options.rs` | implemented |
| 7 | Compact output via app preference, `--compact` or `SOLIDCRAFT_MCP_COMPACT=1` | `crates/mcp/src/options.rs`; `docs/mcp.md` "Compact output" | implemented |
| 8 | **Control channel is off on a new install**; `--control PORT` / `SOLIDCRAFT_CONTROL_PORT` still open one | `crates/ui-egui/src/prefs.rs` `agent_control: bool = false` + test `agent_control_is_off_unless_saved_on`; `crates/ui-egui/src/control_switch.rs`; `apps/solidcraft/src/main.rs` `--control` | implemented |
| 9 | Token is 256-bit, in `control/PORT.token`; port in `control/current.port`; loopback only; 16 connections; 60 s (3600 s batch) timeout | `crates/control/src/auth.rs` (unchanged); `docs/control-protocol.md` "Token", "Limits" | implemented |
| 10 | **82** documented methods/commands on the control channel, unchanged from v0.40.1 | rows of the method tables in `docs/control-protocol.md` (82 in both tags, identical name set); dispatch in `crates/control/src/server.rs` and `crates/ui-egui/src/control.rs` | implemented |
| 11 | UI can be driven with real input events (`ui.click`, `ui.drag`, `ui.key`, `ui.text`, `ui.scroll`, `ui.menu`, `ui.pick`, `ui.screenshot`, `ui.render`) | `docs/control-protocol.md` "UI" table; `crates/ui-egui/src/scenario.rs`, `crates/ui-egui/src/control.rs` | implemented |
| 12 | Panel/layout commands (`panel.*`, `layout.save/apply/reset/get/workspace.select`) are engine commands | `crates/engine/src/cmd/panels.rs`; `crates/control/src/server.rs`; `docs/control-protocol.md` first section | implemented |
| 13 | **24** CLI verbs: 19 listed + 5 unlisted (`inspect`, `fuzz-one`, `licenses`, `bench-edit`, `save-stress`), unchanged from v0.40.1 | `apps/solidcraft-cli/src/main.rs` `COMMANDS` table (diff vs v0.40.1 empty); installed `--help` | implemented |
| 14 | New global `--plugin-limits FILE.json` sets user fuel/memory ceilings; `{max_fuel, max_memory_mib}` defaults 100000000000 / 128, invocation defaults 10,000,000 / 64 MiB; local sessions only, `mcp --headless` accepts it | `apps/solidcraft-cli/src/main.rs` (usage constant, parser, "controls local sessions" error); installed `--help` footer | implemented |
| 15 | `solidcraft-cli mcp setup` adds a server to OpenCode, Claude Desktop, Claude Code or Cursor | `apps/solidcraft-cli/src/main.rs` (`USAGE_MCP`, "mcp setup"); installed `--help` | implemented |
| 16 | Scripts are a JSON list of commands; `script` turns a design's history back into one; `eval` measures as JSON | `docs/scripts.md`; `apps/solidcraft-cli/src/main.rs` `run`/`eval`/`script` usage | implemented |
| 17 | Native design is a ZIP container (`.sc`) holding `container.json` + `document.json` + `blobs/<sha256>.<ext>`; **document format 55** | `crates/format/src/container.rs`; `docs/design-container.md`; `crates/doc/src/format/v55/`; probe: `run build.json --save box.sc` then `unzip` → `document.json` `"format": "solidcraft/55"`; release notes "0.41.0 writes design file format 55" | implemented |
| 18 | Format 55 adds Move rotation origin, snap-point construction geometry, dragged spline tangent handles, Split Face loops, projected-vertex names, plugin data | release notes "Compatibility"; `crates/doc/src/format/v55/`; `crates/doc/src/plugin_data.rs`; command params for `solid.move` (`matrix`, `origin`), `solid.split_face` (`loops`), `sketch.spline.handles` | implemented |
| 19 | A design can carry `plugins/<plugin-id>/` files (base64 in plain JSON), at most 1024 files, kept byte for byte without the plugin; `storage` capability is future work | `crates/doc/src/plugin_data.rs` (`PREFIX = "plugins/"`, `MAX_FILES = 1024`, doc comment); `docs/plugins.md` "Plugin data in a design" | implemented |
| 20 | Legacy `.solidcraft` / `.solvecraft` and plain `.json` designs still open; new saves are `.sc` | `crates/io/src/lib.rs` `DESIGN_EXT`, `LEGACY_DESIGN_EXTS`, `DESIGN_EXTS`; `docs/compatibility.md` | implemented |
| 21 | **19** format-registry rows; GLB export only, glTF import only, URDF export only, FreeCAD/Rhino import only, DXF/SVG sketch import | `crates/io/src/formats.rs` `FORMATS` (19 `id:` rows, unchanged from v0.40.1) | implemented |
| 22 | A file from a newer build opens with a warning and keeps what this build cannot read; 0.40.x opens a 0.41 design with a warning, 0.30.1 refuses it | `crates/format/src/newer.rs`; `docs/compatibility.md`; release notes "Compatibility" | implemented |
| 23 | Send to Slicer / Installed Slicers commands exist | `file.send_to_slicer`, `file.slicers`, `file.open_in_easyprint` in `solidcraft-cli commands`; `crates/engine/src/cmd/file.rs` (`send_to_slicer`), `crates/engine/src/slicers.rs` | implemented |
| 24 | Async render jobs (`render.preflight/start/status/cancel/export`) | `docs/mcp.md` intro; `docs/render-jobs.md`; `render.*` ids in the registry (65) | implemented |
| 25 | **5** embedded agent skills served by `skill_reference` (modeling, editing, checking, mechanisms, sheet metal) and **19** in `skills/` | `crates/mcp/src/skill_reference.rs` `Skill` table; live `skill_reference` with an unknown name replies "Available skills: solidcraft-checking, solidcraft-editing, solidcraft-mechanisms, solidcraft-modeling, solidcraft-sheetmetal"; `skills/*/SKILL.md` (19 folders plus a README) | implemented |
| 26 | Kernel is the vendored `solidcore` (Rust port of NVIDIA SMLib, Apache-2.0) behind `crates/smlib`; unchanged this round | `crates/smlib/src/lib.rs`; `Cargo.toml` workspace deps; `solidcore/README.md`; `crates/kernel` diff vs v0.40.1 shows no crate swap | implemented |
| 27 | **32** crates under `crates/` (30 at v0.40.1), including `craft-plugin` and `craft-plugin-wasm` | `crates/` listing (32 folders with `Cargo.toml`); `docs/plugins.md` "Phase 1 splits the host into two app-agnostic crates" | implemented |
| 28 | Assemblies with joints/motion/contact, sheet metal, plastic features, configurations, materials, BOM, notes, point clouds | `joint.*` 19, `motion.*` 11, `contact.*` 7, `sheet.*` 13, `plastic.*` 7, `config.*` 8, `material.*` 8, `assembly.bom`, `note.*` 4, `pointcloud.*` 5 in `solidcraft-cli commands`; `docs/capabilities.md` | implemented |
| 29 | Oracle reports **90/90** pass (69 analytic, 21 FreeCAD) | `docs/oracle.md` generated summary line (unchanged); `tests/oracle/` (90 case folders) | implemented (doc-level; not replayed) |
| 30 | Independent clean-room; no CAD-vendor affiliation; MIT OR Apache-2.0 | `README.md` Disclaimer/Licence; `NOTICE`; `DISCLAIMER.md`; `LICENSE-MIT`, `LICENSE-APACHE` | policy |
| 31 | macOS bundle signed with a Developer ID and notarized; Windows builds now use SignPath-provided signing (SmartScreen may still warn until the production cert) | `spctl -a -vv` on the installed bundle: "accepted, source=Notarized Developer ID"; `README.md` Download (SignPath paragraph) | implemented (packaging) |
| 32 | Web app runs the same engine in the browser (`solidcraft-web`, browser command API) | `apps/solidcraft-web/`; `docs/browser-api.md` | implemented (doc-level) |
| 33 | Agent chat panel hosts ACP/API agents, desktop only; asks before executing external plugin code | `docs/agent-chat.md`; `README.md` Plugins ("Agent chat asks before executing external plugin code"); `ui.agent_chat` in `docs/control-protocol.md` | implemented |
| 34 | **Plugins are sandboxed WebAssembly components** run against the command registry: WIT `craft:plugin@0.1.0`, capability `commands@0.1`, no WASI/network, fuel/memory/deadline, one undo step, rollback on failure | `docs/plugins.md`; `docs/plugin-runtime.md` (boundary, lifecycle, manifest); `crates/craft-plugin/wit/plugin.wit`; `crates/engine/src/plugin.rs`; release notes "Plugins, first version" | implemented (experimental) |
| 35 | `plugin.install` unpacks a zip (one plugin, safe paths, 16 MiB per entry / 64 MiB unpacked / 16 KiB manifest; no code runs); `plugin.inspect` reads a folder and returns manifest + approval SHA-256; `plugin.run` needs that exact hash and one entry | `crates/engine/src/cmd/plugin.rs` (specs, `install`, `inspect`, `run`); `docs/plugins.md` "Installing"; `docs/plugin-runtime.md` steps 1–4; README "Run explicitly" | implemented |
| 36 | Plugins may call only commands their manifest lists; `file`/`doc`/`app`/`plugin` groups need a manifest permission plus a user grant; `net` is refused; file access needs folder grants | `docs/plugins.md` "Commands and permissions"; `crates/engine/src/plugin.rs` (`COMMAND_GROUPS`, `AppState.file_grants`, `command_groups`) | implemented |
| 37 | Over the running desktop, `plugin.run` is refused inside `engine.batch` and `engine.script`; headless CLI scripts may include it; the desktop runs it on a worker | `crates/ui-egui/src/control.rs` `batch_refusal` / `script` (refusal text `ui.plugin_standalone`); `crates/ui-egui/src/control_job.rs`; README "Run explicitly" | implemented |
| 38 | Slow agent commands compute off the window thread by default on new installs; each waiting command is its own cancellable operations row | `crates/ui-egui/src/prefs.rs` `agent_off_thread: bool = true` (was false at v0.40.1) + migration test; release notes "#15362, #15381"; `docs/control-protocol.md` `ui.operations` (`next`, `percent`) | implemented |
| 39 | 0.41 repairs: near-tangent fillet/chamfer mitre instead of failure; 2° tangent chain; STEP export orientation; STEP import wrapped sphere/cone faces; sheet-metal fold across tabs keeps faces; GLB keeps assembly nodes; `lay_on_print_faces`; Move `matrix`/`origin`; Split Face `loops`; Split Body by closed surface; snap points; ISO thread sizes M3.5/M7/M33/M39/M45; contour-flange tangent arcs; Constrain dialog | release notes "New"/"Fixed"/"Also in this release"; `crates/engine/src/cmd/features.rs` (`solid.move` params `matrix`, `origin`; `solid.split_face` `loops`); `crates/engine/src/cmd/file.rs` (`lay_on_print_faces`); `docs/threads.md`; `crates/doc/src/thread_forms.rs`; `docs/capabilities.md` GLB line; source tree | implemented (release-notes + source; not exercised) |

## 2. Counts, with the method used

| Surface | v0.41.0 (measured) | v0.40.1 | Method |
|---|---:|---:|---|
| Engine commands | **642** (1 planned: `surface.fillet`) | 634 | `solidcraft-cli commands` parsed as JSON, unique `id`; `planned` field for the one planned id |
| Typed contracts | **572** of 642 (70 with neither schema) | 561 / 73 | MCP `describe_command` for every id in one headless session; `input` and `output` both non-null |
| MCP tools | **22** | 22 | first string argument of every `tool(...)` in `crates/mcp/src/tools.rs`; confirmed by live `tools/list` |
| CLI verbs | **19 listed + 5 unlisted** (plus global `--plugin-limits`) | 19 + 5 | `Command { …, listed: … }` rows in `apps/solidcraft-cli/src/main.rs`; diff vs v0.40.1 empty |
| Control methods/commands | **82** | 82 | rows of the method tables in `docs/control-protocol.md` (identical name set at both tags) |
| In-repo agent skills | **19** | 19 | folders under `skills/` |
| Embedded skills | **5** | 5 | `Skill { name: … }` entries in `crates/mcp/src/skill_reference.rs`; live reply |
| Format-registry rows | **19** | 19 | `id:` entries inside `pub static FORMATS` in `crates/io/src/formats.rs` |
| Workspace crates | **32** | 30 | folders under `crates/` with a `Cargo.toml` |
| docs pages | **139** | 137 | `ls docs/*.md` (+ `plugin-runtime.md`, `plugin-test-guide.md`) |
| Oracle cases | **90/90** (69 analytic / 21 FreeCAD) | 90/90 | summary line in `docs/oracle.md`; `tests/oracle/` case folders |
| Control port | **27878**, next free up to 27893 | same | `docs/control-protocol.md` "What listens"; `crates/ui-egui/src/prefs.rs` `agent_control_port: u16 = 27878` |
| Design format | **55** | 54 | `crates/doc/src/format/v55/`; probe save → `document.json` `"format": "solidcraft/55"` |
| Plugin host limits | invocation **10,000,000 fuel / 64 MiB**; user ceilings **100,000,000,000 / 128 MiB** | n/a | installed `solidcraft-cli --help` `--plugin-limits` footer; `crates/engine/src/plugin.rs` `HostLimits` |

Deltas measured by diffing the same surfaces against `v0.40.1` from the two GitHub tarballs
(`codeload` at `3c8efdb…` and `0c529228…`): commands 634 -> 642 (+8, 0 removed: `plugin.inspect`,
`plugin.install`, `plugin.list`, `plugin.run`, `model.mesh`, `file.import_cache_clear`,
`sketch.spline.handles`, `sketch.spline.reset_handles`), typed contracts 561 -> 572, crates 30 -> 32,
docs 137 -> 139, design format 54 -> 55; MCP tools, CLI verbs, control methods, format rows,
in-repo/embedded skills and the oracle summary unchanged. `docs/features.md` went 634 -> 636 rows
(only the two sketch ids) while the registry has 642.

## 3. Drift between docs and code (code wins)

| Doc statement | Code / measured truth |
|---|---|
| `docs/features.md` lists every command (generated by `cargo xtask features`) | 636 rows vs 642 ids in `solidcraft-cli commands`; missing `plugin.inspect/install/list/run`, `model.mesh`, `file.import_cache_clear`. `xtask/src/features.rs` has no filter, so the page was simply not regenerated at the release |
| `docs/control-protocol.md` launch table: "Let AI agents connect" on "(the default)"; "Old preference files … load with it on" | `crates/ui-egui/src/prefs.rs` `agent_control: bool = false`; test `agent_control_is_off_unless_saved_on` asserts off for a new install **and** for prefs saved before the setting; `docs/control-protocol.md` line ~418 itself says "off by default" |
| `README.md` and `docs/capabilities.md`: "75 of 76" reference parts | `docs/oracle.md`: 90/90 (69 analytic, 21 FreeCAD) |
| `docs/mcp.md` "Agent skills": lists `solidcraft-reporting` | `crates/mcp/src/skill_reference.rs` embeds modeling, editing, checking, mechanisms, **sheetmetal**; reporting is not embedded |
| `crates/mcp/src/tools.rs` `skill_reference` description lists four skills | table embeds five (sheetmetal missing from the text only) |
| `docs/oracle.md`: 90/90 pass | same page's validation note says case 95's centre-of-mass reference was corrected after the run and needs a replay |
| `AGENTS.md` / `docs/book` imply every command has input and output schemas | 70 of 642 have neither; the coverage test's `SCHEMA_RULE_STRICT` is `false`, so it warns, and `unconverted.txt` exempts only old commands |
| `docs/compatibility.md` "Edge references after the kernel swap" | holds at v0.41.0; no new edge-reference work in this release |
| `docs/rfcs/0002-plugins.md`: "Only the Preferences page exists today. No plugin runs." | Contradicts the implemented phase 1 in the same tree (`crates/engine/src/cmd/plugin.rs`, `docs/plugins.md`, `docs/plugin-runtime.md`) and the v0.41.0 release notes, which announce the plugin runtime. The RFC's status table still says "Draft"; treat the implementation and `docs/plugins.md` as the truth |
| `crates/engine/src/schema/unconverted.txt` | 21 exempted ids at v0.41.0 (18 at v0.40.1); the coverage test still only warns (`SCHEMA_RULE_STRICT: bool = false`) |

## 4. Re-measured, carried forward, unverified

**Re-measured at v0.41.0:** command ids (642), typed-contract coverage (572), MCP tools (22),
CLI verbs (19 + 5) and the new `--plugin-limits` flag, control methods/commands (82),
format-registry rows (19), in-repo and embedded skills (19 / 5), crates (32), docs pages (139),
design format (55, by saving a probe design and reading `document.json`), oracle summary (90/90),
the control-channel default (off) and `agent_off_thread` (now on by default). **Carried forward
from the previous audits after path re-resolution:** the sketch `created:` contract, the design
container layout, the render-job flow, the MCP protocol revisions, the file-scope rules, and the
licensing/clean-room statements.

- GUI appearance, dialogs and menu labels were not exercised; claims about them come from
  `README.md`, `docs/control-protocol.md`, `docs/agent-chat.md`, `docs/plugins.md` and the command
  registry's toolbar placement.
- The plugin runtime was not executed in this round: no package was installed or run. Claims come
  from `docs/plugins.md`, `docs/plugin-runtime.md`, `crates/engine/src/{plugin.rs,cmd/plugin.rs}`,
  `crates/craft-plugin`, and the release notes; the `plugin.*` command contracts were read from
  the installed CLI's `commands` output.
- Geometric capability lists (fillet/chamfer/boolean extents, sheet-metal options, 0.41 fixes) are
  the project's own release notes, `docs/capabilities.md` and `ROADMAP.md` claims; no part was
  built in this round.
- The browser build (`apps/solidcraft-web`) and `docs/browser-api.md` were read at doc level; the
  web app does not run plugins.

## 5. Read-only verification commands

```sh
# from the v0.41.0 source tree
solidcraft-cli --version                                                # solidcraft-cli 0.41.0
solidcraft-cli commands | jq length                                     # 642
solidcraft-cli commands | jq -r '.[] | select(.planned) | .id'          # surface.fillet
solidcraft-cli exec solid.box '{"length":20,"width":10,"height":5}' >/dev/null
solidcraft-cli run build.json --save box.sc                            # then unzip: "format": "solidcraft/55"
perl -0777 -ne 'while (/\btool\(\s*"([a-z_0-9]+)"/g) { print "$1\n" }' \
  crates/mcp/src/tools.rs | sort -u | wc -l                             # 22
grep -cE 'Command \{ name: ".*listed: true' apps/solidcraft-cli/src/main.rs    # 19
grep -cE 'Command \{ name: ".*listed: false' apps/solidcraft-cli/src/main.rs   # 5
ls docs/*.md | wc -l                                                   # 139
ls -d skills/*/ | wc -l                                                # 19
ls -d crates/*/ | wc -l                                                # 32
grep -c '    agent_off_thread: bool = true' crates/ui-egui/src/prefs.rs  # 1
grep -c '    agent_control: bool = false' crates/ui-egui/src/prefs.rs    # 1
```

Headless MCP count of typed contracts: initialize `solidcraft-cli mcp --headless`, then call
`describe_command` for each of the 642 ids and count replies with non-null `input` and `output`
(572 both / 70 neither).
