---
name: wordcraft
description: >-
  WordCraft is an open-source, clean-room reimplementation of Microsoft Word in Rust (alpha,
  v0.18.1): a ribbon word processor that reads and writes .docx (password-protected and
  AES-encrypted included), opens legacy .doc, reads .mht/.mhtml, reads and writes .odt/.ott/.fodt,
  exports PDF/PNG (optionally with a strict check that refuses a silently incomplete render),
  runs several documents and several windows, plus a CLI (wordcraft-cli), an 18-tool MCP server,
  a localhost JSON control channel and a headless screenshot harness for agents. Trigger this
  skill whenever the user mentions WordCraft, .docx/.doc/.odt/.rtf/.html/.md/.tex documents in a
  WordCraft context, wordcraft-cli, WordCraft's MCP tools or control channel, personal templates,
  mail merge, macros, track changes, or asks what WordCraft can or cannot do, which formats it
  opens or saves, how to script, automate, batch-convert, verify, repair or troubleshoot it — even
  if the app is not named but the job is word-processor work ("write a .docx", "convert this .doc
  to PDF", "check nothing is missing from this PDF", "decrypt this .docx", "add comments and track
  changes", "mail-merge a letter", "make a report from Markdown"). Do not use it for Microsoft
  Word itself or other word processors.
---

# WordCraft

**Audit basis.** Refreshed **2026-11-12** against tag **v0.18.1**, commit **`079f478bd85df7bcc567e3bafa7d7219096f9c3c`** — `git rev-parse HEAD` in the pinned checkout confirms, and the installed app bundle matches (its binary prints `wordcraft 0.18.1 (079f478b)`). The previous release this skill described was **v0.16.0** (`02a802cbafe45b5c8fecc00490c8f6b78c5ba251`).

**v0.16.0 → v0.18.1 delta.** The diff is **358 files (+23,251/−1,410)**, cumulative across the two intermediate releases (this shallow checkout holds only the v0.16.0 and v0.18.1 tag objects). Registry: **671** live command ids (656 at v0.16.0); the additions are nine paragraph tools — `para.convertBreaks`, `para.blankBetween`, `para.separateParagraphs`, `para.removeBlank`, `para.trimLeadingSpaces`, `para.removeExtraSpaces`, `para.spacesToIndent`, `para.indentToSpaces`, `para.removeLineBreaks` (`crates/engine/src/cmd/para/tools.rs`) — plus `text.deleteSentenceBack` (`crates/engine/src/cmd/text/delete.rs`), `view.paperColor` and the window commands `view.arrangeAll` / `view.sideBySide` / `view.syncScroll` (`crates/engine/src/cmd/view.rs`), and `file.strictReport` (`crates/engine/src/cmd/file.rs`). **Strict export (#6005)** is the headline for agents: `file.save`, `file.saveAs`, `file.exportPdf` and `file.exportPng` take `strict: true` and write nothing if the output would draw a character no face has or leave out a picture, and `file.strictReport {markup?, page?}` returns the schema-1 JSON report (256-entry caps; reasons `missing_part`, `external_target`, `link_only`, `undecodable`, `unsupported_format`) — `crates/engine/src/strict.rs`, `crates/layout/src/{strict,missing}.rs`, `crates/doc/src/missing.rs`; the CLI's `convert --strict` and `render --strict` exit **3** with the report on stderr (`apps/wordcraft-cli/src/main.rs`). MCP: **18** tools, adding `insert_table` (a filled table in one call, backed by `insert.spreadsheet`, 1–1000 rows × 1–63 cells) (`crates/mcp/src/tools.rs`); a bridged mutation whose delivery or reply is unknown now returns `outcome unknown` and is never replayed (`crates/mcp/src/backend.rs`). The control channel is still **22** methods, but a request still queued after 60 s is cancelled and can never run, one that started reports an unknown outcome, unauthenticated connections are capped at 64, and `ui.inspect` now carries `windows` (`apps/wordcraft/src/control_server.rs`, `crates/ui-egui/src/control/handler.rs`). View › Window is real across the app's native windows — Arrange All, Side by Side, Synchronous Scrolling — and `view.switchWindows` takes `window` as well as `id` (`crates/engine/src/cmd/view.rs`, `crates/ui-egui/src/windows/arrange.rs`), which lifts catalog coverage to **509/521 (97.7%)**; the missing list falls to 11 distinct features. Personal templates: `file.newFromTemplate` takes `data` (base64 bytes), `password` and `replaceBlank`, and a template opened from the file manager starts a new document and is never written over (`crates/engine/src/cmd/tools/specs.rs`, `crates/ui-egui/src/documents.rs`). Formats: RTF now reads and writes footnotes, endnotes and comments (#1053) (`crates/formats/src/rtf/`), the ODT gap-19 batch lands frames, styles, picture and heading work (`crates/formats/src/odt/`), and Strict Open XML documents open their shapes, text boxes, groups and canvases (`crates/docx/tests/it/strict_drawings.rs`); open/save extensions stay **23/16** (`crates/engine/src/io.rs`). CLI: **10** subcommands and **22** flags (+`--strict`). Docs still print 508/520; dialog names are **92** (+`dateTime`) and `.key()` sites **167**.

**v0.15.1 → v0.16.0 delta.** 475 files changed. Registry 652 → **656** ids (`font.missing`, `format.emphasisMark`, `select.member`, `smartArt.itemColor`); control methods 21 → 22 (`file.closeDocument`); `OPEN_EXTS`/`SAVE_EXTS` 21/14 → **23/16** (`.ott`, `.fodt` on both, ODT gap-19 work, password-protected ODT); `file.printPdf` took `pagesPerSheet` (n-up and booklets); catalog 505/520 → 506/521; the web build gained a page host (`data-host="page"`).

**v0.14.0 → v0.15.1 delta.** 316 files changed. The automation sets did not move (652 ids, same MCP tools and control methods). Proofing was unified into one Hunspell engine with a language table and affix features (#4191, #4575); View › Macros (run/delete/record); Chinese and Japanese characters counted as words; Alt/F keytips; HTML empty comments; CSV separator detection; TOC page numbers as PAGEREF fields; undefined DOCX styles formatted as Normal.

**Verify against your installed version** — the ArtCraft Launcher auto-updates, so a newer build may differ; every count quoted here was re-measured at this tag, and code paths that moved were re-cited. The measurement method for each count is in `evidence.md`.

## Overview

WordCraft is an open-source, clean-room reimplementation of Microsoft Word (Microsoft 365) in pure Rust — "writing and document design" — by the ArtCraft team (`README.md`). It is at **alpha** (`ROADMAP.md`): self-rated ~60% ready for real work, ~55% for a mainstream practitioner's week and ~63% for everyday essentials, with **509 of 521** ribbon/menu catalog features wired to live commands (97.7%; derived from `crates/engine/src/catalog.rs` against the registry — the committed `docs/parity-checklist.md` still prints 508/520, one row behind). One codebase serves macOS, Windows, Linux, BSD and the web: egui/eframe on the GPU, no Electron. Source: GitHub **storytold/wordcraft**, MIT OR Apache-2.0. It reads and writes Microsoft's formats from published specifications (ECMA-376/ISO 29500, MS-DOC, OASIS ODF, MS-OFFCRYPTO), never from their code.

Everything user-visible is a **command with an id**; the ribbon, keyboard, command search, CLI, control channel and MCP all dispatch the same registry. **Several documents can be open at once, and a document can have several native windows** (`crates/ui-egui/src/windows.rs`); automation addresses a *document* by id, and a *window* by the key `ui.inspect` reports.

## Capabilities (verified)

### Automation surface at a glance

Every number below was re-counted from this tag's code on 2026-11-12; the change column says explicitly where a set is unchanged at v0.18.1. The repo's own prose counts are stale (see the note under the table).

| Surface | v0.18.1 | Change since v0.16.0 |
|---|---|---|
| Engine commands (`CommandSpec::new` with a literal id) | **671** | +15 (nine `para.*` tools, `text.deleteSentenceBack`, `view.paperColor`, `view.arrangeAll`, `view.sideBySide`, `view.syncScroll`, `file.strictReport`); 673 sites including 2 test fixtures in `crates/engine/src/tests.rs` |
| Catalog coverage | **509 / 521 (97.7%)** | +3 rows live (`view.arrangeAll`, `view.sideBySide`, `view.syncScroll`); `docs/parity-checklist.md` says 508/520 — stale by one row |
| CLI subcommands | **10** | unchanged at v0.18.1 (`apps/wordcraft-cli/src/main.rs` `SUBCOMMANDS`) |
| CLI flags | **22** plus `-h/--help`, `--version` | +1 (`--strict`) |
| MCP tools | **18** | +1 (`insert_table`); `crates/mcp/src/tools.rs` |
| Control-channel methods | **22** | unchanged at v0.18.1; timeout and admission behaviour changed (`apps/wordcraft/src/control_server.rs`) |
| Interface languages | **28** | unchanged at v0.18.1; `craft-i18n.rev` also unmoved (`1e515422…`) |
| Built-in proofing languages | **16** | unchanged at v0.18.1 (`crates/ui-egui/src/ribbon/language.rs`) |
| Default shortcuts | **167** `.key()` sites, **164** command bindings | +1 binding (`text.deleteSentenceBack`); three sites are diff helpers in `crates/engine/src/cmd/tools/compare.rs` |
| Open / save extensions | **23 / 16** literals (open includes the compound `wcraft.json`) | unchanged at v0.18.1 (`crates/engine/src/io.rs`) |
| Dialog names | **92** distinct `Dialog::name` values | +1 (`dateTime`); docs say 61 modal dialogs — a different measure |

Do not quote the repo's command counts: `README.md` still prints "422 commands", `ROADMAP.md` prints "433 commands" and "493 / 508", and `docs/mcp.md` describes `list_commands` as "over 270 of them" — all stale. Count with `wordcraft-cli commands --json` on the build you drive. The dialog count runs the other way: `docs/gaps.md` gap 7 says "61 modal dialogs", the code answers to 92 distinct names (measured across the five `Dialog::name` methods in `crates/ui-egui/src/dialogs.rs` and `crates/ui-egui/src/dialogs/`).

### Carried from v0.12.0–v0.16.0 (still true at v0.18.1)

- Multi-document work; `doc` addressing on the document tools (`execute`, `batch`, `save_document`, `type_text`, `select_text`, `get_text`, `inspect_document`, `render_page`), `engine.execute`/`document.inspect`/`ui.render`, and `file.closeDocument {id?, force?}`. `view.newWindow` opens another window on one document; each window has its own selection, zoom, view mode and panes.
- AES-encrypted Word files open: agile (Word 2010+) and Standard (Word 2007-era AES) methods (`crates/docx/src/crypt.rs`).
- Regex Replace expands capture groups; scale all style font sizes at once; style sets keep the document's own styles; task panes dock/float on craft-ui's shared panes.
- Import hardening: legacy `.doc` reader budgets, render/PDF/metafile budgets, DOCX package and writer hardening, bounded MCP line reads; Zotero bridge loopback-only with a same-user check on Linux (`crates/zotero/src/peer.rs`).
- Dialog depth: 92 dialog names, modal except Find and Replace, Symbol, Mark Index Entry, Cross-reference and Insert Merge Field.

### Editing, formatting, document features

- Writing: typing/IME, AutoCorrect, list autoformat, selections, clipboard with formatting (HTML/RTF from other programs), undo/redo incl. an undo-history list (`edit.undoTo`, `edit.undoHistory`), find & replace with regex (capture-group expansion); typing behaviour is pinned to Word's by `crates/engine/src/tests/typing.rs`. `text.deleteSentenceBack` deletes to the sentence start (or the previous sentence at a boundary) and never crosses a paragraph or cell boundary.
- **Paragraph tools** (`Home › Paragraph › Paragraph Tools`, `crates/engine/src/cmd/para/tools.rs`): convert line breaks to paragraphs, insert blank paragraphs between, separate paragraphs, delete blank paragraphs, remove leading spaces, remove extra spaces, convert spaces to indentation and back, remove line breaks. Each works on the selection or `{"scope": "all"}`, is one undo step, respects Track Changes, and refuses more than 10,000 paragraphs.
- Formatting, paragraphs, styles/themes/style sets, lists (Arabic letter numbering drawn), tables (styles with band sizes, merge/split, sort, formulas, Convert to Text), pages/sections (margins, columns, headers/footers with editable three-column presets, watermark, line numbers, hyphenation, drop caps, page borders), objects (pictures with crop/recolour/background removal, shapes, text boxes, groups, drawing canvases with per-member selection via `select.member`, wrap, free rotation), references (TOC, footnotes/endnotes, citations APA/MLA/Chicago/IEEE, captions, table of figures, index, cross-references, Zotero), review (spelling/grammar, comments with local-time stamps, track changes incl. moves and formatting revisions, accept/reject, compare with a character-level fallback counter, restrict editing), mail merge (CSV/spreadsheets, rules, Finish & Merge, Print Documents), Draw-tab ink, Read Aloud, Print/Web/Draft/Read/Focus/Full Screen views.
- Fonts: `font.missing` reports the fonts a document asks for that are not installed, the family each is drawn in and whether that substitute measures the same (`metricCompatible`); the font box and status bar flag them (`crates/engine/src/cmd/font.rs`). Emphasis marks are a real text property (`format.emphasisMark`), drawn and written to DOCX (`w:em`) and ODT (`style:text-emphasize`).
- Content controls (`w:sdt`), move tracking (`w:moveFrom`/`w:moveTo`), formatting revisions and glossary/building blocks round-trip.
- Fields: date fields follow the document's language for their default picture (`crates/engine/src/cmd/references/fields.rs`); SEQ fields in a tracked deletion keep their result and do not count, locked SEQ fields count but keep their result.

### Import / open (by extension, `crates/engine/src/io.rs` OPEN_EXTS)

- `.docx` / `.docm` / `.dotx` / `.dotm` (Word package; Strict Open XML read via namespace mapping, including shapes, text boxes, groups and canvases), `.doc` / `.dot` (Word 97-2003 binary reader, `crates/docbin`), `.txt`, `.md`, `.markdown`, `.html`/`.htm`, `.rtf`, `.odt`/`.ott`/`.fodt` (OpenDocument text; flat `.fodt` too), `.mht`/`.mhtml` (single-file web page; **read only** — saving MHT remains a gap), `.tex`/`.latex`/`.ltx`, `.xml` (Word XML Document / Flat OPC or Word 2003 XML), `.json` (WordCraft's native document model), and `*.wcraft.json`.
- Extensionless or unknown-extension files open **by content** when they are Word/RTF/XML/HTML/text, with encoding detection.
- Passwords: `.docx` opens and saves with a password — **agile** (Word 2010+) and **Standard** (Word 2007-era AES, `crates/docx/src/crypt.rs`); `.odt`/`.ott` open and save with a password (AES-256-CBC, `crates/formats/src/odt/crypt.rs`); `.doc` protected with XOR/RC4/RC4 CryptoAPI opens — untested on Word-written files; AES `.doc` is refused (`docs/gaps.md` gap 9).
- Pictures: PNG, JPEG, GIF, WebP, BMP, TIFF, plus Windows/Enhanced Metafile `.wmf`/`.emf` at their frame size. Not SVG, ICO, HEIC (`crates/engine/src/cmd/insert/objects.rs` `image_ext`).
- Pictures a DOCX names but cannot bring in (a missing part, an external target, a link-only picture with no embedded copy) are recorded beside the document and reported by strict export, never fetched.

### Save / native format / export (`crates/engine/src/io.rs` SAVE_EXTS)

- Native-lossless: `.docx`/`.docm`/`.dotx`/`.dotm` via `crates/docx`, Word XML Document (Flat OPC) and Word 2003 XML `.xml`, and `.json` for agents. A file opened with a password is saved with it again; exports that cannot carry one (pdf, html, txt) stay plain.
- `.odt`/`.ott`/`.fodt` are read and written nearly whole (repo self-estimate ~90%, `docs/file-format-parity.md`); a document saved without edits keeps what WordCraft does not model (`docs/gaps.md` gap 19). A password-protected `.odt`/`.ott` saves encrypted (`crates/formats/src/odt/crypt.rs`).
- Copies/export: `.pdf` (krilla through the pinned `craft-pdf`), `.png` page images, `.txt`, `.md`, `.html`, `.rtf`, `.tex` (partial fidelity — see limitations). PDF/PNG follow the Numeral setting for digit shapes.
- **Strict export** (#6005): add `"strict": true` to `file.save`, `file.saveAs`, `file.exportPdf` or `file.exportPng` (a `.pdf` or `.png` target only; any other target is a parameter error). Nothing is written if the output would draw a character no installed face can draw or drop a picture; the command fails with a `strict: …` message. `file.strictReport {"markup"?, "page"?}` returns the same report without writing (`crates/engine/src/strict.rs`, `crates/engine/src/cmd/file.rs`). In the CLI, `convert --strict` and `render --strict` exit **3** and put one stderr line per kind plus one JSON line on stderr; exit 1 is an ordinary error, so `3` is the code to branch on.
- Print Markup (`--markup` / `markup: true`): comments and tracked changes in PDF/PNG, a comment list in HTML/Markdown/text.
- `.doc` cannot be written; saves are atomic-by-design (temp file + replace; a failed save keeps the original bytes).

### Personal templates

- `file.listTemplates {"dir"?}` lists `.dotx`/`.dotm` in the user templates folder (top level plus one subfolder level as categories, ≤500 templates, ≤64 categories; network folders and relative paths refused; the automation read root applies). Without `dir` it uses the folder saved in File › Options and **errors if none is saved** — always pass `dir` headlessly.
- `file.newFromTemplate {"path", "data"?, "password"?, "replaceBlank"?}` opens the file as a new, untitled, **dirty** document attached to that template (no extension check). `data` carries base64 bytes when the path is not valid Unicode; `password` opens a protected template; `replaceBlank: true` lets an untouched blank document give way (what the file manager's "New" does). `file.saveTemplate {"path"}` **appends `.dotx` unless the path already ends `.dotx` or `.dotm` (any case)** — `out.docx` becomes `out.docx.dotx`. The GUI path is `ui.saveAsTemplate` (system dialog) — unusable headlessly. ODT templates are not listed by `file.listTemplates`.
- A `.dotx`/`.dotm` opened from the platform (macOS "Open with", Explorer's New) starts a new document based on it and is never written over; `file.open` still opens the template itself for editing (`crates/ui-egui/src/documents.rs`).

### Automation surfaces (all four drive the same commands)

- **CLI**: `wordcraft-cli convert|info|text|inspect|render|run|commands|parity|mcp|zotero` with flags `--markup`, `--strict`, `--update-fields`, `--format wordml2003|flatopc`, `--page`, `--scale`, `--file`, `--template`, `--cmd 'id={json}'`, `--save`, `--print`, `--author`, `--password`, `--password-file`, `--script FILE|-`, `--json`, `--markdown`, `--connect`, `--automation-read-root`, `--automation-write-root`, and Zotero's `--trace`, `--port` (`apps/wordcraft-cli/src/main.rs` usage text is authoritative). A repeated or value-less `--format` is an error rather than silently ignored.
- **`run --script`**: a JSON job file or stdin — `{"file"?, "template"?, "commands": […], "save"?: ["out.docx", "out.pdf"]}` — runs the commands, then saves to each output, format by extension. Relative `file`/`save` paths resolve against the script's folder; capped at 4 MiB, 100,000 commands, 64 outputs. A failing command stops the run with `command N (id): …` and exit 1 before any output is written. `--print` echoes each command's `id: <json>` result.
- **MCP server** over stdio: `wordcraft-cli mcp` (headless) or `--connect 127.0.0.1:<port>` (bridged to a running app). **18 tools**: `list_commands`, `execute`, `insert_table`, `batch`, `new_document`, `open_document`, `save_document`, `type_text`, `select_text`, `get_text`, `inspect_document`, `render_page`, `parity`, `list_documents`, and app-only `screenshot`, `click`, `key`, `ui_inspect` (`crates/mcp/src/tools.rs`). The document tools — `execute`, `batch`, `save_document`, `type_text`, `select_text`, `get_text`, `inspect_document`, `render_page` — take optional `"doc": <int>` to target an open document; `list_documents` enumerates them. `insert_table` takes `values` (rows of cells, all the same length, 1–1000 × 1–63), optional `header` and `style`; it is the one-call form of `insert.spreadsheet`. Protocol revision `2025-06-18`, resources `wordcraft://document` and `wordcraft://commands`.
- **MCP delivery semantics**: with `--connect`, a request not yet written is retried once; once sending starts, a failed write or a lost reply is **outcome unknown** for a mutation and is never resent. Read-only retries are limited to `document.inspect`, `engine.commands`, `ui.inspect`, `ui.parity` and path-less `ui.render`/`ui.screenshot` (`crates/mcp/src/backend.rs`, `docs/mcp.md`). Inspect the document before repeating the operation yourself.
- **Control channel**: app started with `--control <port>`; JSON lines over `127.0.0.1` with a per-window key from `<settings>/control-key.<instance>` (`local-<port>` outside Flatpak; mode 0600, removed on exit) (`crates/control-key/src/lib.rs`, `apps/wordcraft/src/control_server.rs`). **22 methods**: `engine.execute {command, params, doc?}`, `engine.commands`, `document.inspect {doc?}`, `ui.inspect`, `ui.click`, `ui.clickText`, `ui.move`, `ui.drag`, `ui.press`/`ui.release`, `ui.wheel`, `ui.key`, `ui.text`, `ui.screenshot`, `ui.render {doc?}`, `ui.parity`, `ui.resize`, `ui.focus`, `file.close`, `file.closeDocument {id?, force?}`, `file.exportPng`, `app.quit`; any other method name is treated as a command id (`crates/ui-egui/src/control/handler.rs`; `docs/control-protocol.md`). `ui.key`/`ui.text` are background-safe and reply `{"queued": true}` before the edit is applied. `file.close` and `file.closeDocument` refuse a document with unsaved changes unless `{"force": true}`.
- **Control timeouts**: a 1 MiB request line and a 30 s first-request window apply; a request still queued after 60 s is cancelled and can never run, while one that had started at the deadline returns an `outcome unknown` error. At most 64 unauthenticated connections are admitted. `ui.inspect` now carries `windows` (ids, the active one, the Side by Side pair); `ui.screenshot` captures the root viewport, so select a secondary window with `view.switchWindows {"window": <key>}` first.
- **Macros**: `tools.recordMacro` / `tools.macros` record and replay command sequences.
- **Headless UI screenshots**: `cargo run -p wordcraft-ui-egui --example ui_shot -- script.jsonl` — JSON lines of control requests plus `{"shot": "<path>.png"}`, `{"steps": n}`, `{"wait": ms}`, `{"empty": true}`.

### Platform

- WebAssembly web build exists and is CI-checked: `apps/wordcraft-web` (`?webgl`, `?sample`, iframe `?host=parent` with `&author=`, and a page host mode: `data-host="page"` on the canvas serves a page's own document over DOM `CustomEvent`s; no TCP control channel). The page API `window.wordcraft` exposes `request`, `execute`, `commands`, `docInspect`, `uiInspect` and `screenshot` as promises over the same control requests (`apps/wordcraft-web/src/api.rs`); Open/Save go through the browser or the host bridge.
- Local recovery of unsaved work (desktop only), **per document**, covers new drafts and edits; snapshots are taken at most every ten seconds; password-protected documents get no plaintext recovery copies; headless/CLI/web sessions create none (`crates/engine/src/recovery/desktop.rs`).
- Native printing through craft-libs' `craft_ui::printing`: `ui.printSettings`, `ui.printSubmit`/`ui.print`, `file.printPdf` (also takes `paper` to scale onto another paper size, and `pagesPerSheet` to impose n-up sheets or folded booklets: 1|2|4|6|9|16|`"booklet"`|`"bookletReverse"`). A print job with no CUPS destinations answers `noPrinters`.
- Zotero integration (`crates/zotero`, `docs/zotero.md`) — needs the Zotero desktop app running; loopback-only client with a same-user check on Linux. In-app: `ui.zotero.*`; from a terminal: `wordcraft-cli zotero <command> <file>` (`addEditCitation`, `addEditBibliography`, `addNote`, `refresh`, `removeCodes`, `setDocPrefs`).
- **Startup update prompt with direct self-updating** (craft-update); Windows installs per-user by default.

## Known limitations and not-implemented

Ranked shortfalls with evidence are in **docs/gaps.md** — read it before promising anything. The blocking (beta) list:

1. **DOCX has no real-world corpus test**: no corpus of files from Word, Google Docs, LibreOffice and Pages ships in the repo; `crates/docx/tests` are synthetic fixtures. Treat fidelity on files you did not create as unverified and round-trip the user's file.
2. **Word's native ink is not drawn from its strokes** (its picture fallback shows) and **OLE objects show only their picture**; every ink form, drawing canvas, group shape, chart and SmartArt is preserved and written back with all parts.
3. **Field crashes and freezes** remain open: startup crash on Intel UHD Graphics (#170), macOS 12.7.6 Intel crash (#979), Thai-font and font-selector freezes (#59, #31). Save-path reliability was narrowed, not closed.
4. **Pagination differs from Word**: no Aptos-metric font, legacy compatibility options partial, no page-by-page comparison harness.
5. Still missing from the review/data model: drag-and-drop moves (no text drag yet), tracked style-definition changes, custom-XML binding evaluation.
6. Print dialog depth: driver tray/options and device-specific settings — WordCraft imposes n-up sheets and booklets through `pagesPerSheet`, but Word's printer-driver options are not exposed.
7. Dialog depth: **92** dialog names in code against Word's ~100 (the repo's own count says 61 modal — a different measure).

Catalog features with **no command** (12 rows, 11 distinct features; `insert.inkEquation` is listed twice): `tools.dictate`, `insert.onlinePicture`, `insert.model3d`, `insert.screenshot`, `addins.get`, `insert.video`, `insert.inkEquation`, `draw.inkToMath`, `review.translate`, `review.blockAuthors`, `view.readLayout` (`crates/engine/src/catalog.rs`).

Other verified gaps:
- **Strict export is not a completeness proof**: it checks drawn characters and pictures only. It depends on the fonts installed on the host, reports pictures dropped on DOCX open for DOCX input only, and a PNG of any page is refused for a missing or external picture anywhere in the document, unused headers included. It does not detect dropped tables, fields, styles or formatting.
- **Charts/SmartArt from Word are read-only** (no embedded-workbook editing); no combo/3D/stock charts. WordCraft's own charts and SmartArt are editable, and SmartArt items take a colour of their own (`smartArt.itemColor`).
- **`.doc` is read-only** — WordCraft never writes Word 97-2003; Word 6/95 files are refused. No PDF Reflow, no Works/WordPerfect. **MHT opens but cannot be saved** (gap 26).
- **No VBA execution** (macros in `.docm` are preserved, never run), no Office add-ins, no cloud storage, no real-time co-authoring.
- **Proofing** covers **16** built-in English/European/Spanish variants: English (US, UK, Australia, Canada), Polish, Portuguese (Brazil), Italian, Croatian, Turkish, Russian, Czech, Indonesian, Spanish (Spain, Mexico, Latin America, Uruguay) — non-English dictionaries are read from the system; Bulgarian and German have hyphenation only. Every other language needs an installed Language pack, and none of them has grammar rules (`docs/gaps.md` gap 8).
- **Writing fidelity is partial for non-Word formats**: ODT ~90% (repo self-estimate), RTF ~50% — footnotes, endnotes and comments now read and write, but revisions coverage is incomplete — HTML ~65%, MHT ~60%, Word 2003 XML ~55% and lossy (never opened in Word), Flat OPC ~65% (`docs/file-format-parity.md`).
- **RTL/East Asian depth** is incomplete: kashida; RTL in HTML/RTF (ODT RTL paragraphs are read and written; the Arabic interface's dialogs mirror).
- Mail merge sources: CSV/TSV/TXT and `.xlsx/.xlsm/.xls/.ods` only; no Outlook/Access/database sources, no email merge (`crates/formats/src/sheet.rs`).
- No in-app AI assistant (agent control is external, over CLI/MCP).
- Default shortcuts: 164 command bindings vs Word's ~250 (docs say 140/158 — stale).
- Screen-reader access is exposed through AccessKit but has not been tested with NVDA/VoiceOver/Orca.
- **Personal templates are narrow**: `.dotx`/`.dotm` only, one subfolder level, ≤500 entries, network folders refused, and the GUI picker needs a saved folder.
- The **desktop app's automation is not confined**: `--automation-read-root`/`--automation-write-root` apply to the headless MCP server only and are an error with `--connect`.
- Interface translations come from `storytold/craft-i18n`; without the `CRAFT_I18N_DIR` checkout at the pinned SHA the build is English only. 28 interface languages ship; Hindi, Indonesian and pt-PT are missing (gap 11).
- The View › Window commands are **desktop-only**; in the web, CLI and a headless MCP session they are disabled (no other native window exists).

## How to operate

Launch (macOS):
- App: `open -a WordCraft` or `open -a WordCraft --args <file.docx>`. Binary inside the bundle: `WordCraft.app/Contents/MacOS/WordCraft`. Bundle id `ai.storyteller.wordcraft`.
- App flags: `wordcraft [--sample] [--control PORT] [FILE…]`; `--version`, `-h|--help` (verified against the installed 0.18.1 binary). A bad `--control` port exits with status 2.
- **`wordcraft-cli` is not inside the app bundle.** Get it from the release artifact `wordcraft-cli-<ver>-macos-universal.zip` or build it: `cargo run --release -p wordcraft-cli -- <args>`.
- Environment variables that matter to agents: `WORDCRAFT_CONTROL_PORT`, `WORDCRAFT_CONTROL_KEY` (for `mcp --connect`), `WORDCRAFT_PROFILE_DIR` (isolated profile incl. recovery/keys), `WORDCRAFT_NO_PREFS`, `WORDCRAFT_PASSWORD`, `WORDCRAFT_REGION=en-US`, `WORDCRAFT_LANGUAGE`, `RUST_LOG`.

Document and window model: **several documents at once, each in one or more native windows** (`crates/ui-egui/src/windows.rs`). File ▸ New opens a document in a new window; `view.newWindow` adds a window on the same document (its own selection, zoom, view mode and panes); `view.switchWindows {id?|window?}` lists documents and switches either; `file.closeDocument {id, force?}` closes a document (all its windows); closing one of a document's windows leaves it open. Automation targets a document with `doc` (engine commands name it `id`), and a window with the key `ui.inspect` → `windows`. Recovery is per document.

Core commands (exact ids, from `crates/engine/src/cmd/file.rs`, `crates/engine/src/cmd/tools/specs.rs`, `crates/engine/src/cmd/user_templates.rs`, `crates/engine/src/cmd/view.rs`, `crates/engine/src/cmd/font.rs`):
`file.new {"template": "blank|sample|letter|resume|report"}` (an unrecognised name silently yields a blank document), `file.open {"path": …, "password"?}`, `file.save {"path"?, "password"?, "markup"?, "format"?, "strict"?}`, `file.saveAs`, `file.encrypt {"password": string | null}`, `file.rename {"name"}`, `file.exportPdf {"path": …, "markup"?, "strict"?}`, `file.exportPng {"path":…, "page"?, "scale"?, "strict"?}`, `file.strictReport {"markup"?, "page"?}`, `file.printPdf {"path", "range"?, "pages"?, "parity"?, "copies"?, "collate"?, "paper"?, "pagesPerSheet"?}`, `file.close {"force"?}` / `file.closeDocument {id, force?}`, `file.setAuthor {"name"}`, `file.properties`, `file.info`, `document.inspect`, `document.text`, `font.missing {}`, `review.trackChanges {"value": true}`, `review.restrict {"mode"?|"stop": true}`, `references.updateFields`, `file.listTemplates {"dir"?}`, `file.newFromTemplate {"path", "data"?, "password"?, "replaceBlank"?}`, `file.saveTemplate {"path"}`, `mailings.first|last|goToRecord|printDocuments`, `view.switchWindows {id?|window?}`, `view.stylesPaneDock`, `view.paperColor {"value": "document|green|cream|gray"}`.

Positions in command params and `document.inspect` are `{"story": "body" | {"part": n}, "path": [block, row, cell, block, …], "off": byteOffset}` (`docs/control-protocol.md`).

CLI recipes (verified usage strings):
```sh
wordcraft-cli convert report.docx report.pdf        # docx, doc [read], pdf, odt, rtf, html, md, tex, txt, json, png, xml
wordcraft-cli convert report.docx report.pdf --strict   # exit 3 and no file if a character or picture would be lost
wordcraft-cli render report.docx out.png --page 2 --scale 2 --strict
wordcraft-cli convert report.docx out.xml --format wordml2003   # or flatopc (the default Word XML Document)
wordcraft-cli convert report.odt report.docx        # ODT is read and written; .ott/.fodt are save targets too
wordcraft-cli render report.docx out.png --page 2 --scale 2     # scale defaults to 2.0, page to 1
wordcraft-cli text report.docx                      # plain text, list labels kept
wordcraft-cli info report.docx                      # pages, words, paragraphs, properties (JSON)
wordcraft-cli inspect report.docx                   # structure as JSON
wordcraft-cli run --template sample --cmd 'select.text={"text":"Membership"}' \
  --cmd format.bold --save out.docx
wordcraft-cli run --script job.json                 # commands + saves from a JSON file (- = stdin)
wordcraft-cli run --file in.docx --cmd 'file.strictReport={}' --print   # report, writes nothing
wordcraft-cli convert locked.docx out.pdf --password '…'      # or --password-file / WORDCRAFT_PASSWORD
wordcraft-cli commands --json                       # every command id, label, params, shortcut
wordcraft-cli mcp --author "Claude (copyedit)" \
  --automation-read-root project --automation-write-root project/out
wordcraft-cli zotero refresh paper.docx --save paper.docx
```
Exit status: 0 on success, 1 on error with the message on stderr, **3** on a strict refusal (`convert --strict`, `render --strict`); a failing `run` writes nothing; `wrote <path>` is printed only after a successful save. Through `run`, MCP or the control channel a strict refusal is an ordinary command error (`strict: …`), not exit 3.

Printing imposition headlessly (booklet or 2-up sheets):
```sh
wordcraft-cli run --file report.docx --cmd 'file.printPdf={"path":"booklet.pdf","pagesPerSheet":"booklet"}'
wordcraft-cli run --file report.docx --cmd 'file.printPdf={"path":"two-up.pdf","pagesPerSheet":2,"paper":"A4"}'
```

Using a personal template headlessly (no `file.new` template name exists for these; `listTemplates` demands a full path):
```sh
T="$PWD/templates"
wordcraft-cli run --cmd "file.listTemplates={\"dir\":\"$T\"}" --print   # discovery
wordcraft-cli run --cmd "file.newFromTemplate={\"path\":\"$T/Contract.dotx\"}" \
  --cmd 'select.text={"text":"[Client]"}' --cmd 'text.insert={"text":"Acme Ltd"}' --save out.docx
wordcraft-cli run --file out.docx --cmd "file.saveTemplate={\"path\":\"$T/Acme contract.dotx\"}"
```
`file.newFromTemplate` leaves the document untitled and dirty; save it outside the templates folder. Pass `replaceBlank: true` only when you know an untouched blank document is the active one.

Driving the running app (control channel):
```sh
open -a WordCraft --args --control 7981
cat "$HOME/Library/Application Support/WordCraft/control-key.local-7981"
# then one JSON object per line to 127.0.0.1:7981, e.g.
{"id":1,"key":"<key>","method":"engine.execute","params":{"command":"text.insert","params":{"text":"Hello"}}}
{"id":2,"key":"<key>","method":"engine.execute","params":{"command":"document.inspect","doc":1}}
{"id":3,"key":"<key>","method":"ui.screenshot","params":{"path":"shot.png"}}
{"id":4,"key":"<key>","method":"file.closeDocument","params":{"id":1,"force":true}}
```
An unauthorised request gets `{"ok":false,"error":"unauthorized"}` and the connection closes; a line over 1 MiB, or bad JSON, also closes it; a connection with no authorised request within 30 s is closed. A request still queued after 60 s is cancelled and can never run; if it had started, the reply says the outcome is unknown — inspect before retrying. `wordcraft-cli mcp --connect` sends the key only to `127.0.0.1` (`localhost` included, never `::1`); to drive an app on another machine, forward its port to `127.0.0.1` and set `WORDCRAFT_CONTROL_KEY`. Open/Save/Export pick formats by file extension; `--save`/`file.save` over an existing file replaces it in place.

Reading the app's own diagnostics: `<settings>/logs/wordcraft.log` (rotated, 16 MiB cap; `WORDCRAFT_NO_PREFS` runs log to stderr only). Unreadable .docx parts, pictures/fonts a PDF export left out, and recovered panics land there.

## Working with an AI agent

Legitimate, reliable agent work with WordCraft:
- **Do document work headlessly.** `wordcraft-cli mcp`, `wordcraft-cli run` (flags or `--script`) need no window, no focus and no GUI driving. Verify your own work with `inspect_document` / `get_text` / `render_page` instead of screenshots.
- **Prove a PDF or PNG is complete.** Run `file.strictReport {}` (or the CLI's `--strict`) before delivering: the report says `"strict": "failed"` and names the code points and picture parts that would be missing (the CLI exits 3). This is the one check WordCraft offers against silent render loss; it covers glyphs and pictures, not layout or semantic loss.
- **Work across documents and windows**: open several with `open_document`/`file.new`, address each with `"doc"` (`list_documents` enumerates), close with `file.closeDocument {id, force?}`. A second window on one document is a desktop-only view, not a second document — do not expect `doc` ids to change when `view.newWindow` runs.
- **Clean up text with the paragraph tools** instead of retyping: `para.removeExtraSpaces`, `para.removeBlank`, `para.convertBreaks`, `para.spacesToIndent` and the rest take `{"scope": "all"}` and run as one undo step, preserving tracked changes.
- **Prepare inputs**: write Markdown/HTML/CSV/text in the shell and bring it in (`open_document`, `insert.textFromFile`, `mailings.recipients` for `.csv/.tsv/.txt` with encoding detection and `.xlsx/.xlsm/.xls/.ods`, `insert.picture` with a path or base64 bytes).
- **Produce deliverables**: convert/export to PDF/ODT/RTF/HTML/MD/tex/txt/PNG from the CLI (docx and pdf in one `run --script`), insert a filled table in one MCP call with `insert_table`, impose n-up sheets or booklets with `pagesPerSheet`, and hand the `.docx` on for Word.
- **Attribute your edits**: pass `--author "Claude (copyedit)"` (or `file.setAuthor`) so reviewers can tell agent edits from people's, and turn tracking on explicitly with `review.trackChanges {"value": true}`. Under Restrict Editing the author cannot be changed and most `file.*` commands are refused — do not try to work around it.
- **Confine yourself**: run the headless MCP server with `--automation-read-root`/`--automation-write-root` (a missing root grants none of that access; the roots must exist). This also bounds the personal-templates folder.
- **Repair/interpret native projects**: the native format is `.docx` itself; `.json` is the engine's own model (media bytes and opaque parts included as base64). Recovery snapshots are per-document versioned JSON under `recovery/`, taken at most every ten seconds; the newest edits can be lost.
- **Check fonts before blaming layout**: `font.missing {}` lists the fonts the document asks for that are not installed; a `metricCompatible` substitute keeps line breaks, anything else can move pages. The same fonts decide what a strict export can draw.
- **Do not**: drive the GUI blind by clicking at guessed coordinates — prefer commands; assume SVG/ICO/HEIC images load (they don't); assume `.doc` can be written (it can't); assume MHT can be saved (it can't); assume charts, SmartArt, OLE or native ink *from Word* can be edited (they are preserved through saves, not editable); assume `.docx` fidelity on real-world files (gap #1); assume a headless session writes recovery copies (it doesn't); call `ui.saveAsTemplate` headlessly (it opens a system dialog); expect `view.arrangeAll`/`view.sideBySide`/`view.syncScroll` to work headlessly (they need native windows).
- **Watch these footguns**: `file.saveTemplate` appends `.dotx` (`out.docx` → `out.docx.dotx`); `file.new {"template": "MyTemplate"}` silently gives a blank document — use `file.newFromTemplate {"path"}`; `file.listTemplates` without `dir` errors when no folder is saved; `review.trackChanges` without `value` *toggles* (it can turn tracking off in a document saved with it on); `format.highlight` without `color` toggles; `file.close`/`file.closeDocument` error on unsaved changes unless `{"force": true}` (which discards them); `ui.key`/`ui.text` replies `{"queued": true}` before the edit has been applied — inspect document/widget state before the next dependent step; a `mcp --connect` bridge that starts first reports "not reachable … will retry on each call" until the app's port opens; after an `outcome unknown` from the bridge or the control channel, re-running a mutation may apply it twice; `strict` on any target other than PDF/PNG is a parameter error, not a promise.

## Verification protocol

Alpha software that never crashes by design but is unproven on real-world files: trust nothing you did not re-open.

1. **Throwaway round-trip first**: new → type/format → save `.docx` → reopen → export `.pdf`, all in a scratch directory (`wordcraft-cli run --template blank --cmd … --save t.docx`, then `wordcraft-cli convert t.docx t.pdf`, then `wordcraft-cli inspect t.docx`). Repeat the round trip in `.odt` when ODT is the deliverable — its fidelity is good but self-estimated, not measured.
2. **Never trust a silent export**: the CLI prints `wrote <path>` only after the command returned Ok, and a failing command writes nothing; still check the file exists, is non-zero, and re-read it. For PDF/PNG deliverables, run `--strict` (exit 3) or `file.strictReport` and act on the report; a pass is not proof of layout fidelity.
3. **Compare structure, not just text**: `inspect`/`document.inspect` shows styles, tables, sections — use it to catch silent loss (the known failure mode is content dropped without a warning; gap #1).
4. **Keep the user's original untouched**: work on a copy; WordCraft's save replaces the file in place (safely, but in place). Recovery copies exist for the desktop app only, are unencrypted, and the newest edits before a crash can be lost.
5. **Version and back up** project files per session; update the app only between projects (the launcher auto-updates; the version you script against may change — this skill was measured on v0.18.1).
6. **Re-check the command set you script against**: re-read `wordcraft-cli commands --json` on the installed build and look for the ids you call; the repo's documentation counts drift for months (README still says 422 commands vs 671 in code).

## Sources & evidence

- Repo: https://github.com/storytold/wordcraft (org `storytold`), inspected read-only at **tag `v0.18.1`**, commit **`079f478bd85df7bcc567e3bafa7d7219096f9c3c`** ("Merge tested main for v0.18.1", 2026-11-11), audited **2026-11-12**; the `v0.16.0` tag object was used for set diffs. The installed bundle matches the tag.
- Installed app: `/Applications/WordCraft.app` — 0.18.1, bundle id `ai.storyteller.wordcraft`; its binary prints `wordcraft 0.18.1 (079f478b)` (verified with `--version` and `--help`; the GUI was never launched, and `wordcraft-cli` is not in the bundle). If your installed version differs, verify against it.
- Key files read: README.md, ROADMAP.md, Cargo.toml, AGENTS.md, craft-i18n.rev, docs/{gaps,file-format-parity,mcp,control-protocol,recovery,zotero,parity-checklist,ui-parity,testing}.md, apps/wordcraft/src/{main.rs,control_server.rs}, apps/wordcraft-cli/src/{main.rs,script.rs,automation_args.rs}, apps/wordcraft-web/src/{main.rs,host.rs,api.rs}, crates/engine/src/{io.rs,catalog.rs,session.rs,strict.rs,file_access.rs}, crates/engine/src/cmd/ (mod, file, tools/specs, tools/actions, tools/compare, user_templates, font, format, canvas, smart_art, view, text/delete, para, para/tools, mailings, protect, table, references, fields), crates/engine/src/recovery/desktop.rs, crates/engine/tests/{strict_export,strict_pictures}.rs, apps/wordcraft-cli/tests/it/strict.rs, crates/docx/src/{crypt.rs,units.rs,wordml2003.rs}, crates/docx/tests/it/{strict_drawings,picture_links,line_numbering}.rs, crates/docbin/src/{lib,crypt}.rs, crates/formats/src/{rtf,mht,latex,markdown,sheet}.rs, crates/formats/src/rtf/, crates/formats/src/odt/, crates/mcp/src/{tools,server,backend}.rs, crates/ui-egui/src/{windows,control,control/handler,dialogs,printing,print_page,i18n,language_packs,ribbon/language,documents}.rs, crates/ui-egui/src/windows/arrange.rs, crates/ui-egui/src/dialogs/dialogs_insert/date_time.rs, crates/ui-egui/examples/ui_shot.rs, crates/pdf/src/imposition.rs, crates/doc/src/{document.rs,missing.rs}, crates/layout/src/{strict,missing}.rs, crates/control-key/src/lib.rs, crates/zotero/, xtask/src/main.rs.
- Counts were re-measured from this tag's code and the installed `--version`/`--help` on 2026-11-12; the method for each is in `evidence.md`. Sets that did not move are marked "unchanged at v0.18.1" in the table; the sets that moved with the code are named there (shortcuts 166 → 167 `.key()` sites, dialogs 91 → 92, missing catalog features 15/14 → 12/11), and HTML fidelity was refreshed from the repo's own table (60% → 65%).
- Nothing was built or launched; the clone and the installed bundle were only read/version-checked. Where the repo contradicts itself (command counts, dialog count, shortcut count, catalog coverage, gap #1) the contradiction is stated in place rather than resolved by guesswork.
