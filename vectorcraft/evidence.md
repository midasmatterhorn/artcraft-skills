# VectorCraft — evidence ledger (tag v0.24.1)

Audit basis: this checkout is tag **`v0.24.1`**, commit **`f4922aa7ac99a4f6d56fc68a83a44945207ec610`**
("Merge tested main for v0.24.1", 2026-11-11); a shallow clone pinned at the release tag, with the
`v0.22.0` ref present for set diffs. Inspection date **2026-11-12**. The installed VectorCraft.app
bundle matches the tag (`CFBundleIdentifier ai.storyteller.vectorcraft`, short version 0.24.1);
its binary prints `vectorcraft 0.24.1`; the GUI was never launched. Previous release described by
the skill: v0.22.0 (`654749c16eb20b6d3182a96defb66e11d1a9649a`).

v0.22.0 -> v0.24.1 delta: **1,304 files changed, +242,142 / -11,521** (local
`git diff --shortstat`); **+47 engine command ids, zero removed** (908 -> 955), **UI commands
427 -> 453**, **prompts 5 -> 8**, **MCP fixed resources 3 -> 4**, **browser API 9 -> 11**,
**open/place extensions 43/47 -> 46/50**, effect catalogue **116 -> 118**, panels **44 -> 47**.
New capability families: JavaScript scripting (`crates/js`, `crates/engine/src/script/`), SVG
Filters, spell check, composite fonts and Dynamic Text, HEIC/HEIF and JPEG XL import, PSD/PSB
layers, 3D mesh export and importer plug-ins.

