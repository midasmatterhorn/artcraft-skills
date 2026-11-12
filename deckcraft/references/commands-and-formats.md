# DeckCraft — commands, shortcuts, control methods, MCP tools and file formats (agent reference)

**Pin:** tag `v0.18.1`, commit `7cc73ab1895ed2e30c8afbcada20c70b9ea0a440` — the code shipped in
DeckCraft 0.18.1. **Verified:** 2026-11-12 against a read-only clone at this tag; `v0.16.0`
(`a3e2254d…`) was diffed for every set. All citations are repo-relative (`path` or `path:symbol`).
Counts were re-parsed from the registries at this tag, not carried over. The v0.16.0→v0.18.1 delta
moves no id set: 329 engine commands, 57 shortcuts, 52 UI commands, 12 CLI subcommands, 25 control
methods (+2 aliases), 25 MCP tools, 49 transitions, 107 animations, 8 themes, 11 layouts + `Custom`,
183 shape presets, 28 chart types, 45/9/17 SmartArt, 6 starters, 70 icons and 40 warps are identical
at both tags (see §"Where the counts come from"). What changed is architecture and behaviour: the
`opus`, `ogg`, `isobmff` and `matroska` crates became craft-libs dependencies (workspace 24 → 20
crates), the web build gained `window.deckcraft`, `shape.adjust`/`shape.quickStyle` reject an invalid
index, `format.paragraph` validates its align name, `shape.lock` applies a group+child pair once,
PPTX keeps body/group 3-D XML and unconnected SmartArt text, over-budget charts are kept verbatim,
photo-album edit refuses to truncate, MCP batches are capped, and the UI caps live video decoders.

---

## Where the counts come from (v0.18.1)

| Surface | Count | Extracted from |
|---|---:|---|
| Engine commands | **329** (234 ordinary + 57 `noundo` + 38 `query`) | `cmd!` literals in `crates/engine/src/cmd/*.rs`; ids diffed between tags: +0/−0 |
| Engine shortcuts | **57** commands, 56 distinct strings | the shortcut argument of each `cmd!`; `Cmd+Shift+V` appears twice |
| UI-only commands | **52** (15 with shortcuts) | `UI_COMMANDS` in `crates/ui-egui/src/lib.rs` |
| CLI subcommands | **12** | `SUBCOMMANDS` in `apps/deckcraft-cli/src/help.rs` |
| Control methods | **25** + aliases `ui.menu.invoke`, `command` | top-level arms of `match req.method.as_str()` in `crates/ui-egui/src/control.rs` |
| MCP tools | **25** | `tool(` names in `crates/mcp/src/tools.rs` |
| Web page API | **6** functions | `PageApi` wiring in `apps/deckcraft-web/src/api.rs` (`request` plus `Methods::default()`) |
| Transitions | **49** rows (48 + `none`) | `TRANSITIONS` in `crates/model/src/anim.rs` |
| Animations | **107** (24 entrance, 17 emphasis, 23 exit, 40 path, 3 media) | `ANIMATIONS` in `crates/model/src/anim.rs` |
| Themes / variants | **8** / 4 each | `builtin_themes`, `theme_variants` in `crates/model/src/theme.rs` |
| Layouts | **11** + `Custom` | `LayoutType` in `crates/model/src/lib.rs` |
| Shape presets | **183** in 9 categories | `CATALOG` in `crates/geom/src/preset/catalog.rs` |
| Chart types | **28** (7 `chartEx` + `RegionMap`) | `ChartType` in `crates/model/src/chart.rs` |
| SmartArt | **45** layouts, 9 styles, 17 colour sets | `LAYOUTS`/`STYLES`/`COLORS` in `crates/engine/src/cmd/smartart.rs` |
| Starter decks | **6** | `starters()` in `crates/engine/src/templates.rs` |
| Lucide icons | **70** (1.56.0) | `ICONS` in `crates/engine/src/icon_data.rs` |
| Text warps | **40** | `CATALOG` in `crates/geom/src/warp.rs` |
| Pattern fills | **48** gallery tiles, 54 DrawingML names | `PATTERN_GALLERY`/`PATTERN_LABELS` in `crates/ui-egui/src/panels/fillui.rs` |
| 3-D presets | 28 cameras offered (62 known), 12 bevels, 12 materials, 15 light rigs | `crates/engine/src/cmd/three_d.rs` |
| Date/time field formats | **13** | `DATE_FORMATS` in `crates/engine/src/cmd/insert/text_fields.rs` |
| UI languages | **1** (English only) | no `locales/`, no i18n crate or dependency |
| Workspace crates | **20** (was 24) | `crates/` directories + `Cargo.toml` members |

## Command families

Everything DeckCraft does is a command. A command is a `CommandSpec` with id, label, ribbon/menu
place, optional shortcut, a parameter doc, an enabled check and a run function
(`crates/engine/src/cmd.rs`). Ids follow PowerPoint's ribbon and menu structure.

