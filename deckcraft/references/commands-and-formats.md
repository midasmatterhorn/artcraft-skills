# DeckCraft — commands, shortcuts, control methods, MCP tools and file formats (agent reference)

**Pin:** tag `v0.12.0`, commit `29f0f7772c47aa2bfb74fcbb0c4d3b1503300849` — the code shipped in
DeckCraft 0.12.0. **Verified:** 2026-10-29 against a read-only clone at that tag. All citations are
repo-relative (`path` or `path:symbol`). Counts were re-parsed from the registries at this tag, not
carried over. The v0.11.1→v0.12.0 delta: **326 → 328 engine commands** (+`format.languageAll`,
+`slide.selectRange`), MCP tools 25 and the control dispatch set unchanged; Reuse Slides gained a
slide chooser, proofing language can be set for the whole presentation, Preferences chooses
inches/centimetres, and the parameter-validation and media-decoder hardening wave landed.

---

## What changed at v0.11.1

Compared with the v0.10.0 skill (commit `b47195feec0f0fe4220d8943ad1c8add5dad8072`):

- **+6 engine commands, 320 → 326.** `crates/engine/src/cmd/points.rs` 7 → 11
  (`shape.deleteSegment`, `shape.segmentType`, `shape.openPath`, `shape.closePath`: Edit Points
  segment add/delete, straight/curved segment type and open/close path from the right-click menu);
  `crates/engine/src/cmd/review.rs` 22 → 23 (`review.reject`: reject one revision or all after
  Compare); `crates/engine/src/cmd/reuse.rs` 1 → 2 (`slide.reuseList`: pick which slides of the
  other deck to insert). Kind split 229/55/36 → **233 ordinary / 56 `noundo` / 37 `query`**, still
  28 command modules with unique ids.
- **RTF outlines (new format surface).** `crates/format/src/rtf.rs` writes PowerPoint's Outline/RTF
  save type (`slides_to_rtf`) and reads one back (`sniff_rtf`, `rtf_to_outline`); `rtf` joined
  `WRITABLE_EXTENSIONS` (`crates/engine/src/cmd/file.rs`), `save_bytes`, `format_for_path`,
  `file.export`, `file.open` (sniffed by content, so an `.rtf`-named or RTF-bodied file opens as an
  outline), `slide.fromOutline` payloads, the MCP `export` enum (`crates/mcp/src/tools.rs`) and
  `deckcraft-cli convert`/`run --save`.
- **Pattern fills.** A 48-tile gallery (`crates/ui-egui/src/fillui.rs::PATTERN_GALLERY`, labels in
  `PATTERN_LABELS`, 54 DrawingML names known) over tiles drawn from `crates/render/src/pattern.rs`;
  `a:pattFill` is read and written for shape and chart series fills (`crates/pptx/src/{read,write}`).
- **Slide-show type `browsed`.** `show.setup {type: speaker|browsed|kiosk}` now has a real effect:
  `browsed` runs the show in a window instead of filling the screen
  (`crates/ui-egui/src/show.rs::show_fills_screen`), and the type round-trips through PPTX
  (`crates/pptx/src/write/mod.rs`, `crates/pptx/src/read/mod.rs`).
- **EMF+-only metafiles draw.** `crates/metafile/src/emfplus.rs` plays every MS-EMFPLUS drawing
  record for a file that carries no plain EMF fallback; dual EMF+ files still draw their EMF half
  (`crates/metafile/src/emf.rs`).
- **Chart text colour:** `chart.options {textColor}` (and Font Color on a selected chart) colours
  title, axes, legend and data labels and writes `c:txPr`, with PowerPoint's 65 %-theme default when
  unset (`crates/engine/src/cmd/insert.rs`).
- **Table cell-range selection:** dragging while the caret is in a cell selects a range
  (`crates/engine/src/lib.rs:157`), and formatting applies to the selected cells.
- **AutoFormat as you type:** lists (`*`, `-`, `--`, `>`, `<>`, `1.`, `1)`, `I.`, `i.`, `A.`, `a)`,
  `a)` + space/tab) and superscript ordinals, switchable with
  `text.autocorrect {lists?, ordinals?}` (`crates/engine/src/cmd/text.rs::autocorrect`,
  `auto_list_style`).
