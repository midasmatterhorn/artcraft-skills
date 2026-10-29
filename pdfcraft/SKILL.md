---
name: pdfcraft
description: PdfCraft is the ArtCraft PDF workbench, a clean-room Acrobat Pro reimplementation for macOS, Windows, Linux, FreeBSD and the web. Use this skill whenever the user mentions PdfCraft or pdfcraft-cli, asks what it can do, which file formats or shortcuts it supports, or asks to read, render, search, organize, combine, split, rotate, annotate, fill, calculate, sign, redact, OCR, compare, print, protect, layer, measure or convert a PDF; when preparing assets or inputs for it; when driving it headlessly through the CLI, the MCP server or the UI control channel; or when verifying, repairing or troubleshooting its output — even if the app is not named (for example "merge these PDFs", "make this scan searchable", "fix this form's calculation order", "redact this contract", "convert this PDF to Word").
---

Audit basis: this checkout is tag `v0.15.0`, commit `75360d1d7db06fed974f48c914d4c04132757187`. The installed `/Applications/PdfCraft.app` reports version `0.15.0` (bundle id `ai.storyteller.pdfcraft`, minimum macOS 11.0), and `/Applications/PdfCraft.app/Contents/MacOS/PdfCraft --version` prints `pdfcraft 0.15.0`, so the bundle matches this source. **Verify against your installed version** if the ArtCraft Launcher has auto-updated since. Deep detail: `references/automation-tools.md` lists all 179 automation tools at this tag.

## Overview

PdfCraft is an open-source, pure-Rust PDF reader and editor ("The PDF workbench; an open-source, modern PDF reader and editor", `README.md`), built clean-room with Adobe Acrobat Pro as the documented parity target (`docs/target-app-parity.md`). It is **alpha** (README "What's next": 57% of its tracked Acrobat features, 94% of core essentials, ~55% ready for everyday work) and runs on macOS, Windows, Linux and FreeBSD plus a WebAssembly shell (`apps/pdfcraft-web`, `docs/architecture.md`). Source: GitHub storytold/pdfcraft. The UI migrated to egui 0.37 this release, with side panels on craft-ui task panes, craft-ui ComboBoxes everywhere, and **native macOS menus from craft-menu**.

The PDF object graph is the document model: there is no separate project file, so the `.pdf` **is** the project (`docs/architecture.md` §Data model and editing). Pages are drawn by the vendored `hayro` 0.7.x family while PdfCraft's own renderer is built (`docs/gaps.md` gap 2; `vendor/README.md`), so rendering is good but not Acrobat-measured. This tag (v0.15.0, 2026-10-28) keeps the automation surface identical to v0.14.0 and spends its budget on XFA form performance and correctness, redaction hardening (F-008/F-011), page-image export on worker threads, a Page tools menu, Persian, and the usual platform refresh.

## Capabilities (verified)

Unless a bullet says **partial**, the path is wired into the UI and/or the CLI at this tag. If your installed version differs, run `/Applications/PdfCraft.app/Contents/MacOS/PdfCraft --version` and `pdfcraft-cli tools` before trusting flags or tool names. Tool names live in `crates/automation/src/tools.rs`; command ids in `crates/engine/src/commands.rs`; UI panels and dialogs are under `crates/ui-egui/src`.

### Automation surface at a glance

| Surface | Count at v0.15.0 | Change vs the v0.14.0 skill |
|---|---|---|
| Automation tools (`crates/automation/src/tools.rs`) | **179** (153 inline + 26 multi-line `t(` entries) | unchanged set |
| Command registry (`crates/engine/src/commands.rs:165` `COMMANDS`) | **205** | unchanged set (id diff: 0 added, 0 removed) |
| Tools mapped to a command (`ToolDef::command`) | 71 | unchanged |
| CLI subcommands (`apps/pdfcraft-cli/src/main.rs`) | **14 documented**, plus internal `check-one` | unchanged; 25 `--flag` names |
| UI control methods (`crates/ui-egui/src/control/requests.rs`) | **17** | unchanged |
| Interface languages (`crates/ui-egui/src/i18n/`) | **35** (English + 34 catalogs; **Persian `fa` added**) | +1 |
| All tools catalogue (`crates/engine/src/catalog.rs`) | 150 items, 24 groups, 5 categories; planned badges remain a plan | unchanged |
| MCP tools | the same **179**, or 17 entries under `--compact` (15 core + `tool_search` + `tool_call`) | unchanged |
| MCP resources | 4 URI templates + 2 list resources | unchanged; 16 MiB request-line cap |
| Convertible input extensions (`CONVERTIBLE`, `crates/create/src/lib.rs`) | **12** | unchanged |
| Office export targets (`OfficeFormat::from_extension`, `crates/engine/src/compare.rs`) | **4** kinds / 5 extensions | unchanged |
| Form-data extensions (`crates/xfdf/src/lib.rs`) | **8** → 6 formats | unchanged |
| Page-image export formats | **3** (png, jpeg, tiff; `pdfcraft-cli render` also writes `.pam`) | unchanged; **exported on worker threads (~80% less wall time)** |

