# SoundCraft — evidence ledger (tag v0.20.1)

Audit basis: this checkout is the release tag **`v0.20.1`**, commit
**`a52bbdccbe15342f44e0de1906bf71a621e7a68f`** (`git rev-parse HEAD`); inspection date
**2026-11-12**. The clone is shallow and carries only the v0.18.0 and v0.20.1 tag objects, so
`git diff v0.18.0..HEAD` runs here but the v0.19.x/v0.20.0 commits do not. The installed bundle's
read-only `--version` prints `soundcraft 0.20.1 (macos aarch64)`
(`CFBundleShortVersionString` 0.20.1, `CFBundleIdentifier` `ai.storyteller.soundcraft`); only
`--version` and `--help` were run and the GUI was never launched. The previous ledger described
v0.18.0 (`5ff012ab88490cdfc635ee304c1019885e1b880d`).

v0.18.0 → v0.20.1 delta, measured here: **171 files changed, +3,824/−5,732** (`git diff
v0.18.0..HEAD --stat`). Most deletions are `crates/audio-io` (31 files), removed when audio formats
moved to the shared `craft-audio` crate. The engine command-id set is **unchanged at 484**: the same
multiline-aware extraction over a `git archive v0.18.0` tree and over HEAD returns 389 literal ids +
94 helper-macro ids + 1 direct `CommandSpec` both times, and the complete dotted-id literal set
(553 distinct strings, including aliases and parameter keys) diffs clean. The UI registry is
**unchanged at 70**, with an identical sorted id list, so a running app's `engine.commands` reply stays
**554**. MCP (17 tools + 2 resources), control methods (17 + 2 aliases) and CLI subcommands (10) did
not move; the CLI gained no subcommand, only flags inside existing ones (`--in-place` on
`convert`/`run`/`script`, `--compact` on `info`/`run`/`script`/`commands`/`describe`/`app`). Behaviour: formats from craft-audio with a seventh write
alias (`aifc`), defensive exports (exclusive part files, hard-link refusal, clip-name skipping),
the 128-fold import growth guard, locked clips kept whole on edits, per-sample volume automation,
hosted-instrument latency compensation, new Smart Tool/zoom/arrow shortcuts, descriptive display
labels with five disabled placeholders, and updater result states.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | **484 engine command specs, unchanged v0.18.0 → v0.20.1** | 389 non-test literal `cmd!(` ids + helper macros `toggle!` 17 / `flag!` 61 / `radio!` 6 / `option!` 10 + 1 direct `CommandSpec` (`crates/engine/src/cmd/plugin_state.rs`) = 484; 32 production modules registered by `command_specs()` (`crates/engine/src/cmd.rs`); id literals diffed clean against the v0.18.0 tag tree | implemented (unchanged at this tag) |
| 2 | 70 UI commands, unchanged; 554 live ids with no overlap | `crates/ui-egui/src/menus.rs` `UI_COMMANDS`; `crates/ui-egui/src/control.rs::command_list` appends them to the engine list; per-UI-id `grep -F` over `crates/engine/src` found no shared id | implemented (unchanged) |
| 3 | 10 CLI subcommands; new/omitted flags are inside existing ones: `convert --in-place`, `info --compact`, `run`/`script --inspect --compact --in-place`, `app --compact` | `apps/soundcraft-cli/src/args.rs` (10 `Command` variants; `ConvertArgs::in_place`, `EngineArgs::compact/in_place`, `AppArgs::compact`); `apps/soundcraft-cli/src/catalog.rs` (`commands --json`) | implemented (flag corrections) |
| 4 | 17 MCP tools + 2 resources, protocol `2025-06-18`, batch cap 1000 | `crates/automation/src/mcp.rs` (17 `tool(` names; `soundcraft://session`, `soundcraft://commands`; `MAX_BATCH_CALLS = 1000`) | implemented (unchanged) |
| 5 | 17 control methods (+2 aliases), screenshot binding/errors, MCP-only path roots | `crates/ui-egui/src/control.rs` dispatch; `crates/automation/src/args.rs` (roots); `crates/engine/src/file_access.rs` | implemented (unchanged) |
| 6 | **Audio formats come from `craft-audio`; `crates/audio-io` is gone; write aliases are 7 incl. `aifc`; new import formats Opus, AC-3/E-AC-3, MOV/MKA audio** | `Cargo.toml` (craft-audio at `75895c…`, features `decode`, `lossless-encode`, `peaks`, `serde`); `crates/model/src/source.rs` (`FileFormat::of`); `apps/soundcraft-cli/src/args.rs` (help from `DECODE_EXTENSIONS`/`ENCODE_EXTENSIONS`); `apps/soundcraft-cli/tests/it/behaviour.rs` asserts `wav, wave, bwf, aif, aiff, aifc, flac`; `docs/file-format-parity.md` revision row | implemented (new in the v0.18.0→v0.20.1 delta) |
| 7 | **Exports are defensive**: exclusive part files; `write_file` follows symlinks but refuses dangling links, non-regular/read-only files and hard links; bounces/saves rename a fresh part; Export Clips skips occupied names and numbers a same-named run once | `crates/engine/src/io.rs` (`create_new`, `write_synced`, `write_file`, `write_export_checked`, `export_clips`, `clip_file`, `ClipNames`); tests `exclusive_tests`, `export_replacement_tests` | implemented (new in the v0.18.0→v0.20.1 delta) |
| 8 | **Import refuses >128-fold sample-rate growth** and the ~4 GiB f32 cap; session load, clip-group import and Sampler share it | `crates/engine/src/io/import.rs` (`MAX_RATE_EXPANSION = 128`, `at_rate`, `RateError`); `crates/engine/src/io/session.rs`; `crates/engine/src/cmd/sampler.rs`; `crates/engine/src/clip_group_file.rs` | implemented (guard new in the v0.18.0→v0.20.1 delta) |
| 9 | **Time- and edit-locked clips keep their extent** on Separate, Trim and range edits; Event Time Insert/Cut split locked clips first; Strip Silence cuts all points in one pass | `crates/engine/src/edit.rs` (`separate_at_if`, `separate_all_at`, `separate_at_points`, `trim_to`/`trim_start_to`/`trim_end_to`); `crates/engine/src/cmd/event.rs`; `crates/engine/src/io/strip.rs` | implemented (new in the v0.18.0→v0.20.1 delta) |
| 10 | **Track volume (trim/VCA) and master volume automation read at every sample**, dB-linear and capped; hosted instrument latency compensated; audio-thread strips serial; Consolidate renders a bounded clip-FX tail | `crates/mix/src/automation.rs` (`apply_gain`, `copy_with_gain`, `Level`); `crates/mix/src/strip.rs` (`apply_fader`, `run_inserts`); `crates/mix/src/lib.rs`; `crates/mix/src/threads.rs`; `crates/mix/src/offline.rs` | implemented (new in the v0.18.0→v0.20.1 delta) |
| 11 | **Shortcuts**: F5–F10 tools; F6+F7 / F7+F8 either order and Cmd/Ctrl+7 Smart Tool; Cmd/Ctrl+6 Pencil; only zoom keys repeat; plain Left/Right centre the Edit window on a selection | `crates/ui-egui/src/shortcuts.rs` (`tool_key`, `REPEATING`, `repeating_command`, `centre_on_selection`, `zoom_key`); `crates/engine/src/cmd/edit.rs` (`edit.tool` shortcut doc) | implemented (new in the v0.18.0→v0.20.1 delta) |
| 12 | **Descriptive display labels, stable ids**: Beat Analysis, Punch Recording, MusicXML, Rendered (High Quality), Analog Saturation, No ARA plug-ins, Tempo Sync, Search; `lofi` shows "Bit Crusher"; five catalog leaves disabled as placeholders; legacy paths still dispatch | `crates/engine/src/feature_names.rs`; `crates/engine/src/catalog.rs` (`LEGACY_LABEL_ALIASES`, `PLACEHOLDERS`, `is_placeholder`); `crates/ui-egui/src/menus.rs` (`display_menu_label`, `item_state`); `crates/dsp/src/plugins/harmonic.rs` | implemented (new in the v0.18.0→v0.20.1 delta) |
| 13 | **`.scraft`**: `format_version` 1, pretty JSON, duplicate document field refused, 256 MiB read/save cap, atomic save, ten numbered `Backups/`, in-memory audio saved as float WAV; `.scraftz` browser-only | `crates/model/src/session.rs` (`FORMAT_VERSION`, `from_json`); `crates/engine/src/io.rs` (`MAX_SESSION_BYTES`, `write_session`, `back_up`, `session_file`); `crates/engine/src/io/bundle.rs`; `crates/engine/src/io/session.rs`; `crates/ui-egui/src/dialogs/files.rs` | implemented (carried; re-verified) |
| 14 | **Recording streams takes to disk** (WAV per take, header every second); input routing via `track.input`; never-saved sessions without a settings folder use a random 0700 folder; recovery clears record-arm/input-monitor | `crates/playback/src/record.rs` (`TakeWriter`, header every 1 s); `crates/engine/src/io.rs::plan_takes`; `crates/ui-egui/src/app/playback.rs` (`fallback_take_dir`); `crates/engine/src/autosave.rs` (`create_unique_folder`, recovery) | implemented (takes carried; folder new) |
| 15 | **30 built-in plug-ins, 34 channel formats, 512 catalog leaves, 397/512 engine parity** | `crates/dsp/src/plugins.rs` (`REGISTRY` 30); `crates/model/src/mixer.rs` (`ChannelFormat::ALL: [ChannelFormat; 34]`); `crates/engine/catalog/menus.txt` (512 lines); `docs/parity-checklist.md` (397/512, 77.5 %) | implemented (unchanged) |
| 16 | **Preferences**: nine pages, only Theme / Reduce Visual Effects / Levels of Undo wired; every other control disabled with "This preference is not available yet." | `crates/ui-egui/src/preferences.rs` (`PreferencesPage::ALL` 9, `on_disabled_hover_text`); `crates/ui-egui/src/menus.rs` (`setup.preferences`); `crates/engine/src/cmd/options.rs` / `view_more.rs` (the two UI commands) | implemented (mostly placeholder) |
| 17 | **Updater reports installing/ready/installed/failed, offers Restart to Update, installs at exit** | `crates/ui-egui/src/updates_ui.rs` (`shows_result`, `RestartToUpdate`, `start_pending_update`); `apps/soundcraft/src/main.rs` (`on_exit` calls `start_pending_update`) | implemented (new in the v0.18.0→v0.20.1 delta) |
| 18 | **Video hardening**: MJPEG dimensions checked before decode; H.264 per-request byte and no-picture budgets; movie paths read-checked and regular-file-only | `crates/video/src/movie.rs` (`declared_size`, `MAX_REQUEST_BYTES`, `MAX_SAMPLES_WITHOUT_PICTURE`); `crates/ui-egui/src/video_track.rs::open_movie`; `crates/engine/src/io.rs::read_file_inside` | implemented (new in the v0.18.0→v0.20.1 delta) |
| 19 | **`setup.playback_engine` is headless-stored but desktop-applied**: a programmatic desktop call routes device/buffer through `ui.audio_device` and applies delay compensation; headless returns `applied: false` | `crates/engine/src/cmd/setup_more.rs::engine_settings`; `crates/ui-egui/src/panels/windows.rs::setup_audio_command` / `audio_device_command`; `crates/ui-egui/src/menus.rs::run_ui_command` | implemented (corrected from the previous claim) |
| 20 | **Absences**: no MIDI hardware I/O; no AAF/OMF/`.ptx`; no compressed export; video decode-only; no ADM/Atmos; no control surfaces or external sync; no AU discovery/editors | `docs/gaps.md` G-02/G-03/G-05/G-10/G-11/G-12/G-17/G-21; `crates/engine/src/cmd/setup_more.rs` (`setup.midi_*` settings only); `crates/playback/src` (no MIDI device layer); `crates/engine/src/cmd/audiosuite.rs` (hosted ids refused) | not implemented (verified absent) |
| 21 | **`Cmd+Alt+L` collision**: `clip.loop` and `edit.move_selection_left` both declare it; the handler resolves the earlier-registered `edit.move_selection_left`, so Clip Loop must be called by id. `Space` (play/stop/toggle) is handled before the registry | `crates/engine/src/cmd/edit.rs` (`edit.move_selection_left`), `crates/engine/src/cmd/clip.rs` (`clip.loop`), `crates/engine/src/cmd.rs` (`command_specs` registration order), `crates/ui-egui/src/shortcuts.rs::command_for` | implemented (known collision) |

