---
name: wordcraft
description: >-
  WordCraft is an open-source, clean-room reimplementation of Microsoft Word in Rust (alpha,
  v0.12.0): a ribbon word processor that reads and writes .docx (password-protected and
  AES-encrypted included), opens legacy .doc, exports PDF, runs several documents at once (one
  window each), plus a CLI (wordcraft-cli), a 17-tool MCP server, a localhost JSON control channel
  and a headless screenshot harness for agents. Trigger this skill whenever the user mentions
  WordCraft, .docx/.doc/.odt/.rtf/.html/.md/.tex documents in a WordCraft context, wordcraft-cli,
  WordCraft's MCP tools or control channel, personal templates, mail merge, macros, track changes,
  or asks what WordCraft can or cannot do, which formats it opens or saves, how to script, automate,
  batch-convert, verify, repair or troubleshoot it — even if the app is not named but the job is
  word-processor work ("write a .docx", "convert this .doc to PDF", "decrypt this .docx", "add
  comments and track changes", "mail-merge a letter", "make a report from Markdown"). Do not use it
  for Microsoft Word itself or other word processors.
---

# WordCraft

Audit basis: this checkout is tag `v0.12.0`, commit `3de6ff95af86c19d67030cd96dba15cd6a45a25e`. The installed `/Applications/WordCraft.app` reports version `0.12.0` with bundle id `ai.storyteller.wordcraft`, and its binary prints `wordcraft 0.12.0 (3de6ff95)`, so the bundle matches this source. **Verify against your installed version** (`wordcraft --version`, `wordcraft-cli --version`) if the ArtCraft Launcher has auto-updated since. No `references/` directory ships with this skill: everything below is cited inline to the repo.

## Overview

WordCraft is an open-source, clean-room reimplementation of Microsoft Word (Microsoft 365) in pure Rust — "writing and document design" — by the ArtCraft team (`README.md`). It is at **alpha** (`ROADMAP.md:3`): self-rated ~60% ready for real work, ~55% for a mainstream practitioner's week and ~63% for everyday essentials (`ROADMAP.md:25–27`), with **505 of 520** ribbon/menu catalog features wired to live commands (97.1%; `docs/parity-checklist.md:5`). One codebase serves macOS, Windows, Linux, BSD and the web: egui/eframe on the GPU (migrated to egui 0.37 this release), no Electron. Source: GitHub **storytold/wordcraft**, MIT OR Apache-2.0. It reads and writes Microsoft's formats from published specifications (ECMA-376/ISO 29500, MS-DOC, OASIS ODF, MS-OFFCRYPTO), never from their code.

Everything user-visible is a **command with an id**; the ribbon, keyboard, command search, CLI, control channel and MCP all dispatch the same registry. **Several documents can be open at once this release — one native window per document** (`crates/ui-egui/src/windows.rs`), and MCP, the control channel and the CLI address a document by id.

## Capabilities (verified)

### Automation surface at a glance

Every number below was re-counted from this tag's code on 2026-10-29; the repo's own prose counts are stale (see the note under the table).

| Surface | v0.12.0 | Change since v0.11.0 |
|---|---|---|
| Engine commands (`CommandSpec::new` with a literal id) | **648** | **+5**: multi-document ids (`file.closeDocument`, `view.stylesPaneDock`, `view.switchWindows`) plus further additions in other namespaces; **0 removed** |
| Catalog coverage | **505 / 520 (97.1%)** | was 504/520 (96.9%); `docs/parity-checklist.md:5` |
| CLI subcommands | **10** | unchanged (`apps/wordcraft-cli/src/main.rs` `SUBCOMMANDS`) |
| CLI flags | **21** plus `-h/--help`, `--version` | unchanged |
| MCP tools | **17** | **+1**: `list_documents` (multi-document, `crates/mcp/src/tools.rs`) |
| Control-channel methods | **21**, plus command-id fallthrough | **+2**: `file.close`, `file.exportPng`; `engine.execute`/`document.inspect`/`ui.render` take `doc` (`crates/ui-egui/src/control.rs` header, `control/handler.rs`) |
| Interface languages | **27** | unchanged count; catalogs live in `storytold/craft-i18n` (`craft-i18n.rev` now `9205108c…`) |
| Proofing variants | **15** | unchanged (`crates/proof/src/lang.rs`) |
| Default shortcuts | 167 specs carry a `.key()` | was 164 (+3); docs say 140/158 — stale |
| Open / save extensions | 19 / 14 | unchanged (`crates/engine/src/io.rs`) |

Do not quote the repo's command counts: README and ROADMAP still print hundreds-low numbers and `docs/mcp.md` says "over 270" tools — all stale; count with `wordcraft-cli commands --json`. The dialog count runs the other way: docs say "60 modal dialogs", the code answers to 89 distinct names at v0.11.0, and **Custom Document Properties** (`file.properties` dialog, PR #2997) joins this line.

### New in v0.12.0 (verified against the v0.11.0 source)

- **Several open documents**: File ▸ New opens another document; **one native window per open document** (`crates/ui-egui/src/windows.rs:1`); View ▸ New Window opens another window on the same document (`view.switchWindows`); per-document recovery, Document1 naming, and warnings for hidden documents. **MCP, the control channel and the CLI address a document by id**: every MCP tool takes optional `"doc": <int>` (`crates/mcp/src/tools.rs:54`), control `engine.execute`/`document.inspect`/`ui.render` take `doc` (`crates/ui-egui/src/control.rs:16`), and `file.closeDocument {doc}` closes one.
- **AES-encrypted Word files open (Standard encryption)**: ECMA-376 packages encrypted with the older *Standard* method (Word 2007 era; MS-OFFCRYPTO §2.3.4.5–§2.3.4.9, AES keys) decrypt alongside the *agile* method (`crates/docx/src/crypt.rs:12,54,95,150`; PR #2628).
- **AutoFormat "Add a period with double-space"** option and an AutoCorrect Options button in Options › Proofing (PR #3318).
- **Regex Replace expands capture groups** (PR #4201).
- **Scale all style font sizes at once** (PR #2620); applying a style set keeps the document's own styles and defaults (PR #4013).
- **Arabic letter numbering drawn** (`arabicAlpha`, `arabicAbjad`, PR #4218); Arabic-Indic digits kept as typed in Arabic numeral mode (PR #3329).
- **File ▸ Info Custom Document Properties dialog** (PR #2997).
- **Filter-as-you-type command search** in Customize Ribbon, Quick Access Toolbar and Keyboard pickers (PR #1848).
- **Editable three-column header/footer presets** (PR #2266).
- **Task panes on craft-ui's shared panes**: Styles docks left/right or floats; dropping a pane outside or inside a docked pane orders the side (PRs #3109, #4386).
- **Continuous sections** running off a page go onto the next; empty section marks stack to the page bottom (PR #3936).
- **Zotero bridge hardened**: loopback-only client, same-user check on Linux (PR #3876).
- **Hardening wave**: layout runs in linear time on hostile documents, bounded proofing work, legacy `.doc` reader budgets, render/PDF/metafile budgets, font-ingestion checks, DOCX package/writer hardening (glossary privacy scrub, case-insensitive part names), bounded MCP line reads, bounded `review.compare` LCS work; **PDF export is ~24% faster** (PRs #3866–#3877 and follow-ups, #4602).
- **Import fixes**: LaTeX `\genfrac` (binomials survive export), RTF backslash-space/soft breaks/zero-width spaces, Markdown comment/code-span fixes, ODT negative timezone offsets and author fallback, DOCX `sym` hex prefixes and break/note-reference normalization, repeated DOCX style replacement across saves.
- **Per-user Windows installer** (no administrator rights, PR #2560/PR policy); **startup update prompt with direct self-updating** (craft-update); egui 0.37 migration.
- Carried from v0.11.0 and re-verified: mail-merge record navigation/ranges and Print Documents, `view.readPageColor`, Spanish proofing ×4, highlight toggling, AutoFormat `*bold*`/`_italic_`, Convert to Text, field depth (docinfo fields, `\* CardText|OrdText|DollarText|Hex`), Restrict Editing enforced on `file.*` and identity, line caps, no-op commands are not edits, DOCX unset default font size, MCP bridge that starts before the app, `type_text {"paragraphs": true}`, external i18n catalogs.

### Editing, formatting, document features
- Writing: typing/IME, AutoCorrect, list autoformat, selections, clipboard with formatting (HTML/RTF from other programs), undo/redo incl. an undo-history list (`edit.undoTo`, `edit.undoHistory`), find & replace with regex (capture-group expansion now); typing behaviour is pinned to Word's by `crates/engine/src/tests_typing.rs`.
- Formatting, paragraphs, styles/themes/style sets, lists (Arabic letter numbering drawn), tables (styles with band sizes, merge/split, sort, formulas, Convert to Text), pages/sections (margins, columns, headers/footers with editable three-column presets, watermark, line numbers, hyphenation, drop caps, page borders), objects (pictures with crop/recolour/background removal, shapes, text boxes, groups, drawing canvases, wrap, free rotation), references (TOC, footnotes/endnotes, citations APA/MLA/Chicago/IEEE, captions, table of figures, index, cross-references, Zotero), review (spelling/grammar, comments with local-time stamps, track changes incl. moves and formatting revisions, accept/reject, compare, restrict editing), mail merge (CSV/spreadsheets, rules, Finish & Merge, Print Documents), Draw-tab ink, Read Aloud, Print/Web/Draft/Read/Focus/Full Screen views.
- Content controls (`w:sdt`), move tracking (`w:moveFrom`/`w:moveTo`), formatting revisions and glossary/building blocks round-trip.

### Import / open (by extension, `crates/engine/src/io.rs` OPEN_EXTS)
- `.docx` / `.docm` / `.dotx` / `.dotm` (Word package; Strict Open XML read via namespace mapping), `.doc` / `.dot` (Word 97-2003 binary reader, `crates/docbin`), `.txt`, `.md`, `.markdown`, `.html`/`.htm`, `.rtf`, `.odt`, `.tex`/`.latex`/`.ltx`, `.xml` (Word XML Document / Flat OPC or Word 2003 XML), `.json` (WordCraft's native document model), and `*.wcraft.json`.
- Extensionless or unknown-extension files open **by content** when they are Word/RTF/XML/text, with encoding detection.
- Password-protected `.docx` opens and saves with a password — **agile** encryption (Word 2010+) and **Standard** encryption (Word 2007-era AES, read) (`crates/docx/src/crypt.rs`); `.doc` protected with XOR/RC4/RC4 CryptoAPI opens — untested on Word-written files; AES `.doc` is refused (`docs/gaps.md`).
- Pictures: PNG, JPEG, GIF, WebP, BMP, TIFF, plus Windows/Enhanced Metafile `.wmf`/`.emf` at their frame size. Not SVG, ICO, HEIC.

### Save / native format / export (`crates/engine/src/io.rs` SAVE_EXTS)
- Native-lossless: `.docx`/`.docm`/`.dotx`/`.dotm` via `crates/docx`, Word XML Document (Flat OPC) and Word 2003 XML `.xml`, and `.json` for agents. A file opened with a password is saved with it again; exports that cannot carry one (pdf, html, txt) stay plain.
- Copies/export: `.pdf` (krilla through the pinned `craft-pdf`), `.png` page images, `.txt`, `.md`, `.html`, `.rtf`, `.odt`, `.tex` (partial fidelity — see limitations). PDF/PNG follow the Numeral setting for digit shapes.
- Print Markup (`--markup` / `markup: true`): comments and tracked changes in PDF/PNG, a comment list in HTML/Markdown/text.
- `.doc` cannot be written; saves are atomic-by-design (temp file + replace; a failed save keeps the original bytes).

### Personal templates
- `file.listTemplates {"dir"?}` lists `.dotx`/`.dotm` in the user templates folder (top level plus one subfolder level as categories, ≤500 templates, ≤64 categories; network folders and relative paths refused; the automation read root applies). Without `dir` it uses the folder saved in File › Options and **errors if none is saved** — always pass `dir` headlessly.
- `file.newFromTemplate {"path"}` opens the file as a new, untitled, **dirty** document attached to that template (no extension check). `file.saveTemplate {"path"}` **appends `.dotx` unless the path already ends `.dotx` or `.dotm` (any case)** — `out.docx` becomes `out.docx.dotx`. The GUI path is `ui.saveAsTemplate` (system dialog) — unusable headlessly.

### Automation surfaces (all four drive the same commands)
- **CLI**: `wordcraft-cli convert|info|text|inspect|render|run|commands|parity|mcp|zotero` with flags `--markup`, `--update-fields`, `--format wordml2003|flatopc`, `--page`, `--scale`, `--file`, `--template`, `--cmd 'id={json}'`, `--save`, `--print`, `--author`, `--password`, `--password-file`, `--script FILE|-`, `--json`, `--markdown`, `--connect`, `--automation-read-root`, `--automation-write-root`, and Zotero's `--trace`, `--port` (`apps/wordcraft-cli/src/main.rs` usage text is authoritative).
- **`run --script`**: a JSON job file or stdin — `{"file"?, "template"?, "commands": […], "save"?: ["out.docx", "out.pdf"]}` — runs the commands, then saves to each output, format by extension. Relative `file`/`save` paths resolve against the script's folder; capped at 4 MiB, 100,000 commands, 64 outputs. A failing command stops the run with `command N (id): …` and exit 1 before any output is written.
- **MCP server** over stdio: `wordcraft-cli mcp` (headless) or `--connect 127.0.0.1:<port>` (bridged to a running app). **17 tools**: `list_commands`, `execute`, `batch`, `new_document`, `open_document`, `save_document`, `type_text`, `select_text`, `get_text`, `inspect_document`, `render_page`, `parity`, **`list_documents` (new)**, and app-only `screenshot`, `click`, `key`, `ui_inspect` (`crates/mcp/src/tools.rs`). Every tool takes optional `"doc": <int>` to target an open document. Protocol revision `2025-06-18`, resources `wordcraft://document` and `wordcraft://commands`.
- **Control channel**: app started with `--control <port>`; JSON lines over `127.0.0.1` with a per-window key from `<settings>/control-key.<instance>` (`local-<port>` outside Flatpak; mode 0600, removed on exit) (`crates/control-key/src/lib.rs:38`). **21 methods**: `engine.execute {command, params, doc?}`, `engine.commands`, `document.inspect {doc?}`, `ui.inspect`, `ui.click`, `ui.clickText`, `ui.move`, `ui.drag`, `ui.press`/`ui.release`, `ui.wheel`, `ui.key`, `ui.text`, `ui.screenshot`, `ui.render {doc?}`, `ui.parity`, `ui.resize`, `ui.focus`, **`file.close`, `file.exportPng` (new)**, `app.quit`; any other method name is treated as a command id (`crates/ui-egui/src/control.rs` header, `control/handler.rs`; `docs/control-protocol.md`). `ui.key`/`ui.text` are background-safe and reply `{"queued": true}` before the edit is applied.
- **Macros**: `tools.recordMacro` / `tools.macros` record and replay command sequences.
- **Headless UI screenshots**: `cargo run -p wordcraft-ui-egui --example ui_shot -- script.jsonl` — JSON lines of control requests plus `{"shot": "<path>.png"}`, `{"steps": n}`, `{"wait": ms}`, `{"empty": true}`.

### Platform
- WebAssembly web build exists and is CI-checked: `apps/wordcraft-web` (`?webgl`, `?sample`, iframe `?host=parent` with `&author=`; no TCP control channel, Open/Save go through the browser); `cargo xtask wasm` checks the layers for wasm32.
- Local recovery of unsaved work (desktop only), now **per document**, covers new drafts and edits; password-protected documents get no plaintext recovery copies; headless/CLI/web sessions create none.
- Native printing through craft-libs' `craft_ui::printing`: `ui.printSettings`, `ui.printSubmit`/`ui.print`, `file.printPdf` (also takes `paper` to scale onto another paper size).
- Zotero integration (`crates/zotero`, `docs/zotero.md`) — needs the Zotero desktop app running; loopback-only client with a same-user check on Linux. In-app: `ui.zotero.*`; from a terminal: `wordcraft-cli zotero <command> <file>`.
- **Startup update prompt with direct self-updating** (craft-update); Windows installs per-user by default.

## Known limitations and not-implemented

Ranked shortfalls with evidence are in **docs/gaps.md** — read it before promising anything. The blocking (beta) list, gaps #1–#7:

1. **DOCX has no real-world corpus test**: no corpus of files from Word, Google Docs, LibreOffice and Pages ships in the repo; `crates/docx/tests` are synthetic fixtures. Revision entries elsewhere cite private-corpus measurements, which contradicts "untested" — do not assume either way: treat fidelity on files you did not create as unverified and round-trip the user's file.
2. **Word's native ink is not drawn from its strokes** (its picture fallback shows) and **OLE objects show only their picture**; every ink form, drawing canvas, group shape, chart and SmartArt is preserved and written back with all parts.
3. **Field crashes and freezes** remain open: startup crash on Intel UHD Graphics (#170), macOS 12.7.6 Intel crash (#979), Thai-font and font-selector freezes (#59, #31). Save-path reliability was narrowed, not closed.
4. **Pagination differs from Word**: no Aptos-metric font, legacy compatibility options partial, no page-by-page comparison harness.
5. Still missing from the review/data model: drag-and-drop moves (no text drag yet), tracked style-definition changes, custom-XML binding evaluation.
6. Print dialog depth: driver tray/options and pages per sheet remain.
7. Dialog depth: ~90 dialog names against Word's ~100.

Catalog features with **no command** (15 rows after `view.switchWindows` gained one this line): `tools.dictate`, `insert.onlinePicture`, `insert.model3d`, `insert.screenshot`, `addins.get`, `insert.video`, `insert.inkEquation`, `draw.inkToMath`, `review.translate`, `review.blockAuthors`, `view.arrangeAll`, `view.sideBySide`, `view.syncScroll`, `view.readLayout` (`docs/parity-checklist.md`).

Other verified gaps:
- **Charts/SmartArt from Word are read-only** (no embedded-workbook editing); no combo/3D/stock charts. WordCraft's own charts and SmartArt are editable.
- **`.doc` is read-only** — WordCraft never writes Word 97-2003; Word 6/95 files are refused. No PDF Reflow, no MHT, no Works/WordPerfect.
- **No VBA execution** (macros in `.docm` are preserved, never run), no Office add-ins, no cloud storage, no real-time co-authoring.
- **Proofing** covers **15** variants: English (US, UK, Canada), Polish, Portuguese, Italian, Croatian, Turkish, Russian, Czech, Indonesian, Spanish (Spain, Mexico, Latin America, Uruguay) — non-English dictionaries are read from the system; Bulgarian and German have hyphenation only.
- **Writing fidelity is partial for non-DOCX formats**: RTF and ODT ~50%, HTML ~60%, Word 2003 XML write drops shapes/charts/equations.
- **RTL/East Asian depth** is incomplete: kashida, RTL in HTML/ODT/RTF.
- Mail merge sources: CSV/TSV/TXT and `.xlsx/.xlsm/.xls/.ods` only; no Outlook/Access/database sources, no email merge.
- No in-app AI assistant (agent control is external, over CLI/MCP).
- Default shortcuts: 167 bindings vs Word's ~250 (measured; docs say 140/158 — stale).
- Screen-reader access is exposed through AccessKit but has not been tested with NVDA/VoiceOver/Orca.
- **Personal templates are narrow**: `.dotx`/`.dotm` only, one subfolder level, ≤500 entries, network folders refused, and the GUI picker needs a saved folder.
- The **desktop app's automation is not confined**: `--automation-read-root`/`--automation-write-root` apply to the headless MCP server only and are an error with `--connect`.
- Interface translations come from `storytold/craft-i18n`; without the `CRAFT_I18N_DIR` checkout at the pinned SHA the build is English only.

## How to operate

Launch (macOS):
- App: `open -a WordCraft` or `open -a WordCraft --args <file.docx>`. Binary: `/Applications/WordCraft.app/Contents/MacOS/WordCraft`. Bundle id `ai.storyteller.wordcraft`.
- App flags: `wordcraft [--sample] [--control PORT] [FILE…]`; `--version`, `-h|--help`. A bad `--control` port exits with status 2.
- **`wordcraft-cli` is not inside the app bundle.** Get it from the release artifact `wordcraft-cli-<ver>-macos-universal.zip` or build it: `cargo run --release -p wordcraft-cli -- <args>`.
- Environment variables that matter to agents: `WORDCRAFT_CONTROL_PORT`, `WORDCRAFT_CONTROL_KEY` (for `mcp --connect`), `WORDCRAFT_PROFILE_DIR` (isolated profile incl. recovery/keys), `WORDCRAFT_NO_PREFS`, `WORDCRAFT_PASSWORD`, `WORDCRAFT_REGION=en-US`, `WORDCRAFT_LANGUAGE`, `RUST_LOG`.

Document model: **several documents at once, one native window each** (`crates/ui-egui/src/windows.rs`); File ▸ New opens another, View ▸ New Window re-windows the same document, `view.switchWindows` lists windows, `file.closeDocument {doc}` closes one, and automation targets a document with `doc` (MCP tools, control `engine.execute`/`document.inspect`/`ui.render`). Recovery is per document.

Core commands (exact ids, from `crates/engine/src/cmd/file.rs`, `cmd/tools.rs`, `cmd/user_templates.rs`):
`file.new {"template": "blank|sample|letter|resume|report"}` (an unrecognised name silently yields a blank document), `file.open {"path": …, "password"?}`, `file.save {"path"?, "password"?, "markup"?, "format"?}`, `file.saveAs`, `file.encrypt`, `file.rename {"name"}`, `file.exportPdf {"path": …, "markup"?}`, `file.exportPng {"path":…, "page"?, "scale"?}`, `file.printPdf {"path", "range"?, "pages"?, "copies"?, "collate"?, "paper"?}`, `file.close {"force"?}` / `file.closeDocument {doc}`, `file.setAuthor {"name"}`, `file.properties`, `file.info`, `document.inspect`, `document.text`, `review.trackChanges {"value": true}`, `review.restrict {"mode"?|"stop": true}`, `references.updateFields`, `file.listTemplates {"dir"?}`, `file.newFromTemplate {"path"}`, `file.saveTemplate {"path"}`, `mailings.first|last|goToRecord|printDocuments`, `view.switchWindows`, `view.stylesPaneDock`.

Positions in command params and `document.inspect` are `{"story": "body" | {"part": n}, "path": [block, row, cell, block, …], "off": byteOffset}` (`docs/control-protocol.md`).

CLI recipes (verified usage strings):
```sh
wordcraft-cli convert report.docx report.pdf        # docx, doc [read], pdf, odt, rtf, html, md, tex, txt, json, png, xml
wordcraft-cli convert report.docx out.xml --format wordml2003   # or flatopc (the default Word XML Document)
wordcraft-cli render report.docx out.png --page 2 --scale 2     # scale defaults to 2.0, page to 1
wordcraft-cli text report.docx                      # plain text, list labels kept
wordcraft-cli info report.docx                      # pages, words, paragraphs, properties (JSON)
wordcraft-cli inspect report.docx                   # structure as JSON
wordcraft-cli run --template sample --cmd 'select.text={"text":"Membership"}' \
  --cmd format.bold --save out.docx
wordcraft-cli run --script job.json                 # commands + saves from a JSON file (- = stdin)
wordcraft-cli run --file in.docx --cmd edit.undo --cmd 'file.exportPdf={"path":"out.pdf"}'
wordcraft-cli convert locked.docx out.pdf --password '…'      # agile or Standard encryption; or --password-file / WORDCRAFT_PASSWORD
wordcraft-cli commands --json                       # every command id, label, params, shortcut
wordcraft-cli mcp --author "Claude (copyedit)" \
  --automation-read-root project --automation-write-root project/out
wordcraft-cli zotero refresh paper.docx --save paper.docx
```
Exit status: 0 on success, 1 on error with the message on stderr. A failing `run` writes nothing; `wrote <path>` is printed only after a successful save.

Using a personal template headlessly (no `file.new` template name exists for these):
```sh
wordcraft-cli run --cmd 'file.listTemplates={"dir":"templates"}' --print   # discovery
wordcraft-cli run --cmd 'file.newFromTemplate={"path":"templates/Contract.dotx"}' \
  --cmd 'select.text={"text":"[Client]"}' --cmd 'text.insert={"text":"Acme Ltd"}' --save out.docx
wordcraft-cli run --file out.docx --cmd 'file.saveTemplate={"path":"templates/Acme contract.dotx"}'
```
`file.newFromTemplate` leaves the document untitled and dirty; save it outside the templates folder.

Driving the running app (control channel):
```sh
open -a WordCraft --args --control 7981
cat "$HOME/Library/Application Support/WordCraft/control-key.local-7981"
# then one JSON object per line to 127.0.0.1:7981, e.g.
{"id":1,"key":"<key>","method":"engine.execute","params":{"command":"text.insert","params":{"text":"Hello"}}}
{"id":2,"key":"<key>","method":"engine.execute","params":{"command":"document.inspect","doc":1}}
{"id":3,"key":"<key>","method":"ui.screenshot","params":{"path":"shot.png"}}
```
An unauthorised request gets `{"ok":false,"error":"unauthorized"}` and the connection closes; a line over 1 MiB, or bad JSON, also closes it; a connection with no authorised request within 30 s is closed. `wordcraft-cli mcp --connect` sends the key only to loopback addresses; to drive an app on another machine, forward its port and set `WORDCRAFT_CONTROL_KEY`. Open/Save/Export pick formats by file extension; `--save`/`file.save` over an existing file replaces it in place.

Reading the app's own diagnostics: `<settings>/logs/wordcraft.log` (rotated, 16 MiB cap; `WORDCRAFT_NO_PREFS` runs log to stderr only). Unreadable .docx parts, pictures/fonts a PDF export left out, and recovered panics land there.

## Working with an AI agent

Legitimate, reliable agent work with WordCraft:
- **Do document work headlessly.** `wordcraft-cli mcp`, `wordcraft-cli run` (flags or `--script`) need no window, no focus and no GUI driving. Verify your own work with `inspect_document` / `get_text` / `render_page` instead of screenshots.
- **Work across documents**: open several with `open_document`/`file.new`, address each with `"doc"` (`list_documents` enumerates), close with `file.closeDocument {doc}`.
- **Prepare inputs**: write Markdown/HTML/CSV/text in the shell and bring it in (`open_document`, `insert.textFromFile`, `mailings.recipients` for `.csv/.tsv/.txt` with encoding detection and `.xlsx/.xlsm/.xls/.ods`, `insert.picture` with a path or base64 bytes).
- **Produce deliverables**: convert/export to PDF/ODT/RTF/HTML/MD/tex/txt/PNG from the CLI (docx and pdf in one `run --script`), and hand the `.docx` on for Word.
- **Attribute your edits**: pass `--author "Claude (copyedit)"` (or `file.setAuthor`) so reviewers can tell agent edits from people's, and turn tracking on explicitly with `review.trackChanges {"value": true}`. Under Restrict Editing the author cannot be changed and most `file.*` commands are refused — do not try to work around it.
- **Confine yourself**: run the headless MCP server with `--automation-read-root`/`--automation-write-root` (a missing root grants none of that access; the roots must exist). This also bounds the personal-templates folder.
- **Repair/interpret native projects**: the native format is `.docx` itself; `.json` is the engine's own model (media bytes and opaque parts included as base64). Recovery snapshots are per-document versioned JSON under `recovery/`, taken at most every ten seconds; the newest edits can be lost.
- **Do not**: drive the GUI blind by clicking at guessed coordinates — prefer commands; assume SVG/ICO/HEIC images load (they don't); assume `.doc` can be written (it can't); assume charts, SmartArt, OLE or native ink *from Word* can be edited (they are preserved through saves, not editable); assume `.docx` fidelity on real-world files (gap #1); assume a headless session writes recovery copies (it doesn't); call `ui.saveAsTemplate` headlessly (it opens a system dialog).
- **Watch these footguns**: `file.saveTemplate` appends `.dotx` (`out.docx` → `out.docx.dotx`); `file.new {"template": "MyTemplate"}` silently gives a blank document — use `file.newFromTemplate {"path"}`; `file.listTemplates` without `dir` errors when no folder is saved; `review.trackChanges` without `value` *toggles* (it can turn tracking off in a document saved with it on); `format.highlight` without `color` toggles; `file.close` over the control channel errors on unsaved changes unless `{"force": true}` (which discards them); `ui.key`/`ui.text` replies `{"queued": true}` before the edit has been applied — inspect document/widget state before the next dependent step; a `mcp --connect` bridge that starts first reports "not reachable … will retry on each call" until the app's port opens.

## Verification protocol

Alpha software that never crashes by design but is unproven on real-world files: trust nothing you did not re-open.

1. **Throwaway round-trip first**: new → type/format → save `.docx` → reopen → export `.pdf`, all in a scratch directory (`wordcraft-cli run --template blank --cmd … --save t.docx`, then `wordcraft-cli convert t.docx t.pdf`, then `wordcraft-cli inspect t.docx`).
2. **Never trust a silent export**: the CLI prints `wrote <path>` only after the command returned Ok, and a failing command writes nothing; still check the file exists, is non-zero, and re-read it. PDFs don't open in WordCraft — check a PDF elsewhere, or render the page with `wordcraft-cli render t.docx page.png` and look at the PNG.
3. **Compare structure, not just text**: `inspect`/`document.inspect` shows styles, tables, sections — use it to catch silent loss (the known failure mode is content dropped without a warning; gap #1).
4. **Keep the user's original untouched**: work on a copy; WordCraft's save replaces the file in place (safely, but in place). Recovery copies exist for the desktop app only, are unencrypted, and the newest edits before a crash can be lost.
5. **Version and back up** project files per session; update the app only between projects (the launcher auto-updates; the version you script against may change).
6. **Re-check the command set you script against**: re-read `wordcraft-cli commands --json` on the installed build and look for the ids you call; the repo's documentation counts drift for months (README still says 422 commands vs 648 in code).

## Sources & evidence

- Repo: https://github.com/storytold/wordcraft (org `storytold`), inspected read-only at **tag `v0.12.0`**, commit **`3de6ff95af86c19d67030cd96dba15cd6a45a25e`** ("Release 0.12.0", 2026-10-28), audited 2026-10-29.
- Installed app `/Applications/WordCraft.app` is exactly this release: bundle id `ai.storyteller.wordcraft`, and the binary prints `wordcraft 0.12.0 (3de6ff95)`. If your installed version differs, verify against it (`wordcraft --version`, `wordcraft-cli --version`).
- Key files read: README.md, ROADMAP.md, Cargo.toml, AGENTS.md, craft-i18n.rev, docs/{gaps,file-format-parity,mcp,control-protocol,recovery,zotero,parity-checklist}.md, apps/wordcraft/src/main.rs, apps/wordcraft-cli/src/{main.rs,script.rs,automation_args.rs}, crates/engine/src/{io.rs,catalog.rs,session.rs,file_access.rs}, crates/engine/src/cmd/ (mod, file, tools, user_templates, mailings, view, format, protect, table), crates/docx/src/crypt.rs (agile + Standard), crates/docbin/src/{lib,crypt}.rs, crates/formats/src/{rtf,odt,latex,markdown}.rs, crates/mcp/src/{tools,server,backend}.rs, crates/ui-egui/src/{windows,control,control/handler,dialogs,printing,zotero}.rs, crates/ui-egui/examples/ui_shot.rs, crates/proof/src/lang.rs, crates/control-key/src/lib.rs, crates/zotero/, xtask/src/main.rs.
- Counts were re-measured from this tag's code on 2026-10-29 (see the table and `evidence.md`), and the capability delta since v0.11.0 was established by diffing this tree against the v0.11.0 release source (fetched shallow ref): commands 643 → 648 (+5, none removed), catalog 504/520 → 505/520, MCP tools 16 → 17 (+`list_documents`), control methods 19 → 21 (+`file.close`, `file.exportPng`; `doc` addressing), shortcut-bearing specs 164 → 167, CLI 10/21 → 10/21, proofing 15 → 15, languages 27 → 27, formats unchanged.
- Nothing was built or launched; the clone and the v0.11.0 release source were only read, and the installed app was version-checked from its binary. Where the repo contradicts itself (command counts, dialog count, shortcut count, gap #1) the contradiction is stated in place rather than resolved by guesswork.
