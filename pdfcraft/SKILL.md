---
name: pdfcraft
description: PdfCraft is the ArtCraft PDF workbench, a clean-room Acrobat Pro reimplementation for macOS, Windows, Linux, FreeBSD and the web. Use this skill whenever the user mentions PdfCraft or pdfcraft-cli, asks what it can do, which file formats or shortcuts it supports, or asks to read, render, search, organize, combine, split, rotate, annotate, fill, calculate, sign, redact, OCR, compare, print, protect, layer, measure, prepress or convert PDFs (including Word/Excel/PowerPoint to PDF and PDF to Word); when preparing assets or inputs for it; when driving it headlessly through the CLI, the MCP server or the UI control channel; or when verifying, repairing or troubleshooting its output — even if the app is not named (for example "merge these PDFs", "make this scan searchable", "fix this form's calculation order", "redact this contract", "convert this PDF to Word", "fix these hairlines").
---

**Audit basis.** Refreshed 2026-11-12 against tag **v0.21.1**, commit **`b503b2e62dfeec5598f344e4e287d9c9cbdb34fa`** — `git rev-parse HEAD` in the pinned checkout confirms, and the installed bundle matches (its binary prints `pdfcraft 0.21.1`). The previous release this skill described was v0.19.0 (`8c572792d6760bdc903d6f9a032e3e38e8f71cb8`).

