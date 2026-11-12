# FilmCraft — round 2026-11-12 changes

Re-pinned: v0.18.0 (`015d5b3`) -> v0.20.1 (`cedf0c9`, installed `filmcraft 0.20.1`).

## Corrected / re-measured

- **Export formats 21 -> 22.** The new variant is `Format::Mp3` (`crates/export/src/format.rs`,
  `ALL: [Format; 22]`), written by a new in-repo encoder crate `crates/mp3enc` through
  `crates/export/src/mp3_out.rs`. CBR only, 16-48 kHz, mono or stereo, no ID3 or gapless tag
  (`crates/mp3enc/README.md` "Not yet"). CLI `--format mp3` and the `.mp3` extension guess were added
  (`apps/filmcraft-cli/src/main.rs`).
- **Built-in export presets 44 -> 45**: one new preset, "MP3 48 kHz 320 kbps"
  (`crates/export/src/presets.rs`, counted as the `p(` entries of `builtin_presets`).
- **Engine command ids 398 -> 399**: added **`lumetri.exportCube`**, removed none. It bakes a clip's
  Color Grading pipeline to a 3D `.cube` LUT (default size 33), samples it at the playhead and names
  what a LUT cannot hold in `leftOut` (`crates/engine/src/color.rs`, `crates/render/src/lumetri_cube.rs`).
- **The feature-naming migration landed.** Display labels changed, ids did not:
  effect `lumetri` "Lumetri Color" -> **Color Grading**; panels "Lumetri Color" -> **Color Grading**
  and "Lumetri Scopes" -> **Video Scopes**; the presets folder shows **Color Grading Presets** under
  the unchanged key `Lumetri Presets`; the preference is now **Enable External Video Output**
  (`playback.enableTransmit`). Old names stay lookup aliases for effects, panels and shortcut imports,
  and FCP7/FCPXML/EDL keep writing `Lumetri Color` so exports are byte-identical
  (`docs/feature-naming.md`, `crates/project/src/effect.rs` `find_effect_by_name` /
  `interchange_name`, `crates/ui-egui/src/dock.rs`, `crates/engine/src/shortcuts.rs`).
- **PSD stills open — the previous limitation was wrong.** `psd` was already in
  `STILL_EXTENSIONS` at v0.18.0 and `crates/media/src/still/psd.rs` decodes the flattened composite
  (grayscale/RGB, 8 or 16 bits kept at 8, raw or PackBits, merged transparency unblended from white).
  The skill no longer lists PSD as unreadable; what stays absent is layers, PSB, CMYK, Lab, indexed,
  32-bit and ZIP-compressed documents (`docs/file-format-parity.md:57`).
- **Video Display Format is a sequence setting.** `sequence.settings` accepts
  `videoDisplay: timecode|feet35|feet16|frames`; `SequenceSettings::display` is new and files from
  before it load as Timecode. The Timecode effect gained a `time_format` choice with the same four
  options (`crates/time/src/lib.rs` `TimeDisplay`, `crates/project/src/sequence.rs`,
  `crates/project/src/effect/vfx.rs`). Project schema is still 17: the field is `#[serde(default)]`.
- **New items can be created inside a bin.** `file.newSequence` and every `File ▸ New` item command
  (`newAdjustmentLayer`, `newBarsAndTone`, `newBlackVideo`, `newColorMatte`, `newCountingLeader`,
  `newTransparentVideo`) accepts `bin: binId`; a bin that does not exist is an error, not a silent
  fall back to the root (`crates/engine/src/commands.rs`, `crates/engine/src/named_targets_tests.rs`).
  `file.newSequenceFromClip` and `file.newBin` keep their existing parameters (`items`, `parent`).
- **Named targets are declared, not inferred from prose.** `CommandSpec` carries `NamedKeys`
  (`clips`/`clip`/`items`/`item`) derived from the parameter doc, and a differential test enforces
  that a command documenting a key really reads it (`crates/engine/src/commands.rs`). The
  `command.list` JSON shape is unchanged; agents see the same `params` string.
- **A screenshot without `path` goes to a private temp folder.** `ui.screenshot` with no `path` is
  written to an owner-only `FilmCraft-<nonce>` folder under the engine temp dir
  (`private_temp_dir`, `crates/engine/src/lib.rs`; `crates/ui-egui/src/control.rs`), and the
  session-log / voice-over fallbacks use that folder instead of the shared temp dir when no data
  directory is configured (`crates/ui-egui/src/panels/menu_dialogs.rs` `logs_dir`,
  `crates/engine/src/voiceover.rs` `media_dir`).
- **Audio codecs and Ogg changed owner.** AAC, AC-3/E-AC-3, MP1/MP2, Opus, FLAC and the Ogg demuxer
  moved to craft-libs (`craft-audio`, `craft-media`); the per-codec crates `aac`, `ac3`, `mpa`, `opus`, `flac`,
  `ogg` are deleted here and the whole craft-libs pin moved from `c5a1cbfb…` to **`b72cb4d6…`**
  (`Cargo.toml`, `docs/architecture.md`). Container/codec behaviour beyond the re-export is not
  auditable in this repo.
- **`--graphics low-power`** joins the modes (Linux integrated GPU); `--help` was run live and prints
  it (`apps/filmcraft/src/args.rs`).
