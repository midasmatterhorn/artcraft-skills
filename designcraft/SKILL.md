---
name: designcraft
description: DesignCraft is the ArtCraft team's clean-room, open-source InDesign-class page-layout app (pure Rust; `.designcraft` project format; IDML/INDD/INDT import; PDF/X-4 and PDF/X-1a export, PDF/A-2b, EPUB with Split Document, editable PPTX, HTML, PNG and JPEG export; batch export of layouts and versions; preflight; headless CLI, MCP server and JSON control channel). Trigger this skill whenever the user mentions DesignCraft — or a `.designcraft`, `.idml`, `.indd`, `.indt`, `.dcbook`, `.dclib`, `.ase` or command-script file — asks what it can or cannot do, which formats it opens or writes, its keyboard shortcuts, how to automate or script it, how to prepare or convert assets for it, how to place PDFs and choose their layers, how to thread text or target a table by id, how to check links, how to verify or repair its output, or how to troubleshoot it. Also trigger when the job is described without naming the app — "lay out a magazine", "thread this story across three columns", "set this on a baseline grid", "export a PDF/X-4", "export a press-ready PDF/X-1a", "export every layout and version at once", "make an EPUB from these pages", "split the EPUB into chapters", "batch-export every page to PNG", "place these photos in a brochure", "hide a layer of this placed PDF", "convert these text variables to text", "import my InDesign shortcuts", "why did my white object vanish on press". Do not guess its capabilities from InDesign knowledge — read this first.
---

# DesignCraft

**Audit basis.** Refreshed 2026-11-12 against tag **v0.20.1**, commit **`33a467872268c98536231491865b4011b0275b17`** — `git rev-parse HEAD` in the pinned checkout confirms, and the installed `DesignCraft.app` bundle matches (`CFBundleShortVersionString 0.20.1`, `DesignCraftBuildCommit` the same SHA; the bundled CLI prints `designcraft-cli 0.20.1`, the desktop binary `designcraft 0.20.1`). The previous release this skill described was v0.18.0 (`58ac6d29b260e033f4291afc4318b507cfd90fd9`).