The `cmd!` macro has three forms (`crates/engine/src/cmd.rs`, `macro_rules! cmd`):

- `cmd!(id, …)` — journaled and undoable (an ordinary edit);
- `cmd!(noundo id, …)` — journaled, not undoable (navigation, save, playback, settings);
- `cmd!(query id, …)` — neither journaled nor undoable (read-only queries).

`command_specs()` concatenates the per-family `specs()` functions in this order: file, edit, slide,
reuse, insert, smartart, shape, background, picture_style, recolor, arrange, selection, merge,
points, text, format, design, ideas, transition, animation, table, find, review, inspect, media,
artistic, zoom, compress. That order breaks shortcut ties. `Session::execute` is the single dispatch
path for the UI, keyboard, CLI, control channel and MCP (`crates/engine/src/lib.rs`),
panic-guarded by `crates/engine/src/guard.rs`.

**Total: 329 commands** (234 ordinary + 57 `noundo` + 38 `query`); all ids unique.

| Family module (under `crates/engine/src/cmd/`) | Commands | Covers |
|---|---:|---|
| file | 21 | new (theme/template/size), templates, open/adopt/openBytes, save/saveAs/saveTemplate/saveBytes, export, info, render, close, properties, AutoRecover, revert, colour at a point, next window |
| edit | 12 | undo/redo, cut/copy/paste (rich HTML), pasteSpecial, pasteText, duplicate (repeats a move), delete, select all/deselect/select |
| slide | 22 | new/duplicate/delete/move/layout/reset/hide/notes/rename, sections, `slide.fromOutline`, navigation, select slides |
| reuse | 2 | `slide.reuseList` (list the other deck's slides) + `slide.reuse` (insert them, scaled to the destination) |
| insert | 23 | text box, picture, photo album (+edit), table, chart (+type/data/options incl. `textColor`), audio, video, WordArt, slide number, date/time, symbol, hyperlink, SmartArt, icons, preset shapes, action buttons |
| smartart | 13 | Text Pane outline, add/promote/demote/remove nodes, layout, style, colours, picture, convert to shapes/text |
| shape | 27 | connect (grouped shapes too), freeform, ink to shape, sites, move/resize/rotate/flip (not SmartArt), adjust (validated index), change, smooth corners, fill (solid/gradient/picture/pattern), line, effects (shadow/glow/reflection/soft edges/bevel/3-D), quick style (validated index), rename, alt text, visibility, lock (group+child once), default, crop, picture adjust, media options, size and position |
| background | 1 | Remove Background |
| picture_style | 2 | Picture Styles gallery + apply |
| recolor | 3 | Recolor presets, Set Transparent Colour, gallery |
| arrange | 19 | order, group/ungroup/regroup (≤32 deep), align (to slide or selection), distribute, rotate, flip, nudge, guides, reorder |
| selection | 3 | Selection pane: select, Show All, Hide All |
| merge | 1 | Merge Shapes (`union` / `combine` / `fragment` / `intersect` / `subtract`); merged shapes' animations are dropped and their triggers cleared |
| points | 11 | Edit Points: enter/exit, add/delete point, move point/handle, point type, segment type, delete segment, open/close path, points query |
| text | 15 | text edit/insert/delete/move caret/select, AutoCorrect (+AutoFormat lists/ordinals), compose (IME), commit, set/get, fonts used, replace font |
| format | 49 | character, paragraph (strict align, incl. `thaiDist`), bullets/numbering, tabs, columns (1–16), direction, autofit, wrap, margins, painter, font add/rescan, WordArt transform |
| design | 24 | themes/variants/colours/fonts/effects, Browse for Themes (master + layouts), background (+Apply to All), slide size, header/footer (+date format), masters/layouts/placeholders |
| ideas | 2 | Design Ideas gallery + apply |
| transition | 6 | transition set/options/timing/sound/apply-all/list (Preview plays from the previous slide) |
| animation | 11 | animation set/add/remove/move/timing/options/clear, painter, list/get |
| table | 21 | rows/columns, merge/split, distribute, widths/heights, borders, styles, cell fill/margins/align, range selection, draw/erase line; `cells` must be `[row, col]` pairs inside the table |
| find | 2 | Find, Replace |
| review | 23 | comments (`comment.next`/`prev` validate `index`), spelling, thesaurus, dictionary, accessibility, revisions (accept/reject/end), compare, slide show start/end/setup(`speaker/browsed/kiosk`)/custom show |
| inspect | 5 | `document.inspect`, `slide.inspect`, `slide.actions` (read-only action settings), `shape.inspect`, `commands.list` |
| media | 8 | play/pause/toggle/stop, seek, info, poster frame, GIF play |
| artistic | 1 | Artistic Effects |
| zoom | 1 | Insert ▸ Zoom (linked summary/section/slide pictures) |
| compress | 1 | Compress Pictures (a grouped picture is measured at its displayed size) |

Notes for agents:

- `deckcraft-cli commands [FILTER]` lists ids, labels and parameter docs; `deckcraft-cli describe
  COMMAND` prints one command's parameters and what it acts on (`apps/deckcraft-cli/src/help.rs`).
- Queries are safe in loops. `noundo` commands change the document but cannot be undone; a save
  discards the document's recovery entry (`crates/engine/src/cmd/file.rs::mark_saved`).
- UI-only actions (views, panes, dialogs, palette, Quick Access Toolbar) live in `UI_COMMANDS`
  (`crates/ui-egui/src/lib.rs:98`, 52 entries). They run through `engine.execute` in the desktop app
  and are rejected headlessly (`crates/mcp/src/headless.rs`).
- Parameter docs are the contract: `?` marks an optional key, a spaced ` | ` separates alternative
  key sets, and `→` starts the answer. Doc strings lag the code: `format.align` and `format.paragraph`
  accept `thaiDist`/`justifyLow` (and `format.paragraph` accepts `centre`), but their docs do not list
  all of them (`crates/engine/src/cmd/format.rs`). `format.paragraph`/`format.paragraphDialog` error on
  an unknown align; `format.align` still silently falls back to left (`crates/engine/src/cmd/format/paragraph.rs`).
- Photo albums: `insert.photoAlbum` takes at most **48 items**, **32 MiB a picture**, **64 MiB in
  all**; `insert.photoAlbumEdit` seeds within those limits and **refuses** an album too large for
  the editor rather than replacing it with a truncated copy (`crates/engine/src/cmd/insert/album.rs`).

## Verified keyboard shortcuts

Sources: the engine registry's `shortcut` field matched by `shortcut_matches`
(`crates/engine/src/keys.rs`); UI-only shortcuts in `UI_COMMANDS`; implicit keys in
`Session::key`/`text_key`; slide-show keys in `crates/ui-egui/src/show.rs`. `Cmd` matches Command on
macOS and Ctrl elsewhere; `Alt` matches Option/Alt. **57 engine commands carry a shortcut.**

### Engine registry shortcuts (57)

- **File:** `file.new` Cmd+N · `file.open` Cmd+O · `file.save` Cmd+S · `file.saveAs` Cmd+Shift+S ·
  `file.close` Cmd+W · `window.next` Cmd+` (`file.rs`)
- **Edit:** `edit.undo` Cmd+Z · `edit.redo` Cmd+Y · `edit.cut` Cmd+X · `edit.copy` Cmd+C ·
  `edit.paste` Cmd+V · `edit.pasteText` Cmd+Shift+V · `edit.duplicate` Cmd+D · `edit.delete` Delete ·
  `edit.selectAll` Cmd+A · `edit.deselect` Escape (`edit.rs`)
- **Format:** `format.bold` Cmd+B · italic Cmd+I · underline Cmd+U · `format.strikethrough`
  Cmd+Shift+X · superscript Cmd+Shift+= · subscript Cmd+= · grow Cmd+Shift+. · shrink Cmd+Shift+, ·
  `format.case` Shift+F3 · `format.clear` Cmd+Space · `format.fontDialog` Cmd+T · alignLeft Cmd+L ·
  alignCenter Cmd+E · alignRight Cmd+R · justify Cmd+J · indent Tab · outdent Shift+Tab ·
  `format.painter` Cmd+Shift+C · `format.painterApply` Cmd+Shift+V (`format.rs`)
- **Arrange:** `arrange.bringToFront` Cmd+Shift+] · bringForward Cmd+] · sendBackward Cmd+[ ·
  sendToBack Cmd+Shift+[ · group Cmd+Alt+G · ungroup Cmd+Alt+Shift+G · regroup Cmd+Alt+J (`arrange.rs`)
- **Slides:** `slide.new` Cmd+Shift+N · `slide.next` PageDown · `slide.previous` PageUp ·
  `slide.first` Home · `slide.last` End (`slide.rs`)
- **Insert/review/media/animation:** `insert.hyperlink` Cmd+K · `media.play` Alt+P · `comment.add`
  Cmd+Alt+M · `review.spelling` F7 · `show.fromStart` Cmd+Shift+Enter · `show.fromCurrent`
  Cmd+Enter · `animation.painter` Alt+Shift+C · `animation.painterApply` Alt+Shift+V · `text.edit`
  Enter · `text.delete` Backspace

**One collision:** `edit.pasteText` and `format.painterApply` both declare Cmd+Shift+V. `edit` is
registered before `format`, so the key path runs `edit.pasteText`; call `format.painterApply` by id.

### UI-only shortcuts (15 of the 52 `UI_COMMANDS` entries)

`view.gridlines` Shift+F9 · `view.guides` Alt+F9 · `view.zoomIn` Cmd+= · `view.zoomOut` Cmd+- ·
`review.thesaurusPane` Shift+F7 · `view.collapseRibbon` Cmd+F1 · `show.start` F5 ·
`app.backstage` Alt+F · `app.closePresentation` Cmd+W · `app.print` Cmd+P · `app.palette`
Cmd+Shift+P · `app.preferences` Cmd+, · `app.pasteSpecial` Cmd+Alt+V · `app.find` Cmd+F ·
`app.replace` Cmd+H.

### Implicit keys in the engine (`crates/engine/src/keys.rs`)

- **Editing text:** Enter = new paragraph, Shift+Enter = line break, Escape = `text.exit`; Tab at a
  paragraph start indents, Shift+Tab outdents; in a table Tab = next cell, Shift+Tab = previous, Tab
  in the last cell adds a row; in a table a drag or Shift+arrow selects a cell range (Delete clears
  its text). Arrows/Home/End/Backspace/Delete map to `text.move`/`text.delete`; Cmd+] / Cmd+[ grow
  and shrink the font.
- **Shape selected:** arrows nudge 6 pt (Alt 1 pt), Backspace/Delete = `edit.delete`, Enter/F2 =
  `text.edit`, Escape = `edit.deselect`, Tab cycles the selection.
- **Nothing selected:** PageDown/Down/Right = `slide.next`; PageUp/Up/Left = `slide.previous`;
  Home/End = first/last; Enter = `slide.new`; Tab cycles shapes.
- Freeform and Edit Points end on Enter/Escape; in Edit Points, dragging a point's handle with
  Shift, Ctrl/Cmd or Alt/Option sets its type (smooth, straight, corner) and Esc before the button is
  released cancels the drag with no undo step.

### Slide show keys (`crates/ui-egui/src/show.rs`, `keyboard`)

Next: Right/Down/Space/PageDown/N/Enter (Enter also commits a typed slide number). Previous:
Left/Up/Backspace/PageUp/P. Escape/Minus backs out (Escape first clears a typed number). Home/End
first/last. B or `.` black, W or `,` white, E erases ink. Cmd+L laser, Cmd+A arrow, Cmd+P pen.
Digits 0–9 type a slide number, Enter jumps (1-based). G opens See All Slides — in the presenter
window, which sends the chosen slide to the show; while it is open only G/Escape/Minus work. Z arms
zoom. T pauses the presenter timer, R resets it. `[`/`]` change notes size.

## Control channel

Start `deckcraft --control PORT` (or set `DECKCRAFT_CONTROL_PORT`). The server binds `127.0.0.1`
only and speaks JSON lines: one request object per line, one reply per line
(`apps/deckcraft/src/control_server.rs`; `crates/ui-egui/src/control.rs`). A line that is not a JSON
object with a string `method` gets one error reply and the connection closes.

Limits (`Limits::default`, `control_server.rs`): 16 concurrent connections, **256 MiB** request line
(`docs/control-protocol.md` still says 16 MiB — stale), 64 queued requests, 600 s idle, 30 s
reply-write block, 60 s UI wait. A request still queued when the wait expires is abandoned and never
run late.

**25 canonical methods plus the aliases `ui.menu.invoke` and `command`:**

| Method (aliases) | Params | What it does |
|---|---|---|
| `engine.execute` (`ui.menu.invoke`, `command`) | `{command, params}` | Run any engine or UI command |
| `engine.commands` | — | 329 engine commands + the 52 UI commands in the app (engine only, headless) |
| `document.inspect` | — | Slides, sections, layouts, theme, media, selection |
| `ui.inspect` | — | UI state, tool, window/canvas/slide rects, dialog, Backstage page, show state, documents, perf |
| `ui.pointer` | `{events:[{kind: down\|drag\|up\|move\|doubleclick\|tripleclick\|contextclick, x, y, mods?, pressure?}]}` | Pointer input in **slide points** through the active tool; one gesture keeps at most 100 000 samples (`crates/engine/src/tools/drag.rs::MAX_GESTURE_POINTS`) |
| `ui.key` / `ui.text` / `ui.ime` | `{key, shift?, alt?, cmd?}` / `{text}` / `{preedit, active?}` or `{commit}` | Keys (also drive a running show), typing, IME composition |
| `ui.tool.select` | `{tool, preset?}` | `select`, `text`/`textBox`, `shape`(+preset), a preset name, `curve`, `freeform`, `scribble`, `pen`, `highlighter`, `eraser` |
| `ui.move` / `ui.click` / `ui.drag` | screen points (`click`: `button?, count?`; `drag`: `toX, toY, steps?`) | Real egui pointer input — reaches every widget, menu and pane |
| `ui.set` | `{tab?, view?, pane?, zoom?, dark?, notes?, ribbonCollapsed?, formatTab?}` | UI state; returns the full state |
| `ui.dialog.open` / `ui.dialog.close` | `{id, fields?}` | Open/close a dialog by id, optionally pre-filling fields |
| `ui.screenshot` | `{path?}` | Whole-window PNG (base64 when no path) |
| `ui.render` | `{slide?, scale?, edit?, path?}` | Render a slide (works headlessly); base64 or a file |
| `ui.resize` / `ui.focus` | `{width, height}` / — | Window control |
| `show.start` / `show.end` | `{from?, custom?, reading?}` / — | Start (slide, custom show, or configured start) / end |
| `app.open` / `app.save` / `app.export` | `{path}` / `file.save` params / `file.export` params | File operations |
| `app.quit` | `{save?}` | Quit without asking; `{"save": true}` saves first (untitled documents still need a human in the Save dialog) |

Notes:

- The module comment in `crates/ui-egui/src/control.rs` still lists `show.key`; there is **no**
  `show.key` arm — drive a show with `ui.key`. The same comment also omits some arms; the `match` is
  authoritative.
- `ui.set view` maps `sorter`/`outline`/`notesPage`; anything else is `Normal` (Reading View is
  `view.reading` as a UI command).
- `deckcraft-cli app [--port PORT] COMMAND [PARAMS]` or `--method METHOD [PARAMS]` sends one
  request; default port **7979** (`apps/deckcraft-cli/src/main.rs`; `crates/mcp/src/lib.rs`).
- Headless MCP accepts only `engine.execute`/`command`/`ui.menu.invoke`, `engine.commands`,
  `document.inspect`, `ui.pointer`, `ui.key`, `ui.text`, `ui.tool.select`, `ui.render`
  (`app.renderSlide`), `app.open`, `app.save`, `app.export`, and a stub `ui.inspect`; every other
  `ui.*`/`app.*` method returns “it needs the desktop app” (`crates/mcp/src/headless.rs`).

## Web page API (`window.deckcraft`)

Every web build of DeckCraft installs a page object over the same command channel
(`apps/deckcraft-web/src/api.rs`; craft-libs `craft-web-api`). It is not a network port: any script
of the page's origin can call it, and a same-origin parent/opener holding the window can too.

| Function | Call | Underlying method |
|---|---|---|
| `request` | `request(method, params)` | any control method, as given |
| `execute` | `execute(command, params)` | `engine.execute {command, params}` |
| `commands` | `commands()` | `engine.commands {}` |
| `docInspect` | `docInspect(params)` | `document.inspect` |
| `uiInspect` | `uiInspect(params)` | `ui.inspect` |
| `screenshot` | `screenshot(params)` | `ui.screenshot` (adds `data: true`; an inline PNG lands in `data`) |

Each returns a Promise that resolves with the method's result or rejects with an `Error`; the call
times out after **30 s**. The shared crate refuses a 65th call waiting at once (`busy`), and a call
the page gave up on is released so the app skips it if it has not started (`apps/deckcraft-web/src/api.rs`;
`packaging/web/README.md`). Opening and saving files stay with the `?host=parent` host messages
(`deckcraft:open`, `deckcraft:save`, `deckcraft:dirty`, `deckcraft:ready`, `deckcraft:failed`) —
`window.deckcraft` drives the document, not the host.

## MCP tools

`deckcraft-cli mcp` serves MCP over stdio — headless by default, or with `--connect PORT`
(`host:port` allowed); `--sample` opens the sample deck. Protocol revision **2025-06-18**, also
accepting 2025-03-26 and 2024-11-05 (`crates/mcp/src/server.rs`). Resources:
`deckcraft://document`, `deckcraft://commands`; no templates. A request frame is capped at 16 MiB
(`crates/mcp/src/server.rs::MAX_FRAME_BYTES`), and a JSON-RPC batch at **1 000 messages / 64 MiB of
replies** (`MAX_BATCH_ITEMS`, `MAX_BATCH_BYTES`).

**25 tools** (`tool_definitions()`, `crates/mcp/src/tools.rs`). “RO” = `readOnlyHint`; “app” =
connected mode only (`APP_ONLY`).

| Tool | Mode | Maps to |
|---|---|---|
| `list_commands` | RO | `engine.commands` (+ `filter`) |
| `run_command` | | `engine.execute` |
| `batch` | | several commands; stops at the first error unless `keepGoing`; **1 000 commands / 64 MiB of results** |
| `new_presentation` | | `file.new` (`theme`, `blank`) |
| `open_presentation` / `save_presentation` | | `file.open` / `file.save` (an image path is refused) |
| `export` | | `file.export` (png/jpeg/pptx/deckcraft/outline/rtf/pdf/gif and options) |
| `inspect_document` / `inspect_slide` | RO | `document.inspect` / `slide.inspect` |
| `render_slide` | RO | `ui.render`, returned as an image block (headless scale clamps 0.05–8, default 1) |
| `add_slide` / `go_to_slide` | | `slide.new` (layout, title, body) / `slide.go` |
| `add_shape` | | `shape.insert` (+ fill/line when given) |
| `add_text_box` | | `insert.textBox` + `text.exit` + `edit.select` |
| `set_text` | | `text.set` |
| `insert_picture` | | `insert.picture` (path or base64) |
| `insert_table` / `insert_chart` | chart takes optional `x`/`y`/`w`/`h` | `insert.table` / `insert.chart` |
| `select` / `pointer` | | `edit.select` / `ui.pointer` |
| `select_tool` / `key` / `type_text` | | `ui.tool.select` / `ui.key` / `ui.text` |
| `screenshot` | RO, app | `ui.screenshot` as an image block |
| `call_app` | app | any control-channel method |

- Arguments are strict: a key not in the tool's schema is refused with the expected list
  (`unknown_argument_error` in `tools.rs`). Keys inside `run_command`'s `params` belong to the
  command.
- Connected mode validates the reply envelope, caps a reply at 16 MiB and reconnects instead of
  replaying (`crates/mcp/src/backend.rs`; `docs/mcp.md`).
- File confinement: `--automation-read-root DIR` / `--automation-write-root DIR` confine every path a
  command reads and writes, links followed; a root omitted grants none of its access, `--flag=DIR` is
  accepted, **both flags may be repeated to grant more folders**, and the roots apply to the
  in-process server only — they conflict with `--connect` (`crates/engine/src/file_access.rs`;
  `apps/deckcraft-cli/src/automation_args.rs`). A save's temporary sibling must also be inside the
  write root (`crates/engine/src/io.rs`).
- The server's instructions describe the intended flow: `new_presentation → add_slide →
  add_shape`/`add_text_box`/`insert_picture`/`insert_chart` → `inspect_slide` → `render_slide` →
  `save_presentation` (`crates/mcp/src/server.rs`).
- A headless server starts with **no document** (`Headless::new`), so call `new_presentation` or
  `open_presentation` first.
- `batch` gathers every reply before returning; on a deck with large notes, many `inspect_slide`
  calls can pass 64 MiB, after which the remaining entries are refused and the tool returns an error
  (`crates/mcp/src/tools.rs`).

## Save/open/export formats

**Open / read** (`crates/engine/src/cmd/file.rs::open_other`):

| Input | Recognised by | Notes |
|---|---|---|
| `.deckcraft` | zip whose stored `mimetype` is `application/vnd.storyteller.deckcraft+zip` (`crates/format/src/lib.rs`) | Native; legacy `.slidecraft` still read; unknown fields ignored; `chart-parts/<index>` hold retained chart payloads |
| `.pptx` / `.potx` / `.ppsx` | OOXML zip (`crates/pptx/src/lib.rs::sniff`) | Read via `pptx::import_checked`, then repaired; unreadable slides reported as `lostSlides`; media lengths/sizes filled from headers |
| password-protected OOXML | `cfb::is_encrypted` | Refused with a clear message |
| `.txt` / `.md` | by extension | Outline import; Markdown headings become slides (`crates/format/src/lib.rs`) |
| `.rtf` (or any RTF body) | `deckcraft_format::rtf::sniff_rtf` | Outline import through `rtf_to_outline` (`crates/format/src/rtf.rs`) |
| `.thmx` (theme), also `.pptx`/`.potx` | `design.browseTheme {path}` or `{name, data}` (`crates/engine/src/cmd/design.rs`) | Applies the theme; a `.pptx`/`.potx` also brings its master and layouts (`crates/pptx/src/lib.rs::import_theme`) |

Native load budgets: **256 MiB for `presentation.json`**, 2 GiB per entry, 4 GiB total for media +
chart sidecars, 100 000 items (`crates/format/src/lib.rs:27-34`), and the notes page size is clamped
to the slide-size bounds. Every read needs a regular file of at most 2 GiB
(`crates/engine/src/io.rs::read_file`).

PPTX import budgets that show up as behaviour: **1 000 000 points per chart**, **4 000 000 points
and 256 MiB of chart decode per presentation**. A chart past those is kept as its original part
(`Chart.verbatim`), shown empty, and written back whole (`crates/pptx/src/read/chart.rs`,
`crates/pptx/src/write/chart.rs`).

**Save** (`file.save {path?, format?: deckcraft|pptx}`, `file.saveAs`, `file.saveTemplate`;
`crates/engine/src/cmd/file.rs`): the format comes from `format?`, else the path's extension
(`format_for_path`). `WRITABLE_EXTENSIONS = deckcraft, pptx, potx, ppsx, pdf, png, jpg, jpeg, gif,
txt, md, rtf`. `save_bytes` understands `pptx|potx|ppsx` (correct content types for template and
show), `outline|txt`, `rtf`, `pdf`, `gif`, **refuses `png`/`jpeg`/`jpg`** ("saving a presentation as a
single image isn't supported; use file.export"), and falls back to the **native** format for anything
else — so `file.save {path: "x.odp"}` still writes native zip bytes under that name. Use
`file.export`/`--export`/`convert` for images. `file.save` without a path (and no stored path)
returns `{"needsPath": true}` and writes nothing. A save canonicalizes the target (writes through
symlinks), preserves the existing file's permissions, and uses a hidden
`.deckcraft.<pid>.<n>.saving` sibling created exclusively in the target's directory, renamed over it
and removed on failure (`crates/engine/src/io.rs::write_file`).

**Export** (`file.export`):

| Format | Options (optional unless shown) | Bounds / defaults |
|---|---|---|
| `png` / `jpeg` | `slide?: index`, `all?: bool`, `scale?`, `transparentBackground?: bool` (png only) | scale default 2, clamped 0.01–16 and to the renderer's 16 000 px side; JPEG quality 92; DPI = scale × 72; `all` writes `stem1.png`, `stem2.png`… (not zero-padded); every index validated before any write |
| `pptx` / `potx` / `ppsx` / `deckcraft` | — | `.potx`/`.ppsx` get `template.main+xml` / `slideshow.main+xml` content types (`crates/pptx/src/lib.rs::export_as`) |
| `outline` / `txt` | — | plain-text outline; includes table cell text, indented so table rows stay on their slide; footer, date and slide-number placeholders are left out (`crates/format/src/lib.rs::slides_to_outline`) |
| `rtf` | — | Outline/RTF: one paragraph per slide title (outline level 0) and per body paragraph, keeping bold, italic and underline; footer/date/slide-number placeholders skipped (`crates/format/src/rtf.rs::slides_to_rtf`) |
| `pdf` | `layout?: slides\|notes\|handouts`, `perPage?: 1\|2\|3\|4\|6\|9` (anything else is an error), `paper?: letter\|a4\|legal\|a3`, `orientation?`, `dpi?`, `slides?: [index]\|"1-3,5"`, `includeHidden?`, `textLayer?`, `frame?` | defaults: slides layout, 6-per-page handouts, letter portrait, dpi 200 (clamped 36–600), hidden excluded, text layer on, frame on; slide artwork is raster at the DPI, capped at 64M pixels per slide; the text layer uses evaluated field values (`crates/pdf/src/lib.rs`; `crates/engine/src/cmd/file.rs::pdf_options`) |
| `gif` | `width?: px 16-3840 \| small\|medium\|large\|extraLarge`, `secondsPerSlide?: 0.1-600`, `loop?`, `slides?`, `includeHidden?` | width default medium 960 (presets 640/960/1280/1920), 5 s per slide, loop forever; one frame per slide, per-frame 256-colour palette; ≤500 frames, ≤3840 px side, ≤200M total pixels (`crates/engine/src/gif_export.rs`) |

An unknown extension with no `format` is treated as `deckcraft` by `file.export` (native bytes under
that name); the CLI refuses unknown extensions for `convert`, `run --save` and `run --export` up
front (`apps/deckcraft-cli/src/main.rs::output_format`).

Read-back queries: `file.info`, `file.render {slide?, scale?, edit?, transparentBackground?} →
{png: base64, width, height}`, `file.saveBytes {format?: deckcraft|pptx} → {data: base64}`.

## CLI at a glance

`deckcraft-cli` subcommands (`apps/deckcraft-cli/src/help.rs`): `info`, `render`,
`render-transition`, `convert`, `run`, `commands`, `describe`, `app`, `mcp`, `bench`, `links`,
`version`.

- `info FILE` prints `document.inspect` JSON.
- `render (FILE | --sample) [--slide N | --all] [--scale S] [--edit] [--transparent] OUT` — PNG per
  slide; `--all` writes `slide-01.png…`; `--slide` 0-based; default scale 2.
- `render-transition FILE --slide N --t T[,T...] [--width PX] OUT.png`.
- `convert IN OUT` — `.deckcraft`, `.pptx` (and `.potx`/`.ppsx`), `.pdf`, `.txt`/`.md`/`.rtf`,
  `.png`/`.jpg` (first slide only, via `file.export {slide:0}`), `.gif`; other extensions are refused.
- `run [--in FILE | --sample] [--cmd ID[=JSON] | --cmd-file FILE]... [--save OUT] [--export OUT
  [--export-params JSON]] [--print]` — commands in order; stops and saves nothing on the first
  failure; `--print` prints answers (not a printer flag). `--cmd-file` reads one command a line from
  a UTF-8 file (blank lines and full-line `#` comments skipped, CRLF and a BOM accepted, 16 MiB a
  line) and may repeat and mix with `--cmd` in order.
