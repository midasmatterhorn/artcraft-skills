# AniCraft — evidence and count methods (round 2026-11-12)

Audit basis: tag **v0.2.1**, commit `d0beaf253274948b55ee9e1107749f9491bff880`, inspected
**2026-11-12**. Installed bundle: **AniCraft 0.2.1**, bundle id `ai.storyteller.anicraft`.
Live replies: `AniCraft --version` → `AniCraft 0.2.1 (early alpha)`; `anicraft-cli --version`
→ `anicraft-cli 0.2.1`. Previous skill: **none** (first audit).

Status vocabulary: **implemented** = code path exists and is wired into the app/CLI/MCP;
**partial** = exists but visibly incomplete (the missing part is named); **not implemented** =
absent from code; **drift** = documentation contradicts the code.

## Claim → evidence

| # | Claim | Evidence (repo-relative) | Status |
|---|---|---|---|
| 1 | The engine exposes **240 commands in 33 namespaces**; 52 have default shortcuts, 165 mutate the document | `crates/engine/src/lib.rs` (`commands()`, 35 `specs()` groups); `crates/engine/src/cmds_file.rs`, `cmds_timeline.rs`, `cmds_draw.rs`, `cmds_library.rs`, `cmds_plugin.rs`, `cmds_sound.rs`, `cmds_actions.rs`, `find.rs`, `explorer.rs`, `publish.rs`, `merge.rs`, `multi.rs`, `onion.rs`; measured from `anicraft-cli commands` | implemented |
| 2 | Every operation is a command with checked params; `edit.undo`/`redo` cover edits | `crates/engine/src/lib.rs` (`Session::execute`), `crates/engine/src/history.rs`, `crates/engine/src/params.rs` | implemented |
| 3 | Irreversible actions refuse without `"confirm": true`; tiered confirmations live in the engine | `crates/engine/src/confirm.rs`; `docs/adr/0004-destructive-actions.md` | implemented |
| 4 | **5 MCP tools** over **3 protocol revisions** (2025-06-18, 2025-03-26, 2024-11-05), stdio JSON-RPC | `crates/cli/src/mcp.rs` (`PROTOCOLS`, `tools()`); live `initialize` + `tools/list` returned 5 tools and serverInfo `anicraft` 0.2.1 | implemented |
| 5 | **11 CLI subcommands** plus `help`/`--version`: `info`, `render`, `render-seq`, `gif`, `commands`, `run`, `exec`, `new`, `bench`, `serve`, `mcp` | `crates/cli/src/lib.rs` (`USAGE`, `run()`), `crates/cli/src/main.rs`; `anicraft-cli --help` | implemented |
| 6 | `.anicraft` is versioned JSON, **format v3**, opens v1/v2, refuses newer versions | `crates/engine/src/format.rs` (`FORMAT_NAME`, `FORMAT_VERSION = 3`; v1/v2 tests) | implemented |
| 7 | Opens Adobe Animate `.fla` and `.xfl` (folder) as an **untitled import**, so Save never overwrites the source | `crates/engine/src/cmds_file.rs` (`is_animate`, `open`), `crates/xfl/`; `docs/adr/0009-xfl-import.md`, `docs/adr/0054-fla-packages-and-a-hardened-zip-reader.md` | implemented, fidelity partial (see #8) |
| 8 | XFL gaps: no motion tweens, armatures, camera, per-character styles; no self-extracting/top-folder `.fla`, encrypted archives, sound/video items | `docs/roadmap.md` (M4 row); `docs/adr/0016-motion-tweens.md` (Not yet); `docs/adr/0054-fla-packages-and-a-hardened-zip-reader.md` (Not in this slice) | partial |
| 9 | Imports SVG drawings, PNG/JPEG images, WAV/Ogg/MP3 sounds to the stage | `crates/engine/src/cmds_file.rs` (`file.import`), `crates/svg/`, `crates/engine/src/cmds_sound.rs` (`is_sound`), `crates/engine/src/cmds_drop.rs` | implemented |
| 10 | Exports PNG, PNG sequence, SVG, animated GIF, sprite sheet + JSON, Lottie, self-contained HTML canvas, MP4/WebM, WAV | `crates/engine/src/cmds_file.rs` (`file.export_*`), `crates/engine/src/publish.rs`; `docs/roadmap.md` Files row | implemented |
| 11 | Video export uses the **user's ffmpeg**; no encoder is bundled | `file.export_video` params in `crates/engine/src/cmds_file.rs`; `ANICRAFT_FFMPEG`; `docs/adr/0026-packaging-and-signing.md`, `docs/legal/compliance.md` | implemented with external dependency |
| 12 | **Publish** writes **9 formats** from in-document settings, with a background run in the app and a report headless | `crates/doc/src/publish.rs` (`PublishFormat::ALL` = 9), `crates/engine/src/publish.rs`, `src/publish_panel.rs`; `docs/adr/0060-publish-settings-and-publish.md` | implemented, first slice (gaps in #13) |
| 13 | Publish gaps: no `PublishSettings.xml` import, extra placeholders, outputs outside the document folder, progress for HTML/Lottie/audio, preset files | `docs/adr/0060-publish-settings-and-publish.md` (Not yet) | partial |
| 14 | Timeline: scenes, layers and folders, guide/motion-guide/mask layers, keyframes, classic/shape/motion tweens, easing, onion skin, multi-frame editing | `crates/doc/src/lib.rs`, `eval.rs`, `motion.rs`, `easing.rs`; `crates/engine/src/cmds_timeline.rs`, `cmds_frames.rs`, `multi.rs`; `src/onion.rs`; ADRs 0011, 0016, 0023, 0030, 0047, 0051 | implemented (motion tweens first slice) |
| 15 | Motion-tween gaps: no key dragging in time, eased presets with strengths, 3D, Split Motion, Lottie property curves, XFL motion-tween import | `docs/adr/0016-motion-tweens.md` (Not yet) | partial |
| 16 | Drawing: Pen/Subselection/Pencil, rectangle/oval/polystar/line, merge drawing, Paint Bucket/Ink Bottle, Brush, Eraser, Eyedropper, width tool, text | `crates/engine/src/cmds_draw.rs`, `cmds_path.rs`, `cmds_raw*.rs`, `cmds_brush.rs`, `cmds_erase.rs`, `cmds_paint.rs`, `cmds_width.rs`, `cmds_text.rs`; `crates/geom/src/planar.rs`; ADRs 0012, 0018, 0031–0034, 0041–0046 | implemented (per-tool gaps named in `docs/roadmap.md`) |
| 17 | Symbols: graphic/movie clip/button, nested timelines, **9-slice scaling**, filters, blend modes, colour effects | `crates/doc/src/nine_slice.rs`, `filter.rs`, `color_effect.rs`, `lib.rs` (`BlendMode`); `crates/engine/src/cmds_library.rs`, `symbol.set_scale_grid`; ADRs 0055, 0056 | implemented first slice |
| 18 | 7 filter kinds and 14 blend modes; 5 colour-effect styles including None | `crates/doc/src/filter.rs` (`Filter` variants); `crates/doc/src/lib.rs` (`BlendMode`); `crates/doc/src/color_effect.rs` (`ColorStyle::ALL`) | implemented |
| 19 | Bones/IK and a camera layer | `crates/doc/src/armature.rs`, `camera.rs`; `crates/engine/src/cmds_bone.rs`, `cmds_camera.rs`; ADRs 0027, 0043; `docs/roadmap.md` M7 | partial (first slice; limits in roadmap) |
| 20 | Sound: WAV/Ogg/MP3 import, waveforms, envelopes, layer volume/mute, sounds in symbols, button-state sounds, WAV export | `crates/audio/`, `crates/doc/src/sound.rs`, `crates/engine/src/cmds_sound.rs`; ADRs 0020, 0039, 0057 | implemented first slice |
| 21 | Timeline actions, frame scripts, a pure player, Test Movie and HTML runtime export | `crates/actions/`, `crates/doc/src/player.rs`, `crates/engine/src/cmds_actions.rs`, `cmds_script.rs`, `src/test_movie.rs`; ADRs 0024, 0028, 0052 | implemented, ActionScript subset (see #22) |
| 22 | ActionScript support is a bounded subset; arrays, `switch`, `for in`/`for each`, objects, closures, `try` are refused with a located message | `crates/actions/src/as3/lower.rs` (e.g. "arrays aren't supported yet", "switch statements aren't supported yet"); `docs/adr/0052-actionscript-small-logic.md` | partial |
| 23 | Find and Replace plus Movie Explorer, headless as `find.*` and `explorer.tree` | `crates/engine/src/find.rs`, `explorer.rs`, `src/find_panel.rs`, `src/movie_explorer.rs`; ADR 0058 | implemented first slice |
| 24 | Desktop drops, Open Recent and a start screen | `crates/engine/src/cmds_drop.rs`, `cmds_recent.rs`, `src/drop.rs`, `src/recent.rs`, `src/start.rs`; ADR 0059 | implemented first slice (gaps in ADR) |
| 25 | Crash-recovery autosave with session locks and restore/discard | `crates/engine/src/recovery.rs`, `src/autosave.rs`; ADR 0015 | implemented |
| 26 | GPU stage is the default stage renderer with CPU fallback; **exports use the CPU oracle** | `Cargo.toml` (default features `gpu-stage`, `sound-output`), `crates/gpu/`, `crates/render/`; ADRs 0019, 0029, 0032, 0048 | implemented |
| 27 | Web build: same program for `wasm32-unknown-unknown`, WebGL2, CPU stage | `scripts/build-web.sh`, `scripts/build-web.ps1`, `src/web.rs`, `docs/web.md`; ADR 0036 | partial (not hosted; browser gaps) |
| 28 | Web gaps: no sound in the editor, no GPU stage, no video export, no plug-in installs, no zipped PNG sequence, no IndexedDB/threads, not browser-verified | `docs/roadmap.md` Platforms row; `docs/web.md` | partial |
| 29 | WebAssembly plug-ins: ABI v1, `wasmi` sandbox, fuel/memory/wall-time/request limits, one undo step per run | `crates/plugins/src/lib.rs`, `runtime.rs` (`Limits`), `crates/engine/src/cmds_plugin.rs` (`plugin_may_call`), `docs/plugins.md`; ADR 0017 | implemented first slice |
| 30 | Interface strings are keyed for translation, with a pseudo-locale; **no AniCraft catalog is shipped**, so 0.2.1 is English-only | `src/i18n/mod.rs` (`READY` has 35 codes; `Pseudo`), `build.rs` (`CRAFT_I18N_DIR` optional), `docs/localisation.md` | partial |
| 31 | Accessibility first pass: AccessKit names/roles, panel focus keys, high-contrast theme, 75–200 % scale | `src/a11y.rs`, `docs/accessibility.md`; ADR 0022 | partial (stage items not exposed) |
| 32 | One document per window; no tabs/multi-document | `docs/roadmap.md` (Ease of use row: "Not yet: several open documents"); `docs/adr/0059-files-from-the-desktop-recent-files-and-start-screen.md` (Not yet) | not implemented |
| 33 | No SWF import or export; SWF bytecode not planned | `docs/roadmap.md` M6 row; `docs/requirements.md` lists SWF only as optional; no command or module implements it | not implemented |
| 34 | Native document is plain JSON and can be read/rewritten by an agent, but must keep `format` + `version` + `document` and pass validation | `crates/engine/src/format.rs` | implemented |
| 35 | Test suite size: **1,088 `#[test]` functions** vs "133 tests" in `docs/roadmap.md` | `grep -rho '#[test]' --include='*.rs'`; `docs/roadmap.md` Tests row | drift |
| 36 | Installed bundle and version | bundle `Info.plist` (`0.2.1`, `ai.storyteller.anicraft`); `codesign -dv` (universal x86_64+arm64, Developer ID, notarization ticket stapled); `AniCraft --version` → `AniCraft 0.2.1 (early alpha)`; `anicraft-cli --version` → `anicraft-cli 0.2.1` | implemented / verified live |

## Count methods

All counts are at commit `d0beaf253274948b55ee9e1107749f9491bff880`, 2026-11-12. The installed
`anicraft-cli` 0.2.1 is the primary live instrument; source is the tie-breaker.

| Quantity | Method | Result |
|---|---|---|
| Engine commands | `anicraft-cli commands` → parse the JSON array | **240** |
| Command namespaces | Group the same JSON by the id before the first `.` | **33** |
| Commands with default shortcuts | Count entries whose `shortcut` is non-null | **52** |
| Mutating commands | Count entries whose `mutates` is true | **165** |
| Command registry groups | Count `v.extend(…::specs())` calls in `commands()` (`crates/engine/src/lib.rs`) | **35** |
| MCP tools | Live `initialize` then `tools/list` on `anicraft-cli mcp`; also `tools()` in `crates/cli/src/mcp.rs` | **5** |
| MCP protocol revisions | `PROTOCOLS` constant; live `initialize` reply | **3** (2025-06-18, 2025-03-26, 2024-11-05) |
| CLI subcommands | Read `USAGE` and `run()` match arms; cross-check `anicraft-cli --help` | **11** functional + `help`/`--version` |
| Publish formats | Length of `PublishFormat::ALL` | **9** |
| Filter kinds | Variants of `Filter` in `crates/doc/src/filter.rs` | **7** |
| Blend modes | Variants of `BlendMode` in `crates/doc/src/lib.rs` | **14** |
| Colour-effect styles | Length of `ColorStyle::ALL` | **5** (4 effects + None) |
| Easing presets | Length of `Easing::PRESETS` | **8** |
| Native format version | `FORMAT_VERSION` in `crates/engine/src/format.rs` | **3** |
| Crates | Entries under `crates/` | **13** |
| ADRs | `docs/adr/*.md` minus `README.md` | **59** |
| Tests | `grep -rho '#\[test\]' --include='*.rs' .` | **1,088** attributes |
| Locales marked ready | Length of `READY` in `src/i18n/mod.rs` | **35** codes, no shipped AniCraft catalog |
| Sample document | `anicraft-cli info --sample` | 1280×720, 24 fps, 48 frames, 5 layers, 2 library items, 1 scene |

## What was re-measured, carried forward, or found drifted

* **Re-measured at v0.2.1:** all rows in the count table above, the import/export matrix, the
  confirmation rule, the MCP frame base (0-based), the CLI frame base (1-based), and the
  installed-bundle version lines.
* **Carried forward:** nothing from an earlier AniCraft skill (none existed). Within the code,
  the MCP tool set and protocol revisions are **unchanged at v0.2.1** (5 tools, 3 revisions) and
  were verified live anyway.
* **Doc drift (code wins):**
  1. README "What's missing" lists audio layers and a GPU renderer; both ship in 0.2.1
     (`crates/audio/`, `crates/gpu/`, `Cargo.toml` default `gpu-stage`).
  2. README workspace map lists 9 crates and omits `actions`, `audio`, `gpu`, `plugins`; its
     CLI line omits `gif` and `bench`.
  3. `docs/roadmap.md` says "133 tests"; there are 1,088 `#[test]` attributes.
  4. `docs/roadmap.md` interactivity row says "Not yet: … keyboard events, variables" while
     ADR 0052 and `crates/actions/src/as3` implement typed variables and keyboard listeners.
  5. `docs/requirements.md` lists SWF export as optional P1; `docs/roadmap.md` says SWF
     bytecode is not planned and no code path exists.
  6. `docs/roadmap.md` says macOS/Linux CI runners are missing and the build was "verified on
     Windows only"; a signed macOS 0.2.1 bundle is installed on this machine. The skill
     describes the audited macOS bundle without claiming broad macOS verification.
* **Delta attribution caveat:** the checkout is a single-commit shallow tag, so v0.2.0 cannot
  be diffed. The delta paragraph attributes ADR 0052 and 0055–0060 surfaces to v0.2.1 from the code and
  ADR files present at the tag plus `CHANGELOG.md`; every named path was opened.

## Repo files read for this audit

`README.md`, `AGENTS.md`, `Cargo.toml`, `CHANGELOG.md`, `docs/roadmap.md`, `docs/mcp.md`,
`docs/plugins.md`, `docs/web.md`, `docs/localisation.md`, `docs/accessibility.md`,
`docs/requirements.md`, `docs/adr/README.md`, and ADRs 0004, 0009, 0016, 0019, 0024, 0026,
0028, 0035, 0036, 0039, 0040, 0043, 0052, 0054, 0055, 0056, 0057, 0058, 0059, 0060.
Source: `crates/engine/src/{lib,format,confirm,history,params,find,explorer,publish,recovery,cmds_file,cmds_timeline,cmds_draw,cmds_library,cmds_plugin,cmds_sound,cmds_actions}.rs`,
`crates/cli/src/{lib,main,mcp}.rs`, `crates/doc/src/{lib,easing,filter,color_effect,publish,nine_slice,camera,armature,player,sound}.rs`,
`crates/plugins/src/{lib,runtime}.rs`, `crates/actions/src/as3/{lower,parse}.rs`,
`crates/audio/Cargo.toml`, `src/{main,app,i18n/mod,platform,start,recent,drop,autosave,test_movie}.rs`,
`scripts/i18n-extract.sh`, `scripts/build-web.sh`.

## Live, read-only probes performed

* `AniCraft --version` → `AniCraft 0.2.1 (early alpha)` (the binary returns before opening a
  window; `src/main.rs`).
* `anicraft-cli --version` → `anicraft-cli 0.2.1`.
* `anicraft-cli --help` → the 11-subcommand usage block.
* `anicraft-cli commands` → 240 commands, 33 namespaces, 52 shortcuts, 165 mutating.
* `anicraft-cli info --sample` → sample stage/frames/layers/library.
* `anicraft-cli mcp` with `initialize` + `tools/list` on stdin → 5 tools, protocol 2025-06-18.

No GUI launch, no build, no test execution, no export writes.