## 2. Automation-surface counts: v0.18.0 → v0.20.1

| Surface | v0.18.0 (measured) | v0.20.1 (measured) | Change |
|---|---:|---:|---|
| Engine specs | 484 (389+94+1) | **484 (389+94+1)** | unchanged (id literals diffed) |
| UI commands (`UI_COMMANDS`) | 70 | **70** | unchanged (id list identical) |
| `engine.commands` on a running app | 554 | **554** | unchanged |
| MCP tools | 17 + 2 resources | **17 + 2** | unchanged |
| Control methods | 17 (+2 aliases) | **17 (+2)** | unchanged |
| CLI subcommands | 10 | **10** | unchanged |
| Built-in plug-ins | 30 (27 processors + 3 instruments) | **30** | unchanged |
| AudioSuite legacy non-plug-in names | 7 | **7** | unchanged |
| Channel formats (`ChannelFormat::ALL`) | 34 | **34** | unchanged |
| Write extension aliases | 6 | **7** (`+aifc`) | +1 |
| Menu catalog leaves | 512 | **512** | unchanged (parity 397/512 = 77.5 %) |
| Workspace library crates | 14 | **13** | −1 (`crates/audio-io` removed) |
| Craft-libs pins | all `c5a1cbf…` | **audio/media `75895c…`; docpath/ui/update `6e03f65…`** | split pins |
| egui fork pin | `6d518fc7…` | **`6d518fc7…`** | unchanged |