## 1. Capability claims -> evidence -> tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 955 engine command ids (908 at v0.22.0; +47, none removed) | `crates/engine/src/cmd.rs` `cmd!` macro; every `cmd!(…)` / `query cmd!(…)` literal under `crates/engine/src/` parsed and set-diffed vs `v0.22.0` | implemented |
| 2 | 453 UI commands, unique ids | `crates/ui-egui/src/menus/ui_commands.rs` `UI_COMMANDS`: 453 four-tuples (427 at v0.22.0) | implemented |
| 3 | 33 MCP tools | `crates/mcp/src/tools/definitions.rs`: 31 multi-line `tool(` blocks + `tool("undo"…)` / `tool("redo"…)` = 33 | implemented |
| 4 | 8 MCP prompts | `crates/mcp/src/prompts.rs` `PROMPTS`: poster, icon-set, recolor, trace-and-style, export-set, check-spelling, variables-bind, path-tools (5 at v0.22.0) | implemented |
| 5 | 4 fixed resources + 4 URI templates | `crates/mcp/src/resources.rs` `list()` = document, document/json, commands, command-reference; `TEMPLATES` = object, command, effect, swatch (3 + 4 at v0.22.0) | implemented |
| 6 | 29 canonical control methods (30 accepted strings) | `crates/ui-egui/src/control.rs` match arms: 29 dotted names + the `command` alias | implemented |
| 7 | 7 CLI subcommands | `apps/vectorcraft-cli/src/main.rs` `USAGE`: mcp, run, commands, convert, info, bench, perf | implemented |
| 8 | 11 browser calls on `window.vectorcraft` | `apps/vectorcraft-web/src/api.rs` sets inspect, openFile, captureDownloads, files, readFile; the shared `PageApi` (`craft-web-api` dependency) installs request, execute, commands, docInspect, uiInspect, screenshot | implemented |
| 9 | `OPEN_EXTS` 46, `PLACE_EXTS` 50 | `crates/engine/src/cmd/fileio/formats.rs:514` (46 quoted entries) and `:603` (50; adds txt, rtf, docx, doc). New here: heic, heif, jxl | implemented |
| 10 | `FORMATS` 29 entries: 27 readable, 20 writable + plug-in formats | `crates/engine/src/cmd/fileio/formats.rs:352`: 21 `Format { … }` blocks + 8 one-line `reader(…)` entries; 19 `read: true` blocks + 8 readers = 27; 20 `write: true` | implemented |
| 11 | `SAVE_FORMATS` = vectorcraft, template, pdf, svg, svgz, ai, eps (7) | `crates/engine/src/cmd/fileio/save.rs:24` | implemented |
| 12 | 57 Photoshop-style filters = 56 `PIXEL_EFFECTS` + `blur.gaussian` | `crates/effects/src/pixel.rs:47` `PIXEL_EFFECTS: [&str; 56]` | implemented |
| 13 | Effect catalogue 118 = 91 direct + 15 warps + 12 Pathfinder | `crates/effects/src/catalog.rs` `effect_catalog()` (82 quoted ids + 9 constants: REVOLVE, EXTRUDE, INFLATE, ROTATE, CLASSIC_EXTRUDE, TRAP, CROP_MARKS, RASTERIZE, SVG_FILTER), `WARP_STYLES: […; 15]`; `crates/effects/src/group.rs:30` `PATHFINDER_EFFECTS: […; 12]` | implemented |
| 14 | 94 tool ids | `crates/tools/src/catalog.rs` 94 `t("` occurrences (unchanged at v0.24.1) | implemented |
| 15 | 47 `ICON_PANELS` entries | `crates/ui-egui/src/state.rs:169`; Color Wheel, 3D and Materials and Script Console are new | implemented |
| 16 | 28 interface languages = 27 `.tsv` + English | `ls crates/ui-egui/src/i18n/*.tsv` = 27; no new catalogue this round (Georgian was updated) | implemented |
| 17 | Native file `VERSION = 4`, document model `FORMAT_VERSION = 3` | `crates/format/src/lib.rs` re-exports `VERSION` from the pinned `craft-vectorcraft-format` (rev `6e03f65bf`); `crates/doc/src/limits.rs:20` | implemented |
| 18 | JavaScript scripts run (ES5.1 + E4X) | `crates/js/src/lib.rs`; `crates/engine/src/cmd/scripts.rs` `script.run`/`stop`/`engines`/`engine.drop`/`console`/`listInstalled`; `crates/engine/src/script/{mod,console,dollar,dialogs,files,folder,include}.rs`; CLI proof `apps/vectorcraft-cli/tests/it/script.rs` | implemented |
| 19 | A run is one transaction with fuel/heap/slice limits | `crates/engine/src/script/mod.rs` (`DEFAULT_FUEL`, `MAX_FUEL`, `HEAP_BYTES`, `MAX_ENGINES`, `ENGINE_HEAP_BYTES`); rollback and one "Run Script" undo step documented in the `script.run` param doc | implemented |
| 20 | Script Console panel, File › Scripts, Other Script… | `crates/ui-egui/src/panels/script_console.rs`; `crates/ui-egui/src/menus/tree.rs`; `crates/ui-egui/src/menus/ui_commands.rs` `ui.runScript`, `ui.checkScript` | implemented |
| 21 | Reference-app scripts are still only statically checked | `crates/engine/src/cmd/scripts.rs` `EXTS = jsx, jsxinc, jsxbin`; `crates/scriptcheck/src/`; `docs/gaps.md` G6 (no document object model, `#engine` refused) | partial (static only) |
| 22 | SVG Filters are implemented (the last vector-effect stub) | `crates/engine/src/cmd/svgfilter.rs` (`apply`/`define`/`delete`/`import`/`list`), `crates/effects/src/svg_filter.rs`, catalogue entry `SVG_FILTER`; `docs/effects-parity.md` 1/1 | implemented |
| 23 | Spell check, Auto Spell Check, custom dictionary | `crates/engine/src/cmd/spelling.rs` (`check`, `suggest`, `addWord`, `removeWord`, `changeWord`, `dictionary`, `ignoreAll`, `editDictionary`); `crates/ui-egui/src/dialogs/custom_dictionary.rs`; `docs/type-parity.md`; Check Spelling dialog still a `todos` stub in `crates/ui-egui/src/menus/tree.rs` | partial |
| 24 | Composite fonts and Dynamic Text | `crates/engine/src/cmd/compositefonts.rs`, `crates/doc/src/text/composite.rs`, `.vccomposite` import/export; `type.dynamicText` in `crates/engine/src/cmd/typemenu.rs`, `crates/engine/src/cmd/typecmd/block.rs`, `crates/engine/src/tests/dynamic_text.rs` | partial (composite fonts) / implemented (dynamic text) |
| 25 | PSD/PSB open with layers; place stays merged | `crates/engine/src/cmd/fileio/psdlayers.rs`; `crates/engine/src/cmd/fileio/load.rs`; `layers: true` default and `layers: false` merged in `document.open` (`crates/engine/src/cmd/fileio/commands.rs`); README states place is merged | implemented |
| 26 | HEIC/HEIF and JPEG XL are read | `crates/engine/src/cmd/fileio/heifread.rs`, `jxlread.rs`, `formats.rs` (`.heic`, `.heif`, `.jxl`); `docs/file-format-parity.md` detail rows | implemented |
| 27 | 3D assets export as OBJ+MTL, glTF 2.0, USDA, USDZ | `crates/engine/src/cmd/fileio/mesh3d.rs` (`FORMATS_3D = usda, usdz, gltf, obj`); `crates/engine/src/cmd/assets.rs` (`assets.add3D`, `export3D`, `set3DFormat`); `crates/effects/src/solids/` | implemented (export only) |
| 28 | Importer plug-ins add read-only `plugin.<id>` formats | `crates/engine/src/cmd/fileio/importer.rs`; `document.open {importer, params}` and `file.openWith` in `crates/engine/src/cmd/fileio/commands.rs`; `docs/plugins.md` | implemented |
| 29 | Plug-in API level 2: host imports, permissions/grants, commands, settings/cache, safe mode | `crates/plugins/src/{manifest,runtime,wat,host}.rs`; `crates/plugins/src/permissions.rs`; `crates/engine/src/cmd/plugin.rs` (`plugin.safeMode`, `setEnabled`, `clearCache`); `docs/plugins.md` | implemented |
| 30 | MCP lists desktop UI commands and a command reference | `crates/mcp/src/ui_catalog.rs` (UI commands with `ui: true`), `crates/mcp/src/headless.rs`; `crates/mcp/src/resources.rs` `REFERENCE_URI`; `crates/engine/src/cmd/apiref.rs`, `crates/apischema/` | implemented |
| 31 | Ruler guides are document objects on layers; conic gradients | `crates/doc/src/guides.rs`, `crates/doc/src/document_guides.rs` (`NodeKind::RulerGuide`); `crates/engine/src/cmd/docmenu.rs` (`guide.add`, `view.guides.*`); `crates/engine/src/cmd/{gradient,paint}.rs` conic kind | implemented |
| 32 | Compare a render with an image (RMSE + diff PNG) | `crates/engine/src/cmd/edit.rs` `document.compare` | implemented |
| 33 | PDF long pages in points; CLI safe mode/grants/editing flags | `crates/engine/src/cmd/fileio/pdf.rs` `longPagesInPoints`; `apps/vectorcraft-cli/src/main.rs` `--safe-mode`, `--allow-plugin-grants`, `--preserve-editing`, `--legacy-name-encoding`, `perf --native-io` | implemented |
| 34 | Action-set `.aia` reading, preferences export/import, pixel-grid commands | `crates/engine/src/cmd/actionset.rs`; `crates/engine/src/cmd/prefscmds.rs`; `crates/engine/src/cmd/object/pixelgrid.rs` | implemented |
| 35 | No generative AI features | `docs/gaps.md` G18; no such command or crate found | not implemented (verified absent) |
| 36 | Control port is unauthenticated and loopback-only; MCP is stdio-only | `crates/ui-egui/src/control.rs`; `docs/control-protocol.md:26`; `docs/mcp.md` › Not implemented | implemented (limits) |
| 37 | No reference-app document object model; `#engine` refused | `docs/gaps.md` G6; `script.run` param doc (`#engine` refused as unsupported; `#targetengine` supported) | not implemented |

