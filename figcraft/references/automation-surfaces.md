# FigCraft automation surfaces — operational detail

Load this when a job is bigger than a couple of command calls. Re-checked at tag **v0.18.1**
(commit `4acc293c2ec941ac1400837ee7e3ab51780399f8`, 2026-11-12): the CLI, MCP, control-channel and
locale shapes are the same as at v0.16.0 except where noted (CLI clap-parsed with `connect publish`,
**19** MCP tools, **3 resources + 2 templates + 4 prompts**, **17** app control methods, **25**
locales, plugin API **6**; the command registry grew by nine ids). Repo-relative paths only; no
machine paths are named.

## 1. Three ways in, one command registry

Every user-visible behaviour is a command in `crates/engine/src/cmd/*` (plus the area modules) with
an id, label, parameter docs and an undo flag (`spec!` macro in `crates/engine/src/cmd.rs`). The
menus, shortcuts, Actions palette, CLI, control channel, MCP server and WASM plugins all dispatch
the same ids (`docs/architecture.md` › Commands). This tag registers **646 `spec!` sites** (v0.16.0:
637; some ids are const-built — count your build with `figcraft-cli commands --json`), of which
**641 have distinct literal ids**. The generated parity checklist lags: it says **212 / 212** menu
items but was generated 2026-10-21; `catalog::MENU` minus `OWN` and `collab.*` now counts **214**
(the three `Text ▸ Text direction` rows are new; `text.directionAuto` is in `OWN`).

Largest namespaces (carried from the previous audit; the live registry is authoritative): `text`
57+, `view` 48, `vector` 42, `tool` 29, `object` 28, `file` 22, `component` 21, `proto` 21,
`selection` 21, `library` 18, `variable` 18, `edit` 16, `comment` 14, `pref` 13, `plugin` 11,
`style` 10, `arrange` 10, `collab` 22, `board` 23, `transform` 9, `annotation`/`instance`/`version`/
`page` 8 each, `branch` 7, `align`/`stroke`/`shape` 6 each. New at this tag: `text.direction*`
(4 ids), `board.mindMap`, `board.mindMapAdd`, `selection.createColorStyle`, `tool.crosshair`,
`collab.reconnect`.

The Dev Mode code generators live in `crates/engine/src/dev/` (`crates/engine/src/dev/codegen.rs`,
`crates/engine/src/dev/codegen/{arkui,compose,css,html,swift}.rs`,
`crates/engine/src/dev/{tailwind,component_codegen}.rs`).

Discovery, in order of usefulness to an agent:

```sh
figcraft-cli commands --filter component      # id, label, params, shortcut, * = undoable
figcraft-cli commands --json --filter style   # {id, label, params, menu, shortcut, undoable}
figcraft-cli commands --json | wc -l          # the live count of your build
```

MCP equivalents: `list_commands {filter}` and the resource `figcraft://command/<id>`.

## 2. `figcraft-cli`

Build: `cargo build --release -p figcraft-cli` → `target/release/figcraft-cli`.
Not inside the macOS `.app` (only the Linux AppImage bundles it as `FigCraft.AppImage cli …`); macOS
releases ship a separate `figcraft-cli-<version>-macos-<arch>.zip` (`packaging/macos/package.sh`).

Ten subcommands plus `help` / `--help` / `-h` and `--version` / `-V` / `version`
(`apps/figcraft-cli/src/main.rs`):