## 3. Uncertain / not verified

- **`engine.commands` = 554 is derived, not observed.** `soundcraft-cli` is not installed on the
  authoring machine and the app bundle ships only the GUI binary, so the count comes from the code:
  484 `command_specs()` entries plus the 70 `UI_COMMANDS` that `command_list` appends, with an
  overlap check (per-id `grep -F` across `crates/engine/src`) finding no shared id. Confirm live
  with `soundcraft-cli commands | wc -l` (484, CLI side only) or one `engine.commands` call against
  an open app (554).
- **The pinned craft-audio rev is not available in any local checkout.** `Cargo.toml` pins
  `75895c0321d8cb6e175a42466cba050352b117c5`, but the local craft-libs checkout and the Cargo git
  caches do not contain that commit. The 7-entry write list is nevertheless in-repo evidence: the
  CLI integration test asserts the exact error text (`apps/soundcraft-cli/tests/it/behaviour.rs`),
  and `docs/file-format-parity.md` (updated 2026-11-11) states that `.aifc` is a writable name and
  that Opus, AC-3/E-AC-3 and `.mov`/`.mka` audio are new on import. The exact `DECODE_EXTENSIONS`
  array was not opened at the pinned rev; the read list here is the app's `FileFormat` mapping plus
  that parity doc, not a byte-for-byte copy of the constant.
