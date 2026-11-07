# VectorCraft — evidence ledger (tag v0.22.0)

Audit basis: this checkout is tag **`v0.22.0`**, commit **`654749c16eb20b6d3182a96defb66e11d1a9649a`**
("Release 0.22.0", 2026-11-06); a shallow clone at the tag, with the `v0.21.0` ref present for set diffs.
Inspection date **2026-11-07**. The installed VectorCraft.app bundle matches the tag
(`CFBundleIdentifier ai.storyteller.vectorcraft`), binary prints `vectorcraft 0.22.0`; the GUI was never launched.

v0.21.0 → v0.22.0 delta: **858 files changed, +97,302 / −5,778**; **+22 engine command ids, zero removed**
(886 → 908): `addon.shapes.*` (box3d, configure, ellipse, polygon, rectangle, spiral, star),
`addon.contour.set`, `addon.color.fillToStroke`/`strokeToFill`, `addon.document.batchTraceFolder`,
`addon.select.byArtboards`/`byLinkStatus`, `addon.type.releasePath`/`textTweaker`, `document.move`,
`select.globalEditExclude`, `select.same.textFillAndStrokeColor`, `stroke.weightUp`/`weightDown`,
`text.glyphAlternates`/`setGlyphAlternate`; **UI commands 410 → 427**; **languages 26 → 27** `.tsv`
(+`hi.tsv`); native save gained `precision: 0..9`, the CLI gained `--ppi`, and raster export defaults to
the document's raster-effects resolution. Previous v0.20.0 → v0.21.0 delta: 461 files changed, +2 ids
(`addon.color.swatchLegend`, `select.same.linkBlockSeries`), Variables panel, Recolor sliders, `.ai` v7
palettes, native envelope, Affinity stroke width profiles, PDF spot gradients.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 908 engine command ids (886 at v0.21.0; +22, none removed) | `crates/engine/src/cmd.rs` `cmd!` macro; every `cmd!(… "id" …)` and `query cmd!` literal under `crates/engine/src/` parsed with `cmd!\(\s*(?:query\s+)?"([a-z0-9][a-zA-Z0-9.]*)"` and set-diffed vs `v0.21.0` | implemented |
| 2 | 427 UI commands, unique ids | `crates/ui-egui/src/menus/ui_commands.rs` `UI_COMMANDS`; 427 `(`-led tuple entries (410 at v0.21.0) | implemented |
| 3 | 33 MCP tools | `crates/mcp/src/tools/definitions.rs`: 31 `tool(` block definitions + `tool("undo"…)`/`tool("redo"…)` single-line = 33 | implemented |
| 4 | 5 prompts; 3 fixed resources + 4 URI templates | `crates/mcp/src/prompts.rs` `PROMPTS` (5 `PromptDef`); `crates/mcp/src/resources.rs` `list()` (3) and `TEMPLATES` (4: object, command, effect, swatch) | implemented |
| 5 | 29 canonical control methods (30 accepted strings with the `command` alias) | `crates/ui-egui/src/control.rs` match arms: `"engine.execute" \| "ui.menu.invoke" \| "command"` shared alias; 29 dotted names | implemented |
| 6 | 9 browser API calls | `apps/vectorcraft-web/src/api.rs` `install`: request, execute, commands, inspect, screenshot, openFile, captureDownloads, files, readFile | implemented |
| 7 | 7 CLI subcommands; `run`/`convert` take `--ppi` | `apps/vectorcraft-cli/src/main.rs` `USAGE`: mcp, run, commands, convert, info, bench, perf; `--ppi` parsed in both batch paths | implemented |
| 8 | `OPEN_EXTS` 43, `PLACE_EXTS` 47 | `crates/engine/src/cmd/fileio/formats.rs:509` (43 quoted entries), `:592` (47; adds txt, rtf, docx, doc) | implemented |
| 9 | `SAVE_FORMATS` = vectorcraft, template, pdf, svg, svgz, ai, eps (7) | `crates/engine/src/cmd/fileio/save.rs:24` | implemented |
| 10 | 21 catalogue formats: 19 readable, 20 writable + `plugin.<id>` | `crates/engine/src/cmd/fileio/formats.rs:352` `FORMATS` (21 `Format {` entries; `ait` not writable, `png8`/`txt` not readable) | implemented |
| 11 | 57 Photoshop-style filters = 56 `PIXEL_EFFECTS` + `blur.gaussian` | `crates/effects/src/pixel.rs:47` `PIXEL_EFFECTS: [&str; 56]` | implemented |
| 12 | Effect catalogue 116 = 86 literal + 15 warps + 12 Pathfinder + Trap + Crop Marks + Rasterize | `crates/effects/src/catalog.rs` `effect_catalog()` 86 `g(`/`r(` entries, `WARP_STYLES` 15; `crates/effects/src/group.rs:30` `PATHFINDER_EFFECTS: 12` | implemented |
| 13 | 94 tool ids | `crates/tools/src/catalog.rs` 94 `t("` occurrences | implemented |
| 14 | 44 `ICON_PANELS` entries on craft-ui docking | `crates/ui-egui/src/state.rs:168`; `crates/ui-egui/src/panel_docking.rs` | implemented |
| 15 | 28 interface languages = 27 `.tsv` + English; Hindi new and machine-assisted | `ls crates/ui-egui/src/i18n/` = 27 `.tsv`; `hi.tsv` added in the diff; `docs/localization-parity.md` calls it a 7,877-row machine-assisted draft | implemented |
| 16 | Native file `VERSION = 4`, document model `FORMAT_VERSION = 3` | `crates/format/src/lib.rs` re-exports `VERSION` from craft-vectorcraft-format; `crates/engine/src/cmd/fileio/save.rs` param doc "version?: 4 (3, 2 or 1…)"; `crates/doc/src/limits.rs:20` `FORMAT_VERSION: u32 = 3` | implemented |
| 17 | `document.save {precision: 0..9}` rounds path geometry only | `crates/format/src/lib.rs` `SaveOptions.precision` (`:151`) and `body()` calling `round_geometry` (`:245`); `crates/engine/src/cmd/fileio/save.rs` param doc; `docs/mcp.md` › Native files (anchors/handles in layers, symbols, graph designs, patterns, masks and brushes; colours, transforms and type exact) | implemented |
| 18 | Raster export defaults to the document's raster-effects resolution | `crates/engine/src/cmd/fileio/encode.rs` ("`ppi`, else 72 × `scale`, else the document's resolution"); `commands.rs` export params | implemented |
| 19 | Ghostscript `eps2write` EPS files open | `crates/eps/src/import/tests_generators.rs:582` `GPL Ghostscript 10.04.0 (eps2write)` round-trip; import parser under `crates/eps/src/import/` | implemented |
| 20 | `.ai` import: linked images with placeholder, threaded area type, 1-bit masks colorized, clipping intersections | `crates/eps/src/import/ai/read/art.rs` (`missing_placeholder`, `colorized_raster`, 1-bit ImageMask), `crates/egui/src/import/ai/legacy_text.rs` (threads), `crates/eps/src/import/ai/read/document.rs` | implemented |
| 21 | Documents float/cascade/dock; symbol 9-slice guides on canvas; Recolor Edit-tab wheels; Objects on Path Space; Document Info dedupe; Import Data Sets all columns | `crates/ui-egui/src/doc_windows.rs`; `crates/ui-egui/src/canvas/tool_overlays.rs:172`; `crates/ui-egui/src/dialogs/recolor.rs:14-22`; `crates/engine/src/cmd/objects_on_path.rs:10`; `crates/engine/src/cmd/docinfo.rs` (`HashSet<*const Node>` dedupe); `crates/engine/src/cmd/variablecmds/csv.rs` | implemented |
| 22 | No reference-app scripting; `.jsx` static check only; no generative AI | `crates/scriptcheck/`; `README.md` "What's missing"; `docs/gaps.md` G18 | not implemented (verified absent) |
| 23 | Control port unauthenticated, loopback only; MCP stdio only | `crates/ui-egui/src/control.rs`; `docs/control-protocol.md`; `docs/mcp.md` › Not implemented | implemented (limits) |

