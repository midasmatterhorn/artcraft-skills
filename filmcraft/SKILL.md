---
name: filmcraft
description: FilmCraft is an open-source, professional non-linear video editor (editing, multicam, colour, effects, titles, captions, audio mixing, export) written in pure Rust, mirroring Adobe Premiere Pro's workflow, for macOS/Windows/Linux and the web. Trigger this skill whenever the user mentions FilmCraft (or "fcproj"/".fcproj", "filmcraft-cli", the FilmCraft control channel or MCP server, "window.filmcraft", a `.prfpset` effect preset), asks what it can or cannot do, which formats it reads or writes, how to script or automate it, how to prepare or convert media for it, how to verify or repair its exports and project files, or troubleshoot it — and also when they never name the app but describe the job — "cut this footage", "make a rough cut", "export an H.264 MP4", "grade this clip", "add captions to this video", "hand an EDL/AAF to an editor", "drive a video editor from an agent". Prefer this skill over generic NLE knowledge for anything FilmCraft touches; do not assume Premiere-only capabilities (`.prproj` import, plug-ins, upload destinations) exist here.
---

# FilmCraft

**Audit basis.** Refreshed 2026-11-07 against tag **v0.18.0**, commit **`015d5b3ea37e1202a529e6245d3cc021c8c16ffd`** — `git rev-parse HEAD` in the pinned checkout confirms, and the installed `/Applications/FilmCraft.app` matches (its binary prints `filmcraft 0.18.0`; bundle id `ai.storyteller.filmcraft`). This supersedes v0.17.0 (`eb59ec09daaea519c9c8fffa404a594ae50d00e0`).

**v0.17.0 → v0.18.0 delta.** 308 files changed (+14 708/−1 517; the checkout carries one squashed release commit). One new automation id: **`presets.scan`** ("Scan Preset Library", `crates/engine/src/presets.rs`) — **+1 engine command, none removed**. Effect presets became an interchange format: **Premiere Pro `.prfpset`** (plain XML or gzip) and FilmCraft `.json` packs are detected by content (`crates/engine/src/prfpset.rs`, `is_preset_file`) and arrive via **File ▸ Import**, the Presets and Effects panels' **Import Presets…** button, a drop on the window (both routes go through `file.import`), or the auto-scanned `<data dir>/Effect Presets` folder. **The built-in H.264 encoder now writes High 10 (10-bit 4:2:0) and High 10 Intra**: `H264Profile::High10` (`crates/export/src/settings.rs`), mapped in `crates/export/src/encoders.rs`, MXF OP1a writing `profile_idc` 110 (`crates/export/src/mxf_out.rs:52`), exposed as `h264Profile: "baseline|main|high|high10"` and `h264IntraOnly` on `file.exportMedia` (`crates/engine/src/commands.rs`) and as two new built-in presets — **42 → 44** (`crates/export/src/presets.rs`). APV export profiles widen to `4444-10|4444-12|400-10` on the same command; the `Format` enum stays at **21**. Behaviour that changes agent work: `timeline.move` takes a **time object** per move at the sequence rate and **refuses a bad entry by its index** instead of skipping it (`crates/engine/src/commands.rs`, `docs/control-protocol.md`); `clip.speedDuration` gained **`maintainPitch`** (Maintain Audio Pitch; omitted = unchanged); an image-sequence export returns **`path` = first still, `lastPath`, `basePath`** and `filmcraft-cli export` prints "first to last" (`crates/engine/src/export_tools.rs:590`, `apps/filmcraft-cli/src/main.rs`); `captions.export` warnings **name each character SCC/MCC drop or replace**, TTML/DFXP write the track's **`xml:lang`**, and `captions.import` takes `name`/`language` (`docs/captions.md`, `crates/engine/src/captions.rs`); an unreadable clip's badge **says why** ("no decoder for Apple Intermediate Codec video", `crates/codecs/src/lib.rs:120-135`); a key chord matches only with **exactly its modifiers** (`crates/ui-egui/src/app/keys.rs:216`). Interchange: AAF top-level compositions carry `Usage_TopLevel`, EDL media relinked with **Align Timecode** lands on the file's own time, an EDL clip named only by clip name is **missing** rather than offline, an OTIO item's sample rate no longer sets the sequence rate, EDL/OMF export reports **name the video tracks left out**, and `bitDepth` accepts `"24"` but refuses anything except 16 or 24 (`crates/engine/src/aaf_omf.rs`, `crates/interchange/`). The rest is decode hardening (AVI chunk containment, DNx/APV/DNG/MP4 sample extents, H.264/HEVC slice and picture bounds, preset/transcript bounds) — no new codec or container.

**v0.16.0 → v0.17.0 delta** (previous round, folded). 75 files; no dotted command id added or removed; schema, languages, workspaces, CLI and control counts settled at the values quoted below; presets 39 → 42; craft-libs pinned at one revision `c5a1cbfb…`. Wave: SRT byte-order-mark handling, sub-dollar TTS amounts, ALE rejecting zero/negative/non-finite FPS.

