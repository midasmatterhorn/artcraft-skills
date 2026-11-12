---
name: filmcraft
description: FilmCraft is an open-source, professional non-linear video editor (editing, multicam, Color Grading, effects, titles, captions, audio mixing, export) written in pure Rust, mirroring Adobe Premiere Pro's workflow, for macOS/Windows/Linux and the web. Trigger this skill whenever the user mentions FilmCraft (or "fcproj"/".fcproj", "filmcraft-cli", the FilmCraft control channel or MCP server, "window.filmcraft", a `.prfpset` effect preset), asks what it can or cannot do, which formats it reads or writes, how to script or automate it, how to prepare or convert media for it, how to verify or repair its exports and project files, or how to troubleshoot it — and also when they never name the app but describe the job — "cut this footage", "make a rough cut", "export an H.264 MP4", "grade this clip", "bake this grade to a LUT", "add captions to this video", "hand an EDL/AAF to an editor", "drive a video editor from an agent". Prefer this skill over generic NLE knowledge for anything FilmCraft touches; do not assume Premiere-only capabilities (`.prproj` import, plug-ins, upload destinations) exist here.
---

# FilmCraft

**Audit basis.** Refreshed 2026-11-12 against tag **v0.20.1**, commit **`cedf0c9bd060eb06a977d532402be2097c9ebe42`** — `git rev-parse HEAD` in the pinned checkout confirms, and the installed FilmCraft bundle matches (its binary prints `filmcraft 0.20.1`; bundle id `ai.storyteller.filmcraft`). This supersedes v0.18.0 (`015d5b3ea37e1202a529e6245d3cc021c8c16ffd`).

**v0.18.0 → v0.20.1 delta.** 433 files changed (+17 709/−23 234; one squashed release commit). **MP3 export exists**: a new in-repo Layer III encoder (`crates/mp3enc`, `crates/export/src/mp3_out.rs`) adds `Format::Mp3`, so export formats go **21 → 22** and built-in presets **44 → 45** ("MP3 48 kHz 320 kbps"); it is CBR only, 16–48 kHz, mono/stereo, no ID3 or gapless tag (`crates/mp3enc/README.md`). **The feature-naming migration landed**: the `lumetri` effect displays as **Color Grading**, the panels as **Color Grading** and **Video Scopes**, the preset folder as **Color Grading Presets** (key still `Lumetri Presets`), and the preference as **Enable External Video Output** — ids are unchanged, old names remain lookup aliases, and FCP7/FCPXML/EDL still write `Lumetri Color`, so exports are byte-identical (`docs/feature-naming.md`, `crates/project/src/effect.rs`, `crates/ui-egui/src/dock.rs`). One new query, **`lumetri.exportCube`** (engine ids **398 → 399**), bakes a clip's grade into a 3D `.cube` LUT and names what it could not bake (`crates/engine/src/color.rs`, `crates/render/src/lumetri_cube.rs`). **Video Display Format** is a sequence setting: `sequence.settings` takes `videoDisplay: timecode|feet35|feet16|frames`, and the Timecode effect gained a matching `time_format` (`crates/time/src/lib.rs`, `crates/project/src/sequence.rs`, `crates/project/src/effect/vfx.rs`). **`file.newSequence` and the `File ▸ New` item commands** (adjustment layer, bars and tone, black video, color matte, counting leader, transparent video) accept **`bin`**, and an unknown bin is an error rather than a fall back to the root; named target keys (`clips`/`clip`/`items`/`item`) are now declared on the command spec and test-enforced (`crates/engine/src/commands.rs`). Default **screenshots go to an owner-only temp folder**, and the session-log and voice-over fallbacks use the same private folder instead of the shared temp dir (`private_temp_dir`, `crates/engine/src/lib.rs`). **The audio codecs (AAC, AC-3/E-AC-3, MP1/MP2, Opus, FLAC) and the Ogg demuxer moved to craft-libs** (`craft-audio`, `craft-media`; pin `b72cb4d6…`), so the six per-codec crates (`aac`, `ac3`, `mpa`, `opus`, `flac`, `ogg`) are gone from this repo; `--graphics low-power` joins the Linux modes. DNG gained **raw development settings and opcode lists in the crate only** (`ProcessOptions`, `apply_opcodes` off by default) — the app still imports with as-shot settings (`crates/media/src/still/dng.rs`). The wave is otherwise hardening: audio effects recover from non-finite samples, mixer/remix plans are validated, previews stream to disk, proxies remember their source, OpenEXR ZIP reuses deflate tables, and H.264 encoding got faster with no new knobs.

**v0.17.0 → v0.18.0 delta** (previous round, folded). One new engine id, **`presets.scan`**; effect presets became an interchange format (**Premiere `.prfpset`**, plain or gzip, and FilmCraft JSON packs, sniffed by content and auto-scanned from `<data dir>/Effect Presets`); the built-in H.264 encoder gained **High 10 and High 10 Intra** (10-bit 4:2:0, MXF `profile_idc` 110) with presets **42 → 44**; `timeline.move` takes time objects and refuses a bad entry by index; `clip.speedDuration` gained `maintainPitch`; still-image exports report `path`/`lastPath`/`basePath`.

**v0.16.0 → v0.17.0 delta** (folded). 75 files; command ids added `colors.addCustom`, `colors.updateCustom`, `colors.removeCustom`, `markers.delete`; presets 39 → 42; SRT byte-order-mark handling, sub-dollar TTS amounts, ALE rejecting zero/negative/non-finite FPS.

**Verify against your installed version** — the ArtCraft Launcher auto-updates, so a newer build may differ; every count quoted here was re-measured or re-checked at this tag (a set that did not move is dated "unchanged at v0.20.1" and its method named in `evidence.md`), and code paths that moved were re-cited.

## Overview

