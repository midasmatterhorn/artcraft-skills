# SolidCraft — evidence ledger (tag v0.42.0)

Audit basis: the source is tag **`v0.42.0`**, commit **`1b1e940cc48e4d1d5d01971a4be20e2e55647066`**
("Merge main into release for 0.42.0", 2026-11-14; `git rev-parse HEAD` in the pinned read-only checkout returns it and
`git describe --tags` returns `v0.42.0`). Inspection date **2026-11-15**. The installed bundle
matches: `CFBundleShortVersionString` 0.42.0, `CFBundleIdentifier` `io.tangencylabs.solidcraft`,
notarized Developer ID; its binaries print `solidcraft 0.42.0` and `solidcraft-cli 0.42.0`. The GUI
was never launched. The previous round audited v0.41.0
(`3c8efdb51952ed9a5f3ebc722c2bad1454fe6d80`).

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | **647** engine commands, dotted ids, one planned (`surface.fillet`, #769) | `solidcraft-cli commands` = 647 unique ids (installed 0.42.0); that id carries `planned: "769"` and `disabled_reason: "not supported yet (issue #769)"`; `crates/engine/src/cmd/surface.rs` `planned!`; `docs/features.md` has 646 rows (one behind: `sketch.insert_airfoil`) | implemented |
| 2 | 612 commands describe both typed input and output JSON Schemas; 35 describe neither (one is the planned `surface.fillet`) | MCP `describe_command` called with `id` for all 647 ids in one `solidcraft-cli mcp --headless` session, counting non-null `input`/`output`; exemption list `crates/engine/src/schema/unconverted.txt` (16 ids); coverage test `crates/engine/src/schema/coverage_tests.rs` warns only (`SCHEMA_RULE_STRICT: bool = false`) | implemented (partial coverage) |
| 3 | Sketch commands return `created: {points, curves, constraints, dimensions}` | `created_doc!` in `crates/engine/src/cmd/mod.rs`; every sketch command's `params` text in `solidcraft-cli commands` carries the note | implemented |
| 4 | **22** MCP tools, same names as v0.41.0 | `crates/mcp/src/tools.rs` `tool_definitions_with` (22 `tool(...)` names, `sort -u`); live `tools/list` returned the same 22 and `serverInfo.version` 0.42.0 | implemented |
| 5 | MCP protocol revisions 2025-06-18 / 2025-03-26 / 2024-11-05, unchanged | `crates/mcp-server/src/server.rs` `PROTOCOL_VERSION` / `SUPPORTED_VERSIONS`; live `initialize` negotiated 2025-06-18 | implemented |
| 6 | MCP argument schemas use `anyOf` where an argument has two types, replacing two-type `type` lists | `crates/mcp/src/tools.rs` (`timeline_arg`, `bodies`, `value`/`expression`, `additionalProperties`); in-code reasons: Moonshot refused every tool with a two-type argument, Gemini refused the list form | implemented |
| 7 | `describe_command` takes `id` | live call with `command` refused: "describe_command: missing required argument `id`"; the same call with `id` returns the schemas | implemented |
| 8 | **Control channel is off on a new install**; `--control PORT` / `SOLIDCRAFT_CONTROL_PORT` still open one; port 27878, next free to 27893 | `crates/ui-egui/src/prefs.rs` `agent_control: bool = false` + test `agent_control_is_off_unless_saved_on`, `agent_control_port: u16 = 27878`; `apps/solidcraft/src/main.rs` parses `--control`; `docs/control-protocol.md` | implemented |
| 9 | Token is 256-bit, in `control/PORT.token`; port in `control/current.port`; loopback only; 16 connections; 60 s (3600 s batch) timeout | `crates/control/src/auth.rs` (identical to v0.41.0 by `diff`); `docs/control-protocol.md` "Limits" | implemented |
| 10 | **82** documented methods/commands, identical name set at v0.41.0 | first-column ids of the method tables in `docs/control-protocol.md` (30 panel/layout + 11 engine + 42 UI rows, 82 unique; `engine.execute` sits in two tables); tree-to-tree diff adds and removes none; dispatch in `crates/control/src/server.rs`, `crates/ui-egui/src/control.rs` | implemented |
| 11 | UI can be driven with real input events (`ui.click`, `ui.drag`, `ui.key`, `ui.text`, `ui.scroll`, `ui.menu`, `ui.pick`, `ui.screenshot`, `ui.render`) | `docs/control-protocol.md` "UI" table; `crates/ui-egui/src/scenario.rs`, `crates/ui-egui/src/control.rs` | implemented |
| 12 | `view.pick` is an app-handled control method, not a registry command, and is unavailable in headless MCP | `crates/mcp/src/tools.rs` `execute` tool description says it is handled by the app and absent from `list_commands`/`describe_command`; `docs/mcp.md` says the same; `view.pick` is absent from `solidcraft-cli commands` (647 ids contain no such id) | implemented |
| 13 | **24** CLI verbs: 19 listed + 5 unlisted (`inspect`, `fuzz-one`, `licenses`, `bench-edit`, `save-stress`), unchanged | `apps/solidcraft-cli/src/main.rs` (`listed: true` × 19, `listed: false` × 5); installed `--help` | implemented |
| 14 | Two new CLI flags: `--require-allow-path` (mcp), `--script-relative` (run) | `apps/solidcraft-cli/src/main.rs` (`USAGE_MCP`, `USAGE_RUN`, parser, refusal text "every --allow-path folder is missing or unusable"); installed `--help` shows both; a tree-to-tree flag diff finds exactly these two added and none removed | implemented |
| 15 | A `--allow-path` folder that cannot be used is reported, not dropped | `apps/solidcraft-cli/src/main.rs` `eprintln!("solidcraft mcp: allow-path {} ignored: {}")`; `docs/mcp.md` (folder rules section) | implemented |
| 16 | `--plugin-limits FILE.json` ceilings (100000000000 fuel / 128 MiB) with 10,000,000 / 64 MiB invocation defaults, local sessions only | `apps/solidcraft-cli/src/main.rs`; installed `--help` footer; `crates/engine/src/plugin.rs` `HostLimits` | implemented |
| 17 | Scripts are a JSON list of commands; `script` turns a design's history back into one; `eval` measures as JSON | `docs/scripts.md`; `apps/solidcraft-cli/src/main.rs` usage; probe: `eval` on a 40×30×20 box replied `volume_mm3` 24000.0, `area_mm2` 5200.0 | implemented |
| 18 | Native design is a ZIP container holding `container.json`, `document.json` and `blobs/<sha256>.<ext>`; **document format 57** | `crates/format/src/container.rs`; `docs/design-container.md`; probe: `run build.json --save box.sc` then `unzip` → `document.json` `"format": "solidcraft/57"` and `format_pending` naming two changes | implemented |
| 19 | Format 56 is folded from five change files; 57 adds two pending changes (extrude-to-object placements, plane-at-angle named axis) | `crates/doc/src/format/v56/cell-grid-feature.rs`, `frame-member-locate.rs`, `frame-standard-sizes.rs`, `occurrence-move-expressions.rs`, `pattern-names-by-source.rs`; `crates/doc/src/format/pending/extrude-to-object-keeps-picked-placements.rs`, `plane-at-angle-follows-named-axis.rs`; `crates/doc/src/format.rs` (`FORMAT` = `FORMATS.current()`) | implemented |
| 20 | **New: signed provenance** — `provenance/log.cbor` chain of COSE_Sign1 (Ed25519) or OpenPGP records over the authoritative entries, chained by digest, bounded envelope, truncation signed | `crates/io/src/design/provenance.rs`; `docs/formats/cose-provenance.md` (envelope CDDL, manifest, record kinds, limits) | implemented (module + spec; not exercised end to end) |
| 21 | `file.verify` reports unsigned/valid/not_covered/invalid/unsupported plus `truncated`, and records with method/key/author | `crates/engine/src/cmd/file.rs` (`file.verify`, `VerifyResult`); probe on an unsigned `.sc`: `{"status":"unsigned","records":[],"truncated":false}` | implemented (read-only path exercised) |
| 22 | `file.gpg_keys` lists GnuPG keys with fingerprint/key_id/user_id/on_card, desktop only | `crates/engine/src/cmd/file.rs`; `crates/engine/src/gpg.rs` | implemented (desktop) |
| 23 | `file.save` takes `sign`/`signing_key` and returns `signature`; scripts and agents are refused | `file.save`'s `params` in `solidcraft-cli commands`; live refusal: "signing is only available from the app's Save, with the key chosen in Preferences; a script or agent cannot sign" | implemented (refusal exercised) |
| 24 | `doc.open` takes `verify` and reports `signature`, plus KiCad options | `doc.open`'s `params` in `solidcraft-cli commands` | implemented |
| 25 | Security preferences carry the trust model: `sign_saved_designs` (false), `signing_key` (empty), `trusted_signing_keys` (empty: only these show as verified, others in grey), `verify_opened_designs` (false) | `crates/ui-egui/src/prefs.rs` (`PAGE_SECURITY` settings), `crates/ui-egui/src/prefs/security.rs`; `docs/control-protocol.md` prefs list | implemented |
| 26 | **New: KiCad PCB import** — 20th format row, `.kicad_pcb`/`.kicad_pro`, B-rep substrate with drilled holes, copper overlay or 0.035 mm solids, silkscreen, text, footprint 3D models | `crates/io/src/formats.rs` (`id: "kicad"`, `ImportTarget::Kicad`); `crates/io/src/kicad_in.rs`; `docs/kicad-import.md`; `docs/book/src/dev/kicad-import.md` | implemented (source + doc; no fixture in this tree, not exercised) |
| 27 | **New commands**: `sketch.insert_airfoil` (Selig/Lednicer `.dat` → one fit spline, chord/pivot/angle/flip/tolerance), `solid.cell_grid` (hex/square/triangle/circle/polygon field, ≤250 cells, `clip`/`direction`, keep-out loops, not sheet metal), `view.origin_axes_across_view` | `crates/engine/src/cmd/sketch_import.rs`; `crates/engine/src/cmd/cell_grid.rs`; `docs/features.md` rows; `docs/book/src/guide/files.md` "Airfoil coordinate files"; the ids' `params` text in `solidcraft-cli commands` | implemented |
| 28 | **Format registry, 20 rows** | `crates/io/src/formats.rs` `FORMATS` (20 `id:` entries) | implemented |
| 29 | IGES exports through `file.export` by extension although the command's `format` enum omits it | `crates/io/src/formats.rs` `iges` row `export: Some(ExportSpec { command: "file.export", format: None, … })`; `file.export`'s `params` enum lists `stl|stla|obj|step|3mf|3mf-tagged|glb|urdf|json` | implemented |
| 30 | **Measurements are exact for B-rep bodies** — volume, area, centre of mass and box from SMLib mass properties; mesh bodies from triangles | `crates/kernel/src/measure.rs` (`measure_mass`, `crate::guard("SMLib mass properties", …)`, `measured_by: "smlib"`); `crates/kernel/src/body.rs` `volume_at` doc comment; probe: `eval` on a 40×30×20 box replied `volume_mm3` 24000.0 with `measured_by: "smlib"` | implemented |
| 31 | Format 57 reads every earlier format; a newer file opens with a warning and keeps what it cannot read | `crates/format/src/newer.rs`; `docs/compatibility.md`; `crates/doc/src/format.rs` (`Newer`, `formats`/`take_version` tests) | implemented |
| 32 | Legacy `.solidcraft` / `.solvecraft` and plain `.json` designs still open; new saves are `.sc` | `crates/io/src/lib.rs` `DESIGN_EXT`, `LEGACY_DESIGN_EXTS`, `DESIGN_EXTS`; `docs/compatibility.md` | implemented |
| 33 | **19** in-repo agent skills; **5** embedded (`modeling`, `editing`, `checking`, `mechanisms`, `sheetmetal`) | `skills/*/` (19 folders plus `skills/README.md`); `crates/mcp/src/skill_reference.rs` `Skill` table; live reply lists the five | implemented |
| 34 | Plugins unchanged: WIT `craft:plugin@0.1.0`, capability `commands@0.1`, four `plugin.*` commands, one call one undo step, no WASI/network | `crates/craft-plugin/wit/plugin.wit`; `crates/engine/src/plugin.rs`; `crates/engine/src/cmd/plugin.rs`; `docs/plugins.md`, `docs/plugin-runtime.md`; the plugin crate sources are byte-identical by tree diff | implemented (experimental) |
| 35 | Plugin data in a design: `plugins/<plugin-id>/`, at most 1024 files, kept byte for byte | `crates/doc/src/plugin_data.rs`; `docs/plugins.md` | implemented |
| 36 | Over the running desktop, `plugin.run` is refused inside `engine.batch`/`engine.script` | `crates/ui-egui/src/control.rs` (`ui.plugin_standalone`); `README.md` "Run explicitly" | implemented |
| 37 | `agent_off_thread` is on by default; each waiting command is its own cancellable row | `crates/ui-egui/src/prefs.rs` `agent_off_thread: bool = true` + migration test; `docs/control-protocol.md` `ui.operations` | implemented |
| 38 | **33** crates, including the new dependency-free `display-units` (mm/cm/m/in/ft formatting) | `crates/*/` with a `Cargo.toml`; `crates/display-units/src/lib.rs`; tree-to-tree diff adds only `display-units` | implemented |
| 39 | **140** docs pages (new `docs/kicad-import.md`); the docs page count moved only by that file | `docs/*.md` count; tree-to-tree diff adds `kicad-import.md`, removes none | implemented |
| 40 | Oracle **90/90** (69 analytic, 21 FreeCAD), unchanged; case 95 replay note still present | `docs/oracle.md` summary line and per-case table (`| analytic |` 69, `| freecad` 21); `tests/oracle/` has 90 case folders | implemented (doc-level; not replayed) |
| 41 | macOS bundle signed (Developer ID) and notarized; Windows builds are SignPath-signed while the production certificate is not in place, so SmartScreen may warn | `spctl -a -vv` on the installed bundle: "accepted, source=Notarized Developer ID, origin=Developer ID Application: …"; `README.md` Download | implemented (packaging) |
| 42 | Independent clean-room; no CAD-vendor affiliation; MIT OR Apache-2.0 | `README.md` Disclaimer/Licence; `NOTICE`; `DISCLAIMER.md`; `LICENSE-MIT`, `LICENSE-APACHE` | policy |
| 43 | Drawings still have no app/command path; `.scdwg` is reader/writer groundwork only | `crates/doc/src/drawing.rs`; `crates/io/src/design/drawing.rs`; `ROADMAP.md` (drawings milestone in progress, 3 of 21 pieces, branch unmerged) | not implemented (roadmap) |
| 44 | No CAM; Send to Slicer exports to a slicer only | `ROADMAP.md` "Manufacturing / CAM"; `file.send_to_slicer`/`file.slicers` in the registry; `crates/engine/src/slicers.rs` | not implemented (roadmap) |

## 2. Counts, with the method used

| Surface | v0.42.0 (measured) | v0.41.0 | Method |
|---|---:|---:|---|
| Engine commands | **647** (1 planned: `surface.fillet`) | 642 | `solidcraft-cli commands` parsed as JSON, unique `id`; `planned` field for the one planned id |
| Typed contracts | **612** of 647 (35 with neither) | 572 / 642 (70) | MCP `describe_command {id}` for every id in one headless session; `input` and `output` both non-null |
| MCP tools | **22** | 22 | first string argument of every `tool(...)` in `crates/mcp/src/tools.rs` (`sort -u`); live `tools/list` |
| CLI verbs | **19 listed + 5 unlisted** | 19 + 5 | `Command { …, listed: … }` rows in `apps/solidcraft-cli/src/main.rs`; tree diff empty |
| CLI flags | **+2** (`--require-allow-path`, `--script-relative`) | — | `--[a-z-]+` literals in `apps/solidcraft-cli/src/main.rs`, old tree against new |
| Control methods/commands | **82** | 82 | first-column ids of the method tables in `docs/control-protocol.md` (multi-id rows counted per id; `engine.execute` appears twice, so 82 unique) |
| In-repo agent skills | **19** | 19 | folders under `skills/` |
| Embedded skills | **5** | 5 | `Skill { name: … }` entries in `crates/mcp/src/skill_reference.rs`; live reply |
| Format-registry rows | **20** | 19 | `id:` entries inside `pub static FORMATS` in `crates/io/src/formats.rs` |
| Workspace crates | **33** | 32 | folders under `crates/` with a `Cargo.toml` |
| docs pages | **140** | 139 | `ls docs/*.md` |
| Oracle cases | **90/90** (69 analytic / 21 FreeCAD) | 90/90 | summary line and per-case Source column in `docs/oracle.md`; `tests/oracle/` case folders |
| Control port | **27878**, next free up to 27893 | same | `docs/control-protocol.md` "What listens"; `crates/ui-egui/src/prefs.rs` `agent_control_port: u16 = 27878` |
| Design format | **57** | 55 | probe save → `document.json` `"format": "solidcraft/57"`; `format_pending` names the two pending changes; folded changes under `crates/doc/src/format/v56/` |
| Schema exemption list | **16** ids | 17 | non-comment lines in `crates/engine/src/schema/unconverted.txt` |

Deltas measured by diffing the same surfaces between the v0.42.0 checkout and a v0.41.0 tree fetched
as a tarball (`codeload` at `3c8efdb…`) into a scratch folder — the checkout itself was not touched:
commands 642 -> 647 (+5, none removed: `file.gpg_keys`, `file.verify`, `sketch.insert_airfoil`,
`solid.cell_grid`, `view.origin_axes_across_view`), typed contracts 572 -> 612 (commands with
neither 70 -> 35), design format 55 -> 57, format rows 19 -> 20 (`kicad`), crates 32 -> 33
(`display-units`), docs 139 -> 140 (`kicad-import.md`), `docs/features.md` 636 -> 646 rows
(stale by one now: `sketch.insert_airfoil`), schema exemptions 17 -> 16 (`sheet.export_dxf`
gained its contract). The command delta was derived by extracting dotted id literals from
`crates/engine/src/**/*.rs` in both trees with one regex and intersecting with the registry: that
extraction reproduces exactly 642 ids in the old tree (the v0.41.0 live count) and 647 in the new
one, so the five ids are the whole delta.

Unchanged and re-measured at both tags: MCP tools 22 (identical name set), control methods 82
(identical name set), CLI verbs 19 + 5, embedded skills 5, in-repo skills 19, oracle summary 90/90,
control-channel default (off) and `agent_off_thread` (true), MCP protocol revisions, plugin WIT
contract and plugin crate sources.

## 3. Drift between docs and code (code wins)

| Doc statement | Code / measured truth |
|---|---|
| `docs/features.md` lists every command (generated by `cargo xtask features`) | 646 rows vs 647 ids in `solidcraft-cli commands`; missing `sketch.insert_airfoil`. The page was regenerated during this release (it was six behind at v0.41.0), so the gap is now one row |
| `docs/control-protocol.md` launch table: "Let AI agents connect" on "(the default)" | `crates/ui-egui/src/prefs.rs` `agent_control: bool = false`; test `agent_control_is_off_unless_saved_on` asserts off for a new install **and** for prefs saved before the setting; the same page says "off by default" elsewhere |
| `README.md` and `docs/capabilities.md`: "75 of 76" reference parts | `docs/oracle.md`: 90/90 (69 analytic, 21 FreeCAD) |
| `docs/mcp.md` "Agent skills": lists `solidcraft-reporting` | `crates/mcp/src/skill_reference.rs` embeds modeling, editing, checking, mechanisms, **sheetmetal** |
| `crates/mcp/src/tools.rs` `skill_reference` description lists four skills | the table embeds five (`sheetmetal` missing from the text only) |
| `docs/oracle.md`: 90/90 pass | the same page's validation note says case 95's centre-of-mass reference was corrected after the run and needs a replay |
| `docs/rfcs/0002-plugins.md`: "Only the Preferences page exists today. No plugin runs." | contradicted by `crates/engine/src/cmd/plugin.rs`, `docs/plugins.md`, `docs/plugin-runtime.md` and the shipped runtime; the RFC's status table still says "Draft" |
| `AGENTS.md` / `docs/book` imply every command has input and output schemas | 35 of 647 have neither; the coverage test's `SCHEMA_RULE_STRICT` is `false`, so it warns, and `unconverted.txt` exempts only 16 |
| (previous skill, corrected here) "mass properties come from fine tessellation, not exact integration" | `crates/kernel/src/measure.rs` `measure_mass` uses SMLib mass properties for B-rep bodies and the probe replies `measured_by: "smlib"` |
| (previous skill, corrected here) "21 exempted ids in `unconverted.txt`" | the v0.41.0 file lists 17 ids and the v0.42.0 file 16 |

## 4. Re-measured, carried forward, unverified

**Re-measured at v0.42.0:** command ids (647), typed-contract coverage (612, 35 with neither),
MCP tool names (22) and the `anyOf` schema change, CLI verbs (19 + 5) and the two new flags,
control methods/commands (82), format-registry rows (20), in-repo and embedded skills (19 / 5),
crates (33), docs pages (140), design format (57, by saving a probe design and reading
`document.json`), oracle summary (90/90), the control-channel default (off, port 27878),
`agent_off_thread` (true), and the mass-properties implementation (exact for B-rep bodies).

**Carried forward from earlier audits after re-resolution:** the design-container layout
(`container.json` + `document.json` + `blobs/`), the render-job flow, the MCP file-scope rules, the
control token and limits, the sketch `created:` contract, the plugin surface and the
licensing/clean-room statements. Each was checked against this tree; none contradicted v0.42.0.

- GUI appearance, dialogs and menu labels were not exercised; claims about them come from
  `README.md`, `docs/control-protocol.md`, `docs/agent-chat.md`, `docs/plugins.md`,
  `docs/book/src/guide/files.md` and the registry's toolbar placement.
- **Signing was verified only from the refusing side.** No signed design was produced: `file.save
  {sign: true}` is refused for scripts and agents, and the app's Save was not run. The verification
  statuses (`signed`, `not_covered`, `invalid`, `unsupported`, `truncated`) are read from
  `crates/io/src/design/provenance.rs` and `docs/formats/cose-provenance.md`; only the `unsigned`
  path was exercised live.
- **KiCad import was not exercised**: this tree carries no `.kicad_pcb` fixture. The import
  behaviour is read from `crates/io/src/kicad_in.rs`, `docs/kicad-import.md` and the `doc.open`
  contract in the registry.
- **No part was built beyond a box probe.** Geometric capability lists (fillet/chamfer/boolean
  extents, sheet-metal options, cell-grid behaviour) are the project's own docs, the registry's
  command contracts and `ROADMAP.md`.
- **No plugin package was installed or run**; the plugin section is unchanged from v0.41.0 after
  re-reading `docs/plugins.md`, `docs/plugin-runtime.md`, the engine's plugin modules and the
  byte-identical crate sources.
- The browser build (`apps/solidcraft-web`, `docs/browser-api.md`) was read at doc level: it runs
  the same engine but not plugins, and not KiCad import in this round's docs.

## 5. Read-only verification commands

```sh
# from the pinned v0.42.0 checkout; CLI at the app bundle
git rev-parse HEAD                                                      # 1b1e940cc48e4d1d5d01971a4be20e2e55647066
solidcraft-cli --version                                                # solidcraft-cli 0.42.0
solidcraft-cli commands | jq length                                     # 647
solidcraft-cli commands | jq -r '.[] | select(.planned) | .id'          # surface.fillet
perl -0777 -ne 'while (/\btool\(\s*\n?\s*"([a-z_0-9]+)"/g) { print "$1\n" }' \
  crates/mcp/src/tools.rs | sort -u | wc -l                             # 22
grep -cE 'Command \{ name: ".*listed: true' apps/solidcraft-cli/src/main.rs    # 19
grep -cE 'Command \{ name: ".*listed: false' apps/solidcraft-cli/src/main.rs   # 5
grep -cE '^\s+id: "' crates/io/src/formats.rs                           # 20
ls docs/*.md | wc -l                                                    # 140
ls -d skills/*/ | wc -l                                                 # 19
ls -d tests/oracle/*/ | wc -l                                           # 90
grep -c '| analytic |' docs/oracle.md                                   # 69
grep -c '| freecad' docs/oracle.md                                      # 21
grep -c '    agent_off_thread: bool = true' crates/ui-egui/src/prefs.rs  # 1
grep -c '    agent_control: bool = false' crates/ui-egui/src/prefs.rs    # 1
```

Probes run against the installed CLI (all in a scratch folder, no GUI, nothing written into the
checkout):

```sh
solidcraft-cli run build.json --save box.sc      # then unzip: "format": "solidcraft/57", format_pending: [2 changes]
solidcraft-cli run build.json --out plain.sc     # plain JSON (file.export), also "solidcraft/57"
solidcraft-cli eval box.sc                       # volume_mm3 24000.0, area_mm2 5200.0, measured_by "smlib"
solidcraft-cli exec file.verify '{"path":"box.sc"}'   # status "unsigned", records [], truncated false
solidcraft-cli run sign.json                     # refused: a script or agent cannot sign
```

Headless MCP counts: initialize `solidcraft-cli mcp --headless` (protocol 2025-06-18, server
version 0.42.0), call `tools/list` (22) and `describe_command {"id": <each of 647>}`, counting
replies with non-null `input` and `output` (612 both / 35 neither).

## CLI availability (measured 2026-11-15)

- Release asset: `solidcraft-cli-0.42.0-macos-universal.zip`, 150.9 MB, on
  `https://github.com/tangency-labs/solidcraft/releases/download/v0.42.0/`.
- `SHA256SUMS.txt` (48 lines; every line is the plain two-field `<sha256>  <asset>` form, so
  `grep -F "$ASSET"` matches exactly the CLI-zip line and no alias):
  `c50be9965a9bb4246bbf7cc23471c6eef74fc85a614d5dac546d0a57cd5716a8  solidcraft-cli-0.42.0-macos-universal.zip`
- Bundle `find`: `/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli` exists — the bundle's
  `Contents/MacOS` holds `SolidCraft` and `solidcraft-cli` — and running it prints
  `solidcraft-cli 0.42.0`. A launcher install can therefore use the bundle copy directly.
- Ran: the bundle copy only (`--version`). No download was run for SolidCraft; the round's
  end-to-end proof (download → checksum compare → unzip → `install -m 0755` → `--version`) was run
  once on the smallest CLI asset in this batch, MaterialCraft's 11.9 MB zip, and its real output is
  pasted in that skill's evidence file. The manifest fetch above is the only network step for
  SolidCraft.
