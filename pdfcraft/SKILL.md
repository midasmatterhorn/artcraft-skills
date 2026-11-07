---
name: pdfcraft
description: PdfCraft is the ArtCraft PDF workbench, a clean-room Acrobat Pro reimplementation for macOS, Windows, Linux, FreeBSD and the web. Use this skill whenever the user mentions PdfCraft or pdfcraft-cli, asks what it can do, which file formats or shortcuts it supports, or asks to read, render, search, organize, combine, split, rotate, annotate, fill, calculate, sign, redact, OCR, compare, print, protect, layer, measure or convert a PDF; when preparing assets or inputs for it; when driving it headlessly through the CLI, the MCP server or the UI control channel; or when verifying, repairing or troubleshooting its output — even if the app is not named (for example "merge these PDFs", "make this scan searchable", "fix this form's calculation order", "redact this contract", "convert this PDF to Word").
---

**Audit basis.** Refreshed 2026-11-07 against tag **v0.19.0**, commit **`8c572792d6760bdc903d6f9a032e3e38e8f71cb8`** — `git rev-parse HEAD` in the pinned checkout confirms, and the installed bundle matches (its binary prints `pdfcraft 0.19.0`). The previous release this skill described was v0.18.1 (`8bb0528`).

**v0.18.1 → v0.19.0 delta.** 375 files changed. Automation: **195** tools (184 at v0.18.1; +`bookmark_copy`, `bookmark_export`, `bookmark_import`, `comments_copy`, `comments_paste`, `model_add`, `model_render`, `ocr_dictionary`, `ocr_review_apply`, `ocr_words`, `page_enhance_scan`, nothing removed) and **214** registry commands (210 at v0.18.1; +`comment.copy`, `comment.paste`, `ocr.correct`, `ocr.enhance`). New surfaces: **3D models** — `model_add` embeds a U3D or PRC file as a 3D annotation with a poster, `model_render` draws a PRC model to PNG (U3D cannot be drawn); **bookmark trees** export to and import from JSON and copy between documents (`crates/organize/src/outline_io.rs`); **comments copy/paste between documents** (`comments_copy` returns XFDF, `comments_paste` adds it); **PCX** joins the convertible inputs (13 extensions); **IBAN** joins the redaction patterns (6); **OCR** gained a second engine and a review loop (pure-Rust `ocrs` plus an optional external `tesseract` process, ensemble strategies, confidence bands, `ocr_words`/`ocr_review_apply`/`ocr_dictionary`, editable output) and **`page_enhance_scan`** cleans scanned pages in place. Encryption now reads every legal crypt-filter form and full saves keep `/Encrypt`; JBIG2 optimisation encodes only what the decoder takes and shares a symbol dictionary across up to 16 images; a redacted or sanitized copy gets a **new file identifier** (`crates/redact/src/lib.rs:667`, ISO 32000-2 §14.4); compare gained page-scoped engine calls that no tool argument exposes yet.

**Verify against your installed version** — the ArtCraft Launcher auto-updates, so a newer build may differ; every count quoted here was re-measured at this tag, and code paths that moved were re-cited. The measurement method for each count is in `evidence.md`.

**v0.17.0 → v0.18.1 delta (previous round).** 260 files changed. Automation: **184** tools (183 at v0.17.0; the addition is `doc_bates_multi`) and **210** registry commands (205 at v0.17.0), which are the base of the counts above. Wave: rewritten form XObjects keeping `/PCAdded`, structure titles following removed descriptions in redaction, a new document's page tree written once, and a wheel lockup at the edge of non-continuous view. The "35 languages" claim stays dropped: the `.tsv` language catalogs are gone (the `craft-i18n.rev` pin carries them), so no language count is measurable in-tree.

## Overview

PdfCraft is an open-source, pure-Rust PDF reader and editor ("The PDF workbench; an open-source, modern PDF reader and editor", `README.md`), built clean-room with Adobe Acrobat Pro as the documented parity target (`docs/target-app-parity.md`). It is **alpha** (README "What's next": 57% of its tracked Acrobat features, 94% of core essentials, ~55% ready for everyday work) and runs on macOS, Windows, Linux and FreeBSD plus a WebAssembly shell (`apps/pdfcraft-web`, `docs/architecture.md`). Source: GitHub storytold/pdfcraft. The UI migrated to egui 0.37 this release, with side panels on craft-ui task panes, craft-ui ComboBoxes everywhere, and **native macOS menus from craft-menu**.

