# PdfCraft — evidence ledger (tag v0.21.1)

Audit basis: this checkout is tag **`v0.21.1`**, commit **`b503b2e62dfeec5598f344e4e287d9c9cbdb34fa`** ("Merge tested main for v0.21.1", 2026-11-11); inspection **2026-11-12**. `git rev-parse HEAD` in the pinned checkout matches. The installed bundle prints `pdfcraft 0.21.1`; the GUI was never launched.

v0.19.0 → v0.21.1 delta (measured, not quoted from notes): **872 files** changed (`git diff --shortstat v0.19.0..HEAD`, +165 335 / −11 319). The round's compare API reports 1 957 commits and caps its file list at 300; the clone's tag diff is the file count used here. Automation **+13 tools, none removed**; **+7 registry command ids, none removed**; control methods 17 = 17; `apps/pdfcraft-cli/src/main.rs` zero diff. New surfaces: prepress (hairlines, colour conversion, printer marks, driver papers), find/replace inside paragraphs, grouped-text preparation, cross-document object copy/paste, Office import through LibreOffice, split view, initial-view chrome hiding, portfolio presentation, full-screen transitions, custom-stamp line, comment pop-ups, field focus/pointer scripts, redaction regex, optimizer discards, XFA milestone 12, accessibility layout-table conversion, and a web `window.pdfcraft` API.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 208 automation tools (+13 at v0.21.1, none removed) | `crates/automation/src/tools.rs` — 208 top-level `t(` declarations (195 at v0.19.0); additions `accessibility_layout_table_to_blocks`, `attachment_edit`, `comment_popup`, `doc_convert_colours`, `doc_fix_hairlines`, `doc_printer_marks`, `form_focus`, `js_event`, `object_copy`, `object_paste`, `printer_papers`, `text_prepare`, `text_replace` | implemented |
| 2 | 221 registry command ids (+7) | `crates/engine/src/commands.rs:167` `COMMANDS` — 221 `c("id")` (214 at v0.19.0); additions `edit.replace`, `prepress.convert_colors`, `prepress.hairlines`, `prepress.marks`, `prepress.marks.remove`, `view.split`, `view.toggle_interface` | implemented |
| 3 | 17 UI control methods, including `ui.panel` (not `ui.dock`) | `crates/ui-egui/src/control/requests.rs` — identical set at both tags: state/commands/command/set/open/inspect/click/focus/resize/quit/drag/move/type/key/screenshot/panel/dock.reset | implemented; previous skill's `ui.dock` was wrong |
| 4 | CLI 14 documented subcommands + internal `check-one`; 34 `--flag` names | `apps/pdfcraft-cli/src/main.rs` match arms; `--flag` strings across `apps/pdfcraft-cli/src/*.rs`; zero diff between tags | implemented |
| 5 | 58 launch view/preference keys | top-level match arms of `PdfCraftApp::set_option`, `crates/ui-egui/src/app/control.rs` | implemented; previous skill said 46 |
| 6 | 104 tools carry a command id, covering 77 distinct ids (75 registry ids) | `.cmd("…")` in `crates/automation/src/tools.rs`; intersection with `COMMANDS`; `edit.undo`/`edit.redo` are not registry entries. 99 / 73 at v0.19.0 | implemented |
| 7 | 146 of 221 commands have no headless tool | `COMMANDS` minus the 75 mapped ids | measured |
| 8 | Catalogue: 152 entries in 23 groups, 29 sections; 21 planned entries (24 at v0.19.0), 5 planned groups | `crates/engine/src/catalog.rs:75` `TOOL_GROUPS` — 149 `item(` + 3 `menu_item(`; 23 `ToolGroup {`; 29 `ToolSection {`; the three prepress entries moved from Planned to Ready | implemented; previous skill's 150/24/30 was off by one on each |
| 9 | 13 convertible input extensions, unchanged | `CONVERTIBLE`, `crates/create/src/lib.rs:779` — images plus `txt`/`text` | implemented |
| 10 | 28 Office import extensions through LibreOffice | `OFFICE_EXTENSIONS`, `crates/create/src/office.rs` — doc/docx/docm/dot/dotx/dotm/odt/ott/rtf, xls/xlsx/xlsm/xlt/xltx/xltm/ods/ots, ppt/pptx/pptm/pot/potx/potm/pps/ppsx/ppsm/odp/otp | implemented (desktop only) |
| 11 | Office import paths differ | File ▸ Open converts in a background worker (`crates/ui-egui/src/platform/open_worker.rs:224`); `doc_combine`/`doc_create_multiple` convert (`crates/automation/src/assemble.rs`, `crates/engine/src/session/files.rs`); `doc_open` opens PDF only (`crates/automation/src/documents.rs:106`); GUI Combine/Insert/Create Multiple refuse on the frame thread (`crates/ui-egui/src/workflows/combine_ui/parts.rs:42`, `crates/ui-egui/src/workflows/create_multiple_ui.rs:46`, `crates/ui-egui/src/workflows/files.rs:669`) | implemented / **partial by path** |
| 12 | `doc_create` text uses Inter for Latin/Greek/Cyrillic outside WinAnsi | `crates/automation/src/tools.rs` `doc_create`; `crates/create/src/text_font.rs`; other scripts refused | implemented; previous "WinAnsi only" was too strict |
| 13 | 23 print paper presets (was 21) | `PAPERS`, `crates/print/src/settings.rs:233`; driver names via `printer_papers` (`crates/automation/src/tools.rs`) | implemented |
| 14 | 20 `comment_add` types (previous prose said 19) | `crates/automation/src/tools.rs` `comment_add` `type` enum | implemented |
| 15 | 6 redaction patterns plus a custom regex with checksum validators | `PATTERNS`, `crates/redact/src/patterns.rs:17`; `regex`/`validate` in `redact_mark`, `crates/automation/src/tools.rs`; `crates/redact/src/user_regex.rs` | implemented |
| 16 | Office export: 5 kinds / 7 extensions, unchanged | `OfficeFormat::from_extension`, `crates/engine/src/compare.rs:180` — docx, pptx, html/htm, rtf, md/markdown | implemented, **partial/lossy** |
| 17 | Form-data: 8 extensions → 6 formats, unchanged | `Format::from_extension`, `crates/xfdf/src/lib.rs:75` — xfdf, fdf, xml, xdp, csv, txt/tab/tsv | implemented |
| 18 | Page-image export: 3 formats, unchanged | `ImageFormat`, `crates/engine/src/export.rs:362` — png, jpeg, tiff | implemented |
| 19 | MCP compact 17 entries; 4 resource templates + 2 list resources; 16 MiB line cap | `COMPACT_CORE_TOOLS`, `crates/automation/src/mcp.rs:45` (15 core) + `tool_search` + `tool_call`; `resource_templates()` (4) and `resource_list()` (2); `MAX_LINE_BYTES` 16 MiB | implemented |
| 20 | Split view and initial-view chrome hiding | `view.split` / `crates/ui-egui/src/panes.rs`; `view.toggle_interface` / `crates/ui-egui/src/viewer_prefs.rs` (`HideToolbar`, `HideMenubar`, `HideWindowUI`, ISO 32000-2 Table 147) | implemented |
| 21 | Portfolio: file list and `/D` document first; `doc_info` reports both | `crates/ui-egui/src/app/files.rs:564-587`; `crates/render/src/inspect/model.rs:817`; `crates/automation/src/json.rs:351` | implemented; no tool extracts an attachment |
| 22 | 3D: PRC renders from named/orbit views; U3D still cannot draw | `model_render` in `crates/automation/src/tools.rs`; `crates/prc-render/src/nav/{mod,orbit,axes}.rs` | implemented / **partial** (U3D) |
| 23 | Text replace inside paragraphs and preparation of grouped text | `text_replace` (`crates/engine/src/find_replace.rs`) and `text_prepare` (`crates/automation/src/tools.rs`); command `edit.replace` | implemented; partial coverage (see skips) |
| 24 | Copy/paste page objects within or between documents | `object_copy` / `object_paste`; `crates/engine/src/rich_copy.rs`, `crates/engine/src/object_clip.rs` | implemented |
| 25 | Prepress: fix hairlines, convert colours, printer marks, driver papers | `crates/edit/src/hairlines.rs`, `crates/edit/src/convert_colours.rs`, `crates/edit/src/printer_marks.rs`; commands `prepress.*`; `printer_papers` | implemented / **partial** (no ICC, output intent or separations) |
| 26 | Document actions: Open, WillSave and WillPrint run | `crates/engine/src/js.rs:819` `DocumentScriptEvent`; call sites `crates/ui-egui/src/editing/save.rs:131`, `workflows/print_ui.rs:639`, `engine/src/js.rs:1095` `run_open_scripts` | implemented; other triggers absent |
| 27 | Accessibility: 32 rules in 7 categories; layout table → blocks tool | `crates/a11y/src/lib.rs:3,77`; `accessibility_layout_table_to_blocks`, `crates/a11y/src/layout_table.rs` | implemented |
| 28 | XFA milestone 12: prototypes, traversal, linked images, table rows, master-page fields, template properties | `crates/xfa/src/{proto,traverse,linked_images}.rs`; `crates/js/src/xfa/props.rs`; `xfa_to_static` | implemented / **partial** (full XFA still incomplete) |
| 29 | No Preflight panel; PDF/A only 2b/3b and structural | `crates/preflight/src/lib.rs:41` `Level::{A2b,A3b}`; catalogue's Preflight is `Planned("M11")` (`crates/engine/src/catalog.rs:411`) | not implemented / partial |
| 30 | Headless OCR is English-only | `crates/ocr/src/ocrs.rs:32` `LANGUAGES = [("en", "English")]`; tool `language` enum built from it; Tesseract allow-list in `crates/ocr/src/tesseract.rs` is not exposed | implemented with limit |
| 31 | Attachments are one-way; `content_copy` is added content only | `attachment_add`/`attachment_delete`/`attachment_edit`; no extract tool; `content_copy` vs `object_copy` in `crates/automation/src/tools.rs` | implemented with limits |
| 32 | Web: in-page `window.pdfcraft` API with `?control`; OCR in Web Workers | `apps/pdfcraft-web/src/api.rs`; `apps/pdfcraft-ocr-worker/src/main.rs`; `apps/pdfcraft-web/index.html` | implemented / **partial web build** |