**v0.19.0 → v0.21.1 delta.** 872 files changed (`git diff --shortstat v0.19.0..HEAD`, +165,335 / −11,319; the round's compare reports 1,957 commits and caps its file list at 300). Automation: **208** tools (195; +13, none removed) and **221** registry commands (214; +7). New surfaces: **prepress** — `doc_fix_hairlines`, `doc_convert_colours`, `doc_printer_marks` and `printer_papers`, commands `prepress.hairlines` / `convert_colors` / `marks` / `marks.remove` (`crates/edit/src/{hairlines,convert_colours,printer_marks}.rs`); **editing** — `text_replace` (find/replace inside paragraphs, `edit.replace`), `text_prepare` (text inside supported Form XObjects made editable) and `object_copy`/`object_paste` (page objects plus their resources, within or between documents) (`crates/engine/src/{find_replace,rich_copy,object_clip}.rs`); **Office import** — 28 Word/Excel/PowerPoint/OpenDocument/RTF extensions through an installed LibreOffice (`crates/create/src/office.rs`), used by File ▸ Open, `doc_combine` and `doc_create_multiple`, but not by `doc_open` or the GUI's Combine/Insert/Create Multiple frame-thread paths; **UI** — split view (`view.split`, ⌘\) and documents that hide their own chrome (`/HideToolbar`, `/HideMenubar`, `/HideWindowUI`) with `view.toggle_interface` (F8), a portfolio's file list with its `/D` document first, full-screen page transitions and display times (`crates/ui-egui/src/canvas/presenter.rs`), and `--combine`; **forms/XFA** — `form_focus`, `js_event`, a custom stamp's `line`, comment pop-ups, attachment descriptions, and XFA prototypes/traversal/linked images/table rows/master-page fields/template properties; **protect/optimize** — a redaction `regex` with checksum `validate`, optimizer discards (search index, external refs, form actions) and `target_bytes`; **print** — 23 paper presets and CUPS landscape sheets (`crates/print/src/sheets.rs`); **web** — an in-page `window.pdfcraft` API with `?control` and a Web Worker OCR build. Control methods stay 17; the CLI stays 14 documented subcommands + `check-one`; convertible inputs stay 13.

**Verify against your installed version** — the ArtCraft Launcher auto-updates, so a newer build may differ; every count quoted here was re-measured at this tag, and code paths that moved were re-cited. The measurement method for each count is in `evidence.md`.

**v0.18.1 → v0.19.0 delta (previous round).** 375 files changed. Automation: **195** tools (184 at v0.18.1; +`bookmark_copy`, `bookmark_export`, `bookmark_import`, `comments_copy`, `comments_paste`, `model_add`, `model_render`, `ocr_dictionary`, `ocr_review_apply`, `ocr_words`, `page_enhance_scan`, none removed) and **214** registry commands (210; +`comment.copy`, `comment.paste`, `ocr.correct`, `ocr.enhance`). That round added 3D models (U3D/PRC annotation with a poster; PRC→PNG), bookmark tree export/import/copy, comment copy/paste between documents, PCX input, IBAN redaction, a second OCR engine with review/dictionary/confidence, in-place scan enhancement, and a new file identifier for redacted or sanitized copies.

## Overview

PdfCraft is an open-source, pure-Rust PDF reader and editor ("The PDF workbench; an open-source, modern PDF reader and editor", `README.md`), built clean-room with Adobe Acrobat Pro as the documented parity target (`docs/target-app-parity.md`). It is **alpha** (README: 57% of its tracked Acrobat features, 94% of core essentials, about 55% ready for everyday work) and runs on macOS, Windows, Linux and FreeBSD plus a WebAssembly shell (`apps/pdfcraft-web`, `docs/architecture.md`). Source: GitHub storytold/pdfcraft. The UI is egui 0.37, with side panels on craft-ui task panes, craft-ui ComboBoxes and native macOS menus from craft-menu.

The PDF object graph is the document model: there is no separate project file, so the `.pdf` **is** the project (`docs/architecture.md` §Data model and editing). Pages are drawn by the vendored `hayro` 0.7.x family while PdfCraft's own renderer is built (`docs/gaps.md` gap 2; `vendor/README.md`), so rendering is good but not Acrobat-measured. The round's changes concentrate on XFA layout/scripting depth, form and redaction hardening, prepress tools, Office import through LibreOffice, and the split-view/portfolio interface work. Every capability below is grounded in the code at v0.21.1; where a claim is only promised by a doc it says **claimed but unverified**, and the key files are listed under Sources.

## Capabilities (verified)

Unless a bullet says **partial**, the path is wired into the UI and/or the CLI at this tag. If your installed version differs, run the bundle's `Contents/MacOS/PdfCraft --version` and `pdfcraft-cli tools` before trusting flags or tool names. Tool names live in `crates/automation/src/tools.rs`; command ids in `crates/engine/src/commands.rs`; UI panels and dialogs are under `crates/ui-egui/src`.

### Automation surface at a glance

| Surface | Count at v0.21.1 | Change vs the v0.19.0 skill |
|---|---|---|
| Automation tools (`crates/automation/src/tools.rs`) | **208** (208 top-level `t(` declarations) | **+13** (listed in the delta above); 0 removed |
| Command registry (`crates/engine/src/commands.rs:167` `COMMANDS`) | **221** | **+7** (`edit.replace`, `prepress.*` ×4, `view.split`, `view.toggle_interface`); 0 removed |
| Tools carrying a command id (`ToolDef::command`) | **104** tools, **77** distinct ids, **75** of them registry ids | 99 / 73 / 71 at v0.19.0 |
| CLI subcommands (`apps/pdfcraft-cli/src/main.rs`) | **14 documented**, plus internal `check-one`; **34** `--flag` names | unchanged at v0.21.1 (zero diff in that file) |
| UI control methods (`crates/ui-egui/src/control/requests.rs`) | **17** | unchanged at v0.21.1; corrected set: `ui.panel`, not `ui.dock` |
| Launch view/preference keys (`PdfCraftApp::set_option`) | **58** | corrected: the old text said 46 |
| Interface languages | no in-tree count | unchanged at v0.21.1: `crates/ui-egui/src/i18n/` holds only `crates/ui-egui/src/i18n/tests.rs`; catalogs come from the `craft-i18n` pin in `craft-i18n.rev` |
| All tools catalogue (`crates/engine/src/catalog.rs:75`) | **152 entries** (149 `item` + 3 `menu_item`) in **23 groups**, **29 sections**; 21 entries and 5 whole groups are planned | totals unchanged at v0.21.1; **planned entries 24 → 21** (Convert colors, Add printer marks and Fix hairlines became ready) |
| MCP tools | the same **208**, or 17 entries under `--compact` (15 core + `tool_search` + `tool_call`) | +13 |
| MCP resources | 4 URI templates + 2 list resources | unchanged at v0.21.1; 16 MiB request-line cap |
| Convertible input extensions (`CONVERTIBLE`, `crates/create/src/lib.rs:779`) | **13** | unchanged at v0.21.1 |
| Office import extensions (`OFFICE_EXTENSIONS`, `crates/create/src/office.rs`) | **28** (Word/Excel/PowerPoint/OpenDocument/RTF) through an installed LibreOffice | **new** |
| Office export targets (`OfficeFormat::from_extension`, `crates/engine/src/compare.rs:180`) | **5** kinds / 7 extensions (`docx`, `pptx`, `html`/`htm`, `rtf`, `md`/`markdown`) | unchanged at v0.21.1 |
| Form-data extensions (`crates/xfdf/src/lib.rs:75`) | **8** extensions → 6 formats | unchanged at v0.21.1 |
| Redaction patterns (`crates/redact/src/patterns.rs:17`) | **6** (phone, email, credit card, SSN, date, IBAN) + a custom `regex` with `validate` | patterns unchanged; regex **new** |
| Page-image export formats | **3** (png, jpeg, tiff; `pdfcraft-cli render` also writes `.pam`) | unchanged at v0.21.1; exported on worker threads |
| Print paper presets (`PAPERS`, `crates/print/src/settings.rs:233`) | **23** | **+2** (was 21) |

`pdfcraft-cli tools` is the live capability contract; the full name/title/hint table is in `references/automation-tools.md`. Every tool has a JSON Schema, read-only or destructive hints and an optional registry command id. Repo docs lag badly: `docs/target-app-parity.md` and `docs/ui-parity.md` still say "141 automation tools" and "184 registered commands" (real at v0.21.1: **208** tools / **221** registered commands).

### Reading, navigation and text
- Tiled CPU rendering with single, continuous, two-up and two-page layouts, rotation, full screen, Read mode, light/dark/system themes and per-tab history. Optional gapless page display and an independent thumbnail slider. **New at v0.21.1:** full screen plays a page's transition (`/Trans`) and advances on its display time (`/Dur`), bounded and stopped by leaving full screen (`crates/ui-egui/src/canvas/presenter.rs`).
- **Split view:** the current document in two panes, to the right or below, or any tab split from its tab menu (`view.split`, ⌘\; `crates/ui-egui/src/panes.rs`). One document can show in both panes with shared edits and undo but independent scroll, zoom and selection.
- Documents that hide their own chrome (`/HideToolbar`, `/HideMenubar`, `/HideWindowUI`, ISO 32000-2 Table 147) open that way; `view.toggle_interface` (F8) brings the interface back for that tab (`crates/ui-egui/src/viewer_prefs.rs`).
- Reading-order text extraction (columns, RTL runs, vertical CJK), find-as-you-type, text selection and permission-aware copy. `pdfcraft-cli text` refuses text from a document that forbids copying unless the owner password is supplied.
- Bookmarks (nested, searchable, with colour and bold/italic), page thumbnails, page labels, transitions, word/character counts, layers, attachments, reading colours and the document's initial view. The bookmark tree exports to and imports from JSON (`bookmark_export`, `bookmark_import`; `crates/organize/src/outline_io.rs`) and copies from another document by page number (`bookmark_copy`).
- **Portfolios:** a PDF portfolio opens its `/D` document first and shows its file list in the tab, in place of the cover sheet; `/View /H` keeps the list hidden (`crates/ui-egui/src/app/files.rs:564-587`). `doc_info` reports `portfolio.initial` (the presented attachment's name) and `portfolio.view` (`crates/automation/src/json.rs:351`); the attachments themselves are still not extractable by any tool.
- Open parameters: a path such as `manual.pdf#page=12`, `#nameddest=Intro` or `#Intro` opens the file and applies the destination; other Adobe parameters are ignored (`crates/engine/src/open_parameters.rs`; `doc_open` reports `destination`).
- Reopening a file can restore the page, zoom and page display it was last shown with (desktop only, 100 files; `crates/ui-egui/src/persist/last_view.rs`).
- PDF 1.0–2.0, repair of damaged files with the repairs reported. Whole-file operation: no lazy disk read yet.

### Page organization, combine, split, create
- Rotate, reverse, delete, move, duplicate, replace, extract, insert blank/file pages, crop/boxes, page labels, transitions. Page copy/cut/paste exist only as commands.
- A **Page tools menu** in the Pages panel.
- Combine with one bookmark per file, carrying links, named destinations, form fields, layer defaults, attachments and nested bookmarks; split by page count, before pages, top-level bookmarks or maximum size.
- Create PDFs from blank pages, images (PNG/JPEG/TIFF including multi-page and BigTIFF, GIF, BMP, JPEG 2000, PCX) and `.txt`/`.text` — 13 extensions (`CONVERTIBLE`, `crates/create/src/lib.rs`); **partial** for text: WinAnsi plus Latin/Greek/Cyrillic the bundled Inter face covers, while CJK, Arabic, Hebrew and Indic text is refused (`crates/create/src/text_font.rs`).
- **Office import (new at v0.21.1):** 28 Word/Excel/PowerPoint/OpenDocument/RTF extensions convert to PDF through an installed LibreOffice (`OFFICE_EXTENSIONS`, `crates/create/src/office.rs`). File ▸ Open converts in a background worker (`crates/ui-egui/src/platform/open_worker.rs:224`); `doc_combine` and `doc_create_multiple` convert headlessly. `doc_open` still opens PDFs only, and the GUI's Combine, Insert Pages and Create Multiple refuse an Office file on the frame thread (`crates/ui-egui/src/workflows/combine_ui/parts.rs:42`, `crates/ui-egui/src/workflows/create_multiple_ui.rs:46`, `crates/ui-egui/src/workflows/files.rs:669`). **Partial:** no HTML, web-page, PostScript or EPS import; the converter needs LibreOffice and is not network-sandboxed (gap 8, `docs/gaps.md`).
- Compare two documents: text diff plus optional visual-region diff, PDF report, or differences added as comments. The engine has page-scoped calls (`compare_pages`, `compare_report_of`, `mark_differences_of` in `crates/engine/src/compare.rs`) that no tool argument exposes yet. **Partial:** no filters for images/annotations/formatting, no page ranges, no scanned-document support.
- Action Wizard: list built-in actions/steps and run an action or a custom step list over many files. No action creation UI.

### Comments, bookmarks, forms, layers, attachments
- **20** `comment_add` types (unchanged at v0.21.1); replies, review status, locking and summarization; flattening is `doc_flatten`. Comment threads resolve through each reply's `/IRT`; `comment_list` reports per-reply status and the displayed rectangle; `comment_*` refuse a shared `id`. Comments copy between documents as XFDF (`comments_copy`/`comments_paste`) and a pop-up can be opened, closed or moved (`comment_popup`, new at v0.21.1).
- Custom stamps can now carry a fill-in `line` under the picture with `{name}`, `{date}` and `{time}`, as a dynamic stamp (`stamp_custom`'s new `line` argument).
- AcroForm listing, filling with regenerated appearances, field creation, properties, tab order, calculations and field JavaScript, automatic detection, data import/export; dotted field names create parent hierarchies. `form_focus` (new) runs a field's enter/exit scripts and `js_event` (new) runs a widget's pointer/focus scripts. With NeedAppearances, check boxes and radio buttons draw their `/MK` caption.
- **XFA (much deeper at v0.21.1):** prototypes (`use`/`usehref`) are resolved before parsing, a subform without a height is as tall as its content, flowed rows and subform sets lay out as their container says, a table row starts at its minimum height and splits at page breaks, a master-page field keeps its own value per page, a linked picture is drawn from the `XFAImages` name tree, a dynamic form runs all opening scripts and lays out once, and XFA 3.3 template properties are readable from scripts (`crates/xfa/src/{proto,traverse,linked_images}.rs`, `crates/js/src/xfa/props.rs`). **Partial:** full XFA layout, scripting and flattening remain incomplete; `xfa_to_static` flattens a form to a static one and drops its scripts.
- Form calculation order with `reads`/`issues` and set/move/`fix`; text-field tables 1–100 × 1–50 with per-column name patterns. `form_calculation_order fix=true` cannot repair a formula `cycle`; a formula has to change.
- Document-level attachments can be added, deleted and have their description edited (`attachment_add`, `attachment_delete`, `attachment_edit`); an attachment row opens on a double-click and has a right-click menu. Still **no tool extracts an attachment**.
- Layers: `layer_set` is a view setting — `page_render` draws with it, the file never changes. Fill & Sign without prepared fields.
- **3D models:** `model_add` embeds a U3D or PRC file (recognised by its first bytes) as a 3D annotation in a rectangle, with a poster taken from a PDF page or an image; `model_render` draws a page's **PRC** model to PNG with headlight shading and can now choose a named view or orbit/turn/zoom/pan it (`crates/prc`, `crates/prc-render/src/nav/`). **Partial:** U3D cannot be drawn, and no tool reads a model's measurements or activates it in a viewer.
- Links, JavaScript: `link_*`, `js_run`, `js_document_scripts`, `js_set_document_script`, `form_set_script`, `js_event`; `doc_flatten` bakes appearances in. Document actions `Open`, `WillSave` and `WillPrint` run in the host, with unasked scripts limited to highlight/zoom/focus/page requests (`crates/engine/src/js.rs`); the other document triggers are not implemented.

### Protect, redact, sanitize, standards
- Standard security handler R2–R6: RC4-40/128, AES-128/256, user/owner passwords with SASLprep, permissions, re-encryption on save. No certificate (public-key) encryption.
- Redaction by rectangle, text find, word list, pattern, **custom regular expression** (Rust regex syntax, at most 1024 bytes, optional `luhn`/`mod97`/`iban` checksum validation; `crates/redact/src/user_regex.rs`) or whole pages, with FOIA/Privacy Act overlay codes. Applying removes text, images, vectors, comments and form fields under the marks and runs a verification pass. Confidential vector paths behind clipping are not retained, and unused Type 3 glyph programs and fonts are unlinked, on redaction.
- Faux-redaction audit finds text still extractable under painted boxes; paint-order and colour-aware, fails closed on unreadable content, honours the copy permission, budgeted. A redacted or sanitized copy gets a **new file identifier** so it is a different file from its source (`crates/redact/src/lib.rs`, ISO 32000-2 §14.4).
- Remove hidden information / Sanitize, with categories listed first. `standards_remove_id` strips PDF/A or PDF/X identification.
- Printing obeys document permissions; low-quality-only printing rasterizes at ≤150 dpi.

### Signatures
- Sign with `.p12`/`.pfx` digital IDs, macOS Keychain identities or the Windows certificate store; PAdES B-B, SHA-256; certification signatures; visible signatures; self-signed ID creation; trust list; validation including changes made after signing.
- Validation checks embedded RFC 3161 timestamp tokens and offline CRL/OCSP evidence with a DSS for PAdES B-LT. **Partial:** no timestamp-server setting and no online fetching; engine-only TSA APIs. No PKCS #11/smart cards on macOS/Linux, no OS trust store, no signing in the browser.

### OCR, print, export, optimize, accessibility, measuring, editing
- OCR adds an invisible searchable text layer or, with `output_mode: editable`, a visible editable one (`crates/ocr/README.md`); batch recognition, camera-photo straightening, preprocessing, per-word confidence bands and a review loop — `ocr_words` lists each word with confidence, band and suspect flag, `ocr_review_apply` applies corrections as one undoable step, `ocr_dictionary` keeps per-language word lists. Two engines behind one trait: the pure-Rust `ocrs` (default, `en` only, ONNX models fetched by packaging) and an optional external `tesseract` process, chosen with `engine` and merged with `strategy` (`primary`, `confidence`, `rover`) (`crates/ocr/src/{ocrs,tesseract}.rs`); recognition can be limited to a rectangle (`region`) or forced over pages that already have text (`force_ocr`). **Partial:** the tool's `language` enum is still `["en"]` (built from `crates/ocr/src/ocrs.rs:32` `LANGUAGES`), so Tesseract's allow-listed codes are not reachable headlessly.
- Print with Acrobat-style options — ranges, odd/even, reverse, fit/actual/shrink/custom, multiple/cut-stack, booklet, poster, **23 paper presets**, copies, duplex, grayscale, CUPS driver options, "print as image", or write a print-ready PDF. The chosen paper is sent to the spooler as its `media`; `printer_papers` lists a driver's own sizes and default, and a **landscape sheet stays landscape on CUPS** (`crates/print/src/sheets.rs`, `crates/print/src/settings.rs`).
- Export pages as PNG/JPEG/TIFF (on worker threads), all embedded images, reading-order text, Word `.docx`, PowerPoint `.pptx`, HTML, RTF or Markdown (`.md`/`.markdown` — `OfficeFormat::from_extension`) (**partial** for Office — basic/lossy; HTML has a rich default and a `simple` CSS-free mode). Images exported keep soft-mask Decode opacity ranges; JPEG 2000, Separation and over-budget images are listed under `skipped`.
- Reduce File Size and the PDF Optimizer with `compatibility`, `object_streams`, `lzw_to_flate`, image downsampling/compression, `target_bytes`, and **new** discards: embedded search index, links to other documents (`GoToR`/`GoToE`/`Launch`/`ImportData`), and form submit/import/reset actions (`crates/optimize/src/{external_refs,form_actions}.rs`). Signed documents are refused.
- **Prepress (new at v0.21.1, partial):** `doc_fix_hairlines` gives strokes narrower than a threshold a width; `doc_convert_colours` rewrites colour operators to gray/RGB/CMYK by device formulas (no ICC profile and no output intent; it reports `loses_conformance`); `doc_printer_marks` adds trim/bleed marks, registration targets, colour bars and a page-information line outside the trim box, and widens the page when needed (`crates/edit/src/{hairlines,convert_colours,printer_marks}.rs`). Output preview, separations, overprint, ink manager, flattener preview and colour-management settings are still absent.
- PDF/A-2b and PDF/A-3b verification and conversion; **partial** (structural rules only). No Preflight panel, no PDF/UA or PDF/X verification, and no CMYK output intent.
- Accessibility Checker with 32 rules in 7 categories (unchanged at v0.21.1), HTML report, alt text, tag property edits, text-only auto-tagging and a new **layout table → blocks** conversion (`accessibility_layout_table_to_blocks`, `crates/a11y/src/layout_table.rs`).
- Calibrated 2D measurements with CSV export and snapping.
- Edit existing text in place, move mixed objects, edit images and added content, import an openly licensed TTF/OTF. **New at v0.21.1:** `text_replace` rewrites a match inside its paragraph, keeping fonts/sizes/colours and rewrapping (it reports what it skipped: spans, scanned text, missing glyphs, non-editable text); `text_prepare` makes grouped text inside supported Form XObjects editable on one page; `object_copy`/`object_paste` copy page objects and their resources within or between documents (`crates/engine/src/{find_replace,rich_copy}.rs`).
- Headers/footers with Bates numbering, watermarks and backgrounds; `doc_remove_marks` removes header/footer, watermark, background or printer marks. Dotted day-first dates are accepted.
- Document properties: title/author/subject/keywords plus custom properties through `doc_set_info`, with XMP kept in step; the Initial View tab reads and writes navigation, layout, magnification, page, window and interface options (`doc_initial_view`).
- **Import fixes:** an imported FDF comment's pop-up is placed on the page; an empty field in imported XFDF clears the field; a luminosity soft mask in a DeviceCMYK group converts per ISO 32000-2 10.4.2; FormCalc `Round` no longer overflows to infinity and AFNumber does not print "inf"; FormCalc url Decode rejects `+` as a hex digit.

### Platform, interface and packaging
- Native macOS/Windows/Linux/FreeBSD app plus a WebAssembly shell; no account, telemetry or cloud processing. Windows installs per-user by default.
- **Interface translations come from pinned `craft-i18n` catalogs** (`craft-i18n.rev` = `575cfdef…`, embedded at build time via `crates/ui-egui/src/i18n.rs`), so no language total is measurable in-tree at v0.21.1. Chinese interface text can still show missing-glyph boxes, Arabic RTL is not qualified end to end, and no help is translated. A missing entry falls back to English instead of failing.
- The macOS `.app` contains only the GUI; the CLI is a separate signed/notarized release asset.
- **Menus come from craft-menu and are native on macOS**; side panels sit on craft-ui task panes and the shared rail; every dropdown is a craft-ui ComboBox.
- **Startup update prompt with direct self-updating.**
- **Web build partial:** browser print dialog, no crash-recovery store, only a subset of fonts embedded. It now exposes an in-page `window.pdfcraft` API over the UI control channel when opened with `?control`, and OCR runs in Web Workers (`apps/pdfcraft-web/src/api.rs`, `apps/pdfcraft-ocr-worker/src/main.rs`); there is no network transport.
- Robustness: one shared decode budget per page walk (256 MiB, 50 000 form entries per page), 16 MiB MCP request lines, bounded audit, bounded Office-export form depth; a saved file keeps its hidden and system attributes on Windows.

## Known limitations and not-implemented

The repo's ranked shortfall list is `docs/gaps.md`; read it before promising anything.

- **Rendering is borrowed and fidelity is unmeasured against Acrobat.** Pages come from vendored `hayro` 0.7.x; the replacement renderer is incomplete. README claims about kerning, colour emoji, blend modes and script coverage are **claimed but unverified** here.
- **Existing-text editing is improved but not general.** `text_replace` works inside editable paragraphs; rotated text, CJK/RTL replacement, lists, superscript/subscript, structure-tag retention and arrange/align remain missing or fragile. `text_replace` can make a longer replacement overlap what follows, unreported; `text_prepare` refuses unsafe transparency, tags or malformed content.
- **Office import exists but is partial and path-dependent.** It needs an installed LibreOffice and desktop builds; `doc_open` does not convert Office files, and the GUI's Combine, Insert Pages and Create Multiple refuse them on the frame thread. There is no HTML, web-page, PostScript or EPS import. Office export is lossy (no `.xlsx`; text/layout fidelity limited).
- **`doc_create` text is not arbitrary Unicode.** It handles WinAnsi plus Latin/Greek/Cyrillic via the bundled Inter face; CJK, Arabic, Hebrew and Indic text is refused. `page_add_text` adds Arabic/Hebrew/Thai when the build has those craft-fonts faces.
- **Headless OCR is English-only.** The tool's `language` enum offers `en` (from `crates/ocr/src/ocrs.rs::LANGUAGES`), so no accents, Cyrillic, Greek, CJK, Arabic, Hebrew or Indic recognition through the CLI or MCP path; the optional Tesseract engine names allow-listed codes in `crates/ocr/src/tesseract.rs` but no surface passes them. Editable-text OCR output exists, but it fails without the models (or, for Tesseract, that binary).
- **Prepress is partial, not Preflight.** Hairlines, device-space colour conversion and printer marks are in; there is no Preflight panel, no ICC profile or output intent, no separations/overprint/ink manager/flattener preview, no output preview, and PDF/A remains 2b/3b structural only. No PDF/X or PDF/UA verification.
- **Signatures:** no PKCS #11/smart cards on macOS/Linux, no timestamp-server setting, no online OCSP/CRL fetching, no OS trust store, no signing in the browser.
- **Attachments are one-way:** `attachment_add`/`attachment_delete`/`attachment_edit` exist, the panel opens/saves them, but no tool extracts an attachment's bytes.
- **Copy/paste is split:** `content_copy` pastes *added* text boxes/images only; `object_copy`/`object_paste` handle page objects and their resources. Neither is a general system clipboard, and `object_copy` refuses text used as a clipping path.
- **Forms:** the wider Acrobat JavaScript object model is incomplete; form submission, barcode fields and rich-text values are missing; only `Open`/`WillSave`/`WillPrint` document actions run; XFA flattening is partial. `form_calculation_order` can report a `cycle` but **cannot fix it**.
- **Compare** has Text/Visual filters but no image/annotation/formatting filters, no page ranges through a tool (the engine has page-scoped calls), and no scanned-document support.
- **No scanners, no GPU page rasterization, no pen pressure, no Read Out Loud.**
- **Preferences are sparse**; the remaining print-production tools (output preview, separations, ink manager, flattener preview, colour management) are absent.
- **Performance:** the whole file is held in memory; file-backed lazy input is blocked on the renderer. Hostile files are bounded, not fast (page-image export is worker-threaded).
- **UI precision:** moving selected objects across pages, rulers/grids/guides and multiple windows are missing; split view is now in.
- **No AI/cloud features**; a local/opt-in provider is planned. Portfolio support is a viewer: the file list and `/D` document are read, but no tool creates or reorganizes a portfolio's collection, and attachments cannot be extracted headlessly.
- **Other PDF gaps:** no certificate encryption, no linearized save, no `.xdp` as a document, no `.sequ` action files; JPEG 2000 and Separation images cannot be exported as images; `model_render` draws PRC only, not U3D.
- **Copy- and print-protected documents:** extraction, copy, compare and OCR text output honour permissions; never bypass.
- **View-only settings do not save:** page gaps, layer visibility and reading colours change the view, not the file.
- **The All tools catalogue is a plan, not a promise, in both directions.**
- **Repo docs lag the code:** several still say 141 automation tools / 184 commands (real at v0.21.1: **208** / **221**), and `docs/gaps.md` gap 18 still calls colour conversion missing. Trust the code and `pdfcraft-cli tools`.

## How to operate

### Launch (macOS)
- App: `PdfCraft.app` as installed by the ArtCraft Launcher (bundle id `ai.storyteller.pdfcraft`, minimum macOS 11.0). The binary is `Contents/MacOS/PdfCraft` inside the bundle.
- `open -a PdfCraft` or `open -a PdfCraft FILE.pdf`; pass flags with `open -a PdfCraft --args --control ~/.pdfcraft-control.json`.
- The bundle's `Contents/MacOS/PdfCraft --version` prints `pdfcraft 0.21.1` and `-h`/`--help` prints usage, both without opening a window.
- Launch parsing: explicit flags are `--version`, `-h`/`--help`, `--control FILE`, `--create-images [images…]`, `--combine files…`, `--two-paged`, `--new-window`; **every other `--key value` is a view/preference key** handed to `set_option` (**58** keys). An unknown key is refused by `set_option` and logged; the app still opens.
- View keys: `--page N`, `--zoom 150`, `--layout single|continuous|two-up|two-page`, `--page-gaps on|off`, `--cover on|off`, `--rotate 0|90|180|270`, `--select <ranges>`, `--find <text>`, `--comment PAGE:INDEX`, `--layer "Name=on|off"`, `--grid-zoom 50..300`, `--thumbnail-zoom 50..150`, `--organize on|off`, `--fields on|off`, `--always-default-view on|off`.
- Panels/mode/tools: `--panel comments|bookmarks|pages|fields|layers|attachments|signatures|accessibility|tags|search|compare|none`, `--mode all|read|edit|convert|sign`, `--tool <catalogue id>`, `--quick <quick tool>`, `--tools full|expanded|collapsed`, `--tools-side left|right`, `--palette <query>`, `--dialog properties|security|fonts|custom|…|none`.
- Preferences: `--theme light|dark|system`, `--language auto|<code>`, `--author <name>`, `--date-format …`, `--ui-scale …`, and more; keys are taken verbatim.
- One window, several documents as tabs; split view adds a second pane (`view.split`), and panels can be floated, tab-stacked or split. On Windows and Linux/BSD a launch that only names files hands them to the running instance; `--new-window` starts an independent window.

### Headless CLI (not installed with the app)
`pdfcraft-cli` is a separate signed/notarized asset: `pdfcraft-cli-<version>-macos-universal.zip`. Use the same release as the app where possible; the control protocol is internal and may change between versions.

Documented subcommands: `info`, `render`, `text`, `edit`, `combine`, `extract`, `split`, `check`, `audit`, `batch`, `tools`, `run`, `ui`, `mcp`; the internal `check-one` worker is spawned by `check`.

```sh
pdfcraft-cli info report.pdf          # + declared pdfa/pdfua, output_intents, xfa
pdfcraft-cli text paper.pdf --page 3
pdfcraft-cli render paper.pdf --page 1 --dpi 144 --out p1.png    # .png/.jpg/.tif/.pam
pdfcraft-cli edit in.pdf --rotate 1,2:90 --delete 5 --title "Q3" --out out.pdf
pdfcraft-cli combine a.pdf b.pdf --out combined.pdf
pdfcraft-cli extract report.pdf --pages 1,3,5-8 --out highlights.pdf
pdfcraft-cli split report.pdf --every 10 --out-dir parts/
pdfcraft-cli batch scans --recursive --steps ocr,optimize --out-dir out --root .
pdfcraft-cli tools | jq '.[].name'
pdfcraft-cli run text_find doc=1 query=invoice
pdfcraft-cli run --script steps.json --root ./work --report
pdfcraft-cli audit maybe-redacted.pdf      # exits non-zero on findings
```

A script is a JSON array of `{"tool": "...", "args": {...}}` steps; one session keeps document ids stable (`doc_open` → 1). With `--root DIR` every read/write path must resolve inside DIR. `--report` prints one JSON document with per-step status/result. `doc_open` accepts Adobe open parameters on the path (`#page=12`, `#nameddest=Intro`, `#Intro`).

### MCP (opt-in, stdio, no port)
Add `{"command":"pdfcraft-cli","args":["mcp","--root","work/pdfs"]}` to the agent's MCP config. `--compact` makes `tools/list` return 15 core tools plus `tool_search` and `tool_call` (17 entries); `tools/call` still accepts any of the 208 names. For least privilege use `--automation-read-root` and `--automation-write-root` instead of one broad `--root`. Resources: `pdfcraft://document`, `pdfcraft://commands` and the templates `pdfcraft://doc/{doc}/info`, `…/text`, `…/page/{page}/text`, `…/page/{page}/image{?dpi}`. Request lines over 16 MiB get a JSON-RPC error instead of memory growth.

### UI control channel (opt-in)
Start the app with `--control ~/.pdfcraft-control.json`, then use `pdfcraft-cli ui --control ~/.pdfcraft-control.json …`:
`inspect query=…`, `click label="Organize pages"`, `key key=K modifiers='["command"]'`, `command id=comment.square`, `drag from='[400,300]' to='[600,420]'`, `screenshot --out window.png`, `quit`.
The file holds the loopback port and a random token; the CLI authenticates first and refuses a symlink or a file readable by another user. The app accepts 8 unauthenticated connections at a time, each with 10 s to authenticate. The 17 methods are `ui.state`, `ui.commands`, `ui.command`, `ui.set`, `ui.open`, `ui.inspect`, `ui.click`, `ui.focus`, `ui.resize`, `ui.quit`, `ui.drag`, `ui.move`, `ui.type`, `ui.key`, `ui.screenshot`, `ui.panel`, `ui.dock.reset`. `ui.panel` drives side panels (`panel: tools|side`, `open`, `width`); `ui.dock.reset` resets them. `ui.state.active` reports `page`, `zoom_percent`, `layout`, `page_gaps`, `selected_pages`, `viewport` and `pages_on_screen` rectangles for aiming clicks. `ui.quit` asks the normal Save/Don't save/Cancel prompt and never discards silently.

### Document model, save and export
- The PDF is the document; there is no sidecar project file. Converted images/text/Office files are new unsaved PDFs.
- Edits stay in memory as undo steps; autosave writes a recovery snapshot every 60 s. Encrypted documents stay encrypted on disk.
- Save (`⌘S`) writes an **incremental update appended to the same file**, preserving the original bytes and prior signatures; Save As is a full rewrite; writes are atomic through a staging file. `doc_save` `full: true` forces the rewrite.
- A full rewrite happens where it must: redaction, PDF/A conversion, password change, sanitize, Save As with garbage collection, or print imposition; signed documents are protected from optimizer rewrites.
- Export formats are chosen by extension: images `.png/.jpg/.tif`; Office/HTML `.docx/.pptx/.html/.htm/.rtf/.md/.markdown`; form/comment data `.xfdf/.fdf/.xml/.xdp/.csv/.txt`; text `.txt`; a print job goes to a printer name or a PDF path. Page-image export defaults to 150 dpi and runs on worker threads.

### Panels and keyboard (verified in the command registry)
Panels: comments, bookmarks, pages (with its Page tools menu), fields, layers, attachments, signatures, accessibility, tags, search, compare.

`⌘K` command palette · `⌘F` find / `⇧⌘F` advanced search · `⇧⌘H` replace · `⌘G` / `⇧⌘G` next/previous match · `⌘Z` / `⇧⌘Z` undo/redo · `⌘S` / `⇧⌘S` save / save as · `⌘O` open · `⌘W` close · `⌘P` print · `⌘D` document properties · `⌘J` JavaScript console · `⌘B` add bookmark · `⌘,` preferences · `⌘L` full screen · `⌃⌘H` Read mode · `⌘3` fit visible · `⌘\` split view · `F8` show/hide toolbars and panels · `⌃Tab` next tab · `⌘[` / `⌘]` previous/next view · `⇧⌘N` go to page. On Windows/Linux the command modifier is Ctrl. With a comment selected, arrow keys nudge it one screen pixel.

## Working with an AI agent

**Legitimate work.**
- Prefer the headless tool table over GUI automation. `pdfcraft-cli tools` (or MCP `tools/list`) is the capability contract; `command_list` maps UI commands to tools, and **146 of the 221** registry commands have no tool — check before you promise one.
- Prepare inputs: images and `.txt` for `doc_create`; XFDF/FDF/XML/XDP/CSV for `doc_import_data`; `.p12`/`.pfx` or Keychain/Windows-store identities for signing; openly licensed TTF/OTF for `text_font_import`; document-level attachment files for `attachment_add`; Office documents for `doc_combine`/`doc_create_multiple` (LibreOffice required).
- Inspect and repair: `doc_info` exposes warnings, repairs, portfolio initial/view, page transitions, `open_destination`, fonts and unreadable objects; `doc_revisions` + `doc_open_revision` show what each incremental save appended; `pdfcraft-cli info` tells you which PDF/A or PDF/UA level a file *claims*.
- Verify with independent observations: `page_render`/`render_preview` for pixels, `text_extract` for text, `doc_audit_redactions` after redaction, `pdfa_verify` after PDF/A conversion, `print_readiness` before printing, and external `qpdf`, `pdftotext`, `pdftoppm`, `pdfsig` or a real viewer where installed. Page-image export parallelises, so batch renders finish much faster.
- For UI work, launch with `--control`, use `ui.inspect` to get the accessibility tree, click by unique label or widget id, then `ui.screenshot` to confirm. Never reuse coordinates from an older launch.
- For prepress, check the page size in `doc_info` before and after `doc_printer_marks` (the page can widen), re-render after `doc_fix_hairlines`/`doc_convert_colours`, and re-run `pdfa_verify` after colour conversion: `doc_convert_colours` reports `loses_conformance` and leaves the old PDF/A identification in place — `standards_remove_id` takes that off if the file no longer conforms.

**Must not.**
- Do not drive the GUI blind or assume a deterministic layout across launches.
- Do not assume HTML/PostScript/EPS import, `.xlsx` export, SVG/EPS/PS/JP2 export, PDF/X or PDF/UA verification, or OCR in any language but English.
- Do not call `doc_open` on a Word/Excel/PowerPoint file: it opens PDFs only. Use File ▸ Open, `doc_combine` or `doc_create_multiple`; expect the GUI's Combine/Insert/Create Multiple to refuse Office on the frame thread.
- Do not rewrite signed documents destructively; incremental save keeps signatures valid, but any full rewrite invalidates certification. Keep the original bytes.
- Do not use `doc_create` for CJK, Arabic, Hebrew or Indic text; it will refuse.
- Do not expect a tool to extract an attachment, to copy page objects with `content_copy` (use `object_copy`/`object_paste`), or to persist `layer_set`/page gaps in the PDF.
- Do not expect a timestamp server or PKCS #11 token in the CLI/UI.
- Do not use `form_calculation_order fix=true` to repair a formula `cycle`, or `standards_remove_id` as a compliance fix.
- Do not treat `doc_convert_colours` as a prepress separation: no ICC profile, no output intent, and spot colours are converted rather than kept.
- Do not put the control file in a shared folder or assume the MCP server/control channel is on; both are opt-in and loopback/stdio only.
- Do not assume `pdfcraft-cli` exists on a machine with only the macOS app installed.

## Verification protocol

Alpha-software discipline for every session:
1. **Throwaway round-trip first.** In a scratch folder, open → edit → `doc_save` to a *new* path → reopen with `pdfcraft-cli info`/`text` and in Preview/Acrobat or `qpdf --check`.
2. **Never trust a silent export.** Re-render exported images, re-read exported text, and open `.docx/.pptx` in Word/PowerPoint or LibreOffice before declaring success; Office export is known lossy.
3. **Redaction is not done until audited.** Run `pdfcraft-cli audit` (or `doc_audit_redactions`) on the saved file; the audit fails closed on unreadable content. The redaction hardening reduces what survives, but the audit is still the gate.
4. **Signatures:** after signing, use `sign_list` (and `pdfsig`/OpenSSL if available) on the saved file.
5. **Print and view settings:** before a print job, check `print_readiness` and the document's permissions. Page gaps, layer visibility and reading colours are view state.
6. **Prepress changes need their own check.** After `doc_fix_hairlines` or `doc_convert_colours`, re-render the pages and compare; after `doc_printer_marks`, check the page size in `doc_info` and re-render; after colour conversion, re-run `pdfa_verify` if the file claimed PDF/A.
7. **Office import is a conversion, not a fidelity guarantee.** Compare the page count and re-render the first pages; LibreOffice must be installed, and the converter is not sandboxed.
8. **Backups and versions.** Keep the original PDF before any full rewrite. Check versions before trusting this skill's flags or tools — this edition was measured at v0.21.1 (`pdfcraft 0.21.1`), and a newer launcher update may differ; update apps only between projects.
9. **Hostile or huge files.** Use `pdfcraft-cli check` when a file misbehaves. Bounds are explicit — hitting one is a documented refusal, not corruption. Read `logs/pdfcraft.log` under the user's Application Support/PdfCraft folder for internal errors.

## Sources & evidence

- Repo: https://github.com/storytold/pdfcraft · tag `v0.21.1` · inspected commit `b503b2e62dfeec5598f344e4e287d9c9cbdb34fa` (released 2026-11-12); date of inspection 2026-11-12. The checkout is a shallow clone pinned to the release tag, and it carries the `v0.19.0` tag too, so every id set was diffed between the two tags; it was not modified or built.
- Installed app: `/Applications/PdfCraft.app` 0.21.1, bundle id `ai.storyteller.pdfcraft`, minimum macOS 11.0; its binary prints `pdfcraft 0.21.1`. The GUI was never launched; `--version` and `--help` were run read-only. The macOS bundle contains only `PdfCraft`, not `pdfcraft-cli`.
- Counts were machine-derived from code at this tag and diffed against `v0.19.0`: tools **208** (195; +13, none removed), registry commands **221** (214; +7), control methods 17 = 17, CLI subcommands 14 + internal `check-one` (zero diff), convertible inputs 13, Office import extensions 28, redaction patterns 6 (+ regex), catalogue 152 entries in 23 groups / 29 sections, page-image export 3 formats, form data 8 extensions to 6 formats, print papers 23.
- Key files read: `README.md`, `Cargo.toml`, `craft-i18n.rev`, `docs/gaps.md`, `docs/architecture.md`, `docs/target-app-parity.md`, `docs/mcp.md`, `docs/file-format-parity.md`, `apps/pdfcraft/src/{main,startup}.rs`, `apps/pdfcraft-cli/src/main.rs`, `apps/pdfcraft-web/src/api.rs`, `apps/pdfcraft-ocr-worker/src/main.rs`, `crates/automation/src/{tools,mcp,json,comments,documents,assemble}.rs`, `crates/engine/src/{commands,catalog,compare,find_replace,rich_copy,object_clip,open_parameters,export,js,session/files}.rs`, `crates/create/src/{lib,office,text_font}.rs`, `crates/xfdf/src/lib.rs`, `crates/redact/src/{patterns,user_regex,lib}.rs`, `crates/ocr/src/{lib,ocrs,tesseract}.rs` and `crates/ocr/README.md`, `crates/organize/src/outline_io.rs`, `crates/prc/`, `crates/prc-render/src/nav/`, `crates/ui-egui/src/{panes,viewer_prefs,state}.rs`, `crates/ui-egui/src/canvas/presenter.rs`, `crates/ui-egui/src/app/{control,files}.rs`, `crates/ui-egui/src/control/{requests,host,transport}.rs`, `crates/ui-egui/src/i18n.rs`, `crates/render/src/inspect/{core,model}.rs`, `crates/print/src/{settings,sheets}.rs`, `crates/edit/src/{hairlines,convert_colours,printer_marks}.rs`, `crates/a11y/src/{lib,layout_table}.rs`, `crates/xfa/src/{proto,traverse,linked_images}.rs`, `crates/js/src/xfa/props.rs`, `crates/optimize/src/{external_refs,form_actions}.rs`, `crates/cos/src/budget.rs`, `crates/platform/src/owner_only.rs`, `crates/sign/`, `crates/forms/`, `vendor/README.md`, `parity/acrobat-features.toml`.
- Shared libraries: `storytold/craft-libs` is pinned at `787a7a0f…` for craft-ui, craft-menu, craft-i18n, craft-keymap and craft-quit (`Cargo.toml`); `craft-update` is pinned at `6e03f65b…`. Interface catalogs come from `storytold/craft-i18n` at the commit in `craft-i18n.rev` (`575cfdef…`). craft-menu provides the native macOS menus.
- Companion files: `evidence.md` (claim → evidence → tier table) and `references/automation-tools.md` (all 208 tool names, titles, hints and command mappings, regenerated from `tools()` at this tag).