`pdfcraft-cli tools` is the live capability contract; the full name/title/hint table is in `references/automation-tools.md`. Every tool has a JSON Schema, read-only (48) or destructive (25) hints and an optional registry command id. Repo docs lag badly: several still say "141 automation tools" and "184 registered commands" (real: 179 / 205).

### Reading, navigation and text
- Tiled CPU rendering with single, continuous, two-up and two-page layouts, rotation, full screen, Read mode, light/dark/system themes and per-tab history. Optional gapless page display and an independent thumbnail slider.
- Reading-order text extraction (columns, RTL runs, vertical CJK), find-as-you-type, text selection and permission-aware copy. `pdfcraft-cli text` refuses text from a document that forbids copying unless the owner password is supplied.
- Bookmarks (nested, searchable, with colour and bold/italic), page thumbnails, page labels, transitions, word/character counts, layers, attachments, reading colours and the document's initial view. **New:** Document Properties reads a named opening destination's page, so choosing page 1 replaces it (ISO 32000-2 12.3.2.4, PR #4574).
- Reopening a file can restore the page, zoom and page display it was last shown with (desktop only, 100 files).
- PDF 1.0–2.0, repair of damaged files with the repairs reported. Whole-file operation: no lazy disk read yet.

### Page organization, combine, split, create
- Rotate, reverse, delete, move, duplicate, replace, extract, insert blank/file pages, crop/boxes, page labels, transitions. Page copy/cut/paste exist only as commands.
- **New:** a **Page tools menu in the Pages panel** (PR #4583).
- Combine with one bookmark per file, carrying links, named destinations, form fields, layer defaults, attachments and nested bookmarks; split by page count, before pages, top-level bookmarks or maximum size.
- Create PDFs from blank pages, images (PNG/JPEG/TIFF including multi-page and BigTIFF, GIF, BMP, JPEG 2000) and `.txt`/`.text` — 12 extensions; **partial** for text: WinAnsi only.
- Compare two documents: text diff plus optional visual-region diff, PDF report, or differences added as comments. **Partial:** no filters for images/annotations/formatting, no page ranges, no scanned-document support.
- Action Wizard: list built-in actions/steps and run an action or a custom step list over many files. No action creation UI.

### Comments, bookmarks, forms, layers, attachments
- 19 markup kinds; replies, review status, locking and summarization; flattening is `doc_flatten`. Comment threads resolve through each reply's `/IRT`; `comment_list` reports per-reply status and the displayed rectangle; `comment_*` refuse a shared `id`.
- AcroForm listing, filling with regenerated appearances, field creation, properties, tab order, calculations and field JavaScript, automatic detection, data import/export; dotted field names create parent hierarchies. **New:** with NeedAppearances, check boxes and radio buttons draw their `/MK` caption (ISO 32000-2 Table 224, PR #4454).
- **XFA (much faster and more correct this release):** a **static XFA form whose data fills thousands of fields opens in seconds** (PR #4638); a laid-out XFA form's **signature fields are named by their SOM path** so other viewers find the signature (PR #4507); a round XFA check box's field highlight is round (PR #4512); XFA image-hash parsing rejects non-hex characters. `xfa_to_static` converts an XFA form to a static form; document-level "PDF container" scripts are skipped from `js_run` while XFA layout is active.
- Form calculation order with `reads`/`issues` and set/move/`fix`; text-field tables 1–100 × 1–50 with per-column name patterns.
- Document-level attachments can be added and deleted headlessly. **New:** an attachment's row opens on a double-click and has a right-click menu (PR #4513). Still **no tool extracts an attachment**.
- Layers: `layer_set` is a view setting — `page_render` draws with it, the file never changes. Fill & Sign without prepared fields.
- Links, JavaScript: `link_*`, `js_run`, `js_document_scripts`, `js_set_document_script`, `form_set_script`; `doc_flatten` bakes appearances in.

### Protect, redact, sanitize, standards
- Standard security handler R2–R6: RC4-40/128, AES-128/256, user/owner passwords with SASLprep, permissions, re-encryption on save. No certificate (public-key) encryption.
- Redaction by rectangle, text find, word list, pattern or whole pages, with FOIA/Privacy Act overlay codes; applying removes text, images, vectors, comments and form fields under the marks and runs a verification pass. **New hardening (redaction proposals F-008/F-011):** confidential **vector paths behind clipping are no longer retained** after redaction, and **unused Type 3 glyph programs and fonts are unlinked** on redaction (PRs #4577, #4579) — less hidden data survives in the output.
- Faux-redaction audit finds text still extractable under painted boxes; paint-order and colour-aware, fails closed on unreadable content, honours the copy permission, budgeted.
- Remove hidden information / Sanitize, with categories listed first. `standards_remove_id` strips PDF/A or PDF/X identification.
- Printing obeys document permissions; low-quality-only printing rasterizes at ≤150 dpi.

### Signatures
- Sign with `.p12`/`.pfx` digital IDs, macOS Keychain identities or the Windows certificate store; PAdES B-B, SHA-256; certification signatures; visible signatures; self-signed ID creation; trust list; validation including changes made after signing.
- Validation checks embedded RFC 3161 timestamp tokens and offline CRL/OCSP evidence with a DSS for PAdES B-LT. **Partial:** no timestamp-server setting and no online fetching; engine-only TSA APIs. No PKCS #11/smart cards on macOS/Linux, no OS trust store.

### OCR, print, export, optimize, accessibility, measuring, editing
- OCR adds an invisible searchable text layer; batch recognition, camera-photo straightening. **Partial:** English/unaccented Latin only; models must be installed — **packaging now fetches them from the ONNX URLs** (the legacy RTEN URLs return 403, PR #5039).
- Print with Acrobat-style options — ranges, odd/even, reverse, fit/actual/shrink/custom, multiple/cut-stack, booklet, poster, 21 paper presets, copies, duplex, grayscale, CUPS driver options, "print as image", or write a print-ready PDF. The chosen paper is sent to the spooler as its `media`.
- Export pages as PNG/JPEG/TIFF (**on worker threads — about 80% less wall time**, PR #5026), all embedded images, reading-order text, Word `.docx`, PowerPoint `.pptx`, HTML or RTF (**partial** for Office — basic/lossy). **New:** Word export keeps an italic run inside its sentence's paragraph (PR #4411). Images exported keep soft-mask Decode opacity ranges; undecodable JPEG 2000/JBIG2/CCITT/Separation images are listed under `skipped`.
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
- **35 selectable interface languages** (English + 34 catalogs; Persian added this release); Chinese interface text can still show missing-glyph boxes, Arabic layout is not mirrored, and no help is translated. A missing entry falls back to English instead of failing.
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
- **OCR reads only unaccented Latin (`en`).** No accents, Cyrillic, Greek, CJK, Arabic, Hebrew or Indic recognition; no editable-text OCR output.
- **No Preflight; PDF/A only 2b/3b and partial.** No PDF/X or PDF/UA verification; CMYK documents get no output intent.
- **Signatures:** no PKCS #11/smart cards on macOS/Linux, no timestamp-server setting, no online OCSP/CRL fetching, no OS trust store, no signing in the browser.
- **Attachments are one-way:** `attachment_add`/`attachment_delete` exist, the panel opens/saves them, but no tool extracts an attachment's bytes.
- **`content_copy` is the only paste path and it is headless-only**; it copies *added* content only.
- **Forms:** wider Acrobat JavaScript object model incomplete; document actions, form submission, barcode fields and rich-text values missing; XFA flattening incomplete. `form_calculation_order` can report a `cycle` but **cannot fix it**.
- **Compare** has Text/Visual filters but no image/annotation/formatting filters, no page ranges and no scanned-document support.
- **No scanners, no GPU page rasterization, no pen pressure, no Read Out Loud.**
- **Preferences are sparse**; print-production tools (output preview, separations, ink manager, printer marks, colour conversion) are absent.
- **Performance:** the whole file is held in memory; file-backed lazy input is blocked on the renderer. Hostile files are bounded, not fast (page-image export is now worker-threaded).
- **UI precision:** moving selected objects across pages, rulers/grids/guides, multiple windows and split view are missing.
- **No AI/cloud features**; a local/opt-in provider is planned.
- **Other PDF gaps:** no certificate encryption, no linearized save, no portfolio view, no `.xdp` as a document, no `.sequ` action files; JPEG 2000/JBIG2/CCITT/Separation images cannot be exported as images.
- **Copy- and print-protected documents:** extraction, copy, compare and OCR text output honour permissions; never bypass.
- **View-only settings do not save:** page gaps, layer visibility and reading colours change the view, not the file.
- **The All tools catalogue is a plan, not a promise, in both directions.**
- **Repo docs lag the code:** several still say 141 automation tools / 184 commands (real: 179 / 205). Trust the code and `pdfcraft-cli tools`.

## How to operate

### Launch (macOS)
- App: `/Applications/PdfCraft.app` (bundle id `ai.storyteller.pdfcraft`, minimum macOS 11.0). Binary: `/Applications/PdfCraft.app/Contents/MacOS/PdfCraft`.
- `open -a PdfCraft` or `open -a PdfCraft FILE.pdf`; pass flags with `open -a PdfCraft --args --control ~/.pdfcraft-control.json`.
- `/Applications/PdfCraft.app/Contents/MacOS/PdfCraft --version` prints `pdfcraft 0.15.0` and `-h`/`--help` prints usage, both without opening a window.
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
Add `{"command":"pdfcraft-cli","args":["mcp","--root","work/pdfs"]}` to the agent's MCP config. `--compact` makes `tools/list` return 15 core tools plus `tool_search` and `tool_call` (17 entries); `tools/call` still accepts any of the 179 names. For least privilege use `--automation-read-root` and `--automation-write-root` instead of one broad `--root`. Resources: `pdfcraft://document`, `pdfcraft://commands` and the templates `pdfcraft://doc/{doc}/info`, `…/text`, `…/page/{page}/text`, `…/page/{page}/image{?dpi}`. Request lines over 16 MiB get a JSON-RPC error instead of memory growth.

### UI control channel (opt-in)
Start the app with `--control ~/.pdfcraft-control.json`, then use `pdfcraft-cli ui --control ~/.pdfcraft-control.json …`:
`inspect query=…`, `click label="Organize pages"`, `key key=K modifiers='["command"]'`, `command id=comment.square`, `drag from='[400,300]' to='[600,420]'`, `screenshot --out window.png`, `quit`.
The file holds the loopback port and a random token; the CLI authenticates first and refuses a symlink or a file readable by another user. The app accepts 8 unauthenticated connections at a time, each with 10 s to authenticate. The 17 methods are `ui.state`, `ui.commands`, `ui.command`, `ui.set`, `ui.open`, `ui.inspect`, `ui.click`, `ui.focus`, `ui.resize`, `ui.quit`, `ui.drag`, `ui.move`, `ui.type`, `ui.key`, `ui.screenshot`, `ui.dock`, `ui.dock.reset`. `ui.state.active` reports `page`, `zoom_percent`, `layout`, `page_gaps`, `selected_pages`, `viewport` and `pages_on_screen` rectangles for aiming clicks. `ui.quit` asks the normal Save/Don't save/Cancel prompt and never discards silently.

### Document model, save and export
- The PDF is the document; there is no sidecar project file. Converted images/text are new unsaved PDFs.
- Edits stay in memory as undo steps; autosave writes a recovery snapshot every 60 s. Encrypted documents stay encrypted on disk.
- Save (`⌘S`) writes an **incremental update appended to the same file**, preserving the original bytes and prior signatures; Save As is a full rewrite; writes are atomic through a staging file. `doc_save` `full: true` forces the rewrite.
- A full rewrite happens where it must: redaction, PDF/A conversion, password change, sanitize, Save As with garbage collection, or print imposition; signed documents are protected from optimizer rewrites.
- Export formats are chosen by extension: images `.png/.jpg/.tif`; Office `.docx/.pptx/.html/.htm/.rtf`; form/comment data `.xfdf/.fdf/.xml/.xdp/.csv/.txt`; text `.txt`; a print job goes to a printer name or a PDF path. Page-image export defaults to 150 dpi and runs on worker threads.

### Panels and keyboard (verified in the command registry)
Panels: comments, bookmarks, pages (with its new Page tools menu), fields, layers, attachments, signatures, accessibility, tags, search, compare.

`⌘K` command palette · `⌘F` find / `⇧⌘F` advanced search · `⌘G` / `⇧⌘G` next/previous match · `⌘Z` / `⇧⌘Z` undo/redo · `⌘S` / `⇧⌘S` save / save as · `⌘O` open · `⌘W` close · `⌘P` print · `⌘D` document properties · `⌘J` JavaScript console · `⌘B` add bookmark · `⌘,` preferences · `⌘L` full screen · `⌃⌘H` Read mode · `⌘3` fit visible · `⌃Tab` next tab · `⌘[` / `⌘]` previous/next view · `⇧⌘N` go to page. On Windows/Linux the command modifier is Ctrl. With a comment selected, arrow keys nudge it one screen pixel.

## Working with an AI agent

**Legitimate work.**
- Prefer the headless tool table over GUI automation. `pdfcraft-cli tools` (or MCP `tools/list`) is the capability contract; `command_list` maps UI commands to tools, and 134 of 205 commands have no tool — check before you promise one.
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
6. **Backups and versions.** Keep the original PDF before any full rewrite. Check versions before trusting this skill's flags or tools; update apps only between projects.
7. **Hostile or huge files.** Use `pdfcraft-cli check` when a file misbehaves. Bounds are explicit — hitting one is a documented refusal, not corruption. Read `logs/pdfcraft.log` under the user's Application Support/PdfCraft folder for internal errors.

## Sources & evidence

- Repo: https://github.com/storytold/pdfcraft · tag `v0.15.0` · inspected commit `75360d1d7db06fed974f48c914d4c04132757187` ("Release 0.15.0", 2026-10-28); date of inspection 2026-10-29. The checkout is a shallow clone pinned to the release tag (plus a fetched `v0.14.0` ref for set diffs); it was not modified or built.
- Installed app: `/Applications/PdfCraft.app` 0.15.0, bundle id `ai.storyteller.pdfcraft`, minimum macOS 11.0; binary `--version` → `pdfcraft 0.15.0`. The macOS bundle contains only `PdfCraft`, not `pdfcraft-cli`.
- Counts were machine-derived from code at this tag and diffed against the fetched v0.14.0 files: tools 179 → 179 (153 inline + 26 multi-line `t(` entries), commands 205 → 205 (id diff clean), control methods 17 → 17, languages 34 → 35 (+`fa`), CLI 14+`check-one` unchanged.
- Key files read: `README.md`, `Cargo.toml`, `docs/gaps.md`, `docs/mcp.md`, `apps/pdfcraft/src/main.rs`, `apps/pdfcraft-cli/src/main.rs`, `crates/automation/src/tools.rs`, `crates/engine/src/commands.rs`, `crates/engine/src/compare.rs`, `crates/ui-egui/src/control/requests.rs`, `crates/ui-egui/src/i18n/`, `crates/ui-egui/src/panels/pages.rs`, `crates/render/src/raster/{,work_queue}.rs`, `crates/xfa/src/{lib,layout}.rs`, `crates/redact/src/`, `crates/xfdf/src/lib.rs`, `crates/forms/`, `crates/sign/`, `crates/ocr/`, `crates/print/src/lib.rs`, `crates/create/src/lib.rs`, `crates/cos/src/{budget,writer}.rs`.
- Shared libraries consulted: `storytold/craft-libs` crates pinned across three revisions this release (`e11f9d9a…` for craft-menu, plus `6d518fc7…`/`a517b384…` — `Cargo.toml`); craft-menu provides the native macOS menus.
- Companion files: `evidence.md` (claim → evidence → tier table) and `references/automation-tools.md` (all 179 tool names, titles, hints and command mappings).