- **Columns dialog:** `format.columns` with no `count`/`spacing` opens it; values are 1–16 columns
  and spacing in points (`crates/engine/src/cmd/format.rs`).
- **Stricter indices, including `slide.layout`.** At v0.10.0 `slide.layout` treated an invalid
  `index` as absent; it now rejects a negative or fractional index like `slide.duplicate`,
  `slide.delete`, `slide.move`, `slide.reset`, `slide.hide`, `slide.notes` and `section.add`
  (`crates/engine/src/cmd/mod.rs::opt_usize_param`).
- **Group nesting is capped at 32** (`MAX_GROUP_DEPTH`, `crates/engine/src/cmd/arrange.rs`), the
  depth PPTX import reads and the canvas draws.
- **File I/O hardening:** a read needs a regular file of at most 2 GiB; a save canonicalizes the
  target (writing through a symlink) and keeps its permissions
  (`crates/engine/src/io.rs::read_file`, `write_file`).

Counts that did **not** change: 57 engine shortcuts, 50 UI commands (15 shortcuts), 12 CLI
subcommands, 25 control methods (+2 aliases), 25 MCP tools, 49 transition rows, 107 animation
entries (24/17/23/40/3), 8 themes × 4 variants, 11 layouts + `Custom`, 183 shape presets, 28 chart
types, 45 SmartArt layouts / 9 styles / 17 colour sets, 6 starter decks, 70 Lucide icons, 40 text
warps.

## Command families

Everything DeckCraft does is a command. A command is a `CommandSpec` with id, label, ribbon/menu
place, optional shortcut, a parameter doc, an enabled check and a run function
(`crates/engine/src/cmd/mod.rs`). Ids follow PowerPoint's ribbon and menu structure.

The `cmd!` macro has three forms (`crates/engine/src/cmd/mod.rs`, `macro_rules! cmd`):

- `cmd!(id, …)` — journaled and undoable (an ordinary edit);
- `cmd!(noundo id, …)` — journaled, not undoable (navigation, save, playback, settings);
- `cmd!(query id, …)` — neither journaled nor undoable (read-only queries).

`command_specs()` concatenates the per-family `specs()` functions in this order: file, edit, slide,
reuse, insert, smartart, shape, background, picture_style, recolor, arrange, selection, merge,
points, text, format, design, ideas, transition, animation, table, find, review, inspect, media,
artistic, zoom, compress. That order breaks shortcut ties. `Session::execute` is the single dispatch
path for the UI, keyboard, CLI, control channel and MCP (`crates/engine/src/lib.rs:609`),
panic-guarded by `crates/engine/src/guard.rs`.

**Total: 328 commands** (was 326 = 233 ordinary + 56 `noundo` + 37 `query` at v0.11.1; the two new
commands are `format.languageAll` and `slide.selectRange`); all ids unique.

