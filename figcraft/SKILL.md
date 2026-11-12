---
name: figcraft
description: >
  FigCraft is an open-source, pure-Rust, offline interface-design, prototyping and whiteboard app (a
  clean-room reimplementation of the Figma Design workflow): frames, auto layout, components,
  styles, variables, vector networks, prototyping, Developer Mode, mind maps and board files, on
  macOS, Windows, Linux, FreeBSD and the web. Trigger it whenever the user mentions FigCraft or a
  `.figcraft` file, asks what it can or cannot do, which formats it opens or writes, how to script,
  automate, batch or headlessly drive it (figcraft-cli, MCP, the JSON control channel), wants assets
  prepared for a design file, needs output verified or repaired, or asks to troubleshoot it — and
  when the app is not named but the job is one of its jobs: "make a mockup", "design a screen /
  landing page / dashboard", "build a design system", "export these frames to PNG/PDF/SVG", "open
  this .fig or Figma file JSON", "convert this Sketch or Penpot file", "prototype this flow", "hand
  this off to a developer", "make a retro board", "make a mind map". Do not guess capabilities from
  Figma knowledge — FigCraft is not Figma and runs no Figma plugins.
---

**Audit basis.** Refreshed **2026-11-12** against tag **v0.18.1**, commit
**`4acc293c2ec941ac1400837ee7e3ab51780399f8`** — `git rev-parse HEAD` in the pinned checkout
confirms. The installed bundle is `FigCraft.app` version 0.18.1 (bundle identifier
`ai.storyteller.figcraft`), and its binary prints `FigCraft 0.18.1
(4acc293c2ec941ac1400837ee7e3ab51780399f8)` for `--version` (which returns before any window is
created). The previous release this skill described was **v0.16.0**
(`f45b261687880e56d1bad11ec82b45131e57ef8b`).

**v0.16.0 → v0.18.1 delta.** Measured in the checkout, not copied from release notes: `git diff
v0.16.0..HEAD` changes **448 files** (+22,803/−1,969; the shallow clone holds one squashed commit
between the tags). `spec!` registration sites **637 → 646** (**488 → 493** in
`crates/engine/src/cmd/`), with nine ids new and **none removed**: `board.mindMap`,
`board.mindMapAdd`, `collab.reconnect`, `selection.createColorStyle`, `text.direction` and its
`Auto`/`Ltr`/`Rtl` variants, `tool.crosshair`; `board.*` 21 → **23**, `collab.*` 21 → **22**,
locale catalogs 24 → **25** (`zh-Hant`). CLI **10** verbs, MCP **19** tools, **17** app control
methods and plugin **API 6** are unchanged. Feature work: **mind maps, step 1** —
`board.mindMap` places a root and up to 20 children on curved branch connectors, `board.mindMapAdd`
adds a child or sibling, and a touched map is laid out again from its root (88 between columns, 48
between siblings; 2,000 nodes, depth 64) (`crates/doc/src/board_mindmap.rs` `mind_layout`,
`crates/engine/src/boards/board/mindmap.rs`, `docs/boards-parity.md`); **per-paragraph text
direction** — Text ▸ Text direction, `text.direction {direction}`, `node.set textDirection`,
inspect `textDirection`/`lineDirections`, CSS `direction`, `.fig` `sourceDirectionality`
(`crates/engine/src/cmd/text.rs`, `docs/ui-parity.md`); **Selection colors** gained
`selection.createColorStyle` and per-row library style menus
(`crates/engine/src/selection/selection_colors.rs`, `crates/ui-egui/src/panels/selection_colors.rs`);
**Suggest auto layout** splits a frame into rows/columns and wraps bands in nested auto layout
frames (`crates/engine/src/cmd/structure/suggest.rs`); the **placement crosshair** for arrow-key
placement with a shape/frame tool (`tool.crosshair`, `crates/engine/src/cmd/view.rs`); **export
profiles** — `colorProfile` (sameAsFile/srgb/displayP3) on PNG/JPG/WebP and JPG `quality` 1–100
(default 90) on `file.export`, export settings and MCP `export` (`crates/engine/src/cmd/file.rs`,
`crates/engine/src/export_profile_tests.rs`), plus `.fig` scale fixes for Scale-tool instances
(`crates/format/src/fig/export/scale.rs`); **the handoff mode is called Developer Mode** in the UI,
CLI help and all catalogs, with ids `view.devMode`/`dev.*` and saved fields unchanged and "Dev Mode"
kept as an Actions-palette search alias (`docs/feature-names.md`, `crates/engine/src/catalog.rs`
`SEARCH_ALIASES`, `crates/ui-egui/src/naming_tests.rs`); the web build's `window.figcraft` is now the
shared `craft-web-api` page API plus FigCraft's file functions, with a 30 s request timeout and
cancellation (`apps/figcraft-web/src/api.rs`, `docs/control-protocol.md`); `collab.reconnect` and
paced reconnect queues (`crates/engine/src/sharing/live/join.rs`, `crates/collab-net/src/throttle.rs`).
Hardening: CLI `info`/script errors escape terminal control characters
(`apps/figcraft-cli/src/files.rs`), import id collisions fixed
(`crates/engine/src/cmd/file/import_ids.rs`), Thai/Lao/Khmer/Burmese breaks via ICU4X
(`crates/text/src/breaks.rs`), SVG `color()`/`color-mix()` import
(`crates/svg/src/import/css_color.rs`), and a pending update installs on quit
(`apps/figcraft/src/main.rs`).

