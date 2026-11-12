---
name: anicraft
description: "AniCraft 0.2.1 is an open-source, clean-room Adobe-Animate-shaped 2D vector animation studio (early alpha) for macOS, Windows, Linux and the web, with stage, timeline, layers, keyframes, classic and shape tweens, symbols, masks, bones, a camera layer, sound, and a 240-command engine that is fully scriptable through `anicraft-cli` (render, GIF, commands, exec, run, serve, MCP) and a five-tool MCP server. Trigger this skill whenever the user mentions AniCraft, asks what it can or cannot do, which formats it opens or writes (.anicraft, .fla, .xfl, SVG, PNG, JPEG, WAV, Ogg, MP3; PNG/SVG/GIF/Lottie/HTML/video export), its shortcuts, how to script, automate, prepare assets for, verify or troubleshoot it — and also when they describe the job without naming the app: \"animate this character\", \"make a bouncing ball\", \"open this Animate file\", \"export a sprite sheet\", \"tween these frames\". Do not infer Animate or SWF behaviour; read this first."
---

**Audit basis (2026-11-12).** Tag **v0.2.1**, commit `d0beaf253274948b55ee9e1107749f9491bff880` (released 2026-11-12). Installed bundle: **AniCraft 0.2.1**, bundle id `ai.storyteller.anicraft`; `AniCraft --version` prints `AniCraft 0.2.1 (early alpha)` and the bundled `anicraft-cli --version` prints `anicraft-cli 0.2.1` (both run read-only). This is the **first AniCraft skill**, so it supersedes no earlier skill release; the app release it supersedes is **v0.2.0**. Every count below was re-measured at the tag, not copied from README or release notes.

**Delta: v0.2.0 → v0.2.1 (first audit).** This release's tree carries the surfaces behind **ADR 0052 and 0055–0060**: ActionScript "small logic" (typed variables, expressions, `if`/loops, functions across frames, property reads, enter-frame and keyboard listeners) in `crates/actions/src/as3/` and `crates/engine/src/cmds_script.rs`; 9-slice symbol scaling in `crates/doc/src/nine_slice.rs` and `src/scale_grid.rs`; the completed colour-effect model in `crates/doc/src/color_effect.rs`; Find and Replace plus Movie Explorer in `crates/engine/src/find.rs`, `explorer.rs`, `src/find_panel.rs` and `src/movie_explorer.rs`; button-frame sounds and hit-area editing in `crates/engine/src/cmds_sound.rs` and `src/test_movie.rs`; desktop drops, Open Recent and the start screen in `crates/engine/src/cmds_drop.rs`, `cmds_recent.rs`, `src/drop.rs`, `src/recent.rs` and `src/start.rs`; and Publish Settings/Publish in `crates/doc/src/publish.rs`, `crates/engine/src/publish.rs` and `src/publish_panel.rs`. The checkout is a single-commit shallow tag, so there is no v0.2.0 tree to diff — the attribution comes from the ADR files, modules and `CHANGELOG.md` agreeing at this tag (see `evidence.md`).

## Overview

AniCraft is an open-source, clean-room reimplementation of Adobe Animate's 2D vector animation workflow, written in **pure Rust** with an egui/eframe shell — no Electron, Tauri or webview (`README.md`, `Cargo.toml`). A document is plain data and the picture at a frame is a pure function, `evaluate(doc, frame)`; the CPU renderer is the reference oracle, and the stage can draw with wgpu (`crates/doc/src/eval.rs`, `crates/render/`, `crates/gpu/`). It runs natively on macOS, Windows, Linux and FreeBSD and builds for the browser as WebAssembly (`scripts/build-web.sh`, `docs/web.md`). The repo is `storytold/anicraft`, **MIT OR Apache-2.0**, in 13 crates with a strict downward-only layer stack and no `unsafe` (`Cargo.toml` `unsafe_code = "forbid"`; `src/architecture_tests.rs`). Version 0.2.1 is **early alpha**: capable authoring, interchange, headless automation and an MCP server exist, but it is not production animation software (`src/app.rs` `RELEASE_STAGE`; `README.md` status note). This skill documents AniCraft only — do not infer Adobe Animate menus, SWF export or the full ActionScript API from it.