| Subcommand | Notes |
|---|---|
| `info <file> [--json]` | Pages, node counts, top-level frames, styles/variables/images. Repairs and import warnings go to stderr as `note:` lines (`notes` in JSON; control characters escaped). `missingFonts: [{family, layers}]` for fonts the file names that aren't installed. |
| `export <file> -o <out> [--format png\|jpg\|svg\|webp\|pdf\|fig\|penpot] [--scale N] [--page NAME] [--node ID\|NAME] [--bleed LENGTH] [--crop-marks] [--bleed-marks] [--cmyk]` | `-o` directory → one file per top-level frame; `-o` with an image extension → one file for `--node` or the whole page. `--node` takes an id (`12` or `0:12`) or a layer name. Format = `--format`, else the extension, else png. `--scale` default 1, max 64. `--bleed` takes points or `3mm`/`0.125in`, up to 2 in. A visible tree deeper than 256 descendant levels fails SVG/PDF without touching an existing destination. **No `--color-profile`/`--quality` flag**: use `run` with `file.export` or MCP `export`. |
| `convert <in> <out>` | Format by extension, both ways. In: `.figcraft`, `.penpot`, `.json` (FigCraft or REST API), `.fig`, `.jam` (content-sniffed; not in the CLI help), `.sketch`, `.svg`, `.png/.jpg/.jpeg/.webp/.gif/.tif/.tiff/.bmp`. Out: `.figcraft`, `.json` (FigCraft JSON), `.svg`, `.png/.jpg/.webp`, `.pdf`, `.fig`, `.penpot`. |
| `render <file> -o <out> [--scale N] [--page NAME]` | Whole page with its background, as png, jpg or webp; large pages scale down to fit 16384 px. |
| `run <script.json\|script.jsonl> [--in <file>] [--out <file>]` | Headless command script; one JSON result line per step; **all-or-nothing, one undo step**. No network: it cannot host or join live sessions. |
| `commands [--json] [--filter TEXT]` | The command catalog. |
| `mcp [--attach PORT] [--timeout SECONDS] [--automation-read-root DIR]… [--automation-write-root DIR]…` | MCP on stdio, headless or attached. `--timeout` is 1–600 s and sets the attach wait. The headless session can host, join and publish live sessions (`collab.*`) and use plugin directories. |
| `connect publish <file> …` | Publishes a code repository's component mappings (code connect) to a design file. |
| `plugin publish <folder> --server ws://host:port/[?key=KEY]` | Publishes a plugin folder to a `figcraft-server` directory; the key comes from the address or `FIGCRAFT_SERVER_KEY` (never printed). Prints name, version, size and SHA-256. |
| `perf [--layers N[,N…]] [--instances N[,N…]]` | Synthetic benchmark tables. Layer sizes clamp to 10–2,000,000; instance workloads default 2000 and cap at 100,000. |

Flags, exhaustively: `--json` (info, commands), `--format`/`--scale`/`--page`/`--node`/`-o`/`--out`/
`--bleed`/`--crop-marks`/`--bleed-marks`/`--cmyk` (export), `-o`/`--out`/`--scale`/`--page` (render),
`--in`/`--out` (run), `--filter` (commands), `--attach`/`--timeout` (mcp), `--server` (plugin
publish), `--layers`/`--instances` (perf), the two automation roots (info/export/convert/render/run/
mcp), `--no-system-fonts` everywhere, and global `--help`/`-h` and `--version`/`-V`.

Every subcommand accepts `--no-system-fonts` (or `FIGCRAFT_NO_SYSTEM_FONTS=1`) for machine-identical
text layout, e.g. in CI. Exit code 2 = bad arguments (usage printed), 1 = failure, 0 = success.
`--help` / `-h` may appear anywhere among a subcommand's options and exits 0, even after a bad option
(`apps/figcraft-cli/src/args.rs`).

`info`, `export`, `convert`, `render`, `run` and `mcp` also take `--automation-read-root DIR` /
`--automation-write-root DIR` (each repeatable; the folders must exist) and confine every file that
subcommand touches — a run given only a read root cannot write at all (`docs/cli.md` › Confining a
run).

Script shapes accepted by `run`: a JSON array of `{"command": id, "params": {…}}`, an object
`{"commands": […]}` (as `command.batch` takes), or JSON lines (blank lines and `//` comments
skipped). Ids are assigned in order — a new document's first page is id 1, so the first created
layer is 2 — and `{"$step": n}` (zero-based) resolves to the `id` from step *n*'s result, with
`{"$step": n, "field": "…"}` for another field. Steps can be named with `as` and referenced with
`$ref`, and `field` accepts paths; batch errors name the failing step. A script can start from a
starter template: `file.newFromTemplate {template}` as its first step makes the template the
document the rest of the script (and `--out`) acts on. A failing step prints
`{"step":i,"command":…,"ok":false,"error":…,"rolledBack":true}` and exits 1; earlier steps are taken
back and `--out` is not written. `command.batch` takes `onError: "abort"|"continue"` (default abort);
`continue` rolls back only the failed steps and returns one outcome per step.