**v0.15.0 → v0.16.0 delta (history).** 133 files (+4,156/−545). The automation surface was
shape-identical — 10 CLI verbs, 19 MCP tools, 17 control methods, 24 locales — with exactly one new
command id, `text.wrapStyle` (`auto|balance|pretty`); feature work was glass rebuilt to the
reference tool's optics, the Bend tool curving a sharp point on a click, and the web build's
embedding host bridge (`?host=parent`, `data-host="page"`). Older history (v0.13.x–v0.15.0) is
folded into `CHANGES.md`.

**Verify against your installed version** — the ArtCraft Launcher auto-updates, so a newer build may
differ; every headline count was re-measured at this tag, and the measurement method for each count
is in `evidence.md`.

# FigCraft

## Overview

FigCraft is a native, offline interface-design and prototyping app written entirely in Rust
(egui/eframe UI, tiny-skia CPU renderer, no Electron), built clean-room from public documentation and
observed behaviour against Figma Design (`README.md`, `docs/target-app-parity.md`). It is **alpha**:
the README still says "about 49%" of the way to replacing proprietary tools, while the measured table
says **~53% ready**, **~85% feature breadth** and **~94% core-editor breadth** (`ROADMAP.md`,
`docs/target-app-parity.md` › Headline). It runs on macOS, Windows, Linux, FreeBSD and in the browser
via WebAssembly; source is GitHub `storytold/figcraft`, MIT OR Apache-2.0. Every user-visible action
is a command in one registry — **646 `spec!` registration sites** (493 in `crates/engine/src/cmd/`;
641 distinct literal ids, a few const-built) covering the catalogued menu tree
(`crates/engine/src/cmd.rs` `spec!`, `crates/engine/src/catalog.rs`) — dispatched identically by the
UI, CLI, control channel and MCP server.

## Capabilities (verified)

**Model and editing**
- Frames, groups, sections, mask groups, rectangles (squircle corners), ellipses with arc/ring
  handles, polygons, stars, lines, text, vector networks, boolean groups, components, sets,
  instances, slices and board objects (`crates/doc/src/node.rs` `NodeKind`, `crates/doc/src/props.rs`).
- **Auto layout**: flow, wrap and grid with fixed/hug/`fr` tracks, spans, padding, gaps, Hug/Fill/
  Fixed sizing, min/max sizes, absolute children, baseline cross-align and `contentAlign`; layers
  drag across nested auto layout frames with coherent sizing (`crates/layout/src/lib.rs`,
  `crates/engine/src/al_nesting_tests.rs`). **Suggest auto layout** (`layout.suggest`) splits a
  frame's layers into rows or columns by their gaps, wraps each multi-layer band in a hugging frame,
  recurses, keeps the frame's size and returns `warnings` for uneven gaps and overlaps
  (`crates/engine/src/cmd/structure/suggest.rs`, `docs/ui-parity.md`).
- **Vector networks**: Pen/Pencil, vector edit mode (bend, paint bucket, lasso, cut), shape builder,
  editable booleans, per-point radius/handles/caps/joins, variable-width strokes, outline stroke,
  dashes with a Dash cap setting, per-side strokes, stretch and scatter brushes with pen pressure,
  text on a path, pattern fills, per-region fills and fill rules with loop reversal; a Bend click on
  a sharp point curves it between its neighbours (`crates/engine/src/canvas/vectoredit/`,
  `crates/pathops/src/{lib,brush}.rs`, `crates/engine/src/canvas/shapebuilder.rs`).
- **Text**: in-place editing, mixed styles, auto width/height with max lines, truncation, variable
  font axes, OpenType features, lists, bidi/RTL with **per-paragraph direction** (Auto / Left to
  right / Right to left), HarfRust shaping plus system or `craft-fonts` fonts, missing-font
  reporting/loading/refitting, `FIGCRAFT_DEFAULT_FONT`, JIS X 4051 kinsoku and Thai/Lao/Khmer/
  Burmese word breaks (`text.direction*`, `text.missingFonts`, `text.loadFont`, `text.refit`,
  `text.wrapStyle`, `text.fit`; `crates/engine/src/cmd/text.rs`, `crates/engine/src/fonts.rs`,
  `crates/text/src/breaks.rs`). Wrap style Auto/Balance/Pretty is per layer; text styles carry
  paragraph spacing, indent, list style and OpenType features, but not direction.
- **Paint and effects**: solid and linear/radial/angular/diamond gradients, image fills with
  adjustments, crop on Cmd/Ctrl resize, paste images into shapes, pattern fills, blend modes,
  inner/drop shadows, uniform and progressive blur, noise, texture, **glass** (variables, thick-lens
  bend, bevel light line, 8 dispersion steps, frost 0–100) and masks; LCH/OKLCH models; sRGB or
  Display P3 documents with profile conversion (`crates/render/src/{glass,backdrop,images}.rs`,
  `crates/color/src/lib.rs`).
- **Components and design systems**: mains, instances with per-layer overrides, sets and variants,
  boolean/text/instance-swap/slot properties, swap/detach/reset/restore, playground, paint/text/
  effect/grid styles, variables (colour/number/string/boolean) with modes, aliases, scopes and
  bindings, JSON/CSS import/export, Dart constants for Flutter, local libraries read read-only and
  installed from `.figcraft` library files (`crates/doc/src/styles.rs`,
  `crates/engine/src/assets/library.rs`, `docs/components-parity.md`).