## 2. Automation-surface counts: v0.21.0 → v0.22.0

| Surface | v0.21.0 | v0.22.0 (measured) | Change |
|---|---:|---:|---|
| Engine command ids | 886 | **908** | +22 |
| UI commands | 410 | **427** | +17 |
| MCP tools | 33 | **33** | unchanged |
| MCP prompts | 5 | **5** | unchanged |
| MCP resources | 3 fixed + 4 templates | **3 + 4** | unchanged |
| Control methods | 29 canonical / 30 accepted | **29 / 30** | unchanged |
| CLI subcommands | 7 | **7** | unchanged |
| Browser API | 9 | **9** | unchanged |
| Open / place extensions | 43 / 47 | **43 / 47** | unchanged |
| Save formats | 7 | **7** | unchanged |
| Format catalogue | 21 (19 read, 20 write) | **21 (19/20)** | unchanged |
| Photoshop-style filters | 57 | **57** | unchanged |
| Effect catalogue | 116 | **116** | unchanged |
| Tools | 94 | **94** | unchanged |
| Panels (`ICON_PANELS`) | 44 | **44** | unchanged |
| Languages (tsv + English) | 26 + 1 = 27 | **27 + 1 = 28** | +Hindi |
| Native file version | 4 | **4** | unchanged |