- **DNG raw development settings exist only in the crate.** `ProcessOptions` (white balance,
  exposure, highlights, demosaic quality, `target_size`, `apply_opcodes`) and the opcode lists are new
  in `crates/dng`, but the app still imports through `filmcraft_dng::decode` and exposes no raw
  controls (`crates/media/src/still/dng.rs`); `Highlights::Recover` develops like `Clip`.
- **"H.264 is our only software delivery codec" was already stale** in the README; the skill keeps
  saying the built-in encoders cover H.264 (up to High 10), ProRes, DNxHR, APV, MJPEG, the still
  formats and now MP3.
- **Caption export UI gained a track picker** when the sequence has more than one caption track
  (`docs/captions.md`, `crates/ui-egui/src/panels/caption_export.rs`); the engine formats and
  commands are unchanged.

Counts that did **not** move at v0.20.1, stated as such in the skill: CLI subcommand words 13, MCP
tools 17 + 2 resources, control methods 24, panels 28, workspaces 10, UI languages 17, project schema
17, caption formats 7, transitions 112 (84 current + 21 Legacy + 7 Obsolete), blend modes 27, camera
log curves 10, shortcut presets 4, effect catalogue (93 video across 16 folders, 53 audio).

## Method

- Audit basis from `git rev-parse HEAD` = `cedf0c9bd060eb06a977d532402be2097c9ebe42` (tag `v0.20.1`,
  one squashed release commit). The installed bundle prints `filmcraft 0.20.1`, `--help` matches the
  source, and `Info.plist` says 0.20.1 / `ai.storyteller.filmcraft` / macOS 11.0. The GUI was never
  launched.
- Round is a tree diff (the checkout squashes the release): `git diff --shortstat v0.18.0..HEAD` =
  **433 files changed, 17 709 insertions, 23 234 deletions** — the deletions are mostly the six codec
  crates that moved to craft-libs.
- Counts are code reads at this tag: `Format::ALL` (22); `builtin_presets` `p(` calls (45);
  `grep -c '#\[tool('` in `crates/automation/src/server.rs` (17) plus the two resource URIs; control
  dispatch arms in `crates/ui-egui/src/control.rs` (24 method names); CLI `HELP` + dispatch (13
  words); `WORKSPACES: [&str; 10]` and `PanelKind::ALL: [PanelKind; 28]` in `crates/ui-egui/src/dock.rs`;
  `ls crates/ui-egui/src/i18n/*.tsv` (16) + English; `assert_eq!(SCHEMA_VERSION, 17)`;
  captions `Format::ALL: [Format; 7]`; `BLEND_MODES` (27); `LogCurve::ALL: [LogCurve; 10]`;
  `tr(` in `crates/project/src/vtransition.rs` (112); `BUILTIN_PRESETS: [&str; 4]`.
- Command-id delta by the same extraction at both tags: first string literal of every
  `cmd!`/`query!`/`spec(`/`query(` invocation plus every `CommandSpec { id: "…" }` literal under
  `crates/engine/src` (tests excluded). Set diff v0.18.0 -> v0.20.1: added `lumetri.exportCube`,
  removed nothing. UI-only ids (`uic!`) stayed at 223, no addition.
- Effect catalogue: the `CATALOGUE` table in `crates/project/src/effect/vfx.rs` sums to **16 folders /
  93 video effects** at both tags and `PREMIERE_AUDIO_EFFECTS: [&str; 53]` covers the audio set. The
  definition id set over `crates/project/src/effect.rs`, `crates/project/src/effect/vfx.rs`,
  `crates/project/src/effect/audio.rs`, `crates/project/src/vtransition.rs`
  and `crates/project/src/graphic.rs` is identical at both tags
  (170 `video(`/`audio(` ids, 0 added, 0 removed); `vfx.rs` changed one Timecode parameter and one
  test label, `effect.rs` only the label/alias/interchange-name work.
- Every repo path cited in `SKILL.md`, `evidence.md` and `references/` was re-resolved against this
  checkout.

## Unchanged

- Import tables (extensions, container openers, decoded video/audio), the interchange matrix, the
  project format and migration chain, proxies / ingest / Project Manager, and the automation
  transports (CLI, control channel with its mandatory 64-hex token, MCP on stdio) — path-verified and
  carried.
- Limitations: no `.prproj`, no plug-in hosting, AV1 has no encoder, HEVC is hardware-only, camera raw
  is DNG only, no captions in the video stream, one project at a time, speech-to-text and Kokoro TTS
  off in official builds.
- The `.prfpset` effect-preset import and the preset scan folder (`crates/engine/src/prfpset.rs`,
  `presets.rs`) — untouched this round.

## Known gap in this round

- No runtime enumeration: the macOS bundle ships only the GUI binary, so `filmcraft-cli commands`,
  `describe` and MCP `command_list` were not run. The registry total is a static extraction, and the
  catalogue totals above are dated bottles, not fresh enumerations.
- The GUI was not launched: panel behaviour, the new Feet + Frames ruler and the Effect Controls
  fixes are read from code and tests, not observed.
- Deep feature prose (trimming, multicam, Essential Sound, GPU/CPU rendering, export ranges) was
  path-checked and carried, not re-derived statement by statement.
- craft-libs was consulted only for the `craft-web-api` page surface and the pin; the moved codec
  behaviour is not auditable in this repository.
