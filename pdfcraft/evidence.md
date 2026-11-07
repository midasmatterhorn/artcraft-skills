# PdfCraft — evidence ledger (tag v0.19.0)

Audit basis: this checkout is tag **`v0.19.0`**, commit **`8c572792d6760bdc903d6f9a032e3e38e8f71cb8`** ("Release 0.19.0: the internal crates' version requirements", 2026-11-06); inspection **2026-11-07**. `git rev-parse HEAD` in the pinned checkout matches. The installed bundle prints `pdfcraft 0.19.0`; the GUI was never launched.

v0.18.1 → v0.19.0 delta (measured, not quoted from notes): **375 files** changed (`git diff --stat v0.18.1..HEAD`, +58 349 / −3 517). Automation **+11 tools, none removed**; **+4 registry command ids, none removed**; control methods 17 = 17; `apps/pdfcraft-cli/src/main.rs` zero diff. New surfaces: 3D models (U3D/PRC annotation, PRC→PNG), bookmark tree export/import/copy, comment copy/paste between documents, PCX input, IBAN redaction pattern, a second OCR engine with review/dictionary/confidence, in-place scan enhancement, and a new file identifier for redacted or sanitized copies.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 195 automation tools (+11 at v0.19.0, none removed) | `crates/automation/src/tools.rs` — unique `t("name"` set = 195 (162 inline + 33 wrapped; 184 at v0.18.1); additions `bookmark_copy`, `bookmark_export`, `bookmark_import`, `comments_copy`, `comments_paste`, `model_add`, `model_render`, `ocr_dictionary`, `ocr_review_apply`, `ocr_words`, `page_enhance_scan` | implemented |
| 2 | 214 registry command ids (+4) | `crates/engine/src/commands.rs:165` `COMMANDS` — 214 `c("id")` (210 at v0.18.1); `comment.copy`, `comment.paste`, `ocr.correct`, `ocr.enhance` added | implemented |
| 3 | 17 UI control methods unchanged | `crates/ui-egui/src/control/requests.rs` — identical 17-method set at both tags | implemented |
| 4 | Interface languages: no in-tree count | `crates/ui-egui/src/i18n/` holds only `tests.rs`; catalogs are embedded from the `craft-i18n` pin (`craft-i18n.rev` = `575cfdef…`) by `crates/ui-egui/src/i18n.rs` | unmeasurable (claim dropped) |
| 5 | CLI 14 documented subcommands + internal `check-one` | `apps/pdfcraft-cli/src/main.rs` match arms; zero diff between tags | implemented |
| 6 | 99 tools carry a command id, covering 73 registry ids | per-`t(` chunk `.cmd("…")` (99) ∩ `COMMANDS` (73 of 214; 71 of 210 at v0.18.1; `edit.undo`/`edit.redo` are tool-only names) | implemented |
| 7 | 13 convertible input extensions (+`pcx`) | `CONVERTIBLE`, `crates/create/src/lib.rs:749` | implemented |
| 8 | 6 redaction patterns (+`Iban`) | `PATTERNS`, `crates/redact/src/patterns.rs:17` | implemented |
| 9 | 3D models: `model_add` takes U3D or PRC with a poster; `model_render` draws PRC to PNG | tool descriptions in `crates/automation/src/tools.rs`; `crates/prc/`, `crates/prc-render/`; U3D draw returns an error | implemented / **partial** (no U3D rendering) |
| 10 | Bookmark tree export, import and copy between documents | `crates/organize/src/outline_io.rs`; `bookmark_export`, `bookmark_import`, `bookmark_copy` | implemented |
| 11 | Comment copy/paste between documents | `crates/automation/src/comments.rs`; `comments_copy` returns XFDF, `comments_paste` adds it; commands `comment.copy`/`comment.paste` | implemented |
| 12 | OCR: two engines, ensemble strategies, confidence bands, review loop, dictionary | `crates/ocr/src/{lib,ocrs,tesseract}.rs`, `crates/ocr/README.md`, `crates/ocr/src/confidence.rs`; tools `ocr_words`/`ocr_review_apply`/`ocr_dictionary`; existing OCR tools gained `engine`, `strategy`, `retain_review` | implemented; `language` enum still `["en"]` |
| 13 | Scanned pages are cleaned in place | `crates/engine/src/scan_clean.rs:207` `enhance_scanned_pages`; tool `page_enhance_scan` | implemented |
| 14 | A redacted or sanitized copy gets a new file identifier | `crates/redact/src/lib.rs:667`, `crates/redact/src/sanitize.rs:678` (ISO 32000-2 §14.4) | implemented |
| 15 | Compare has page-scoped engine calls that no tool argument exposes | `crates/engine/src/compare.rs` (`compare_pages`, `compare_report_of`, `mark_differences_of`); `doc_compare*` schemas have no `pages` argument | implemented (engine), not reachable headlessly |
| 16 | Page-image export runs on worker threads | `crates/render/src/raster/work_queue.rs` | implemented (unchanged) |
| 17 | XFA: static form with thousands of filled fields; signature fields named by SOM path; round checkbox highlight | PRs #4638, #4507, #4512; `crates/xfa/src/{lib,layout}.rs` | implemented (carried) |
| 18 | Redaction F-008/F-011: vector paths behind clipping not retained; unused Type 3 glyph programs unlinked | PRs #4577, #4579; `crates/redact/src/` | implemented (carried) |
| 19 | Native macOS menus from craft-menu; craft-ui task panes; craft-ui ComboBox | PRs #4752, #4606; `crates/ui-egui/src/` | implemented (carried) |
| 20 | No Office import; no PDF/X or PDF/UA verification; attachments one-way; no timestamp server | `docs/gaps.md`; attachment tool set | not implemented (verified absent) |
| 21 | Office export: 5 kinds / 7 extensions (was reported as 4/5) | `OfficeFormat::from_extension`, `crates/engine/src/compare.rs:180` — `docx`, `pptx`, `html`/`htm`, `rtf`, `md`/`markdown`; Markdown already present at v0.18.1 | implemented, **corrected** |
| 22 | All-tools catalogue unchanged: 150 items in 24 groups (30 sections) | `crates/engine/src/catalog.rs:75` `TOOL_GROUPS` | implemented (carried) |