## Capabilities (verified)

**Command engine and automation surface**

* **240 engine commands in 33 namespaces**, each with id, label, menu path, optional shortcut, parameter documentation and a `mutates` flag (`crates/engine/src/lib.rs` `commands()`; 35 `specs()` groups across `crates/engine/src/`). 52 carry default shortcuts; 165 mutate the document. Menus and the command palette are generated from the registry; the shortcut editor adds the tool and view key tables (`src/keymap.rs`, `src/app.rs`).
* **Undo/redo** with structural sharing (`crates/engine/src/history.rs`); **tiered confirmations** enforced in the engine, so agents and scripts hit the same guard: irreversible actions refuse until params carry `"confirm": true` (`crates/engine/src/confirm.rs`, `docs/adr/0004-destructive-actions.md`).
* **`anicraft-cli`** — 11 headless subcommands: `info`, `render`, `render-seq`, `gif`, `commands`, `run`, `exec`, `new`, `bench`, `serve`, `mcp`, plus `help`/`--version` (`crates/cli/src/lib.rs`, `crates/cli/src/main.rs`; verified with `anicraft-cli --help`).
* **MCP server** (`anicraft-cli mcp`) — stdio JSON-RPC with **5 tools** (`anicraft_commands`, `anicraft_run`, `anicraft_run_script`, `anicraft_document`, `anicraft_render`) over protocol revisions **2025-06-18, 2025-03-26 and 2024-11-05** (`crates/cli/src/mcp.rs`; verified by a live `initialize` + `tools/list` handshake). `anicraft_render` returns an actual PNG image, not a path.
* **JSON-lines channel** (`anicraft-cli serve`) — `{"id","cmd","params"}` in, `{"id","ok","result","revision","frame"}` out; `{"cmd":"quit"}` ends it (`crates/cli/src/lib.rs` `handle_request`, `serve`).
* **WebAssembly plug-ins** — sandboxed `wasmi` host, ABI v1, one atomic undo step per run, `plugin.install/list/run/remove/reload` (`crates/plugins/`, `crates/engine/src/cmds_plugin.rs`, `docs/plugins.md`; ADR 0017).

**Stage, drawing and timeline**

* Stage with scenes, layers, layer folders, guide/motion-guide/mask layers, keyframes, classic tweens, shape tweens, motion tweens with a Motion Editor, 8 easing presets, the Classic slider and arbitrary cubic-Bézier ease, motion paths and shape hints (`crates/doc/src/lib.rs`, `eval.rs`, `motion.rs`, `easing.rs`, `hints.rs`; `crates/engine/src/cmds_timeline.rs`, `cmds_frames.rs`, `cmds_motion.rs`, `cmds_hints.rs`).
* Onion skinning, Edit Multiple Frames, multi-frame selection/cut/copy/paste across layers (`src/onion.rs`, `crates/engine/src/multi.rs`, `cmds_timeline.rs`; ADRs 0047, 0051).
* Pen, Subselection, Pencil, rectangle/oval/polystar/line, Object Drawing, merge drawing, Paint Bucket, Ink Bottle, Brush, Eraser, Eyedropper, variable-width strokes, and text blocks (`crates/engine/src/cmds_draw.rs`, `cmds_path.rs`, `cmds_raw*.rs`, `cmds_brush.rs`, `cmds_erase.rs`, `cmds_paint.rs`, `cmds_width.rs`, `cmds_text.rs`; `crates/geom/src/`).
* Symbols and instances — graphic, movie clip and button; nested timelines; 9-slice scaling; filters; blend modes; colour effects; library folders, rename, duplicate, swap, use counts, unused-item cleanup, preview and search (`crates/doc/src/nine_slice.rs`, `filter.rs`, `color_effect.rs`, `library.rs`; `crates/engine/src/cmds_library.rs`; `src/library.rs`).
* Bones with inverse kinematics and a camera layer with pan/zoom/rotate/tint (`crates/doc/src/armature.rs`, `camera.rs`; `crates/engine/src/cmds_bone.rs`, `cmds_camera.rs`).
* Sound — WAV (own reader), Ogg Vorbis and MP3 import, waveforms, per-frame envelopes, layer volume/mute, sounds inside symbols, button-state sounds, WAV export (`crates/audio/`, `crates/doc/src/sound.rs`, `crates/engine/src/cmds_sound.rs`).
* Interactivity — timeline actions, kept frame scripts, a bounded ActionScript 3 subset that runs, a pure player, Test Movie and HTML canvas export (`crates/actions/`, `crates/doc/src/player.rs`, `crates/engine/src/cmds_actions.rs`, `cmds_script.rs`, `src/test_movie.rs`; ADRs 0024, 0028, 0052).

