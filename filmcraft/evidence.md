# FilmCraft — evidence ledger (tag v0.20.1)

Audit basis: this checkout is tag **`v0.20.1`**, commit **`cedf0c9bd060eb06a977d532402be2097c9ebe42`**
("Merge tested main for v0.20.1"); the previous skill was pinned at v0.18.0 =
`015d5b3ea37e1202a529e6245d3cc021c8c16ffd`. The installed bundle reports `filmcraft 0.20.1` from
`--version` (and prints the same `--help` text as `apps/filmcraft/src/args.rs`); `Info.plist` has
CFBundleShortVersionString `0.20.1`, CFBundleIdentifier `ai.storyteller.filmcraft`, minimum macOS
11.0. Inspection date **2026-11-12**. The GUI was never launched; only `--version`, `--help` and
plist reads were used.

Round shape: `git rev-list --count v0.18.0..HEAD` = **1** (the checkout squashes the release), so the
round is measured as a tree diff — `git diff --shortstat v0.18.0..HEAD` = **433 files changed,
17 709 insertions, 23 234 deletions**. The deletions are mostly the six audio/container crates that
moved to craft-libs.

## 1. Capability claims → evidence → tier

| # | Claim (v0.20.1 unless stated) | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | MP3 export from an in-repo Layer III encoder | `crates/export/src/mp3_out.rs`; `crates/mp3enc/` (`Config::cbr`, `DELAY = 1057`); `Format::Mp3` in `crates/export/src/format.rs` | implemented |
| 2 | Export formats 22; presets 45 (new "MP3 48 kHz 320 kbps") | `crates/export/src/format.rs` (`ALL: [Format; 22]`); `crates/export/src/presets.rs` (`p(` entries of `builtin_presets`) | implemented |
| 3 | New query `lumetri.exportCube`: a clip's grade as a 3D `.cube` | `crates/engine/src/color.rs` (`export_cube`, params `{clip?, path, size=33}`); `crates/render/src/lumetri_cube.rs` | implemented |
| 4 | Naming migration: effect/panel labels are descriptive, ids stable, old names are aliases, interchange unchanged | `crates/project/src/effect.rs` (`find_effect_by_name`, `search_aliases`, `interchange_name`); `crates/ui-egui/src/dock.rs` (`title`, `from_name`); `crates/engine/src/shortcuts.rs` (`PANELS`, `check_panel`); `docs/feature-naming.md` | implemented |
| 5 | Sequence Video Display Format: Timecode / Feet + Frames 35mm / 16mm / Frames | `crates/time/src/lib.rs` (`TimeDisplay`, `VIDEO`, `frames_per_foot`); `crates/project/src/sequence.rs` (`settings.display`, serde default); `crates/engine/src/commands.rs` (`sequence.settings.videoDisplay`) | implemented |
| 6 | Timecode effect has a Time Format choice | `crates/project/src/effect/vfx.rs` (`ch("time_format", …)`) | implemented |
| 7 | `file.newSequence` and the `File ▸ New` item commands take `bin`; an unknown bin is an error | `crates/engine/src/commands.rs` (`bin_p`, params strings) | implemented |
| 8 | Named target keys (`clips`/`clip`/`items`/`item`) are declared on the command spec and tested | `crates/engine/src/commands.rs` (`NamedKeys`, `command_specs`); `crates/engine/src/named_targets_tests.rs` | implemented |
| 9 | Select All also selects captions; Clear / Ripple Delete remove clips and captions in one undo | `crates/engine/src/commands.rs` (`edit.selectAll`, `deletes`), `crates/engine/src/clip_ops.rs` | implemented |
| 10 | A screenshot without `path` is written to a private temp dir; session log and voice-over fall back to it when no data dir is set | `crates/engine/src/lib.rs` (`private_temp_dir`); `crates/ui-egui/src/control.rs`; `crates/ui-egui/src/panels/menu_dialogs.rs` (`logs_dir`); `crates/engine/src/voiceover.rs` (`media_dir`) | implemented |
| 11 | PSD stills open as the flattened composite (8/16-bit grey or RGB, raw/PackBits) | `crates/media/src/lib.rs` (`STILL_EXTENSIONS` includes `psd`); `crates/media/src/still/psd.rs` (`sniff`, `decode`); refusals named in its module doc | implemented |
| 12 | Audio codecs (AAC, AC-3/E-AC-3, MP1/MP2, Opus, FLAC) and Ogg come from craft-libs at one pin | `Cargo.toml` (`craft-audio` features, `craft-media`, `rev = "b72cb4d6…"`); `docs/architecture.md`; `crates/*/Cargo.toml` re-exports | implemented (not auditable beyond the pin) |
| 13 | DNG raw development settings and opcode lists exist in the crate only | `crates/dng/src/options.rs` (`ProcessOptions`), `crates/dng/src/opcode.rs`; app import still `filmcraft_dng::decode` in `crates/media/src/still/dng.rs` | crate-only, not wired into the app |
| 14 | `--graphics low-power` (Linux) exists; usage text matches the binary | `apps/filmcraft/src/args.rs` (`USAGE`, `graphics_mode`); live `--help` run of the installed binary | implemented |
| 15 | The mixer graph refuses absurd total latency / compensation delays; audio buffers are bounded | `crates/render/src/mixer.rs` (`MAX_GRAPH_LATENCY_S`, graph state `None` past the limits), `crates/media/src/generators.rs` (`validate_audio_buffer_shape`), `crates/export/src/run.rs` | implemented |
| 16 | Previews stream to disk one second at a time and use a unique part file | `crates/engine/src/previews.rs` (`wav_header_f32`, part names with pid + counter) | implemented |
| 17 | Proxy jobs remember the source they started from and do not apply to relinked media | `crates/engine/src/proxies.rs` (`started_from`, `source_durations`) | implemented |
| 18 | 17 MCP tools + 2 resources, unchanged | `crates/automation/src/server.rs` (17 `#[tool(`, `filmcraft://document`, `filmcraft://commands`) | implemented |
| 19 | 24 control methods, unchanged (only the default screenshot path moved) | `crates/ui-egui/src/control.rs`; `docs/control-protocol.md` | implemented |
| 20 | 13 CLI subcommand words; `mp3` added to `--format` and the extension guess | `apps/filmcraft-cli/src/main.rs` (`HELP`, dispatch, `format_for`) | implemented |
| 21 | 28 panels, 10 workspaces, panel names accept old and new labels | `crates/ui-egui/src/dock.rs` (`PanelKind::ALL`, `WORKSPACES`, `from_name`) | implemented |
| 22 | 17 UI languages (16 catalogues + English); the new labels are translated | `crates/ui-egui/src/i18n/*.tsv` (16 files, e.g. `de.tsv` "Color Grading", `tr.tsv` "Harici Video Çıkışını Etkinleştir") | implemented |
| 23 | Project schema 17; `display` is a defaulted field, so old files load | `crates/format/src/lib.rs` (`assert_eq!(SCHEMA_VERSION, 17)`); `crates/project/src/sequence.rs` | implemented |
| 24 | 7 caption formats, 112 transitions, 27 blend modes, 10 log curves, 4 shortcut presets | `crates/captions/src/lib.rs`; `crates/project/src/vtransition.rs` (`tr(`); `crates/project/src/effect.rs` (`BLEND_MODES`); `crates/color/src/log.rs`; `crates/engine/src/shortcuts.rs` | implemented |
| 25 | No `.prproj`, no plug-ins, AV1 has no encoder, HEVC hardware-only, DNG-only raw, no captions in the video stream, one project at a time, STT/Kokoro off in releases | `docs/gaps.md`; `crates/export/src/format.rs` (`has_builtin_encoder`); `crates/codecs`; packaging scripts pass no features | not implemented (verified absent) |