The PDF object graph is the document model: there is no separate project file, so the `.pdf` **is** the project (`docs/architecture.md` §Data model and editing). Pages are drawn by the vendored `hayro` 0.7.x family while PdfCraft's own renderer is built (`docs/gaps.md` gap 2; `vendor/README.md`), so rendering is good but not Acrobat-measured. v0.15.0 (2026-10-28) kept the engine registry identical to v0.14.0 and spent its budget on XFA form performance and correctness, redaction hardening (F-008/F-011), page-image export on worker threads, a Page tools menu, Persian, and the usual platform refresh.

v0.16.0–0.16.1 changes the automation surface by **+3 tools** and **no engine-command change** (205 `c(` ids at both tags): **`doc_backdrops`**, **`bookmark_from_text_styles`** and **`text_styles`**. Feature highlights: **form calculation order** is first-class — `form_calculation_order` reports each field's calculation (sum/product/average/notations/custom scripts) and `form_set_props` refuses unknown, mistyped or conflicting `calculate`/`validate` keys and notations it could not store as written; **Page properties sets the selected pages' tab order** (#4516); **Import comments copies another PDF's comments onto the same pages** (#4595); **Alt+Left / Alt+Right walk the view history** (#3632); the **window title marks unsaved changes** (#3640); **Export Data as CSV keeps formula-like cells as text** (#2524); reading-colour preferences gained a settings shortcut (#2627); content streams step over a malformed token instead of ending the page; Type1 fonts with an OpenType-wrapped CFF program draw their own face; a moved comment is drawn where it goes while dragged; and CJK viewer fidelity landed exact GBK glyph rasters for installed Chinese families.

## Capabilities (verified)

Unless a bullet says **partial**, the path is wired into the UI and/or the CLI at this tag. If your installed version differs, run the bundle's `Contents/MacOS/PdfCraft --version` and `pdfcraft-cli tools` before trusting flags or tool names. Tool names live in `crates/automation/src/tools.rs`; command ids in `crates/engine/src/commands.rs`; UI panels and dialogs are under `crates/ui-egui/src`.

### Automation surface at a glance

| Surface | Count at v0.19.0 | Change vs the v0.18.1 skill |
|---|---|---|
| Automation tools (`crates/automation/src/tools.rs`) | **195** (unique `t("name"` set, wrapped declarations included) | **+11** (listed in the delta above); 0 removed |
| Command registry (`crates/engine/src/commands.rs:165` `COMMANDS`) | **214** | **+4** (`comment.copy`, `comment.paste`, `ocr.correct`, `ocr.enhance`); 0 removed |
| Tools carrying a command id (`ToolDef::command`) | **99** tools, **73** distinct registry ids | 96 tools / 71 ids at v0.18.1 |
| CLI subcommands (`apps/pdfcraft-cli/src/main.rs`) | **14 documented**, plus internal `check-one`; 25 `--flag` names | unchanged at v0.19.0 (zero diff in that file) |
| UI control methods (`crates/ui-egui/src/control/requests.rs`) | **17** | unchanged at v0.19.0 (identical set) |
| Interface languages | no in-tree count | not measurable: `crates/ui-egui/src/i18n/` holds only `tests.rs`; catalogs come from the `craft-i18n` pin in `craft-i18n.rev` |
| All tools catalogue (`crates/engine/src/catalog.rs:75`) | 150 items, 24 groups, 30 sections; 24 items and 5 groups badged planned | unchanged at v0.19.0 |
| MCP tools | the same **195**, or 17 entries under `--compact` (15 core + `tool_search` + `tool_call`) | +11 |
| MCP resources | 4 URI templates + 2 list resources | unchanged at v0.19.0; 16 MiB request-line cap |
| Convertible input extensions (`CONVERTIBLE`, `crates/create/src/lib.rs`) | **13** | **+`pcx`** |
| Office export targets (`OfficeFormat::from_extension`, `crates/engine/src/compare.rs`) | **5** kinds / 7 extensions (`docx`, `pptx`, `html`/`htm`, `rtf`, `md`/`markdown`) | corrected: Markdown was already there at v0.18.1 |
| Form-data extensions (`crates/xfdf/src/lib.rs`) | **8** extensions → 6 formats | unchanged at v0.19.0 |
| Redaction patterns (`crates/redact/src/patterns.rs`) | **6** (phone, email, credit card, SSN, date, IBAN) | **+`Iban`** |
| Page-image export formats | **3** (png, jpeg, tiff; `pdfcraft-cli render` also writes `.pam`) | unchanged at v0.19.0; exported on worker threads (~80% less wall time) |

`pdfcraft-cli tools` is the live capability contract; the full name/title/hint table is in `references/automation-tools.md`. Every tool has a JSON Schema, read-only or destructive hints and an optional registry command id. Repo docs lag badly: several still say "141 automation tools" and "184 registered commands" (real at v0.19.0: **195** tools / **214** registered commands).

### Reading, navigation and text
- Tiled CPU rendering with single, continuous, two-up and two-page layouts, rotation, full screen, Read mode, light/dark/system themes and per-tab history. Optional gapless page display and an independent thumbnail slider.
- Reading-order text extraction (columns, RTL runs, vertical CJK), find-as-you-type, text selection and permission-aware copy. `pdfcraft-cli text` refuses text from a document that forbids copying unless the owner password is supplied.
- Bookmarks (nested, searchable, with colour and bold/italic), page thumbnails, page labels, transitions, word/character counts, layers, attachments, reading colours and the document's initial view. **New at v0.19.0:** the bookmark tree exports to and imports from JSON (`bookmark_export`, `bookmark_import`; `crates/organize/src/outline_io.rs`) and copies from another document by page number (`bookmark_copy`); a bookmark whose page the target lacks is kept without a destination and listed in `unmapped`. **New (v0.18.1):** Document Properties reads a named opening destination's page, so choosing page 1 replaces it (ISO 32000-2 12.3.2.4, PR #4574).
- Reopening a file can restore the page, zoom and page display it was last shown with (desktop only, 100 files).
- PDF 1.0–2.0, repair of damaged files with the repairs reported. Whole-file operation: no lazy disk read yet.

### Page organization, combine, split, create
- Rotate, reverse, delete, move, duplicate, replace, extract, insert blank/file pages, crop/boxes, page labels, transitions. Page copy/cut/paste exist only as commands.
- **New:** a **Page tools menu in the Pages panel** (PR #4583).
- Combine with one bookmark per file, carrying links, named destinations, form fields, layer defaults, attachments and nested bookmarks; split by page count, before pages, top-level bookmarks or maximum size.
- Create PDFs from blank pages, images (PNG/JPEG/TIFF including multi-page and BigTIFF, GIF, BMP, JPEG 2000, and **PCX** new at v0.19.0) and `.txt`/`.text` — 13 extensions (`CONVERTIBLE`, `crates/create/src/lib.rs`); **partial** for text: WinAnsi only.
- Compare two documents: text diff plus optional visual-region diff, PDF report, or differences added as comments. **New at v0.19.0:** the engine has page-scoped calls (`compare_pages`, `compare_report_of`, `mark_differences_of` in `crates/engine/src/compare.rs`) that no tool argument exposes yet. **Partial:** no filters for images/annotations/formatting, no page ranges, no scanned-document support.
- Action Wizard: list built-in actions/steps and run an action or a custom step list over many files. No action creation UI.

### Comments, bookmarks, forms, layers, attachments
- 19 markup kinds; replies, review status, locking and summarization; flattening is `doc_flatten`. Comment threads resolve through each reply's `/IRT`; `comment_list` reports per-reply status and the displayed rectangle; `comment_*` refuse a shared `id`. **New at v0.19.0:** `comments_copy` returns the chosen comments and their replies as XFDF and `comments_paste` adds them to this or another document under names of their own, so pasting twice gives two sets (`crates/automation/src/comments.rs`; command ids `comment.copy`/`comment.paste`).
- AcroForm listing, filling with regenerated appearances, field creation, properties, tab order, calculations and field JavaScript, automatic detection, data import/export; dotted field names create parent hierarchies. **New:** with NeedAppearances, check boxes and radio buttons draw their `/MK` caption (ISO 32000-2 Table 224, PR #4454).
- **XFA (much faster and more correct at v0.18.1):** a **static XFA form whose data fills thousands of fields opens in seconds** (PR #4638); a laid-out XFA form's **signature fields are named by their SOM path** so other viewers find the signature (PR #4507); a round XFA check box's field highlight is round (PR #4512); XFA image-hash parsing rejects non-hex characters. `xfa_to_static` converts an XFA form to a static form; document-level "PDF container" scripts are skipped from `js_run` while XFA layout is active.
- Form calculation order with `reads`/`issues` and set/move/`fix`; text-field tables 1–100 × 1–50 with per-column name patterns.
- Document-level attachments can be added and deleted headlessly. **New:** an attachment's row opens on a double-click and has a right-click menu (PR #4513). Still **no tool extracts an attachment**.
- Layers: `layer_set` is a view setting — `page_render` draws with it, the file never changes. Fill & Sign without prepared fields.
- **3D models (new at v0.19.0):** `model_add` embeds a U3D or PRC file (recognised by its first bytes) as a 3D annotation in a rectangle, with a poster taken from a PDF page or an image; `model_render` draws a page's **PRC** model to PNG with headlight shading (`crates/prc`, `crates/prc-render`). **Partial:** U3D cannot be drawn, and no tool activates, rotates or measures a model.
- Links, JavaScript: `link_*`, `js_run`, `js_document_scripts`, `js_set_document_script`, `form_set_script`; `doc_flatten` bakes appearances in.

### Protect, redact, sanitize, standards
- Standard security handler R2–R6: RC4-40/128, AES-128/256, user/owner passwords with SASLprep, permissions, re-encryption on save. No certificate (public-key) encryption.
- Redaction by rectangle, text find, word list, pattern or whole pages, with FOIA/Privacy Act overlay codes; applying removes text, images, vectors, comments and form fields under the marks and runs a verification pass. **New hardening (redaction proposals F-008/F-011):** confidential **vector paths behind clipping are no longer retained** after redaction, and **unused Type 3 glyph programs and fonts are unlinked** on redaction (PRs #4577, #4579) — less hidden data survives in the output.
- Faux-redaction audit finds text still extractable under painted boxes; paint-order and colour-aware, fails closed on unreadable content, honours the copy permission, budgeted. **New at v0.19.0:** **IBAN** joins the built-in patterns (phone, email, credit card, SSN, date, IBAN — `crates/redact/src/patterns.rs`), and a redacted or sanitized copy gets a **new file identifier** so it is a different file from its source (`crates/redact/src/lib.rs:667`, ISO 32000-2 §14.4).
- Remove hidden information / Sanitize, with categories listed first. `standards_remove_id` strips PDF/A or PDF/X identification.
- Printing obeys document permissions; low-quality-only printing rasterizes at ≤150 dpi.

### Signatures
- Sign with `.p12`/`.pfx` digital IDs, macOS Keychain identities or the Windows certificate store; PAdES B-B, SHA-256; certification signatures; visible signatures; self-signed ID creation; trust list; validation including changes made after signing.
- Validation checks embedded RFC 3161 timestamp tokens and offline CRL/OCSP evidence with a DSS for PAdES B-LT. **Partial:** no timestamp-server setting and no online fetching; engine-only TSA APIs. No PKCS #11/smart cards on macOS/Linux, no OS trust store.

### OCR, print, export, optimize, accessibility, measuring, editing
- OCR adds an invisible searchable text layer or, with `output_mode: editable`, a visible editable one (`crates/ocr/README.md`); batch recognition, camera-photo straightening, preprocessing, per-word confidence bands and a review loop — `ocr_words` lists each word with confidence, band and suspect flag, `ocr_review_apply` applies corrections as one undoable step, `ocr_dictionary` keeps per-language word lists. **New at v0.19.0:** two engines behind one trait — the pure-Rust `ocrs` (default, `en` only, ONNX models fetched by packaging) and an optional external `tesseract` process, chosen with `engine` and merged with `strategy` (`primary`, `confidence`, `rover`) (`crates/ocr/src/{ocrs,tesseract}.rs`); recognition can be limited to a rectangle (`region`) or forced over pages that already have text (`force_ocr`). **Partial:** the tool's `language` enum is still `["en"]` (built from `crates/ocr/src/ocrs.rs::LANGUAGES`), so Tesseract's 12 allow-listed codes are not reachable headlessly; models or the `tesseract` binary must be installed.
- Print with Acrobat-style options — ranges, odd/even, reverse, fit/actual/shrink/custom, multiple/cut-stack, booklet, poster, 21 paper presets, copies, duplex, grayscale, CUPS driver options, "print as image", or write a print-ready PDF. The chosen paper is sent to the spooler as its `media`.
- Export pages as PNG/JPEG/TIFF (**on worker threads — about 80% less wall time**, PR #5026), all embedded images, reading-order text, Word `.docx`, PowerPoint `.pptx`, HTML, RTF or Markdown (`.md`/`.markdown` — `OfficeFormat::from_extension`) (**partial** for Office — basic/lossy). **New:** Word export keeps an italic run inside its sentence's paragraph (PR #4411). Images exported keep soft-mask Decode opacity ranges; undecodable JPEG 2000/JBIG2/CCITT/Separation images are listed under `skipped`.
- Reduce File Size and the PDF Optimizer with `compatibility`, `object_streams`, `lzw_to_flate`; signed documents are refused.
- PDF/A-2b and PDF/A-3b verification and conversion; **partial** (structural rules only). No PDF/UA or PDF/X verification.
- Accessibility Checker with 32 rules in 7 categories, HTML report, alt text, tag property edits, text-only auto-tagging. **New:** the accessible window is named with the window title (PR #4640).
- Calibrated 2D measurements with CSV export and snapping.
- Edit existing text in place, move mixed objects, edit images and added content, import an openly licensed TTF/OTF. **New:** resizing an image under a shared clip scales its own clip too (PR #4639); a moved text box's drag preview shows the box alone (PR #4475); an added image can be cropped by more than half from one side (PR #4521).
- Headers/footers with Bates numbering, watermarks and backgrounds. **New:** dotted day-first dates in header and footer (PR #4503).
- Document properties: title/author/subject/keywords plus custom properties through `doc_set_info`, with XMP kept in step.
- **Import fixes:** an imported FDF comment's pop-up is placed on the page (PR #4493); an empty field in imported XFDF clears the field, as FDF and XML do (PR #4483); a luminosity soft mask in a DeviceCMYK group converts per ISO 32000-2 10.4.2, so 100% K masks fully (PR #4423); FormCalc `Round` no longer overflows to infinity and AFNumber does not print "inf" for large finite values; FormCalc url Decode rejects `+` as a hex digit.

### Platform, interface and packaging
- Native macOS/Windows/Linux/FreeBSD app plus a WebAssembly shell; no account, telemetry or cloud processing. Windows installs per-user by default now.
- **Interface translations come from pinned `craft-i18n` catalogs** (`craft-i18n.rev` = `575cfdef…`, embedded at build time via `crates/ui-egui/src/i18n.rs`), so no language total is measurable in-tree at v0.19.0. Chinese interface text can still show missing-glyph boxes, Arabic layout is not mirrored, and no help is translated. A missing entry falls back to English instead of failing.
- The macOS `.app` contains only the GUI; the CLI is a separate signed/notarized release asset.
- **Menus come from craft-menu and are native on macOS** (PR #4752); side panels sit on craft-ui task panes and the shared rail (PR #4606); every dropdown is a craft-ui ComboBox.
- **Startup update prompt with direct self-updating** (PR #4654).
- Web build **partial**: browser print dialog, no crash-recovery store, no control-channel transport, only a subset of fonts embedded.
- Robustness: one shared decode budget per page walk (256 MiB, 50 000 form entries per page), 16 MiB MCP request lines, bounded audit, bounded Office-export form depth; a saved file keeps its hidden and system attributes on Windows (PR #4647).

## Known limitations and not-implemented

The repo's ranked shortfall list is `docs/gaps.md`; read it before promising anything.

- **Rendering is borrowed and fidelity is unmeasured against Acrobat.** Pages come from vendored `hayro` 0.7.x; the replacement renderer is incomplete. README claims about kerning, colour emoji, blend modes and script coverage are **claimed but unverified** here.
- **Existing-text editing is improved but not general.** Latin text with an embeddable matching face works; rotated text, CJK/RTL editing, lists, superscript/subscript, structure-tag retention and arrange/align remain missing or fragile.
- **Office import is absent; Office export is lossy.** No Create PDF from Word, Excel, PowerPoint, HTML, web page, PostScript or EPS; no `.xlsx`, `.doc`, SVG, EPS, PostScript or XML-spreadsheet export.
- **`doc_create` text is WinAnsi only**; other characters are refused. `page_add_text` adds Arabic/Hebrew/Thai when the build has those craft-fonts faces.
- **Headless OCR is English-only.** The tool's `language` enum offers `en` (from `crates/ocr/src/ocrs.rs::LANGUAGES`), so no accents, Cyrillic, Greek, CJK, Arabic, Hebrew or Indic recognition through the CLI or MCP path; the optional Tesseract engine names 12 codes in `crates/ocr/src/tesseract.rs` but no surface passes them. Editable-text OCR output exists, but it fails without the models (or, for Tesseract, that binary).
- **No Preflight; PDF/A only 2b/3b and partial.** The PDF/A panel reports the checks it ran, not a conformance verdict. No PDF/X or PDF/UA verification; CMYK documents get no output intent.
- **Signatures:** no PKCS #11/smart cards on macOS/Linux, no timestamp-server setting, no online OCSP/CRL fetching, no OS trust store, no signing in the browser.
- **Attachments are one-way:** `attachment_add`/`attachment_delete` exist, the panel opens/saves them, but no tool extracts an attachment's bytes.
- **`content_copy` is the only paste path and it is headless-only**; it copies *added* content only.
- **Forms:** wider Acrobat JavaScript object model incomplete; document actions, form submission, barcode fields and rich-text values missing; XFA flattening incomplete. `form_calculation_order` can report a `cycle` but **cannot fix it**.
- **Compare** has Text/Visual filters but no image/annotation/formatting filters, no page ranges through a tool (the engine has page-scoped calls), and no scanned-document support.
- **No scanners, no GPU page rasterization, no pen pressure, no Read Out Loud.**
- **Preferences are sparse**; print-production tools (output preview, separations, ink manager, printer marks, colour conversion) are absent.
- **Performance:** the whole file is held in memory; file-backed lazy input is blocked on the renderer. Hostile files are bounded, not fast (page-image export is now worker-threaded).
- **UI precision:** moving selected objects across pages, rulers/grids/guides, multiple windows and split view are missing.
- **No AI/cloud features**; a local/opt-in provider is planned.
- **Other PDF gaps:** no certificate encryption, no linearized save, no portfolio view, no `.xdp` as a document, no `.sequ` action files; JPEG 2000/JBIG2/CCITT/Separation images cannot be exported as images; `model_render` draws PRC only, not U3D.
- **Copy- and print-protected documents:** extraction, copy, compare and OCR text output honour permissions; never bypass.
- **View-only settings do not save:** page gaps, layer visibility and reading colours change the view, not the file.
- **The All tools catalogue is a plan, not a promise, in both directions.**
- **Repo docs lag the code:** several still say 141 automation tools / 184 commands (real at v0.19.0: **195** / **214**). Trust the code and `pdfcraft-cli tools`.

## How to operate

### Launch (macOS)
- App: `PdfCraft.app` as installed by the ArtCraft Launcher (bundle id `ai.storyteller.pdfcraft`, minimum macOS 11.0). The binary is `Contents/MacOS/PdfCraft` inside the bundle.
- `open -a PdfCraft` or `open -a PdfCraft FILE.pdf`; pass flags with `open -a PdfCraft --args --control ~/.pdfcraft-control.json`.
- The bundle's `Contents/MacOS/PdfCraft --version` prints `pdfcraft 0.19.0` and `-h`/`--help` prints usage, both without opening a window.
- Launch parsing: explicit flags are `--version`, `-h`/`--help`, `--control FILE`, `--create-images [images…]`, `--new-window`; **every other `--key value` is a view/preference key** handed to `set_option` (46 keys). Unknown keys fail with a message.
- View keys: `--page N`, `--zoom 150`, `--layout single|continuous|two-up|two-page`, `--page-gaps on|off`, `--cover on|off`, `--rotate 0|90|180|270`, `--select <ranges>`, `--find <text>`, `--comment PAGE:INDEX`, `--layer "Name=on|off"`, `--grid-zoom 50..300`, `--thumbnail-zoom 50..150`, `--organize on|off`, `--fields on|off`, `--always-default-view on|off`.
- Panels/mode/tools: `--panel comments|bookmarks|pages|fields|layers|attachments|signatures|accessibility|tags|search|compare|none`, `--mode all|read|edit|convert|sign`, `--tool <catalogue id>`, `--quick <quick tool>`, `--tools full|expanded|collapsed`, `--tools-side left|right`, `--palette <query>`, `--dialog properties|security|fonts|custom|…|none`.
- Preferences: `--theme light|dark|system`, `--language auto|<code>`, `--author <name>`, `--date-format …`, `--ui-scale …`, and more; keys are taken verbatim.
- One window, several documents as tabs; panels can be floated, tab-stacked or split. On Windows and Linux/BSD a launch that only names files hands them to the running instance; `--new-window` starts an independent window.

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

A script is a JSON array of `{"tool": "...", "args": {...}}` steps; one session keeps document ids stable (`doc_open` → 1). With `--root DIR` every read/write path must resolve inside DIR. `--report` prints one JSON document with per-step status/result.

### MCP (opt-in, stdio, no port)
Add `{"command":"pdfcraft-cli","args":["mcp","--root","work/pdfs"]}` to the agent's MCP config. `--compact` makes `tools/list` return 15 core tools plus `tool_search` and `tool_call` (17 entries); `tools/call` still accepts any of the 195 names. For least privilege use `--automation-read-root` and `--automation-write-root` instead of one broad `--root`. Resources: `pdfcraft://document`, `pdfcraft://commands` and the templates `pdfcraft://doc/{doc}/info`, `…/text`, `…/page/{page}/text`, `…/page/{page}/image{?dpi}`. Request lines over 16 MiB get a JSON-RPC error instead of memory growth.

### UI control channel (opt-in)
Start the app with `--control ~/.pdfcraft-control.json`, then use `pdfcraft-cli ui --control ~/.pdfcraft-control.json …`:
`inspect query=…`, `click label="Organize pages"`, `key key=K modifiers='["command"]'`, `command id=comment.square`, `drag from='[400,300]' to='[600,420]'`, `screenshot --out window.png`, `quit`.
The file holds the loopback port and a random token; the CLI authenticates first and refuses a symlink or a file readable by another user. The app accepts 8 unauthenticated connections at a time, each with 10 s to authenticate. The 17 methods are `ui.state`, `ui.commands`, `ui.command`, `ui.set`, `ui.open`, `ui.inspect`, `ui.click`, `ui.focus`, `ui.resize`, `ui.quit`, `ui.drag`, `ui.move`, `ui.type`, `ui.key`, `ui.screenshot`, `ui.dock`, `ui.dock.reset`. `ui.state.active` reports `page`, `zoom_percent`, `layout`, `page_gaps`, `selected_pages`, `viewport` and `pages_on_screen` rectangles for aiming clicks. `ui.quit` asks the normal Save/Don't save/Cancel prompt and never discards silently.

### Document model, save and export
- The PDF is the document; there is no sidecar project file. Converted images/text are new unsaved PDFs.
- Edits stay in memory as undo steps; autosave writes a recovery snapshot every 60 s. Encrypted documents stay encrypted on disk.
- Save (`⌘S`) writes an **incremental update appended to the same file**, preserving the original bytes and prior signatures; Save As is a full rewrite; writes are atomic through a staging file. `doc_save` `full: true` forces the rewrite.
- A full rewrite happens where it must: redaction, PDF/A conversion, password change, sanitize, Save As with garbage collection, or print imposition; signed documents are protected from optimizer rewrites.
- Export formats are chosen by extension: images `.png/.jpg/.tif`; Office/HTML `.docx/.pptx/.html/.htm/.rtf/.md/.markdown`; form/comment data `.xfdf/.fdf/.xml/.xdp/.csv/.txt`; text `.txt`; a print job goes to a printer name or a PDF path. Page-image export defaults to 150 dpi and runs on worker threads.

### Panels and keyboard (verified in the command registry)
Panels: comments, bookmarks, pages (with its new Page tools menu), fields, layers, attachments, signatures, accessibility, tags, search, compare.

`⌘K` command palette · `⌘F` find / `⇧⌘F` advanced search · `⌘G` / `⇧⌘G` next/previous match · `⌘Z` / `⇧⌘Z` undo/redo · `⌘S` / `⇧⌘S` save / save as · `⌘O` open · `⌘W` close · `⌘P` print · `⌘D` document properties · `⌘J` JavaScript console · `⌘B` add bookmark · `⌘,` preferences · `⌘L` full screen · `⌃⌘H` Read mode · `⌘3` fit visible · `⌃Tab` next tab · `⌘[` / `⌘]` previous/next view · `⇧⌘N` go to page. On Windows/Linux the command modifier is Ctrl. With a comment selected, arrow keys nudge it one screen pixel.

## Working with an AI agent

**Legitimate work.**
- Prefer the headless tool table over GUI automation. `pdfcraft-cli tools` (or MCP `tools/list`) is the capability contract; `command_list` maps UI commands to tools, and 143 of the 214 registry commands have no tool — check before you promise one.
- Prepare inputs: images and `.txt` for `doc_create`; XFDF/FDF/XML/XDP/CSV for `doc_import_data`; `.p12`/`.pfx` or Keychain/Windows-store identities for signing; openly licensed TTF/OTF for `text_font_import`; document-level attachment files for `attachment_add`.
- Inspect and repair: `doc_info` exposes warnings, repairs and the initial destination; `doc_revisions` + `doc_open_revision` show what each incremental save appended; `pdfcraft-cli info` tells you which PDF/A or PDF/UA level a file *claims*.
- Verify with independent observations: `page_render`/`render_preview` for pixels, `text_extract` for text, `doc_audit_redactions` after redaction, `pdfa_verify` after PDF/A conversion, `print_readiness` before printing, and external `qpdf`, `pdftotext`, `pdftoppm`, `pdfsig` or a real viewer where installed. Page-image export now parallelises, so batch renders finish much faster.
- For UI work, launch with `--control`, use `ui.inspect` to get the accessibility tree, click by unique label or widget id, then `ui.screenshot` to confirm. Never reuse coordinates from an older launch.

**Must not.**
- Do not drive the GUI blind or assume a deterministic layout across launches.
- Do not assume Office/HTML/PostScript import, `.xlsx` export, SVG/EPS/PS/JP2 export, PDF/X or PDF/UA verification, or OCR in any language but English.
- Do not rewrite signed documents destructively; incremental save keeps signatures valid, but any full rewrite invalidates certification. Keep the original bytes.
- Do not use `doc_create` for non-WinAnsi text; it will refuse.
- Do not expect a tool to extract an attachment, to copy page objects with `content_copy`, or to persist `layer_set`/page gaps in the PDF.
- Do not expect a timestamp server or PKCS #11 token in the CLI/UI.
- Do not use `form_calculation_order fix=true` to repair a formula `cycle`, or `standards_remove_id` as a compliance fix.
- Do not put the control file in a shared folder or assume the MCP server/control channel is on; both are opt-in and loopback/stdio only.
- Do not assume `pdfcraft-cli` exists on a machine with only the macOS app installed.

## Verification protocol

Alpha-software discipline for every session:
1. **Throwaway round-trip first.** In a scratch folder, open → edit → `doc_save` to a *new* path → reopen with `pdfcraft-cli info`/`text` and in Preview/Acrobat or `qpdf --check`.
2. **Never trust a silent export.** Re-render exported images, re-read exported text, and open `.docx/.pptx` in Word/PowerPoint or LibreOffice before declaring success; Office export is known lossy.
3. **Redaction is not done until audited.** Run `pdfcraft-cli audit` (or `doc_audit_redactions`) on the saved file; the audit fails closed on unreadable content. The F-008/F-011 hardening reduces what survives, but the audit is still the gate.
4. **Signatures:** after signing, use `sign_list` (and `pdfsig`/OpenSSL if available) on the saved file.
5. **Print and view settings:** before a print job, check `print_readiness` and the document's permissions. Page gaps, layer visibility and reading colours are view state.
6. **Backups and versions.** Keep the original PDF before any full rewrite. Check versions before trusting this skill's flags or tools — this edition was measured at v0.19.0 (`pdfcraft 0.19.0`), and a newer launcher update may differ; update apps only between projects.
7. **Hostile or huge files.** Use `pdfcraft-cli check` when a file misbehaves. Bounds are explicit — hitting one is a documented refusal, not corruption. Read `logs/pdfcraft.log` under the user's Application Support/PdfCraft folder for internal errors.

## Sources & evidence

- Repo: https://github.com/storytold/pdfcraft · tag `v0.19.0` · inspected commit `8c572792d6760bdc903d6f9a032e3e38e8f71cb8` (release 2026-11-06); date of inspection 2026-11-07. The checkout is a shallow clone pinned to the release tag, and it carries the `v0.18.1` tag too, so every id set was diffed between the two tags; it was not modified or built.
- Installed app: `/Applications/PdfCraft.app` 0.19.0, bundle id `ai.storyteller.pdfcraft`, minimum macOS 11.0; its binary prints `pdfcraft 0.19.0`. The GUI was never launched. The macOS bundle contains only `PdfCraft`, not `pdfcraft-cli`.
- Counts were machine-derived from code at this tag and diffed against `v0.18.1`: tools **195** (184 at v0.18.1; +11, none removed), registry commands **214** (210; +4), control methods 17 = 17, CLI subcommands 14 + internal `check-one` (zero diff in `apps/pdfcraft-cli/src/main.rs`), convertible inputs 13 (12), redaction patterns 6 (5), catalogue 150 items in 24 groups at both tags, page-image export 3 formats, form data 8 extensions to 6 formats.
- Key files read: `README.md`, `Cargo.toml`, `craft-i18n.rev`, `docs/gaps.md`, `docs/mcp.md`, `docs/architecture.md`, `docs/target-app-parity.md`, `apps/pdfcraft/src/main.rs`, `apps/pdfcraft-cli/src/main.rs`, `crates/automation/src/{tools,mcp,comments}.rs`, `crates/engine/src/{commands,catalog,compare,export,ocr}.rs`, `crates/create/src/lib.rs`, `crates/xfdf/src/lib.rs`, `crates/redact/src/{patterns,lib}.rs`, `crates/ocr/src/{lib,ocrs,tesseract}.rs` and `crates/ocr/README.md`, `crates/organize/src/outline_io.rs`, `crates/prc/`, `crates/prc-render/`, `crates/ui-egui/src/i18n.rs`, `crates/ui-egui/src/control/requests.rs`, `crates/ui-egui/src/panels/pages.rs`, `crates/render/src/raster/work_queue.rs`, `crates/forms/src/af/format.rs`, `crates/xfa/src/{lib,layout}.rs`, `crates/sign/`, `crates/cos/src/{budget,writer}.rs`, `vendor/README.md`.
- Shared libraries: `storytold/craft-libs` is pinned once this release at `787a7a0f…` for craft-ui, craft-menu and craft-i18n (`Cargo.toml`); interface catalogs come from `storytold/craft-i18n` at the commit in `craft-i18n.rev` (`575cfdef…`). craft-menu provides the native macOS menus.
- Companion files: `evidence.md` (claim → evidence → tier table) and `references/automation-tools.md` (all 195 tool names, titles, hints and command mappings, regenerated from `tools()` at this tag).