- **The commit count is not measurable in this clone.** It is shallow, with one commit object
  (`a52bbdc`). The release-notes compare says 72 commits; that number is not restated as measured.
- **GUI behaviour was not launched.** Command registries, UI source and its tests, the menu catalog,
  docs and packaging are the evidence. Where the skill says a control is disabled or a shortcut
  works, it is the code path plus its unit test, not a screen recording.
- **`docs/parity-checklist.md` is the repo's generated report**, not re-generated here (that would
  need a build). Its 397/512 and per-menu table were read at this pin and match the previous pin.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `docs/roadmap.md` alpha gate: device/rate/buffer chosen "by `setup.playback_engine`"; "Takes held in RAM until stop" | `ui.audio_device` changes devices; the desktop app's `setup.playback_engine` routes through it; takes stream to a WAV per take and the header is rewritten every second (`crates/playback/src/record.rs`). The remaining G-01 gap is the duplex/channel-routing path, not device choice. |
| `docs/gaps.md` G-16 lists track-preset recall UI/browser as missing | recall commands exist (`track.save_preset` / `track.load_preset`); the missing part is the browser/UI |
| `docs/localization-parity.md` Korean row: "no Hangul font fallback" | `crates/ui-egui/src/fonts.rs` appends a system Hangul fallback |
| `README.md`: "Any sample rate and bit depth" | import refuses a rate more than 128× below the session rate and caps the sample budget (`crates/engine/src/io/import.rs`); `ui.audio_device` accepts 8 kHz–768 kHz and buffers 16–8192 |
| `docs/target-app-parity.md` and `docs/egui-037-migration-plan.md` still refer to `crates/audio-io` | the crate is gone; formats come from `craft-audio`, and `docs/architecture.md` / `docs/file-format-parity.md` were updated at this tag |
| `docs/ui-parity.md` shortcut table does not mention the Smart Tool chords, zoom auto-repeat or selection arrows | `crates/ui-egui/src/shortcuts.rs` implements them; the in-app Keyboard Shortcuts window is the live list |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # a52bbdccbe15342f44e0de1906bf71a621e7a68f
git -C <clone> rev-parse --is-shallow-repository                # true
git -C <clone> diff --stat v0.18.0..HEAD | tail -1              # 171 files changed, 3824 insertions(+), 5732 deletions(-)
# literal ids, multiline-aware, non-test engine sources (389):
perl -0777 -ne 'while (/cmd!\(\s*(?:\w+\s+)?"([^"]+)"/g) { print "$1\n"; }' \
  $(find crates/engine/src -name '*.rs' -not -path '*tests*') | sort -u | wc -l