## 3. Control channel (`figcraft --control PORT`)

Loopback only (`127.0.0.1`), newline-delimited JSON, one reply per request, in order. The port can
also come from `FIGCRAFT_CONTROL_PORT`. Implementation: `crates/ui-egui/src/control.rs` (methods),
`apps/figcraft/src/control_server.rs` (socket: `MAX_LINE` 32 MiB, `MAX_CONNECTIONS` 8,
`MAX_QUEUED_REQUESTS` 8, 60 s default `TIMEOUT`); documented in `docs/control-protocol.md`.
**17 methods** in the app; the docs list 18 because they include `events.poll`, which only the MCP
bridge implements.

Limits that matter to a client:
- request line ≤ 32 MiB before the newline; a line that is not JSON ends the connection;
- at most 8 active connections, 8 queued requests per queue; a full queue answers
  `control request queue is full`;
- the default wait is 60 s; a request may set `timeoutMs` beside `id`/`method` (whole milliseconds,
  up to 600 000). A timed-out request says whether it was dropped unrun or is still running;
- methods that need a **drawn** frame (`ui.screenshot`, `ui.input`, `window.new`) fail at once when
  the window is minimised or hidden, while every state method (`engine.execute`, `document.inspect`,
  `node.get`, `ui.inspect`, `ui.pointer`, `ui.key`, `ui.type`, `ui.set`, `ui.render`, `window.list`)
  keeps working. Under Wayland a minimised window is detected after ~0.2 s without a frame, so state
  requests take about half a second there. `NEEDS_FRAME` in `crates/ui-egui/src/control.rs` is the list.

Coordinates are page units, y down. `x`/`y` in `node.create`/`node.set` are relative to the parent
frame (groups have no coordinate space of their own). Every method takes an optional `window` id
(0 = main; `window.list` enumerates).

| Method | Params / result |
|---|---|
| `engine.execute` | `{command, params?}` → the command's result. Same ids as menus/CLI/MCP. |
| `engine.commands` | `{}` → the command catalog. |
| `document.inspect` | `{depth? (default 8, capped at 64), allPages?, fields?, outline?}` → document JSON. |
| `node.get` | `{id, depth?, fields?, outline?}` → one layer, including `pluginData` and Developer Mode fields when present. |
| `ui.inspect` | `{}` → panels, tool, canvas work/latency, presenter/preview, import report, focus region, `uiScale`, windows, annotations/codeLinks/measurements. |
| `ui.pointer` | `{kind, x, y, to?, steps?, shift?, alt?, cmd?, ctrl?, pressure?, pressureTo?}` — mouse/pen gesture with the current tool. |
| `ui.key` | `{key, shift?, alt?, cmd?, ctrl?}` — a key or shortcut as if typed on the canvas. |
| `ui.type` | `{text}` — type into the text editor. |
| `ui.input` | `{events}` — raw window events: move/down/up/key/text/scroll/leave, `{hold:{alt?,shift?,cmd?}}`, `{gamepad:…}`. Needs a drawn frame. |
| `ui.menu.invoke` | `{id}` — invoke a menu item by command id. |
| `ui.set` | Panel/mode switches: right/left tabs, theme, home section/search/recents, Actions palette, main menu, variables editor, layer filter, style picker, prototype editor, context menu, comment panel, Developer Mode compare (`devCompareVersion`), plugins window, icon gallery, export preview, colour-profile dialog, and more. Returns the new `ui.inspect`. |
| `ui.screenshot` | `{path?}` → PNG of the whole window with UI chrome; without `path`, base64 `{format:"png",width,height,data}`. Needs a visible window. |
| `ui.render` | `{path?, scale?, ids?}` → PNG of the document without UI chrome; works without a visible window. |
| `window.new` | `{path?, index?}` → `{window}`; moves an open file or opens a path/new file. Browser/screen-reader builds keep one window. |
| `window.list` | `{}` → every window with tabs, active file and focus. |
| `window.focus` | `{id}` → bring a window forward; later requests go there. |
| `app.quit` | `{}` — close the app without asking about unsaved changes. |

