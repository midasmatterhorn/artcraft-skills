# FilmCraft file formats — what the code actually reads and writes

Version: repo tag **v0.20.1**, commit `cedf0c9bd060eb06a977d532402be2097c9ebe42` (inspected 2026-11-12).
Carried from v0.18.0 unless marked **New in 0.20.1**. The v0.20.1 wave adds MP3 export, PSD was already
importable (the previous note was wrong), DNG gained lossy-JPEG raw data and crate-level raw settings,
and the audio codecs plus Ogg moved to craft-libs. No import or export table row lost a format.
Every list below is read out of the code, not the marketing docs. Where a doc contradicts the code, the
contradiction is named and the code wins.

**Naming (0.20.1).** Display labels changed, identifiers did not: the `lumetri` effect is shown as
**Color Grading**, the panels as Color Grading / Video Scopes, the preset folder as Color Grading
Presets (key `Lumetri Presets`). FCP7 XML, FCPXML and EDL still write `Lumetri Color`
(`crates/project/src/effect.rs`, `interchange_name`), so interchange files are unchanged.

**Shared ownership.** `crates/isobmff` (MP4/MOV), `crates/matroska` (MKV/WebM), `crates/mxf` and
`crates/bitstream` are re-export shims over `craft-media`; the Ogg demuxer now lives in `craft-media`
too (the former ogg crate is gone), and the audio codecs
(AAC, AC-3/E-AC-3, MP1/MP2, Opus, FLAC) come from `craft-audio` — all from craft-libs pinned at one
revision, `rev = "b72cb4d68ca09cf067f144afc1f13abe1e82e1ed"` (`Cargo.toml`; `docs/architecture.md`).
What this repo proves is that the openers are registered and wired; box/element-level behaviour beyond
`docs/file-format-parity.md` lives in that pin — write "uncertain — see Cargo.toml pin" instead of guessing.

## Import extension lists (authoritative)

`crates/media/src/lib.rs` (unchanged from v0.18.0):

```rust
STILL_EXTENSIONS = ["png","jpg","jpeg","gif","webp","tif","tiff","bmp","tga","dpx","exr","hdr","dng","psd"]
AUDIO_EXTENSIONS = ["wav","wave","bwf","aif","aiff","mp3","mp2","m4a","aac","flac","ogg","opus"]
VIDEO_EXTENSIONS = ["mp4","m4v","mov","mkv","webm","avi","mxf","mts","m2ts","m2t","ts","mpg","mpeg",
                    "vob","mod","tod","m2v","m1v","mpv","3gp","y4m","apv"]
```

`is_importable()` is exactly membership in those three lists (the Media Browser and drag/drop filter on it).
Files that fail to open still import with an error per file.

Container openers, in the order they are tried (`crates/codecs/src/lib.rs`):
`mp4` (MP4/MOV), `mkv` (Matroska/WebM), `mxf` (OP1a/OP-Atom), `ogg`, `mpeg` (TS/PS/ES), `apv`, `avi`, `y4m`,
`audio` (standalone compressed audio). Then `filmcraft_media` falls back to: OpenEXR sniff, Radiance HDR
sniff, WAV, animated GIF/APNG/WebP, generic stills. There is also a streaming `reader_openers` registry
(index on open, samples on demand) used for platform media sources such as the web app's WebCodecs MP4.
File bytes are read through a guarded regular-file reader that refuses FIFOs and devices and caps at the
handle's length (new in 0.20.1, `crates/media/src/reader.rs`).

Animated WebP joins animated GIF and APNG as a movie clip: every frame composited onto the full canvas
with the file's disposal method, per-frame delays (sub-10 ms clamped to 10 ms), identical consecutive
frames merged, transparency kept; a one-frame file falls back to the still decoder
(`crates/media/src/animated.rs`).

`file.import` sniffs interchange documents as well (AAF/OMF structured storage, `<xmeml`, `<fcpxml`,
`"OTIO_SCHEMA"`, EDL headers) and imports them as timelines (`crates/interchange/src/lib.rs`).