for m in toggle flag radio option; do grep -rhoE "\b$m!\(" crates/engine/src/ | wc -l; done  # 17 61 6 10
grep -rc 'CommandSpec {' crates/engine/src/cmd/ | grep -v ':0$'   # 1 (plugin_state.rs)
awk '/pub fn command_specs/,/^}/' crates/engine/src/cmd.rs | grep 'v.extend(' | grep -vc panic_probe  # 32
# compare the full id-literal set with the v0.18.0 tree:
git archive v0.18.0 | tar -x -C <scratch>                        # then rerun the extraction on both trees
# UI registry (70):
awk '/pub const UI_COMMANDS/,/^\];/' crates/ui-egui/src/menus.rs | grep -cE '^\s+\("'
grep -cE '^\s+tool\(' crates/automation/src/mcp.rs               # 17
perl -0777 -ne '$n=0; while (/tool\(\s*"([^"]+)"/g) { $n++ } print "$n\n"' crates/automation/src/mcp.rs  # 17
grep -oE 'soundcraft://[a-z_]+' crates/automation/src/mcp.rs | sort -u   # 2 resources
sed -n '49,61p' apps/soundcraft-cli/src/args.rs                 # 10 subcommands
grep -n 'cannot write `\.xyz`' -A 1 apps/soundcraft-cli/tests/it/behaviour.rs  # 7 write aliases
grep -n 'MAX_RATE_EXPANSION\|MAX_IMPORT_SAMPLES' crates/engine/src/io/import.rs
grep -n 'MAX_SESSION_BYTES' crates/engine/src/io.rs              # 256 MiB
grep -n 'MAX_BATCH_CALLS' crates/automation/src/mcp.rs           # 1000
grep -n 'ChannelFormat; 34' crates/model/src/mixer.rs            # 34 formats
wc -l crates/engine/catalog/menus.txt                            # 512 leaves
grep -n 'Menu items implemented' docs/parity-checklist.md        # 397 / 512
ls -d crates/*/ | wc -l                                          # 13 library crates
```

## 6. Shared pins read from `Cargo.toml` / `Cargo.lock`

- `craft-audio`, `craft-media`: `75895c0321d8cb6e175a42466cba050352b117c5`
- `craft-docpath`, `craft-ui`, `craft-update`: `6e03f65bf45181db77ba6229716e6624db9eb25b`
- egui fork (`ecolor`, `emath`, `epaint`, `egui`, `eframe`, `egui_extras`, …): `6d518fc799681571963842f95b55a6b68431b15a` (unchanged)
- Workspace version 0.20.1; edition 2024; `rust-version = "1.90"`.

## Round 2026-11-12 (refresh)

- Pinned to `v0.20.1` = `a52bbdccbe15342f44e0de1906bf71a621e7a68f`; installed
  `soundcraft 0.20.1 (macos aarch64)`.
- Re-measured: engine 484 (unchanged — the v0.18.0 tree was extracted and the full id-literal set
  compared), UI commands 70 (unchanged), live `engine.commands` 554, CLI 10 subcommands, 17 MCP
  tools + 2 resources, 17 control methods, 30 plug-ins, 34 channel formats, 512 catalog leaves,
  397/512 parity. Write aliases corrected 6 → **7** (`aifc`); workspace crates 14 → **13**.
- Re-resolved every repo path cited in `SKILL.md` against the clone: all present; the
  `crates/audio-io/**` citations from the previous skill were replaced by `craft-audio` references
  and `crates/model/src/source.rs`, because that crate was removed.
- Added rows 6–12, 17–19 and 21 for the surfaces the v0.18.0 → v0.20.1 diff actually changed; rows 3,
  13–16 and 20 were updated in place. The previous round's rows were re-checked rather than copied.