## 2. Automation-surface counts: v0.22.0 -> v0.24.1

| Surface | v0.22.0 | v0.24.1 (measured) | Change |
|---|---:|---:|---|
| Engine command ids | 908 | **955** | +47 |
| UI commands | 427 | **453** | +26 |
| MCP tools | 33 | **33** | unchanged at v0.24.1 |
| MCP prompts | 5 | **8** | +3 |
| MCP resources | 3 fixed + 4 templates | **4 + 4** | +1 fixed |
| Control methods | 29 canonical / 30 accepted | **29 / 30** | unchanged at v0.24.1 |
| CLI subcommands | 7 | **7** | unchanged at v0.24.1 (new flags) |
| Browser API | 9 | **11** | +2 |
| Open / place extensions | 43 / 47 | **46 / 50** | +3 / +3 |
| Save formats | 7 | **7** | unchanged at v0.24.1 |
| Format catalogue | 27 (25 read, 20 write)* | **29 (27 read, 20 write)** | +2 readers |
| Photoshop-style filters | 57 | **57** | unchanged at v0.24.1 |
| Effect catalogue | 116 | **118** | +2 |
| Tools | 94 | **94** | unchanged at v0.24.1 |
| Panels (`ICON_PANELS`) | 44 | **47** | +3 |
| Languages (tsv + English) | 27 + 1 = 28 | **27 + 1 = 28** | unchanged at v0.24.1 |
| Native file version | 4 | **4** | unchanged at v0.24.1 |

