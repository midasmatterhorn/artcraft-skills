# DesignCraft agent surfaces at a glance

All paths are repo-relative to https://github.com/storytold/designcraft.

Verified at tag v0.14.0, commit `7da69c16ce221f46e8f27cb41e0c88167c8be416`, 2026-10-29.
Installed `/Applications/DesignCraft.app` reports `0.14.0` and the same build commit.

## 1. CLI (`designcraft-cli`)

Source: `apps/designcraft-cli/src/main.rs` (module doc; the `USAGE` const; subcommand dispatch in
`main`). Not inside the macOS `.app` — install the separate
`designcraft-cli-<ver>-macos-universal.zip` release asset, `cargo install --path
apps/designcraft-cli --locked` (`docs/mcp.md` §From source), or build `cargo build --release -p
designcraft-cli`.

```text
designcraft-cli run [--in FILE | --sample] [--cmd ID[=JSON]]... [--page N] [--scale S]
                    [--pdf-options JSON] [--export OUT] [--all-pages DIR]
designcraft-cli commands [FILTER]        # engine commands as JSON
designcraft-cli describe COMMAND         # label, menu, shortcut, params for one command
designcraft-cli script [FILE|-] [--in FILE | --sample] [--connect PORT]
                       [--save OUT] [--export OUT] [--keep-going]
designcraft-cli app [--port PORT] COMMAND [JSON]
designcraft-cli app [--port PORT] --method METHOD [JSON]
designcraft-cli mcp [--connect PORT] [--sample]
                    [--automation-read-root DIR]... [--automation-write-root DIR]...
designcraft-cli perf [--pages N] [--frames N] [--chars N] [--images N] [--runs N] [--strict]
designcraft-cli bench FILE [--runs N]
designcraft-cli validate-pdf FILE.pdf    # built-in PDF/X-4 checks
designcraft-cli links
designcraft-cli --version
```

- `run`: `--page`, `--scale` and `--pdf-options` apply to the exports that follow them; one after
  the last export is an error, and a bad export extension fails before anything runs.
  `--export` writes the type its extension names: `.png` or no extension (a page; `.jpg`/`.jpeg` →
  JPEG), `.pdf`, `.designcraft` (Save As), `.idml`, `.epub`, `.pptx`, `.html`/`.htm`, and
  `.rtf`/`.txt` (the story being edited or of the selected frame); any other extension is an error.
  `--cmd id={"json"}` runs commands with `$N.path` result references; results print as JSON, and a
  params key the command's description doesn't name is an error. `--all-pages DIR` writes
  `page-001.png`… at the current scale.