## 2. Count methods used this round

| Surface | v0.18.0 | v0.20.1 | Method |
|---|---:|---:|---|
| Engine command ids | 398 | **399** (+`lumetri.exportCube`, 0 removed) | First string literal of every `cmd!`/`query!`/`spec(`/`query(` call plus every `CommandSpec { id: "…" }` literal under `crates/engine/src`, tests excluded; set difference. `uic!` UI-only ids: 223 at both tags |
| CLI subcommand words | 13 | **13** | `HELP` block + dispatch words in `apps/filmcraft-cli/src/main.rs` (`version` and `help` are words in the subcommand position) |
| MCP tools / resources | 17 / 2 | **17 / 2** | `grep -c '#\[tool('` in `crates/automation/src/server.rs`; resource URIs at the server builder |
| Control methods | 24 | **24** | Method-name arms in `crates/ui-egui/src/control.rs`, expanded across the `|` alternatives |
| Export formats | 21 | **22** | `Format::ALL: [Format; 22]` in `crates/export/src/format.rs` |
| Built-in presets | 44 | **45** | `p(` entries inside `builtin_presets` in `crates/export/src/presets.rs` |
| Panels / workspaces | 28 / 10 | **28 / 10** | `PanelKind::ALL: [PanelKind; 28]`, `WORKSPACES: [&str; 10]` in `crates/ui-egui/src/dock.rs` |
| UI languages | 17 | **17** | `ls crates/ui-egui/src/i18n/*.tsv` = 16 + English |
| Project schema | 17 | **17** | `SCHEMA_VERSION = MIGRATIONS.len() + 1` with `assert_eq!(SCHEMA_VERSION, 17)` |
| Caption formats | 7 | **7** | `Format::ALL: [Format; 7]` in `crates/captions/src/lib.rs` |
| Blend modes / log curves | 27 / 10 | **27 / 10** | `BLEND_MODES` entries; `LogCurve::ALL: [LogCurve; 10]` |
| Transitions | 112 | **112** | `tr(` definitions in `crates/project/src/vtransition.rs` = 84 current in 10 folders + 21 Legacy + 7 Obsolete |
| Shortcut presets | 4 | **4** | `BUILTIN_PRESETS: [&str; 4]` in `crates/engine/src/shortcuts.rs` |
| Effect catalogue | 93 video / 16 folders, 53 audio | **93 / 16, 53 (unchanged)** | Video: the `CATALOGUE` table in `crates/project/src/effect/vfx.rs`, names per folder summed (16 folders, 93 names at both tags). Audio: `PREMIERE_AUDIO_EFFECTS: [&str; 53]` in `crates/project/src/effect/audio.rs`. Definition id set across `crates/project/src/{effect,graphic,vtransition}.rs` and `effect/{vfx,audio}.rs`: 170 ids at both tags, 0 added, 0 removed |