**Older history (v0.15.0 → v0.16.0 wave, folded).** A hardening wave plus the "Integration: backlog round r1" merge; the command ids added in that period were `colors.addCustom`, `colors.updateCustom`, `colors.removeCustom` and `markers.delete`. It also brought validated clip targets on destructive commands, `effects.apply` appending at the end of a clip's stack, GIF binary transparency, and faster H.264 software export. Details in `CHANGES.md`.

**Verify against your installed version** — the ArtCraft Launcher auto-updates, so a newer build may differ; every count quoted here was re-measured or re-checked at this tag (totals that were carried because their defining modules did not change are named in `evidence.md`), and code paths that moved were re-cited.

## Overview

FilmCraft is an open-source professional non-linear video editor written from scratch in Rust: its panels, workspaces, tools and shortcuts mirror Adobe Premiere Pro, and its codecs, containers and renderer are its own (README.md; clean-room rules in `AGENTS.md` §2 — ffmpeg is used only as an external test oracle). The parity target is Premiere Pro 2026, tracked in `docs/target-app-parity.md`, and the project calls itself **alpha** with an author-measured **~86 % feature breadth / ~56 % ready for real work** (README.md "Status"). It runs natively on macOS, Windows (x64/arm64/x86), Linux (x86_64/aarch64/riscv64), as a FreeBSD 14 x86_64 tarball, and in the browser via WebAssembly (`apps/filmcraft-web`, `docs/web.md`). The engine is headless and command-driven: the egui UI (egui 0.37 with craft-ui's shared docking and ComboBoxes), `filmcraft-cli`, a JSON-lines control channel and an MCP server dispatch the same command ids (`crates/engine/src/commands.rs`; the registry is assembled from ~15 engine modules that each build `CommandSpec`). Source: GitHub `storytold/filmcraft`.

## Capabilities (verified)

### Editing (implemented)

- Three-point editing: Source monitor In/Out → `source.insert` (`,`) / `source.overwrite` (`.`); `sequence.lift` (`;`) / `sequence.extract` (`'`) — both put the removed range on the clipboard (PR #3211). Trim tools and modes: ripple, roll, slip, slide, rate-stretch, razor (`timeline.razor`), Trim Monitor plus deterministic dynamic trimming (`trim.shuttle` / `trim.tick` / `trim.shuttleStop` / `trim.playAround`).
- Add Edit (⌘K), ripple delete/close gap — Close Gap with no gap selected closes the sequence's gaps (PR #2008) — nesting, markers with colour/name/duration and `markers.exportCsv`, scene edit detection, subclips, sync/merge clips, multicam source sequences with live angle switching (`multicam.selectCamera1..9` generated by `camera_keys!`, `crates/engine/src/multicam.rs:132`).
- Trim Mode linked audio (0.14.0, carried): edit linked audio with picture (#3085); Alt-drag of a clip edge trims only that side of a link; enabling a clip enables only the Alt-selected side of a link. Unlink works on a selection that also holds unlinked clips; move plans reject repeated clip identities.
- Mask vertex multi-select (0.14.0, carried): drag a marquee or Shift-click several mask vertices in the Program monitor and move them together.
- **Speed changes can keep pitch**: `clip.speedDuration` accepts `maintainPitch` (new at v0.18.0) and `sequence.inspect` reports each clip's `maintainPitch`; time interpolation (`frameSampling` / `frameBlending` / `opticalFlow`) applies when a clip's frame rate differs from the sequence's.
- **`timeline.move` takes time objects** (new at v0.18.0): each entry is `{clip, track, time}` where `time` is ticks or `{"seconds"|"frame"|"timecode"}` at the sequence rate; an entry missing `clip`, `track` or `time` is refused **naming its index** (`moves[2] needs …`), never silently skipped.
- **Exact integer time**: 254 016 000 000 ticks per second (`crates/time/src/lib.rs`); commands accept `ticks`, `seconds`, `frame` or `timecode`.
- Undo is copy-on-write snapshots with a **200-step history limit**; History-panel pruning (`history.deleteRedoable`, `history.clear`).
- Work area bar and duplicate-frame markers (`sequence.workAreaBar`, `sequence.setWorkArea*`, `sequence.showDuplicateFrameMarkers`, `sequence.duplicateFrames`).
- Four shortcut presets (FilmCraft Default, Premiere Pro Compatible, Final Cut Pro Compatible, Avid Media Composer Compatible). **A chord only matches with exactly its modifiers** (`crates/ui-egui/src/app/keys.rs:216`) — an extra held modifier no longer triggers the command, so synthetic `ui.key` calls must carry the chord exactly.
- **10 built-in workspace layouts** (`WORKSPACES: [&str; 10]`, `crates/ui-egui/src/dock.rs`): Editing, Assembly, Color, Effects, Audio, Captions and Graphics, Vertical, Learning, Review, All Panels; **28 dockable panel kinds** (`PanelKind::ALL: [PanelKind; 28]`); docking/floating is scriptable (`window.dockPanel`, `window.floatPanel`, `window.dockAction`). Chords: `Alt+Shift+1`–`Alt+Shift+8` map to Editing, Assembly, Color, Effects, Audio, Captions and Graphics, Learning, Review; `Alt+Shift+0` resets, and Vertical / All Panels have no chord (`crates/ui-egui/src/panels/keyboard.rs`, `crates/ui-egui/src/menus.rs`).

### Colour, effects, motion (implemented; some effects approximate)

- Lumetri-style colour: Basic Correction, Creative looks, RGB + hue/sat/luma curves, three-way wheels, HSL Secondary, Vignette; LUT import/export for `.cube` (1D/3D/shaper; a `#` inside a quoted `.cube` TITLE parses) and `.3dl`.
- **10 camera log curves** — S-Log3, V-Log, Canon Log 2/3, LogC3, LogC4, Apple Log, D-Log, Fujifilm F-Log and F-Log2 (`LogCurve::ALL: [LogCurve; 10]`, `crates/color/src/log.rs`).
- **93 video effects across 16 folders**; **53 audio effects**; **84 video transitions + 21 Legacy** in 10 folders (`crates/project/src/effect.rs`, `crates/project/src/effect/`, `crates/project/src/vtransition.rs`); **27 blend modes** (`BLEND_MODES`, `crates/project/src/effect.rs`; the README still says "26"). These catalogues are unchanged at v0.18.0.
- **Effect names resolve through an alias table** (new at v0.18.0): Premiere/After Effects names ("ADBE Drop Shadow", "Mettle SkyBox Glow") and Spanish display names ("Sombra paralela", "Desenfoque gaussiano") map to the same effect, alongside the existing display-name lookup (`resolve_effect_alias`, `crates/engine/src/commands.rs`). `effects.apply` answers with the applied instances `{clip, index, effect}`, appends at the end of the stack, and refuses a video effect on an audio-only selection.
- Compositing: wgpu GPU compositor (Metal/Vulkan/DX12/WebGPU) with a CPU reference renderer; Push transitions are drawn on the GPU during export since v0.18.0. **Approximate, not exact**: Warp Stabilizer is 2-D, Morph Cut has no face tracking; AI effects (Object Mask, Generative Extend) do not exist.

### Audio (implemented)

- Loudness meters to ITU-R BS.1770 / EBU R128, matching ffmpeg's `ebur128` to 0.1 LU.
- Own DSP: EQ, filters, dynamics, true-peak limiter, delay, reverb, DeNoise, DeHummer, pitch shift; keyframable, latency-compensated (`crates/audio-dsp`).
- Audio Track Mixer / Clip Mixer with faders, pan, five insert slots per track, sends, submixes, and Read/Latch/Touch/Write automation; the Mix row's level drives the Mix fader.
- Essential Sound (Dialogue/Music/SFX/Ambience, loudness auto-match, ducking) via `essentialSound.*`; `ducking.against` takes the same type names `setType` takes since v0.18.0.
- Audio-clock playback and voice-over recording with punch-in; a failed/lost audio output is reopened every 2 s while playing.

### Titles, graphics, captions, transcripts (implemented, with build gates)

- Text engine (OpenType shaping, kerning, ligatures, bidi), Type/Shape/Pen tools, graphic clips with text/shape layers, `.fcgt` graphics templates. Per-character **Stroke / Stroke 2** appearance controls were fixed at v0.18.0. `.mogrt` is refused by design.
- Caption tracks in Subtitle / CEA-608 / CEA-708 / Teletext. Import and export **7 formats** (`Format::ALL: [Format; 7]`, `crates/captions/src/lib.rs`) — SRT, WebVTT, SCC, MCC, EBU STL, TTML, DFXP — plus burn-in and SRT/VTR sidecars. At v0.18.0: SCC/MCC export **warns which characters it dropped or replaced**, TTML/DFXP write the track language as `xml:lang`, import reads `name`/`language`, and a TTML cue with an unclosed `<` no longer breaks the file.
- Text-based editing: `transcript.*` commands work, **but recognition needs a `whisper` build**; official releases pass no `--features`, so `transcript.generate` returns "speech-to-text is not available in this build". Import a transcript with `transcript.set`.
- Text-to-speech narration: `tts.*` with built-in Basic Female / Basic Male formant voices; Kokoro-82M neural voices need the `kokoro`/`neural-voices` feature (off in releases).
- Interface localisation: English + **16 catalogues** (`crates/ui-egui/src/i18n/*.tsv`: bs, cs, de, es, fr, id, it, ja, ko, pl, pt-BR, ru, sv, tr, uk, zh-CN) = **17 languages**, unchanged at v0.18.0. Missing translations show English and do not fail a build.

### Import and open (implemented — exact lists)

- Extension lists are code, not docs: `STILL_EXTENSIONS`, `AUDIO_EXTENSIONS`, `VIDEO_EXTENSIONS` (`crates/media/src/lib.rs`).
- Container openers, in order: MP4/MOV, Matroska/WebM, MXF, Ogg, MPEG-TS/PS + MPEG-1/2 ES, APV, AVI, Y4M, standalone audio; plus a streaming `reader_openers` registry. Stills/WAV/animated images fall back in `crates/media`. Animated WebP joins animated GIF and APNG as importable movie clips.
- Video decoded: H.264 (8-bit 4:2:0 software; High 10/4:2:2 only through OS hardware), HEVC Main/Main 10, VP8, VP9, AV1, ProRes, DNxHD/HR, MPEG-2/1, MJPEG, APV, uncompressed QuickTime (raw 24-bit RGB, 2vuy, v210).
- Audio decoded: AAC-LC, AC-3, E-AC-3 (partial — plays the 5.1 core), Opus, Vorbis, MP1/MP2/MP3, FLAC, ALAC, PCM.
- Stills incl. EXR, DPX, Targa, DNG/CinemaDNG, Radiance HDR. Image sequences: `file.importImageSequence`, CLI `probe --image-sequence`.
- **Effect presets are importable media** (new at v0.18.0): `.prfpset` (Premiere XML, plain or gzip) and FilmCraft JSON preset packs are sniffed by content in `file.import`, imported through `presets.import`, and auto-scanned from `<data dir>/Effect Presets` by `presets.scan` (`crates/engine/src/prfpset.rs`). Import reports skipped presets and parameters the target effects lack.
- Container crates (`isobmff`, `matroska`, `bitstream`) remain thin re-exports of `craft-media` from craft-libs (one revision for all four craft crates, `c5a1cbfb…`, `Cargo.toml:76-91`); container behaviour beyond the re-export surface is *not* auditable in this repo.
- A file FilmCraft cannot decode still imports, and the **Unreadable badge explains why** — Apple Intermediate Codec is named instead of `Unknown` ("no decoder for Apple Intermediate Codec video", `crates/codecs/src/lib.rs:120-135`).

### Native project format and durability (implemented)

- `.fcproj` = UTF-8 JSON with `format: "filmcraft.project"` and an explicit `schema_version` — **17** at this tag (`assert_eq!(SCHEMA_VERSION, 17)`, `crates/format/src/lib.rs`; unchanged at v0.18.0). Every version migrates on load; newer files are refused (`TooNew`).
- Load-time hardening: embedded LUT text over 8 MiB dropped, media frame sizes validated, `next_id` raised past the largest id in use.
- Media referenced by path (never embedded), with size + first/last-MiB fingerprints for relinking.
- **Atomic saves** for projects, auto-saves, recovery snapshots and preferences.
- Auto-save ring (default every 5 min, 20 versions) plus a crash-recovery journal ~1 s after each edit; saving a project creates its previews folder only when there are previews.
- Offline media never blocks opening: missing files render a "MEDIA NOT FOUND" slate; repair with `media.findMissing` / `media.relink` / `media.autoRelink` / `media.search` / `media.status`. Media an EDL names starts at timecode 00:00:00:00 until its file is linked; relink with **Align Timecode** to land on the same frames.
- Proxies, ingest (copy/transcode/createProxies), Project Manager collect/consolidate; proxy/Project-Manager file I/O uses the media pool's policy-approved resolved path.

### Export (implemented)

- Export formats are the `Format` enum, **21 variants** (unchanged at v0.18.0; `crates/export/src/format.rs`): H.264, HEVC, AV1, ProRes, DNxHR, APV, MJPEG, PNG/TIFF/BMP/JPEG/Targa/DPX/EXR sequences, GIF, WAV, AIFF, AAC (`.m4a` or ADTS `.aac`), FLAC, MXF OP1a, MXF OP-Atom.
- Availability is machine-dependent and queryable: `export.formats` reports `available` per format. **AV1 registers no encoder on any platform**; **HEVC has no software encoder** (VideoToolbox on macOS, NVENC on Windows).
- **44 built-in presets** ("Match Source – Adaptive High Bitrate" default), plus user presets in `<data dir>/export-presets.json`. New at v0.18.0: **"H.264 High 10 Master"** (High 10, CRF 16, 10-bit master) and **"H.264 High 10 Intra"** (every frame a keyframe, CRF 12) (`crates/export/src/presets.rs`).
- **H.264 encode profiles**: `h264Profile: "baseline|main|high|high10"` plus `h264IntraOnly` on `file.exportMedia` (new at v0.18.0). High 10 is 10-bit 4:2:0 from the built-in encoder in MP4/MOV and MXF OP1a (`crates/export/src/encoders.rs`, `crates/export/src/mxf_out.rs:52`); HDR exports keep their 10-bit precision, SDR exports are rendered at 8 bits first.
- Export queue as background jobs with progress/ETA/cancel, Quick Export, render previews.
- Hardware encoding: H.264 via VideoToolbox (macOS) or NVENC (Windows/Linux, opt-in); HEVC export is hardware-only.
- Ranges: `entire|inOut|workArea|custom`. Options include `sdr` (tone-map HDR→SDR), `burnCaptions`, `captionSidecar`, `alpha`, `exrCompression`, `loudnessLufs`, `hardwareEncoding`, `gpuRendering`, `maxThreads` (CPU-thread cap), `apvProfile` (now `422-10|422-12|444-10|444-12|4444-10|4444-12|400-10`).
- **Image sequences never write the path you give them**: `a.png` becomes `a000.png`; the result names `path` (first still), `lastPath` (last still) and `basePath` (the name they are numbered from), and `filmcraft-cli export` prints "first to last" (new at v0.18.0, `crates/engine/src/export_tools.rs:590`). GIF export keeps binary transparency when alpha is on.
- Offline media in an export is reported, not hidden: the result lists `offlineMedia`, exit status 1 unless `--allow-offline`.

### Interchange (implemented; partly unvalidated)

- Import **and** export: CMX 3600 EDL, Final Cut Pro 7 XML (`xmeml` v4/v5), FCPXML 1.9–1.11, OpenTimelineIO JSON, AAF (Edit Protocol), OMF 2.0; ALE export only; markers CSV export only.
- Detection sniffs content before trusting the extension. Every importer merges as one undoable step and returns a report.
- AAF/OMF export `bitDepth` accepts `16` or `24` and refuses anything else (v0.18.0; `"24"` as a string included). EDL/OMF export reports **name the video tracks they cannot carry**; an EDL clip named only by clip name is reported missing rather than offline.
- **Unvalidated in the wild**: AAF/OMF have never been opened in Media Composer/Pro Tools.

### Automation surface (implemented)

- CLI `filmcraft-cli` with **13 subcommand words**: `exec`, `run`, `commands`, `describe`, `inspect`, `import`, `export`, `render`, `probe`, `bench-decode`, `mcp`, `version`, `help` (unchanged at v0.18.0; `apps/filmcraft-cli/src/main.rs`). `export --list-presets`, `--bridge`, `--project`, `--demo`, `--save`, `--save-as`, `--data-dir`, `--keep-going`, `--compact` as before.
- Control channel: `filmcraft --control <port>` or `FILMCRAFT_CONTROL_PORT` — JSON-lines on 127.0.0.1, **authenticated exactly as before**: the listener stays closed unless `FILMCRAFT_CONTROL_TOKEN` holds exactly 64 hex characters, and every request must carry the same top-level `token` (`apps/filmcraft/src/control_server.rs`; `docs/control-protocol.md`). **24 methods** (unchanged at v0.18.0; `crates/ui-egui/src/control.rs`): engine.execute/ui.menu.invoke, engine.commands/ui.menu.list, ui.inspect, ui.elements, ui.set, ui.panel.show/close, ui.click/move, ui.drag, ui.scroll, ui.key/type, ui.timeline.hit/locate, ui.playback, ui.screenshot, ui.resize, ui.docking, app.quit, ui.focus, perf.stats.
- MCP server on stdio, headless or via `--bridge`: **17 tools** (`#[tool(` entries in `crates/automation/src/server.rs`) + **2 resources** (`filmcraft://document`, `filmcraft://commands`) — unchanged at v0.18.0; the only server change is a bounded queue for parse-error replies (64), so a client that sends junk and never reads stalls its own input.
- Web build exposes the same engine as JS promises: `window.filmcraft.{execute,request,commands,inspect,screenshot,importFiles,importUrl,openProject,files,readFile,info}`.
- **Registry at v0.18.0**: +1 id (`presets.scan`), none removed — measured by diffing the `cmd!`/`query!` literals and the `CommandSpec`-building modules between tags. The registry spans `crates/engine/src/commands.rs` plus ~14 sibling modules (for example `crates/engine/src/presets.rs`, `crates/engine/src/color.rs`, `crates/engine/src/multicam.rs`, `crates/engine/src/media_browser.rs`), so a single static total is not a stable number and is not quoted here; the UI-only ids live in `uic!` declarations in `crates/ui-egui` (unchanged this round). `filmcraft-cli commands` / MCP `command_list` remain the runtime authority — neither was run here (the macOS bundle ships no CLI).

## Known limitations and not-implemented

Do not assign these to FilmCraft; they are absent from the code or gated off in releases.

- **`.prproj` cannot be opened or written.** Premiere work comes in through FCP7 XML, AAF, OTIO — or, for effect presets only, `.prfpset` (new at v0.18.0).
- **No plug-in hosting**: no VST3/Audio Units, OpenFX, UXP or Adobe plug-in APIs.
- **Delivery codecs**: H.264 (up to High 10 / High 10 Intra software, 8- or 10-bit 4:2:0), ProRes, DNxHR, APV, MJPEG. **H.264 High 4:2:2, High 4:4:4 Predictive and lossless H.264 do not exist**; HEVC needs hardware; **AV1 has no encoder anywhere**; no MPEG-2/DVD/Blu-ray/DCP, no MP3 or WMV/FLV writes, no interlaced encoding.
- **Camera RAW is DNG only**: no R3D, ARRIRAW, Sony RAW/X-OCN, Canon RAW, BRAW, ProRes RAW, JPEG 2000/XS MXF.
- **10-bit / 4:2:2 camera H.264 and HEVC decode only through OS hardware** — the new High 10 support is *encode*; decoding 10-bit H.264 still needs hardware.
- **Stills that will not open**: PSD, HEIF/HEIC, AI/EPS, ICO; EXR only scan-line none/RLE/ZIPS/ZIP/PXR24.
- **No caption codecs embedded in the video stream** — burn-in and sidecar export only.
- **One project at a time.** Sequences open in Timeline tabs; there are no Productions.
- **Speech to text is off in official builds**; import a transcript with `transcript.set`. **Kokoro neural TTS voices are off in official builds**.
- **Export destinations beyond "Media File" do not exist.** The code registers exactly one, `export.destination.mediaFile`.
- **AI features are minimal**: no Object Mask, Generative Extend, media-intelligence search, caption translation, model-based Enhance Speech or auto colour.
- **UI/UX gaps**: Productions, the Search panel, Effects-panel custom bins, inline caption/transcript segment editing and source transcripts remain. `docs/ui-parity.md` and `docs/gaps.md` have repeatedly lagged the code.
- **Windows and Linux are far less tested than macOS**; **the web app shell is incomplete**.
- **Performance**: colour grading, keys and export rendering run on the CPU; GPU compositing is partial (Push transitions now export on the GPU).
- **FreeBSD aarch64 is not in the release.**
- **Container behaviour is only partly auditable here**: MP4/MOV, Matroska/WebM and bit I/O come from `craft-media` at the pinned revision.
- **Known doc drift (trust the code)**: README "26 blend modes" (code 27) and "around 30 transitions" (code 84 + 21 Legacy); README ">650 commands" against a registry whose static total is not reproducible; `docs/roadmap.md` M6 still says "24 built-in presets" (code 44); `docs/project-files.md` has lagged the schema example.

## How to operate

**Launch (macOS).** `open -a FilmCraft` or `open -a FilmCraft cut.fcproj`. A `.fcproj` argument opens as a project; any other file is imported as media. Binary: `/Applications/FilmCraft.app/Contents/MacOS/FilmCraft`; app id `ai.storyteller.filmcraft`, documents UTI `ai.storyteller.filmcraft.project`, minimum macOS 11.0.

**Desktop flags** (from the `USAGE` string; an unknown option is an error, not a file name):

```
filmcraft [options] [project.fcproj | media files...]
  --control <port>      localhost JSON-lines control server   (FILMCRAFT_CONTROL_PORT;
                        also needs FILMCRAFT_CONTROL_TOKEN, 64 hex chars)
  --control-input-only  accept widget input only from the control server (needs --control)
  --demo | --empty      demo project or empty project
  --recover | --no-recover
  --data-dir <dir>      auto-save, crash recovery and logs    (FILMCRAFT_DATA_DIR)
  --graphics <mode>     default | dx12 (Windows) | software (Windows, Linux)
  --version             print version   -h/--help  print help
```

Started with `--control`, the app opens without stealing focus. Cmd+Q routes through `app.quit` so unsaved changes prompt.

**Data directory (macOS):** `~/Library/Application Support/FilmCraft` — preferences.json, Auto-Save/, Recovery/, Logs/filmcraft.log, Media Cache/, workspaces.json, `Effect Presets/` (scanned `.prfpset`/`.json` packs), presets.json, user export presets.

**The CLI is not inside the .app.** On macOS `filmcraft-cli` ships as a separate release asset, `filmcraft-cli-<version>-macos-<arch>.zip`, or build it: `cargo run --release -p filmcraft-cli -- commands`.

**Control channel with authentication.** Both the desktop and any bridge/raw client must share one token in the environment; without it the desktop never listens:

```sh
export FILMCRAFT_CONTROL_TOKEN="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
filmcraft --control 9876 &
filmcraft-cli mcp --bridge 127.0.0.1:9876      # inherits the token; adds "token" to every line
python3 - <<'PY'
import json, os, socket
s = socket.create_connection(("127.0.0.1", 9876)); f = s.makefile("rw")
f.write(json.dumps({"id":1, "token": os.environ["FILMCRAFT_CONTROL_TOKEN"],
                    "method":"engine.execute", "params":{"command":"sequence.addEdit","params":{"seconds":3}}})+"\n"); f.flush()
print(f.readline())
PY
```

Do not put the token in arguments, logs, or a checked-in `.mcp.json`. Limits: 4 MiB per line, 16 concurrent connections, 120 s socket read/write timeout, 60 s wait for a UI reply; a non-request line gets one error and the connection closes. `ui.click` takes `count` 0–10 and `ui.drag` `steps` 0–1024. `ui.key` needs the chord's modifiers exactly.

**CLI shape** (full reference: `references/cli-and-protocol.md`):

```sh
filmcraft-cli commands razor                    # find command ids
filmcraft-cli describe timeline.razor           # one command: menu, shortcut, params, enabled now
filmcraft-cli --demo inspect sequence           # project/sequence as JSON, no window
filmcraft-cli --project cut.fcproj --save exec timeline.razor seconds=3.5
filmcraft-cli --project cut.fcproj --save import a.mov b.wav presets.prfpset
filmcraft-cli --project cut.fcproj export out.mp4 --preset "YouTube 1080p Full HD" --start 0 --end 10
filmcraft-cli export --list-presets prores
filmcraft-cli --project cut.fcproj render --seconds 2.5 --out frame.png
filmcraft-cli --bridge 127.0.0.1:9876 exec window.workspace.color   # needs FILMCRAFT_CONTROL_TOKEN
filmcraft-cli mcp --demo                                            # MCP on stdio, headless
```

Values parse as JSON when they can, else strings; dotted keys nest (capped at 64 levels). Exit status: 0 success, 1 a command failed or offline media was drawn without `--allow-offline`, 2 usage error.

**Document model.** One project per running app; sequences are the timelines and open in Timeline tabs. Panels dock/float on craft-ui's shared docking; 28 panel kinds; 10 built-in workspaces plus your own saved layouts.

**Core workflow.** Import media (⌘I or `file.import`) → build a sequence (`file.newSequence` / `file.newSequenceFromClip`) → edit on the timeline → save `.fcproj` (⌘S; `file.save` / `file.saveAs` ⇧⌘S / `file.saveCopy` ⌥⌘S) → export (`File ▸ Export ▸ Media…`, `file.exportMedia`, or `export.quick`). Verified keys: `Cmd+Z`/`Cmd+Shift+Z` undo/redo, `Cmd+K` Add Edit, `Cmd+S` save, `Cmd+O` open, `Cmd+I` import, `Alt+Shift+1..8` workspaces (`Alt+Shift+0` reset), `Alt+[` / `Alt+]` work area In/Out.

**Time.** Ticks everywhere: 254 016 000 000 per second. Commands accept `ticks`, `seconds`, `frame` or `timecode` (including `timeline.move`'s per-move `time`, new at v0.18.0).

**Work area.** Show it with `sequence.workAreaBar`, set in/out with `sequence.setWorkAreaIn`/`Out` or both with `sequence.setWorkArea {start,end}`; `range: "workArea"` in an export then works. `export.resolve` errors with "the sequence has no work area" until one exists.

**Effect presets.** `presets.list` / `save` / `apply` / `delete` / `rename` / `export` / `import` / `scan`. Drop `.prfpset` or FilmCraft `.json` packs into `<data dir>/Effect Presets` and run `presets.scan`; `file.import` also accepts them (`crates/engine/src/presets.rs`).

## Working with an AI agent

Legitimate and effective:

- **Headless round trips** with `filmcraft-cli` (no window, no GUI state): import → edit via `exec`/`run` → `export` → verify. `run script.jsonl` takes one `{"id","params"}` per line and stops at the first failure unless `--keep-going`.
- **Drive the live app** through a tokened `--control <port>` or `filmcraft-cli mcp --bridge 127.0.0.1:9876`: run commands, inspect `ui.elements` for automation ids, click/drag/type, screenshot, then `edit.undo` if wrong. Pass the token through the environment of both processes.
- **Enumerate before you guess**: never invent command ids, parameter names or shortcuts. `commands`, `describe <id>` and `command_list` are authoritative. `effects.apply` returns the applied instances — use them to target later `effects.setParam` calls; effect names may be given as FilmCraft names, Premiere/AE names or Spanish aliases (v0.18.0).
- **Prepare and convert inputs**: generate test media with ffmpeg (allowed as an external oracle); convert unsupported sources into what FilmCraft reads; hand over Premiere effect presets as `.prfpset` rather than a project.
- **Interpret and repair project files**: `.fcproj` is documented JSON with a migration chain and atomic writes. Repair by relinking media through commands, not by editing paths while the app has the project open.
- **Verify exports outside the app**: `ffprobe`/`ffmpeg -i` for streams, duration, frame count, A/V sync; check exit status, the `offlineMedia` array, and the returned paths. For stills, read `path` **and** `lastPath`/`basePath` — the sequence is numbered from `basePath`. `sdr: true` tone-maps HDR to SDR; `maxThreads` bounds export CPU use on shared machines.
- **Follow background exports correctly**: local `file.exportMedia` calls block unless `wait:false`; with the bridge, without `wait`, use the returned `poll: "jobs.list"` / `cancel: "jobs.cancel"` hints. Do not pass `wait:false` to a one-shot local CLI process unless you keep it alive.
- **Batch production**: `export.queue.add … start=true wait=true` for several deliverables; `jobs.list` for progress/ETA; `jobs.cancel` to stop. A cancellation removes only this export's files, including numbered stills up to its `lastPath`.
- **Import AAF/OMF repeatedly**: embedded audio is extracted next to the document without clobbering; read the import result.
- **Find repeated frames before trimming**: `sequence.duplicateFrames` returns per-clip ranges that another clip also shows; it skips stills, generators, nests, graphics, adjustment layers, frame holds and keyframed Time Remapping, so an empty result is not proof that no frame repeats.

Must not attempt:

- Do not assume `.prproj`, Premiere projects, plug-ins, upload destinations, Whisper transcription or Kokoro voices exist in the installed build. `.prfpset` presets are the only Premiere document FilmCraft reads.
- Do not start the control server without a token, or reuse one token across machines/sessions in a shared file; the listener refuses to start otherwise.
- Do not drive the GUI blind: read `ui.elements`/`ui.inspect` before clicking by id, and screenshot to confirm. A synthetic key chord must carry exactly the modifiers the chord names.
- Do not hand-edit a `.fcproj` to look like a newer schema or copy a `schema_version` forward.
- Do not expect the headless MCP server to be sandboxed: there are no confinement flags.
- Do not commit screenshots of Adobe products or use Adobe artwork when producing documentation assets (repo rule `AGENTS.md` §1).

## Verification protocol

FilmCraft is alpha and estimates itself "~56% ready for real work". Assume every step can silently produce a wrong-but-valid file:

1. **Throwaway round trip first.** New project → import one clip → place → export → `ffprobe` the output → reopen the project in a second process and check `inspect` matches. Only then touch real work.
2. **Never trust a silent export.** Check the exit status, the `offlineMedia` list and the message naming the written files; for stills, check `path`, `lastPath` and `basePath`.
3. **Read the result as media, not as a file.** Check duration, frame count, frame rate, audio channels and a couple of decoded frames; for a 10-bit H.264 delivery, check the pix_fmt/profile actually written.
4. **Version and back up per session.** Auto-save and the recovery journal are safety nets, not backups. `file.saveAs` / `file.saveCopy` before risky operations.
5. **Mind the schema.** Schema is 17 at v0.18.0; a project saved by a newer build cannot be opened by an older one. Update apps only *between* projects.
6. **Do not trust parity docs or the README over the code.** When a doc and the code disagree, the code wins; when both are silent, write "uncertain" and test.
7. **Record the exact build** you tested (version + commit, e.g. 0.18.0 / `015d5b3…`) — bug reports with real footage and a build id are what the project asks for.

## Sources & evidence

- Repo: https://github.com/storytold/filmcraft — inspected at **tag `v0.18.0`, commit `015d5b3ea37e1202a529e6245d3cc021c8c16ffd`** (shallow checkout at the release tag), **2026-11-07**; the `v0.17.0` ref (`eb59ec09…`) was used for the id and preset diffs. The installed bundle `/Applications/FilmCraft.app` matches the tag: `--version` prints `filmcraft 0.18.0`, `Info.plist` CFBundleShortVersionString `0.18.0`, bundle id `ai.storyteller.filmcraft`; the GUI was never launched.
- Round evidence: `git diff --shortstat v0.17.0..HEAD` = 308 files, +14 708/−1 517; the checkout squashes the release into one commit, so commit counts are not measurable here.
- Files read: `README.md`, `Cargo.toml`, `docs/{agents,architecture,captions,codec-parity,control-protocol,file-format-parity,gaps,graphics,hardware-parity,performance,project-files,target-app-parity,ui-parity,web}.md` and `docs/getting-started-fades.md`, `apps/filmcraft/src/{args,control_server}.rs`, `apps/filmcraft-cli/src/main.rs`, `crates/engine/src/{commands,multicam,presets,prfpset,aaf_omf,export_tools,shortcuts}.rs`, `crates/automation/src/server.rs`, `crates/ui-egui/src/{control,dock,menus}.rs` and `crates/ui-egui/src/app/keys.rs`, `crates/ui-egui/src/i18n/`, `crates/export/src/{lib,format,presets,settings,encoders,mxf_out}.rs`, `crates/codecs/src/lib.rs`, `crates/media/src/lib.rs`, `crates/interchange/src/lib.rs`, `crates/captions/src/lib.rs`, `crates/project/src/{effect,vtransition}.rs`, `crates/project/src/effect/`, `crates/color/src/log.rs`, `crates/format/src/lib.rs`, `crates/time/src/lib.rs`.
- Shared libraries consulted only by pin: `craft-docpath`, `craft-media`, `craft-ui`, `craft-update` at one revision, `c5a1cbfb…` (`Cargo.toml:76-91`).
- See `evidence.md` in this directory for the claim → evidence table, the count methods and what was carried forward.