## Video codecs

| Codec | Decode | Encode | Evidence |
|---|:--:|:--:|---|
| H.264/AVC | yes (8-bit 4:2:0 software; High 10/4:2:2 only via OS hardware) | yes (own encoder: Baseline/Main/High, **High 10 4:2:0 (10-bit) and High 10 Intra**, CABAC, B-frames, CRF/CBR/VBR/2-pass; hardware via VideoToolbox on macOS or NVENC on Windows/Linux when `hardwareEncoding: auto`) | `crates/h264`, `crates/h264enc`, `crates/export/src/{settings,encoders,mxf_out}.rs`, `crates/platform/src/hardware_encode.rs` |
| HEVC/H.265 | yes (Main, Main 10) | **hardware only**: NVENC on Windows writes Main 8-bit SDR and Main 10 HDR (PQ/HLG); VideoToolbox on macOS writes Main 8-bit SDR; **no HEVC encode on Linux**; no software encoder | `crates/hevc`, `crates/export/src/format.rs` (`Format::Hevc` docs), `crates/platform/src/nvenc/export.rs`, issue #30 |
| AV1 | yes (Main profile, 8/10-bit 4:2:0 + mono, film grain, superres) | **none** — no encoder or format probe is registered on any platform, so the `av1` Format is never available | `crates/av1`, `crates/export/src/format.rs` (`has_builtin_encoder`), `crates/platform/src/lib.rs` |
| VP8 / VP9 | yes (VP9 profiles 0–3, 8/10/12-bit, 4:2:0–4:4:4); both also read from MP4 | none | `crates/vp8`, `crates/vp9` |
| Apple ProRes | yes (Proxy…4444 XQ, alpha) | yes (presets 422/LT/HQ/4444/4444 with alpha/4444 XQ) | `crates/prores`, `crates/export/src/presets.rs` |
| Avid DNxHD/HR | yes (ST 2019-1, all CIDs) | yes (DNxHR LB/SQ/HQ/HQX in MOV/MXF) | `crates/dnx` |
| APV (RFC 9924) | yes | yes (422-10/422-12/444-10/444-12 profiles) | `crates/apv` |
| MJPEG | yes | yes | `crates/codecs` (AVI/QuickTime), `crates/export` |
| MPEG-1 / MPEG-2 video | yes | none | `crates/mpeg2v`, `crates/codecs/src/mpeg.rs` |
| Uncompressed RGB/YUV | yes (AVI) / Y4M | none (Y4M is read-only) | `crates/codecs/src/{avi,y4m}.rs` |
| DNG / CinemaDNG | yes (TIFF container, uncompressed, lossless JPEG and lossy JPEG Compression 34892) | none | `crates/dng` |

Exported ProRes flavours are selected by preset/profile; the export UI exposes the 422 family plus
4444 variants (`crates/export/src/presets.rs`).

Not decodable: DivX/Xvid (MPEG-4 Part 2), DV/DVCPRO, camera RAW other than DNG, HEIF/HEIC, AI/EPS and
ICO stills, JPEG 2000. 10-bit / 4:2:2 camera H.264 and HEVC need OS hardware decode — no software
fallback (`docs/gaps.md` G3).

## Audio codecs

The decoders and encoders come from **craft-audio** in craft-libs (`Cargo.toml` features
`aac-decode`, `aac-encode`, `ac3-decode`, `mpa-decode`, `opus-decode`, `flac-encode`); only the MP3
encoder is in this repo (`crates/mp3enc`). Their internals are not auditable here.

