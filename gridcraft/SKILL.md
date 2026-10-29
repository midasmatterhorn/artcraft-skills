---
name: gridcraft
description: >-
  GridCraft is an open-source, clean-room Rust reimplementation of Microsoft Excel: a spreadsheet
  app for macOS (also Windows, Linux, BSD and the web) that reads and writes real .xlsx files and
  can be driven headlessly through a CLI, an MCP server and a live JSON control channel. Use this
  skill whenever the user mentions GridCraft by name; asks what it can do or which formats,
  keyboard shortcuts, commands or worksheet functions it has; wants to create, edit, convert,
  calculate, print or export spreadsheets with it; wants to automate or script it (MCP, CLI,
  control channel, recorded scripts); needs inputs prepared for it (build or convert .xlsx, CSV,
  TSV, JSON, or convert .xls/.xlsb/.ods into .xlsx); wants its output verified, repaired or
  round-tripped (gridcraft-cli check); or reports a symptom (crash, wrong formula result,
  formatting lost on save, Excel saying "we found a problem with some content"). Trigger it even
  when the app is not named but the job is Excel-style spreadsheet work — "make me an Excel file",
  "add a formula column", "sort and filter this sheet", "pivot this data", "export this workbook to
  PDF", "read the values out of this spreadsheet". Do not assume Excel parity from Excel knowledge;
  check this skill first.
---

# GridCraft

**Audit basis:** this checkout is tag `v0.13.0`, commit `43284377d2466037628e57d8ad0c891778fdb45c` ("Release 0.13.0", 2026-10-28). The installed `/Applications/GridCraft.app` reports version `0.13.0` (`CFBundleIdentifier ai.storyteller.gridcraft`) and its binary prints `GridCraft 0.13.0`, so the bundle matches this source. **Verify against your installed version** if the ArtCraft Launcher has auto-updated since. Counts and formats below were re-derived from this tag's code and generated docs; every claim carries a repo-relative pointer.

## Overview

GridCraft is an open-source, clean-room reimplementation of Microsoft Excel's workflow in pure Rust (README.md), by the ArtCraft team; source: `github.com/storytold/gridcraft`. XLSX is the native document format, and the architecture is engine-first: every ribbon button, menu item, dialog OK, keystroke and mouse gesture is a *command* (`crates/engine/src/cmd/`), reachable over a JSON control channel, an MCP server and a headless CLI. Maturity is **alpha**: the core workflow (open XLSX → edit/format → sort/filter → chart/pivot → print to PDF → save XLSX) works end to end, but the project's own estimate is ~75% feature breadth and ~50% "ready for real work" (`docs/target-app-parity.md` summary; ROADMAP.md). It runs natively on macOS 11+, Windows, Linux and BSD, and in the browser via WebAssembly (`apps/gridcraft-web`). The UI migrated to egui 0.37 this release.

## Capabilities (verified)