```
{"id":1,"method":"engine.execute","params":{"command":"shape.rectangle","params":{"x":10,"y":10,"width":100,"height":50}}}
{"id":1,"ok":true,"result":{"id":2}}
{"id":2,"method":"engine.execute","params":{"command":"node.set","params":{"ids":[2],"props":{"fill":"#FF6B6B","cornerRadius":8}}}}
{"id":3,"method":"ui.screenshot","params":{"path":"shot.png"}}
{"id":4,"method":"document.inspect","params":{"depth":4}}
```

Without a `path`, `ui.screenshot` / `ui.render` return the PNG as base64, so an attached agent writes
no temporary files.

**In the browser.** `window.figcraft` installs the shared `craft-web-api` functions — `request`,
`execute`, `commands`, `docInspect`, `uiInspect`, `screenshot` — plus FigCraft's `inspect` (the old
name for `document.inspect`), `openFile(name, bytes)`, `captureDownloads(on)`, `files()` and
`readFile(name)`. Replies settle promises; a call the app does not answer within 30 s rejects and is
cancelled if it had not started (`apps/figcraft-web/src/api.rs`, `docs/control-protocol.md`).

## 4. MCP server

Speaks newline-delimited JSON-RPC 2.0 over stdio (protocol `2025-06-18`; `2025-03-26` and
`2024-11-05` accepted). Incoming lines are capped at 32 MiB before the newline. **19 tools**, three
resources plus two resource templates, four prompts (`crates/mcp/src/tools.rs` `TOOL_NAMES`,
`crates/mcp/src/{resources,prompts,server}.rs`; `docs/mcp.md`).

Client config (MCP clients usually need an absolute path; substitute your own):

```json
{"mcpServers": {"figcraft": {"command": "<path to figcraft-cli>", "args": ["mcp"]},
                "figcraft-app": {"command": "<path to figcraft-cli>", "args": ["mcp", "--attach", "7979"]}}}
```

Headless = an in-process session with one untitled document, CPU renders, no window. Attached =
drives the running app, so the user sees the work.

| Tool | What it does |
|---|---|
| `list_commands {filter?}` | Every command: id, label, menu, shortcut, undoable, params doc. |
| `run_command {command, params}` | Run any command. One undo step for a mutating command; a failure leaves the document unchanged. Programmatic calls never open dialogs. |
| `batch {commands:[{command,params,as?}], label?, onError?}` | Several commands as one undo step (`command.batch`), all-or-nothing by default; `onError: "continue"` rolls back only failed steps and returns per-step outcomes. `{"$step": n}` references an earlier step's `id`. Preferences, clipboard, tool state and UI requests are not rolled back. |
| `create_node {type, x?, y?, width?, height?, parent?, index?, name?, text?, path?, props?}` | Create a frame, rectangle, ellipse, polygon, star, line, arrow, text, vector, section, component or slice; returns `{id, node}`. |
| `set_properties {ids?, props}` | `node.set` on layers: geometry, fills, strokes, effects, radius, auto layout, sizing, constraints, masks, `devStatus`, `textDirection`, text, `pluginData`, etc. Returns the updated layers; auto layout keys given to non-frames are skipped and named in `warnings`. Measurements are made with `devMode.addMeasurement`, not here. |
| `inspect_document {depth?, allPages?, fields?, outline?, maxBytes?}` | The document as JSON: layer tree, styles, variables, selection, undo history. `maxBytes` caps the whole JSON-RPC message (default 8 MiB); a large tree is reported shallower with a `truncated` object. |
| `get_node {id, depth?, offset?, fields?, outline?, maxBytes?}` | One layer as JSON; `pluginData` when written with `set_properties`; `offset` reads children that didn't fit, `truncated` says so. |
| `select {ids}` | Replace the selection (`[]` deselects). |
| `export {ids?, format?, scale?\|size?, path?, bleed?, cropMarks?, bleedMarks?, cmyk?, contentsOnly?, includeBoundingBox?, svgOutlineText?, svgIdAttribute?, svgSimplifyStroke?, vdCompat?, colorProfile?, quality?}` | png/jpg/svg/webp/pdf/xml, or `fig` (whole file, experimental). `colorProfile` is `sameAsFile` (default) / `srgb` / `displayP3` for png/jpg/webp; `quality` is JPG 1–100 (default 90); SVG/PDF/XML are always sRGB. Penpot export is `file.export {format: "penpot"}`, not an MCP export format. Without `path`, images come back as image content, SVG/XML as text, others as base64. |
| `screenshot {ids?, scale?, maxSize?, window?}` | PNG of the page/layers scaled to fit `maxSize` (default 1600). `window: true` captures the attached app window; headless renders the document. |
| `open_file {path, variables?}` | Open `.figcraft`, `.penpot`, `.json` (FigCraft/REST), `.fig`/`.jam` (best effort), `.sketch`, `.svg` or an image. Returns `summary`, `warnings` or `repairs`. |
| `save_file {path?}` | Save as `.figcraft`; `path` required first time. A `.fig` path writes an experimental export copy and leaves the native path/unsaved state alone. |
| `undo` | Undo the last change (one command, batch or gesture). |
| `redo` | Redo the last undone change. |
| `pointer {kind, x, y, to?, steps?, tool?, shift?, alt?, cmd?, pressure?, pressureTo?}` | Mouse/pen gesture in page coordinates: click, double, drag, down, move, up, hover. |
| `key {key, shift?, alt?, cmd?}` | A shortcut or key as if typed on the canvas; while editing text, editing keys go to the editor. |
| `type_text {text, id?}` | Type into the text being edited, or replace text layer `id`'s contents. |
| `inspect_ui {}` | Tool, view, status, panels, timings and the app's windows when attached. |
| `wait_for_changes {after?, timeoutMs?, topics?, limit?}` | Wait for new comment events in the attached app; returns pending events at once, else waits up to `timeoutMs` (default 20 s, max 25 s). Headless returns immediately. |