## 2. Headline counts: v0.19.0 → v0.21.1

| Surface | v0.19.0 (measured) | v0.21.1 (measured) | Change |
|---|---:|---:|---|
| Automation tools | 195 | **208** | +13, none removed |
| Registry commands | 214 | **221** | +7, none removed |
| Tools with a command id (distinct ids / registry ids) | 99 (73 / 71) | **104 (77 / 75)** | +5 tools, +4 ids |
| Read-only / destructive tools | 53 / 30 | **54 / 30** | +1 read-only |
| Commands with no tool | 143 | **146** | +3 after additions |
| UI control methods | 17 | **17** | unchanged at v0.21.1 |
| CLI subcommands | 14 + `check-one` | **14 + `check-one`** | unchanged at v0.21.1 |
| CLI `--flag` names | 34 | **34** | unchanged at v0.21.1 |
| Launch view keys | 58 | **58** | unchanged at v0.21.1 |
| All-tools catalogue | 152 / 23 groups / 29 sections | **152 / 23 / 29** | unchanged totals; planned entries 24 → 21 |
| Convertible input extensions | 13 | **13** | unchanged at v0.21.1 |
| Office import extensions | — (absent) | **28** | new at v0.21.1 |
| Office export | 5 kinds / 7 ext | **5 kinds / 7 ext** | unchanged at v0.21.1 |
| Form-data extensions → formats | 8 → 6 | **8 → 6** | unchanged at v0.21.1 |
| Redaction patterns | 6 | **6** (+ custom regex) | unchanged at v0.21.1 |
| Page-image export formats | 3 | **3** | unchanged at v0.21.1 |
| Print paper presets | 21 | **23** | +2 |
| Comment types | 20 | **20** | unchanged at v0.21.1 |
| MCP compact entries / resources | 17 / 4 templates + 2 | **17 / 4 + 2** | unchanged at v0.21.1 |
| Interface languages | not measurable | **not measurable** | catalogs live in the `craft-i18n` pin |