## 3. Carried forward, not re-derived

- Deep feature prose (trimming, multicam, Essential Sound, proxies / ingest / Project Manager,
  GPU/CPU rendering, export ranges, interchange matrix) was path-verified and carried; this is a
  pin-and-verify refresh, not a new feature audit.
- The limitation list was checked against `docs/gaps.md` at this tag; the MP3 and PSD rows were
  changed because the code moved.

## 4. Uncertain / not verified

- **No runtime enumeration.** The macOS bundle ships only the GUI binary (no `filmcraft-cli`), so
  `filmcraft-cli commands`, `describe`, `export --list-presets` and MCP `command_list` were not run.
  Static extraction is the authority quoted here; the runtime list remains the final word.
- **GUI behaviour not observed.** The Feet + Frames ruler, the caption track picker and the renamed
  panels are read from code and their tests, not seen.
- **Moved codec code.** AAC/AC-3/MPA/Opus/FLAC and the Ogg demuxer now live in craft-libs; only the
  pin (`b72cb4d6…`) and the feature list are auditable here. Do not attribute their internals to this
  repository.
- **`audioCodec` doc drift.** The parameter string says `auto|aac|pcm|flac`, but the enum
  (`crates/export/src/settings.rs`) also accepts `mp3`; the error text repeats the stale list. Treat
  `mp3` as accepted (serde) and the doc string as behind.
