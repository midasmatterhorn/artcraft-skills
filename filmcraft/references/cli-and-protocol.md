# FilmCraft CLI, control channel and MCP — reference

Transcribed from the **v0.14.0** source, commit `a2d8e9ce269aba9c399e36262522e11456df6fbf` (inspected 2026-10-29).
Every flag, tool and method below exists in the code; where a value comes from a doc rather than code, the
path is given. Changes since v0.13.0 are marked **New in 0.14.0** — this wave added no command, CLI
subcommand, MCP tool or control method; it changed behaviours (`effects.apply` answers applied
instances, `effects.setParam` names the parameter and accepted value, exports gained `maxThreads`,
H.264 export got faster) and the shared-module refactor moved declarations without changing the surface.

## 1. `filmcraft-cli`

Source of truth for the flags: the `HELP` const in `apps/filmcraft-cli/src/main.rs:63-145`; dispatch at
`:317-520`. Parser: `apps/filmcraft-cli/src/args.rs` (options may appear anywhere; `--` ends options;
`-V` in the subcommand position is a version query). `filmcraft-cli --version` prints `filmcraft-cli 0.13.0`.

Count unchanged at **11 functional subcommands**, i.e. **12 subcommand words** counting `help` (`-h`; `--version` in the subcommand position also works):

```
filmcraft-cli [OPTIONS] <SUBCOMMAND> [ARGS]

SUBCOMMANDS
  exec <id> [key=value ...]     run one command; prints its result as JSON
  exec <id> '<json params>'     same, params as one JSON object
  run <script.jsonl | ->        commands, one {"id","params"} per line (# comments ok), in order:
                                file.exportMedia waits for its file before the next line and before
                                exit unless its params say "wait": false
  commands [filter] [--json]    list commands (id, label, shortcut, params)
  describe <id>                 one command as JSON (menu, shortcut, params, enabled now)
  inspect [project|sequence]    project tree or active sequence as JSON (default: both)
  import <file>...              import media into the project
  export <out> [--preset name] [--format f] [--range r] [--start s --end s] [--settings json]
         [--gpu-rendering auto|off] [--scale f] [--quality 0-100] [--no-audio] [--queue] [--allow-offline]
  export --list-presets [query] list export presets (name, category, format) as JSON
  render --seconds S --out f.png [--scale 0.5] [--allow-offline]
  probe <media> [--image-sequence]      media info as JSON (MXF/Ogg/BWF/image-sequence details)
  bench-decode <media> [--frames N]
  mcp                                   MCP server on stdio (headless, or --bridge)
  help | --version

OPTIONS
  --project <cut.fcproj>   open this project first (headless)
  --demo                   open the built-in demo project (headless)
  --save                   save the project back to --project when done
  --save-as <cut.fcproj>   save to this path when done
  --bridge <127.0.0.1:PORT>  send commands to the running app (`filmcraft --control PORT`)
  --data-dir <dir>         FilmCraft data directory for user export presets (headless)
  --keep-going             `run`: report failing lines and continue
  --compact                one-line JSON output
```

Notes (all verified in code):

- `export` writes through `file.exportMedia` with `wait: true` (or `export.queue.add` with
  `start: true, wait: true` for `--queue`), then prints the result and a stderr line
  `exported <paths> in <s>s` (`apps/filmcraft-cli/src/main.rs`).