- `app` defaults to port 7979 (`--port`/`--connect`); `--method` calls any control-channel method.
- `mcp`: the automation roots confine every file the agent's commands read (open, placed images,
  data sources, libraries) and write (save, export, package), links followed. **Each flag may be
  given more than once at this tag (#1552)**, in `--flag DIR` and `--flag=DIR` spelling; a path
  inside any root of its kind passes, and the roots' common parent, `..`, a link out of them or the
  other kind's roots stay refused. A kind left out grants none of its access; combining the roots
  with `--connect` is an error (`apps/designcraft-cli/src/automation_args.rs`, `docs/mcp.md`).
- `script --save` is Save As after the script succeeds; `--export` routes like `run` but
  `.designcraft` writes a copy (`file.saveACopy`).
- Exit status is non-zero on failure; `script --keep-going` records errors per step instead.
- `validate-pdf FILE.pdf` prints `{path, standard: "PDF/X-4", valid, issues}` and exits non-zero
  when a check fails. Checks: PDF version, output intent and profile, Info and XMP identification,
  image interpolation, encryption, trim boxes, Type 3 fonts, device RGB under a CMYK output intent,
  and **fonts that draw visible text without an embedded font program** (including inside placed
  PDF forms) — with font names and pages. Render mode 3 (invisible OCR text) is exempt
  (`crates/pdf/src/pdfx.rs:212`, `crates/pdf/src/pdfx/fonts.rs:16`, `docs/agents.md`).
- `perf`/`bench` measure budgets on a synthetic stress document or a real file
  (`apps/designcraft-cli/src/perf.rs`); `--strict` exits non-zero when a budget is exceeded.
- **Unknown parameter keys**: `run --cmd`, `script` steps (through the backend), MCP and the control
  channel reject a key the command's params description doesn't name (`crates/engine/src/cmd/
  params.rs:224`, `check_params`; `apps/designcraft-cli/src/main.rs`; `crates/ui-egui/src/control.rs:164`).
  `Session::execute` itself only checks in `#[cfg(test)]` builds, so the in-app Scripts panel is the
  one path that may ignore an unknown key. `docs/agents.md`'s "most commands ignore parameters they
  don't know" is stale for the CLI/MCP/control path.

## 2. Script syntax (`designcraft-cli script`, `script.run`, MCP `batch`)

Source: `apps/designcraft-cli/src/main.rs` `SCRIPT_HELP`; `crates/engine/src/script.rs`;
`docs/agents.md`.

```text
command.id {"param": 1}            # one step per line; also command.id={json} or bare id
{"command": "command.id", "params": {...}}    # JSON-lines form, or a JSON array
# comment / // comment             # blank lines skipped; UTF-8 ± BOM; LF or CRLF
```

- `"$N.path"` = value at `path` of step N's result (0-based; comments/blank lines are not steps);
  `"$last.path"` = previous step; `"${N.path}"` interpolates inside a longer string; `"$$"` writes a
  literal `$`; any other string starting with `$` stays as written.
- Text parameters: `\n` = new paragraph, `\u2028` = forced line break (`\u000b`, Word's line
  break, is read as one too), `\t` = tab.
- Result: `{"completed": n, "results": [...]}`, plus `failedIndex`/`failedCommand`/`error` on
  failure; `--keep-going` converts failures to `{"error": …, "command": …}` results.
- `script.run` (the Scripts panel) runs the same text as one undo step and restores the document,
  selection and history when a step fails (`crates/engine/src/cmd/scripts.rs`).

## 3. MCP tools (`designcraft-cli mcp`) — 26, unchanged at v0.13

Source: `crates/mcp` (`tools.rs` — `tool_definitions` :83, `dispatch` :555; `server.rs`, `headless.rs`,
`backend.rs`); `docs/mcp.md`. `crates/mcp/src/tools.rs` is byte-identical to v0.12.0.
Protocol: newline-delimited JSON-RPC 2.0 on stdin/stdout (`2025-06-18`, also `2025-03-26`,
`2024-11-05`); logs on stderr. An argument a tool doesn't take, and a command `params` key the
command doesn't name, are invalid-params errors; `execute` and `batch` check every step before the
first runs.

| Group | Tools |
|---|---|
| commands (3) | `list_commands` (filter, enabledOnly; returns `{count, commands}`), `execute`, `batch` |
| document (7) | `inspect_document`, `get_story`, `set_story_text`, `new_document`, `open_document`, `save_document`, `place_image` |
| render (3) | `render_page`, `export_png`, `screenshot` |
| input (5) | `select_tool`, `pointer`, `key`, `type_text`, `ime` |
| window (8) | `click`, `drag`, `menu_list`, `ui_inspect`, `ui_set`, `dialog_set`, `dialog_confirm`, `dialog_cancel` |

- Headless: in-process `designcraft_engine::Session`, starts with an empty Letter document;
  `--sample` opens the sample magazine. `--automation-read-root`/`--automation-write-root` confine
  file access (in-process only, repeatable).
- Connected: `--connect PORT` (or `HOST:PORT`) proxies to the running app; window tools
  (`screenshot`, `click`, `drag`, `menu_list`, `ui_inspect`, `ui_set`, `dialog_*`) return an
  error in headless mode, and UI-only commands (`view.*`, `window.*`, `help.*`,
  `edit.dynamicSpelling`, `app.*` except `app.links`) error too (`docs/mcp.md` "Modes"). This is
  how `window.importShortcuts`, `view.goBack`/`view.goForward` and the new paragraph dialogs are
  reached from MCP.
- Connected `list_commands` returns engine **and** UI commands (UI entries carry `"ui": true`);
  headless `list_commands` returns engine commands only.
- Resources: `designcraft://document`, `designcraft://commands`. `app.links` works everywhere;
  `help.about {tab?}` opens the About window in the running app.

## 4. Control channel (`designcraft --control PORT`)

Source: `apps/designcraft/src/control_server.rs` (`MAX_LINE` = 4 MiB :22, `MAX_CONNECTIONS` = 16
:24); `crates/ui-egui/src/control.rs` (`handle_request` :149); `docs/control-protocol.md`. Start with
`designcraft --control PORT` or `DESIGNCRAFT_CONTROL_PORT`. JSON lines on `127.0.0.1`; one
request/one reply per line (the reply echoes the request's `id`). `control.rs` and
`control_server.rs` are unchanged from v0.12.0: still 26 dispatch arms (the table below collects
the grouped aliases).

Rules that matter: only requests are read; a line that is not a JSON object with a string `method`
gets one error reply and the connection is closed, so anything after it on that connection never
runs; max 16 connections; lines are capped at 4 MiB; no authentication (enable only while in use);
the web build has no control channel. Clients that get an error reply should reconnect
(`docs/control-protocol.md`).

| Method | Params / purpose |
|---|---|
| `engine.execute` / `ui.menu.invoke` / `command` | `{command, params}`; without `params`, `ui.menu.invoke` acts like choosing the menu item (opens dialogs); an unknown params key is an error |
| `engine.commands` | every engine command plus UI commands (`"ui": true`) in the running app |
| `document.inspect` | pages (incl. `gutter`, `customColumns`, `columnRects`), spreads, items, stories (overset), styles, swatches, selection (incl. `guides`), `canUndo` |
| `ui.inspect` | tool, UI state, view, canvas rect, window, documents, dialog, perf |
| `ui.menu.list` / `ui.tool.list` / `ui.tool.select` | menus / tools / select a tool |
| `ui.pointer` | `{events:[{kind: down\|drag\|up\|move\|doubleclick, x, y, space? ("screen"\|"canvas"; default doc points), clicks?, mods?}], mods?}` through the active tool; returns selection, tool, cursor |
| `ui.key` / `ui.text` | `{key, shift?, alt?, cmd?, ctrl?}` synthetic key / `{text}` inserts at the explicit caret, or types into a focused field or dialog |
| `ui.ime` | `{preedit?, active?: [start, end], commit?}` input-method events as the system IME sends them |
| `ui.paste` | `{text}`: what Ctrl/Cmd+V delivers (text, or SVG markup as editable paths); the system clipboard is never read |
| `ui.move` / `ui.click` / `ui.drag` | real egui pointer input in screen points (reaches widgets/menus/dialogs); `button?`, `count?` (1–255), `steps?` (drag, default 8) |
| `ui.set` | `brightness`, `panel`, `status`, `rulers`, `frameEdges`, `guides`, `baselineGrid`, `documentGrid`, `textThreads`, `screenMode`, `zoom`, `page` (1-based), `fit`, `controlBar`, `closePanel`, `dockExpanded` |
| `ui.dialog.open` / `.set` / `.confirm` / `.cancel` | open a dialog by id (`{id, fields?}`) and fill/close it |
| `ui.resize` / `ui.focus` | window size / focus |
| `ui.screenshot` / `ui.render` | window PNG / headless page render (page 0-based, scale, bleed; PNG, or base64 without a path) |
| `app.open` / `app.save` / `app.export` | files (export = PNG of a page) |
| `app.quit` | quits **without** asking about unsaved changes (the `app.quit` command / ⌘Q asks) |

Notes: default shortcuts owned by the macOS native menu (incl. Command-Z) are skipped by the
egui shortcut handler; after a drag wait for both the expected document state and
`document.inspect.canUndo` before testing undo; `ui.key` does not synthesize Cocoa menu events —
use `ui.menu.invoke` to test a menu command (`docs/control-protocol.md`). `ui.click`/`ui.drag`
validate the whole gesture before queuing input: at most 10,003 pending events
(`MAX_PENDING_POINTER_EVENTS`, `crates/ui-egui/src/control.rs:118`); a click uses
1 + 2×`count`, a drag 1 + `steps` + 2×`count`; over-budget requests return `ok: false` and leave
the queue unchanged.

Panel docking is driven by UI commands through `engine.execute` (`docs/control-protocol.md` §Shared
panel docking): `window.panel.move {panel, anchor, zone?: tab|center|left|right|top|bottom, before?}`,
`window.panel.float {panel, x?, y?, width?, height?}`, `window.panel.dock {panel, anchor?, zone?,
before?}`, `window.panel.activate {panel}`, `window.panel.close {panel}`, and
`window.panel.layout {action}` with the shared MoveFloating/ResizeSplit/Move/SetStackOpen schema.

Headless window screenshots with no visible window:
`cargo run -p designcraft-ui-egui --example ui_shot -- script.jsonl`
(`crates/ui-egui/examples/ui_shot.rs`): each line is a control request, `{"shot": "out.png"}` or
`{"steps": n}`; a first line `{"empty": true}` skips the sample document.

## 5. Coordinates and text offsets

- Points (1/72 in), y down, spread space; page indices for `render_page`/`export_png` are
  0-based; commands that create items take `spread` (body index,
  `{"kind":"parent","index":0}`, or `{"kind":"doc","index":n}`) (`docs/mcp.md`). `pointer`
  events may use `"space": "screen"` (egui points, see `ui_inspect` → `canvasRect`).
- `guide.*` and `layout.moveColumnGuide` take `page` as the page's index **within its spread**;
  `document.inspect` page `index` is absolute and each spread lists its own `pages` array — map
  between them by position.
- Story text positions are UTF-8 byte offsets (é = 2 bytes; — and は = 3): `anchor`/`focus`,
  `start`/`end`, `pos`, story `length`, overset position; an offset inside a character snaps to
  its start — except in `story.replaceRange`, where it, an `end` past the story, or a crossed
  range is an error that leaves the story unchanged (`docs/mcp.md` "Text offsets").
- `layout.pages.insert` takes `count` 1–9999 and `after` as a 0-based page index (default: the last
  page) (`crates/engine/src/cmd/layout.rs`).

## 6. Guides and custom column guides

### Ruler guides

| Command | Params / result |
|---|---|
| `guide.add` | `{orientation: horizontal\|vertical\|both, position, point?: [x,y], spread?, page?, at?, spreadGuide?, liquid?}` → `{page, index}` or `{guides: [...]}` for `both` |
| `guide.move` | `{spread?, page, index, position}` → null |
| `guide.moveBy` | `{dx?, dy?, guides?: [{spread?, page, index}]}` (default: selected) → `{moved}` |
| `guide.list` | `{spread?}` → `[{page, index, orientation, position, spread, selected}]` |
| `guide.select` | `{page, index}` or `{guides: [...]}`, `add?`, `toggle?` → `{selected}` |
| `guide.selectAll` | `{spread?}` (menu Edit, `Cmd+Alt+G`) → `{selected}`; skips locked/hidden layers |
| `guide.deselect` | `{}` |
| `guide.delete` | `{page, index}` or `{}` for the selection → `{deleted}` |
| `guide.deleteAll` | `{spread?}` → `{deleted}` |
| `layout.createGuides` | `{rows?, columns?, rowGutter?, columnGutter?, fitTo?: margins\|page, removeExisting?, spread?, page?}`; rows/columns 0–1000 |

- Positions are spread coordinates and must be finite, within ±1,000,000 pt. At most 10,000 guides
  per `guide.add`/`layout.createGuides` (`crates/engine/src/cmd/guides.rs:20,25,130`).
- Guides live on a page, on the active layer (`guide.add`). `spreadGuide: true` makes a guide cross
  the pasteboard; `liquid: true` makes a Page-tool liquid guide (page guides only).
- `view.lockGuides {on?: bool}` (UI command, `Cmd+Alt+;`) only blocks pointer dragging and persists
  in `ui.json`; commands still move a guide unless the guide or its layer is locked/hidden
  (`Guide::editable_in`, `crates/doc/src/page.rs`). Put guides on a layer and lock the layer to
  protect them from commands.
- Dragging snaps along the guide's axis to other guides, margins, columns, bleed, page and object
  edges/centres, and the document grid; Shift snaps to ruler ticks, Cmd suspends snapping
  (`crates/ui-egui/src/canvas.rs` `guide_spot`, `crates/tools/src/snap.rs` `Gesture::Guide`).

### Column guides

Column positions are stored per page (`Columns.positions`: 2 × count offsets from the margin box's
left edge) and validated: finite, ascending, first 0, last margin width, ≤ 216 columns
(`crates/doc/src/page.rs` `valid_column_positions`, `MAX_COLUMNS` :46).

| Command | Params / result |
|---|---|
| `view.lockColumnGuides` | `{on?: bool}` (default: toggle) → `{locked}`; document setting, default **true**, saved in the document and IDML `ColumnGuideLocked` |
| `layout.moveColumnGuide` | `{spread?, parent?, page, gutter, position}` → `{positions, left}`; refuses while column guides are locked |
| `document.inspect` | each page has `columns` (count), `gutter`, `customColumns`, `columnRects` |
| `layout.marginsAndColumns` | keeps custom positions unless `columns` or `gutter` changes; margin-width changes scale them |
| `file.place {autoflow}`, `layout.pages.insert`, `layout.parents.new` | carry custom positions to new pages/parents; pages that cross the spine mirror them |

- `gutter` 0 is the gutter between the first two columns. `position` is the new left edge of that
  gutter in spread x. Both edges move together, keeping the gutter width, clamped to neighbouring
  gutters/margins. The reply's `positions` are offsets from the margin-box left edge; `left` is in
  spread x.

## 7. Placed graphics, placed PDFs and layer options (v0.13)

### Placed-PDF layer visibility

| Command | Params / result |
|---|---|
| `object.pdfLayers` | `{id?}` → `[{name, visible, default, overridden}]`; with no explicit id, the first placed PDF anywhere in the selection |
| `object.layerOptions` | `{ids?, hidden: [layer name], useDefaults?: bool}` → `{hidden, useDefaults}` |

- `useDefaults: false` with an empty `hidden` list means **explicitly all on**; legacy `hidden: []`
  (no `useDefaults`) resets to the file defaults; `useDefaults: true` cannot be combined with a
  non-empty `hidden` (`crates/engine/src/cmd/pdflayers.rs`). `object.pdfLayers` with an explicit
  non-PDF `id` is an error; `object.layerOptions` filters its targets down to placed PDFs and
  errors only when none of them is one.
- Every explicit choice is validated by one real visibility rewrite per distinct source **before**
  any item is edited or an undo step recorded, so a mixed selection stays atomic; a layerless or
  unrewritable PDF is refused with a message telling you to use the file defaults or replace it.
  Resetting to defaults needs no rewrite and is always allowed.
- Output: plain and PDF/X-4 export keep vector artwork and optional content with the file defaults
  or per-placement overrides, including independent states for repeated placements, booklet output
  and book merging. PDF/A-2b prepares an export-only 300 ppi raster copy with the choices applied.
  Embedded IDML export stores a separate PDF variant per placement; external-only IDML export is
  rejected when a choice would be lost, and `file.package`'s report names a placement whose choice
  the packaged IDML copy cannot carry (`docs/pdf-layer-visibility.md`,
  `crates/pdf/src/optional_content.rs`).

### Retained IDML graphic-layer options (not rendered)

- IDML `GraphicLayerOption`/`GraphicLayer` settings are kept on each `Graphic.layer_options`, per
  placement, not on the shared asset; scalar attributes, layer order, parent/child links, IDs,
  names, original/current visibility, link-update policy and view/export/print flags survive import,
  native save/reopen and IDML export. Native files that hold them require **format version 4**, so
  older readers refuse them instead of silently dropping the field (`crates/doc/src/assets.rs:48`,
  `docs/graphic-layer-options.md`).
- This is preservation, **not layer-aware rendering**: the renderer and PDF exporter use the asset's
  composite/default appearance. Changed visibility or explicit view/export/print states produce an
  import warning, a persistent `unsupportedGraphicLayers` preflight issue and a PDF export warning.
  Do not promise appearance fidelity from a retained IDML layer choice.

## 8. New and changed engine/UI surfaces at v0.14.0 (v0.13 items below still apply)

### EPUB Split Document

| Command | Params / result |
|---|---|
| `document.epubSplit` | `{split?: "off"\|"exportTags"\|{style: name}}` → `{split}` (query with no `split`); stored with the document, survives rename and IDML (`EPubExportPreference`) |
| `file.exportEpub` | adds `split?: "off"\|"exportTags"\|{style: name}` for one export (document setting by default) |
| `style.exportTag` | adds `split?: bool` (paragraph styles only; EPUB-only Export Tagging flag) |

- `off` (default) writes one content file; `exportTags` splits before each paragraph whose style has
  Split Document on; `{style}` splits before each paragraph of that style. Navigation and note links
  point across the files (`crates/epub/src/lib.rs:42,1063`; `crates/engine/src/cmd/export.rs:15,19`).

### Type, notes and variables

| Command | Params / result |
|---|---|
| `story.options` | `{story?, frame?, opticalMargin?: bool, opticalMarginSize?: pt (0.1–1296, default 12)}` → `{stories}`; Story panel; `type.selectionAttrs.storyOptions` mirrors it (`null` where stories differ) |
| `type.para` / paragraph styles | `ignoreOpticalMargin?` opts a paragraph out of the story's hanging punctuation |
| `list.bullets` / `list.numbers` | `{on?: bool}` (default: off when every selected paragraph has the list, else on); applies/strips the default hanging indent (18 pt / −18 pt) |
| `note.convertFromText` | `{author?}` → `{story, id}`; selected text becomes a new note |
| `note.next` / `note.previous` | `{}` → `{story, id, pos}`; caret after the neighbouring note's anchor; unavailable in table cells/footnotes |
| `variables.convertToText` | `{}` — selected variable instances become the text they show on their page |
| `variables.convertAllToText` | `{name}` — every instance of one variable in the document becomes text; the variable stays defined |
| `app.hyphenationDialog` | `{}` — Hyphenation Settings of the selected paragraphs (UI command; connected app only) |
| `app.keepOptionsDialog` / `app.nestedStylesDialog` / `app.grepStylesDialog` | `{}` — the matching Paragraph Style Options sections for the selected paragraphs (UI commands) |

### Alignment, navigation and recent files

| Command | Params / result |
|---|---|
| `selection.key` | `{id}` — makes a selected item (≥ 2 selected) the Align key object; toggling clears it |
| `object.align` | `{edge, to?: selection\|keyObject\|margins\|page\|spread, ids?}`; `to` defaults to `keyObject` while a key object is set |
| `view.goBack` / `view.goForward` | `{}` (UI, `Cmd+PageUp`/`Cmd+PageDown`) — retrace page jumps at the current zoom; a new jump drops the pages ahead; scrolling adds no entry; deleted pages are skipped (`crates/ui-egui/src/page_history.rs`) |
| `file.openRecent` | `{index}` (engine) — open an entry from File › Open Recent |
| `app.openRecent` | `{index}` (UI) — the same with an alert when the file can't be opened |
| `prefs.set` | `recentFilesMax?: 0–100` (default 20) trims/extends the recent list |

### Export and print changes

- `file.exportPdf` adds `created?: int (Unix seconds)` for reproducible output (default: now).
- `file.print` adds `created?: int` too.
- `file.exportPdf` with `standard: "x4"` and `designcraft-cli validate-pdf` now report fonts that
  draw visible text without an embedded font program, including inside placed PDF forms; invisible
  (render mode 3) text is exempt. Nothing embeds, substitutes or outlines those fonts automatically
  (`docs/gaps.md` §28).

## 9. Shortcut import (`window.importShortcuts`)

Source: `crates/ui-egui/src/shortcut_import.rs` (unchanged from v0.12.0); UI command entry in
`crates/ui-egui/src/menus.rs`; `docs/file-format-parity.md` keyboard row.

```text
window.importShortcuts {path | text}
  → {set, imported, changed, conflictsCleared, skipped, unmatched,
     unmatchedWithoutShortcut, unreadable}
```

- Input is a set saved by InDesign's Keyboard Shortcuts ▸ **Show Set**: `.txt`, UTF-8 (BOM
  accepted) or UTF-16 (BOM or zero-byte pattern), Windows (`Shift+Ctrl+S`) or Mac (`⇧⌘S`) key names,
  at most 8 MiB (`MAX_BYTES` :17). Lines are `<item> --- <context>: <keys>, <context>: <keys>` or
  `[none defined]`.
- Matching: menu path + label first, then engine menu placement, then a unique label. Only the
  **Default** context applies; a type/text command with no Default entry takes its **Text** entry.
  A matched command takes the set's shortcut (or loses its own when the set says `[none defined]`);
  commands holding a key the set takes lose theirs and appear in `conflictsCleared`. When two items
  want the same keys, the later one wins and the earlier is listed in `skipped` with `takenBy`.
- `changed` lists `{id, label, item, from, to}`. `unmatched` lists `{item, keys, reason?}`; tool
  items that cannot change are marked `reason: "tool keys are fixed"`. `unreadable` lists
  unreadable key strings with a reason. `imported` counts applied decisions.
- Limitations: no `.indk` files, no non-Default contexts, no Control-key chords (macOS Control is
  not a command modifier here), no writing/exporting a set. It is a UI command: headless MCP errors;
  use the connected app (`designcraft-cli app window.importShortcuts …` or MCP connected `execute`).
- Reset everything with `window.resetShortcuts {}`; set one command with
  `window.setShortcut {id, shortcut: "Cmd+Alt+J" | "" | null}` → `{shortcut, conflicts}`.

## 10. Sample commands that create content

| Command | Params (from the command registry) |
|---|---|
| `file.new` | `{preset?, intent?, units?, width?, height?, pages?, startPage?, facingPages?, columns?, gutter?, margins?, bleed?, slug?, title?, primaryTextFrame?}` — new documents get `[Basic Paragraph]` hyphenation defaults (capitalized/last word/across column off) |
| `file.newSample` | `{}` — multi-page magazine (`crates/engine/src/sample.rs`) |
| `frame.create` | `{spread?, rect: [x0,y0,x1,y1], shape?, content?, sides?, starInset?, text?, caret?, vertical?}` → `{id, story?}` |
| `text.thread` | `{from?, to?, rect?, spread?, autoflow?}` → `{story, from, to, overset, pagesAdded}`; autoflow fills the following pages before adding pages |
| `file.place` | `{path\|base64, name?, frame?, spread?, x?, y?, width?, height?, pdfPage?, pdfCrop?, loadCursor?, layoutPage?, page?, rect?, autoflow?, removeStyles?, styleMap?, styleConflicts?, link?}` — text files and `.xlsx` flow into frames/tables |
| `object.layerOptions` / `object.pdfLayers` | see §7 |
| `document.epubSplit` / `file.exportEpub` | see §8 |
| `file.exportPdf` | `{path?, pages?, flatten?, spreads?, fullScreen?, bookmarksPanel?, pageLayout?, view?, advanceSeconds?, bleed?, marks?, standard?: "none"\|"x4"\|"a2b", compressImages?, tagged?, media?, title?, author?, created?}` → `{path, bytes, pages, warnings}` |
| `file.exportEpub` / `file.exportFixedEpub` | `{path?, title?, author?, language?, identifier?, coverImage?, tocTitle?, cover?, embedFonts?, split?, fixedLayout?}` / `{path?, title?, author?, language?}` |
| `file.exportPptx` / `file.exportHtml` | `{path?, pages?, lineBreaks?: keep\|reflow, rasterize?, embedFonts?, title?, author?}` / `{path?, title?, language?}` |
| `file.exportIdml` | `{path?, embedImages? (default true)}` — also `file.exportText`, `file.exportXml`, `file.printBooklet`, `file.print` |
| `object.qrCode` | `{type?: url\|text\|sms\|email\|vcard, content, …, color?, rect?, spread?}` → `{id, content}` (`crates/engine/src/cmd/qr.rs`) |
| `math.insert` / `math.svg` | `{latex, size?, x?, y?, spread?}` / `{latex, size?}` → `{svg, width, height}` (`crates/engine/src/cmd/mathexpr.rs`) |
| `color.extractTheme` → `swatch.addColorTheme` | `{id?}` → up to five colours from a placed raster / `{colors, name?}` (`crates/engine/src/cmd/color_theme.rs`) |
| `data.source.select` → `data.merge` | link CSV/TSV/xlsx, then merge into a new document (`crates/engine/src/cmd/datamerge/`) |
| `font.reload` | `{}` — re-read fonts installed, edited or removed while running (`crates/engine/src/cmd/fonts.rs`) |
| `file.package` | `{dir, idml?: true, pdf?: false, instructions?}` → `{dir, files, report}`; report names a lost placed-PDF layer choice (`crates/engine/src/cmd/package.rs`) |
| `file.close` | `{index?}` — closes **without asking** and discards recovery data; the UI's Close asks (`crates/engine/src/lib.rs:505`) |

Ground truth for params: `designcraft-cli describe <command-id>` — the `params` field is the
command's own documentation string (`crates/engine/src/cmd/mod.rs` `CommandSpec.params`); the
automation boundaries validate keys against it (`crates/engine/src/cmd/params.rs`).

## 11. Live discovery and pitfalls

- `designcraft-cli commands` lists the **542 engine commands** at this tag; it does not list the 176
  UI commands. In a running app, `engine.commands` (control) / `list_commands` (MCP connected)
  returns both, with UI entries marked `"ui": true`. `describe` works for engine commands.
- Counts are code-derived: 542 unique `cmd!` registrations across the `specs()` lists, plus 176
  `UI_COMMANDS`. Versus v0.13.0 (537 + 172): added engine `file.info`, `ink.separations`,
  `note.split`, `text.deleteSurrounding` (+1 const-built id); added UI `help.checkForUpdates`,
  `ui.dock`, `view.storyEditorDepthRuler`, `window.shortcutSets`; nothing removed. MCP stays 26;
  the control dispatch gained `ui.docking` (shared dock layout). New this release: PDF/X-1a:2003
  export through the craft-prepress flattener, Separations Preview of the exported PDF's plates,
  editable tool keys and shortcut sets in the shared Keyboard Shortcuts dialog, Story Editor depth
  ruler, and gradient table-cell fills.
- UI-only commands (`view.*`, `window.*`, `help.*`, `edit.dynamicSpelling`, `app.*` except
  `app.links`) work only in the desktop app; headless MCP errors. This includes
  `window.importShortcuts`, `view.lockGuides`, `view.goBack`/`view.goForward`,
  `app.openRecent`, the paragraph dialogs and panel docking.
- `file.close` and control `app.quit` do not ask; the UI Close/Quit and the `app.quit` command do.
  Save first when driving either from an agent.
- A `.designcraft` package's `meta.json` version above 4 is refused. Prefer open → edit → save
  through commands over hand-editing `document.json` and re-zipping.
- Placed-PDF layer choices are validated before editing: a rejection leaves the document and undo
  state untouched. Retained IDML graphic-layer options warn instead of rendering — check
  `preflight.run` for `unsupportedGraphicLayers`.
- The control channel has no authentication and only binds loopback; do not expose the port.