## 3. Uncertain / not verified

- The +17 UI-command ids were not enumerated individually (net count measured); the live registry
  (`vectorcraft-cli commands`) is the authority.
- GUI behaviour was not launched; registry, source and packaging are the evidence.
- Parity percentages, "ready for real work" percentages and localization scores remain project
  self-assessments; only the counts above were re-measured.
- The pinned `craft-libs` revision is not in the local craft-libs checkout, so the native `VERSION`
  was confirmed from this repo's own `document.save` param doc and the `crates/format` re-export.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `docs/file-format-parity.md`: ~30 formats opened/placed (29) | `OPEN_EXTS` 43, `PLACE_EXTS` 47 |
| `docs/file-format-parity.md`: "PS missing" | `.ps` in `OPEN_EXTS` |
| `docs/target-app-parity.md`: tools 89/92 | `crates/tools/src/catalog.rs` defines 94 ids |
| `ROADMAP.md`: 348/375 menus, 46/50 effects, 74% localization | `docs/target-app-parity.md` 353/375 and a 49/50 measured vector-effect row; `docs/localization-parity.md` ~82% |
| `README.md` "What's missing" lists "the rest of Variables" and 3D beyond Revolve | `dataset.import`, all four `VariableKind`s and Extrude & Bevel/Inflate/Rotate ship (materials do not) |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # 654749c16eb20b6d3182a96defb66e11d1a9649a
git -C <clone> diff --stat v0.21.0..HEAD                        # 858 files, +97,302/-5,778
# command ids: every cmd! literal, both `cmd!` and `query cmd!` forms (multiline), e.g.
python3 -c 'import re,pathlib;print(len({m for p in pathlib.Path("crates/engine/src").rglob("*.rs") for m in re.findall(r"cmd!\(\s*(?:query\s+)?\"([a-z0-9][a-zA-Z0-9.]*)\"",p.read_text(errors="ignore"))}))'   # 908
awk '/pub (static|const) UI_COMMANDS/,/^\];/' crates/ui-egui/src/menus/ui_commands.rs | grep -cE '^\s+(UiCommand|\()'   # 427
grep -cE '^\s+tool\($' crates/mcp/src/tools/definitions.rs          # 31 block defs
grep -c 'tool("' crates/mcp/src/tools/definitions.rs                 # 2 single-line → 33
awk '/pub static PROMPTS/,/^\];/' crates/mcp/src/prompts.rs | grep -c 'PromptDef {'   # 5
grep -oE '^\s+"[a-z]+\.[a-zA-Z.]+".*=>' crates/ui-egui/src/control.rs | grep -oE '"[^"]+"' | sort -u | wc -l  # 30 (29 + `command` alias)
grep -oE 't\("' crates/tools/src/catalog.rs | wc -l             # 94
awk '/pub const OPEN_EXTS/,/^\];/' crates/engine/src/cmd/fileio/formats.rs | grep -c '^\s*"'   # 43
awk '/pub const PLACE_EXTS/,/^\];/' crates/engine/src/cmd/fileio/formats.rs | grep -c '^\s*"'  # 47
grep 'pub const SAVE_FORMATS' crates/engine/src/cmd/fileio/save.rs     # 7 ids incl. eps
awk '/pub fn effect_catalog/,0' crates/effects/src/catalog.rs | grep -cE '^\s+(g|r)\('      # 86 (+15 warps +12 pathfinder +3)
grep -c 'pub const PIXEL_EFFECTS' crates/effects/src/pixel.rs >/dev/null; grep 'PIXEL_EFFECTS: \[' crates/effects/src/pixel.rs  # [&str; 56]
ls crates/ui-egui/src/i18n/ | grep -c tsv                       # 27 (+English)
```