**Files and interchange**

* **Native `.anicraft`**: JSON envelope, **format v3**; v1/v2 files open, newer files are refused with a clear error (`crates/engine/src/format.rs`).
* **Opens Animate documents**: `.fla` archives and `.xfl` folders, including ZIP64 `.fla` layouts and a hardened zip reader (`crates/xfl/`, `crates/engine/src/cmds_file.rs` `is_animate`/`open`; ADRs 0009, 0054). Imported documents are **untitled**, so Save cannot overwrite the Animate file.
* **Imports to the stage**: SVG drawings, PNG/JPEG images, and WAV/Ogg/MP3 sounds (`file.import`; `crates/svg/`, `crates/engine/src/cmds_file.rs`, `cmds_sound.rs`, `cmds_drop.rs` for drops).
* **Exports**: PNG frame, PNG sequence, SVG frame, animated GIF, sprite sheet PNG + JSON frame map, Lottie JSON, self-contained HTML canvas page, MP4/WebM through the user's ffmpeg, and WAV audio (`crates/engine/src/cmds_file.rs` `file.export_*`).
* **Publish**: **9 formats** (HTML, GIF, video, Lottie, sprite sheet, PNG sequence, PNG, SVG, audio) driven by settings stored in the document — in the app a background run with progress and cancel, headless one report (`crates/doc/src/publish.rs`, `crates/engine/src/publish.rs`, `src/publish_panel.rs`; ADR 0060).
* **Find and Replace** over text, fonts, colours, symbols, sounds and bitmaps, plus the **Movie Explorer** (`crates/engine/src/find.rs`, `explorer.rs`; `find.search/replace/goto`, `explorer.tree`).
* **Crash-recovery autosave** and recovery restore/discard (`crates/engine/src/recovery.rs`, `src/autosave.rs`; ADR 0015), desktop drops, Open Recent and a start screen (`src/drop.rs`, `src/recent.rs`, `src/start.rs`; ADR 0059).

**Platform notes**

* GPU stage is the **default** stage renderer in default builds with an automatic CPU fallback; exports always use the CPU oracle (`Cargo.toml` default features `gpu-stage`, `sound-output`; ADRs 0019, 0032).
* macOS shows ⌘ for the registry's `Ctrl+…` shortcuts and has an app menu with a unified title bar; Windows/Linux use Ctrl (`src/platform.rs`, ADR 0006).
* Browser build: the same program for `wasm32-unknown-unknown`, WebGL2, CPU stage, downloads for save/export (`scripts/build-web.sh`, `src/web.rs`, `docs/web.md`; ADR 0036).

## Known limitations and not-implemented