## 3. Uncertain / not verified

- GUI behaviour not launched; registry, tool schemas, engine code and the read-only `--version`/`--help` runs are the evidence.
- The new tools were not exercised end to end: hairline fixing, colour conversion, printer marks, text replace/prepare, object copy/paste, form focus/pointer scripts, portfolio presentation, split view and Office import are read from code and their schemas.
- Office import was not run; no LibreOffice installation or conversion was assumed. The 28 extensions and the worker/frame-thread split are from code.
- U3D rendering was not tested; `model_render` documents that only PRC streams draw.
- The Tesseract OCR engine was not exercised (no `tesseract` binary was assumed or run); its 12-language allow-list is code-only and unreachable because the tool's `language` enum is built from `ocrs::LANGUAGES` (`["en"]`).
- Prepress was not exercised on a real print file; "partial" means the code path and tool exist, not that a print house signed off.
- Text replace's overlap warning (new rows can overlap what follows) is documented in the tool description and not visually verified.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `docs/target-app-parity.md`, `docs/ui-parity.md` still say "141 automation tools / 184 registered commands" | 208 / 221 |
| README says MCP `--compact` returns "about ten core tools" | 15 core + `tool_search` + `tool_call` = 17 |
| `docs/gaps.md` gap 8 says Insert, Combine and Create Multiple do not take Office files | Headless `doc_combine`/`doc_create_multiple` do; GUI Combine/Insert/Create Multiple refuse on the frame thread; File ▸ Open converts in the background |
| `docs/gaps.md` gap 18 lists colour conversion as missing (while also saying fix hairlines is in) | Both are tools (`doc_convert_colours`, `doc_fix_hairlines`) and commands (`prepress.convert_colors`, `prepress.hairlines`) |
| `docs/gaps.md` gap 16 says comment pop-ups cannot be moved | `comment_popup` moves one (`rect`), opens or closes it |
| Previous skill said 150 catalogue entries / 24 groups / 30 sections | 152 / 23 / 29 at both tags |
| Previous skill said 25 CLI `--flag` names / 46 launch keys | 34 / 58 at both tags |
| Previous skill said "no Office import", "no portfolio view", "split view missing" | Office import via LibreOffice; portfolio view and split view exist |
| Previous skill said `ui.dock` is a control method | The method is `ui.panel`; `ui.dock.reset` resets it |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # b503b2e62dfeec5598f344e4e287d9c9cbdb34fa
git -C <clone> diff --shortstat v0.19.0..HEAD                   # 872 files, 165335 insertions, 11319 deletions
python3 - <<'PY'                                                # 208 tools, 195 at v0.19.0
import re, subprocess
for tag in ("v0.19.0", "v0.21.1"):
    src = subprocess.run(["git","show",tag+":crates/automation/src/tools.rs"],capture_output=True,text=True).stdout
    print(tag, len(re.findall(r'\bt\(\s*"([a-z][a-z0-9_.]*)"', src)))