Resources: `figcraft://document`, `figcraft://commands`, `figcraft://comments`,
`figcraft://node/{id}`, `figcraft://command/{id}`. Prompts: `mobile_screen`, `design_system`,
`landing_page`, `prototype_flow` — each returns a step-by-step plan naming tools and verification.

Semantics an agent must respect:
- one mutation = one undo step; `batch` makes several steps one, **all-or-nothing** unless
  `onError: "continue"`;
- programmatic calls never open dialogs (they are dropped);
- attached calls are never auto-replayed after a transport failure — the error says the operation
  may already have completed, so inspect before retrying; an idle-closed connection is replaced on
  the next call;
- `screenshot {window: true}` needs a visible window; `screenshot` without `window` renders the
  document instead;
- responses are bounded: the whole JSON-RPC message may not exceed `maxBytes` (default 8 MiB,
  `MAX_RESPONSE`), 1 KiB is reserved for the `truncated` marker and ~1 KiB for the envelope;
- headless text uses built-in plus system fonts (`--no-system-fonts` /
  `FIGCRAFT_NO_SYSTEM_FONTS=1` pins the built-ins for CI); attached, the app's fonts apply.

## 5. File-access confinement

```sh
figcraft-cli mcp --automation-read-root WORK/project --automation-write-root WORK/project/out
figcraft --control 7979 --automation-read-root WORK/project --automation-write-root WORK/project/out
figcraft-cli render in/doc.figcraft -o out/ok.png --automation-read-root in --automation-write-root out
```

- reads must be inside a read **or** write root; writes only inside a write root; everything else
  is refused with a readable error and nothing is written;
- the roots must be existing folders or the server/app stops at startup (as does any unknown app
  option — a mistyped flag never leaves the app running unconfined);
- every engine file access goes through `crates/engine/src/automation/file_access.rs` (clippy
  forbids `std::fs` elsewhere in the engine), so commands added later are covered too;
- `--attach` plus roots is a usage error: the app does the confining, so start it with the flags;
- path resolution follows symlinks; a non-existent tail must be plain names; a refusal deliberately
  does not reveal what exists outside. Recent files outside the roots are never listed or opened;
- not confined: the files named on the app's own command line at startup (later saves of them are
  confined), and the app's own folders (preferences, recovery copies, plugins installed from a
  plugin directory).

## 6. Document and format details

`.figcraft` (zip) members, from `crates/format/src/lib.rs`:

| Member | Content |
|---|---|
| `document.json` | `{format:"figcraft", version:1, kind?: "board", imageIndex:[{hash,width,height}], …document}` — default-valued fields omitted, so design files carry no `kind` |
| `images/<sha256>` | Raw encoded image bytes (stored, not deflated); names that aren't valid hashes are never read or written back |
| `thumbnail.png` | Optional |
| `versions/index.json`, `versions/<id>.json` | Version history, oldest first, ≤100 versions |
| `branches/index.json`, `branches/<id>/{base,head}.json`, `branches/<id>/versions/` | Branches, ≤100 |
| `library/manifest.json`, `library/document.json`, `library/images/<sha256>` | Present when the file was published as a library |

Reading: a bare `document.json` also opens; structural problems are repaired and reported through
`issues`; a `version` newer than 1 is refused (`FormatError::Newer`); damaged version/library entries
are skipped with a note. `document.json` is capped by a 16× compression-ratio rule within the
512 MiB per-member cap (4 GiB document cap on 64-bit, 1 GiB on 32-bit), and one open unpacks at most
6 GiB in total (2 GiB in the browser), images included. Writing: staging file + one atomic rename
(`write_file_atomic`), so a reader sees the old or the complete new file.

File kind: a board is a `.figcraft` whose `Document.kind` is `Board` (`crates/doc/src/board.rs`
`FileKind`, `id()`: `design` | `board`). Board objects stay ordinary layers with a `board` entry
(`{type: sticky|shape|connector|label|stamp|ink|mindNode, …}`; connectors may say `branch: true`),
and Developer Mode measurements are stored on the layer they start from.

Import warnings surface per format: `.fig`/`.jam`, REST JSON, SVG, Sketch and Penpot return
`warnings` (MCP `open_file`) and `note:` lines (CLI), and fill the app's Import report window.

Export surfaces:
- `file.export` formats: png, jpg, svg, pdf, webp, xml, fig (whole file, experimental) and penpot;
  `colorProfile` and `quality` are new at this tag and are stored per export setting by
  `export.add` / `export.update`;
- `file.exportLayers` writes every layer once per export setting, with suffixes/folders, or the
  Inspect assets (icons as SVG, images as PNG);
- `file.exportFramesPdf` writes every top-level frame of a page, one PDF page each;
- `convert` adds `.json` (FigCraft JSON), `.figcraft` and `.penpot` output; the app's Save always
  writes the native archive, and a `.fig` path on Save/Save as writes an export copy without changing
  the document's native path.

## 7. Boards and mind maps

A board is created with `file.newBoard {name?}` (File ▸ New board, the home screen's New board
card); `inspect_document` reports `kind: "board"`. The board commands refuse on a design file
(`board::NEEDS_BOARD`) and prototyping/Developer Mode refuse on a board (`board::NOT_ON_BOARDS`).

| Command | Params → result |
|---|---|
| `board.sticky {x, y, text?, color?, author?, parent?}` | → `{id, text}`; a 200-wide sticky whose height grows with its text; `color` is a board colour or hex. |
| `board.nextSticky {id?, side?, edit?}` | → `{id, text, connector?}`; same colour as the selected note, placed beside it (a shape gets a joined connector). |
| `board.shape {shape, x, y, width?, height?, text?, color?, parent?}` | → `{id, text}`; rectangle, roundedRectangle, ellipse, diamond, triangle, speechBubble, chevron and the newer arrow/flowchart shapes. |
| `board.connector {from, to, fromSide?, toSide?, style?: straight\|elbow\|curved, startCap?, endCap?, label?}` | → `{id, label?}`; ends are layer ids or `{x, y}` page points; re-routes when either end moves. |
| `board.addConnected {id?, side?: right\|below\|left\|above, edit?, at?}` | → `{id, text, connector}`; the next sticky/shape on that side, 80 units away, joined. `at` places a dragged `+` preview at a page point. |
| `board.label {id, text}` | Sets a connector's middle label (empty removes it). |
| `board.stamp {x, y, stamp}` | → `{id}`; a round badge with the placer's name on hover. |
| `board.ink {path \| points, highlighter?, color?, select?}` | → `{id}`; marker or wide see-through highlighter stroke. |
| `board.setColor` · `board.setStyle` | Recolour objects; change a shape's outline/text size or a connector's routing and arrowheads. |
| `board.reattach` · `board.reshape` | Re-attach a connector end; reshape a connector's path. |
| `board.table {x, y, rows?, cols?}` · `board.tableEdit` | Insert a table and edit cells. |
| `board.template {name, x?, y?}` · `board.templates {}` | Place one of five code-built templates / list them. |
| `board.timer`/`board.timerState` · `board.vote`/`board.voteResults` | Facilitation sessions. |
| `board.mindMap {x?, y?, text?, children?, parent?, edit?}` | → `{id, text, children:[{id,text,connector}]}`; root (`mindNode`, bold 24, no box; text defaults to `Topic`, x/y to the middle of the view) with up to 20 `children` (default `Idea 1..3`), each on a curved branch (connector with `branch: true`: stroke 4, `#757575`, round caps). One undo step. |
| `board.mindMapAdd {id?, relation?: child\|sibling, text?, edit?}` | → `{id, text, connector}`; a child below the others, or a sibling right after; the map lays itself out again. |