Decode: AAC-LC, AC-3, **E-AC-3 (partial — independent substream, 5.1 core; no AHT, enhanced coupling or
7.1 dependent substreams: `docs/codec-parity.md`; the README's "Not yet: … E-AC-3" line is imprecise)**,
Opus (SILK/CELT/hybrid/multistream), Vorbis, MP1/MP2/MP3, FLAC, ALAC, PCM, WAV/BWF.

Encode (`crates/export/src/lib.rs`): AAC-LC (MP4/MOV, `.m4a`, ADTS `.aac`), PCM (WAV/AIFF/MOV/MXF),
FLAC (RFC 9639, `flacLevel` 0–8), **MP3 (new in 0.20.1)**, and the audio inside
H.264/HEVC/ProRes/DNxHR/APV/MJPEG exports.

MP3 is a **CBR-only** stream from `crates/mp3enc`: 32–320 kbit/s at 32/44.1/48 kHz (MPEG-1) and
8–160 kbit/s at 16/22.05/24 kHz (MPEG-2 LSF), mono/stereo/joint stereo, bit reservoir bounded by the
decoder's 7680-bit buffer. No VBR, no short/mixed blocks, no `scfsi`/`preflag`, no intensity stereo, no
Xing/LAME gapless tag and no ID3 — a decoder starts with the encoder delay (`DELAY = 1057` samples, about
24 ms at 44.1 kHz). Export maps arbitrary settings onto valid ones with
`nearest_sample_rate` / `nearest_bitrate` (`crates/export/src/settings.rs`, `mp3_stream`).

Embedded audio extraction (AAF/OMF import) writes `name.wav`, then `name (2).wav`, `name (3).wav` … without
overwriting, and keeps the document's own path separators (backslash paths stay backslash paths)
(`crates/engine/src/interchange.rs`).

## Still images and sequences

Read: PNG, JPEG, GIF, WebP, TIFF, BMP, TGA (incl. RLE/colour maps), DPX (luma/RGB/RGBA, 8–16-bit, packed
10/12-bit, Y'CbCr), OpenEXR (scan-line: none/RLE/ZIPS/ZIP/PXR24, half/float/uint), Radiance HDR, DNG,
**PSD**. Animated GIF, APNG and animated WebP import as clips with transparency
(`crates/media/src/animated.rs`).

**PSD** (`crates/media/src/still/psd.rs`, present since v0.18.0 despite older docs): the flattened
composite only — grayscale (1 channel) or RGB (3), 8 or 16 bits per channel (16 kept at 8), raw or
PackBits rows, merged transparency only when the layer count is negative, unblended from white.
Refused with a message: PSB, bitmap, indexed, CMYK, multichannel, duotone, Lab, 32-bit, and documents
saved without "Maximize Compatibility" (version-info resource 1057 says the image data is not the real
composite). Layers are not read; there is no layer or sequence-of-layers import.

Write (as numbered sequences): PNG, TIFF, BMP, JPEG, TGA, DPX (10-bit), OpenEXR (half float, linear;
uncompressed/RLE/ZIPS/ZIP, or `alpha: true` for RGBA), plus animated GIF (binary transparency on export,
`crates/export/src/lib.rs`).

No HEIF/HEIC, AI/EPS, ICO, PIZ/B44/DWA/tiled/deep EXR (`docs/file-format-parity.md`).

## Captions and subtitles

`crates/captions/src/`: one module per format (srt, vtt, scc, mcc with 608+708, stl for EBU STL, ttml for
TTML/IMSC1/DFXP), plus cea608 and burn (layout + burn-in). Seven import/export formats —
`Format::ALL` (`crates/captions/src/lib.rs`) has all seven, plus caption *tracks* in Subtitle / CEA-608 /
CEA-708 / Teletext (`crates/project/src/caption.rs`).

`captions.import` auto-detects by extension and content and takes `name` and `language` (default: the file's
TTML `xml:lang`, else `en`); `captions.export` takes `format: "srt|vtt|scc|mcc|stl|ttml|dfxp"` or infers it
from the path, plus `track` and `dropFrame` (`crates/engine/src/captions.rs`). TTML and DFXP exports write
the track's language as `xml:lang`, and `captions.export` **warnings name every character the file cannot
carry** — SCC/MCC drop characters CEA-608 has no code for or substitute ASCII, and the CEA-708 service in
MCC substitutes `?` (`docs/captions.md`). The caption export dialog offers a track picker when the sequence
has more than one caption track (0.20.1). CEA-608/708 embedded in a video stream are **not** read or
written; use burn-in (`burnCaptions: true`) or a sidecar (`captionSidecar: "srt"|"vtt"`).

Caption editing at this tag: split (`captions.split`, also the Razor tool on a caption; Shift = every caption
track), merge, trim, move, duplicate (`captions.duplicate`, ⌥-drag), copy/cut/paste through
`edit.copy`/`edit.cut`/`edit.paste`/`edit.pasteInsert` when only captions are selected, delete (lift or
ripple; Select All + Delete removes clips and captions in one undo), per-track style and the Text panel
list that follows the playhead (`docs/captions.md`, `crates/engine/src/captions.rs`).

## Project file — `.fcproj`

- UTF-8 JSON envelope: `{"format": "filmcraft.project", "schema_version": 17, "generator": …, "project": {…}, "view": {…}}`
  (`crates/format/src/lib.rs`; `SCHEMA_VERSION = MIGRATIONS.len() + 1`, and a test asserts 17). Compact on write.
- **New in 0.20.1:** each sequence stores `settings.display` — the Video Display Format (`timecode`,
  `feet35`, `feet16`, `frames`). It is `#[serde(default)]`, so older files load as Timecode; it affects
  presentation, not any stored time (`crates/project/src/sequence.rs`, `crates/time/src/lib.rs`).
- Reading: `MIGRATIONS[i]` upgrades v*i+1* → v*i+2*; the current build reads **every version from 1 to 17**;
  newer versions are refused with an explicit message (`docs/project-files.md`). The first save over an
  upgraded project keeps `<name> (schema vN backup).fcproj`.
- The work area is part of the sequence (`Sequence::work_area`, `crates/project/src/lib.rs`) and feeds
  `range: "workArea"` exports.
- Load-time hardening: embedded LUT text over 8 MiB is dropped with a warning (`MAX_LUT_TEXT_BYTES`),
  media frame sizes are validated, audio-stream lists are truncated to the supported count, `next_id` is
  raised past the largest id in use (or the file is refused when the id space is exhausted), and pin
  chains in graphic templates are bounded to 256 links (0.20.1, `crates/project/src/graphic_design.rs`).
- `view` (open sequences, active sequence, zoom/scroll/playhead per sequence) sits beside the project, is
  not undoable and does not dirty the project.
- Media is by path only; each item also stores a size + first/last-MiB fingerprint (`MediaClip::identity`)
  used by relinking. Stored paths from documents are opened only when local or on the document's own
  network share (`crates/engine/src/doc_path.rs`, built on `craft-docpath`); other paths become offline
  items. Media-pool file I/O (Project Manager, proxies) uses the resolved path, not the stored string.
- Writes are atomic (temp in the same directory → fsync → rename → fsync dir) — projects, auto-saves,
  recovery snapshots, preferences (`docs/project-files.md`); `atomic_write_new` publishes extracted
  audio without replacing an occupied path (`crates/format/src/atomic.rs`).

Related files: auto-saves `Auto-Save/<name>-<timestamp>-<unix seconds>.fcproj`
(`crates/format/src/autosave.rs`; older `<name>-<timestamp>.fcproj` names still list); recovery
`Recovery/<started>-<pid>[-n]/{snapshot.fcproj,session.json,lock}`; preferences data-dir files:
preferences.json; effect-presets.json; export-presets.json; workspaces.json; graphics templates use the
`.fcgt` extension; label colour presets `<data dir>/Label Presets/*.json`. A screenshot requested
without a path goes to an owner-only temp folder (`private_temp_dir`), and the session-log / voice-over
fallbacks use it when no data directory is configured; the session log otherwise lands in `<data dir>/Logs`.

## Effect presets

User effect presets live in `<data dir>/presets.json`. FilmCraft also creates and scans
`<data dir>/Effect Presets` on start-up and whenever `presets.scan` runs, reading **Premiere Pro
`.prfpset`** (plain XML or gzip, a `<PremiereData>` document) and FilmCraft `.json` preset packs, with
their nested folder hierarchy, static parameters, animated keyframes, Bezier curves and keyframe
scaling/anchoring (`crates/engine/src/prfpset.rs`; `crates/engine/src/presets.rs`). The same files are
accepted by `presets.import` and by `file.import` (content sniffed, extension not trusted). One malformed
file is renamed `*.json.unreadable` rather than overwritten. Presets whose effects this build does not
have are reported, not silently dropped.

## Interchange

| Format | Extensions | Import | Export | Module |
|---|---|---|:--:|:--:|
| Final Cut Pro 7 XML (`xmeml` v4/v5) | `.xml` | yes | yes | `crates/interchange/src/fcp7.rs` |
| FCPXML 1.9–1.11 | `.fcpxml`, `.fcpxmld` | yes | yes | `crates/interchange/src/fcpxml.rs` |
| OpenTimelineIO | `.otio` | yes | yes | `crates/interchange/src/otio.rs` |
| CMX 3600 EDL | `.edl` | yes | yes | `crates/interchange/src/edl.rs` |
| AAF (Edit Protocol, MS-CFB) | `.aaf` | yes | yes | `crates/interchange/src/aaf/` (`crates/cfb`) |
| OMF Interchange 2.0 | `.omf`, `.omfi` | yes | yes | `crates/interchange/src/omf/` |
| Avid Log Exchange | `.ale` | no | yes | `crates/interchange/src/ale.rs` |
| Markers CSV | `.csv` | – | yes | `crates/engine/src/marker_export.rs` (100 000-marker / 16 MiB caps) |

Format detection sniffs content (AAF/OMF structured storage, `<xmeml`/`<fcpxml` headers, `"OTIO_SCHEMA"`)
before trusting the extension (`crates/interchange/src/lib.rs`). Imports merge as one undoable step
and return a report of everything that could not be represented; imported sequence settings are validated
before merge (`crates/engine/src/interchange.rs`). AAF/OMF have never been validated in Media
Composer / Pro Tools (`docs/gaps.md` G15). AAF/OMF export takes `bitDepth` 16 or 24 (`"24"` accepted as a
string) and **refuses anything else**; AAF top-level compositions carry the registered `Usage_TopLevel`;
EDL and OMF export reports **name the video tracks they leave out**; an EDL clip named only by clip name
is reported **missing** rather than offline; media an EDL names starts at 00:00:00:00 until linked, and
relinking it with **Align Timecode** lands on the file's own time; an OTIO item's sample rate no longer
sets the sequence rate. Effect names are written through `interchange_name`, so the Color Grading rename
did not change a byte of export (0.20.1).

## Export formats (`crates/export/src/format.rs`, 22 variants)

`h264`, `hevc*`, `av1*`, `prores`, `dnxhr`, `apv`, `mjpeg`, `png`, `tiff`, `bmp`, `jpg`, `tga`, `dpx`, `exr`,
`gif`, `wav`, `aiff`, `aac`, `mp3`, `flac`, `mxf-op1a`, `mxf-opatom`. `*` means "offered only when a platform
encoder registers one": HEVC has probes for VideoToolbox (macOS) and NVENC (Windows); **AV1 has no probe or
encoder anywhere, so it never becomes available** (`crates/export/src/format.rs`,
`crates/platform/src/lib.rs`). Ask the running app: `export.formats` returns `available` per format;
the Export UI greys unavailable formats with the reason (`crates/ui-egui/src/panels/export_mode.rs`,
`unavailable_why`).

Container by format: MP4/MOV (H.264, HEVC, AV1, ProRes, DNxHR, APV, MJPEG), MXF OP1a (DNxHR, ProRes,
H.264 + PCM, start timecode), MXF OP-Atom (picture + one mono PCM file per channel;
`opatom_audio_paths`), numbered stills, GIF, WAV/AIFF/AAC/MP3/FLAC.

**45 built-in presets** (`crates/export/src/presets.rs`; default
`"Match Source – Adaptive High Bitrate"`): Match Source Adaptive High/Medium/Low, High Quality
1080p/2160p, YouTube 1080p/2160p, Vimeo 1080p/2160p, Social Vertical 1080×1920, TikTok 1080×1920,
Instagram Reels 1080×1920, YouTube Shorts 1080×1920, Apple ProRes 422
HQ/422/LT/Proxy/4444/4444 with Alpha/4444 XQ, Avid DNxHR HQ/SQ/LB, H.264 High 10 Master, H.264
High 10 Intra, APV 422-10/422-12, MXF OP1a DNxHR
HQ/ProRes 422 HQ/H.264, MXF OP-Atom DNxHR (Avid), PNG/TIFF/BMP/JPEG/Targa/DPX/OpenEXR Sequences, Animated GIF
640×360, Waveform Audio 48 kHz 16-bit/24-bit, AIFF 48 kHz 16-bit, AAC Audio 48 kHz 320 kbps, **MP3 48 kHz
320 kbps** (0.20.1), FLAC 48 kHz 24-bit. `docs/roadmap.md` M6 still says "24 built-in presets" — stale.

H.264 encode profiles are selectable on `file.exportMedia` (`h264Profile: baseline|main|high|high10`,
`h264IntraOnly`): High 10 writes 10-bit 4:2:0 into MP4/MOV and MXF OP1a (`profile_idc` 110). HDR exports
keep their 10-bit precision; SDR sources are rendered at 8 bits first. High 4:2:2, High 4:4:4 Predictive
and lossless H.264 remain absent. MP3 takes `audioCodec: "mp3"` (the enum accepts it even though the
parameter doc string still omits it) and ignores a sample size.

A format may change the output extension: exporting `out.mp4` as APV writes `out.mp4.mov`
(`apps/filmcraft-cli/src/main.rs`, `written_paths`) — always read the returned `path`. A **still
sequence never writes the path it is given**: `a.png` writes `a000.png`, `a001.png`…, and the result
carries `path` (first still), `lastPath` (last still) and `basePath` (the name they are numbered from,
which `file.import` takes back as the sequence) (`crates/engine/src/export_tools.rs`).

Ranges: `entire`, `inOut`, `workArea` (needs a work area; see `sequence.workAreaBar` /
`sequence.setWorkArea*`) and `custom` (`startSeconds`/`endSeconds`). `sdr: true` tone-maps an HDR sequence
to SDR (`crates/engine/src/export_tools.rs`).

## Colour management (relevant to formats)

Working spaces Rec. 709 / Rec. 2100 PQ / HLG with wide gamut and auto tone mapping
(`sequence.colorSettings`, `clip.interpretFootage`, `color.spaces`), HDR signalling on export, and **10
camera log curves** in `LogCurve::ALL` (`crates/color/src/log.rs`): S-Log3, V-Log, Canon Log 2/3,
LogC3, LogC4, Apple Log, D-Log, Fujifilm F-Log and F-Log2. LUTs are `.cube` (1D/3D/shaper) and `.3dl`,
stored in the project (`lut.*`) with an 8 MiB per-entry text limit. `lumetri.exportCube` samples a clip's
Color Grading pipeline into a `.cube` (2..65 lattice, default 33) and names what a LUT cannot hold.

## Proxies, ingest, Project Manager

Proxy presets (`crates/engine/src/proxies.rs`): `prores_proxy_quarter` (default), `prores_proxy_half`,
`prores_lt_half`, `h264_quarter`, `h264_half`; written to `<media folder>/Proxies/<name>_Proxy.<ext>`.

Ingest actions: `copy`, `transcode`, `createProxies`, `copyAndCreateProxies` (`project.ingestSettings`).
Project Manager modes `collect` and `consolidate` (the latter also accepts `transcode`) with `handles`
(frames, default 30), transcode presets `prores_lt`/`prores_hq`/`h264`, `dryRun` returning the plan and disk
estimate (`crates/engine/src/project_manager.rs`). Exports always use full resolution, never the proxy
(`docs/project-files.md`). A reserved proxy output is removed only if it is still the file the job wrote,
and a finished proxy is applied only when its item still points at the source it was made from (0.20.1).