- The local backend forces `wait: true` on the long commands (`LONG_COMMANDS = ["file.exportMedia"]`,
  `crates/automation/src/long_job.rs:18`) — for `exec` and for every line of `run` — unless the params
  contain exactly `"wait": false`. The process exits after the command, so a background export would
  never be written (#2342). A `wait: false` export from a one-shot local process can be lost; use it only
  with `--bridge` or while something keeps the process alive.
- `--format` resolves through `Format::from_name` (`crates/export/src/lib.rs:160-200`):
  `h264|hevc|av1|prores|dnxhr|apv|mjpeg|mxf-op1a|mxf-opatom|png|tiff|bmp|jpg|tga|dpx|exr|gif|wav|aiff|aac|flac`
  plus aliases (`mp4`, `mov`, `dnx`, `mxf`, `opatom`, `jpeg`, `targa`, `openexr`…). Without `--format`,
  `--preset` wins; otherwise the format is guessed from the extension (`format_for`,
  `apps/filmcraft-cli/src/main.rs:237-252`): `mp4|m4v`→h264, `mov`→prores, `mxf`→mxf-op1a, `png`, `gif`,
  `wav`, `tif|tiff`→tiff, `bmp`, `aif|aiff`→aiff, `m4a|aac`→aac. An unknown extension without `--format`
  is a usage error. **The `HELP` text abbreviates the list** (it omits jpg/tga/dpx/exr/flac) — the enum is
  authoritative.
- `--start`/`--end` imply `range: "custom"` and are forwarded as `startSeconds`/`endSeconds`;
  `--range entire|inOut|workArea`. **New in 0.13.0:** `workArea` now works as soon as the sequence has a
  work area (`sequence.workAreaBar`, `sequence.setWorkArea*`), and errors with "the sequence has no work
  area" otherwise (`crates/engine/src/export_tools.rs:355`, `crates/engine/src/work_area_tests.rs`).
  `--no-audio` sets `audio: false`; `--settings` is ExportSettings JSON merged over the preset;
  `--gpu-rendering` sets `gpuRendering` (`off|auto`).
- Values in `key=value` parse as JSON when possible (`3.5`, `true`, `[1,2]`, `{"a":1}`), else strings;
  dotted keys nest (capped at 64 levels). Numeric options (`--seconds`, `--scale`) must be finite, so a typo
  is a usage error, not a silent default (`finite_opt`, `apps/filmcraft-cli/src/main.rs:587-595`).
- Exit status: `0` success; `1` a command failed, saving failed, or an export/render drew offline media
  without `--allow-offline`; `2` usage error. A closed stdout (`| head`) is not an error.
- `--bridge` refuses `--project`/`--demo`: open projects in the app instead (`exec file.open path=…`).
  **New in 0.13.0:** the bridge sends `FILMCRAFT_CONTROL_TOKEN` (inherited from the environment) as the
  `token` on every request; without it the desktop refuses the connection (`crates/automation/src/bridge.rs`).
- `render` is headless-only; with `--bridge` use the MCP `render_frame` tool or `exec ui.*` commands.
- `mcp` accepts only `--bridge`, `--project`, `--demo`, `--data-dir`; any other option is a usage error.
- `probe` needs `--image-sequence` to treat its argument as the first numbered still of a sequence.
- File reads/writes in the CLI now run on a blocking pool (`read_file`/`read_text`/`write_file`,
  `apps/filmcraft-cli/src/main.rs:140-157`), so a slow disk does not stall the async runtime.

## 2. Desktop control channel

`filmcraft --control 9876` (or `FILMCRAFT_CONTROL_PORT=9876`) — loopback only, one JSON object per line in,
one JSON reply per line out. Transport `apps/filmcraft/src/control_server.rs`; handlers
`crates/ui-egui/src/control.rs`; full table `docs/control-protocol.md`.

**New in 0.13.0 — authentication is mandatory.** The listener stays closed unless
`FILMCRAFT_CONTROL_TOKEN` is exactly 64 hex characters; every request must carry the same value as a
top-level `token` string, compared in constant time. A missing or wrong token answers
`{"ok": false, "error": "control authentication failed; closing the connection"}` and closes the connection
*before* any request is dispatched (`apps/filmcraft/src/control_server.rs:31-41,130-141`).

```sh
export FILMCRAFT_CONTROL_TOKEN="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
filmcraft --control 9876 &
filmcraft-cli mcp --bridge 127.0.0.1:9876
```

Limits: 4 MiB per request line, 16 concurrent connections (further ones get an error line), 120 s read/write
timeout per connection (expiry closes silently, so pooled clients must reconnect; the bridge does), 60 s wait
for a UI reply (`MAX_LINE`/`MAX_CONNECTIONS`/`CONNECTION_TIMEOUT`,
`apps/filmcraft/src/control_server.rs:24-28`, reply timeout `:101`).

**23 methods** (handler ids in `crates/ui-egui/src/control.rs`):

| Method | Params | Notes |
|---|---|---|
| `engine.execute` / `ui.menu.invoke` | `{command, params}` | any engine or UI command id |
| `engine.commands` / `ui.menu.list` | – | command registry / UI menu tree |
| `ui.inspect` | – | tool, workspace, dock, timeline view, playback, fps, settings draft, panels, `keyboardFocus`, `input`… |
| `ui.elements` | `{prefix?}` | every on-screen interactive element: id, label, rect |
| `ui.set` | `{tool, workspace, mode, theme, focused, playbackRes, timeline:{pps,scroll,fit,thumbnails}, program:{…}, source:{…}, clipDialog:{…}, menuDialog:{…}, panels:{…}, export:{…}, keyframeSelection:[…], projectPanel:{…}, mediaBrowser:{…}, settings, gfxTemplates, tts}` | merges into UI state |
| `ui.panel.show` / `ui.panel.close` | `{panel}` | |
| `ui.click` / `ui.move` | `{id}` or `{x,y}`, `button`, `count`, `modifiers` | synthetic pointer input; click `count` is an integer 0–10 (default 1; 0 queues no click); `ui.move` ignores it |
| `ui.drag` | `{from, to, steps, modifiers}` | press–move–release; `steps` 0–1024 (default 12; 0 or 1 uses 2). Out-of-range or non-integer values return an error before any input is queued (`crates/ui-egui/src/control.rs:28-45,338-380`) |
| `ui.scroll` | `{id|x,y, dx, dy, modifiers}` | wheel/trackpad |
| `ui.key` / `ui.type` | `{key}` (`Cmd+K`, `Space`) / `{text}` | keyboard |
| `ui.timeline.hit` / `ui.timeline.locate` | `{x,y,modifiers?}` / `{clip, edge?}` | hit-testing; `kind` is the trim a press would start; **New in 0.13.0:** on the ruler it reports `ruler`, or `workArea` with the bar's `edge` |
| `ui.playback` | `{action: play\|stop\|toggle, speed?}` | |
| `ui.screenshot` | `{path?, panel?}` | PNG of the window or one panel; fails after 10 s with no presented frame |
| `ui.resize`, `app.quit` | `{width,height}` / `{}` | `app.quit` (control method) quits without the save prompt; the **command** `app.quit` asks first |
| `ui.focus` | `{}` / `{id}` | `{}` activates the OS window; `{id}` focuses a widget (reply acknowledges; `ui.inspect.keyboardFocus` reports the actual focus) |
| `perf.stats` | – | decode/playback/frames/monitor/ui/process counters (cumulative — diff two readings) |

Rules of thumb (`docs/control-protocol.md`):

- A line that is not a JSON object with a string `method` gets one error reply and the connection is
  closed (also for invalid UTF-8 and lines over 4 MiB — an HTTP request cannot smuggle a command in).
- Commands that act on a selection are disabled until something is selected, unless you name targets
  (`clips`/`clip`, `items`/`item`); naming targets leaves the selection alone.
- Tracks are ids or names (`"V1"`, `"A2"`); naming a missing track is an error, never a fallback track.
- `ui.elements` describes the last rendered frame; after a layout change, retry on the next frame.
- Started with `--control`, the app opens without activating itself and UI requests bring the window forward
  without making it key; only `ui.focus {}` activates it. `--control-input-only` (needs `--control`) ignores
  real keyboard, pointer, file drops and menu commands except window close/quit.

## 3. MCP server

`filmcraft-cli mcp` (stdio). Headless: `--demo` or `--project cut.fcproj` (neither = empty project), plus
`--data-dir`. Bridge: `--bridge 127.0.0.1:9876` to the running app (requires the token in the environment).
`.mcp.json` registers both, pointing at `target/release/filmcraft-cli`.

Tools — **17**, unchanged from v0.11.0 (`crates/automation/src/server.rs`, `#[tool_router]` impl; names are
the handler names):

| Tool | Mode | Purpose |
|---|---|---|
| `command_list` | both | every command: id, label, menu, shortcut, params, enabled now (`filter`, `enabled_only`) |
| `command_run` | both | run one command `{id, params}`; edits are undoable |
| `command_batch` | both | `{steps:[{id,params?}], stop_on_error?}` → `{completed, failed, results}` |
| `doc_inspect` | both | project tree + active sequence in one call |
| `render_preview` | both | same as `render_frame` |
| `project_inspect` | both | bins and items with ids, types, durations; active sequence |
| `sequence_inspect` | both | tracks, clips (`start`/`end`, `sourceIn`/`sourceOut`, `speed`, `reverse`, `gainDb`), effects, transitions, markers, playhead, selection |
| `media_import` | both | import files by absolute path (`paths`, optional `bin`, `image_sequence`) |
| `render_frame` | both | PNG of the program frame at `seconds` (headless renders; bridge screenshots the Program monitor); read-only |
| `ui_inspect` | bridge | UI state: tool, workspace, panels, zoom, playback, fps |
| `ui_elements` | bridge | on-screen interactive elements with id, label, rect (`prefix` filter) |
| `ui_click` | bridge | click by `id` or `x`,`y`; `button`, `count` (0–10), `modifiers` |
| `ui_drag` | bridge | press–move–release between points or element ids; `steps` 0–1024 |
| `ui_key` | bridge | key or shortcut: `Space`, `Cmd+K`, `Shift+Delete` |
| `ui_type` | bridge | type text into the focused field |
| `ui_screenshot` | bridge | PNG of the window or one `panel` |
| `ui_control` | bridge | call any control-channel method directly (`ui.set`, `ui.scroll`, `ui.timeline.locate`, …) |

Resources: `filmcraft://document`, `filmcraft://commands` (both `application/json`; MCP 2026-07-28 clients
also get `ttlMs`/`cacheScope` on list/read results).

Mode split: `command_*`, `doc_inspect`, `project_inspect`, `sequence_inspect`, `media_import`,
`render_preview`, `render_frame` work headless and bridged; `ui_*` need the bridge (a live window).

Behaviour worth relying on:

- Every tool carries `title` + `readOnlyHint`/`destructiveHint`/`idempotentHint`/`openWorldHint`.
- Unknown tool arguments are `-32602` errors naming the accepted ones; unknown lines are `-32700` and the
  server keeps serving; a panicking command is reported as `internal error: …` and the session stays usable.
- `command_batch` returns `{completed, failed, results}`; each edit is its own undo step.
- `doc_inspect` pins `sequence.inspect` to the `activeSequence` id it just reported, so the pair is consistent
  even if tabs switch mid-call (`crates/automation/src/server.rs:283-300`).
- Long exports: `command_run {"id":"file.exportMedia","params":{…,"wait":true}}` runs as a background job,
  reports `notifications/progress` when the request carried `_meta.progressToken`, and
  `notifications/cancelled` stops the encode, deletes partial output and sends no response. Without `wait`,
  the result is `{job, path, poll: "jobs.list", cancel: "jobs.cancel"}`. `jobs.list` carries `progress`,
  `etaSeconds`, `finished`, `result`; `export.queue.list` lists the Export Queue only.
- **New in 0.13.0:** bridge screenshots are written to a freshly created owner-only temporary directory
  instead of a predictable shared-temp filename (`crates/automation/src/server.rs:567-580`).
- Headless MCP is **not** confined to a folder; any option other than the four above is rejected (exit 2).

Typical agent loop (`docs/agents.md`): `project_inspect` / `sequence_inspect` → ids → `command_run` →
`render_frame` or `ui_screenshot` → inspect → `edit.undo` if wrong.

## 4. Commands worth memorising

Project/media: `file.newProject`, `file.open`, `file.save`/`file.saveAs`/`file.saveCopy`/`file.revert`,
`file.newSequence`, `file.newSequenceFromClip`, `file.import`, `file.importImageSequence`,
`file.listAutoSaves`, `file.recoveryList`, `file.recover`, `file.discardRecovery`, `file.projectManager`,
`media.status`, `media.findMissing`, `media.relink`, `media.autoRelink`, `media.search`, `media.makeOffline`,
`media.linkMedia`, `media.refreshChanged`, `media.createProxies`/`attachProxies`/`toggleProxies`,
`project.ingestSettings`, `project.notes`/`project.setNotes`.

Editing: `source.insert`, `source.overwrite`, `sequence.lift`, `sequence.extract`, `sequence.addEdit`,
`timeline.move`, `timeline.razor`, `timeline.place`, `timeline.setTrack` (name, label, mute, solo, lock),
`edit.undo`, `edit.redo`, `edit.pasteInsert`, `edit.copy`/`edit.cut`/`edit.paste` (clips **or** captions),
`trim.selectEditPoint`, `trim.shuttle`, `trim.tick`, `trim.shuttleStop`, `trim.playAround`,
`clip.replaceFromBin`, `clip.audioGain`, `clip.makeSubclip`, `clip.synchronize`, `clip.mergeClips`,
`clip.sceneEditDetection`, `markers.*`, `markers.exportCsv`.

**New in 0.13.0:** `sequence.workAreaBar`, `sequence.setWorkAreaIn`, `sequence.setWorkAreaOut`,
`sequence.setWorkArea`, `sequence.showDuplicateFrameMarkers`, `sequence.duplicateFrames`,
`history.deleteRedoable`, `history.clear`, `captions.duplicate`, plus the UI-only ids `mixer.showHideTracks`,
`mixer.meterInputOnly`, `view.transparencyGrid`.

Look/audio/text: `effects.list`, `effects.apply`, `effects.setParam` (rejects out-of-range values),
`lumetri.setInputLut`, `lumetri.setLook`, `lumetri.setSection`, `lumetri.applyMatch`, `lut.*`,
`mixer.*`, `clipMixer.set`, `essentialSound.*`, `captions.*`, `transcript.*`, `tts.*`, `graphics.*`
(templates: `graphics.template.*`, `file.exportGraphicsTemplate`).

Output: `file.exportMedia`, `file.exportFrame`, `export.queue.add/start/list/stop/cancel/retry/remove/move/clear`,
`export.quick`, `export.presets.*`, `export.formats` (per-format `available`), `export.resolve`,
`jobs.list`, `jobs.cancel`, `perf.stats`, `file.exportEdl`, `file.exportFcp7Xml`, `file.exportFcpxml`,
`file.exportOtio`, `file.exportAaf`, `file.exportOmf`, `file.exportAle`, `file.importAaf` (also accepts OMF).

UI/app: `tool.*`, `playback.*`, `view.*` (incl. `view.resetInterfaceZoom`, `view.transparencyGrid`),
`window.workspace.*` (9 built-in layouts + reset/saveChanges/saveAs/edit), `window.panel.*`,
`window.dockPanel`, `window.floatPanel`, `window.dockAction`, `app.settings.<category>`,
`prefs.get`/`prefs.set`/`prefs.reset`/`prefs.schema`, `shortcuts.*`, `command.list`.

`file.exportMedia` parameters (registry, `crates/engine/src/commands.rs:1655`):
`path` (required), `preset`, `settings` (ExportSettings JSON), `format`, `audioCodec: auto|aac|pcm|flac`,
`flacLevel` 0–8, `width`, `height`, `fps`, `bitrateKbps`, `bitrateMode: cbr|vbr1Pass|vbr2Pass|crf`, `crf` 0–51,
`hardwareEncoding: off|auto`, `scale`, `audio`, `quality` 0–100, `burnCaptions`, `alpha`,
`exrCompression: none|rle|zips|zip`, `captionSidecar: srt|vtt`, `loudnessLufs`, `proresProfile`,
`dnxProfile`, `apvProfile`, `mxfVideoCodec`, `sequence`, `range: entire|inOut|workArea|custom`,
`startSeconds`, `endSeconds`, `sdr` (tone-map HDR to SDR), `wait` (default **false** at the engine; the local
CLI forces true).

## 5. Building (developers)

```sh
cargo build --release -p filmcraft -p filmcraft-cli   # app + CLI (packaging/macos/package.sh)
cargo run --release -p filmcraft -- --control 9876
cargo xtask ci        # fmt, lints, tests, layering, asset attribution, wasm check, i18n report
cargo xtask web       # WebAssembly site into target/web/dist
cargo xtask parity    # menu/effects parity against a local plan/premiere reference
```

`CRAFT_FONTS_DIR=<craft-fonts checkout>` adds the shared font set (optional; official releases embed it —
`packaging/macos/package.sh`, README "Get started"). Release builds pass no `--features`, so `whisper` and
`neural-voices`/`kokoro` are **off** in shipped binaries.