- **Selection colors**: a mixed selection lists its shared solid and gradient paints; editing one
  changes every matching fill and stroke in one undo step, a row selects its layers or applies/
  detaches a colour style or variable, library colour styles are offered per row, and
  `selection.createColorStyle {targets, name, description?}` makes a style of the row's whole paint
  and links every fill and stroke it stands for (`selection.colors`, `selection.setPaint`,
  `selection.applyColorStyle`, `selection.bindColorVariable`, `selection.detachColor`,
  `selection.selectColor`; `crates/engine/src/selection/selection_colors.rs`).
- **Boards**: `File ▸ New board` / `file.newBoard`; `.figcraft` stores `kind: "board"` and
  `inspect_document` reports it (`crates/doc/src/board.rs` `FileKind`). **23 `board.*` commands**:
  stickies, shapes, dot/line grid settings, connectors (straight/elbow/curved, re-attachable,
  reshapeable, labelled), `board.addConnected` with drag placement, stamps, ink, labels, text,
  colour/style setters, tables, five board templates, timer and voting sessions, and **mind maps**
  (`board.mindMap`, `board.mindMapAdd`; `crates/engine/src/boards/`). Board objects are ordinary
  layers with a `board` field, so rendering, saving, export, copy/paste, undo and live sessions work
  unchanged; prototyping/Developer Mode refuse on boards.
- **Prototyping**: 10 trigger kinds, 11 actions (overlays position relative to their opener;
  scroll-to, set variable/mode, conditionals), 8 transitions, 13 easings/springs, flows,
  presentation with device frames and live preview (`crates/doc/src/proto.rs`,
  `crates/ui-egui/src/present.rs`, `docs/prototyping-parity.md`).