| Family module (under `crates/engine/src/cmd/`) | Commands | Covers |
|---|---:|---|
| file | 21 | new (theme/template/size), templates, open/adopt/openBytes, save/saveAs/saveTemplate/saveBytes, export, info, render, close, properties, AutoRecover, revert, colour at a point, next window |
| edit | 12 | undo/redo, cut/copy/paste (rich HTML), pasteSpecial, pasteText, duplicate (repeats a move), delete, select all/deselect/select |
| slide | 21 | new/duplicate/delete/move/layout/reset/hide/notes/rename, sections, `slide.fromOutline`, navigation, select slides |
| reuse | 2 | `slide.reuseList` (list the other deck's slides) + `slide.reuse` (insert them) |
| insert | 23 | text box, picture, photo album (+edit), table, chart (+type/data/options incl. `textColor`), audio, video, WordArt, slide number, date/time, symbol, hyperlink, SmartArt, icons, preset shapes, action buttons |
| smartart | 13 | Text Pane outline, add/promote/demote/remove nodes, layout, style, colours, picture, convert to shapes/text |
| shape | 27 | connect, freeform, ink to shape, sites, move/resize/rotate/flip, adjust, change, smooth corners, fill (solid/gradient/picture/pattern), line, effects (shadow/glow/reflection/soft edges/bevel/3-D), quick style, rename, alt text, visibility, lock, default, crop, picture adjust, media options, size and position |
| background | 1 | Remove Background |
| picture_style | 2 | Picture Styles gallery + apply |
| recolor | 3 | Recolor presets, Set Transparent Colour, gallery |
| arrange | 19 | order, group/ungroup/regroup (≤32 deep), align (to slide or selection), distribute, rotate, flip, nudge, guides, reorder |
| selection | 3 | Selection pane: select, Show All, Hide All |
| merge | 1 | Merge Shapes (`union` / `combine` / `fragment` / `intersect` / `subtract`) |
| points | 11 | Edit Points: enter/exit, add/delete point, move point/handle, point type, **segment type, delete segment, open/close path**, points query |
| text | 15 | text edit/insert/delete/move caret/select, AutoCorrect (+AutoFormat lists/ordinals), compose (IME), commit, set/get, fonts used, replace font |
| format | 48 | character, paragraph, bullets/numbering, tabs, **columns (1–16, dialog or values)**, direction, autofit, wrap, margins, painter, font add/rescan, WordArt transform |
| design | 24 | themes/variants/colours/fonts/effects, Browse for Themes (master + layouts), background (+Apply to All), slide size, header/footer (+date format), masters/layouts/placeholders |
| ideas | 2 | Design Ideas gallery + apply |
| transition | 6 | transition set/options/timing/sound/apply-all/list |
| animation | 11 | animation set/add/remove/move/timing/options/clear, painter, list/get |
| table | 21 | rows/columns, merge/split, distribute, widths/heights, borders, styles, cell fill/margins/align, range selection, draw/erase line |
| find | 2 | Find, Replace |
| review | 23 | comments, spelling, thesaurus, dictionary, accessibility, revisions (accept/**reject**/end), compare, slide show start/end/setup(**speaker/browsed/kiosk**)/custom show |
| inspect | 4 | `document.inspect`, `slide.inspect`, `shape.inspect`, `commands.list` |
| media | 8 | play/pause/toggle/stop, seek, info, poster frame, GIF play |
| artistic | 1 | Artistic Effects |
| zoom | 1 | Insert ▸ Zoom (linked summary/section/slide pictures) |
| compress | 1 | Compress Pictures |

Notes for agents:

- `deckcraft-cli commands [FILTER]` lists ids, labels and parameter docs; `deckcraft-cli describe
  COMMAND` prints one command's parameters and what it acts on (`apps/deckcraft-cli/src/help.rs`).
- Queries are safe in loops. `noundo` commands change the document but cannot be undone; a save
  discards the document's recovery entry (`crates/engine/src/cmd/file.rs::mark_saved`).
- UI-only actions (views, panes, dialogs, palette, Quick Access Toolbar) live in `UI_COMMANDS`
  (`crates/ui-egui/src/lib.rs:364`, 50 entries). They run through `engine.execute` in the desktop app
  and are rejected headlessly (`crates/mcp/src/headless.rs`).
- Parameter docs are the contract: `?` marks an optional key, a spaced ` | ` separates alternative
  key sets, and `→` starts the answer.

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

### UI-only shortcuts (15 of the 50 `UI_COMMANDS` entries)

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
Digits 0–9 type a slide number, Enter jumps (1-based). G See All Slides (while open only G/Escape/
Minus work). Z arms zoom. T pauses the presenter timer, R resets it. `[`/`]` change notes size.

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
| `engine.commands` | — | 328 engine commands + the 51 UI commands in the app (engine only, headless) |
| `document.inspect` | — | Slides, sections, layouts, theme, media, selection |
| `ui.inspect` | — | UI state, tool, window/canvas/slide rects, dialog, Backstage page, show state, documents, perf |
| `ui.pointer` | `{events:[{kind: down\|drag\|up\|move\|doubleclick\|tripleclick\|contextclick, x, y, mods?, pressure?}]}` | Pointer input in **slide points** through the active tool |
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
  `show.key` arm — drive a show with `ui.key`.
- `ui.set view` maps `sorter`/`outline`/`notesPage`; anything else is `Normal` (Reading View is
  `view.reading` as a UI command).
- `deckcraft-cli app [--port PORT] COMMAND [PARAMS]` or `--method METHOD [PARAMS]` sends one
  request; default port **7979** (`apps/deckcraft-cli/src/main.rs`; `crates/mcp/src/lib.rs`).
- Headless MCP accepts only `engine.execute`/`command`/`ui.menu.invoke`, `engine.commands`,
  `document.inspect`, `ui.pointer`, `ui.key`, `ui.text`, `ui.tool.select`, `ui.render`
  (`app.renderSlide`), `app.open`, `app.save`, `app.export`, and a stub `ui.inspect`; every other
  `ui.*`/`app.*` method returns “it needs the desktop app” (`crates/mcp/src/headless.rs`).

## MCP tools

`deckcraft-cli mcp` serves MCP over stdio — headless by default, or with `--connect PORT`
(`host:port` allowed); `--sample` opens the sample deck. Protocol revision **2025-06-18**, also
accepting 2025-03-26 and 2024-11-05 (`crates/mcp/src/server.rs`). Resources:
`deckcraft://document`, `deckcraft://commands`; no templates.

**25 tools** (`tool_definitions()`, `crates/mcp/src/tools.rs`). “RO” = `readOnlyHint`; “app” =
connected mode only (`APP_ONLY`).

| Tool | Mode | Maps to |
|---|---|---|
| `list_commands` | RO | `engine.commands` (+ `filter`) |
| `run_command` | | `engine.execute` |
| `batch` | | several commands; stops at the first error unless `keepGoing` |
| `new_presentation` | | `file.new` (`theme`, `blank`) |
| `open_presentation` / `save_presentation` | | `file.open` / `file.save` |
| `export` | | `file.export` (png/jpeg/pptx/deckcraft/outline/**rtf**/pdf/gif and options) |
| `inspect_document` / `inspect_slide` | RO | `document.inspect` / `slide.inspect` |
| `render_slide` | RO | `ui.render`, returned as an image block (headless scale clamps 0.05–8, default 1) |
| `add_slide` / `go_to_slide` | | `slide.new` (layout, title, body) / `slide.go` |
| `add_shape` | | `shape.insert` (+ fill/line when given) |
| `add_text_box` | | `insert.textBox` + `text.exit` + `edit.select` |
| `set_text` | | `text.set` |
| `insert_picture` | | `insert.picture` (path or base64) |
| `insert_table` / `insert_chart` | | `insert.table` / `insert.chart` |
| `select` / `pointer` | | `edit.select` / `ui.pointer` |
| `select_tool` / `key` / `type_text` | | `ui.tool.select` / `ui.key` / `ui.text` |
| `screenshot` | RO, app | `ui.screenshot` as an image block |
| `call_app` | app | any control-channel method |

- Arguments are strict: a key not in the tool's schema is refused with the expected list
  (`unknown_argument_error` in `tools.rs`). Keys inside `run_command`'s `params` belong to the
  command.
- Connected mode validates the reply envelope, caps a reply at 16 MiB and reconnects instead of
  replaying (`crates/mcp/src/backend.rs`; `docs/mcp.md`).
- File confinement: `--automation-read-root DIR` / `--automation-write-root DIR` confine every path
  a command reads and writes, links followed; a root omitted grants none of its access, `--flag=DIR`
  is accepted, a repeated flag is an error, and the roots apply to the in-process server only — they
  conflict with `--connect` (`crates/engine/src/file_access.rs`; `apps/deckcraft-cli/src/automation_args.rs`).
- The server's instructions describe the intended flow: `new_presentation → add_slide →
  add_shape`/`add_text_box`/`insert_picture`/`insert_chart` → `inspect_slide` → `render_slide` →
  `save_presentation` (`crates/mcp/src/server.rs`).
- A headless server starts with **no document** (`Headless::new`), so call `new_presentation` or
  `open_presentation` first.

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

Native load budgets: 2 GiB per entry, 4 GiB total for media + chart sidecars, 100 000 items
(`crates/format/src/lib.rs:27-31`). Every read needs a regular file of at most 2 GiB
(`crates/engine/src/io.rs::read_file`).

**Save** (`file.save {path?, format?: deckcraft|pptx}`, `file.saveAs`, `file.saveTemplate`;
`crates/engine/src/cmd/file.rs`): the format comes from `format?`, else the path's extension
(`format_for_path`). `WRITABLE_EXTENSIONS = deckcraft, pptx, potx, ppsx, pdf, png, jpg, jpeg, gif,
txt, md, rtf`. `save_bytes` understands `pptx|potx|ppsx` (correct content types for template and
show), `outline|txt`, `rtf`, `pdf`, `gif`, and falls back to the **native** format for anything else
— so a `.png`/`.jpg` path through `file.save`/`file.saveAs`/`run --save` writes native zip bytes
under the image name. Use `file.export`/`--export`/`convert` for images. `file.save` without a path
(and no stored path) returns `{"needsPath": true}` and writes nothing. A save canonicalizes the
target (writes through symlinks) and preserves the existing file's permissions
(`crates/engine/src/io.rs::write_file`).

**Export** (`file.export`):

| Format | Options (optional unless shown) | Bounds / defaults |
|---|---|---|
| `png` / `jpeg` | `slide?: index`, `all?: bool`, `scale?`, `transparentBackground?: bool` (png only) | scale default 2, clamped 0.01–16 and to the renderer's 16 000 px side; JPEG quality 92; DPI = scale × 72; `all` writes `stem1.png`, `stem2.png`… (not zero-padded); every index validated before any write |
| `pptx` / `potx` / `ppsx` / `deckcraft` | — | `.potx`/`.ppsx` get `template.main+xml` / `slideshow.main+xml` content types (`crates/pptx/src/lib.rs::export_as`) |
| `outline` / `txt` | — | plain-text outline; includes table cell text, indented so table rows stay on their slide (`crates/format/src/lib.rs::slides_to_outline`) |
| `rtf` | — | Outline/RTF: one paragraph per slide title (outline level 0) and per body paragraph, keeping bold, italic and underline (`crates/format/src/rtf.rs::slides_to_rtf`) |
| `pdf` | `layout?: slides\|notes\|handouts`, `perPage?: 1-9` (menus offer 1/2/3/4/6/9), `paper?: letter\|a4\|legal\|a3`, `orientation?`, `dpi?`, `slides?: [index]\|"1-3,5"`, `includeHidden?`, `textLayer?`, `frame?` | defaults: slides layout, 6-per-page handouts, letter portrait, dpi 200 (clamped 36–600), hidden excluded, text layer on, frame on; slide artwork is raster at the DPI, capped at 64M pixels per slide (`crates/pdf/src/lib.rs`; `crates/engine/src/cmd/file.rs::pdf_options`) |
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
  `.png`/`.jpg` (first slide only, via `file.export {slide:0}`), `.gif`.
- `run [--in FILE | --sample] [--cmd ID[=JSON]]... [--save OUT] [--export OUT [--export-params
  JSON]] [--print]` — commands in order; stops and saves nothing on the first failure; `--print`
  prints answers (not a printer flag).
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

## Desktop file hand-off (macOS)

- `CFBundleDocumentTypes` declares DeckCraft Presentation (`.deckcraft`, `LSHandlerRank Owner`) and
  PowerPoint Presentation/Template/Slide Show (`.pptx`/`.potx`/`.ppsx`, rank `Alternate`), with
  content types and MIME types (`packaging/macos/Info.plist.in`; identical in the installed bundle).
- `apps/deckcraft/src/apple_events.rs` registers `kAEOpenDocuments` and quit before the event loop,
  opens each path with `SlideApp::open_path`, and turns a quit request into a window close (so a
  dirty deck still gets the Save / Don’t Save / Cancel prompt).
- The command line uses `open_from_system`, which starts a show when the last file is `.ppsx`. The
  Apple-event path does not — see the limitations in `SKILL.md`.
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
| Save temporary | `<path>.<pid>.<n>.saving` beside the target, created exclusively, renamed over it, removed on failure | `crates/engine/src/io.rs` |

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

- App: `deckcraft [--control PORT] [--sample] [--show] [FILE...]`, plus `--help`/`--version`.
  `-psn_*` is ignored. A `.ppsx` given last on the command line starts its show
  (`apps/deckcraft/src/main.rs`). The desktop parser is hand-rolled: an unknown argument is treated
  as a file path, so a mistyped flag shows up as a failed open, not a usage error.
  `deckcraft-cli` rejects unknown options.
- CLI: `deckcraft-cli help`, per-subcommand `--help`, `--version` → `deckcraft-cli <version>`.
- Web: `apps/deckcraft-web` with `trunk build --release`; query flags `?webgl`, `?blank`, `?show`.
  No TCP control channel, no audio output, no persisted preferences; files download.
