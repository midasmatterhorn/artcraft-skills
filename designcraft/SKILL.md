---
name: designcraft
description: DesignCraft is the ArtCraft team's clean-room, open-source InDesign-class page-layout app (pure Rust; `.designcraft` project format; IDML/INDD/INDT import; PDF/X-4 and PDF/X-1a export, PDF/A-2b, EPUB with Split Document, editable PPTX, HTML, PNG and JPEG export; headless CLI, MCP server and JSON control channel). Trigger this skill whenever the user mentions DesignCraft — or a `.designcraft`, `.idml`, `.indd`, `.indt`, `.dcbook`, `.dclib`, `.ase` or command-script file — asks what it can or cannot do, which formats it opens or writes, its keyboard shortcuts, how to automate or script it, how to prepare or convert assets for it, how to place PDFs and choose their layers, how to verify or repair its output, or how to troubleshoot it. Also trigger when the job is described without naming the app — "lay out a magazine", "thread this story across three columns", "set this on a baseline grid", "export a PDF/X-4", "export a press-ready PDF/X-1a", "make an EPUB from these pages", "split the EPUB into chapters", "batch-export every page to PNG", "place these photos in a brochure", "hide a layer of this placed PDF", "convert these text variables to text", "import my InDesign shortcuts". Do not guess its capabilities from InDesign knowledge — read this first.
---

# DesignCraft

Audit basis: this checkout is tag `v0.14.0`, commit `7da69c16ce221f46e8f27cb41e0c88167c8be416`. The installed `/Applications/DesignCraft.app` reports version `0.14.0` and its binary prints `designcraft 0.14.0`, so the bundle matches this source. **Verify against your installed version** if the ArtCraft Launcher has auto-updated since. Deep automation detail — CLI flags, script syntax, all 26 MCP tools, the control methods, coordinates, guide and column geometry, layer options, EPUB splitting, shortcut import — is in `references/agent-surfaces.md` next to this file.

## Overview

DesignCraft is a page-layout and publishing application written from scratch in Rust: "an open-source, modern desktop publishing and page layout studio" (`README.md`). It aims at full Adobe InDesign 2026 parity — "faster, open (documented JSON format + IDML), scriptable by agents (MCP), and available on the web" (`ROADMAP.md`) — as a clean-room application (`AGENTS.md`). It runs natively on macOS, Windows and Linux, and in a browser as WebAssembly (`README.md` §Web, `apps/designcraft-web`). The UI migrated to egui 0.37 with craft-ui's shared docking this release. Maturity is **pre-alpha**: the alpha gate is still blocked by fixes to Smart Text Reflow on the Primary Text Frame (#165), ~5–7 h away (`ROADMAP.md:3`, `docs/gaps.md` §0); the maintainers estimate ~80% feature breadth and ~47% "ready for real work" (`docs/target-app-parity.md` §Headline). Source: GitHub `storytold/designcraft`, MIT OR Apache-2.0 (`Cargo.toml`), a layered Cargo workspace enforced by `cargo xtask layers`; shared craft-libs crates provide printing, ICC colour management, atomic writes, PDF writing (craft-pdf now carries overprint/knockout/CMYK blending and spot gradients, plus the craft-prepress flattener for PDF/X-1a) and document-path policy (`Cargo.toml`).

The one idea that governs everything: **every user-visible action is a command** with a stable id and JSON parameters (`crates/engine/src/cmd.rs` `command_specs`), and the UI, CLI, control channel and MCP all go through `Session::execute` (`crates/engine/src/lib.rs`). Prefer commands over GUI poking.

## Capabilities (verified)