\* v0.22.0 measured with the same "21 blocks + 6 readers" method. The previous skill quoted 21 by
counting blocks only; that figure is corrected here.

## 3. Re-measured vs carried forward

- **Re-measured at this tag:** every row in section 2; the new script, SVG-filter, spelling,
  composite-font, PSD-layer, HEIC/JXL, 3D-export, importer-plug-in and MCP-resource claims; all
  repo-relative paths cited in `SKILL.md` were re-resolved.
- **Carried forward after a path check (not re-derived):** the older drawing/paint/type/effects prose
  inherited from v0.22.0 (Pathfinder, appearance, brushes, symbols, blends, perspective, graph types,
  Affinity import, PDF/`.ai` internals, platform notes). Their evidence paths still exist; behaviour
  was not exercised in a build.
- **Not measured:** parity percentages, localization scores, hour estimates, real-world `.ai`
  fidelity, GUI behaviour and performance numbers. Those remain project self-assessments.

## 4. Uncertain / not verified

- The 47 added command ids were enumerated individually, but the +26 UI ids were only counted, not
  listed; the live catalogue (`vectorcraft-cli commands`, MCP `list_commands`, control
  `engine.commands`) is authoritative for a given build.
- `script.run`'s transaction/limits are documented from code and the CLI integration test; no script
  was executed in this audit (no build was run).
- The shared `PageApi` lives in the `craft-libs` checkout, not this repo; the 11-call count is from
  `apps/vectorcraft-web/src/api.rs` plus the `craft-web-api` dependency's source. `craft-libs`
  HEAD differs from the pinned rev; the method names were read from the checkout.