FilmCraft is an open-source professional non-linear video editor written from scratch in Rust: its panels, workspaces, tools and shortcuts mirror Adobe Premiere Pro, and its codecs, containers and renderer are its own (README.md; clean-room rules in `AGENTS.md` §2 — ffmpeg is used only as an external test oracle). The parity target is Premiere Pro 2026, tracked in `docs/target-app-parity.md`, and the project calls itself **alpha** with an author-measured **~86 % feature breadth / ~56 % ready for real work** (README.md "Status", last re-measured 2026-10-10). It runs natively on macOS, Windows (x64/arm64/x86), Linux (x86_64/aarch64/riscv64), as a FreeBSD 14 x86_64 tarball, and in the browser via WebAssembly (`apps/filmcraft-web`, `docs/web.md`). The engine is headless and command-driven: the egui UI (egui 0.37 with craft-ui's shared docking), `filmcraft-cli`, a JSON-lines control channel and an MCP server dispatch the same command ids (`crates/engine/src/commands.rs`; 28 engine modules add their own `fn commands()`). Feature labels follow ArtCraft's descriptive naming (Color Grading, Video Scopes); the historical command and serialization ids were deliberately kept. Source: GitHub `storytold/filmcraft`.

## Capabilities (verified)

### Editing (implemented)

- Three-point editing: Source monitor In/Out → `source.insert` (`,`) / `source.overwrite` (`.`); `sequence.lift` (`;`) / `sequence.extract` (`'`) — both put the removed range on the clipboard (PR #3211). Trim tools and modes: ripple, roll, slip, slide, rate-stretch, razor (`timeline.razor`), Trim Monitor plus deterministic dynamic trimming (`trim.shuttle` / `trim.tick` / `trim.shuttleStop` / `trim.playAround`).
- Add Edit (⌘K), ripple delete/close gap — Close Gap with no gap selected closes the sequence's gaps (PR #2008); a gap whose sync-locked track is blocked greys the command out instead of failing silently (new at v0.20.1, `gap_closable`, `crates/engine/src/commands.rs`) — nesting, markers with colour/name/duration and `markers.exportCsv`, scene edit detection, subclips, sync/merge clips, multicam source sequences with live angle switching (`multicam.selectCamera1..9` generated by `camera_keys!`, `crates/engine/src/multicam.rs`).
- **Select All also selects captions** (new at v0.20.1): `edit.selectAll` fills clip and caption selection, and Clear / Ripple Delete then remove both in **one undo step**; captions on locked tracks stay, and a ripple removes the captions inside its range (PR #1912, `crates/engine/src/commands.rs`).
- Trim Mode linked audio (0.14.0, carried): edit linked audio with picture (#3085); Alt-drag of a clip edge trims only that side of a link; enabling a clip enables only the Alt-selected side of a link. Unlink works on a selection that also holds unlinked clips; move plans reject repeated clip identities.
- Mask vertex multi-select (0.14.0, carried): drag a marquee or Shift-click several mask vertices in the Program monitor and move them together.
- Speed changes can keep pitch: `clip.speedDuration` accepts `maintainPitch` and `sequence.inspect` reports it; time interpolation (`frameSampling` / `frameBlending` / `opticalFlow`) applies when a clip's frame rate differs from the sequence's.
- `timeline.move` takes time objects: each entry is `{clip, track, time}` where `time` is ticks or `{"seconds"|"frame"|"timecode"}` at the sequence rate; an entry missing `clip`, `track` or `time` is refused **naming its index** (`moves[2] needs …`), never silently skipped.
- **Exact integer time**: 254 016 000 000 ticks per second (`crates/time/src/lib.rs`); commands accept `ticks`, `seconds`, `frame` or `timecode`.
- Undo is copy-on-write snapshots with a **200-step history limit**; History-panel pruning (`history.deleteRedoable`, `history.clear`).
- Work area bar and duplicate-frame markers (`sequence.workAreaBar`, `sequence.setWorkArea*`, `sequence.showDuplicateFrameMarkers`, `sequence.duplicateFrames`).
- Four shortcut presets (FilmCraft Default, Premiere Pro Compatible, Final Cut Pro Compatible, Avid Media Composer Compatible; `BUILTIN_PRESETS: [&str; 4]`, `crates/engine/src/shortcuts.rs`). **A chord only matches with exactly its modifiers** (`crates/ui-egui/src/app/keys.rs:216`) — synthetic `ui.key` calls must carry the chord exactly. Scoped shortcut imports accept both the old and the new panel names (`crates/engine/src/shortcuts.rs`).
- **10 built-in workspace layouts** (`WORKSPACES: [&str; 10]`, `crates/ui-egui/src/dock.rs`): Editing, Assembly, Color, Effects, Audio, Captions and Graphics, Vertical, Learning, Review, All Panels; **28 dockable panel kinds** (`PanelKind::ALL: [PanelKind; 28]`). Chords: `Alt+Shift+1`–`Alt+Shift+8` map to Editing, Assembly, Color, Effects, Audio, Captions and Graphics, Learning, Review; `Alt+Shift+0` resets, and Vertical / All Panels have no chord (`crates/ui-egui/src/panels/keyboard.rs`, `crates/ui-egui/src/menus.rs`). Docking/floating is scriptable (`window.dockPanel`, `window.floatPanel`, `window.dockAction`).

### Colour, effects, motion (implemented; some effects approximate)

- **Color Grading** (the effect id is still `lumetri`): Basic Correction, Creative looks, RGB + hue/sat/luma curves, three-way wheels, HSL Secondary, Vignette; LUT import/export for `.cube` (1D/3D/shaper; a `#` inside a quoted `.cube` TITLE parses) and `.3dl`.
- **`lumetri.exportCube`** (new at v0.20.1) writes the clip's Color Grading pipeline — an Apply Match result included — as a 3D `.cube` sampled on a `2..65` lattice (default 33) in the sequence's output encoding. The reply names what a LUT cannot hold in `leftOut` (vignette, sharpen, HSL Secondary denoise/blur and the clip's other effects). It refuses a masked Color Grading effect, and only a Rec. 709 sequence without wide gamut qualifies; `clip` defaults to the first selected graded clip (`crates/engine/src/color.rs`, `crates/render/src/lumetri_cube.rs`).
- **10 camera log curves** — S-Log3, V-Log, Canon Log 2/3, LogC3, LogC4, Apple Log, D-Log, Fujifilm F-Log and F-Log2 (`LogCurve::ALL: [LogCurve; 10]`, `crates/color/src/log.rs`).
- **93 video effects across 16 folders**; **53 audio effects**; **84 video transitions in 10 folders plus 21 Legacy** (112 `tr(` definitions, 7 of them Obsolete) (`crates/project/src/effect.rs`, `crates/project/src/effect/`, `crates/project/src/vtransition.rs`); **27 blend modes** (`BLEND_MODES`, `crates/project/src/effect.rs`; the README still says "26"). The catalogue is **unchanged at v0.20.1** — the definition id set is identical to v0.18.0 (170 ids, none added or removed); only the `lumetri` label and one Timecode parameter changed.
- **Names resolve through aliases** (extended at v0.20.1): Premiere/After Effects names ("ADBE Drop Shadow", "Mettle SkyBox Glow"), Spanish display names ("Sombra paralela") and the retired labels ("Lumetri", "Lumetri Color", "Color Grade") map to the same effect (`resolve_effect_alias`, `crates/engine/src/commands.rs`; `find_effect_by_name` / `search_aliases`, `crates/project/src/effect.rs`). `effects.apply` answers with the applied instances `{clip, index, effect}`, appends at the end of the stack, and refuses a video effect on an audio-only selection.
- Compositing: wgpu GPU compositor (Metal/Vulkan/DX12/WebGPU) with a CPU reference renderer; Push transitions are drawn on the GPU during export. **Approximate, not exact**: Warp Stabilizer is 2-D, Morph Cut has no face tracking; AI effects (Object Mask, Generative Extend) do not exist.

### Audio (implemented)

- Loudness meters to ITU-R BS.1770 / EBU R128, matching ffmpeg's `ebur128` to 0.1 LU.
- Own DSP: EQ, filters, dynamics, true-peak limiter, delay, reverb, DeNoise, DeHummer, pitch shift; keyframable, latency-compensated (`crates/audio-dsp`). At v0.20.1 every effect recovers from a NaN/inf input sample, paired STFT channels cannot leak a non-finite sample into each other, and an unreasonably long stored remix or mixer graph is refused before allocation (`crates/audio-dsp`, `crates/render`).
- Audio Track Mixer / Clip Mixer with faders, pan, five insert slots per track, sends, submixes, and Read/Latch/Touch/Write automation; the Mix row's level drives the Mix fader.
- Essential Sound (Dialogue/Music/SFX/Ambience, loudness auto-match, ducking) via `essentialSound.*`; `ducking.against` takes the same type names `setType` takes.
- Audio-clock playback and voice-over recording with punch-in; a failed/lost audio output is reopened every 2 s while playing. On macOS/Windows/Linux the scrub grain plays on its own output thread so a playhead drag never waits for the device (`apps/filmcraft/src/audio.rs`).

### Titles, graphics, captions, transcripts (implemented, with build gates)

- Text engine (OpenType shaping, kerning, ligatures, bidi), Type/Shape/Pen tools, graphic clips with text/shape layers, `.fcgt` graphics templates. Per-character **Stroke / Stroke 2** appearance controls exist. `.mogrt` is refused by design. Graphic layer shadows clamp hostile stored distance/size/blur to the parameter range instead of allocating (v0.20.1, `crates/project/src/graphic.rs`).
- Caption tracks in Subtitle / CEA-608 / CEA-708 / Teletext. Import and export **7 formats** (`Format::ALL: [Format; 7]`, `crates/captions/src/lib.rs`) — SRT, WebVTT, SCC, MCC, EBU STL, TTML, DFXP — plus burn-in and SRT/VTR sidecars. SCC/MCC export **warns which characters it dropped or replaced**, TTML/DFXP write the track language as `xml:lang`, import reads `name`/`language`, and a TTML cue with an unclosed `<` does not break the file. The export dialog offers a **caption track picker** when the sequence has more than one track (v0.20.1, `docs/captions.md`).
- Text-based editing: `transcript.*` commands work, **but recognition needs a `whisper` build**; official releases pass no `--features`, so `transcript.generate` returns "speech-to-text is not available in this build". Import a transcript with `transcript.set`.
- Text-to-speech narration: `tts.*` with built-in Basic Female / Basic Male formant voices; Kokoro-82M neural voices need the `kokoro`/`neural-voices` feature (off in releases).
- Interface localisation: English + **16 catalogues** (`crates/ui-egui/src/i18n/*.tsv`: bs, cs, de, es, fr, id, it, ja, ko, pl, pt-BR, ru, sv, tr, uk, zh-CN) = **17 languages, unchanged at v0.20.1**; the new descriptive labels are translated in all of them. Missing translations show English and do not fail a build.

### Import and open (implemented — exact lists)

- Extension lists are code, not docs (`crates/media/src/lib.rs`):
  `STILL_EXTENSIONS = png jpg jpeg gif webp tif tiff bmp tga dpx exr hdr dng psd`;
  `AUDIO_EXTENSIONS = wav wave bwf aif aiff mp3 mp2 m4a aac flac ogg opus`;
  `VIDEO_EXTENSIONS = mp4 m4v mov mkv webm avi mxf mts m2ts m2t ts mpg mpeg vob mod tod m2v m1v mpv 3gp y4m apv`.
- Container openers, in order (`crates/codecs/src/lib.rs`): MP4/MOV, Matroska/WebM, MXF, Ogg, MPEG-TS/PS + MPEG-1/2 ES, APV, AVI, Y4M, standalone audio; plus a streaming `reader_openers` registry. Stills/WAV/animated images fall back in `crates/media`. Animated WebP joins animated GIF and APNG as importable movie clips.
- **PSD opens as the flattened composite** — grayscale or RGB, 8 or 16 bits (kept at 8), raw or PackBits rows, merged transparency unblended from white; PSB, CMYK, Lab, indexed, bitmap, duotone, 32-bit and ZIP-compressed documents are refused with a message (`crates/media/src/still/psd.rs`). HEIF/HEIC, AI/EPS and ICO still do not open.
- Video decoded: H.264 (8-bit 4:2:0 software; High 10/4:2:2 only through OS hardware), HEVC Main/Main 10, VP8, VP9, AV1, ProRes, DNxHD/HR, MPEG-2/1, MJPEG, APV, uncompressed QuickTime (raw 24-bit RGB, 2vuy, v210).
- Audio decoded: AAC-LC, AC-3, E-AC-3 (partial — plays the 5.1 core), Opus, Vorbis, MP1/MP2/MP3, FLAC, ALAC, PCM. The AAC/AC-3/MPA/Opus/FLAC decoders and their encoders now come from **craft-audio** in craft-libs (`Cargo.toml` features `aac-decode`, `aac-encode`, `ac3-decode`, `mpa-decode`, `opus-decode`, `flac-encode`), not from this repo.
- Stills incl. EXR (scan-line none/RLE/ZIPS/ZIP/PXR24), DPX, Targa, DNG/CinemaDNG (uncompressed, lossless JPEG and, new at v0.20.1, lossy JPEG Compression 34892), Radiance HDR, PSD. Image sequences: `file.importImageSequence`, CLI `probe --image-sequence`.
- Effect presets are importable media: `.prfpset` (Premiere XML, plain or gzip) and FilmCraft JSON preset packs are sniffed by content in `file.import`, imported through `presets.import`, and auto-scanned from `<data dir>/Effect Presets` by `presets.scan` (`crates/engine/src/prfpset.rs`).
- Container crates (`isobmff`, `matroska`, `mxf`, `bitstream`) are thin re-exports of `craft-media` from craft-libs, and the Ogg demuxer now lives in `craft-media` as well (the former `ogg` crate is gone); container behaviour beyond the re-export surface is *not* auditable in this repo.
- A file FilmCraft cannot decode still imports, and the **Unreadable badge explains why** — Apple Intermediate Codec is named instead of `Unknown` ("no decoder for Apple Intermediate Codec video", `crates/codecs/src/lib.rs`).

### Native project format and durability (implemented)

- `.fcproj` = UTF-8 JSON with `format: "filmcraft.project"` and an explicit `schema_version` — **17** at this tag (`assert_eq!(SCHEMA_VERSION, 17)`, `crates/format/src/lib.rs`; unchanged at v0.20.1). Every version migrates on load; newer files are refused (`TooNew`).
- **Video Display Format** (new at v0.20.1) is stored per sequence as `settings.display` (`Timecode`, `Feet + Frames 35mm`, `Feet + Frames 16mm`, `Frames`), `#[serde(default)]` so older files load as Timecode; the monitors, ruler and the Timecode effect's `time_format` follow it (`crates/time/src/lib.rs`, `crates/project/src/sequence.rs`).
- Load-time hardening: embedded LUT text over 8 MiB dropped, media frame sizes validated, `next_id` raised past the largest id in use, pin chains in templates bounded (v0.20.1, `crates/project/src/graphic_design.rs`).
- Media referenced by path (never embedded), with size + first/last-MiB fingerprints for relinking. Reads go through a guarded regular-file reader that refuses FIFOs and devices and caps at the file's length (v0.20.1, `crates/media/src/reader.rs`).
- **Atomic saves** for projects, auto-saves, recovery snapshots and preferences.
- Auto-save ring (default every 5 min, 20 versions) plus a crash-recovery journal ~1 s after each edit; saving a project creates its previews folder only when there are previews.
- Offline media never blocks opening: missing files render a "MEDIA NOT FOUND" slate; repair with `media.findMissing` / `media.relink` / `media.autoRelink` / `media.search` / `media.status`. Media an EDL names starts at timecode 00:00:00:00 until its file is linked; relink with **Align Timecode** to land on the same frames.
- Proxies, ingest (copy/transcode/createProxies), Project Manager collect/consolidate; proxy/Project-Manager file I/O uses the media pool's policy-approved resolved path. A proxy output is tied to the source file and length it was made from, so a relink mid-job does not apply the wrong proxy (v0.20.1, `crates/engine/src/proxies.rs`).

### Export (implemented)

- Export formats are the `Format` enum, **22 variants** (`crates/export/src/format.rs`): H.264, HEVC, AV1, ProRes, DNxHR, APV, MJPEG, PNG/TIFF/BMP/JPEG/Targa/DPX/EXR sequences, GIF, WAV, AIFF, AAC (`.m4a` or ADTS `.aac`), **MP3** (new at v0.20.1), FLAC, MXF OP1a, MXF OP-Atom.
- Availability is machine-dependent and queryable: `export.formats` reports `available` per format. **AV1 registers no encoder on any platform**; **HEVC has no software encoder** (VideoToolbox on macOS, NVENC on Windows).
- **45 built-in presets** ("Match Source – Adaptive High Bitrate" default), plus user presets in `<data dir>/export-presets.json`. The new preset is **"MP3 48 kHz 320 kbps"** (joint stereo, CBR).
- **MP3 export details** (v0.20.1): the sequence mix only, from `filmcraft-mp3enc`, CBR snapped to a valid Layer III rate — 32–320 kbit/s at 32/44.1/48 kHz, 8–160 kbit/s at 16/22.05/24 kHz — mono or stereo; the effective codec is MP3 for this format whatever `audioCodec` says. **No gapless/Xing tag and no ID3**: a decoder starts with the encoder delay (`DELAY = 1057` samples, about 22–24 ms depending on rate), so a player's timeline begins with that much silence (`crates/mp3enc/src/lib.rs`, `crates/export/src/mp3_out.rs`).
- **H.264 encode profiles**: `h264Profile: "baseline|main|high|high10"` plus `h264IntraOnly`; High 10 is 10-bit 4:2:0 from the built-in encoder in MP4/MOV and MXF OP1a (`crates/export/src/encoders.rs`, `crates/export/src/mxf_out.rs`); HDR exports keep their 10-bit precision, SDR exports are rendered at 8 bits first.
- Export queue as background jobs with progress/ETA/cancel, Quick Export, render previews.
- Hardware encoding: H.264 via VideoToolbox (macOS) or NVENC (Windows/Linux, opt-in); HEVC export is hardware-only.
- Ranges: `entire|inOut|workArea|custom`. Options include `sdr` (tone-map HDR→SDR), `burnCaptions`, `captionSidecar`, `alpha`, `exrCompression`, `loudnessLufs`, `hardwareEncoding`, `gpuRendering`, `maxThreads` (CPU-thread cap), `apvProfile` (`422-10|422-12|444-10|444-12|4444-10|4444-12|400-10`).
- **Image sequences never write the path you give them**: `a.png` becomes `a000.png`; the result names `path` (first still), `lastPath` (last still) and `basePath` (the name they are numbered from), and `filmcraft-cli export` prints "first to last" (`crates/engine/src/export_tools.rs`). GIF export keeps binary transparency when alpha is on.
- Offline media in an export is reported, not hidden: the result lists `offlineMedia`, exit status 1 unless `--allow-offline`.
- OpenEXR ZIP/ZIPS export reuses its deflate hash tables across a frame's chunks (v0.20.1, `crates/export/src/deflate.rs`); the written files are unchanged.

### Interchange (implemented; partly unvalidated)

- Import **and** export: CMX 3600 EDL, Final Cut Pro 7 XML (`xmeml` v4/v5), FCPXML 1.9–1.11, OpenTimelineIO JSON, AAF (Edit Protocol), OMF 2.0; ALE export only; markers CSV export only.
- Detection sniffs content before trusting the extension. Every importer merges as one undoable step and returns a report.
- AAF/OMF export `bitDepth` accepts `16` or `24` and refuses anything else (a string `"24"` included). EDL/OMF export reports **name the video tracks they cannot carry**; an EDL clip named only by clip name is reported missing rather than offline.
- FCP7 XML, FCPXML and EDL write the **stable interchange name** of a renamed effect (`interchange_name` returns `Lumetri Color` for the `lumetri` effect), so a file exported before and after the rename is byte-identical (new at v0.20.1).
- **Unvalidated in the wild**: AAF/OMF have never been opened in Media Composer/Pro Tools.

### Automation surface (implemented)

- CLI `filmcraft-cli` with **13 subcommand words**: `exec`, `run`, `commands`, `describe`, `inspect`, `import`, `export`, `render`, `probe`, `bench-decode`, `mcp`, `version`, `help` (unchanged at v0.20.1; `apps/filmcraft-cli/src/main.rs`). `export --list-presets`, `--bridge`, `--project`, `--demo`, `--save`, `--save-as`, `--data-dir`, `--keep-going`, `--compact` as before; `--format mp3` and `.mp3` extension guessing are new.
- Control channel: `filmcraft --control <port>` or `FILMCRAFT_CONTROL_PORT` — JSON-lines on 127.0.0.1, **authenticated exactly as before**: the listener stays closed unless `FILMCRAFT_CONTROL_TOKEN` holds exactly 64 hex characters, and every request must carry the same top-level `token` (`apps/filmcraft/src/control_server.rs`; `docs/control-protocol.md`). **24 methods** (unchanged at v0.20.1; `crates/ui-egui/src/control.rs`): `engine.execute`/`ui.menu.invoke`, `engine.commands`/`ui.menu.list`, `ui.inspect`, `ui.elements`, `ui.set`, `ui.panel.show`/`ui.panel.close`, `ui.click`/`ui.move`, `ui.drag`, `ui.scroll`, `ui.key`/`ui.type`, `ui.timeline.hit`/`ui.timeline.locate`, `ui.playback`, `ui.screenshot`, `ui.resize`, `ui.docking`, `app.quit`, `ui.focus`, `perf.stats`.
- MCP server on stdio, headless or via `--bridge`: **17 tools** (`#[tool(` entries in `crates/automation/src/server.rs`) + **2 resources** (`filmcraft://document`, `filmcraft://commands`) — unchanged at v0.20.1.
- Web build: `window.filmcraft` is built on craft-libs' shared `craft-web-api` page object and exposes `request`, `execute`, `commands`, `uiInspect`, `screenshot` (`{data, pngBase64}`) plus FilmCraft's `inspect`, `info`, `files`, `readFile`, `importFiles`, `importUrl`, `openProject` (`apps/filmcraft-web/src/api.rs`).
- **Registry at v0.20.1**: a static extraction of the id literals gives **399** ids (+1: `lumetri.exportCube`; none removed) against 398 at v0.18.0. The registry is assembled from `crates/engine/src/commands.rs` plus 28 engine modules that each expose `fn commands()`, and the UI-only ids live in `uic!` declarations in `crates/ui-egui` (223, unchanged), so `filmcraft-cli commands` / MCP `command_list` remain the runtime authority — neither was run here (the macOS bundle ships no CLI).
- **Named targets are declared**: a command's parameter doc names the keys it reads (`"clips":[id]`, `"clip":id`, `"items":[id]`, `"item":id`), `CommandSpec.named` carries them, and a differential test enforces that a documented key is actually read (`crates/engine/src/commands.rs`, `crates/engine/src/named_targets_tests.rs`). Naming targets leaves the selection alone; a target that does not exist is an error.

## Known limitations and not-implemented

Do not assign these to FilmCraft; they are absent from the code or gated off in releases.

- **`.prproj` cannot be opened or written.** Premiere work comes in through FCP7 XML, AAF, OTIO — or, for effect presets only, `.prfpset`.
- **No plug-in hosting**: no VST3/Audio Units, OpenFX, UXP or Adobe plug-in APIs.
- **Delivery codecs**: H.264 (up to High 10 / High 10 Intra software, 8- or 10-bit 4:2:0), ProRes, DNxHR, APV, MJPEG, MP3 (CBR only), FLAC/AAC audio. **H.264 High 4:2:2, High 4:4:4 Predictive and lossless H.264 do not exist**; HEVC needs hardware; **AV1 has no encoder anywhere**; no MPEG-2/DVD/Blu-ray/DCP, no WMV/FLV writes, no interlaced encoding. MP3 has no VBR, Xing/LAME gapless tag, ID3 metadata or short-block switching.
- **Camera RAW is DNG only**: no R3D, ARRIRAW, Sony RAW/X-OCN, Canon RAW, BRAW, ProRes RAW, JPEG 2000/XS MXF. DNG **raw development settings** (custom white balance, exposure, demosaic quality, reduced-resolution target, opcode lists) exist only as a crate API (`ProcessOptions` in `crates/dng/src/options.rs`); import always develops at the file's as-shot settings, full resolution, opcodes off. `Highlights::Recover` is accepted but behaves like `Clip`.
- **10-bit / 4:2:2 camera H.264 and HEVC decode only through OS hardware** — High 10 support is *encode*; decoding 10-bit H.264 still needs hardware.
- **Stills that will not open**: HEIF/HEIC, AI/EPS, ICO, PSB, CMYK/Lab/indexed/32-bit/ZIP-compressed PSD. **PSD does open** as the flattened composite. EXR is scan-line only (none/RLE/ZIPS/ZIP/PXR24); PIZ/B44/DWA, tiled, deep and multi-part EXR are refused.
- **No caption codecs embedded in the video stream** — burn-in and sidecar export only.
- **One project at a time.** Sequences open in Timeline tabs; there are no Productions.
- **Speech to text is off in official builds**; import a transcript with `transcript.set`. **Kokoro neural TTS voices are off in official builds**.
- **Export destinations beyond "Media File" do not exist.** The code registers exactly one, `export.destination.mediaFile`.
- **External video output is a stored preference only.** The renamed **Enable External Video Output** setting (`playback.enableTransmit`) stores a toggle with nothing behind it; it does not drive DeckLink/AJA hardware (`crates/engine/src/settings/schema.rs`, `docs/feature-naming.md`).
- **AI features are minimal**: no Object Mask, Generative Extend, media-intelligence search, caption translation, model-based Enhance Speech or auto colour.
- **UI/UX gaps**: Productions, the Search panel, Effects-panel custom bins, inline caption/transcript segment editing and source transcripts remain. `docs/ui-parity.md` and `docs/gaps.md` have repeatedly lagged the code.
- **Windows and Linux are far less tested than macOS**; **the web app shell is incomplete**; FreeBSD aarch64 is not in the release.
- **Performance**: colour grading, keys and export rendering run on the CPU; GPU compositing is partial (Push transitions export on the GPU).
- **Container and audio-codec behaviour is only partly auditable here**: MP4/MOV, Matroska/WebM, MXF, Ogg, AAC, AC-3, MP1/MP2, Opus and FLAC come from craft-libs at one pin (`b72cb4d6…`).
- **Known doc drift (trust the code)**: README "26 blend modes" (code 27), "around 30 transitions" (code 84 + 21 Legacy), "H.264 is our only software delivery codec" (ProRes/DNxHR/APV/MJPEG/MP3 exist); `docs/roadmap.md` M6 still says "24 built-in presets" (code 45); `docs/gaps.md` G13's leftover sentence still lists MP3 as missing; the `file.exportMedia` doc string omits `mp3` from `audioCodec` though the enum accepts it.

## How to operate

**Launch (macOS).** `open -a FilmCraft` or `open -a FilmCraft cut.fcproj`. A `.fcproj` argument opens as a project; any other file is imported as media. Binary: `FilmCraft.app/Contents/MacOS/FilmCraft`; app id `ai.storyteller.filmcraft`, documents UTI `ai.storyteller.filmcraft.project`, minimum macOS 11.0.

**Desktop flags** (from the `USAGE` string, confirmed by a live `--help`; an unknown option is an error, not a file name):

```
filmcraft [options] [project.fcproj | media files...]
  --control <port>      localhost JSON-lines control server   (FILMCRAFT_CONTROL_PORT;
                        also needs FILMCRAFT_CONTROL_TOKEN, 64 hex chars)
  --control-input-only  accept widget input only from the control server (needs --control)
  --demo | --empty      demo project or empty project
  --recover | --no-recover
  --data-dir <dir>      auto-save, crash recovery and logs    (FILMCRAFT_DATA_DIR)
  --graphics <mode>     default | dx12 (Windows) | low-power (Linux) | software (Windows, Linux)
  --version             print version   -h/--help  print help
```

Started with `--control`, the app opens without stealing focus. Cmd+Q routes through `app.quit` so unsaved changes prompt.

**Data directory (macOS):** `~/Library/Application Support/FilmCraft` — preferences.json, Auto-Save/, Recovery/, Logs/filmcraft.log, Media Cache/, workspaces.json, `Effect Presets/` (scanned `.prfpset`/`.json` packs), presets.json, user export presets. A **screenshot requested without a path** is not written here: it goes to an owner-only `FilmCraft-<nonce>` folder under the system temp dir (`private_temp_dir`) and the reply names the file; the session log (`Logs/session-<pid>.log`) and voice-over recordings fall back to that private folder only when no data directory is configured.

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

Do not put the token in arguments, logs, or a checked-in `.mcp.json`. Limits: 4 MiB per line, 16 concurrent connections, 120 s socket read/write timeout, 60 s wait for a UI reply; a non-request line gets one error and the connection closes. `ui.click` takes `count` 0–10 and `ui.drag` `steps` 0–1024. `ui.key` needs the chord's modifiers exactly. `ui.panel.show {panel}` accepts both "Color Grading" and the old "Lumetri Color" (likewise "Video Scopes" / "Lumetri Scopes").

**CLI shape** (full reference: `references/cli-and-protocol.md`):

```sh
filmcraft-cli commands razor                    # find command ids
filmcraft-cli describe timeline.razor           # one command: menu, shortcut, params, enabled now
filmcraft-cli --demo inspect sequence           # project/sequence as JSON, no window
filmcraft-cli --project cut.fcproj --save exec timeline.razor seconds=3.5
filmcraft-cli --project cut.fcproj --save import a.mov a.wav presets.prfpset
filmcraft-cli --project cut.fcproj export out.mp4 --preset "YouTube 1080p Full HD" --start 0 --end 10
filmcraft-cli --project cut.fcproj export mix.mp3 --preset "MP3 48 kHz 320 kbps"
filmcraft-cli export --list-presets prores
filmcraft-cli --project cut.fcproj render --seconds 2.5 --out frame.png
filmcraft-cli --bridge 127.0.0.1:9876 exec window.workspace.color   # needs FILMCRAFT_CONTROL_TOKEN
filmcraft-cli mcp --demo                                            # MCP on stdio, headless
```

Values parse as JSON when they can, else strings; dotted keys nest (capped at 64 levels). Exit status: 0 success, 1 a command failed or offline media was drawn without `--allow-offline`, 2 usage error.

**Document model.** One project per running app; sequences are the timelines and open in Timeline tabs. Panels dock/float on craft-ui's shared docking; 28 panel kinds; 10 built-in workspaces plus your own saved layouts.

**Core workflow.** Import media (⌘I or `file.import`) → build a sequence (`file.newSequence` / `file.newSequenceFromClip`, optional `bin`) → edit on the timeline → save `.fcproj` (⌘S; `file.save` / `file.saveAs` ⇧⌘S / `file.saveCopy` ⌥⌘S) → export (`File ▸ Export ▸ Media…`, `file.exportMedia`, or `export.quick`). Verified keys: `Cmd+Z`/`Cmd+Shift+Z` undo/redo, `Cmd+K` Add Edit, `Cmd+S` save, `Cmd+O` open, `Cmd+I` import, `Alt+Shift+1..8` workspaces (`Alt+Shift+0` reset), `Alt+[` / `Alt+]` work area In/Out.

**Time and display.** Ticks everywhere: 254 016 000 000 per second. Commands accept `ticks`, `seconds`, `frame` or `timecode`. A sequence's **Video Display Format** changes how the monitors and ruler show time — `sequence.settings {videoDisplay: "feet35"|"feet16"|"frames"|"timecode"}`; it is presentation only, all stored times stay ticks.

**Work area.** Show it with `sequence.workAreaBar`, set in/out with `sequence.setWorkAreaIn`/`Out` or both with `sequence.setWorkArea {start,end}`; `range: "workArea"` in an export then works. `export.resolve` errors with "the sequence has no work area" until one exists.

**Effect presets.** `presets.list` / `save` / `apply` / `delete` / `rename` / `export` / `import` / `scan`. Drop `.prfpset` or FilmCraft `.json` packs into `<data dir>/Effect Presets` and run `presets.scan`; `file.import` also accepts them (`crates/engine/src/presets.rs`).

## Working with an AI agent

Legitimate and effective:

- **Headless round trips** with `filmcraft-cli` (no window, no GUI state): import → edit via `exec`/`run` → `export` → verify. `run script.jsonl` takes one `{"id","params"}` per line and stops at the first failure unless `--keep-going`.
- **Drive the live app** through a tokened `--control <port>` or `filmcraft-cli mcp --bridge 127.0.0.1:9876`: run commands, inspect `ui.elements` for automation ids, click/drag/type, screenshot, then `edit.undo` if wrong. Pass the token through the environment of both processes.
- **Enumerate before you guess**: never invent command ids, parameter names or shortcuts. `commands`, `describe <id>` and `command_list` are authoritative. A parameter doc that shows `"clips":[id]`/`"clip":id` means you may name targets instead of selecting them.
- **Use the current labels, expect the old ones**: Color Grading, Video Scopes and Color Grading Presets are the displayed names; `lumetri.*` ids, the `lumetri` effect id, `PanelKind::LumetriColor` and the `Lumetri Presets` folder key are unchanged. Effect names may be FilmCraft names, Premiere/AE names, Spanish aliases or the retired "Lumetri Color".
- **Bake a grade for another app**: `lumetri.exportCube {clip?, path, size=33}` returns the `.cube` path and a `leftOut` list; re-apply the LUT elsewhere only for the parts it names as included.
- **Prepare and convert inputs**: generate test media with ffmpeg (allowed as an external oracle); convert unsupported sources into what FilmCraft reads; hand over Premiere effect presets as `.prfpset` rather than a project. PSD is acceptable as a still (flattened composite) but its layers are lost.
- **Interpret and repair project files**: `.fcproj` is documented JSON with a migration chain and atomic writes. Repair by relinking media through commands, not by editing paths while the app has the project open.
- **Verify exports outside the app**: `ffprobe`/`ffmpeg -i` for streams, duration, frame count, A/V sync; check exit status, the `offlineMedia` array, and the returned paths. For stills, read `path` **and** `lastPath`/`basePath`. For MP3, expect the decoder delay at the head and no gapless metadata; check the sample rate and bitrate actually written. `sdr: true` tone-maps HDR to SDR; `maxThreads` bounds export CPU use on shared machines.
- **Follow background exports correctly**: local `file.exportMedia` calls block unless `wait:false`; with the bridge, without `wait`, use the returned `poll: "jobs.list"` / `cancel: "jobs.cancel"` hints. Do not pass `wait:false` to a one-shot local CLI process unless you keep it alive.
- **Batch production**: `export.queue.add … start=true wait=true` for several deliverables; `jobs.list` for progress/ETA; `jobs.cancel` to stop. A cancellation removes only this export's files, including numbered stills up to its `lastPath`.
- **Import AAF/OMF repeatedly**: embedded audio is extracted next to the document without clobbering; read the import result.
- **Find repeated frames before trimming**: `sequence.duplicateFrames` returns per-clip ranges that another clip also shows; it skips stills, generators, nests, graphics, adjustment layers, frame holds and keyframed Time Remapping, so an empty result is not proof that no frame repeats.

Must not attempt:

- Do not assume `.prproj`, Premiere projects, plug-ins, upload destinations, Whisper transcription, Kokoro voices, MP3 VBR/gapless or DNG raw controls exist in the installed build. `.prfpset` presets are the only Premiere document FilmCraft reads.
- Do not start the control server without a token, or reuse one token across machines/sessions in a shared file; the listener refuses to start otherwise.
- Do not drive the GUI blind: read `ui.elements`/`ui.inspect` before clicking by id, and screenshot to confirm. A synthetic key chord must carry exactly the modifiers the chord names.
- Do not hand-edit a `.fcproj` to look like a newer schema or copy a `schema_version` forward, and do not expect `videoDisplay` to change stored times.
- Do not expect the headless MCP server to be sandboxed: there are no confinement flags.
- Do not commit screenshots of Adobe products or use Adobe artwork when producing documentation assets (repo rule `AGENTS.md` §1).

## Verification protocol

FilmCraft is alpha and estimates itself "~56% ready for real work". Assume every step can silently produce a wrong-but-valid file:

1. **Throwaway round trip first.** New project → import one clip → place → export → `ffprobe` the output → reopen the project in a second process and check `inspect` matches. Only then touch real work.
2. **Never trust a silent export.** Check the exit status, the `offlineMedia` list and the message naming the written files; for stills, check `path`, `lastPath` and `basePath`; for MP3, check the stream exists, the rate is one Layer III carries and the first samples are the encoder delay rather than missing audio.
3. **Read the result as media, not as a file.** Check duration, frame count, frame rate, audio channels and a couple of decoded frames; for a 10-bit H.264 delivery, check the pix_fmt/profile actually written.
4. **Version and back up per session.** Auto-save and the recovery journal are safety nets, not backups. `file.saveAs` / `file.saveCopy` before risky operations.
5. **Mind the schema.** Schema is 17 at v0.20.1; a project saved by a newer build cannot be opened by an older one. Update apps only *between* projects.
6. **Check the display format before comparing timecodes.** A sequence set to Feet + Frames shows `F+FF` in the ruler and monitors while commands still take ticks, seconds, frames or timecode; read `sequence.inspect` rather than parsing the screen.
7. **Do not trust parity docs or the README over the code.** When a doc and the code disagree, the code wins; when both are silent, write "uncertain" and test.
8. **Record the exact build** you tested (version + commit, e.g. 0.20.1 / `cedf0c9…`) — bug reports with real footage and a build id are what the project asks for.

## Sources & evidence

- Repo: https://github.com/storytold/filmcraft — inspected at **tag `v0.20.1`, commit `cedf0c9bd060eb06a977d532402be2097c9ebe42`** (shallow checkout at the release tag), **2026-11-12**; the `v0.18.0` ref (`015d5b3e…`) was used for the id, format and preset diffs. The installed bundle `/Applications/FilmCraft.app` matches the tag: `--version` prints `filmcraft 0.20.1`, `--help` matches `apps/filmcraft/src/args.rs`, `Info.plist` says 0.20.1, bundle id `ai.storyteller.filmcraft`; the GUI was never launched.
- Round evidence: `git diff --shortstat v0.18.0..HEAD` = 433 files, +17 709/−23 234; the checkout squashes the release into one commit, so commit counts are not measurable here.
- Files read: `README.md`, `Cargo.toml`, `AGENTS.md`, `docs/{agents,architecture,captions,codec-parity,control-protocol,feature-naming,file-format-parity,gaps,hardware-parity,performance,project-files,target-app-parity,ui-parity,web}.md`, `apps/filmcraft/src/{args,control_server,audio}.rs`, `apps/filmcraft-cli/src/main.rs`, `apps/filmcraft-web/src/api.rs`, `crates/engine/src/{commands,color,presets,prfpset,previews,proxies,shortcuts,voiceover,lib}.rs` and `crates/engine/src/named_targets_tests.rs`, `crates/automation/src/server.rs`, `crates/ui-egui/src/{control,dock,menus}.rs`, `crates/ui-egui/src/panels/{caption_export,menu_dialogs}.rs`, `crates/ui-egui/src/i18n/`, `crates/export/src/{format,presets,settings,run,mp3_out,encoders,mxf_out}.rs`, `crates/mp3enc/{README.md,src/lib.rs}`, `crates/dng/{README.md,src/options.rs,src/opcode.rs}`, `crates/media/src/{lib,reader}.rs`, `crates/media/src/still/{psd,exr,dng}.rs`, `crates/codecs/src/lib.rs`, `crates/project/src/{effect,graphic,graphic_design,sequence,vtransition}.rs`, `crates/project/src/effect/{vfx,audio}.rs`, `crates/color/src/log.rs`, `crates/captions/src/lib.rs`, `crates/render/src/lumetri_cube.rs`, `crates/format/src/lib.rs`, `crates/time/src/lib.rs`.
- Shared libraries consulted: `craft-web-api` page surface in craft-libs, and the craft-libs pin `b72cb4d68ca09cf067f144afc1f13abe1e82e1ed` for `craft-docpath`, `craft-media`, `craft-audio`, `craft-ui`, `craft-update` (`Cargo.toml`).
- See `evidence.md` in this directory for the claim → evidence table, the count methods and what was carried forward.