### Core workbook and editing
- **One native window per workbook window (new this release):** `view.newWindow` opens another window **on the same workbook** — no clone, saving from either window saves it — `view.arrangeAll` tiles the windows, `window.list`/`window.close` are new engine commands, and a cell draft stays in its workbook (`crates/engine/src/cmd/extra.rs:167`; PRs #2616–#2619). Several workbooks open side by side; `view.switchWindows` and `window.activate {index}` switch between them.
- Three built-in samples `budget`, `sales`, `grades`: `file.new {sample}`, CLI `--sample`, URL `?sample=` (`crates/engine/src/sample.rs`).
- **354 engine commands** (353 at v0.12.1; +`window.close`, `window.list`); **275 of the 291 Excel catalog ids** implemented, 94.5% (unchanged) — `crates/engine/src/cmd/*.rs`, `crates/engine/src/catalog.rs`, generated `docs/parity-checklist.md`.
- Formatting: fonts, fills, borders, alignment, merges, Excel's number-format language (`crates/numfmt`), cell styles and themes, conditional formatting (CellIs, expression, text, top-10, above-average, time period, duplicate/unique, colour scale, data bar, icon set) and data validation (whole, decimal, list, date, time, text length, custom).
- Tables (structured references, header/total rows, banded rows, style gallery, Resize Table, remove duplicates), notes and threaded comments with replies/resolution/timestamps (**editing a note or comment keeps its thread** now, PR #2515), hyperlinks, pictures floating or inside a cell (PNG/JPEG only), shapes and text boxes (9 kinds), checkboxes, freehand ink with Ink to Shape, sparklines (line/column/win-loss; **removed when their row or column is deleted**, PR #2551).
- Editing: fill handle (drag; right-drag opens Copy Cells / Fill Series / Fill Formatting Only / Fill Without Formatting / Series…), AutoFill with the **Auto Fill Options** button, Flash Fill, Paste Special, Format Painter, Find/Replace, Go To (lists every sheet's defined names, takes several comma-separated targets), Watch Window, undo/redo with bounded history.
- **AutoSum: a selected row gets its total to the right, as in Excel** (PR #2561).
- **Options ▸ Formulas: Maximum Iterations and Maximum Change fields** (UI for the existing calc settings, PR #2493).
- Background error checking: green corner, warning button, Convert to Number, Circular References submenu.
- AutoSave switch in the title bar, persisted across restarts; it saves only workbooks that already have a file. Closing the window with unsaved work asks first.
- Slicers exist as in-sheet filter widgets over one table column, but are **not** written to XLSX.
- **Format Chart Area: Chart Type offers the stacked and 100% stacked types and marks the current one** (PR #2605).
- **Opening a saved workbook without recalculating it** is supported (PR #2512) — useful for inspection of files whose volatile formulas you do not want to run.

### Formulas and calculation
- **513 of Excel's 523 worksheet functions by name, 504 working (96.4%)** — unchanged — including dynamic arrays and spilling, LET/LAMBDA (a self-calling LAMBDA stops at 140 calls with `#NUM!`), MAP/REDUCE/SCAN/BYROW/BYCOL/MAKEARRAY, GROUPBY/PIVOTBY, structured table references, iterative calculation for circular references — `docs/function-parity.md`, `crates/functions/src/`, `crates/calc/src/eval.rs`.
- Evaluate without editing: `gridcraft-cli eval '=SUM(A1:A9)' --in book.xlsx` or `formulas.evaluate`. A formula that could not be typed into a cell is an error that says why, not a silent `#VALUE!`.
- Calculation settings travel with the workbook: automatic / automaticExceptTables / manual, iterative on/off, max iterations and max change (`formulas.calculationOptions`).
- Formula fixes this release: PERCENTRANK no longer returns `#NUM!` for very large significance, MINVERSE's rounding cutoff scales to the input matrix, ISOWEEKNUM/WEEKNUM(…,21) fixed for the first days of the calendar, YEARFRAC basis 0 fixed for February-end starts and 31st ends, IMSQRT no stray real part for negative reals, and range parsing fixed when the second end repeats the sheet name (PRs #2417, #2428, #2443, #2463, #2457, #2473); `datetime_from_serial` returns None past year 9999.
- Carried hardening: accounting negatives read as negative numbers; `INDEX(A1:C3,2)` on a 2-D reference is `#REF!`; REGEXREPLACE bounds each replacement; 16-million-cell budget charged before scanning.

### Files it reads and writes
- **`.xlsx` is native read/write**: cells, shared/array/dynamic formulas, styles, themes (including per-script typefaces; `<scheme val="minor"/>` is now kept on every body-font font on save), merges, conditional formats, validation, tables, notes and threaded comments, hyperlinks, names, freeze panes, outlines, print settings, pictures (shared media written once), shapes incl. ink, sparklines, PivotTables, sheet/workbook protection and Allow Edit Ranges, calc settings — **and each sheet keeps its sheetId across a rewrite** (PR #2513). XLSX save is faster (worksheet XML written without per-cell allocations, PR #2749).
- **Pass-through on save** (kept byte-for-byte when their owner survives): custom document properties, ribbon customisation, custom XML, external workbook links (never followed or refreshed), data connections, sheet query tables, printer settings, form/ActiveX controls, OLE objects, sheet backgrounds with their VML, header/footer pictures, and chart sheets.
- `.xlsm` / `.xltm` keep their VBA project byte-for-byte; macros are **never executed**. `.xltx`/`.xltm` save with the template content type.
- **Import-only**: `.xls`/`.xlt` (BIFF8: values, formulas, number formats, merges, sizes, names, calc and sheet-display settings; chart/macro/dialog sheets skipped), `.xlsb` and `.ods` (worksheet values and cached formula results only).
- **Text/data**: CSV and TSV/TXT/TAB with delimiter/encoding detection; writes the *displayed* text, keeps the separator a file was opened with, refuses output over 512 MiB; `file.open {csvAsText:true}` keeps every field as text. `.json` is a debug serde dump. HTML exports one sheet as a table (pictures as data-URI images, charts as inline SVG; refuses more than 100,001 rows).
- **`.pdf` export**: own PDF 1.7 writer; `file.exportPdf {path?, sheets?: active|all, range?, fitToPage?}` returns `{pages, bytes, path}` or base64; `file.print` returns the same PDF. `http(s)` hyperlinks and internal cell destinations become real PDF link annotations; `file:` links are omitted. The CLI prints huge and tiny numbers in exponent form now.
- **Password-encrypted `.xlsx` open** (Agile AES and Standard encryption, [MS-OFFCRYPTO]) via a `password` param; the Agile `dataIntegrity` HMAC is verified. RC4/Extensible and encrypted `.xls` are refused.
- **Save is refused** for `.xls`, `.xlsb`, `.ods` with an explanatory message. Content wins over the extension.
- Hard caps: 512 MB per decompressed XLSX part and 1 GB per package, 2 GB per file read, 100,001 HTML rows, 512 MiB CSV/TSV output, 16,000,000 cells per array result. Opening an XLSX now **warns for each skipped drawing object and chart** (PR #2555).

### Charts, PivotTables and analysis
- **26 `ChartKind`s**: column/bar/line/pie/doughnut/area/scatter/bubble/radar/histogram/waterfall/funnel/treemap/sunburst/box-whisker/stock/combo and subtypes; chartex parts for histogram/box-whisker/waterfall/funnel/treemap/sunburst, six trendline types, PivotCharts, Recommended Charts, Select Data, Switch Row/Column, Change Type/Colours/Layout.
- Chart objects move and resize; all 2-D kinds survive the XLSX round trip.
- PivotTables: field list, Filters/Rows/Columns/Values areas, report filters, layouts, date grouping, show-values-as, calculated fields, values on rows, grand totals, styles, refresh, change source; round-trip to/from XLSX. Show Details and Enable show details exist (command only).
- Data tools: sort (multi-key), AutoFilter, Advanced Filter, remove duplicates, text-to-columns, Flash Fill, group/ungroup/subtotals, consolidate, scenario manager, Goal Seek, data table; Outline Settings and Show Outline Symbols.
- Solver (Simplex LP with integer/binary branch-and-bound, augmented-Lagrangian nonlinear, Evolutionary; Answer and Limits reports), Forecast Sheet with hindcast, Analysis ToolPak (13 of Excel's 19 tools).
- Printing: native macOS/Windows/Linux printing through the pinned shared `craft-print` library, Page Setup, Page Break Preview, Page Layout view with rulers, draggable margins and in-place header/footer editing.
- Conditional formatting's New Formatting Rule formula box takes references clicked or dragged on the grid.

### Automation surface (the reason to read this skill)
Counts at this tag, with v0.12.1 in brackets: **354 engine commands** (353); **275/291 catalog ids** (unchanged); **22 MCP tools** (21 — added `list_windows`); **11 CLI subcommands** (11); **31 documented control-channel methods** (31) with 34 dispatch arms including aliases; **15 UI-only command ids** served by `engine.commands` (unchanged shape); **70 shortcut bindings on command specs** (70); **365 key-tip sequences** (365); **19 interface languages** (19); **26 chart kinds** (26); **513/523 worksheet functions** (513/523); **3 MCP resources** (3); **14 `check` round-trip categories** (14).

- **The control channel now requires a token (new this release):** the first line of a connection must authenticate with the app's token, and a connection that does not — or later sends a bad line — is closed (#777; `apps/gridcraft/src/control_server.rs:4`, `gridcraft_mcp::control_auth`). The token is `--control-token <token>` or `GRIDCRAFT_CONTROL_TOKEN` (≥ a minimum length), else 256 random bits written to a token file only the user can read whose path is printed to stderr (`gridcraft-cli` reads it) (`apps/gridcraft/src/control_server.rs:26-42`).
- **CLI `gridcraft-cli`** (headless; the app bundle ships no CLI): `info`, `convert`, `eval`, `cat`, `check`, `run`, `commands`, `functions`, `mcp`, `send`, `version` — `apps/gridcraft-cli/src/main.rs`.
- `check` is the one to remember: it recalculates every formula against the file's Excel-cached values (skipping volatile formulas and `fullCalcOnLoad` files), then writes and re-reads the workbook through GridCraft's own XLSX writer and compares 14 categories — package, sheets, values, formulas, numFmts, merges, names, tables, condFormats, validations, charts, comments, hyperlinks, pivots — and validates the package. Flags `--tolerance 1e-9` and `--max-report N`; exit 1 on any difference; `--json` emits schema `gridcraft-check/1`.
- **MCP server** over stdio, protocol `2025-06-18` (older clients answered in their own version); headless (`--in FILE | --sample NAME`) or remote (`--connect PORT`). **22 tools**: `execute_command`, `list_commands`, `inspect_workbook`, `read_range`, `write_range`, `set_cell`, `get_cell`, `evaluate_formula`, `select`, `format_range`, `insert_chart`, `create_table`, `sort_range`, `filter`, `open_workbook`, `save_workbook`, `new_workbook`, `undo`, `redo`, `screenshot`, `list_functions`, **`list_windows` (new — enumerates the open workbook windows)**.

  Resources: `gridcraft://workbook`, `gridcraft://commands`, `gridcraft://functions`; `prompts/list` is empty.
- **Control channel methods** (all behind the token now): read state — `engine.execute`, `engine.commands`, `engine.journal` (10,000 entries / 64 MB, passwords stripped), `document.inspect`, `sheet.read`, `cell.get`, `selection.stats`, `ui.inspect`; drive — `ui.click|drag|move`, `ui.cell.click|drag`, `ui.key|text`, `ui.edit.begin|text|commit|cancel`, `ui.ribbon`, `ui.dialog|set|confirm|cancel`, `ui.message.dismiss`, `ui.menu.invoke`; window/app — `ui.screenshot`, `ui.set`, `ui.resize`, `ui.focus`, `app.open|save|quit`. `ui.backstage {page}` and `ui.ribbonTab` are commands; any other method that is a command id runs that command.
- **UI-only commands** reachable over `engine.execute`/MCP (`engine.commands` marks them `"ui": true`): `ui.ribbonTab`, `view.collapseRibbon`, `view.expandFormulaBar`, `view.darkMode`, `view.theme`, `view.animations`, `options.autoComplete`, `view.interfaceScale`, `ui.dialog`, `ui.backstage`, `ui.printSettings`, `ui.printSubmit`, `app.language.set`, `app.language.english`, `app.language.japanese`.
- **Recorded scripts** (Automate tab): `automate.recordActions`, `automate.newScript`, `automate.allScripts`, `automate.runScript`, `automate.trustScripts`, `automate.deleteScript`, `automate.stopAction`. A workbook opened from a file that carries scripts starts untrusted; steps may not call `file.*`, `link.*` or `window.*` or pass a `path`. Scripts are stored in the workbook as the hidden defined name `_sc_scripts`, so they round-trip XLSX.
- **Engine building blocks**: undo groups, the recording buffer, document `Trust`, and the chunked hidden-name stash `_gc_<key>_<n>`.
- **Web build**: same UI crate via eframe web runner; URL flags `?sample=`, `?webgl`, `?host=parent&author=`, and **`?chrome=` lets an iframe host turn off the title bar and File tab** (new, PR #2444); preferences in `localStorage`; no TCP control channel.
- **Programmatic calls never open dialogs**: `file.open`/`file.save`/`data.getData`/`data.fromTextCsv` without a file path return "missing `path`…: programmatic calls never open dialogs".
- **Interface languages**: 19 (`Language::ALL`): en, es, el, zh, ja, ko, ru, pt, de, cs, fr, sr, tr, pl, it, uk, vi, nl, ro. Untranslated strings fall back to English; command ids, document text, formulas and number formats stay English/en-US. `app.language.set {language|code}` switches at runtime.

## Known limitations and not-implemented

- **Partial:** `.xls` import covers values, formulas, number formats, merges, sizes, names, print area/titles, calc settings and WINDOW2 sheet-display options; no fonts, fills, borders, charts, pictures, comments, conditional formats, validation, hyperlinks or freeze panes; chart/macro/dialog sheets are skipped, BIFF5 and FILEPASS files refused. `.xlsb`/`.ods` import values and cached formula results only. None of the three is ever written.
- **Encryption is read-only**: Agile and Standard `.xlsx` open with a password; saves are always unencrypted and have no save path, so Save asks where to go. RC4/Extensible and encrypted `.xls` are refused.
- **Macros never run.** VBA is carried byte-for-byte only into `.xlsm`/`.xltm`; any other save drops it. GridCraft's recorded scripts are not VBA.
- **Excel-repair-free output is unproven**: no real corpus and no Excel verification. Unmodelled content is dropped when its owner is rewritten — slicers and slicer caches, timelines, the data model, query tables attached to tables, unmodelled `extLst`; chart sheets are passed through unchanged but cannot be viewed, edited or created (open now warns for each skipped drawing/chart).
- **Slicers/timelines:** slicers can be created and clicked in-sheet but are not saved to XLSX; timelines are catalogued but not implemented.
- **Charts are shallow:** no 3-D types, no axis options (min/max/log/units), no error bars, no per-point formatting; data labels and gridlines are just booleans; ~26 of Excel's ~60 subtypes (~43%), chart sheets are not editable. Move and resize do work; the Format Chart Area dialog now offers the stacked/100% stacked types.
- **PivotTables:** no calculated items, `GETPIVOTDATA`, timelines, value/label filters, number grouping or data-model pivots; Show Details and Enable show details exist but have no Options dialog; XLSX round-trip has not been checked in Excel.
- **No Power Query or data model:** Get & Transform is only From Text/CSV, Get Data and From Table/Range; Refresh All refreshes PivotTables only. No From Web, Stocks, Geography, Relationships or Analyze Data.
- **Scale:** recalculation is single-threaded; the project reports ~100 MB workbooks failing to open (#175). Whole-range work is capped and refuses with an error instead of hanging.
- **Text:** no complex shaping (Arabic, Devanagari, Thai) and no bidi; a right-to-left sheet mirrors the grid and HTML export, but text stays LTR inside its box and printing/PDF are not mirrored. PDF export sets characters outside WinAnsi in a predefined, **non-embedded** Adobe-GB1 CID font (STSong-Light / UniGB-UTF16-H): Chinese is tested; Japanese/Korean coverage depends on that font; Arabic/Devanagari/Thai have no glyphs there.
- **Accessibility:** AccessKit is enabled but grid cells and the ribbon are not exposed as an accessible tree; Check Accessibility is a basic scan; no high-contrast mode.
- **No VBA/Office Scripts/add-in or custom-function API, no collaboration/co-authoring, no mobile build, no in-app AI.**
- **Functions:** 18 of Excel's 523 names are absent (including GETPIVOTDATA, IMAGE, STOCKHISTORY, TRANSLATE, DETECTLANGUAGE, CALL, REGISTER.ID, RTD, COPILOT, PY) and 9 are error stubs (7 CUBE functions, WEBSERVICE, FILTERXML).
- **HTML is export-only:** opening `.html`/`.htm` falls through to the CSV/TSV reader.
- **Objects:** inserted icons lose their artwork on XLSX save (#551); Office InkML is not imported; pictures must be PNG/JPEG.
- **Save semantics:** only `.xlsx` and `.json` saves clear the dirty flag and become the document's file; `.csv/.tsv/.html/.pdf` are exports that leave the workbook dirty. `file.close {force:true}` and the control-channel `app.quit` discard unsaved changes without asking.
- **Groundwork, not a feature:** `crates/ui-egui/src/code_editor.rs` (Python and LaTeX syntax colours) is exported but no dialog uses it yet — there is still no Python-in-cells (`PY`) or equation editor.
- **Stale repo prose** (verify against code, not docs): README says "89% of standard ribbon commands" while the generated checklist says 275/291 = 94.5%; `docs/target-app-parity.md` still reports 274/290 and "313 command ids"; several `docs/gaps.md`/`docs/ui-parity.md` rows contradict the code (PDF fonts, shortcuts, localization, solver, CSV raw values); `docs/control-protocol.md` does not yet describe the token authentication. Prefer code and the generated `docs/parity-checklist.md`.

## How to operate

### macOS launch, flags, environment
- `open -a GridCraft`; `open -a GridCraft book.xlsx` — Finder double-clicks and `open` arrive as Apple events, and files dropped on the window open too.
- The binary takes only these flags: `/Applications/GridCraft.app/Contents/MacOS/GridCraft [--control PORT [--control-token TOKEN]] [--sample budget|sales|grades] [files…]`; `--version` prints `GridCraft 0.13.0`.
- Environment: `GRIDCRAFT_CONTROL_PORT=<port>`, **`GRIDCRAFT_CONTROL_TOKEN=<token>`** (the control channel requires it), `GRIDCRAFT_NO_PREFS=1` (the mode for agent test runs), `GRIDCRAFT_NO_NATIVE_MENU`, `RUST_LOG`.
- Settings and logs live under `Library/Application Support/GridCraft/` in the user's home: `ui.json`, `prefs.json`, and `logs/gridcraft.log`, rotated to `.1`/`.2` at each start, 16 MiB cap.

### The CLI (installed separately)
The bundle ships no CLI. Install with `cargo install --path apps/gridcraft-cli` from a source checkout, or the release zip `gridcraft-cli-<ver>-macos-universal.zip`.

```sh
gridcraft-cli info book.xlsx [--json]
gridcraft-cli convert in.xls out.xlsx [--sheet Sales]     # .xlsx/.csv/.tsv/.json/.html/.pdf by extension
gridcraft-cli eval '=XLOOKUP("b",{"a","b"},{1,2})'        # → 2
gridcraft-cli cat book.xlsx --range A1:F20 [--formulas|--csv]
gridcraft-cli run --in book.xlsx --cmd 'cell.set={"cell":"D2","input":"=B2*C2"}' \
    --cmd 'edit.fillDown={"range":"D2:D20"}' --out book.xlsx --print A1:D5
gridcraft-cli check corpus/ --json --tolerance 1e-9       # calc oracle + XLSX round-trip fidelity
gridcraft-cli commands --search chart                     # every command and its params doc
gridcraft-cli functions --category statistical            # function list with signatures
gridcraft-cli send 7979 engine.execute '{"command":"home.bold","params":{"range":"A1:C1"}}'
```

- `run` flags: `--in FILE | --sample NAME`, repeated `--cmd`, `--script FILE`, `--out FILE`, repeated `--print RANGE|used`, `--sheet`, `--quiet`, `--csv`, `--formulas`. A `--cmd` is `id`, `id={json}` or `id {json}`; a script has one step per line; blank lines and `#`/`//` comments are skipped. The first failing step stops the run with a non-zero exit.
- `convert` refuses an unknown output extension; `.pdf` goes through `file.exportPdf` and reports bytes/pages.
- `check` never writes next to its inputs. `--json` output is schema `gridcraft-check/1`.

### MCP
```sh
claude mcp add gridcraft -- gridcraft-cli mcp                     # headless in-process session
claude mcp add gridcraft-app -- gridcraft-cli mcp --connect 7979 # drive the visible app
```
Results are one text block holding pretty JSON; failures set `isError: true`. Unknown tools, missing/wrong arguments are JSON-RPC `-32602`; malformed JSON `-32700`; unknown methods `-32601`. The remote backend uses a 30 s socket timeout: after a timeout, re-read the state instead of retrying blind. `list_windows` enumerates the open workbook windows; address a window where the backend accepts it.

### Control channel (drive the running app)
```sh
/Applications/GridCraft.app/Contents/MacOS/GridCraft --sample sales --control 7979
# stderr prints the token file path (or use --control-token / GRIDCRAFT_CONTROL_TOKEN), then
# newline-delimited JSON to 127.0.0.1:7979 — the FIRST line must authenticate with the token:
{"id":0,"method":"auth","params":{"token":"<token>"}}
{"id":1,"method":"engine.execute","params":{"command":"cell.set","params":{"cell":"B2","input":"=SUM(A1:A9)"}}}
{"id":2,"method":"ui.screenshot","params":{"path":"shot.png"}}
```
- **Authentication is required this release**: a connection that does not authenticate first is closed, as is one that later sends a bad line. `gridcraft-cli send` reads the token file automatically.
- Run `ui.inspect` first (ribbon tab, editor, open dialog, Backstage page, message, grid rect, scroll, perf, windows) and act on what it shows; `ui.screenshot` needs a presented frame.
- Limits: 64 MiB per request line; 10,000 queued synthetic pointer events; the server waits 60 s for the UI, then reports a timeout. A request the client abandoned is dropped unrun; if the app had already started it, the reply says the outcome is unknown — read the cell/state before retrying.
- The port binds localhost only and is token-authenticated; do not expose it.
- `ui.dialog.confirm` sends exactly what the dialog's OK sends; dialogs without an OK command return "this dialog has no OK command; drive it with its own commands".

### Document model and save/export flow
- **One native window per workbook window**: `view.newWindow` shares the workbook (no clone; saving from either window saves it), `view.arrangeAll` tiles, `window.list`/`window.close` manage windows, and `view.switchWindows`/`window.activate` switch workbooks. Sheet tabs at the bottom. File opens the Backstage with 9 pages: home, new (three samples), open (recents), info, saveAs, print, export, options, account.
- Save (`file.save`, `file.saveAs`, ⌘S, ⇧⌘S): the extension picks the format — `.xlsx` (default), `.csv`, `.tsv`, `.json`, `.html`, `.pdf`; a `.pdf` save exports the sheet and leaves the document dirty. `file.saveBytes {format}` returns base64 without writing.
- Exports: `file.exportPdf`, `file.exportCsv`, `file.exportHtml`, `file.printPreview`, and on the desktop `ui.printSettings` / `ui.printSubmit` (native jobs via craft-print).
- Opening a `.xls`/`.xlsb`/`.ods` produces a document titled `<name> (imported).xlsx` with no save path; opening an already-open path switches to it; a password-decrypted workbook also has no save path. Opening a saved workbook without recalculation is supported.

### Keyboard essentials (verified)
- 70 shortcut bindings on command specs (F3 → Paste Names, Ctrl+8 → Show Outline Symbols, Ctrl+Shift+U formula bar), plus a wider keymap table for number formats, borders, F-keys and Alt/Option combinations.
- Essentials: ⌘S save, ⇧⌘S Save As, ⌘O open, ⌘N new, ⌘W close, ⌘Z undo, ⌘Y redo; ⌘B/⌘I/⌘U; ⌘1 Format Cells; ⌘D fill down, ⌘R fill right; ⌃E Flash Fill; ⌘T table; ⌘K link; Ctrl+Shift+L filter; F2 edit; F3 Paste Name; Ctrl+Shift+4 currency; Ctrl+Shift+7 outline border; Ctrl+` show formulas; F9 calculate; Ctrl+[ / Ctrl+] precedents/dependents; Ctrl+6 hide/show objects; Ctrl+8 outline symbols; Ctrl+Shift+U formula bar. Shift+Arrow on a whole column/row keeps the view on the rows/columns it showed (PR #2497).
- Key tips: F10 (or left Alt on Windows/Linux/BSD), then sequence letters; 365 sequences cover every ribbon tab.
- The macOS native menu has Tools ▸ Command Palette… (⌘⇧P).

## Working with an AI agent

**Prefer headless over GUI.** For read/write/convert/verify jobs use `gridcraft-cli` (or MCP) on files: no window, no preferences (set `GRIDCRAFT_NO_PREFS=1` if you launch the app), deterministic. Drive the GUI over the control channel only when the task is genuinely about the UI. Never drive blind — `ui.inspect`/`ui.screenshot` before and after.

Legitimate agent work:
- **Prepare inputs.** Build `.xlsx` from commands (`gridcraft-cli run --script steps.jsonl`), convert `.xls`/`.xlsb`/`.ods`/CSV/TSV into `.xlsx`, or generate CSV/TSV/JSON and import. Use `file.open {csvAsText:true}` when leading zeros must survive. Remember an import opens as an unsaved "(imported).xlsx".
- **Interpret/repair files.** XLSX is native and documented in code. "Repair" means: open in GridCraft, inspect (`info`, `check`), fix with commands or formulas, save as `.xlsx`. Do not promise recovery of parts GridCraft does not model. Open without recalculation when you only want to inspect values.
- **Verify exports honestly.** Run `gridcraft-cli check` on round-tripped files, compare `cat`/`info` output against expectations, check PDF page counts and links. A zero exit from `check` means GridCraft agrees with itself and with the file's cached values; it does **not** prove Excel will open the file without a repair prompt.
- **Scripts.** Recorded scripts are a convenience layer over the same command ids. A workbook received from elsewhere carries its scripts as a hidden name; nothing runs until the workbook is trusted, and script steps cannot touch files, links or windows. A leftover undo group blocks undo/redo: clear it with `automate.stopAction`.
- **Work with two views**: `view.newWindow` now shares the workbook — two windows, one document; `list_windows` (MCP) and `window.list` enumerate them; `view.arrangeAll` tiles.

Must NOT attempt:
- Writing `.xls`/`.xlsb`/`.ods`, or saving password protection; expecting macros to run; expecting slicers/timelines to survive a save; assuming HTML import.
- Raw XML surgery on `.xlsx` files that contain unmodelled parts: GridCraft's own writer is the supported path, and even it drops parts it does not model once it rewrites them. Prefer read-only analysis of such files.
- Treating formulas as locale-independent without checking `docs/formula-input.md`: Spanish input/display exists, but files, commands and APIs use canonical English names and `,` separators.
- Promising PDF output for Arabic, Devanagari or Thai (no glyphs in the CID font, no shaping); verify CJK output visually first.
- Calling `app.quit` or `file.close {force:true}` while a workbook has unsaved changes: both discard them silently. Save first.
- Connecting to a `--control` port without the token (the connection is closed), or assuming the channel is unauthenticated — it is not, since this release.

## Verification protocol (alpha discipline)

1. **Throwaway round-trip before real work**: new workbook → the exact edit → save `.xlsx` → reopen (or `gridcraft-cli info`/`cat`) → `gridcraft-cli check file.xlsx`. Add the source file itself to `check` when testing formula fidelity.
2. **Never trust a silent export.** CSV/HTML/PDF are one-shot exports with no diff UI. Re-read or re-import the artifact. Remember PDF export cannot be assumed to render Arabic/Devanagari/Thai.
3. **Version and back up.** Keep the previous copy of any workbook you edit; autosave covers only workbooks that already have a file. For agent runs, save after each logical step (`--out`) rather than at the end.
4. **Update between projects, not during.** The app auto-updates through the ArtCraft Launcher; update, then re-run your round-trip before a new task.
5. **After a control/MCP timeout, re-read state** (`cell.get`, `sheet.read`, `document.inspect`) before retrying: a queued request is dropped, but one already taken may still finish.
6. **Trust deliberately.** Do not call `automate.trustScripts` on a workbook you did not create unless the user asked you to run its scripts.

## Sources & evidence

- Repo: https://github.com/storytold/gridcraft — inspected at tag **v0.13.0**, commit `43284377d2466037628e57d8ad0c891778fdb45c` ("Release 0.13.0", 2026-10-28). The installed `/Applications/GridCraft.app` prints `GridCraft 0.13.0`. If your installed version differs, verify against it.
- Date of inspection: 2026-10-29. Repo treated read-only (not built or modified).
- Key files read: `README.md`, `Cargo.toml`, `docs/{cli,mcp,control-protocol,parity-checklist,function-parity,chart-parity,file-format-parity,gaps}.md`, `apps/gridcraft-cli/src/{main.rs,check.rs}`, `apps/gridcraft/src/{main.rs,control_server.rs}`, `apps/gridcraft-web/src/main.rs`, `crates/engine/src/{io.rs,lib.rs,sample.rs,catalog.rs,record.rs}`, `crates/engine/src/cmd/` (incl. `extra.rs` window commands), `crates/xlsx/src/`, `crates/pdf/src/lib.rs`, `crates/mcp/src/{tools.rs,server.rs,backend.rs}`, `crates/ui-egui/src/{control.rs,keymap.rs,ribbon.rs,lib.rs,dialogs.rs,grid.rs,i18n/}`, `crates/model/src/{features.rs,workbook.rs,sheet.rs}`, `crates/functions/src/`, `crates/calc/src/eval.rs`, `apps/gridcraft/Cargo.toml`.
- Counts were re-measured from code, not prose: commands by `cmd!` ids (diffed against a fetched `v0.12.1` ref — +`window.close`, +`window.list`); MCP tools by `tool(` calls (+`list_windows`); catalog coverage by the generated `docs/parity-checklist.md` (275/291); languages by the `i18n/` directory (19).
- Shared libraries: the craft-libs crates (incl. `craft-print`) are pinned to one revision, `92d392cf…`, this release.
- Deeper per-topic reference (repo docs): `docs/target-app-parity.md`, `docs/gaps.md`, `docs/architecture.md`, `docs/parity-checklist.md`.