- `app`, `mcp`, `bench [--runs N] [--json]`, `links`, `--version`.
- The CLI is a **separate signed/notarized zip**, not inside the `.app`
  (`packaging/macos/package.sh`); this machine has no `deckcraft-cli` on `PATH`.

## Slide show setup

`show.setup {type?: speaker|browsed|kiosk, loop?, noNarration?, noAnimation?, useTimings?,
showMediaControls?, from?, to?, custom?: name}` (`crates/engine/src/cmd/review.rs`).

- `speaker` fills the screen (the presenter window is a second viewport).
- `browsed` runs the show **in a window** (`crates/ui-egui/src/show.rs::show_fills_screen`); it
  round-trips to and from PPTX `p:showPr`.
- `kiosk` fills the screen and loops until Esc (`crates/anim/src/show.rs`).
- `showMediaControls` round-trips through `p14:showMediaCtrls` (`crates/pptx/src/write.rs`,
  `crates/pptx/src/read.rs`); the rest of the media playback options (#74) are still not written.

## Desktop file hand-off (macOS)

- `CFBundleDocumentTypes` declares DeckCraft Presentation (`.deckcraft`, `LSHandlerRank Owner`) and
  PowerPoint Presentation/Template/Slide Show (`.pptx`/`.potx`/`.ppsx`, rank `Alternate`), with
  content types and MIME types (`packaging/macos/Info.plist.in`; identical in the installed bundle).
- `apps/deckcraft/src/apple_events.rs` registers `kAEOpenDocuments` and quit before the event loop,
  opens each path with `SlideApp::open_path`, and turns a quit request into a window close (so a
  dirty deck still gets the Save / Don’t Save / Cancel prompt).
- The command line uses `open_from_system`, which starts a show when the last file is `.ppsx`
  (`crates/ui-egui/src/app/files.rs`). The Apple-event path does not — see the limitations in
  `SKILL.md`.
- Windows installer (`packaging/windows/deckcraft.wxs`) and Linux desktop file
  (`packaging/linux/ai.storyteller.deckcraft.desktop`) declare the same four extensions.

## Paths

Per-user runtime paths, not repo paths.

| What | Location | Source |
|---|---|---|
| Settings (`ui.json`, `prefs.json`, `logs/`) | macOS `~/Library/Application Support/DeckCraft`; Windows `%APPDATA%\DeckCraft`; Linux `$XDG_CONFIG_HOME/deckcraft` or `~/.config/deckcraft` | `apps/deckcraft/src/main.rs::config_dir` |
| Logs | `<settings>/logs/deckcraft.log`, rotated to `deckcraft.1.log`/`deckcraft.2.log`, capped at 16 MiB | `apps/deckcraft/src/logging.rs` |
| Recovery | macOS `…/DeckCraft/Recovery`; Windows `%APPDATA%\DeckCraft\Recovery`; Linux `$XDG_DATA_HOME/deckcraft/recovery` (or `~/.local/share/deckcraft/recovery`); `<uid>.deckcraft` + `<uid>.json`, `owner-<instance>.lock` | `crates/engine/src/recovery.rs` |
| Dictionaries | `DECKCRAFT_DICTIONARIES` first; macOS `~/Library/Application Support/DeckCraft/Dictionaries`, `~/Library/Spelling`, `/Library/Spelling`; Linux XDG + hunspell/myspell dirs | `crates/engine/src/spell.rs` |
| Save temporary | `.deckcraft.<pid>.<n>.saving` in the target's directory, created exclusively, renamed over the target, removed on failure; must pass the automation write-root check | `crates/engine/src/io.rs` |

Environment variables:

| Variable | Effect |
|---|---|
| `DECKCRAFT_CONTROL_PORT` | default port when `--control` is not given |
| `DECKCRAFT_NO_PREFS` | don’t load or save `ui.json`/`prefs.json` |
| `DECKCRAFT_NO_AUDIO` | play media silently |
| `DECKCRAFT_NO_RECOVERY` | skip AutoRecover and the recovery prompt |
| `DECKCRAFT_DICTIONARIES` | extra dictionary folders (OS path list) |
| `RUST_LOG` | log filter (default `info` for DeckCraft crates, `warn` otherwise) |
| `DECKCRAFT_WAYLAND`, `DISPLAY`, `WAYLAND_DISPLAY` | Linux display backend selection |
| `CRAFT_FONTS_DIR` | build-time checkout of `storytold/craft-fonts` |
| `DECKCRAFT_BUILD_SHA`, `DECKCRAFT_BUILD_DATE` | set by the release workflow; shown in About |
| `WGPU_BACKEND`, `WGPU_DX12_COMPILER` | Windows troubleshooting only (README.md §Downloads) |

## Launch surfaces

- App: `deckcraft [--control PORT] [--sample] [--show] [FILE...]`, plus `--help`/`-h` and
  `--version`/`-V` (both exit before the window and the log file). `-psn_*` is ignored. A `.ppsx`
  given last on the command line starts its show (`apps/deckcraft/src/main.rs`). The desktop parser
  is hand-rolled: an unknown argument is treated as a file path, so a mistyped flag shows up as a
  failed open, not a usage error. `deckcraft-cli` rejects unknown options.
- CLI: `deckcraft-cli help`, per-subcommand `--help`, `--version` → `deckcraft-cli <version>`.
- Web: `apps/deckcraft-web` with `trunk build --release`; query flags `?webgl`, `?blank`, `?show`,
  and `?host=parent` (+ `&author=`) for a same-origin framing page that sends files and stores saves
  (`apps/deckcraft-web/src/host.rs`). Every build also installs `window.deckcraft`
  (`apps/deckcraft-web/src/api.rs`). Otherwise: no TCP control channel, no audio output, no
  persisted preferences; files download.