- **Handoff / Developer Mode** (called Dev Mode before #2135): ready-for-dev status with Changed
  detection and comparison against the marked snapshot or any saved version, annotations,
  measurements kept on the canvas, an inspect-only canvas and read-only layers panel, and generated
  code for **CSS/HTML/React/Vue/Leptos/SwiftUI/Compose/ArkUI plus a React + Tailwind page, a Tailwind
  theme export, Dart constants for Flutter and Android Vector Drawable (XML)**; CSS writes
  `direction` for forced paragraphs (`crates/engine/src/dev/`, `docs/dev-mode-parity.md`).
- **In-file review**: comment threads, named versions with preview/restore/duplicate, and branches
  with update-from-main, review and merge (also in live sessions) (`crates/doc/src/comments.rs`,
  `docs/collaboration-parity.md`).

**Formats it opens (verified in code)**
- `.figcraft` — native zip, or a bare `document.json` (`crates/format/src/lib.rs`).
- `.json` — FigCraft document JSON, or the Figma REST API file response, plus an optional
  local-variables JSON and an `images/<imageRef>.*` folder (`crates/format/src/rest`).
- `.fig` — best-effort import of Figma's own file, never overwritten by Save; large files keep
  layers and library links, budgets come from the file's own size, and an import report lists what
  changed and its coverage (`crates/format/src/fig`).
- **`.jam` / `.penpot` / `.sketch`** — FigJam opens as a **board** (best effort: stickies/shapes
  become frames, connectors vectors, a saved elbow path kept); Penpot 2.x ZIP archives import
  offline; Sketch 48+ imports best effort (`docs/file-format-parity.md`,
  `crates/format/src/{penpot,sketch}.rs`, `docs/penpot.md`).
- `.svg` — imported as an editable frame; unsupported filters are dropped with a warning; CSS
  `color()` and `color-mix()` are resolved (`crates/svg`, `crates/svg/src/import/css_color.rs`).
- Images: `.png`, `.jpg`/`.jpeg`, animated `.gif`, `.webp`, `.bmp`, `.tif`/`.tiff`, with embedded ICC
  profiles honoured (`crates/engine/src/cmd/file.rs`, `crates/render/src/images.rs`).
- PDF is **export-only**; there is no PDF import, no HEIC and no video decode.

**Formats it writes**
- `.figcraft` — native zip: `document.json`, `images/<sha256>`, optional `thumbnail.png`, `versions/`,
  `branches/`, `library/`; staging file plus one atomic rename. Save refuses to overwrite a file
  another app changed or one whose images past the decode budget were not loaded; NaN/infinite
  numbers are written as 0 (`crates/format/src/lib.rs`).
- `.svg`, `.png`, `.jpg`/`.jpeg`, `.webp`, `.pdf`, `.xml` (Android Vector Drawable) and `.fig`
  (`crates/doc/src/props.rs` `ExportFormat::from_ext`, `apps/figcraft-cli/src/files.rs` `write_doc`);
  `.pdf` is one page per top-level frame with selectable text, links, bleed/crop marks and naive CMYK
  (`crates/pdf`, `docs/cli.md`).
- **`.penpot`** — offline Penpot 2.x archive export (`file.export {format: "penpot"}`,
  `figcraft-cli export … --format penpot`; `crates/format/src/penpot.rs`).
- `.fig` — experimental export Figma imports, with component set properties, instance sizes,
  variables with modes, styles, variable-width strokes and grid tracks; effects, images and
  prototypes are unchecked there, and every omission is a `warning` (`crates/format/src/fig/export.rs`,
  `docs/file-format-parity.md` › Export to `.fig`).
- `.json` — FigCraft JSON is written by `figcraft-cli convert`/`run --out`, **not** by the app's Save
  (Save always writes the native archive; `crates/engine/src/cmd/file.rs` `save_to`).

**Automation surfaces (re-measured at this tag)**
- **`figcraft-cli`** — headless engine with **10 subcommands** (unchanged at v0.18.1): `info`,
  `export`, `convert`, `render` (png/jpg/webp), `run` (JSON/JSONL command scripts), `commands`,
  `mcp`, `plugin publish`, `connect publish`, `perf` (`apps/figcraft-cli/src/args.rs`
  `enum Command`, `docs/cli.md`). Every subcommand takes `--no-system-fonts`;
  `info`/`export`/`convert`/`render`/`run`/`mcp` also take `--automation-read-root` and
  `--automation-write-root`; `mcp --attach PORT` takes `--timeout SECONDS` (1–600); `--help`/`-h`
  is accepted anywhere among the options and exits 0.
- **`command.batch`**: steps can be named with `as` and referenced with `$ref`, `field` accepts
  paths, batch errors name the failing step, and a failed step still prints `"rolledBack": true` and
  exits 1 having written nothing (`crates/engine/src/cmd/`, `docs/mcp.md`).
- **Control channel** — `figcraft --control <port>`, loopback-only, newline-delimited JSON with
  **17 methods** (unchanged at v0.18.1): `engine.execute`, `engine.commands`, `document.inspect`,
  `node.get`, `ui.inspect`, `ui.pointer`, `ui.key`, `ui.type`, `ui.input`, `ui.menu.invoke`, `ui.set`,
  `ui.screenshot`, `ui.render`, `window.new/list/focus`, `app.quit` (`crates/ui-egui/src/control.rs`,
  `docs/control-protocol.md`). `document.inspect`/`node.get` take `fields` and `outline` to trim
  responses; state methods answer while minimised, while `ui.screenshot`, `ui.input` and
  `window.new` fail fast (`NEEDS_FRAME`). `events.poll` is documented but only the MCP bridge
  implements it (`crates/mcp/src/headless.rs`); the app's channel answers `unknown method`.
- **MCP server** — `figcraft-cli mcp` (headless) or `--attach <port>` (drives the running app);
  **19 tools** (set unchanged at v0.18.1): `list_commands`, `run_command`, `batch`, `create_node`,
  `set_properties`, `inspect_document`, `get_node`, `select`, `export`, `screenshot`, `open_file`,
  `save_file`, `undo`, `redo`, `pointer`, `key`, `type_text`, `inspect_ui`, `wait_for_changes`;
  **3 resources + 2 templates** (`figcraft://document`, `figcraft://commands`,
  `figcraft://comments`, `figcraft://node/{id}`, `figcraft://command/{id}`) and **4 prompts**
  (`crates/mcp/src/{tools,resources,prompts}.rs`, `docs/mcp.md`). Responses
  are size-bounded: `maxBytes` (default 8 MiB), plus `get_node`'s `offset` and a `truncated` marker.
- **Web page API** — the browser build exposes `window.figcraft`: the shared `craft-web-api`
  functions `request`, `execute`, `commands`, `docInspect`, `uiInspect`, `screenshot`, plus
  FigCraft's `inspect`, `openFile(name, bytes)`, `captureDownloads(on)`, `files()` and
  `readFile(name)`; calls reject after 30 s and an unstarted request is cancelled
  (`apps/figcraft-web/src/api.rs`, `docs/control-protocol.md` › In the browser).
- **Live sessions from a script** — **22 `collab.*` commands** cover host/join/share/publish,
  cursors, chat, spotlight, file management and `collab.reconnect`; `branch.*` commands work inside
  live sessions; the headless MCP session and the attached app can host, join and publish, the
  one-shot `run` cannot (no network link) (`crates/engine/src/sharing/`, `crates/collab-net`,
  `docs/mcp.md` › Live sessions).
- **Plugins** — sandboxed WebAssembly (wasmi, metered fuel, memory cap, no fs/net/clock), manifest
  permissions (**API version 6**, unchanged at v0.18.1; `saveFile` permission), panels, settings and
  canvas widgets that take text input, offer a property menu, open their plugin's panel and draw
  lines and SVG pictures; Rust SDK and four example plugins
  (`crates/plugin/src/manifest.rs:11` `API_VERSION: u32 = 6`, `plugins/examples`, `docs/plugins.md`).
- **Templates** (unchanged at v0.18.1) — eight design starters via `template.list`/
  `file.newFromTemplate`, five board templates (`crates/engine/src/content/templates.rs`,
  `crates/engine/src/boards/board_templates.rs`) and five example documents (`examples/`).
- **Discovery is a command**: `figcraft-cli commands --json` (or MCP `list_commands`) prints each
  command's id, label, menu path, shortcut and parameters; an unknown id gets the nearest one.

**Platform and runtime facts**
- WebAssembly build: **yes**; the browser build joins but cannot host local-network sessions, keeps
  one window, has no system fonts/accessibility tree, and can publish to a server. Its **host bridge
  for embedding** (`?host=parent`, which wins over `data-host="page"`) takes a parent-provided file
  and hands a Save back under the host's file name (`apps/figcraft-web/src/{host,hostmode}.rs`).
- Releases package macOS universal, Windows x64/x86/arm64, Linux (AppImage, deb, rpm, Flatpak,
  tarball), FreeBSD and web (`README.md`, `packaging/`); Windows installs per-user by default.
- **Startup update prompt with direct self-updating** (craft-update crate); an update that waits for
  the app to close installs on quit (`apps/figcraft/src/main.rs`). No `unwrap`/`expect`/`panic` in
  shipped code (clippy denies them), a command guard rolls a panicking command back, and recovery
  copies are written every 10 s (`crates/engine/src/guard.rs`, `apps/figcraft/src/recovery.rs`).
- Accessibility: AccessKit names/roles on desktop, F6 cycles toolbar → layers → canvas → properties,
  reduced motion honoured (`crates/ui-egui/src/a11y.rs`).
- One process shows several **windows**, each with tabs and panels; first run opens the home screen
  (Recents, Online, Templates) (`crates/ui-egui/src/{windows,home}.rs`).

## Known limitations and not-implemented

**Partial** means it exists but is visibly incomplete; the rest are **not implemented** or **claimed
only**. Treat these as hard constraints.

- **Mind maps are step 1 of 4** and command-only: `board.mindMap`/`board.mindMapAdd` place and
  extend a map, but there is no toolbar entry, shortcut, `+` handle, drag-to-reparent, left-side
  creation, mind-map import from `.jam`, or cross-map linking (`docs/boards-parity.md`).
- **Boards are still partial** past mind maps: sticky size presets/stacks, more shapes, a stamp
  wheel, board widgets beyond plugin widgets, washi tape, code blocks, board image cropping,
  audio/huddles, AI features and `.jam` export are missing.
- **Selection colors are partial**: no library *variables* in the row menus and no "new variable
  from a row"; a style created from a row links fill/stroke lists it stands for, not text ranges
  (`docs/ui-parity.md` › Selection colors).
- **Text direction is per paragraph, not in text styles**; `text.directionAuto` is FigCraft's own
  way back to language detection (`crates/engine/src/catalog.rs` `OWN`, `docs/ui-parity.md`).
- **No real-Figma-file validation.** Every `.fig` corpus in the repo is synthetic; import is "best
  effort" and nothing has been checked against real documents (`docs/gaps.md` 1 and 3). Missing
  formats: HEIC images and video fills/triggers (no Rust decoder), `.jam` and `.deck` export
  (`docs/file-format-parity.md`).
- **No Figma plugin compatibility.** FigCraft runs its own WASM plugins (API 6), not JavaScript
  Figma plugins; widgets still have no timers, and there is no public plugin catalogue
  (`docs/gaps.md` 6, `docs/plugins.md`).
- **No AI features at all** and **no spell check** (`docs/gaps.md` 11 and 19).
- **Multiplayer is a preview**: live sessions with sync, cursors, selections, text carets, chat,
  spotlight, per-person undo, invite links, automatic reconnect and `collab.reconnect`, branches in
  sessions, plus a self-hosted `figcraft-server`, but **no accounts and no teams**; codes/links are
  the access and the server stores files unencrypted (`README.md` › Privacy and online sharing).
- **Prototype tail**: no media triggers/actions; controller buttons are read on Windows and in the
  browser but not on macOS, Linux or FreeBSD (`docs/prototyping-parity.md`).
- **Developer Mode tail**: renaming the file from Developer Mode to check its name and the editor
  extension are still missing (code-connect publishing landed 2026-10-30); the component playground
  has no slot control (`docs/dev-mode-parity.md`, `docs/gaps.md` 16).
- **CPU canvas, sRGB screen**: Display P3 documents show sRGB-clipped with a gamut warning and
  soft-proof striping (true P3 is blocked upstream in egui-wgpu) (`docs/hardware-parity.md`).
- **Export limits**: SVG and PDF refuse a tree deeper than 256 descendant levels rather than writing
  an incomplete file; PDF `--cmyk` is the naive `K = 1 − max(R,G,B)` conversion with no output
  intent; SVG, PDF and XML are always sRGB, and JPG quality has no Export-panel control (it exists
  on `file.export`, export settings and MCP `export`) (`docs/file-format-parity.md`, `docs/gaps.md` 23).
- **Screen readers have never been run** against the app; the browser build has no accessibility
  tree, and Linux/browser platform QA is still open (`docs/gaps.md` 22 and 8).
- **Localization status is claimed, not verified here**: **25 catalogs** in
  `crates/ui-egui/locales/` (including new `zh-Hant`); Russian and Turkish were reviewed natively,
  most others are drafts (`docs/localization-parity.md`).
- **Menu-breadth numbers drift, trust code**: `docs/parity-checklist.md` still reports **212 / 212**
  menu items, but it was generated 2026-10-21, before `Text ▸ Text direction`; a static count of
  `catalog::MENU` minus `OWN` and `collab.*` gives **214** items at this tag. Four ids
  (`object.rotate180`, `view.zoom50|100|200`) do not appear as literal `spec!` ids in a static scan,
  so re-run `cargo xtask parity` in a build to confirm all 214 are wired.
- **Bounds worth knowing**: ≤100 versions and ≤100 branches per file; `document.json` is capped by a
  16× compression-ratio rule within 512 MiB per zip member (4 GiB document cap on 64-bit, 1 GiB on
  32-bit); one file open unpacks at most 6 GiB in total (2 GiB in the browser)
  (`crates/format/src/lib.rs` `MAX_VERSIONS`, `MAX_BRANCHES`, `DOCUMENT_RATIO`, `MAX_MEMBER`,
  `MAX_DOCUMENT`, `MAX_UNPACKED`).

## How to operate

**Launch.** Installed app: `FigCraft.app` (bundle `ai.storyteller.figcraft`); `open -a FigCraft
[file.figcraft]` opens a file. The bundle declares the `figcraft` document type, SVG, PNG and JPEG
types and the `figcraft://` URL scheme (`packaging/macos/Info.plist.in`). To pass flags, run the
binary inside the bundle:

```sh
"FigCraft.app/Contents/MacOS/FigCraft" --control 7979 WORK/project/app.figcraft
"FigCraft.app/Contents/MacOS/FigCraft" --control 7979 \
    --automation-read-root WORK/project --automation-write-root WORK/project/out
```

`--control <port>` starts the loopback JSON-lines control server (or set `FIGCRAFT_CONTROL_PORT`);
`--automation-read-root` / `--automation-write-root` (repeatable) confine every file the channel and
windows may read or write; any unknown option — including a mistyped root flag — stops the app at
startup instead of running unconfined (`apps/figcraft/src/args.rs`). An invite link
(`figcraft://join?…`) or a `file://` URL on the command line opens or joins it.

**There is no CLI inside the macOS bundle.** Build it with `cargo build --release -p figcraft-cli` →
`target/release/figcraft-cli`; macOS releases ship a separate
`figcraft-cli-<version>-macos-<arch>.zip` (`packaging/macos/package.sh`). On Linux only,
`FigCraft.AppImage cli <args>` runs it (`packaging/linux/AppRun`).

**CLI surface** (verified in `apps/figcraft-cli/src/args.rs`, `docs/cli.md`):

```sh
figcraft-cli info app.figcraft [--json]                 # + missingFonts per file
figcraft-cli export app.figcraft -o exports/ --scale 2  # one file per top-level frame
figcraft-cli export app.figcraft -o hero.svg --node "Hero"
figcraft-cli convert in.svg out.figcraft                # .sketch/.fig/.penpot also read
figcraft-cli render app.figcraft -o page.png --scale 2  # png, jpg or webp out
figcraft-cli run build.json --in base.figcraft --out result.figcraft
figcraft-cli commands --filter autoLayout [--json]
```

Every subcommand takes `--no-system-fonts` (or `FIGCRAFT_NO_SYSTEM_FONTS=1`) for reproducible
renders. Exit codes: bad arguments 2, failures 1, success 0 (`--help`/`-h` 0). `--scale` ≤64; pages
shrink to fit 16384 px on `render`; PDF bleed ≤2 in. `export` to a directory writes one file per
top-level frame; an image extension, or `--node`, writes one file. PDF print options
(`--bleed 3mm --crop-marks --bleed-marks --cmyk`) also work. The CLI has **no** colour-profile or
JPG-quality flag: use `run` with `file.export {colorProfile, quality}` or MCP `export`.

**Commands validate, they do not coerce.** Unknown parameter names are refused rather than ignored
(`crates/engine/src/cmd.rs` `refuse_unknown_params`), a fractional `index` in
`proto.interaction.remove`/`set` or `layout.setTrack` is rejected, and invalid `dashes` in `node.set`
are an error — read the error instead of assuming the edit landed.

**Document model.** One process shows several **windows**, each with its own **tabs**, panels and
canvas (`window.new`); a first run opens the **home screen** (Recents, Online, Templates, search).
Files are documents with pages and per-tab unsaved changes. A `.figcraft` also carries a **kind**:
`design` (default) or `board` (`crates/doc/src/board.rs` `FileKind`). Boards get a bottom toolbar,
no Design panel by default and a contextual bar above the selection, and refuse prototyping/Developer
Mode; design files refuse the `board.*` commands.

**Round trip.** Open (`.figcraft` / `.json` / `.fig` / `.jam` / `.sketch` / `.penpot` / `.svg` / image)
→ edit (UI, CLI `run`, control channel, MCP) → **Save** (`.figcraft`, atomic staging + rename) → export
(PNG/JPG/SVG/PDF/WebP/XML, `.fig` or `.penpot`). Saving is never in-place over an imported `.fig`;
"Save as" with a `.fig` name writes an export copy and keeps the `.figcraft` path
(`crates/engine/src/cmd/file.rs`); `pref.autoSave` also auto-saves files that have a path.

**Keyboard shortcuts**: do not invent them. The machine-readable list is `figcraft-cli commands
--json` (each command's `shortcut`) or MCP `list_commands`, generated from `crates/engine/src/
keymap.rs` — **163 `k(` binding rows in 12 groups, unchanged at v0.18.1** (Essential, Tools, View,
Zoom, Text, Shape, Selection, Edit, Transform, Arrange, Components, Prototype) plus **47 gesture
rows**, with macOS and, where they differ, Windows/Linux keys. `docs/ui-parity.md` tracks **136
documented shortcut rows, 135 bound as documented**. Board bindings live in the same table (Q
sticky, B shapes, X connector, M marker, U highlighter, E eraser, W stamp, Shift+Cmd/Ctrl+Enter next
sticky); new this round are the arrow-key placement crosshair, Tab pick-select and Cmd/Ctrl-click on
a padding field. The in-app Keyboard shortcuts panel shows the same keymap.

## Working with an AI agent

What an agent can legitimately do:

- **Drive the app headlessly.** `figcraft-cli run` a JSON array (or `.jsonl`) of
  `{"command": id, "params": {…}}`; `{"$step": n}` resolves to the `id` from step `n`'s result, and
  steps can be **named with `as` and referenced with `$ref`** (with paths in `field`), so one script
  builds a whole screen. Scripts are **all-or-nothing and one undo step**; a failed step names itself
  in the error, prints `"rolledBack": true` and exits 1 having written nothing
  (`apps/figcraft-cli/src/files.rs`).
- **Drive the running app** so the user watches: start it with `--control PORT`, then
  `figcraft-cli mcp --attach PORT` (MCP tools) or speak the JSON-lines protocol directly. Attached
  calls are **never replayed** after a transport failure — inspect before retrying an edit
  (`docs/mcp.md`). In the browser, drive the page through `window.figcraft` (`request`, `execute`,
  `commands`, `docInspect`, `uiInspect`, `screenshot`, `openFile`, `captureDownloads`, `files`,
  `readFile`); a call that the app does not answer within 30 s rejects and is cancelled if unstarted.
- **Confine it.** Pass `--automation-read-root` / `--automation-write-root` to the app, `figcraft-cli
  mcp`, or any `info`/`export`/`convert`/`render`/`run` run. Writes need a write root; reads need
  either; `--attach` plus roots is a usage error (`docs/mcp.md` › Confining file access).
- **Prepare inputs.** Generate or convert assets into formats FigCraft reads: SVG (best editable
  import), PNG/JPG/WebP/GIF/TIFF/BMP, or a `.penpot`/`.sketch` file. For real Figma work the
  highest-fidelity path is the REST API file JSON plus its local-variables JSON plus an
  `images/<imageRef>.png` folder — the importer reads all three (`docs/mcp.md` › Importing REST API
  file JSON). PDF is export-only.
- **Generate batches.** `data.fill` + `text.fit` turn one frame and a JSON list of rows into a
  carousel or a set of post sizes with the text fitted — no per-copy editing loop
  (`crates/engine/src/content/datafill.rs`, `docs/mcp.md` › Filling copies with data).
- **Build and extend boards programmatically.** `file.newBoard` then `board.*`: sticky/shape/ink/
  table/template/timer/vote commands, and mind maps with `board.mindMap {x?, y?, text?, children?}`
  then `board.mindMapAdd {id?, relation: child|sibling, text?}`; the map lays itself out again.
  Read back with `document.inspect` (`kind: "board"`) — see `docs/mcp.md` › Boards.
- **Inspect and repair native files** (cautiously). A `.figcraft` is a plain zip:
  `unzip -p f.figcraft document.json` reads the model, `images/<sha256>` holds raw image bytes, and
  `versions/index.json` / `branches/index.json` hold history. Reading is lenient (problems are
  repaired and reported) but a newer format version is refused (`FormatError::Newer`). Prefer
  repairing through commands; if you must hand-edit, keep `format`/`version` and re-zip every member.
- **Hand off code**: pick the Developer Mode target the consumer needs — React, React + Tailwind
  (page code + theme export), Vue, Leptos, SwiftUI, Compose, ArkUI, plain HTML/CSS, Dart constants
  for Flutter, or Android Vector Drawable — and review import lines, transliterated class names and
  `direction` declarations before shipping (`crates/engine/src/dev/`).
- **Verify output.** `figcraft-cli info <file> --json` for structure, notes and missing fonts;
  re-open an export (`convert` back to `.figcraft`) to prove it decodes; compare a PNG export at a
  known `--scale` against a `ui.render`; for `.fig` output, re-open it in FigCraft and read the
  `warnings` list. When colour matters, state the profile: PNG/JPG/WebP default to the document's
  profile and can be forced to sRGB or Display P3.

What an agent must **not** do:

- Do not automate the GUI by clicking blind: use the control channel (`ui.pointer`, `ui.key`,
  `ui.input`, `ui.menu.invoke`, `ui.set`) or commands; programmatic calls never open dialogs.
  `ui.screenshot`, `ui.input` and `window.new` need a visible window (`docs/control-protocol.md`).
- Do not assume a Figma format or feature works. No video fills, no HEIC, no `.jam` export, no
  `.deck`, no Figma plugins, no AI features; `.fig` is best-effort in, Figma-importable out, and
  unproven on real files. The browser build is not equivalent: it can join but not host
  local-network sessions, keeps one window, has no system fonts or accessibility tree, and Display
  P3 is sRGB-clipped on screen.
- Do not put prototyping or board work in the wrong file kind: `proto.*`/`dev.*` refuse on boards and
  `board.*` refuses on design files (`crates/engine/src/boards/` `NOT_ON_BOARDS`, `NEEDS_BOARD`).
- Do not share to a server uninvited: `collab.share` with `via: "online"` (its default) **publishes
  the document to a server other people run** — only call it when sharing is the request.

## Verification protocol

FigCraft is alpha (v0.18.1); treat every automated run as untrusted until checked:

1. **Throwaway round trip per session.** From a template or a copy: create → edit → `save_file`/
   `--out` to `.figcraft` → reopen → export PNG/PDF. Compare `info` node counts before and after; a
   decoder that only reads what it wrote is how the repo tests `.fig` export.
2. **Never trust a silent export.** Watch stderr: exports and imports print `note:` lines for what was
   dropped, `.fig`/REST/SVG/Sketch/Penpot imports return `warnings` (the `.fig` report states its
   coverage), and a failed SVG/PDF depth check leaves the destination intact. Check the exit code;
   the CLI escapes terminal control characters in `info` and script errors, so odd output is data.
3. **Version and back up project files.** Have the user commit or copy their document before a batch
   of automated edits; version history (≤100 versions), branches, auto-save and 10-second recovery
   copies are safety nets, not backups.
4. **Update between projects.** A `.figcraft` from a newer format version is refused by an older one,
   and a board relies on the `kind` field older builds do not know — verify kind and boards after a
   downgrade before trusting a batch run.
5. **Scope credentials and sharing.** Live sessions and servers are previews with code/link access and
   no accounts; don't put confidential work on a server you don't run, and the public server keeps the
   file until removed or 30 days unopened (`README.md` › Privacy and online sharing).
6. **Mind maps and text direction are new.** Re-inspect a map after a batch (it relayouts from its
   root), and verify paragraph run boundaries in `get_node` before declaring direction correct.

## Sources & evidence

- Repo: https://github.com/storytold/figcraft — inspected at tag **v0.18.1**, commit
  **`4acc293c2ec941ac1400837ee7e3ab51780399f8`** (`git rev-parse HEAD` in the pinned checkout; the tag
  is `v0.18.1`, released 2026-11-12). The installed `/Applications/FigCraft.app` matches the release:
  bundle version 0.18.1, bundle identifier `ai.storyteller.figcraft`, and its binary prints
  `FigCraft 0.18.1 (4acc293c2ec941ac1400837ee7e3ab51780399f8)`. Date inspected: **2026-11-12**. The
  GUI was never launched; the bundle was read through `Info.plist` and a `--version` run
  that returns before creating a window, and the macOS bundle ships no CLI.
- Delta v0.16.0 → v0.18.1, measured in this tree: **448 files changed** (+22,803/−1,969) in
  `git diff v0.16.0..HEAD`; `spec!` sites **637 → 646** and **488 → 493** in
  `crates/engine/src/cmd/`; nine new literal command ids and none removed; `board.*` 21 → 23;
  `collab.*` 21 → 22; locales 24 → 25 (`zh-Hant`). Id-set diffs between the two tags are **empty**
  for MCP `TOOL_NAMES`, CLI `Command` variants, control dispatch and plugin `API_VERSION`.
- Count methods and the claim → path → status ledger: `evidence.md`. Operational detail for larger
  jobs — CLI/MCP/control tables, arguments, limits, path confinement, batch semantics, boards, data
  fill, the server — is in `references/automation-surfaces.md`.
- Key files read: `README.md`, `Cargo.toml`, `ROADMAP.md`, `AGENTS.md`;
  `crates/doc/src/{node,props,proto,styles,board,board_mindmap,lib}.rs`;
  `crates/format/src/{lib,library,penpot,sketch}.rs` and `crates/format/src/fig/{export,kiwi,map}.rs`;
  `crates/engine/src/{fonts,keymap,catalog,guard,cmd}.rs`, `crates/engine/src/automation/file_access.rs`,
  `crates/engine/src/sharing/{live,online}.rs`, `crates/engine/src/content/{datafill,textfit,templates}.rs`,
  `crates/engine/src/boards.rs`, `crates/engine/src/boards/{board/mindmap,board_templates}.rs`, `crates/engine/src/selection/selection_colors.rs`,
  `crates/engine/src/cmd/structure/suggest.rs`, `crates/engine/src/cmd/{file,edit,text,view,variables_io,section}.rs`, `crates/engine/src/dev/`;
  `apps/figcraft-cli/src/{main,args,files}.rs`, `apps/figcraft/src/{main,args,recovery}.rs`,
  `apps/figcraft-server/src/{cli,config}.rs`, `apps/figcraft-web/src/{api,host,hostmode}.rs`,
  `crates/mcp/src/{tools,resources,prompts,server,headless}.rs`,
  `crates/ui-egui/src/{control,windows,home,a11y,board_bar,present,naming_tests}.rs`,
  `crates/ui-egui/src/panels/selection_colors.rs`, `crates/ui-egui/locales/`,
  `crates/{plugin/src/manifest,text/src/breaks}.rs`, `crates/svg/src/import/css_color.rs`,
  `crates/collab-net/src/{throttle,driver}.rs`; `packaging/`; `plugins/examples/`.
- Docs read: `docs/{cli,mcp,control-protocol,file-format-parity,gaps,target-app-parity,boards-parity,
  dev-mode-parity,prototyping-parity,components-parity,collaboration-parity,localization-parity,
  hardware-parity,ui-parity,auto-layout-parity,plugins,parity-checklist,architecture,penpot,feature-names}.md`.
- Shared libraries: FigCraft pins its craft-libs crates (incl. `craft-docpath`, `craft-window`,
  `craft-update`, `craft-web-api`) to one revision and patches `krilla` (`Cargo.toml`); the native
  format is defined in this repo, not in craft-libs.
