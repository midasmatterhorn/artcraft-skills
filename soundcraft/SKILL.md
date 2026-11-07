---
name: soundcraft
description: >-
  SoundCraft is an open-source, pure-Rust digital audio workstation (a clean-room Pro Tools-style
  DAW) for macOS, Windows, Linux, FreeBSD and the browser: multitrack audio and MIDI editing, a
  full mixer with built-in and CLAP/VST3/AU plug-ins, automation, recording, bounce/export, video
  and surround — and every action is a command reachable from the CLI, a JSON control channel and
  an MCP server. Trigger this skill whenever the user mentions SoundCraft (or `.scraft`, `.scraftz`,
  `.scgrp`, `soundcraft-cli`, its control channel/MCP server, or "the SoundCraft app"), asks what it
  can or cannot do, which audio/session/MIDI formats it reads or writes, its keyboard shortcuts, or
  how to launch, script, automate, inspect or troubleshoot it — and equally when they never name it
  but describe the job ("edit this multitrack session", "bounce a mix to WAV", "record takes from my
  interface", "convert audio", "drive a DAW from an agent"). Do not infer SoundCraft behaviour from
  Pro Tools knowledge: read this first.
---

# SoundCraft

**Audit basis.** Refreshed 2026-11-07 against tag **v0.18.0**, commit **`5ff012ab88490cdfc635ee304c1019885e1b880d`** — `git rev-parse HEAD` in the pinned checkout confirms, and the installed SoundCraft 0.18.0 bundle matches: its binary's read-only `--version` prints `soundcraft 0.18.0 (macos aarch64)`. The previous release this skill described was v0.17.0 (`b35dd0f9eb0c08a198c1306021bd138f3a22d87c`).

**v0.17.0 → v0.18.0 delta.** `git diff v0.17.0..HEAD` measures 108 files, +6,468/−554. The engine command-id set is **unchanged at 484**; the UI registry gained two commands (`ui.reduce_visual_effects`, `ui.undo_levels`), **68 → 70**, so a running app answers `engine.commands` with **554** ids. In the surfaces this skill documents:

- **Grid and Nudge gained their full time scales.** `view.grid` takes `format: bars_beats|min_secs|timecode|feet_frames|samples|clips_markers`, `follow_main`, and new `{"timecode":…}` / `{"feet_frames":…}` increment forms; `view.nudge` takes the same `format` list except Clips/Markers; both accept `"whole note"`. Clips/Markers mode draws and snaps at visible clip edges and memory locations, and snapping excludes the clips being moved (`crates/time/src/grid.rs`, `crates/engine/src/cmd/view.rs`, `crates/model/src/session.rs`).
- **A Preferences window landed.** `setup.preferences {value?}` opens nine searchable pages (`crates/ui-egui/src/preferences.rs`), but only UI Theme, Reduce Visual Effects and Levels of Undo are wired; every other control renders disabled with "This preference is not available yet." The command-backed settings are `ui.reduce_visual_effects {mode: never|playback|always}` and `ui.undo_levels {levels: 1..=64}` (default 64); `ui.set` accepts the new `show_preferences`, `undo_levels` and `reduce_visual_effects` fields.
- **WAV bounces carry a Broadcast Wave time reference.** Mix and stem bounces write a `bext` TimeReference equal to the session timecode start plus the bounce start (`crates/engine/src/io.rs` `time_stamp`), and `soundcraft-cli convert` keeps a source's `bext`, rescaled to the output rate (`apps/soundcraft-cli/src/convert.rs`). AIFF and FLAC output have no `bext` chunk.
- **CLI.** `commands --json [--compact]` prints each command's `describe`-style details (worked out against an empty session, not your open one); workspace and plug-in-host warnings and errors now go to **stderr** as `warning:` / `error:`, keeping stdout parseable (`apps/soundcraft-cli/src/catalog.rs`, `apps/soundcraft-cli/src/logger.rs`).
- **Session and bundle hardening.** Sessions are capped at **256 MiB** when read and when saved (`MAX_SESSION_BYTES`), `.scraft` is parsed straight into the document (a document field repeated in one JSON object is refused), and a bundle whose entries share one payload is refused (`crates/engine/src/io.rs`, `crates/engine/src/io/bundle.rs`). Autosave obeys the same cap, and crash recovery comes back with record-arm and input-monitor **off** (`crates/engine/src/autosave.rs`).
- **Live input toggles are transient.** `mix.record_arm`, `mix.input_monitor` and `track.set_record_to_input_only` are non-undoable runtime writes that no longer mark the session dirty (`crates/engine/src/cmd/mix.rs`, `crates/engine/src/dirty.rs`).
- **Command semantics.** `audiosuite.process` refuses hosted `clap:`/`vst3:`/`au:` ids and points at `engine.plugins`; commands taking `clips` process each id once; hosted plug-ins are told offline vs realtime render (VST3 `kOffline`, CLAP `clap.render`), and a plug-in binary that fails to load keeps the system's reason (`crates/engine/src/cmd.rs`, `crates/engine/src/cmd/audiosuite.rs`, `crates/mix/src/instances.rs`, `crates/clap-host/src/`, `crates/vst3-host/src/`). UI-side: Insertion Follows Playback has a toolbar toggle, folder tracks indent under their folder, stereo tracks show stereo input pairs, Alt-click deletes a marker, and a newly created send opens its Send window.

**v0.16.0 → v0.17.0 delta (kept).** 18 files changed; the engine command-id set was unchanged and the UI menu registry is **68** commands, not the 67 the earlier skill carried. Wave: score export notes when bars are shorter than a sixteenth, MIDI export bounded to the notes a trimmed clip still plays, AIFF negative channel counts rejected, and VST3 multi-out instruments accepted with up to 64 audio buses — the limit is real, but only bus 0 is activated per direction, so there is still no discrete multi-out routing (`crates/vst3-host/src/ffi/instance.rs`).

**v0.15.0 → v0.17.0 delta (kept, condensed).** Added **`view.zoom_toggle_cancel`** (Cancel Zoom Toggle — Alt+Shift+E or Alt-click keeps the current view, PR #1101): one command, 483 → 484, none removed. Behaviour: the Clip menu acts on the whole edit selection, Mix clamps clip-FX gain and send-level automation, `transport.play {from}` honours the requested position, `range_param` defaults the range start to the selection start, `AutoParam::parse` keeps parameter-id case, and a hardening wave bounded automation-lane `value_at`, `GridValue::step_samples`, TempoMap bar math, non-finite `remove_dc`/RMS, CAF cookie lengths, drop-frame labels, WAV byte rates, FLAC vendor strings, MIDI-import floods and H.264 POC/DPB. MCP tools (17) and control methods (17) did not move. ⚠️ An earlier audit credited Zoom Toggle cancellation to v0.15.0 — compare-log tail trap; the registration exists only from v0.16.0.

**Verify against your installed version** — the ArtCraft Launcher auto-updates, so a newer build may differ; every count quoted here was re-measured at this tag, and code paths that moved were re-cited. The measurement method for each count is in `evidence.md`.

## Overview

SoundCraft is an open-source, pure-Rust digital audio workstation: a clean-room reimplementation of the Avid Pro Tools workflow (recording, editing, mixing, automation, bounce) that also runs in a browser (`README.md`, `docs/target-app-parity.md`). The parity target is Pro Tools Ultimate 2026.4.1. It is a Cargo workspace of 14 crates plus three entry points — the desktop app (egui 0.37), `soundcraft-cli` (parsed with clap following the repo's RFC-0012), and a WebAssembly build. It is **pre-alpha**: the repo's own generated report counts 397/512 target menu leaves implemented by the engine (77.5 %, `docs/parity-checklist.md`) and the alpha gate still lists failing workflows — interface recording, MIDI recording, session interchange (`docs/roadmap.md` "Alpha gate"). Source: `github.com/storytold/soundcraft`.

## Capabilities (verified)

### The command layer is the API (start here)

- **484 engine command specs** at v0.18.0 — **unchanged at v0.18.0** from v0.17.0 — from the **32** production modules registered by `command_specs()` (`crates/engine/src/cmd.rs`).
  - Breakdown, re-extracted at this tag: **389** literal `cmd!` ids in non-test engine sources + **94** generated by four local helper macros (`toggle!` 17, `flag!` 61, `radio!` 6, `option!` 10) + **1** direct `CommandSpec` (`mix.insert_state`) = **484**. Both the literal and the macro sets are unchanged since v0.16.0.
  - Each spec carries id, label, menu path, shortcut, params doc, enabled reason, journal/undo flags and a run function. Counting textual `cmd!(` occurrences overcounts macro-definition/doc/test lines and misses the 94 generated ids — derive the count from the id literals. Count your own build with the CLI rather than trusting any static number.
- **70 UI commands** at v0.18.0 (68 at v0.17.0) live in the UI crate's `UI_COMMANDS` (`crates/ui-egui/src/menus.rs`): windows, dialogs, `ui.dock`, `ui.dock.reset`, `ui.theme`, `ui.audio_device`, `ui.set`, `ui.reduce_visual_effects`, `ui.undo_levels`, `window.*`, `view.mix_section`, `view.scroll_into_view`. The desktop control channel appends them to `engine.commands`, so a running app reports **554 ids**; `soundcraft-cli commands` and the headless MCP server report **484**. No id overlaps the two sets.
- **CLI** (`soundcraft-cli`, **10 subcommands**, unchanged at v0.18.0, plus `--version`/`--help`; arguments are parsed with clap following RFC-0012, so a flag a subcommand does not take is a usage error): `info FILE`; `convert IN OUT [--bit-depth 16|24|32f] [--rate HZ] [--normalize] [--dither|--no-dither]`; `run [--in S.scraft | --demo] [--cmd ID[=JSON]]… [--bounce OUT] [--start T --end T] [--save S.scraft] [--inspect]`; `script FILE [--in S | --demo] [--save S] [--bounce OUT [--start T --end T]] [--keep-going]`; `commands [FILTER] [--json [--compact]]`; `describe ID`; `app [--port P] METHOD [JSON]`; `mcp [--connect PORT] [--demo] [--automation-read-root DIR]… [--automation-write-root DIR]…`; `parity [--write PATH]`; `plugins`.
  - `commands --json` (new at v0.18.0) is the machine-readable form of `commands`: one object per command with the fields `describe` prints. Its `enabled`/`disabled_reason` are evaluated against an empty session, not against a session you have open.
  - Carried behaviour: every flag accepts `--flag=value`; `run`, `script` and `convert` **reject unknown options and missing values**; `--cmd=ID=JSON` inline; `--bounce` with no `--start`/`--end` bounces the **whole session**; `convert` dithers only when resolution is lost unless `--dither`/`--no-dither` says otherwise; `script --keep-going` still exits non-zero when a command failed.
  - `app` shorthand: a dotted command id is wrapped as `engine.execute`; accepted control methods stay methods. Caveat: `ui.scroll` and `ui.zoom` are **not** in that whitelist, so `soundcraft-cli app … ui.scroll/ui.zoom` is misrouted; send those two over the raw TCP channel (`apps/soundcraft-cli/src/app.rs`).
- **MCP over stdio** (`crates/automation/src/mcp.rs`): protocol `2025-06-18` (accepts `2025-03-26`, `2024-11-05`); **17 tools + 2 resources, unchanged at v0.18.0**. Core: `list_commands`, `execute`, `batch`, `inspect_session`, `new_session`, `open_session`, `save_session`, `import_audio`, `bounce_mix`, `parity`. App-only (need the desktop app plus `mcp --connect`): `screenshot`, `ui_inspect`, `ui_set`, `menu_invoke`, `click`, `drag`, `key`. Resources: `soundcraft://session` and `soundcraft://commands`.
  - `batch` runs up to **1000** calls (`MAX_BATCH_CALLS`); larger arrays are rejected before anything runs. Any failed call makes the tool result `isError: true`; `keep_going` still runs the rest. Empty batches and non-object messages get a JSON-RPC `Invalid Request` reply.
  - Tool schemas are a subset: `new_session`/`open_session`/`save_session`/`import_audio`/`bounce_mix` forward their arguments to the engine command, so extra engine params work. Verify with `describe`.
- **Desktop control channel**: `soundcraft --control <port>` or `SOUNDCRAFT_CONTROL_PORT`; newline-delimited JSON over TCP on `127.0.0.1`, one reply per line. **17 canonical methods, unchanged at v0.18.0** (`crates/ui-egui/src/control.rs`): `engine.execute` (alias `command`), `engine.commands`, `engine.parity`, `session.inspect` (alias `document.inspect`), `ui.inspect`, `ui.menu.list`, `ui.menu.invoke`, `ui.set`, `ui.move`, `ui.click`, `ui.drag`, `ui.scroll`, `ui.zoom`, `ui.key`, `ui.text`, `ui.screenshot`, `app.quit`. `ui.dock`, `ui.dock.reset`, `ui.theme`, `ui.audio_device`, `ui.reduce_visual_effects`, `ui.undo_levels` and the `setup.*` dialogs are **UI/engine commands** invoked through `engine.execute`, not top-level methods.
  - `ui.screenshot {path?}` writes a PNG, or returns base64 in `png_base64` and the pixel size when no path is given. It binds the request to the window geometry, focus state and open session: a geometry change is retried within its deadline and then fails `screenshot stale`; a focus or session change cancels it; it can also fail `screenshot unavailable: the window has no capturable size yet` before the first paint, `screenshot queue full` (8 pending, 4 in flight), `screenshot too large`, `screenshot timed out`, or `screenshot path longer than 4096 bytes`.
  - Two UI commands refuse a direct call and name the replacement: `ui.new_tracks_dialog` ("call `track.new` with parameters") and `ui.bounce_dialog` ("call `file.bounce_mix` with a path").
  - Offscreen UI, no window: `cargo run -p soundcraft-ui-egui --example ui_shot -- out.png [script.jsonl] [--blank] [--size WxH] [--system-theme light|dark|none]` (`crates/ui-egui/examples/ui_shot.rs`).
- **Path confinement is MCP-only**: `--automation-read-root` / `--automation-write-root` confine every path for the in-process MCP server; each flag may be repeated, a kind left out grants no access of that kind, roots must be existing folders, and `--connect` with roots is refused. The desktop control channel has no equivalent confinement. Limits (`crates/engine/src/file_access.rs`): a symlink resolved inside a root still wins, so the roots bound an agent, they do not sandbox a hostile one.

### Editing and arrangement

- Edit window with tracks/clips/waveforms; Mix window (also as a separate native OS window through `window.mix_separate`); movable/dockable panels Tracks/Groups, Clips, MIDI Editor, Memory Locations, Undo History — Tracks/Groups and Clips dock as full-height columns (`crates/ui-egui/src/docking.rs`).
- Five edit modes Shuffle, Slip, Spot, Grid, Grid-Relative; seven tools Zoom, Trim, Selector, Grabber, Scrubber, Pencil, Smart (`crates/model/src/session.rs`).
- **Grid and Nudge time scales (complete at v0.18.0).** `view.grid {value?, step?, format?, follow_main?, lines?}` and `view.nudge {value?, step?, format?, follow_main?}`; `format` is `bars_beats|min_secs|timecode|feet_frames|samples` (Clips/Markers additionally for grid, and nudge refuses it). Values still accept `"1/16"`, `"1 bar"`, `"1/8t"`, `"1/4."`, `{"seconds"}`, `{"frames"}`, `{"samples"}`, plus the new `{"timecode":"frame|half_frame|quarter_frame|subframe|second|5_frames"}` and `{"feet_frames":"foot|frame|quarter_frame|subframe"}`. `follow_main: true` makes the Grid/Nudge track the main counter, and a `format: "clips_markers"` grid draws and snaps at visible clip boundaries and memory locations. Snapping excludes the clips being moved, so a cross-track move or a stationary nudge cannot snap onto its own edges (`crates/engine/src/cmd/view.rs`, `crates/model/src/session.rs` `grid_lines` / `snap_to_grid_excluding`, `crates/engine/src/edit.rs::grid_delta`). Both settings are saved in the session (`crates/model/src/session.rs` `EditState`).
- Fades/crossfades in five shapes; cut/copy/paste/duplicate/repeat/shift/insert-silence/separate/heal/consolidate/strip-silence/nudge; Tab to Transient; Zoom Toggle; loop, quantize-to-grid, clip gain and gain envelope, clip effects, edit locks, colour, ratings.
- **Strip Silence has three modes**: `edit.strip_silence {…, mode?: strip|extract|separate, name?, number?, zeros?, suffix?}`; `edit.strip_silence_preview` (query) returns the padded ranges it would keep. Since v0.18.0 the window opens with the values it last had (`crates/ui-egui/src/dialogs/strip_silence.rs`).
- **Clip Looping**: `clip.loop {clips?, count?, length?, fill?}`; `clip.unloop {mode?: remove|flatten}`.
- **Clip List › Auto Rename**: `clip.auto_rename {clips?, name?, number?, zeros?, suffix?}` sets the names editing gives the clips it separates; the schemes live in the session and survive save/reopen.
- Playlists with comping lanes, clip groups (`.scgrp`), Clip List, track folders, VCA masters, track freeze/commit/bounce, file-based track presets (`track.save_preset` / `track.load_preset`) and Import Session Data. `.scgrp` import rejects audio paths that are absolute or contain `..` (`crates/engine/src/clip_group_file.rs`).
- **`track.commit` keeps the track's exact `ChannelFormat`**, surround/height/ambisonic included, up to the renderer's 16 channels.
- Commands Keyboard Focus single-key editing in the Edit window; `options.keyboard_focus {commands|clips|groups|none}`.
- Undo/redo for document commands, an undo history window, and `engine.history` returning `{undo, can_redo}`. The depth is 1–64 (default 64) and settable through `ui.undo_levels`; live input toggles do not enter undo.

### Mixing, automation and plug-ins

- 10 inserts and 10 sends per track (`INSERT_SLOTS`/`SEND_SLOTS`, `crates/model/src/mixer.rs`), busses, aux inputs, master faders, VCAs, routing folders, object/bed routing, solo modes, mute/solo groups, phase invert, input trim, pre/post sends, automatic plug-in delay compensation. Aux and Folder strips are ordered by exact acyclic routing depth.
- **30 built-in plug-ins** in `REGISTRY`, unchanged at v0.18.0: 27 processors + 3 instruments (subtractive synth, drum synth, sampler; incl. `auto_pan`, `ring_mod`, `subharmonic`). `engine.plugins` / `soundcraft-cli plugins` list them (`crates/dsp/src/plugins.rs`).
- Offline AudioSuite processing via `audiosuite.process {process, params?, clips?, tracks?, start?, end?}`: any built-in plug-in id from `engine.plugins` **plus seven legacy process names that are not plug-ins** — `normalize`, `reverse`, `duplicate`, `time_stretch`, `pitch_shift`, `varispeed`, `speed_ramp` (unchanged at v0.18.0). Hosted `clap:`/`vst3:`/`au:` ids are refused with a message naming `engine.plugins` (`crates/engine/src/cmd/audiosuite.rs`); `signal_generator` fills a range with a new clip and is also a built-in id.
- Automation: lanes for volume, pan, mute, send level/pan/mute and any insert parameter; seven modes (`crates/model/src/automation.rs`); moving a send fader writes send-level automation (PR #1146); `automation.set_point`, `write_range`, `clear`, `thin`, `thin_all`, `write_to_current`, `write_to_all`, `volume_to_clip_gain`, plus coalesce commands. Mute automation is evaluated per sample inside a render block.
- Third-party hosting in-process: CLAP, VST3 and macOS Audio Units. Discovery: `engine.clap_plugins {rescan?}`, `engine.vst3_plugins {rescan?}`; ids `clap:<id>`, `vst3:<class id hex>`, `au:<type>:<subtype>:<manufacturer>`. **There is no Audio Unit discovery command** — the UI scans AUs at menu time. Since v0.18.0 the hosts are told whether they render offline (`kOffline`, `clap.render`), and a load failure keeps the system's dlopen/GetPluginFactory reason instead of a bare "failed".
- Plug-in editors: CLAP opens the plug-in's own floating window (Windows hosted-embedded), VST3 editors on macOS and Windows, Audio Units never; on the signed macOS build third-party VST3 is refused (library-validation entitlement). A CLAP editor must be asked for on the process main thread, enforced on every platform since v0.18.0 (`crates/clap-host/src/ffi/gui.rs`).
- Plug-in presets are partly UI-only; for a hosted plug-in's opaque state use `mix.insert_state {track, slot, state: base64|null}` — not undoable and not journaled.

### Recording and audio devices

- Record arm, input monitoring, punch on selection or on the fly, pre/post-roll, loop recording with a playlist per take, destructive and track-punch modes.
- **Live input state is transient since v0.18.0**: `mix.record_arm`, `mix.input_monitor` and `track.set_record_to_input_only` write the runtime session, are not undoable, do not mark the document dirty, and are not restored from an autosave (`crates/engine/src/cmd/mix.rs`, `crates/engine/src/dirty.rs`, `crates/engine/src/autosave.rs`).
- Takes **stream to disk** while recording: one WAV per take, the header rewritten every second; after stop the take is decoded into RAM as a session source.
- **Track input routing exists**: `track.input {"input":"In 3"}` (or a bus name / `none`); `plan_takes` records `track.channels()` consecutive device channels starting from that input, wrapped to the device's input count (`crates/engine/src/io.rs::plan_takes`). What is missing is an input/output matrix with per-channel gain/delay and latency reporting.
- Device selection is real: `ui.audio_device {system?, output?, input?, sample_rate?, buffer_size?, list?}` changes the audio system/device/rate/buffer and reopens the player; it refuses while recording. **`setup.playback_engine` is a different, legacy engine command** whose settings playback never reads (headless returns `applied: false`). ASIO is behind the opt-in `asio` build feature.
- Autosave on its own thread after changes, one folder per session, plus crash recovery at launch; `Backups/` beside a session keeps the newest ten **numbered** copies (`Backups/<name> backup <n>.<ext>`) on overwrite.

### MIDI, notation, instruments and time

- Instrument and MIDI tracks, piano-roll editor with velocity lane and event list, note add/edit/delete/move, quantize, input quantize, step input, transpose, real-time properties, MIDI track offsets, retrospective record.
- Standard MIDI File: reads formats 0 and 1 fully and format 2 best-effort; **always writes format 1**. Controller events are indexed per channel and kind since v0.18.0, so a controller number reused across channels no longer collides (`crates/midi/src/sequence.rs`).
- `mix.sampler_load {track?, path, params?}` / `mix.sampler_clear` for the built-in Sampler.
- Score Editor, MusicXML export (`file.export_sibelius`, `file.send_to_sibelius`), printable SVG score (`file.print_score`).
- Monophonic audio-to-MIDI (`edit.copy_audio_as_midi`, `track.extract_midi`) and chord detection to markers.
- Five counter timebases (bars|beats, min:secs, timecode, feet+frames, samples); tempo and meter maps with ramps; key signatures; Identify Beat; Beat Detective; Elastic Audio warping.
- **No MIDI hardware I/O at all**: `setup.midi_*` only store settings.

### Audio and session formats

- **Read:** WAV (PCM 8/16/24/32, float 32/64, extensible, RF64/BW64, BWF, unfinalised recordings) and AIFF/AIFF-C natively; FLAC, MP3, Ogg Vorbis, AAC/ALAC in MP4/M4A/M4B, CAF, Matroska and ADPCM/A-law/µ-law via symphonia 0.6. Format is detected from bytes first (`crates/audio-io/src/lib.rs`).
- **Write:** **six** extensions — `wav`, `wave`, `bwf`, `aif`, `aiff`, `flac` (`FileFormat::write_extensions`) — with optional TPDF dither; WAV switches to RF64 above 4 GiB. Float32 WAV and AIFF-C `fl32` keep finite samples above full scale. There is still no MP3/AAC/Ogg export.
- Waveform overviews are generated in memory, not cached as `.wfm` files.
- **Native session `.scraft`**: pretty-printed serde JSON with `format_version` **1**; a newer version is refused. At v0.18.0 the text is parsed straight into the document (no `serde_json::Value` tree) and a **document field repeated in one JSON object is refused** (`duplicate field`), while keys of map-like data (plugin params, edit values, Auto Rename schemes, MIDI originals) and unknown keys keep the last value / are ignored. Files over **256 MiB** are refused unread and are never written, because they could not be opened again (`MAX_SESSION_BYTES`, `crates/engine/src/io.rs`). `from_json` sanitises and validates (duplicate ids and an exhausted id space are rejected). Audio that only exists in memory is written as 32-bit float WAV into a sibling `Audio Files/` folder; saves are atomic; an overwrite copies the old file to `Backups/` first.
- `.scraftz` is the **browser** bundle (zip of the `.scraft` plus `Audio Files/`, 10,000-entry / 1 GiB caps). Desktop SoundCraft does **not** open it. Since v0.18.0 a bundle whose zip entries share one payload is refused ("bundle: files share data"), and the session inside is subject to the 256 MiB cap (`crates/engine/src/io/bundle.rs`).
- Stored media paths are resolved by `craft_docpath.resolve_absolute`: a stored path is followed only when local or on the session's own network share.
- `.scgrp` clip groups are JSON plus a `<name> Audio/` folder of 32-bit float WAVs.
- One session per running app; there are no session tabs.

### Export, bounce and delivery

- `file.bounce_mix {path, format?: wav|aiff|flac, bit_depth?: 16|24|32f, start?, end?, source?: main|bus name, normalize?, dither?, fold_down?: stereo}` streams the render to disk and returns `{path, bytes, seconds, peak_db, lufs, true_peak_db}`; `dither` defaults true, `normalize` false, omitted range means the edit selection else the whole content. **WAV output now carries a `bext` TimeReference** (session timecode start + bounce start); AIFF/FLAC have nowhere to put it (`crates/engine/src/io.rs`). Bounces are limited to 4 hours (`MAX_BOUNCE_SECS`).
- `file.bounce_stems {dir, format?, bit_depth?, start?, end?, dither?, fold_down?}` writes one file per unmuted, active audio/instrument/MIDI track; stem WAVs carry the same BWF stamp.
- `file.export_clips {dir, clips?, format?: wav}` writes clips as **WAV only**; `file.export_midi {path, tracks?}`, `file.export_session_text {path?, replace?}`, `file.export_selected_tracks_as_session`, `file.export_sibelius`/`file.send_to_sibelius`, `file.print_score`, `file.export_clip_groups`.
- `session.save_template {path, replace?}` writes a clip-stripped `.scraft` (also subject to the 256 MiB cap); there is no template browser.

### Video, surround and platforms

- Video track with thumbnails, Video window with optional timecode burn-in, Video Universe strip; pure-Rust decoding of H.264 (8-bit 4:2:0), Apple ProRes (422 family, 4444/XQ) and Motion JPEG. HEVC, AV1 and DNx movies are recognised by the demuxer but frames return "unsupported". Since v0.18.0 the H.264 decoder bounds hostile streams (SPS size, `frame_num` gaps, long-term references) instead of trusting them (`crates/video/src/h264/`). Container/bitstream layers are shared craft-libs code (`craft_media::isobmff`, `craft_media::bitstream`).
- Surround/immersive mixing: **34** main/bus format choices from Mono to 9.1.6 and 1st–7th Order Ambisonics (`ChannelFormat::ALL`, `crates/model/src/mixer.rs`); `setup.main_format`; surround panners; `track.object` for object/bed routing; Renderer window.
- Native builds for macOS (universal, signed/notarized), Windows x64/x86/arm64 (per-user install by default), Linux (AppImage, deb, rpm, Flatpak, tar.gz, riscv64 tarball; **XWayland drag-and-drop by default on Wayland**), FreeBSD, and WebAssembly. The web build has no TCP control channel and no filesystem.
- **Startup update prompt with direct self-updating** (craft-update).

## Known limitations and not-implemented

Do not assign these; each is absent or partial at v0.18.0:

- **MIDI hardware I/O is absent.** No recording from a keyboard, no live playing through instruments, no MIDI out, clock or MTC.
- **No Pro Tools interchange.** No `.ptx`/`.ptf`, AAF, OMF or Media Composer session import/export; the nearest bridge is `file.import_session_data` between SoundCraft `.scraft` sessions.
- **Audio-interface depth.** Input and output are separate cpal streams; the mix runs in fixed 512-sample blocks; no duplex clock, no I/O matrix, no latency reporting, no record-offset compensation.
- **All audio sources are decoded whole into RAM.** No disk streaming for playback; bounces themselves stream to disk.
- **Plug-in limits.** AAX is not hosted. The signed macOS build refuses third-party VST3 (library-validation entitlement). AU editors are not hosted and AUs have no discovery command; CLAP embedded editors only on Windows; VST3 editors only macOS/Windows. No external sidechain, no ARA, no out-of-process sandboxing. AudioSuite runs built-in plug-ins only, never hosted ones.
- **No compressed export** (MP3/AAC/M4A/Ogg/Opus) even though those decode on import.
- **Video is decode-only and limited.** No HEVC/AV1/DNxHD/DNxHR decode, no video export or bounce-with-video, no external timecode.
- **No immersive delivery.** No ADM BWF, Dolby Atmos renderer integration or binaural.
- **No control surfaces (HUI/MCU/EUCON) and no external sync (MTC/LTC/video reference).**
- **English-only UI, unchanged at v0.18.0.** No string catalog; a Hangul fallback font is appended for Korean names; no other fallbacks (`crates/ui-egui/src/fonts.rs`).
- **Preferences is mostly a catalog.** The nine-page window (`crates/ui-egui/src/preferences.rs`) only wires UI Theme, Reduce Visual Effects and Levels of Undo; every other control is a disabled placeholder that says "This preference is not available yet."
- **Session management is thin.** No template browser, no batch rename; the Workspace window is a one-folder file list. Sessions over 256 MiB cannot be opened or saved.
- **No speech-to-text** (settings only) and **no fidelity harness** against Pro Tools.
- **`.scraftz` does not open on the desktop**; only the browser build opens it.
- **Parity is uneven by area, unchanged at v0.18.0.** The generated report counts 397/512 menu leaves implemented (Window 1/52, AudioSuite 0/28, View 92/112, File 22/30). AudioSuite catalog leaves all map to the single `audiosuite.process` command.
- **Docs still lag the code** in places (alpha-gate input-device row, G-16 track-preset recall, the Hangul fallback denial). Trust the code paths cited here, then `soundcraft-cli describe`.

## How to operate

### Launch on macOS

- `open -a SoundCraft`, or `open -a SoundCraft --args --demo`. A terminal launch of the app executable with `--control` prints `SOUNDCRAFT_CONTROL_PORT=<port>` on **stdout**; `open -a … --args` does not show it, so prefer a fixed port there.
- App flags (verified with the installed binary's `--help`): `--demo` / `--sample`, `--no-audio` (never open an output device in a smoke test), `--control <port>` (`0` = pick a free port and print it), `--version`/`-V`, `-h`/`--help`, and positional files: `.scraft` opens as a session, `.mid`/`.midi`/`.smf` imports MIDI, anything else imports as audio.
- Environment: `SOUNDCRAFT_CONTROL_PORT` (port or loopback `host:port`; another host is ignored with a warning), `SOUNDCRAFT_CONFIG_DIR` (the whole settings folder; empty disables it), `SOUNDCRAFT_NO_PREFS` (recommended for agent test runs), `SOUNDCRAFT_NO_SYSTEM_FONTS`, `SOUNDCRAFT_WAYLAND` (Linux: `1` keeps native Wayland instead of XWayland), `RUST_LOG`. On/off variables take `1/on/true/yes` or `0/off/false/no`.
- Settings on macOS: `~/Library/Application Support/SoundCraft/` — `ui.json`, `Autosave/`, `Presets/`, `logs/soundcraft.log`. A `portable.txt` beside the executable switches to `<exe dir>/SoundCraftData`.
- `soundcraft-cli` is **not inside the app bundle**: install `soundcraft-cli-<ver>-macos-universal.zip` from the release, or build it. Check both versions before mixing them.

### Document and window model

One session per app; `session.new`/`session.open`/`session.close` replace it. Programmatic session switches **do not prompt to save** — save first. Edit and Mix are separate views; `window.mix_separate` puts Mix in its own native window. There are no session tabs. The Preferences window is modal: while it is open, menu entries and single-key editing are disabled.

### Positions, references and ranges

- Positions: a JSON integer (or float) is **samples**; `{"seconds": 2.5}` is seconds; a string is parsed in the current main-counter format then all formats, optionally prefixed with `bars_beats:`, `min_secs:`, `timecode:`, `feet_frames:` or `samples:`. CLI `--start`/`--end` parse a bare decimal as seconds.
- Ranges: `start` + `end`, or `start` + `length`; `start` alone is a point range; both omitted = the edit selection. Tracks by id or name; clips by id; buses by case-insensitive name.
- Grid/Nudge: set them by command, not by string guessing — `view.grid {"format":"timecode","follow_main":true}` is unambiguous, and `edit.separate_on_grid` / `edit.move_clips` / `edit.quantize` use whichever scale is current.

### Open, import, save, export

- New/open: `session.new {name?, sample_rate?, bit_depth?: 24, template?: blank|demo}`; `session.open {path}` never fails on missing media (it warns); `session.save {path?, replace?}`, `session.save_as`, `session.save_copy`, `session.save_template`, `session.revert`, `session.close`.
- Import: `file.import_audio {path | paths: [..], track?, at?, new_tracks?}`, `file.import_midi`, `file.import_video`, `file.import_clip_groups`, `file.import_session_data`.
- Export/bounce: see above. Always read the returned `path`/`bytes`/levels; a completed call does not prove the audio is non-silent. `soundcraft-cli info mix.wav` prints the `bwf.time_reference` a WAV bounce was stamped with.
- Audio device: `ui.audio_device {"list":true}` returns `{config, device, systems}`; applying reopens the devices and refuses while recording. Save before changing devices.

### Keyboard shortcuts (verified in code)

Space play/stop; Shift+Space half-speed; Cmd+Space or F12 record; F1–F4 edit modes; F5–F10 tools; Enter new memory location; Cmd+= Mix/Edit; Tab to transient; Cmd+Shift+N new tracks; Cmd+S/O/N save/open/new; Cmd+E separate; Cmd+D duplicate; Cmd+U strip silence; Cmd+Alt+L loop clip; Cmd+Z undo; Cmd+Shift+K export clips; Cmd+Alt+B bounce mix; Cmd+P print score; Cmd+1 Transport, Cmd+3 Big Counter, Cmd+4 Automation, Cmd+5 Memory Locations, Cmd+9 Video; Alt+Shift+C track commit; Cmd+Alt+[ / ] waveform zoom; Cmd+Ctrl+1–5 zoom presets; Cmd+Alt+0–5 clip rating; Cmd+W close window. In Commands Keyboard Focus, single keys edit: N toggles Insertion Follows Playback, B separates, X/C/V cut/copy/paste, Z undo, O/E-adjacent keys move the timeline selection (`crates/ui-egui/src/shortcuts.rs`). The in-app **Setup › Keyboard Shortcuts** window (`window.shortcuts`) is the live list.

### Recipes that work at this tag

```sh
# Headless: demo session → set a level → insert an EQ → bounce → print the session JSON.
soundcraft-cli run --demo \
  --cmd 'mix.volume={"track":"Kick","db":-6}' \
  --cmd 'mix.insert={"track":"Bass","plugin":"eq_7band"}' \
  --bounce mix.wav --inspect

# Discover a build: ids + labels as text, then every detail as JSON (new at v0.18.0).
soundcraft-cli commands bounce
soundcraft-cli commands --json --compact

# Live app (where a GUI is allowed): fixed control port, no output device, then drive it.
open -a SoundCraft --args --demo --no-audio --control 7801
soundcraft-cli app --port 7801 mix.new_bus '{"name":"Verb"}'
soundcraft-cli app --port 7801 mix.send '{"track":"Bass","bus":"Verb","level_db":-12}'
soundcraft-cli app --port 7801 automation.write_range '{"track":"Bass","param":"volume","start":0,"end":96000,"value":-6}'
soundcraft-cli app --port 7801 file.bounce_mix '{"path":"mix.wav","source":"Verb"}'
soundcraft-cli app --port 7801 ui.screenshot '{"path":"shot.png"}'

# Grid that follows the main counter, then a Clips/Markers grid, then back to a note value.
soundcraft-cli run --in song.scraft --cmd 'view.grid={"format":"timecode","follow_main":true}' --save song.scraft
soundcraft-cli run --in song.scraft --cmd 'view.grid={"format":"clips_markers"}'
soundcraft-cli run --in song.scraft --cmd 'view.grid={"value":"1/16"}'

# Named clips from Strip Silence, then preview the ranges without touching the session.
soundcraft-cli run --in song.scraft --cmd 'edit.strip_silence_preview={"tracks":["Vox"]}'
soundcraft-cli run --in song.scraft \
  --cmd 'edit.strip_silence={"tracks":["Vox"],"mode":"strip","name":"VOX","number":1,"zeros":2}' \
  --save song.scraft --inspect

# Give an MCP client a headless DAW confined to two read folders and one output folder.
claude mcp add soundcraft -- soundcraft-cli mcp --demo \
  --automation-read-root ./project --automation-read-root ./samples \
  --automation-write-root ./out
```

`mix.insert` takes a built-in id from `engine.plugins` (or a `clap:`/`vst3:`/`au:` id); `mix.send` needs the bus to exist. All positions in these examples are samples.

### Discover the build you are talking to

`soundcraft-cli commands <filter>` lists ids/labels/menu paths; `soundcraft-cli commands --json` or `soundcraft-cli describe ID` prints the authoritative parameter doc; over the control channel use `engine.commands {filter}` and `session.inspect`; over MCP use `list_commands` and `inspect_session`. Labels, menu paths and shortcuts can change between releases — bind to **ids**.

## Working with an AI agent

Legitimate, evidence-checkable work:

- **Prepare and convert inputs.** `soundcraft-cli info FILE` probes audio (including a WAV's `bwf` block); `soundcraft-cli convert IN OUT` lands assets in WAV/AIFF/FLAC (output extension decides; anything else is refused) and keeps a BWF source's time reference.
- **Drive it headlessly** with `soundcraft-cli run` / `script` / `mcp`, or bridge MCP to a running app with `--connect`. Prefer `batch` for many edits (cap 1000), then `inspect_session` and `session.audio_health` to verify. Most document commands are undoable; queries, view/session settings, the live input toggles (`mix.record_arm`, `mix.input_monitor`, `track.set_record_to_input_only`) and the explicitly non-journaled `mix.insert_state` are not.
- **Read and repair `.scraft`.** Pretty JSON with `format_version: 1`: you may parse, diff and patch it, but never bump the version, do not add private top-level keys, and **never emit the same document field twice in one object** — the new parser refuses it. Keep ids unique per namespace. Keep `Audio Files/` paths relative to the session folder. Never edit a session while the app or CLI has it open, and keep the file under 256 MiB.
- **Compose mix work from commands.** `mix.new_bus` before `mix.send`; `mix.insert {"plugin":"eq_7band"}` then `mix.insert_params`/`mix.insert_param`; `mix.volume`/`pan`/`trim`; `automation.write_range` or `set_point`; `file.bounce_mix … source:"Verb"` to bounce a bus. `engine.plugins` lists built-ins; AU has no query — know the fourcc id or use the UI. AudioSuite accepts built-ins only.
- **Set the grid explicitly** with `view.grid`/`view.nudge` `format` + `follow_main` instead of assuming a note-value scale; a Clips/Markers grid depends on what is visible, so inspect the session first.
- **Name clips from a batch edit.** `clip.auto_rename` before a cut/Strip Silence run gives every resulting piece a numbered name.
- **Verify exports.** `file.bounce_mix` returns `bytes`, `seconds`, `peak_db`, `lufs`, `true_peak_db`; check the file exists, has plausible duration and non-silent levels, then re-probe with `soundcraft-cli info` (which also shows a WAV's BWF stamp). For a stem set, check `files` count and each file.
- **Automate UI acceptance** with the control channel and its UI commands. Run with `--no-audio` and an isolated `SOUNDCRAFT_CONFIG_DIR`; never arm a track, enable input monitoring or start recording in a smoke test. Screenshots are bound to the geometry/session they were admitted for; expect `screenshot stale`/`canceled` rather than a silently wrong image.
- **What not to attempt:** driving the GUI blind; promising AAF/OMF/`.ptx`, MIDI-hardware recording/playback, MP3/AAC export, ADM/Atmos delivery or video export; opening `.scraftz` on the desktop; assuming `setup.playback_engine` changes the device (use `ui.audio_device`); expecting Audio Unit discovery or AU editors; expecting AudioSuite to run a hosted plug-in; expecting a Preferences placeholder to change anything; reading/copying Pro Tools resources — SoundCraft is clean-room (`AGENTS.md`).

## Verification protocol

SoundCraft is pre-alpha and its docs lag the code in a few places. For any real task:

1. **Round-trip on a throwaway session first**: `session.new` → one edit → `session.save` to a scratch folder → `session.open` it back → `file.bounce_mix` → confirm the returned levels are non-silent and the file exists.
2. **Never trust a silent export**: compare `peak_db`/`lufs`/`true_peak_db` with expectations and re-probe the output with `soundcraft-cli info`; for a WAV bounce, check the `bwf.time_reference` is the timecode position you expect.
3. **Back up and version per session**: copy the whole folder (`.scraft` + `Audio Files/`), not just the JSON; `Backups/` keeps the newest ten numbered copies. Keep sessions under 256 MiB — a larger save is refused before any audio is written.
4. **One session at a time, isolated profile**: run agents with `SOUNDCRAFT_CONFIG_DIR` pointing at a fresh folder. Recovered autosaves come back with record-arm and input-monitor off; re-arm explicitly.
5. **Update apps only between projects**: this skill is pinned to v0.18.0 (`soundcraft 0.18.0 (macos aarch64)`). Check `--version` before relying on a format or parameter detail.
6. **Inspect, don't guess**: `soundcraft-cli describe ID`, `commands --json` and `engine.commands` give the authoritative schema; `session.audio_health` checks loaded media without touching files.

## Sources & evidence

- Repo: https://github.com/storytold/soundcraft — inspected at tag **v0.18.0**, commit `5ff012ab88490cdfc635ee304c1019885e1b880d`, release dated 2026-11-06; inspection date **2026-11-07**. The previous pin was v0.17.0, commit `b35dd0f9eb0c08a198c1306021bd138f3a22d87c` (2026-11-02). Installed bundle: `/Applications/SoundCraft.app`, `soundcraft 0.18.0 (macos aarch64)`, `CFBundleShortVersionString` 0.18.0, `CFBundleIdentifier` `ai.storyteller.soundcraft`; the bundle contains only `SoundCraft`, not `soundcraft-cli`. Only `--version` and `--help` were run; the GUI was never launched.
- Read: `README.md`, `Cargo.toml`, `apps/soundcraft/src/{main.rs,launch_args.rs,config.rs,control_server.rs,env.rs}`, `apps/soundcraft-cli/src/{args.rs,catalog.rs,convert.rs,logger.rs,main.rs,app.rs,info.rs,mcp.rs}`, `crates/engine/src/{cmd.rs,io.rs,autosave.rs,dirty.rs,edit.rs,score.rs,file_access.rs,clip_group_file.rs}`, `crates/engine/src/cmd/{view.rs,view_more.rs,options.rs,mix.rs,edit.rs,file.rs,audiosuite.rs,track.rs,track_more.rs,setup_more.rs,clip.rs,health.rs,plugin_state.rs,zoom_toggle.rs}`, `crates/engine/src/io/{session.rs,bundle.rs}`, `crates/model/src/{session.rs,mixer.rs,track.rs,automation.rs,clip.rs,source.rs}`, `crates/audio-io/src/{lib.rs,wav.rs,flac.rs,aiff.rs}`, `crates/time/src/{grid.rs,tempo.rs,format.rs}`, `crates/midi/src/sequence.rs`, `crates/mix/src/{lib.rs,instances.rs,offline.rs}`, `crates/dsp/src/{lib.rs,plugins.rs,plugins/utility.rs}`, `crates/automation/src/{mcp.rs,args.rs}`, `crates/clap-host/src/{lib.rs,ffi/instance.rs,ffi/gui.rs,plugin.rs}`, `crates/vst3-host/src/{lib.rs,ffi/instance.rs,plugin.rs}`, `crates/ui-egui/src/{menus.rs,control.rs,preferences.rs,shortcuts.rs,toolbar.rs,docking.rs,fonts.rs}`, `crates/ui-egui/examples/ui_shot.rs`, `crates/engine/catalog/menus.txt`, `docs/{cli,mcp,control-protocol,gaps,roadmap,parity-checklist,file-format-parity,ui-parity,localization-parity,target-app-parity}.md`.
- Counts recomputed from source at this pin: **484 engine specs — unchanged at v0.18.0** (389 non-test literal `cmd!` ids + 94 helper-macro ids [toggle 17 / flag 61 / radio 6 / option 10] + 1 direct struct) from **32** registered modules; **70 UI commands** (68 → 70); a running app's `engine.commands` therefore has 554 ids; **17 MCP tools / 2 resources** and **17 control methods (+2 aliases)**, both unchanged; **10 CLI subcommands**, unchanged (plus `commands --json`); **30 built-in plug-ins** and **34 channel formats**, unchanged; **six write extensions**; `FORMAT_VERSION = 1`; `MAX_BATCH_CALLS = 1000`; `MAX_SESSION_BYTES = 256 MiB` (new); `BUNDLE_LIMITS` 10,000 entries / 1 GiB; 512-leaf menu catalog. Menu-parity 397/512 is the repo's generated report, unchanged at this tag.
- Shared library pins from `Cargo.toml`: **unchanged at v0.18.0** — all `craft-libs` crates (`craft-docpath`, `craft-media`, `craft-ui`, `craft-update`) stay at rev `c5a1cbfb…`; the egui fork stays `6d518fc7…`; `egui_extras` 0.37 was added for the About credits tables.
- Evidence table: `evidence.md` next to this file.