### Layout, guides and the document model — implemented
- Facing/non-facing spreads, parent (master) pages with page-number markers, sections, layers, and frames typed text / graphic / unassigned; stories threaded across frames and spreads (`crates/doc/src/{page,story}.rs`; `crates/engine/src/cmd/{layout,thread}.rs`).
- Document setup, page-size presets (incl. A0–A2 posters), bleed/slug, start page, Page tool for pages of their own size (`layout.documentSetup`, `layout.pageSize`, `file.new`).
- Multi-document tabs: `file.activate {index}`, `document.list`, next/previous document (`Cmd+F6` / `Cmd+Shift+F6`) — `crates/engine/src/cmd/file.rs`, `crates/ui-egui/src/menus/`.
- **Ruler guides:** `guide.add` (horizontal/vertical/both; page, spread or liquid guide), `guide.list`, `guide.select`, `guide.selectAll` (`Cmd+Alt+G`), `guide.deselect`, `guide.move`, `guide.moveBy`, `guide.delete`, `guide.deleteAll`, `layout.createGuides` (`crates/engine/src/cmd/guides.rs`; caps 10 000 guides, rows/columns ≤ 1000). Guides are selected like objects and a dragged guide snaps along its axis; Shift snaps to ruler ticks (the 10× tick-spacing step is fixed this release), Cmd suspends snapping.
- **Custom column guides:** a page keeps dragged column positions (`Columns.positions`, `crates/doc/src/page.rs`), `layout.moveColumnGuide {page, gutter, position, spread?|parent?}`, at most 216 columns (`MAX_COLUMNS`); `view.lockColumnGuides` is a document setting, **on by default**, saved in the document and IDML; `view.lockGuides` (`Cmd+Alt+;`) only stops pointer dragging.
- **Page view history:** `view.goBack` (`Cmd+PageUp`) / `view.goForward` (`Cmd+PageDown`) retrace page jumps at the current zoom (`crates/ui-egui/src/page_history.rs`).
- Styles (paragraph, character, object, table, cell, groups), swatches (process/spot/tints/gradients), text wrap, corner options, transparency effects, ICC colour management with working spaces and proof setups.
- Interactions: Pathfinder boolean ops, compound/clipping paths, gradients, stroke styles/arrowheads, tables with merges and graphic cells (**gradient cell fills now draw as gradients on screen and in PDF**, PR #1768), footnotes, endnotes, notes, cross-references, index, TOC, text variables, conditional text, track changes, data merge, XML tags/DTD, articles, object libraries, books, object states, buttons and form fields, page transitions, Flex Layout.
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
- **Story-level Optical Margin Alignment:** `story.options {story?, frame?, opticalMargin?, opticalMarginSize?}` sets hanging punctuation/edges for every paragraph of a story except paragraphs with `ignoreOpticalMargin`; the **Story** panel and `type.selectionAttrs.storyOptions` expose it, and IDML carries `StoryPreference` (`crates/engine/src/cmd/text.rs`).
- Hyphenation Settings (`app.hyphenationDialog`) sets limits, zone, the Better Spacing ↔ Fewer Hyphens slider, Hyphenate Capitalized/Last Word/Across Column and Preview as one undo step.
- **Bulleted/numbered list buttons:** `list.bullets` / `list.numbers {on?}` apply InDesign's default hanging indent and remove it again (`crates/engine/src/cmd/lists.rs`).
- **Notes:** `note.convertFromText {author?}`, `note.next`, `note.previous`, and **`note.split` (new this release)** — Split Note splits a note in two at the insertion point, as in InDesign; deleting a note or converting it to text keeps the caret on the same text; footnote caret edits no longer drop untyped formatting (`crates/engine/src/cmd/editorial.rs`).
- **Convert Variable to Text:** `variables.convertToText` and `variables.convertAllToText {name}` replace each instance with the value it shows on its page; the variable stays defined.
- **Key Object for alignment:** `selection.key {id}` makes a selected item the key object (needs ≥ 2 selected); `object.align`'s `to` defaults to `keyObject` while one is set.
- Column rules (now running from the top line's ascent to the bottom line's descent) and Span Columns, Paragraph Rules above/below, Based on Parent, custom anchored objects with **Relative to Spine**.
- **Story Editor depth ruler (new):** a depth ruler beside the text with View › Story Editor › Show/Hide Depth Ruler (`view.storyEditorDepthRuler`), as in InDesign (`crates/ui-egui/src/story_editor.rs`, PR #1795).
- Fonts: own font DB, shaping (harfrust), outlines (skrifa), variable-font instances, `Document Fonts` folders beside a document (case-insensitive), Type › Reload Fonts (`font.reload`).

### Import / open — implemented
`file.open` decides by content, not extension (`crates/engine/src/cmd/file.rs` `open_path`):
- Native `.designcraft` (zip or legacy single JSON) — `crates/format`.
- `.idml` InDesign Markup imported into the native model — `crates/idml/src/import.rs`; `.indd`/`.indt` converted to IDML in memory by `storytold/indd-utils` (real-file fidelity unmeasured — `docs/gaps.md` §2).
- Placed graphics: PNG, JPEG, GIF, WebP, TIFF, BMP, PSD/PSB composite, SVG, PDF (any page, crop-box choice), PDF-compatible Illustrator files detected as PDF, EPS (TIFF preview or placeholder — no PostScript interpreter) (`crates/images/src/lib.rs`).
- Text: `.txt`/`.text` (UTF-8 or UTF-16), `.md`, `.docx`, `.rtf`, `.xlsx` (first used range becomes a table), Tagged Text; Data Merge sources CSV, TSV, text, `.xlsx`.
- Media (poster/placeholder frames, no playback): mp4, m4v, mov, webm, ogv, mp3, m4a, wav, ogg, oga, aac.
- Swatches `.ase`, ICC `.icc`/`.icm`, XML (with DTD), libraries `.dclib`, books `.dcbook`, and a page of an IDML or `.designcraft` document (`file.place {layoutPage}`) as a group of objects.
- `file.openRecent {index}` backs File › Open Recent (at most `recentFilesMax`, default 20).

### Native format — implemented (format version 4)
`.designcraft` is a zip (`crates/format/src/lib.rs`): `mimetype` (stored, first), `document.json` (pretty JSON), `assets/` entries (byte-for-byte, each file once), `meta.json` (format version and generator) and an optional `preview.png`. Latest reader capability is **version 4**: version 4 covers retained placed-graphic layer options and explicit all-on placed-PDF layer choices. `required_version` pins a file to 4 only when it needs one of those, else keeps 2 or 3 so older readers still open it. Readers upgrade older versions and still open the legacy single-JSON form. Read limits: 100 000 entries, 256 MiB `document.json`, 1 GiB per asset, 4 GiB total; a document with non-finite geometry cannot be saved. Writes are atomic.

### Export — implemented
- **PDF** (`file.exportPdf`): real selectable text with embedded font subsets, DeviceCMYK/RGB/Gray, spot `/Separation`, bleed boxes, crop/bleed marks and page info, pages or spreads, `standard: "none" | "x4" | "x1a" | "a2b"` (**PDF/X-1a:2003 is new this release** — the PDF/X-4 print file flattened by craft-prepress, with overprint/knockout and CMYK blending preserved through the flattener), tagged structure tree, transparency flattening, hyperlink annotations and outlines, interactive options, `created` (Unix seconds) for reproducible files, `file.printBooklet` imposition. **PDF export now writes the File Info title, author, description and keywords** (`file.info`, PR #1712); the composition cache is consulted once per story and page.
- **PDF/X-4 checks:** `designcraft-cli validate-pdf FILE.pdf` prints `{valid, issues}` and exits non-zero on failure; checks include PDF version, output intent, Info/XMP identification, interpolation, encryption, trim boxes, Type 3 fonts, device RGB under a CMYK output intent, and fonts that draw visible text without an embedded font program (including inside placed PDF forms), with font names and pages; render-mode-3 invisible text is exempt (`crates/pdf/src/pdfx.rs`, `crates/pdf/src/pdfx/fonts.rs`).
- **Inks and separations (new):** the document's inks are a `craft_prepress::InkSet` (four process inks plus each spot swatch; `crates/pdf/src/inks.rs`); **Separations Preview shows the exported PDF's plates, spot plates included** (`ink.separations`; the UI thread separates one sheet per frame).
- **EPUB 3** reflowable (`file.exportEpub`) and fixed layout (`file.exportFixedEpub`). **Split Document:** `document.epubSplit {split?}` stores off / before each export-tagged paragraph / before each paragraph of one style; `file.exportEpub {split}` overrides it for one export and `style.exportTag {split}` marks the styles; navigation and note links point across the files.
- **HTML** (`file.exportHtml`): one self-contained page, styles as CSS, images embedded, stories and graphics in reading order; returns `warnings`.
- **PowerPoint** (`file.exportPptx`): every page becomes a slide of editable shapes, pictures, tables and text boxes; `lineBreaks: keep|reflow`, `rasterize` (default true), `embedFonts` (default true); approximations reported in `warnings`.
- **PNG / JPEG** of a page via the renderer (`designcraft-cli run --export out.png`, `--all-pages DIR`; MCP `render_page` / `export_png`; control `ui.render`).
- **IDML** (`file.exportIdml`, `embedImages`), **Text** `.txt`/`.rtf`/tagged (`file.exportText`), **XML** (`file.exportXml`).
- **Print** (`file.print`, `file.printers`, `dryRun`, `created`) through the shared `craft-print` spooler — `docs/gaps.md` §10.

### Automation surfaces — implemented
- **CLI** `designcraft-cli` (`apps/designcraft-cli/src/main.rs`): `run`, `commands [FILTER]`, `describe COMMAND`, `script`, `app`, `mcp`, `perf`, `bench`, `validate-pdf`, `links`, `--version` — 10 subcommands, unchanged at this tag. On macOS it is **not inside `DesignCraft.app`**: the release ships a separate `designcraft-cli-<version>-macos-universal.zip`. `mcp` takes `--automation-read-root`/`--automation-write-root` more than once, in `--flag DIR` and `--flag=DIR` spellings; a non-UTF-8 MCP line now answers a parse error instead of dying.
- **MCP server** `designcraft-cli mcp` — stdio JSON-RPC, protocol 2025-06-18 (older revisions accepted), **26 tools**, byte-identical set to v0.13.0: command discovery/execution (`list_commands`, `execute`, `batch`), document I/O and inspection (`inspect_document`, `get_story`, `set_story_text`, `new_document`, `open_document`, `save_document`, `place_image`), rendering (`render_page`, `export_png`, `screenshot`), input/UI tools (`select_tool`, `pointer`, `key`, `type_text`, `ime`, `click`, `drag`, `menu_list`, `ui_inspect`, `ui_set`, `dialog_set/confirm/cancel`). Read/write root flags confine every path a command touches.
- **Control channel**: `designcraft --control PORT` serves JSON lines on `127.0.0.1` only — the dispatch gained **`ui.docking`** (shared dock layout) this release; 4 MiB line limit, 16 connections, no authentication (`docs/control-protocol.md`).
- **Scripts**: one command per line with `$N.path` references to earlier results (`crates/engine/src/script.rs`; `script.run {text}`). The Scripts panel runs a script as one undo step and restores the document on failure.
- **Shortcuts on the shared craft-keymap crate (new):** panel shortcuts and **editable tool keys**, the shared **Keyboard Shortcuts dialog with shortcut sets** (`window.shortcutSets`), and InDesign shortcut import (`window.importShortcuts {path | text}`) which reads an InDesign Show Set `.txt` (UTF-8/BOM or UTF-16; ≤ 8 MiB), applies its Default context, and reports `{set, imported, changed, conflictsCleared, skipped, unmatched, unmatchedWithoutShortcut, unreadable}` (`crates/ui-egui/src/shortcut_import.rs`, `crates/ui-egui/src/menus/keys.rs`).
- Surface size at this tag: **542 engine command specs** (unique `cmd!` ids across the `specs()` lists wired into `command_specs()`, tests excluded) and **176 UI commands**. Versus v0.13.0 (537 + 172): **+5 engine** — `file.info`, `ink.separations`, `note.split`, `text.deleteSurrounding`, plus one const-built id — and **+4 UI** — `help.checkForUpdates`, `ui.dock`, `view.storyEditorDepthRuler`, `window.shortcutSets`; **nothing removed**. MCP stays 26 and the CLI subcommands are unchanged. Discover the live list with `designcraft-cli commands` and `describe`.

### Platforms — implemented
- macOS, Windows, Linux native (`apps/designcraft`); WebAssembly web build via trunk (`apps/designcraft-web`: WebGPU with a WebGL2 fallback, `?webgl` to force it, `?sample` for the sample magazine). The web build has no control channel, and Save/Export download files instead of writing them. Runtime environment variables: `RUST_LOG`, `WGPU_BACKEND`, `WGPU_POWER_PREF`, `WGPU_ADAPTER_NAME`, `WGPU_VALIDATION_INDIRECT_CALL`, `DESIGNCRAFT_CONTROL_PORT`, `DESIGNCRAFT_CONFIG_DIR`, `DESIGNCRAFT_NO_PREFS`, `DESIGNCRAFT_NO_NATIVE_MENU`, `DESIGNCRAFT_WAYLAND` (Linux). Windows installs per-user by default now.

## Known limitations and not-implemented

Ranked shortfall list: `docs/gaps.md` (kept current by the maintainers — read it before promising work). Headline items at this tag:

- **Pre-alpha.** The alpha gate is blocked by Smart Text Reflow on the Primary Text Frame adding pages users cannot delete (#165). Threading by hand and autoflow fill-the-following-pages-first work.
- **Basic canvas editing still fails for some users** — object copy/paste on Windows and Linux, right-click context menus, formatting at a caret discarded (`docs/gaps.md` §1).
- **Placed graphic layer options are retained, not rendered.** IDML per-placement layer visibility is preserved and warns on import/preflight/PDF export, but the renderer and PDF exporter still use the asset's composite/default appearance; layer-comp choices and a layer-options UI are missing. Placed **PDF** layer choices *are* applied — do not generalise that to IDML/PSD layer options.
- **INDD/INDT opening is unmeasured on real files**; **INDB/INDL are not read**; no QuarkXPress import. **IDML round-trip is not proven on real files** — opened IDML can reflow.
- **EPS is preview-only** — no PostScript interpreter. **No ExtendScript/UXP compatibility**: InDesign scripts do not run; the script language is DesignCraft's own command language. **No plug-in model**. **No in-app media playback**.
- **PDF standards:** PDF/X-1a:2003 joined PDF/X-4 and PDF/A-2b this release, but there is still no PDF/X-3, PDF/UA validation, Adobe `.joboptions` presets, or output-intent choice beyond the built-in profile; PostScript printing is absent. **Placed-PDF font repair is missing** (gap 28): export and `validate-pdf` *detect and name* visible unembedded fonts, but nothing embeds, substitutes or outlines them automatically.
- **HTML export is one basic page; fixed-layout EPUB writes page images** rather than live text and CSS; neither output has animation or timing (gap 17).
- **Hyphenation** for English, Spanish, Portuguese, Norwegian and Greek only; **spelling** English only (gap 13). **No screen-reader exposure**; PDF/UA unverified (gap 25).
- **Startup crashes and blank canvases on some GPU/driver combinations** remain a partly mitigated class (backend fallback + `gpu.json` skip list; gap 5). **Performance**: no incremental composition and no GPU raster — the canvas is CPU-rendered with `vello_cpu`, the GPU only composites the UI (gap 20).
- **Font discovery** still misses fonts that some services/managers activate; disk changes are noticed only on request (`font.reload`) (gap 6). **Localization** is partial: Japanese 95%, Czech/Polish 99%, Georgian 100%, several 61–85%, Hindi/Indonesian/Korean/Vietnamese absent (`ROADMAP.md` §Languages). A missing string shows English and fails no check.
- **Shortcut limits**: the InDesign importer reads only Show Set `.txt` (not `.indk`), applies only the Default context (Text for type/text commands), and rejects macOS Control-key chords; editing tool keys and managing sets happens in the Keyboard Shortcuts dialog, not the importer (`crates/ui-egui/src/shortcut_import.rs`, `menus/keys.rs`).
- **Custom column guides** are horizontal column gutters only; locked by default and `layout.moveColumnGuide` refuses while locked; changing column count or gutter discards the custom positions; a page that changes side of the spine mirrors them.
- **`file.close` is not a safe "close tab"**: it closes without asking and discards the document's recovery data. The UI's File ▸ Close / tab × asks when the document is dirty; `app.quit` asks per dirty document, while the control method `app.quit` quits without asking.
- **Claimed but unverified**: README says "every menu item, tool gesture, panel control and dialog" can be driven over the control channel and MCP. The command registry and control methods are broad, but this audit did not launch the GUI; treat a specific dialog as unverified until `ui.dialog.open` / `ui_inspect` confirms it.
- **Stale documentation to distrust**: `ROADMAP.md` and `docs/target-app-parity.md` still quote old command counts (~200 / 446+99); `docs/agents.md` and the CLI's `SCRIPT_HELP` say most commands ignore unknown parameters, while the CLI, MCP and control channel reject them. Verify with `designcraft-cli describe` against your build.

## How to operate

### Launch on macOS
- GUI: `open -a DesignCraft` (installed under `/Applications/DesignCraft.app`, `CFBundleIdentifier ai.storyteller.designcraft`); to open a file: `open -a DesignCraft brochure.designcraft`. The binary inside the bundle is `/Applications/DesignCraft.app/Contents/MacOS/DesignCraft`.
- Real flags of the desktop binary (`apps/designcraft/src/main.rs`): `--sample`, `--control <port>` (also `DESIGNCRAFT_CONTROL_PORT`), `--version`, `--gpu-skip=<list>` (internal restart bookkeeping), plus any number of file paths.
- **The CLI is not inside the `.app`.** Get it from the separate `designcraft-cli-<version>-macos-universal.zip` release asset, `cargo install --path apps/designcraft-cli --locked`, or `cargo build --release -p designcraft-cli`.
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
designcraft-cli perf [--pages N] [--frames N] [--chars N] [--images N] [--runs N] [--strict]
designcraft-cli bench FILE [--runs N]
designcraft-cli validate-pdf FILE.pdf | links | --version
```
- `--page`, `--scale` and `--pdf-options` apply to the `--export`s that **follow** them; one left after the last export is an error.
- `--export` picks the writer from the extension: `.png`/`.jpg`/`.jpeg` (a page), `.pdf`, `.designcraft` (Save As), `.idml`, `.epub`, `.pptx`, `.html`/`.htm`, `.rtf`/`.txt`; an unknown extension is an error and *nothing runs*; a name with no extension is a PNG of the page.
- `run --cmd ID=JSON` uses `$N.path`/`$last.path` references; a params key the command's description doesn't name is an error (checked by the CLI, MCP and control channel).
- `script` prints `{"completed": n, "results": [...]}` plus `failedIndex`/`failedCommand`/`error` and exits non-zero on failure; `--keep-going` records failures as results instead.
- `mcp` roots may each be repeated; a path inside any root of its kind passes. A root left out grants none of that access, and roots plus `--connect` is an error.

### Document and window model
- Several documents open in tabs; each tab is its own `DocState` with its own undo history, selection and (optionally) its own `Document Fonts` scope. A document is spreads → pages → items; text lives in **stories** threaded through text frames; parent pages contribute items behind a page's own.
- **Coordinates are points (1/72 in), y down, in spread space**: on a facing spread the right page starts at `x = page width`. **Text offsets are UTF-8 byte offsets**, not character counts (`docs/mcp.md` §Text offsets).
- Commands that create items take `spread`: an integer, or `{"kind":"parent","index":N}`. `page` in guide/column commands is the page's **index within its spread**; `document.inspect` page `index` is absolute.
- **Closing:** `file.close {index?}` closes without prompting and discards recovery data; the UI's File ▸ Close / tab × and `app.quit` ask when dirty; the control `app.quit` does not. Save first.

### Recipes for the v0.14 surfaces
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
```
- `object.layerOptions` returns `{hidden, useDefaults}`; `useDefaults` cannot be combined with a non-empty `hidden`. Read `object.pdfLayers` — its `overridden` flag separates a per-placement choice from the file's defaults.
- `document.epubSplit` with no `split` is a query; `off`, `"exportTags"` or `{"style": name}` sets it. After export, unzip the EPUB and count `OEBPS/content*.xhtml`.
- `story.options` also accepts `story`/`frame`; omit both to use the selection. Per-paragraph `ignoreOpticalMargin` opts a paragraph out.
- `selection.key {id}` then `object.align {edge, to?}` — with a key object set, `to` defaults to `keyObject`.
- `list.bullets`/`list.numbers` are toggles: with no `on` they turn off when every selected paragraph already has the list, else on.
- `file.info` sets the document's title/author/description/keywords (File Info dialog); PDF export writes them into the PDF's Info dictionary.

### Open / save / export flows
- Open: `File ▸ Open…` (`Cmd+O`, `file.open {path}`) — content-sniffed; `.idml` and `.indd`/`.indt` route through the IDML interchange module. `file.recentFiles` / `file.openRecent` back Open Recent.
- Save: `File ▸ Save` (`Cmd+S`, `file.save`) and `Save As…` (`Cmd+Shift+S`, `file.saveAs {path}`) write the native `.designcraft` package; `file.saveACopy` writes a copy without changing the open document; writes are atomic.
- Recovery: unsaved documents are written to the recovery folder every 30 s by default (`recoveryMinutes`, minimum 5 s) and reopened after a crash (`crates/engine/src/recovery.rs`; `file.recovery.{save,list,open}`, `file.revert`).
- Export: the `file.export*` commands above, or the CLI's `--export`. Every export returns `{path, bytes, …}` plus a `warnings` array where applicable — **read it**.
- Package: `File ▸ Package` (`app.packageDialog`, `Cmd+Alt+Shift+P`; `file.package {dir, idml?, pdf?, instructions?}`) relinks to a `Links` folder with package-relative link paths, copies placed files and document fonts, writes an IDML copy and a report.

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
7. **Repair and analyse native files.** A `.designcraft` is a zip: unzip, read `document.json`, `meta.json` and `assets/`. **Re-zipping by hand is risky**: the reader requires `document.json`, honours `meta.json`'s version (above 4 is refused), and runs `Document::check()` plus asset wiring on load. Prefer open → re-save through a command.
8. **Verify exports.** `designcraft-cli validate-pdf out.pdf`, `preflight.run`, `story.get` for overset text, `links.list` for missing images, every export's `warnings`, and an EPUB content-file count after `document.epubSplit`.
9. **Work on throwaway copies.** Copy the project file before a session; isolate a run with `DESIGNCRAFT_CONFIG_DIR` pointed at a scratch folder.

**Do not attempt**
- Do not assume parity: check `docs/gaps.md` and `designcraft-cli describe`. ExtendScript, UXP, `.joboptions` presets, plug-ins and Adobe cloud features do not exist (gaps 9, 22, 23).
- Do not promise layer-aware output for IDML/PSD layer options: only placed-**PDF** layer choices render and export; retained IDML graphic-layer settings warn instead.
- Do not promise PDF font repair: unembedded fonts in placed PDFs are detected and named, not fixed (gap 28).
- Do not assume the CLI or MCP server is installed: on macOS the `.app` holds only the desktop app. Build or download it first, and say so.
- Do not run `file.close` or the control method `app.quit` on a dirty document — both discard unsaved work and recovery data. The `app.quit` command (and the UI) asks first.
- Do not expect the shortcut importer to read `.indk`, apply non-Default contexts, or handle macOS Control-key chords; check `changed` and test a shortcut after importing.
- Do not move column guides on a locked document; unlock first and re-lock. Do not interpret EPS/PostScript or expect `.indd`/`.indt` fidelity, INDB/INDL, or QuarkXPress import.
- Do not drive the GUI blind (no screenshot/inspect feedback), and never run `--control` on a port you do not control: the channel has no authentication (`docs/control-protocol.md`).

## Verification protocol

DesignCraft is pre-alpha: treat every export as unverified until you have looked at it.

1. **Throwaway round-trip first.** New document (`file.new` or `--sample`) → one edit → save a `.designcraft` → reopen it (`--in`) → export the same page to PNG *and* PDF → check the PNG visually and the PDF with `validate-pdf` if you asked for `standard: "x4"` or `"x1a"`. If a step fails or geometry moved, stop and report.
2. **Never trust a silent export.** Read the JSON result (`bytes`, `pages`, `slides`, `warnings`) *and* confirm the file exists and is non-empty. A failed *step* in a non-`--keep-going` script still leaves earlier steps applied in the live app: re-inspect before retrying.
3. **Version and back up per session.** The format version is in `meta.json`; version 4 documents are refused by older readers. Keep a copy at the start of a session; to deliver files to someone on an older build, test one round-trip on their version first.
4. **Update between projects, not during one.** After a launcher update, re-verify the bundle version and build commit (`plutil -p /Applications/DesignCraft.app/Contents/Info.plist | grep -E 'Version|BuildCommit'`; at this pin: 0.14.0, commit `7da69c16…`).
5. **Isolate test runs.** `DESIGNCRAFT_CONFIG_DIR` to a scratch folder, `DESIGNCRAFT_NO_PREFS` to avoid writing preferences, and `--automation-read-root`/`--automation-write-root` (repeatable) for MCP.
6. **Prefer re-opening over re-editing.** The reader upgrades and validates on load, so save → reopen is the cheapest proof that an edit produced a valid document.
7. **Verify geometry, not just "no error".** After guide edits read `guide.list`; after `layout.moveColumnGuide` read `document.inspect`'s `columnRects`/`customColumns`. Reopen and confirm they survive (and IDML too, if handing off IDML).
8. **Verify the typographic and EPUB settings.** After `story.options` re-read `type.selectionAttrs.storyOptions`; after `document.epubSplit` unzip the EPUB and count content files, and click one cross-file link target.
9. **Verify a placed-PDF choice in the output.** Export PDF, then check the exported file's optional content (or the warnings) — a choice that could not be applied is an error, and external-only IDML export refuses active choices.

*Verify against your installed version.* The repository at this pin and the installed bundle match exactly; if the launcher has since updated DesignCraft, re-run step 4 and re-check command parameters with `designcraft-cli describe` before relying on them.

## Sources & evidence

- Repository: https://github.com/storytold/designcraft — inspected at tag **v0.14.0**, commit **`7da69c16ce221f46e8f27cb41e0c88167c8be416`** (`git rev-parse HEAD`; "Release 0.14.0", 2026-10-28), audited 2026-10-29.
- Installed app: `DesignCraft.app` in the system Applications folder; the binary prints `designcraft 0.14.0` (`Contents/Info.plist` inspected, never launched). The bundle contains only `DesignCraft`; no `designcraft-cli` is installed on the audit machine.
- Read for this skill: `README.md`, `Cargo.toml`, `ROADMAP.md`, `AGENTS.md`, `docs/{agents,mcp,control-protocol,gaps,target-app-parity,file-format-parity,graphic-layer-options}.md`, `apps/designcraft/src/{main,profile,control_server}.rs`, `apps/designcraft-cli/src/{main,automation_args}.rs`, `crates/format/src/lib.rs`, `crates/engine/src/{lib,script,recovery,io,file_access}.rs`, `crates/engine/src/cmd.rs` and `crates/engine/src/cmd/` (incl. `export.rs`, `pdflayers.rs`, `text.rs`, `variables.rs`, `lists.rs`, `editorial.rs`, `edit.rs`, `object.rs`, `file.rs`, `guides.rs`, `layout.rs`, `params.rs`, `package.rs`), `crates/mcp/src/{tools,server,headless,backend}.rs`, `crates/ui-egui/src/{control,shortcut_import,page_history,story_editor}.rs`, `crates/ui-egui/src/menus/{ui_commands,keys,bar}.rs`, `crates/doc/src/{page,item,assets}.rs`, `crates/compose/src/`, `crates/pdf/src/{lib,pdfx,pdfx/fonts,inks,optional_content}.rs`, `crates/epub/src/lib.rs`, `crates/idml/src/{import,export}.rs`, `crates/images/src/lib.rs`, `crates/textimport/src/lib.rs`.
- Counts were re-measured from this tag's code (`cmd!` ids via `git grep` on v0.13.0 and v0.14.0; `UI_COMMANDS` id sets diffed between the tags): 542 engine / 176 UI / 26 MCP tools / control methods +`ui.docking` / 10 CLI subcommands / format version 4. Live discovery beats this document: `designcraft-cli commands`, `designcraft-cli describe ID`, and `docs/gaps.md`.
- Deep automation tables (CLI, scripts, MCP tools, control methods, coordinates, guides/columns, layer options, EPUB split, story options, shortcut import, sample commands): `references/agent-surfaces.md`.