## 2. Headline counts: v0.18.1 → v0.19.0

| Surface | v0.18.1 (measured) | v0.19.0 (measured) | Change |
|---|---:|---:|---|
| Automation tools | 184 | **195** | +11, none removed |
| Registry commands | 210 | **214** | +4, none removed |
| Tools with a command id (distinct registry ids) | 96 (71) | **99 (73)** | +3 tools, +2 ids |
| UI control methods | 17 | **17** | unchanged at v0.19.0 |
| CLI subcommands | 14 + `check-one` | **14 + `check-one`** | unchanged at v0.19.0 |
| Convertible input extensions | 12 | **13** | +`pcx` |
| Redaction patterns | 5 | **6** | +`Iban` |
| Office export | 5 kinds / 7 ext | **5 kinds / 7 ext** | unchanged at v0.19.0 (the skill's old 4/5 was wrong) |
| Form-data extensions → formats | 8 → 6 | **8 → 6** | unchanged at v0.19.0 |
| Page-image export formats | 3 | **3** | unchanged at v0.19.0 |
| All-tools catalogue | 150 / 24 groups | **150 / 24 groups** | unchanged at v0.19.0 |
| MCP compact entries / resources | 17 / 4 templates + 2 | **17 / 4 templates + 2** | unchanged at v0.19.0 |
| Interface languages | not measurable | **not measurable** | catalogs live in the `craft-i18n` pin |

## 3. Uncertain / not verified

- GUI behaviour not launched; registry, tool schemas and engine code are the evidence.
- The Tesseract OCR engine was not exercised (no binary assumed or run); its 12-language allow-list is code-only and unreachable because the tool's `language` enum is built from `ocrs::LANGUAGES` (`["en"]`).
- U3D rendering was not tested; `model_render` refuses it.
- The `model_add` poster path and `page_enhance_scan` image write-back were read, not exercised on a real scan.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| Several repo docs "141 automation tools / 184 registered commands" | 195 / 214 |
| Previous skill's at-a-glance table "183 tools / 205 commands / 35 languages" | 195 / 214 / no measurable language count |
| Previous skill "71 tools mapped to a command" | 99 tools; 73 distinct registry ids |
| Previous skill "134 of 210 commands have no tool" | 141 of 210 at v0.18.1; 143 of 214 at v0.19.0 |
| Round context compare API "300 files changed" | 375 files in the clone's `v0.18.1..HEAD` diff |
| Previous skill "Office export 4 kinds / 5 extensions" | 5 kinds / 7 extensions (Markdown already at v0.18.1) |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # 8c572792d6760bdc903d6f9a032e3e38e8f71cb8
git -C <clone> diff --stat v0.18.1..HEAD                        # 375 files, +58349 / -3517
grep -oE '\bt\(\s*"[a-z][a-z0-9_.]*"' crates/automation/src/tools.rs | sort -u | wc -l  # 162 inline names
grep -cE '^\s+t\($' crates/automation/src/tools.rs              # 33 wrapped declarations (162+33 = 195)
grep -cE '^\s+c\("|^\s+c\($' crates/engine/src/commands.rs      # 214
grep -oE '"[a-z]+\.[a-zA-Z.]+"' crates/ui-egui/src/control/requests.rs | sort -u | wc -l  # 17
grep -cE '\.cmd\(' crates/automation/src/tools.rs               # 99
grep -c 'Planned(' crates/engine/src/catalog.rs                 # 30 = 24 items + 5 groups + the enum arm
grep -c 'CONVERTIBLE' crates/create/src/lib.rs                  # [&str; 13] at line 749
ls crates/ui-egui/src/i18n/*.tsv | wc -l                        # 0 (catalogs are not in-tree)
```

The exact-set diffs were done with a one-off script over `t\(\s*"name"` and `c\(\s*"id"` at both tags; totals above are the resulting set sizes.

## Round 2026-11-07 (refresh)

- Pinned to `v0.19.0` = `8c572792d6760bdc903d6f9a032e3e38e8f71cb8`; installed `pdfcraft 0.19.0`.
- Tools 184 → **195** (+11, none removed); registry commands 210 → **214** (+4, none removed).
- `references/automation-tools.md` was regenerated from `tools()` at this tag (195 rows) rather than carried forward.
- Corrected the stale counts and the mapped-tool sentence listed in §4; dropped the language total because the catalogs are no longer in-tree.
- Paths: every repo-relative path cited by `SKILL.md` was re-resolved with `git cat-file -e HEAD:<path>`; all exist (brace shorthands expanded). Nothing was deleted for being wrong.