* **Early alpha.** `README.md` says it is "not yet for production animation work"; the roadmap's milestones M2–M8 are still in progress (`docs/roadmap.md`). Do not treat it as a finished Animate replacement.
* **One document per window.** No tabs and no multi-document open; opening another file replaces the current one after the unsaved-changes guard (`docs/roadmap.md`; `docs/adr/0059-files-from-the-desktop-recent-files-and-start-screen.md`).
* **No SWF.** There is no SWF import or export and SWF bytecode is not planned (`docs/roadmap.md` M6 row); `docs/requirements.md` mentions SWF only as an optional idea. Use PNG/SVG/GIF/Lottie/HTML/video instead.
* **ActionScript is a subset.** Variables, expressions, `if`, `for`/`while`/`do`, functions and property reads run; arrays, objects, `switch`, `for in`/`for each`, `new`, closures and `try`/`throw` are refused with a located message (`crates/actions/src/as3/lower.rs`; ADR 0052). The full language, the `flash.*` API and SWF bytecode are not planned.
* **XFL/FLA import is not full fidelity.** No motion-tween import (`motionObjectXML`), armatures, camera, per-character text styles, or sounds stored only in Animate's private format; self-extracting/top-folder `.fla`, encrypted archives and sound/video items are refused or reported (`docs/roadmap.md` M4 row; ADR 0016 and 0054 "Not yet").
* **Motion tweens are a first slice.** No dragging keys in time, ease presets with strengths, saved custom eases, 3D transform, Split Motion, Lottie property curves, or XFL motion-tween import (`docs/adr/0016-motion-tweens.md`).
* **Video needs ffmpeg.** MP4/WebM export streams frames to a user-supplied `ffmpeg` (parameter, `ANICRAFT_FFMPEG`, or `PATH`); no encoder is bundled (`file.export_video` params; `docs/legal/compliance.md`).
* **Export gaps.** Lottie drops bitmap fills, keeps only the innermost nested mask, flattens group fades and reports stretched radial gradients; HTML canvas scales 9-sliced symbols as a whole instead of slicing them (`docs/roadmap.md` Files and Library rows; ADR 0055 "Not yet").
* **Exports are CPU-rendered.** The GPU stage accelerates the editor only; do not promise GPU-speed batch renders (`Cargo.toml` feature comments; ADR 0019).
* **Browser build is partial.** No editor sound, no GPU stage/WebGPU, no video export, no plug-in installs, no zipped PNG sequence, no IndexedDB/threads, and it is not hosted or browser-verified (`docs/web.md`; `docs/roadmap.md` Platforms row).
* **No shipped translations.** The shell is fully keyed for translation and has a pseudo-locale, and 35 locale codes are marked ready, but craft-i18n has no AniCraft catalog yet, so the 0.2.1 UI is English (`src/i18n/mod.rs`, `build.rs`, `docs/localisation.md`).
* **Accessibility is a first pass.** AccessKit names and roles, panel focus keys, high-contrast theme and 75–200 % scaling exist; stage elements/frames are not exposed individually, there is no keyboard menu bar, and no OS contrast following (`src/a11y.rs`, `docs/accessibility.md`; ADR 0022).
* **Smaller gaps** (each in `docs/roadmap.md`): no shared libraries or cross-document library import; no exact desktop drop position (winit limitation); no templates; no Import of `PublishSettings.xml`; no publishing outside the document's folder; no PDF export; no persistence of undo history in recovery; text lacks per-character styles, text on a path and editable input fields; bones lack shape armatures and runtime armatures; the camera lacks perspective depth and XFL import.
* **Packaging caveat.** The macOS bundle exists and was audited here, but `README.md` still says the app was "verified on Windows so far" and `docs/roadmap.md` lists macOS/Linux CI runners as missing. Test your platform rather than assuming parity.

## How to operate

**Desktop.** Launch with `open -a "AniCraft"` on macOS (native builds elsewhere). The window holds one document: a start screen offers New presets, Open, the sample and recent files; after that the stage, tools, timeline, Properties and Library are the main surfaces (`src/start.rs`, `src/app.rs`). The app bundle also contains `anicraft-cli` next to the GUI binary; the release ZIP installs the same CLI separately.