- **DNG `Highlights::Recover`** is accepted but develops like `Clip` (`crates/dng/src/options.rs`).
- **`docs/file-format-parity.md` and `docs/gaps.md` still list OpenEXR PXR24** in one place and refuse
  it in another; the decoder handles code 5 as PXR24 (`crates/media/src/still/exr.rs`), and the
  refusal message's label table is off by one. Not re-tested with a real file this round.

## 5. Doc-vs-code drift found at this tag (code wins)

| Doc / previous-skill statement | Code reality |
|---|---|
| README "26 blend modes", "around 30 transitions" | 27 blend modes; 84 transitions + 21 Legacy (+7 Obsolete) |
| README "H.264 is our only software delivery-codec export" | Built-in encoders: H.264 (up to High 10), ProRes, DNxHR, APV, MJPEG, stills, WAV/AIFF/AAC/FLAC and now MP3 |
| `docs/roadmap.md` M6 "24 built-in presets" | 45 built-in presets |
| `docs/gaps.md` G13 lists "MP3 audio" as missing in the leftover sentence | MP3 export exists (CBR only) and the same entry says so |
| Previous skill: "Stills that will not open: PSD" | PSD opens (flattened composite); HEIF/HEIC, AI/EPS and ICO still do not |
| Previous skill: craft-libs at `c5a1cbfb…` | One pin, `b72cb4d6…`, for `craft-docpath`, `craft-media`, `craft-audio`, `craft-ui`, `craft-update` (`Cargo.toml`) |
| Previous skill: `Lumetri Color` / `Lumetri Scopes` panels | Displayed as Color Grading / Video Scopes; old names still resolve; "Enable External Video Output" is a renamed preference with nothing behind it (`crates/engine/src/settings/schema.rs`) |
| `file.exportMedia` param doc `audioCodec: auto|aac|pcm|flac` | Enum also accepts `mp3` |
| Command params for `file.new*` had no bin | `bin: binId?` on `file.newSequence` and the `File ▸ New` item commands (not on `file.newBin`, which takes `parent`) |

## 6. Verification commands (read-only, re-runnable)

```sh
git -C <clone> rev-parse HEAD                                  # cedf0c9bd060eb06a977d532402be2097c9ebe42
git -C <clone> describe --tags --exact-match HEAD              # v0.20.1
git -C <clone> diff --shortstat v0.18.0..HEAD                  # 433 files changed, +17709/-23234
grep -n 'ALL: \[Format; 22\]' crates/export/src/format.rs
grep -c '^\s*p(' crates/export/src/presets.rs                   # 45
grep -c '#\[tool(' crates/automation/src/server.rs              # 17
grep -n 'PanelKind::ALL: \[PanelKind; 28\]' crates/ui-egui/src/dock.rs
grep -n 'WORKSPACES: \[&str; 10\]' crates/ui-egui/src/dock.rs
ls crates/ui-egui/src/i18n/*.tsv | wc -l                        # 16 catalogues (+English)
grep -n 'assert_eq!(SCHEMA_VERSION, 17)' crates/format/src/lib.rs
grep -n 'Format::ALL: \[Format; 7\]' crates/captions/src/lib.rs
grep -c '^\s*tr(' crates/project/src/vtransition.rs              # 112
grep -oE 'rev = "[0-9a-f]{8}' Cargo.toml | sort -u               # b72cb4d6
grep -n 'pub struct NamedKeys' crates/engine/src/commands.rs
grep -n 'pub fn interchange_name' crates/project/src/effect.rs
grep -n 'pub enum TimeDisplay' crates/time/src/lib.rs
"<installed app binary>" --version                               # filmcraft 0.20.1 (version query only)
```