**v0.18.0 → v0.20.1 delta.** 146 files changed, +8007/−658, and **no registry change**: 555 engine command ids, 190 UI command rows, 26 MCP tools, 11 CLI subcommands and format version 4 are all unchanged at v0.20.1 (re-measured; the live registry returns 555). What moved is behaviour. **Anchored text frames now own their stories**: copy, paste (also into another document, carrying placed graphics), duplicate, release and delete keep each frame's story and ids, nested up to 64 deep (`crates/doc/src/anchored.rs`, `crates/engine/src/cmd/anchored.rs`). The **Links panel** checks file status on a worker thread (2 s minimum poll, at most 4 workers) and the document stores each link's size and time, so an unchanged graphic on a network share is not re-read — the network-path stall (#1444) — while `links.list` keeps its result shape (`crates/ui-egui/src/links_worker.rs`, `crates/engine/src/cmd/links.rs`, `crates/doc/src/assets.rs`). **Preflight gains `whiteOverprint`**: white or [Paper] fills, strokes, gaps, ruby and kenten set to overprint are reported, because they vanish on press (`crates/engine/src/cmd/preflight/white_overprint.rs`). **Page commands now validate and count**: `layout.pages.delete` returns `{deleted}` and `layout.pages.applyParent` `{applied}`; an index past the last page is an error instead of being dropped (`crates/engine/src/cmd/layout/registry.rs`). **Scripts are bounded** — depth 8, 100 000 steps across nested scripts, 16 MiB per `${…}` interpolation, 64 MiB per `$N.path` copy, 256 MiB per resolved step parameter tree (`crates/engine/src/script.rs`). **Table commands with `story?`/`table?` run without a table selection**, defaulting to the whole table (`crates/engine/src/cmd/table/target.rs`, `docs/mcp.md`). Hardening: GREP refuses subroutine calls and bounds empty-match scans (`crates/compose/src/grep.rs`); whole-file reads refuse devices and FIFOs and cap at 4 GiB (`crates/engine/src/io.rs`); recovery entries refuse links (`crates/engine/src/recovery.rs`); package copies the bytes it loaded (`crates/engine/src/cmd/package.rs`); hyperlink and data-merge ranges follow story edits (`crates/doc/src/edit.rs`); DOCX signed character references are dropped, XLSX signed row numbers are rejected and RTF header/footer groups are skipped on import (`crates/textimport/src/`). Typography and UI: the stale preflight warning that PDF export drops ruby and kenten overprint is gone (the export writes it, as `docs/cjk.md` now says), arrowheads on curves point the right way, a graphic implicitly placed with a line or open path selected gets its own frame and leaves the line alone, and the canvas draws a spine hairline where a spread's pages meet (screen only, never exported — `crates/doc/src/page.rs`, `crates/ui-egui/src/canvas/page_decor.rs`). pt-BR is ~100% translated (the maintainers' 2,936-of-2,939 report) and Russian is listed; the updater installs at exit and reports installing/ready/installed/failed, with the Flatpak update permissions repaired in 0.20.1 (`crates/ui-egui/src/updates_ui.rs`, `packaging/linux/flatpak/`).

**Verify against your installed version** — the ArtCraft Launcher auto-updates, so a newer build may differ; every count quoted here was re-measured at this tag, and code paths that moved were re-cited. The measurement method for each count is in `evidence.md`.

**v0.17.0 → v0.18.0 delta.** 214 files changed; +8 engine command ids, +3 UI commands, nothing removed: `file.exportBatch`, `file.exportPresets`, `file.saveExportPreset`, `file.deleteExportPreset`, `layout.alternate.duplicate`/`.delete`/`.options`, `layout.parents.duplicate`, and UI `app.exportBatch`, `app.parentOptions`, `app.alternateLayoutOptions`. **File ▸ Export Layouts and Versions** writes several alternate layouts and versions at once — PDF (marks, bleed, spreads; `standard: none|x4|a2b`), PNG or JPEG — one folder per version, a `{document}/{layout}/{version}/{date}` template, at most 5 000 files and 24 versions, in a DesignCraft export preset (not Adobe `.joboptions`). PDF and PowerPoint exports warn about text their pages had no room for; IDML round-trips a document's hyperlinks; the macOS DMG bundles `designcraft-cli` inside the app; the CLI gains `thumbnail` and `validate-pdf --standard`; the native reader stops charging stored assets against the deflate budget; hyphenation adds Danish. Deep automation detail — CLI flags, script syntax and limits, all 26 MCP tools, the control methods, coordinates, guide and column geometry, layer options, EPUB splitting, table targeting, shortcut import — is in `references/agent-surfaces.md` next to this file.

## Overview

DesignCraft is a page-layout and publishing application written from scratch in Rust: "an open-source, modern desktop publishing and page layout studio" (`README.md`). It aims at full Adobe InDesign 2026 parity — "faster, open (documented JSON format + IDML), scriptable by agents (MCP), and available on the web" (`ROADMAP.md`) — as a clean-room application (`AGENTS.md`). It runs natively on macOS, Windows and Linux, and in a browser as WebAssembly (`README.md` §Web, `apps/designcraft-web`). The UI runs on egui 0.37 with craft-ui's shared docking. Maturity is **pre-alpha**: the alpha gate is still blocked by fixes to Smart Text Reflow on the Primary Text Frame (#165), ~5–7 h away (`ROADMAP.md:3`, `docs/gaps.md` §0); the maintainers estimate ~80% feature breadth and ~47% "ready for real work" (`docs/target-app-parity.md` §Headline). Source: GitHub `storytold/designcraft`, MIT OR Apache-2.0 (`Cargo.toml`), a layered Cargo workspace enforced by `cargo xtask layers`; shared craft-libs crates provide printing, ICC colour management, atomic writes, PDF writing (overprint/knockout/CMYK blending and spot gradients, plus the craft-prepress flattener for PDF/X-1a) and document-path policy (`Cargo.toml`).

The one idea that governs everything: **every user-visible action is a command** with a stable id and JSON parameters (`crates/engine/src/cmd.rs` `command_specs`), and the UI, CLI, control channel and MCP all go through `Session::execute` (`crates/engine/src/lib.rs`). Prefer commands over GUI poking.

## Capabilities (verified)

### Layout, guides and the document model — implemented
- Facing/non-facing spreads, parent (master) pages with page-number markers, sections, layers, and frames typed text / graphic / unassigned; stories threaded across frames and spreads (`crates/doc/src/{page,story}.rs`; `crates/engine/src/cmd/{layout,thread}.rs`).
- Document setup, page-size presets (incl. A0–A2 posters), bleed/slug, start page, Page tool for pages of their own size (`layout.documentSetup`, `layout.pageSize`, `file.new`).
- Multi-document tabs: `file.activate {index}`, `document.list`, next/previous document (`Cmd+F6` / `Cmd+Shift+F6`) — `crates/engine/src/cmd/file.rs`, `crates/ui-egui/src/menus/`.
- **Page commands count what they did:** `layout.pages.delete {pages: [0-based indices]}` → `{deleted}`, `layout.pages.applyParent {pages, parent}` → `{applied}`; both refuse an index past the last page and a non-integer list entry (`crates/engine/src/cmd/layout/registry.rs` `page_indices`).
- **Ruler guides:** `guide.add` (horizontal/vertical/both; page, spread or liquid guide), `guide.list`, `guide.select`, `guide.selectAll` (`Cmd+Alt+G`), `guide.deselect`, `guide.move`, `guide.moveBy`, `guide.delete`, `guide.deleteAll`, `layout.createGuides` (`crates/engine/src/cmd/guides.rs`; caps 10 000 guides, rows/columns ≤ 1000). Guides are selected like objects and a dragged guide snaps along its axis; Shift snaps to ruler ticks (10× the tick spacing), Cmd suspends snapping. A drawn or resized edge also snaps to the page's centre line.
- **Custom column guides:** a page keeps dragged column positions (`Columns.positions`, `crates/doc/src/page.rs`), `layout.moveColumnGuide {page, gutter, position, spread?|parent?}`, at most 216 columns (`MAX_COLUMNS`); `view.lockColumnGuides` is a document setting, **on by default**, saved in the document and IDML; `view.lockGuides` (`Cmd+Alt+;`) only stops pointer dragging.
- **Page view history:** `view.goBack` (`Cmd+PageUp`) / `view.goForward` (`Cmd+PageDown`) retrace page jumps at the current zoom (`crates/ui-egui/src/page_history.rs`).
- **Spread spine:** the canvas draws a hairline at each edge where two pages of a spread meet, in the spread edge's colour; right-to-left spreads and unequal page heights are handled, pages that do not touch get none. It is screen decoration only — never printed or exported (`crates/doc/src/page.rs` `page_seams`, `crates/ui-egui/src/canvas/page_decor.rs`).
- Styles (paragraph, character, object, table, cell, groups), swatches (process/spot/tints/gradients), text wrap, corner options, transparency effects, ICC colour management with working spaces and proof setups.
- Interactions: Pathfinder boolean ops, compound/clipping paths, gradients, stroke styles/arrowheads, tables with merges and graphic cells (gradient cell fills draw as gradients on screen and in PDF), footnotes, endnotes, notes, cross-references, index, TOC, text variables, conditional text, track changes, data merge, XML tags/DTD, articles, object libraries, books, object states, buttons and form fields, page transitions, Flex Layout.
- Generators: QR codes (`object.qrCode`), math expressions (`math.insert`/`math.svg`), colour themes from a placed image (`color.extractTheme`), live captions (`object.caption`).
- Graphics: placed rasters, PDF pages, SVG, PSD composites, EPS previews, image clipping paths read from IDML (`crates/images`, `crates/render`, `crates/idml/src/import.rs`).

### Placed PDFs and placed-graphic layer options — implemented, rendering caveat below
- **Object Layer Options** distinguishes a placed PDF's own defaults from an explicit choice: `object.layerOptions {ids?, hidden: [name], useDefaults?}` where `useDefaults: false` with `hidden: []` means *explicitly all on*, and legacy `hidden: []` resets to file defaults (`crates/engine/src/cmd/pdflayers.rs`). `object.pdfLayers {id?}` lists `{name, visible, default, overridden}`.
- Every explicit choice is validated with one real visibility rewrite per distinct source **before** any item is edited or undo recorded, so a mixed selection stays atomic and a PDF that lists layers but cannot be rewritten is refused.
- Output honours the choice: plain and PDF/X-4 exports keep vector artwork and optional content with per-placement overrides; booklet and book-merge output included; PDF/A-2b applies the choices to an export-only 300 ppi raster copy; embedded IDML stores a separate PDF variant per placement while external-only IDML export rejects active choices; `file.package` reports a placement whose choice an IDML copy cannot carry.
- **IDML `GraphicLayerOption`/`GraphicLayer` settings are retained per placement**; retention is not layer-aware rendering — read **Known limitations** before promising appearance fidelity.

### Text engine — implemented
- Knuth–Plass total-fit paragraph composer plus a single-line composer, with a shared compose cache; optical kerning measured from glyph outlines (`crates/compose/src/`).
- Dictionary hyphenation (Moby list + trained Liang patterns), language-dependent quotes, bidi/RTL with kashida and digit substitution, CJK composition with mojikumi/kinsoku, vertical type, ruby, kenten, warichu, tate-chu-yoko.
- **Anchored text frames own their stories.** A text frame anchored in text (also inside an anchored group, a footnote or a table cell) is in its story's thread like a page frame; copy, paste (also into another document, with the graphics it places), duplicate, release and delete keep story and ids consistent, nested up to 64 (`crates/doc/src/anchored.rs`, `crates/engine/src/cmd/anchored.rs`).
- **Hyperlink and data-merge ranges follow edits:** `Document::adjust_text_ranges` shifts story-external source ranges on insert/delete/replace, so editing text no longer leaves a link on the wrong bytes (`crates/doc/src/edit.rs`, `crates/engine/tests/hyperlink_offsets.rs`).
- **Story-level Optical Margin Alignment:** `story.options {story?, frame?, opticalMargin?, opticalMarginSize?}` sets hanging punctuation/edges for every paragraph of a story except paragraphs with `ignoreOpticalMargin`; the **Story** panel and `type.selectionAttrs.storyOptions` expose it, and IDML carries `StoryPreference` (`crates/engine/src/cmd/text.rs`).
- Hyphenation Settings (`app.hyphenationDialog`) sets limits, zone, the Better Spacing ↔ Fewer Hyphens slider, Hyphenate Capitalized/Last Word/Across Column and Preview as one undo step.
- **Bulleted/numbered list buttons:** `list.bullets` / `list.numbers {on?}` apply InDesign's default hanging indent and remove it again (`crates/engine/src/cmd/lists.rs`).
- **Notes:** `note.convertFromText {author?}`, `note.next`, `note.previous`, and `note.split`; deleting a note or converting it to text keeps the caret on the same text; footnote caret edits no longer drop untyped formatting (`crates/engine/src/cmd/editorial.rs`).
- **Convert Variable to Text:** `variables.convertToText` and `variables.convertAllToText {name}` replace each instance with the value it shows on its page; the variable stays defined.
- **Key Object for alignment:** `selection.key {id}` makes a selected item the key object (needs ≥ 2 selected); `object.align`'s `to` defaults to `keyObject` while one is set.
- Column rules (top line's ascent to the bottom line's descent) and Span Columns, Paragraph Rules above/below, Based on Parent, custom anchored objects with **Relative to Spine**.
- **Story Editor depth ruler:** View › Story Editor › Show/Hide Depth Ruler (`view.storyEditorDepthRuler`), as in InDesign (`crates/ui-egui/src/story_editor.rs`).
- Fonts: own font DB, shaping (harfrust), outlines (skrifa), variable-font instances, `Document Fonts` folders beside a document (case-insensitive, and a bare document filename looks in the current directory), missing Korean sans falls back to a sans face, and Type › Reload Fonts (`font.reload`).

### Preflight and links — implemented
- **`preflight.run {minPpi?}`** returns `issues [{severity, kind, message, item?, page?}]`: overset/unplaced text, missing fonts and glyphs, missing or low-resolution graphics, RGB content in print documents, empty text frames, unsupported placed-graphic layers, and now **`whiteOverprint`** — a fill, stroke, stroke gap, ruby or kenten in [Paper] or a colour that lays down no ink, set to overprint, which would disappear on press. White text in a frame set to Overprint Fill still knocks out and prints and is not reported; `[None]`, gradients and spot inks above a 0% tint are not white (`crates/engine/src/cmd/preflight.rs`, `crates/engine/src/cmd/preflight/white_overprint.rs`, #2401).
- **Links:** `links.list` returns every used placed graphic with `{asset, name, path, status: ok|modified|missing|embedded, refused?, pixels, pdfCrop?, uses: [{id, page, ppi}]}` and linked text files with `{story, name, path, status (also tooLarge), edited, uses}`. The panel's statuses come from a background worker so a dead network share cannot freeze the UI; the document keeps the size and time of the file each link's bytes came from, so once recorded an unchanged link needs no read, even on the first check after opening. The command itself is synchronous (`crates/engine/src/cmd/links.rs`, `crates/ui-egui/src/links_worker.rs`, `crates/doc/src/assets.rs`).

### Import / open — implemented
`file.open` decides by content, not extension (`crates/engine/src/cmd/file.rs` `open_path`):
- Native `.designcraft` (zip or legacy single JSON) — `crates/format`.
- `.idml` InDesign Markup imported into the native model — `crates/idml/src/import.rs`; `.indd`/`.indt` converted to IDML in memory by `storytold/indd-utils` (real-file fidelity unmeasured — `docs/gaps.md` §2).
- Placed graphics: PNG, JPEG, GIF, WebP, TIFF, BMP, PSD/PSB composite, SVG, PDF (any page, crop-box choice), PDF-compatible Illustrator files detected as PDF, EPS (TIFF preview or placeholder — no PostScript interpreter; a DOS EPS TIFF preview is read where the spec puts it) (`crates/images/src/lib.rs`, `crates/images/src/eps.rs`).
- Text: `.txt`/`.text` (UTF-8 or UTF-16), `.md`, `.docx`, `.rtf`, `.xlsx` (first used range becomes a table), Tagged Text; Data Merge sources CSV, TSV, text, `.xlsx`. The importers are strict about malformed input: DOCX signed numeric character references are dropped, XLSX signed row numbers are rejected, and RTF header/footer groups (`headerl`, `headerr`, `headerf`, `footer*`) are skipped (`crates/textimport/src/{docx,xlsx,rtf}.rs`).
- Media (poster/placeholder frames, no playback): mp4, m4v, mov, webm, ogv, mp3, m4a, wav, ogg, oga, aac.
- Swatches `.ase`, ICC `.icc`/`.icm`, XML (with DTD), libraries `.dclib`, books `.dcbook`, and a page of an IDML or `.designcraft` document (`file.place {layoutPage}`) as a group of objects.
- `file.openRecent {index}` backs File › Open Recent (at most `recentFilesMax`, default 20).
- Whole-file reads (open, place, import) accept **regular files only, at most 4 GiB**; a device, FIFO or endless stream returns an error instead of hanging (`crates/engine/src/io.rs`).

### Native format — implemented (format version 4, unchanged at v0.20.1)
`.designcraft` is a zip (`crates/format/src/lib.rs`): `mimetype` (stored, first), `document.json` (pretty JSON), `assets/` entries (byte-for-byte, each file once), `meta.json` (format version and generator) and an optional `preview.png`. Latest reader capability is **version 4**: it covers retained placed-graphic layer options and explicit all-on placed-PDF layer choices. `required_version` pins a file to 4 only when it needs one of those, else keeps 2 or 3 so older readers still open it. Readers upgrade older versions and still open the legacy single-JSON form. Read limits: 100 000 entries, 256 MiB `document.json`; deflated entries share a 4 GiB expansion budget (1 GiB per deflated asset), while a **stored** entry — a placed image, as the writer stores them — is read at its size in the archive and charged to the archive's own size instead, so a saved document opens at any placed-image size. A document with non-finite geometry cannot be saved. Writes are atomic.

### Export — implemented
- **PDF** (`file.exportPdf`): real selectable text with embedded font subsets, DeviceCMYK/RGB/Gray, spot `/Separation`, bleed boxes, crop/bleed marks and page info, pages or spreads, `standard: "none" | "x4" | "x1a" | "a2b"` (**PDF/X-1a:2003** — the PDF/X-4 print file flattened by craft-prepress, with overprint/knockout and CMYK blending preserved), tagged structure tree, transparency flattening, hyperlink annotations and outlines, interactive options, `created` (Unix seconds) for reproducible files, `file.printBooklet` imposition. **PDF export writes the File Info title, author, description and keywords** (`file.info`); it also writes ruby and kenten overprint. **It warns about text the exported pages had no room for** — read `warnings`; the same applies to PowerPoint export (`crates/engine/src/cmd/preflight.rs` `overset_warnings`).
- **PDF/X checks:** `designcraft-cli validate-pdf FILE.pdf [--standard x4|x1a]` prints `{path, standard, valid, issues, warnings}` and exits non-zero on failure; without `--standard` it picks the standard from the file's own `GTS_PDFXVersion` (PDF/X-1a:2003 gets the 1a checks). Checks include PDF version, output intent, Info/XMP identification, interpolation, encryption, trim boxes, Type 3 fonts, device RGB under a CMYK output intent, and fonts that draw visible text without an embedded font program (including inside placed PDF forms), with font names and pages; render-mode-3 invisible text is exempt (`crates/pdf/src/pdfx.rs`, `crates/pdf/src/pdfx/fonts.rs`, `crates/pdf/src/pdfx1a.rs`).
- **Inks and separations:** the document's inks are a `craft_prepress::InkSet` (four process inks plus each spot swatch; `crates/pdf/src/inks.rs`); **Separations Preview shows the exported PDF's plates, spot plates included** (`ink.separations`).
- **Export Layouts and Versions** (`file.exportBatch`): one job writes several **alternate layouts** and several **versions** at once — PDF (marks crop/bleed/page-info, spreads, `standard: none|x4|a2b`, `ppi`, `quality`), PNG or JPEG — with a `{document}/{layout}/{version}/{date}` name template, a folder per version by default, `dryRun` to list the files only; at most 5 000 files, 24 versions, 120-character names. Jobs are saved as DesignCraft export presets (100 max; `file.exportPresets`, `file.saveExportPreset`, `file.deleteExportPreset` — not Adobe `.joboptions`).
- **EPUB 3** reflowable (`file.exportEpub`) and fixed layout (`file.exportFixedEpub`). **Split Document:** `document.epubSplit {split?}` stores off / before each export-tagged paragraph / before each paragraph of one style; `file.exportEpub {split}` overrides it for one export and `style.exportTag {split}` marks the styles; navigation and note links point across the files. CSS class names for styles that slug alike are numbered uniquely even across thousands of names (`crates/epub/src/css.rs`).
- **HTML** (`file.exportHtml`): one self-contained page, styles as CSS, images embedded, stories and graphics in reading order; returns `warnings`.
- **PowerPoint** (`file.exportPptx`): every page becomes a slide of editable shapes, pictures, tables and text boxes; `lineBreaks: keep|reflow`, `rasterize` (default true), `embedFonts` (default true); approximations and text its slides had no room for are reported in `warnings`.
- **PNG / JPEG** of a page via the renderer (`designcraft-cli run --export out.png`, `--all-pages DIR`; MCP `render_page` / `export_png`; control `ui.render`). `render_page`/`export_png` page 0 is the first page — the same page is position 1 in `file.exportPdf`'s `pages`.
- **IDML** (`file.exportIdml`, `embedImages`) carrying the document's **hyperlinks** (page destinations, page-item and text sources) — **Text** `.txt`/`.rtf`/tagged (`file.exportText`), **XML** (`file.exportXml`). IDML import keeps a hyperlink on a page item or a text run.
- **Print** (`file.print`, `file.printers`, `dryRun`, `created`) through the shared `craft-print` spooler — `docs/gaps.md` §10.

### Automation surfaces — implemented
- **CLI** `designcraft-cli` (`apps/designcraft-cli/src/main.rs`): `run`, `commands [FILTER]`, `describe COMMAND`, `script`, `app`, `mcp`, `perf`, `bench`, `validate-pdf`, `thumbnail`, `links`, `--version` — **11 subcommands, unchanged at v0.20.1**. On macOS the app bundle installs it at `Contents/MacOS/designcraft-cli` (`docs/mcp.md`); a separate `designcraft-cli-<version>-macos-universal.zip`, `cargo install --path apps/designcraft-cli --locked`, or `cargo build --release -p designcraft-cli` are the alternatives. `mcp` takes `--automation-read-root`/`--automation-write-root` more than once, in `--flag DIR` and `--flag=DIR` spellings; a non-UTF-8 MCP line answers a parse error instead of dying.
- **MCP server** `designcraft-cli mcp` — stdio JSON-RPC, protocol 2025-06-18 (older revisions accepted), **26 tools, unchanged at v0.20.1**: command discovery/execution (`list_commands`, `execute`, `batch`), document I/O and inspection (`inspect_document`, `get_story`, `set_story_text`, `new_document`, `open_document`, `save_document`, `place_image`), rendering (`render_page`, `export_png`, `screenshot`), input/UI tools (`select_tool`, `pointer`, `key`, `type_text`, `ime`, `click`, `drag`, `menu_list`, `ui_inspect`, `ui_set`, `dialog_set/confirm/cancel`). Read/write root flags confine every path a command touches. Every input schema is **closed** (`additionalProperties: false`) and keys are checked at every level, so a misspelt key in a `batch` step, a `pointer` event or `mods` is an invalid-params error naming its path; every tool carries all four MCP hints (`crates/mcp/src/tools.rs`, `server.rs`).
- **Control channel**: `designcraft --control PORT` serves JSON lines on `127.0.0.1` only; 4 MiB line limit, 16 connections, no authentication (`docs/control-protocol.md`). `crates/ui-egui/src/control.rs` and `apps/designcraft/src/control_server.rs` are byte-identical to v0.18.0: **28 dispatch arms / 31 accepted method strings** (30 dotted names plus the `command` alias), unchanged at v0.20.1. The earlier "27 methods" figure was an undercount; use `engine.commands` / `ui.inspect` to discover live behaviour.
- **Scripts**: one command per line with `$N.path` references to earlier results (`crates/engine/src/script.rs`; `script.run {text}`). A compact line's parameters must be a JSON object (`command.id {...}`, `command.id={...}`), not bare values. The Scripts panel runs a script as one undo step and restores the document on failure. Bounds at v0.20.1: nesting depth 8, 100 000 steps for a script and the scripts it runs, 16 MiB per `${…}` interpolation, 64 MiB per `$N.path` copy, 256 MiB per resolved step parameter tree (`MAX_SCRIPT_DEPTH`, `MAX_SCRIPT_STEPS`, `MAX_INTERPOLATED_BYTES`, `MAX_REFERENCED_BYTES`, `MAX_STEP_PARAM_BYTES`).
- **Tables without a selection:** a command whose params list `story?` and `table?` runs with `table` (the id `table.insert`/`table.get` return) and optionally `story`, even when nothing in a table is selected; without a cell range it targets the whole table. A missing table, or one not in the given story, is an error (`crates/engine/src/cmd/table/target.rs`, `docs/mcp.md` §Tables without a selection).
- **Shortcuts on the shared craft-keymap crate:** panel shortcuts and **editable tool keys**, the shared **Keyboard Shortcuts dialog with shortcut sets** (`window.shortcutSets`), and InDesign shortcut import (`window.importShortcuts {path | text}`) which reads an InDesign Show Set `.txt` (UTF-8/BOM or UTF-16; ≤ 8 MiB), applies its Default context, and reports `{set, imported, changed, conflictsCleared, skipped, unmatched, unmatchedWithoutShortcut, unreadable}` (`crates/ui-egui/src/shortcut_import.rs`, `crates/ui-egui/src/menus/keys.rs`).
- Surface size at this tag: **555 engine command ids** (the live registry — `designcraft-cli commands` returns 555 entries; the same set extracted from `cmd!(` in `crates/engine/src`) and **190 UI command rows** in `UI_COMMANDS` (`crates/ui-egui/src/menus/ui_commands.rs`) — **both unchanged at v0.20.1** (v0.17.0: 547 + 187; v0.18.0: 555 + 190). MCP stays 26 and the control surface is byte-identical. Discover the live list with `designcraft-cli commands` and `describe`.

### Platforms — implemented
- macOS, Windows, Linux native (`apps/designcraft`); WebAssembly web build via trunk (`apps/designcraft-web`: WebGPU with a WebGL2 fallback, `?webgl` to force it, `?sample` for the sample magazine). The web build has no control channel, and Save/Export download files instead of writing them. Runtime environment variables: `RUST_LOG`, `WGPU_BACKEND`, `WGPU_POWER_PREF`, `WGPU_ADAPTER_NAME`, `WGPU_VALIDATION_INDIRECT_CALL`, `DESIGNCRAFT_CONTROL_PORT`, `DESIGNCRAFT_CONFIG_DIR`, `DESIGNCRAFT_NO_PREFS`, `DESIGNCRAFT_NO_NATIVE_MENU`, `DESIGNCRAFT_WAYLAND` (Linux). Windows installs per-user by default.

## Known limitations and not-implemented

Ranked shortfall list: `docs/gaps.md` (kept current by the maintainers — read it before promising work). Headline items at this tag:

- **Pre-alpha.** The alpha gate is blocked by Smart Text Reflow on the Primary Text Frame adding pages users cannot delete (#165). Threading by hand and autoflow fill-the-following-pages-first work.
- **Basic canvas editing still fails for some users** — object copy/paste on Windows and Linux, right-click context menus, formatting at a caret discarded (`docs/gaps.md` §1).
- **Placed graphic layer options are retained, not rendered.** IDML per-placement layer visibility is preserved and warns on import/preflight/PDF export, but the renderer and PDF exporter still use the asset's composite/default appearance; layer-comp choices and a layer-options UI are missing. Placed **PDF** layer choices *are* applied — do not generalise that to IDML/PSD layer options.
- **INDD/INDT opening is unmeasured on real files**; **INDB/INDL are not read**; no QuarkXPress import. **IDML round-trip is not proven on real files** — opened IDML can reflow.
- **EPS is preview-only** — no PostScript interpreter. **No ExtendScript/UXP compatibility**: InDesign scripts do not run; the script language is DesignCraft's own command language. **No plug-in model**. **No in-app media playback**.
- **PDF standards:** PDF/X-1a:2003, PDF/X-4 and PDF/A-2b exist, but there is still no PDF/X-3, PDF/UA validation, Adobe `.joboptions` presets, or output-intent choice beyond the built-in profile; PostScript printing is absent. **Placed-PDF font repair is missing** (gap 28): export and `validate-pdf` *detect and name* visible unembedded fonts, but nothing embeds, substitutes or outlines them automatically.
- **HTML export is one basic page; fixed-layout EPUB writes page images** rather than live text and CSS; neither output has animation or timing (gap 17).
- **Hyphenation** is bundled for English, Danish, Dutch, French, German (2006 reform only), Greek, Italian, Norwegian, Portuguese and Spanish — **10, unchanged at v0.20.1**; **spelling** is English only (gap 13). Esperanto is a text language (quotes, locale) but has no hyphenation (#1201), and German 1901/traditional variants fall back to no hyphenation. **No screen-reader exposure**; PDF/UA unverified (gap 25).
- **Alternate layouts are page-range copies, not liquid redesigns**: `layout.createAlternate` copies the source layout's pages at the new size and objects follow the liquid (auto-fit) rules; `layout.alternate.options` only renames or resizes them, and a layout's pages keep their source pages' parents. **Export Layouts and Versions** writes PDF/PNG/JPEG only (`standard` none/x4/a2b — no X-1a, EPUB, HTML or PPTX in a batch job).
- **Startup crashes and blank canvases on some GPU/driver combinations** remain a partly mitigated class (backend fallback + `gpu.json` skip list; gap 5). v0.20.1 also asks the adapter for its largest buffer as well as its largest texture side, which removes one large-frame panic (`apps/designcraft/src/gpu_limits.rs`) but does not close the gap. **Performance**: no incremental composition and no GPU raster — the canvas is CPU-rendered with `vello_cpu`, the GPU only composites the UI (gap 20).
- **Font discovery** still misses fonts that some services/managers activate; disk changes are noticed only on request (`font.reload`) (gap 6).
- **Localization** is partial, and the old percentages were stale: **15 non-English interface languages** are selectable, unchanged at v0.20.1 (`crates/ui-egui/src/i18n.rs` `LANGUAGES`). pt-BR is **2,936 of 2,939 strings (~100%)**, AI-drafted with native-speaker review still pending; the maintainers' 2026-11-04 report gives Japanese 95%, Arabic 85%, French/German 83%, Czech 69%, Italian 68%, Ukrainian 65%, Polish 64%, Hungarian 65%, Russian 63%, Georgian 98%, Swedish 98%. Hindi, Indonesian, Korean and Vietnamese interfaces are absent. A missing string shows English and fails no check.
- **Scripts have hard limits**: nesting depth 8, 100 000 steps across nested scripts, 16 MiB per interpolation, 64 MiB per reference, 256 MiB per resolved step. A generated script that pastes a story into itself stops with an error rather than growing until memory runs out (`crates/engine/src/script.rs`).
- **GREP styles and Find/Change refuse subroutine calls and recursion** (`\g<name>`, `\g<1>`, `\g<-1>`): the pattern errors instead of compiling, because the regex engine inlines each call. Empty-match scanning is also budgeted, so a pattern that only matches empty can return fewer matches than the paragraph length (`crates/compose/src/grep.rs`).
- **Whole-file reads refuse non-regular files**: `file.open`, `file.place` and every whole-file read reject a device, FIFO or other endless source and anything over 4 GiB; use a regular file (`crates/engine/src/io.rs`). Capped reads (some importers) still stop at their own cap but can open a device.
- **Link statuses can lag**: the panel shows the last statuses a worker found until new ones arrive, so right after renaming a file on a slow share the panel may still say OK. Poll with `links.list` when the answer must be current; it is synchronous.
- **Shortcut limits**: the InDesign importer reads only Show Set `.txt` (not `.indk`), applies only the Default context (Text for type/text commands), and rejects macOS Control-key chords; editing tool keys and managing sets happens in the Keyboard Shortcuts dialog, not the importer (`crates/ui-egui/src/shortcut_import.rs`, `menus/keys.rs`).
- **Custom column guides** are horizontal column gutters only; locked by default and `layout.moveColumnGuide` refuses while locked; changing column count or gutter discards the custom positions; a page that changes side of the spine mirrors them.
- **`file.close` is not a safe "close tab"**: it closes without asking and discards the document's recovery data. The UI's File ▸ Close / tab × asks when the document is dirty; `app.quit` asks per dirty document, while the control method `app.quit` quits without asking.
- **Claimed but unverified**: README says "every menu item, tool gesture, panel control and dialog" can be driven over the control channel and MCP. The command registry and control methods are broad, but this audit did not launch the GUI; treat a specific dialog as unverified until `ui.dialog.open` / `ui_inspect` confirms it.
- **Stale documentation to distrust**: `docs/target-app-parity.md` still quotes old command counts (446 engine + 99 UI, and ~200); `docs/agents.md` and the CLI's `SCRIPT_HELP` say most commands ignore unknown parameters, while the CLI, MCP and control channel reject them; `docs/localization-parity.md`'s "Other shipped languages" table still prints pre-catalogue percentages. Verify with `designcraft-cli describe` against your build.

## How to operate

### Launch on macOS
- GUI: `open -a DesignCraft` (bundle id `ai.storyteller.designcraft`); to open a file: `open -a DesignCraft brochure.designcraft`. The executable inside the bundle is `Contents/MacOS/DesignCraft`.
- Real flags of the desktop binary (`apps/designcraft/src/main.rs`): `--sample`, `--control <port>` (also `DESIGNCRAFT_CONTROL_PORT`), `--version`, `--gpu-skip=<list>` (internal restart bookkeeping), plus any number of file paths.
- **The CLI ships inside the macOS app bundle** at `Contents/MacOS/designcraft-cli`; the separate `designcraft-cli-<version>-macos-universal.zip` asset still exists, as do `cargo install --path apps/designcraft-cli --locked` and `cargo build --release -p designcraft-cli`. An independently installed CLI is not changed by app updates; the bundled one is.
- State lives in the app's settings folder (`~/Library/Application Support/DesignCraft/` on macOS): `ui.json`, `prefs.json`, `logs/designcraft.log` (rotates, 16 MiB cap), `gpu.json`, and `Recovery/`. `portable.txt` next to the app switches to a `DesignCraftData` folder; `DESIGNCRAFT_CONFIG_DIR` overrides both.

### CLI reference (exact, from `apps/designcraft-cli/src/main.rs`)
```
designcraft-cli run [--in FILE(.designcraft|.idml|.indd|.indt) | --sample] [--cmd ID[=JSON]]...
                   [--page N] [--scale S] [--pdf-options JSON] [--export OUT] [--all-pages DIR]
designcraft-cli commands [FILTER]          # engine commands as JSON; FILTER matches id/label/menu
designcraft-cli describe COMMAND           # label, menu path, shortcut and parameters of one command
designcraft-cli script [FILE|-] [--in FILE | --sample] [--connect PORT] [--save OUT]
                       [--export OUT] [--keep-going] [--help]
designcraft-cli app [--port PORT] COMMAND [JSON] | app --method METHOD [JSON]
designcraft-cli mcp [--connect PORT] [--sample] [--automation-read-root DIR]... [--automation-write-root DIR]...
designcraft-cli perf [--pages N] [--runs N] [--strict]
designcraft-cli bench FILE [--runs N]
designcraft-cli validate-pdf FILE.pdf [--standard x4|x1a] | thumbnail FILE.designcraft OUT.png [SIZE]
designcraft-cli links | --version
```
- `--page`, `--scale` and `--pdf-options` apply to the `--export`s that **follow** them; one left after the last export is an error.
- `--export` picks the writer from the extension: `.png`/`.jpg`/`.jpeg` (a page), `.pdf`, `.designcraft` (Save As), `.idml`, `.epub`, `.pptx`, `.html`/`.htm`, `.rtf`/`.txt`; an unknown extension is an error and *nothing runs*; a name with no extension is a PNG of the page.
- `run --cmd ID=JSON` uses `$N.path`/`$last.path` references; a params key the command's description doesn't name is an error (checked by the CLI, MCP and control channel).
- `script` prints `{"completed": n, "results": [...]}` plus `failedIndex`/`failedCommand`/`error` and exits non-zero on failure; `--keep-going` records failures as results instead. Scripts are subject to the depth/step/byte limits above.
- `mcp` roots may each be repeated; a path inside any root of its kind passes. A root left out grants none of that access, and roots plus `--connect` is an error.
- `thumbnail` writes the document's **saved** first-page preview (fitted to `SIZE` px, never rendered) and refuses an output that names the input document; a file without a preview is an error. `validate-pdf` defaults to the file's own `GTS_PDFXVersion` and prints `standard` plus a separate `warnings` array.

### Document and window model
- Several documents open in tabs; each tab is its own `DocState` with its own undo history, selection and (optionally) its own `Document Fonts` scope. A document is spreads → pages → items; text lives in **stories** threaded through text frames; parent pages contribute items behind a page's own.
- **Coordinates are points (1/72 in), y down, in spread space**: on a facing spread the right page starts at `x = page width`. **Text offsets are UTF-8 byte offsets**, not character counts (`docs/mcp.md` §Text offsets).
- Commands that create items take `spread`: an integer, or `{"kind":"parent","index":N}`. `page` in guide/column commands is the page's **index within its spread**; `document.inspect` page `index` is absolute.
- **Page indices are 0-based and validated** in `layout.pages.delete` / `layout.pages.applyParent`: an index at or past `page_count` errors with the count in the message, and a repeated index counts once in the reply.
- **Tables have ids.** `table.insert` and `table.get` return a `table` id; table commands accept `{table, story?, row?, col?, rows?, cols?}` and, without a cell range, act on the whole table.
- **Closing:** `file.close {index?}` closes without prompting and discards recovery data; the UI's File ▸ Close / tab × and `app.quit` ask when dirty; the control `app.quit` does not. Save first.

### Recipes for the v0.14–v0.20 surfaces
```sh
# Explicitly show every layer of the selected placed PDF, then read the state back
designcraft-cli run --in brochure.designcraft \
  --cmd 'object.layerOptions={"useDefaults":false}' \
  --cmd 'object.pdfLayers={}'

# Split a reflowable EPUB before paragraphs of one style, for this export only
designcraft-cli run --in brochure.designcraft \
  --cmd 'document.epubSplit={"split":{"style":"Heading 1"}}' \
  --export book.epub

# Press-ready PDF/X-1a (flattened), then validate it
designcraft-cli run --in brochure.designcraft \
  --cmd 'file.info={"title":"Brochure","author":"A. Designer","keywords":"print"}' \
  --export press.pdf
designcraft-cli validate-pdf press.pdf

# Story-wide hanging punctuation, then a list and a variable converted to text
designcraft-cli run --in brochure.designcraft \
  --cmd 'story.options={"opticalMargin":true,"opticalMarginSize":12}' \
  --cmd 'list.bullets={"on":true}' \
  --cmd 'variables.convertAllToText={"name":"Running Header"}' \
  --export page.pdf

# Delete two pages and hear how many went; then apply a parent to two pages
designcraft-cli run --sample \
  --cmd 'layout.pages.delete={"pages":[1,2]}' \
  --cmd 'layout.pages.applyParent={"pages":[0,1],"parent":"A"}'

# Create a table at a caret in a text frame, then fill a cell by table id (no cell selection)
designcraft-cli run --in catalogue.designcraft \
  --cmd 'frame.create={"rect":[36,36,300,200],"content":"text","text":"","caret":0}' \
  --cmd 'table.insert={"rows":4,"cols":4}' \
  --cmd 'table.setCell={"table":"$1.table","row":0,"col":0,"fill":"[Black]"}'
```
- `object.layerOptions` returns `{hidden, useDefaults}`; `useDefaults` cannot be combined with a non-empty `hidden`. Read `object.pdfLayers` — its `overridden` flag separates a per-placement choice from the file's defaults.
- `document.epubSplit` with no `split` is a query; `off`, `"exportTags"` or `{"style": name}` sets it. After export, unzip the EPUB and count `OEBPS/content*.xhtml`.
- `story.options` also accepts `story`/`frame`; omit both to use the selection. Per-paragraph `ignoreOpticalMargin` opts a paragraph out.
- `selection.key {id}` then `object.align {edge, to?}` — with a key object set, `to` defaults to `keyObject`.
- `list.bullets`/`list.numbers` are toggles: with no `on` they turn off when every selected paragraph already has the list, else on.
- `file.info` sets the document's title/author/description/keywords (File Info dialog); PDF export writes them into the PDF's Info dictionary.
- `layout.pages.delete` refuses to delete every page, counting duplicates once; `layout.pages.applyParent` with `parent: null` or `"[None]"` clears the parent.

### Open / save / export flows
- Open: `File ▸ Open…` (`Cmd+O`, `file.open {path}`) — content-sniffed; `.idml` and `.indd`/`.indt` route through the IDML interchange module. `file.recentFiles` / `file.openRecent` back Open Recent.
- Save: `File ▸ Save` (`Cmd+S`, `file.save`) and `Save As…` (`Cmd+Shift+S`, `file.saveAs {path}`) write the native `.designcraft` package; `file.saveACopy` writes a copy without changing the open document; writes are atomic.
- Recovery: unsaved documents are written to the recovery folder every 30 s by default (`recoveryMinutes`, minimum 5 s) and reopened after a crash (`crates/engine/src/recovery.rs`; `file.recovery.{save,list,open}`, `file.revert`).
- Export: the `file.export*` commands above, or the CLI's `--export`. Every export returns `{path, bytes, …}` plus a `warnings` array where applicable — **read it**.
- Package: `File ▸ Package` (`app.packageDialog`, `Cmd+Alt+Shift+P`; `file.package {dir, idml?, pdf?, instructions?}`) relinks to a `Links` folder with package-relative link paths, copies placed files and document fonts, writes an IDML copy and a report. It copies the bytes the document loaded, not whatever is at the path now, and refuses to overwrite a font destination that changed after loading.

### Verified end-to-end examples
```sh
# Headless: build a page and export it three ways (--scale applies to the exports after it)
designcraft-cli run --sample \
  --cmd 'frame.create={"rect":[36,36,540,300],"content":"text","text":"Hello"}' \
  --export page.png --scale 2 --export page@2x.png --export page.pdf

# Discover then call a command (never guess params)
designcraft-cli commands note && designcraft-cli describe note.split

# Drive a running app (start it with a control port first)
designcraft --sample --control 7979 &
designcraft-cli app document.inspect
designcraft-cli app --method ui.render '{"page":0,"scale":2}'
```
MCP registration (`docs/mcp.md`):
```sh
claude mcp add designcraft -- designcraft-cli mcp \
  --automation-read-root "$PWD" --automation-write-root "$PWD/out"
```

## Working with an AI agent

**Legitimate and productive**
1. **Prepare inputs.** Convert to formats `crates/images` reads (PNG, JPEG, GIF, WebP, TIFF, BMP, PSD composite), author SVG or single-page PDF for vector/print art, write `.docx`/`.rtf`/`.txt`/`.md` (UTF-8 or UTF-16) for copy, and CSV/TSV/XLSX for Data Merge. Generate a test document with `file.newSample`.
2. **Drive it through commands, not pixels.** Prefer `designcraft-cli run --cmd`, `script` with `$N.path` wiring, MCP `batch`, or the control channel. Gesture paths exist (`ui.pointer`, `key`, `text`, `ime`, `dialog_*`), but commands are deterministic and return JSON.
3. **Look at the result.** `render_page`/`export_png`/`ui.render` return or write PNGs — read the image after layout work; `ui.screenshot` gives the whole window.
4. **Inspect programmatically.** `document.inspect` (pages incl. `columnRects`/`customColumns`, items, stories with `overset`, styles, swatches, selection incl. `guides`), `story.get`, `links.list`, `font.list`, `preflight.run {minPpi?}`, `document.preferences`; view state is UI-only (`ui.inspect`). `designcraft-cli describe` gives exact parameter names.
5. **Set up geometry programmatically.** `guide.add`/`guide.move`/`guide.moveBy`, read back with `guide.list`; move column gutters with `layout.moveColumnGuide` after `view.lockColumnGuides {on:false}`, then verify `columnRects`.
6. **Type work.** `story.options` for story-wide hanging punctuation, `list.bullets`/`list.numbers` for list buttons, `note.*` (incl. `note.split`) for notes, `variables.convertToText` when a client wants the running headers flattened, `style.exportTag`/`document.epubSplit` before an EPUB deliverable.
7. **Address tables by id.** Use `table.insert`/`table.get`'s `table` (plus `story` when ambiguous) rather than selecting cells with pointer gestures; verify with `table.get` after structural edits.
8. **Repair and analyse native files.** A `.designcraft` is a zip: unzip, read `document.json`, `meta.json` and `assets/`. **Re-zipping by hand is risky**: the reader requires `document.json`, honours `meta.json`'s version (above 4 is refused), and runs `Document::check()` plus asset wiring on load. Prefer open → re-save through a command.
9. **Verify exports.** `designcraft-cli validate-pdf out.pdf`, `preflight.run` (including `whiteOverprint`), `story.get` for overset text, `links.list` for missing images, every export's `warnings`, and an EPUB content-file count after `document.epubSplit`.
10. **Work on throwaway copies.** Copy the project file before a session; isolate a run with `DESIGNCRAFT_CONFIG_DIR` pointed at a scratch folder.

**Do not attempt**
- Do not assume parity: check `docs/gaps.md` and `designcraft-cli describe`. ExtendScript, UXP, `.joboptions` presets, plug-ins and Adobe cloud features do not exist (gaps 9, 22, 23).
- Do not promise layer-aware output for IDML/PSD layer options: only placed-**PDF** layer choices render and export; retained IDML graphic-layer settings warn instead.
- Do not promise PDF font repair: unembedded fonts in placed PDFs are detected and named, not fixed (gap 28).
- Do not assume a separate CLI install is needed: on macOS the app bundle carries `designcraft-cli` in `Contents/MacOS/`. Use that path (or a separately installed CLI), and say which one you used.
- Do not run `file.close` or the control method `app.quit` on a dirty document — both discard unsaved work and recovery data. The `app.quit` command (and the UI) asks first.
- Do not expect the shortcut importer to read `.indk`, apply non-Default contexts, or handle macOS Control-key chords; check `changed` and test a shortcut after importing.
- Do not move column guides on a locked document; unlock first and re-lock. Do not interpret EPS/PostScript or expect `.indd`/`.indt` fidelity, INDB/INDL, or QuarkXPress import.
- Do not feed a GREP style subroutine calls (`\g<…>`) or expect a pattern that matches empty at every character to return every position; the engine refuses or budgets those.
- Do not generate an unbounded script: nesting stops at 8, steps at 100 000 and interpolated/referenced text at 16/64 MiB. Split the work or write intermediate files instead.
- Do not point `file.open`/`file.place` at a device or FIFO, and do not drive the GUI blind (no screenshot/inspect feedback). Never run `--control` on a port you do not control: the channel has no authentication (`docs/control-protocol.md`).

## Verification protocol

DesignCraft is pre-alpha: treat every export as unverified until you have looked at it.

1. **Throwaway round-trip first.** New document (`file.new` or `--sample`) → one edit → save a `.designcraft` → reopen it (`--in`) → export the same page to PNG *and* PDF → check the PNG visually and the PDF with `validate-pdf` if you asked for `standard: "x4"` or `"x1a"`. If a step fails or geometry moved, stop and report.
2. **Never trust a silent export.** Read the JSON result (`bytes`, `pages`, `slides`, `warnings`) *and* confirm the file exists and is non-empty. A failed *step* in a non-`--keep-going` script still leaves earlier steps applied in the live app: re-inspect before retrying.
3. **Version and back up per session.** The format version is in `meta.json`; version 4 documents are refused by older readers. Keep a copy at the start of a session; to deliver files to someone on an older build, test one round-trip on their version first.
4. **Update between projects, not during one.** After a launcher update, re-verify the bundle version and build commit (`plutil -p` on the app's `Contents/Info.plist`, grep `Version|BuildCommit`; at this pin: 0.20.1, commit `33a4678…`). The bundled `designcraft-cli` updates with the app; a separately installed CLI does not. The updater now asks to close only when no document is dirty and installs at exit; a failed install is reported on the next start.
5. **Isolate test runs.** `DESIGNCRAFT_CONFIG_DIR` to a scratch folder, `DESIGNCRAFT_NO_PREFS` to avoid writing preferences, and `--automation-read-root`/`--automation-write-root` (repeatable) for MCP.
6. **Prefer re-opening over re-editing.** The reader upgrades and validates on load, so save → reopen is the cheapest proof that an edit produced a valid document.
7. **Verify geometry, not just "no error".** After guide edits read `guide.list`; after `layout.moveColumnGuide` read `document.inspect`'s `columnRects`/`customColumns`. Reopen and confirm they survive (and IDML too, if handing off IDML).
8. **Verify the typographic and EPUB settings.** After `story.options` re-read `type.selectionAttrs.storyOptions`; after `document.epubSplit` unzip the EPUB and count content files, and click one cross-file link target.
9. **Verify a placed-PDF choice in the output.** Export PDF, then check the exported file's optional content (or the warnings) — a choice that could not be applied is an error, and external-only IDML export refuses active choices.
10. **Verify what a batch job and a page command report.** `file.exportBatch` returns `files` (use `dryRun` first); `layout.pages.delete`/`applyParent` return `deleted`/`applied`, so compare that count with the request.
11. **Check white-overprint before print.** Run `preflight.run` and read `whiteOverprint` issues: a white object set to overprint looks fine on screen and vanishes on press. Fix the colour or the overprint setting, then re-run.

*Verify against your installed version.* The repository at this pin and the installed bundle match exactly; if the launcher has since updated DesignCraft, re-run step 4 and re-check command parameters with `designcraft-cli describe` before relying on them.

## Sources & evidence

- Repository: https://github.com/storytold/designcraft — inspected at tag **v0.20.1**, commit **`33a467872268c98536231491865b4011b0275b17`** (`git rev-parse HEAD`; "Merge tested main for v0.20.1", 2026-11-11), audited **2026-11-12**. The v0.18.0 ref in the same checkout was used for set diffs (146 files, +8007/−658).
- Installed app: `/Applications/DesignCraft.app` — `CFBundleShortVersionString 0.20.1`, `DesignCraftBuildCommit 33a4678…`, `CFBundleIdentifier ai.storyteller.designcraft` (`Contents/Info.plist` inspected, GUI never launched). The bundle contains `Contents/MacOS/designcraft-cli`, which prints `designcraft-cli 0.20.1`; the desktop binary prints `designcraft 0.20.1`; its read-only `--version`, `--help`, `commands` (555 entries) and `describe` runs are the live cross-check.
- Read for this skill: `README.md`, `Cargo.toml`, `ROADMAP.md`, `AGENTS.md`, `docs/{agents,mcp,control-protocol,gaps,target-app-parity,file-format-parity,graphic-layer-options,pdf-layer-visibility,localization-parity,cjk}.md`, `apps/designcraft/src/{main,gpu_limits,control_server}.rs`, `apps/designcraft-cli/src/{main,automation_args}.rs`, `crates/format/src/lib.rs`, `crates/engine/src/{lib,io,script,recovery,file_access}.rs`, `crates/engine/src/cmd.rs` and `crates/engine/src/cmd/` (incl. `anchored.rs`, `export.rs`, `export/pdf.rs`, `export/formats.rs`, `export_batch.rs`, `preflight.rs`, `preflight/white_overprint.rs`, `pdflayers.rs`, `links.rs`, `package.rs`, `table/target.rs`, `text.rs`, `variables.rs`, `lists.rs`, `editorial.rs`, `file.rs`, `file/place.rs`, `guides.rs`, `layout.rs`, `layout/registry.rs`, `params.rs`), `crates/mcp/src/{tools,server,headless,backend}.rs`, `crates/ui-egui/src/{control,links_worker,shortcut_import,page_history,story_editor,updates_ui,i18n}.rs`, `crates/ui-egui/src/menus/{ui_commands,keys}.rs`, `crates/ui-egui/src/canvas/page_decor.rs`, `crates/doc/src/{anchored,page,item,assets,edit}.rs`, `crates/compose/src/{hyphen,grep}.rs`, `crates/pdf/src/{lib,pdfx,pdfx/fonts,pdfx1a,inks,optional_content}.rs`, `crates/epub/src/{lib,css}.rs`, `crates/idml/src/{import,export}.rs`, `crates/images/src/{lib,eps}.rs`, `crates/textimport/src/{lib,docx,xlsx,rtf,export}.rs`, `packaging/linux/flatpak/`.
- Counts re-measured at v0.20.1 (`cmd!` id set and `UI_COMMANDS` rows extracted from the clone at both tags, MCP tool calls and control arms counted, CLI subcommands read from `USAGE` and the installed `--help`, format version from source, live registry cross-checked): **555 engine / 190 UI / 26 MCP tools / 28 control arms (31 method strings) / 11 CLI subcommands / format version 4 / 10 hyphenation languages / 15 non-English interface languages** — all unchanged from v0.18.0 except the corrected control figure. Live discovery beats this document: `designcraft-cli commands`, `designcraft-cli describe ID`, and `docs/gaps.md`.
- Deep automation tables (CLI, scripts and their limits, MCP tools, control methods, coordinates, guides/columns, table targeting, layer options, EPUB split, story options, shortcut import, sample commands): `references/agent-surfaces.md`.