**Core workflow.** Draw on the active layer at the playhead → insert keyframes (`F6`) or blank keyframes (`F7`) → create a classic tween (`timeline.create_tween`) or shape tween (`timeline.create_shape_tween`) → scrub or play → save `.anicraft` → export or publish. Opening `.fla`/`.xfl` imports into an untitled document; Save then asks for a new `.anicraft` name and never overwrites the source (`crates/engine/src/cmds_file.rs`).

**Headless CLI.** All subcommands operate through the same engine and command ids:

| Command | Use |
|---|---|
| `anicraft-cli --version` | `anicraft-cli 0.2.1` |
| `anicraft-cli info <file\|--sample>` | Document JSON: stage, scenes, layers, keyframes, library, sounds, selection, revision |
| `anicraft-cli commands` | The 240-command registry as JSON |
| `anicraft-cli render <file\|--sample> --out frame.png [--frame N] [--scale S]` | One PNG frame |
| `anicraft-cli render-seq <file\|--sample> --out-dir dir [--from A] [--to B] [--scale S]` | PNG sequence |
| `anicraft-cli gif <file\|--sample> --out anim.gif [--from A] [--to B] [--scale S] [--overwrite yes]` | Animated GIF |
| `anicraft-cli new --out file.anicraft [--width W] [--height H] [--fps F]` | New document |
| `anicraft-cli exec <file\|--sample> <id> '<json>' [--save out.anicraft]` | One command |
| `anicraft-cli run <file\|--sample> script.json [--save out.anicraft]` | A JSON array of `{"cmd","params"}` steps |
| `anicraft-cli serve [file\|--sample]` | JSON-lines control channel |
| `anicraft-cli mcp [file\|--sample]` | MCP server on stdio |
| `anicraft-cli bench [--layers N] [--shapes N] [--frames N]` | Performance probe (release build for meaningful numbers) |

Rules that prevent quiet mistakes:

* **Frame bases differ.** CLI `--frame`, `--from` and `--to` are **1-based** (frame 0 is rejected); command params and MCP `anicraft_render`/`anicraft_document` frames are **0-based** (`crates/cli/src/lib.rs` `one_based`; `crates/cli/src/mcp.rs`).
* **A script and the MCP batch use different keys.** CLI `run` takes `[{"cmd":"draw.rect","params":{…}}]`; MCP `anicraft_run_script` takes `{"steps":[{"command":"draw.rect","params":{…}}]}` (`crates/cli/src/lib.rs`; `crates/cli/src/mcp.rs`).
* **Use `"confirm": true`** only after the user agrees; without it, overwriting/deleting/irreversible commands fail with a message (`crates/engine/src/confirm.rs`).
* **Plug-ins are opt-in headless.** Pass `--plugins <folder>` or set `ANICRAFT_PLUGINS`; otherwise headless runs load none and stay repeatable (`crates/cli/src/lib.rs`, `docs/plugins.md`).
* **Save to a new path** when testing (`--save out.anicraft` or `file.save {"path": …}`); `file.save` with no path only works when the session already has a file name.

**MCP.** Register `anicraft-cli` as an MCP stdio server with args `["mcp", "<path to a document>"]` (or `["mcp", "--sample"]`). The server's instructions and tool descriptions are part of the contract: discover commands with `anicraft_commands`, run with `anicraft_run` or `anicraft_run_script`, inspect with `anicraft_document`, look with `anicraft_render` (`docs/mcp.md`, `crates/cli/src/mcp.rs`). `anicraft_render` returns an `image/png` content block plus a one-line description; the picture's longest edge is capped at 2048 px, scale defaults to 0.5 and must be ≤ 4.

**Publish.** `publish.settings_get` returns the document's profile; `publish.settings_set` changes formats and options (`format` is one of `html`, `gif`, `video`, `lottie`, `sprite_sheet`, `png_sequence`, `png`, `svg`, `audio`); `file.publish` writes the enabled formats and returns the report. Output names are relative to the document's folder and `{name}` expands to the document name (`crates/engine/src/publish.rs`; ADR 0060).