PY
grep -cE '^\s+c\("|^\s+c\($' crates/engine/src/commands.rs      # 221
grep -oE '"[a-z]+\.[a-zA-Z.]+"' crates/ui-egui/src/control/requests.rs | sort -u | wc -l  # 17
grep -cE '\.cmd\(' crates/automation/src/tools.rs               # 104 (per-block parsing gives 77 distinct ids)
grep -c 'Planned(' crates/engine/src/catalog.rs                 # 27 = 21 items + 5 groups + the enum declaration
grep -n 'CONVERTIBLE' crates/create/src/lib.rs                  # [&str; 13]
grep -n 'pub const PAPERS' crates/print/src/settings.rs       # [&str, (f64,f64); 23]
ls crates/ui-egui/src/i18n/*.tsv | wc -l                        # 0 (catalogs are not in-tree)
```

The exact-set diffs were done with a one-off script over the tool and command declarations at both tags; totals above are the resulting set sizes.

## Round 2026-11-12 (refresh)

- Pinned to `v0.21.1` = `b503b2e62dfeec5598f344e4e287d9c9cbdb34fa`; installed `pdfcraft 0.21.1`.
- Tools 195 → **208** (+13, none removed); registry commands 214 → **221** (+7, none removed).
- `references/automation-tools.md` was regenerated from `tools()` at this tag (208 rows) rather than carried forward.
- Corrected the stale counts, the `ui.dock` method name, the Office-import/portfolio/split-view/print-production claims, and the limits around `content_copy`, document actions and `doc_create` text listed in §4.
- Paths: every repo-relative path cited by `SKILL.md` was re-resolved with `git cat-file -e HEAD:<path>`; all exist (brace shorthands expanded). Nothing was deleted for being wrong.