Mind-map layout (`crates/doc/src/board_mindmap.rs` `mind_layout`): children stand in one column
88 units right of the widest node of the parent's column, 48 apart, centred on the parent; a node is
its text, sized to it. A map's shape is read from its branches (the parent is the layer a branch
arrives from). After every edit, undo or live change a touched map is laid out again from its first
node, so moving the root moves the map and a child moved by hand goes back (or swaps with the sibling
whose middle it passed). Caps: 2,000 nodes, depth 64. Missing: toolbar entry, shortcuts, `+` handles,
dragging a node onto another to reparent, left-side creation by command, and mind-map import from `.jam`.

Pointer tools for boards: `tool.sticky`, `tool.shape`, `tool.connector`, `tool.marker`,
`tool.highlighter`, `tool.eraser`, `tool.stamp`. Board keys in the keymap: Q sticky, B shapes,
X connector, M marker, U highlighter, E eraser, W stamp, Shift+Cmd/Ctrl+Enter next sticky.

```json
[
  {"command": "file.newBoard", "params": {"name": "Retro"}},
  {"command": "board.sticky", "params": {"x": 0, "y": 0, "text": "Went well", "color": "green"}},
  {"command": "board.sticky", "params": {"x": 240, "y": 0, "text": "To improve", "color": "pink"}},
  {"command": "board.connector", "params": {"from": {"$step": 1}, "to": {"$step": 2}, "style": "elbow"}}
]
```

Mind map, from scratch:

```json
[
  {"command": "file.newBoard", "params": {"name": "Plan"}},
  {"command": "board.mindMap", "params": {"x": 200, "y": 200, "text": "Launch",
    "children": ["Design", "Build", "Ship"]}},
  {"command": "board.mindMapAdd", "params": {"id": {"$step": 1, "field": "id"}, "relation": "child",
    "text": "Screens"}}
]
```

## 8. Data fill and text fitting

`data.fill {id, rows, gap?, formats?, dir?, format?, scale?}` repeats a frame once per row in one
undo step; each key of a row names a layer in the copy, a string sets its text, and
`{text?, fill?, visible?}` sets more. `formats: [{name?, width, height}]` makes every row once per
size (the copy is resized so its auto layout reflows); `dir` exports each copy after the edits land.
Returns `{ids, missing, files?, errors?}` (`crates/engine/src/content/datafill.rs`).

`text.fit {ids?, maxLines?, minSize?, orphans?}` gives a fixed-width text the largest font size
(down to `minSize`, default 60% of the current) that stays within `maxLines` and its box; it avoids
one-word last lines and never grows text (`crates/engine/src/content/textfit.rs`).

```json
{"command": "data.fill", "params": {"id": 80, "dir": "out/carousel", "rows": [
  {"name": "01-cover", "Headline": "Your site in 7 days", "Badge": {"visible": true}},
  {"name": "02-proof", "Headline": "Lighthouse 100, under a second", "Badge": {"visible": false}}
]}}
```

## 9. Live sessions from a script (`collab.*`)

**22 `collab.*` commands** at this tag. The headless MCP session and the attached app can host, join
and publish; the one-shot `run` cannot (no network link). The web build can join and publish, but
not host on the local network.