**Shortcuts.** The registry stores `Ctrl+…`; macOS renders ⌘ and the Apple modifier order (`src/platform.rs` `shortcut_label`). Common defaults: `Ctrl+N/O/S`, `Ctrl+Z`/`Ctrl+Y`, `F5` insert frame, `F6` keyframe, `F7` blank keyframe, `F8` convert to symbol, `Ctrl+F` Find, `Ctrl+Enter` Test Movie, `F1` shortcut editor, `Ctrl+K` command palette, `Shift+F12` Publish. `references/commands.md` lists all 52 registry shortcuts; the in-app editor can rebind everything and only stores changes (`src/keymap.rs`, `src/dialogs.rs`).

## Working with an AI agent

**Legitimate work around AniCraft**

* **Discover, don't guess.** Call `anicraft_commands` (MCP) or `anicraft-cli commands`, filter by words, and use the real id and params. Command ids and param keys are stable English even when the UI is translated (`crates/engine/src/lib.rs`; `docs/mcp.md`).
* **Drive the headless engine**, not the GUI: `exec`/`run` for batch edits, `serve` for a long-lived session, `mcp` for interactive tool use. Every edit is undoable, validated and subject to the same confirmations as the app.
* **Prepare inputs**: convert artwork to SVG, images to PNG/JPEG, audio to WAV/Ogg/MP3; keep SVG simple (the importer reports unsupported soft masks, per-character positions and text on a path). Build `.fla`/`.xfl` fixtures only from public format knowledge and treat imports as untitled.
* **Inspect documents**: `.anicraft` is plain JSON (`format`, `version`, `document`, plus shared `paths`). Read it, but prefer commands for edits; if you rewrite it by hand, preserve the envelope and validate by reopening with `info` (`crates/engine/src/format.rs`).
* **Verify output** by rendering a PNG and looking at it (`anicraft_render` returns the image; `render` writes one), and by checking exported file sizes, frame counts and dimensions — not by trusting a zero exit code alone.
* **Extend safely** with `.wasm` plug-ins: a plug-in runs in a sandbox, cannot touch `file.*`, `plugin.*`, the clipboard or undo/redo, and its whole run is one undo step (`crates/engine/src/cmds_plugin.rs` `plugin_may_call`; `docs/plugins.md`). Load it headless with `--plugins`.

**What not to attempt**

* **Do not drive the GUI blind.** No accessibility-driven clicking, no synthetic mouse/keyboard into the window, no relying on panel positions. There is no GUI automation API; the supported surfaces are the CLI, `serve`, MCP and the command registry.
* **Do not promise SWF, full ActionScript, or Animate-grade XFL fidelity.** See the limitations above; unsupported features are reported, not silently emulated.
* **Do not assume Animate semantics** for menus, shortcuts or file behaviour. Menu paths, shortcut labels and format support come from this repo, not from Adobe documentation.
* **Do not edit the user's only copy.** Work on a copy or `--save` a new path, especially for `.fla` imports and publish outputs; `file.save`/exports can overwrite when paths collide.
* **Do not use `--screenshot` as headless verification.** It is a desktop-app flag (the CLI delegates to the GUI binary); launching the GUI is outside this skill's workflow (`crates/cli/src/main.rs`, `src/main.rs`).
* **Do not run plug-ins from untrusted sources** just because the sandbox exists: a plug-in can still edit the open document (one undo step) and read a compact document view.

**A safe agent loop**