- The pinned `craft-vectorcraft-format` rev is not checked out at HEAD in the local `craft-libs`
  (`VERSION` read there is 4; this repo's own save param doc also says `version?: 4`).

## 5. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `docs/mcp.md` initialize table: "Three fixed resources and four templates", "Five ready-made workflows" | `crates/mcp/src/resources.rs` `list()` = 4 fixed resources; `crates/mcp/src/prompts.rs` = 8 prompts |
| `docs/file-format-parity.md` summary row: HEIC/HEIF and PS missing; second summary row says 29 opened | `.heic/.heif`, `.jxl` and `.ps` are in `OPEN_EXTS` (46); the detail rows already say HEIC/JXL are read |
| `docs/effects-parity.md` header: "Illustrator effects 49/50" | its own table and `crates/effects/src/catalog.rs` now count 50/50 (SVG Filters implemented) |
| `README.md` "What's missing": scripting | `script.run` and the ES5.1 engine ship; only the reference-app DOM is missing (`docs/gaps.md` G6) |
| `ROADMAP.md`: 348/375 menu items, 89/92 tools, 46/50 effects | `docs/target-app-parity.md` prints 353/375; the code has 94 tools and a 118-entry effect catalogue |
| `docs/target-app-parity.md`: tools 89/92 | `crates/tools/src/catalog.rs` defines 94 ids |
| `docs/file-format-parity.md` summary: "Formats opened or placed 29/30" | `OPEN_EXTS` 46, `PLACE_EXTS` 50 (including Place-only text formats) |

## 6. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # f4922aa7ac99a4f6d56fc68a83a44945207ec610
git -C <clone> diff --shortstat v0.22.0..HEAD                  # 1304 files, +242142/-11521
# command ids: every cmd! literal, both `cmd!` and `query cmd!` forms
python3 -c 'import re,pathlib;print(len({m for p in pathlib.Path("crates/engine/src").rglob("*.rs") for m in re.findall(r"cmd!\(\s*(?:query\s+)?\"([a-z0-9][a-zA-Z0-9.]*)\"",p.read_text(errors="ignore"))}))'   # 955
python3 - <<'EOF'   # UI_COMMANDS four-tuples
import re;t=open("crates/ui-egui/src/menus/ui_commands.rs").read();i=t.index("pub const UI_COMMANDS");b=t[i:t.index("\n];",i)];print(len(re.findall(r"(?m)^    \(",b)))   # 453
EOF
grep -cE '^\s+tool\($' crates/mcp/src/tools/definitions.rs          # 31 (+2 single-line = 33)
grep -cE '^\s{4}PromptDef \{' crates/mcp/src/prompts.rs             # 8
grep -cE '^\s{4}Template \{' crates/mcp/src/resources.rs             # 4
awk '/pub const OPEN_EXTS/,/^\];/' crates/engine/src/cmd/fileio/formats.rs | grep -c '^\s*"'   # 46
awk '/pub const PLACE_EXTS/,/^\];/' crates/engine/src/cmd/fileio/formats.rs | grep -c '^\s*"'  # 50
awk '/pub const FORMATS/,/^\];/' crates/engine/src/cmd/fileio/formats.rs | grep -cE '^\s+Format \{'   # 21 blocks
awk '/pub const FORMATS/,/^\];/' crates/engine/src/cmd/fileio/formats.rs | grep -cE '^\s+reader\('   # 8 readers -> 29
grep 'pub const SAVE_FORMATS' crates/engine/src/cmd/fileio/save.rs     # 7 ids incl. eps
grep -n 'PIXEL_EFFECTS: \[' crates/effects/src/pixel.rs               # [&str; 56]
grep -n 'WARP_STYLES: \[' crates/effects/src/catalog.rs               # [(&str, &str); 15]
grep -n 'PATHFINDER_EFFECTS: ' crates/effects/src/group.rs             # 12
grep -oE 't\("' crates/tools/src/catalog.rs | wc -l                   # 94
awk '/pub const ICON_PANELS/,/^\];/' crates/ui-egui/src/state.rs | grep -cE '^\s+\('   # 47
ls crates/ui-egui/src/i18n/*.tsv | wc -l                              # 27 (+English = 28)
grep -n 'FORMAT_VERSION' crates/doc/src/limits.rs                     # 3
```