| Group | Commands |
|---|---|
| Host/join/share | `collab.host` (port 47900 default, `bind: local\|lan\|IP`), `collab.share {via?, access?, server?, name?, port?, bind?}` (`access`: edit/comment/view), `collab.join {code\|link}`, `collab.reconnect`, `collab.stop`, `collab.leave` |
| Publishing | `collab.publish`, `collab.serverInfo`, `collab.manageFile`, `collab.files`, `collab.openFile`, `collab.forgetFile`, `collab.recoverFile`, `collab.report` |
| Presence/inspection | `collab.peers`, `collab.diff`, `collab.follow`, `collab.spotlight`, `collab.removePerson`, `collab.cursor`, `collab.cursorChat` |

`collab.reconnect {}` → `{status}`: for the open file's session when it is disconnected, a waiting
reconnect tries now, and a session that couldn't go on is joined again there, with what you changed
since going on top. Refused when nothing was lost. Sessions reconnect until you leave; offline edits
merge on rejoin through the three-way merge branches use.

`collab.registerLinks {on?}` is app-level: it makes the Windows build the opener of `figcraft://`
invite links (macOS and Linux packages declare the scheme at install time).

**Caution:** `collab.share` with `via: "online"` (its default) publishes the document to a server
other people run — the public default unless Preferences name another. Only call it when sharing is
the request; prefer `collab.host` (local, no server) for a demo. Codes and links are the only access;
there are no accounts. The server stores files unencrypted, and the default public server keeps a
file until removed or 30 days unopened.

## 10. Server (preview)

`figcraft-server` (`cargo build --release -p figcraft-server`; releases ship a Linux build) has
subcommands: `serve` (default), `key [--rotate]`, `check`, `files [list] [--sort …]`, `files remove`,
`links list\|create\|revoke`, `plugins [list\|remove] [--version N]`, `reports`, `block-ip`,
`unblock-ip`, `blocked` (`apps/figcraft-server/src/cli.rs`, `docs/server.md`). The repo also ships
`packaging/server/{Caddyfile,caddy-test.sh}` for the TLS reverse proxy setup.

Config keys include `listen`, `data`, `public_url`, `max_files`, `max_file_mb`, `max_links`,
`max_connections`, `max_people`, `compact_after`/`compact_mb`, `max_plugins`/`max_plugin_mb`/
`max_plugins_mb`, `max_log_mb`, `open_publish`, `operator_contact`, `terms_url`, `trusted_proxy`,
`idle_days`, `max_total_mb`, and per-address limits (`max_files_per_ip`, `max_mb_per_ip`,
`max_connections_per_ip`, `connects_per_minute`, `publishes_per_hour`, `messages_per_second`)
(`apps/figcraft-server/src/config.rs`). `GET /healthz` answers `ok`. Deploy on a Linux box with a TLS
reverse proxy; the desktop app connects over `wss://` with certificates verified (`FIGCRAFT_CA_FILE`
for a private authority).

## 11. Recipes that match the semantics

Build a screen headlessly, then export it:

```json
[
  {"command": "file.newFromTemplate", "params": {"template": "mobile-app"}},
  {"command": "frame.create", "params": {"preset": "iPhone 16", "x": 0, "y": 0, "name": "Home"}},
  {"command": "node.create", "params": {"type": "text", "parent": {"$step": 1}, "x": 24, "y": 64,
    "text": "Welcome", "props": {"fontSize": 32, "fontStyle": "Bold"}}}
]
```

```sh
figcraft-cli run build.json --out home.figcraft
figcraft-cli export home.figcraft -o out/ --format png --scale 2
figcraft-cli info home.figcraft --json
```

Attach to a running app and verify after each change (replace `2` with the id your create call
returned):

```json
{"id":1,"method":"engine.execute","params":{"command":"layout.add","params":{"ids":[2],"direction":"vertical"}}}
{"id":2,"method":"document.inspect","params":{"depth":3}}
{"id":3,"method":"ui.render","params":{"ids":[2],"path":"out/card.png"}}
```

Use `document.inspect`/`get_node` after every batch, and `screenshot`/`ui.render` before declaring a
design done. A failed command is not a partial success: check `ok`, then inspect the document.