1. `anicraft-cli info --sample` (or the user's file) to learn stage, scenes, layers and revision.
2. `anicraft-cli commands` → choose ids and exact params; never invent flags.
3. `anicraft-cli exec … --save work.anicraft` for one edit, or `run` a script for several; stop on the first error.
4. `anicraft-cli render work.anicraft --frame N --out check.png` and inspect the picture.
5. `anicraft-cli info work.anicraft` to confirm the document changed as intended.
6. Export with `gif`/`file.export_*`/`file.publish`; check the files; keep the working `.anicraft` as the source of truth.

## Verification protocol

1. **Pin the version first.** Run `anicraft-cli --version` and `AniCraft --version`; this skill describes 0.2.1. A different build may have different commands, formats or fixes.
2. **Do a throwaway round trip** before touching real work: `new --out test.anicraft` → `exec test.anicraft draw.rect '{"x":10,"y":10,"w":50,"h":50}' --save test.anicraft` → `info test.anicraft` → `render test.anicraft --frame 1 --out check.png` → inspect the PNG → `gif test.anicraft --out check.gif` → open the GIF elsewhere. This catches silent no-ops and wrong frame bases.
3. **Check both frame bases explicitly.** Pass `--frame 1` to the CLI for the first frame; pass `"frame": 0` to commands/MCP for the same frame. An off-by-one is the most common automation bug here.
4. **Never trust a silent export.** Confirm the file exists and is non-trivial; check PNG magic/dimensions, GIF frame count/timing, SVG root and dimensions, HTML page size, Lottie JSON parses, WAV sample rate/duration. Exports return JSON; read it (`file.export_*` results).
5. **Read the import report.** Opening `.fla`/`.xfl` returns `report`, `skipped`, `kept`, `runs` and `missing_fonts`. Treat reported items as absent; do not assume they survived (`crates/engine/src/cmds_file.rs` `open`).
6. **Keep the native file.** Save `.anicraft` before and after risky exports; exports are derived artefacts. Recovery autosave is a crash aid, not a backup, and it does not keep undo history (`docs/roadmap.md`; ADR 0015).
7. **Version the project, not just the app.** Format v3 opens v1/v2, but an older AniCraft refuses a file written by a newer one (`crates/engine/src/format.rs`). Archive the `.anicraft` with the exported media per session, and keep the app version that produced it.
8. **Update between projects.** The app is early alpha and each release moves commands and formats; finish and archive a project, then update, then re-run step 2 on a copy.

## Sources & evidence

* Repo: https://github.com/storytold/anicraft — tag **v0.2.1**, commit **`d0beaf253274948b55ee9e1107749f9491bff880`**, inspected **2026-11-12**.
* Installed bundle audited: `/Applications/AniCraft.app` — version **0.2.1**, bundle id `ai.storyteller.anicraft`, universal (x86_64 + arm64), Developer ID-signed with a stapled notarization ticket; CLI version `anicraft-cli 0.2.1`.
* Key files read: `Cargo.toml`, `README.md`, `AGENTS.md`, `CHANGELOG.md`, `docs/roadmap.md`, `docs/mcp.md`, `docs/plugins.md`, `docs/web.md`, `docs/localisation.md`, `docs/accessibility.md`, `docs/adr/README.md` and ADRs 0004, 0016, 0019, 0024, 0028, 0036, 0040, 0052, 0054, 0055, 0056, 0057, 0058, 0059, 0060.
* Code: `crates/engine/src/{lib,format,confirm,history,params,find,explorer,publish,recovery,cmds_file,cmds_timeline,cmds_library,cmds_plugin,cmds_sound,cmds_actions}.rs`; `crates/cli/src/{lib,main,mcp}.rs`; `crates/doc/src/{lib,easing,filter,color_effect,publish,nine_slice,camera,armature,player,sound}.rs`; `crates/plugins/src/`; `crates/actions/src/as3/`; `crates/audio/`; `crates/gpu/`; `src/{main,app,platform,start,recent,drop,autosave,test_movie,i18n/mod}.rs`; `scripts/build-web.sh`.
* Live evidence: `anicraft-cli --version`, `--help`, `commands` (240), `info --sample`, and an MCP `initialize` + `tools/list` exchange (5 tools, protocol 2025-06-18). No GUI launch, build or export write was performed.
* Count methods, the claim-by-claim evidence table and the doc-drift log are in `evidence.md`; this round's corrections and gaps are in `CHANGES.md`; full CLI/MCP details are in `references/cli.md`; the namespace, shortcut and recipe tables are in `references/commands.md`.
