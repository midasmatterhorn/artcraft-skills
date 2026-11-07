# SoundCraft — evidence ledger (tag v0.18.0)

Audit basis: this checkout is the release tag **`v0.18.0`**, commit
**`5ff012ab88490cdfc635ee304c1019885e1b880d`** (`git rev-parse HEAD`); inspection date
**2026-11-07**. The shallow clone also carries the previous tag object, so
`git diff v0.17.0..HEAD` runs here. The installed bundle's read-only `--version` prints
`soundcraft 0.18.0 (macos aarch64)` (`CFBundleShortVersionString` 0.18.0,
`CFBundleIdentifier` `ai.storyteller.soundcraft`); only `--version` was run and the GUI was never
launched. The previous ledger described v0.17.0 (`b35dd0f9eb0c08a198c1306021bd138f3a22d87c`).

v0.17.0 → v0.18.0 delta, measured here: **108 files changed, +6,468/−554** (`git diff
v0.17.0..HEAD --stat`). The engine command-id set is **unchanged at 484**: the same multiline-aware
extraction over a `git archive v0.17.0` tree and over HEAD returns 389 literal ids + 94
helper-macro ids + 1 direct `CommandSpec` both times, with no id added or removed. The UI registry
moved **68 → 70** — `ui.reduce_visual_effects` and `ui.undo_levels` were added, nothing was removed
— so a running app's `engine.commands` reply (`crates/ui-egui/src/control.rs::command_list` appends
`UI_COMMANDS` to the engine list) goes **552 → 554**. MCP (17 tools + 2 resources), control methods
(17 + 2 aliases) and CLI subcommands (10) did not move; the CLI gained `commands --json` inside the
existing `commands` subcommand. Behaviour: complete Grid/Nudge time scales, a Preferences window,
BWF `bext` TimeReference on WAV bounces and kept on `convert`, stderr logging, the 256 MiB session
cap with duplicate-field / duplicate-payload refusals, transient live input toggles, offline-render
flags to hosted plug-ins, and MIDI controller indexing by channel and kind.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | **484 engine command specs, unchanged v0.17.0 → v0.18.0** | 389 non-test literal `cmd!(` ids + helper macros `toggle!` 17 / `flag!` 61 / `radio!` 6 / `option!` 10 + 1 direct `CommandSpec` (`crates/engine/src/cmd/plugin_state.rs`) = 484; 32 production modules registered by `command_specs()` (`crates/engine/src/cmd.rs`) | implemented (unchanged at this tag) |
| 2 | 17 MCP tools + 2 resources, unchanged at v0.18.0 | `crates/automation/src/mcp.rs` — 17 `tool(` entries; resources `soundcraft://session`, `soundcraft://commands` | implemented |
| 3 | 17 control methods (2 aliases), unchanged at v0.18.0 | `crates/ui-egui/src/control.rs` dispatch arms; `command_list` appends the UI registry | implemented |
| 4 | 10 CLI subcommands; `commands --json [--compact]` added at v0.18.0; warnings/errors to stderr; `convert` keeps a BWF source's `bext` | `apps/soundcraft-cli/src/args.rs` (10 variants); `catalog.rs` (`args.json` → `print_json` over `command_specs()`); `logger.rs` (`warning:` / `error:`); `convert.rs` | implemented (+`commands --json`) |
| 5 | Send-fader moves write send-level automation | PR #1146 (carried); `crates/engine/src/cmd/edit.rs` send-level automation write path | implemented |
| 6 | Zoom Toggle cancellable via `view.zoom_toggle_cancel` (Alt+Shift+E / Alt-click) | `crates/engine/src/cmd/zoom_toggle.rs` `cancel` + registration (since v0.17.0); `crates/ui-egui/` binding | implemented (carried) |
| 7 | MCP replies Invalid Request to empty batches / non-object messages | `crates/automation/src/mcp.rs` envelope validation | implemented |
| 8 | `.scgrp` import refuses absolute audio paths and `..` | `crates/engine/src/clip_group_file.rs` path validation | implemented |
| 9 | Byte-budgeted score/MusicXML output; hostile-input bounds (H.264 SPS size, `frame_num` gaps, long-term references; CAF/BWF/WAV/FLAC caps; MIDI-import floods; VST3 bus layouts) | `crates/engine/src/score.rs`; `crates/video/src/h264/{params.rs,dpb.rs}`; `crates/audio-io/src/`; `crates/vst3-host/src/` | implemented (H.264 bounds new at this tag) |
| 10 | `setup.playback_engine` is still a stored-only command (`applied: false`) | `crates/engine/src/cmd/setup_more.rs` doc comment + result JSON | verified absent (still) |
| 11 | No MIDI hardware I/O; no Pro Tools interchange; no compressed export; video decode-only; no ADM/Atmos; no control surfaces | `docs/gaps.md`; `docs/roadmap.md` "Alpha gate" (three workflows **no**) | not implemented (verified absent) |
| 12 | **Grid and Nudge have their full time scales**: `format:` `bars_beats\|min_secs\|timecode\|feet_frames\|samples` (+ `clips_markers` for grid only, refused by `view.nudge`), `follow_main`, `{"timecode"}` / `{"feet_frames"}` increments, `"whole note"`; snapping excludes the clips being moved | `crates/engine/src/cmd/view.rs` (`view.grid` / `view.nudge` docs + `ClipsMarkers` refusal); `crates/time/src/grid.rs` (`GridScale`); `crates/model/src/session.rs` (`grid_follow_main`, `nudge_follow_main`, `grid_clips_markers`) | implemented (new at this tag) |
| 13 | **Preferences window**: nine pages (Display, Operation, Editing, Mixing, Metering, Processing, Midi, Collaboration, Synchronization), searchable; only theme, reduce-visual-effects and undo levels are wired, every other control disabled with "This preference is not available yet." | `crates/ui-egui/src/preferences.rs` (`PreferencesPage::ALL: [PreferencesPage; 9]`, `on_disabled_hover_text`); `setup.preferences {"value": true}` handler in `crates/ui-egui/src/menus.rs`; `ui.reduce_visual_effects`, `ui.undo_levels` in `UI_COMMANDS`; `ui.set` fields per `menus.rs` tests | implemented (mostly placeholder) |
| 14 | WAV bounces carry a BWF `bext` TimeReference (session timecode start + bounce start); AIFF/FLAC have no `bext`; `convert` rescales a kept `bext` to the output rate | `crates/engine/src/io.rs` `time_stamp` + `EncodeOptions { bwf: … }`; `apps/soundcraft-cli/src/convert.rs` | implemented (new at this tag) |
| 15 | Sessions capped at **256 MiB** on read and save; `.scraft` parsed straight into the document and a repeated field in one JSON object refused; bundle entries sharing one payload refused; autosave obeys the cap and recovery comes back with record-arm / input-monitor off | `crates/engine/src/io.rs` (`MAX_SESSION_BYTES = 256 << 20`); `crates/engine/src/io/bundle.rs` (`BUNDLE_LIMITS` 10,000 entries / 1 GiB); `crates/engine/src/autosave.rs` (recovery clears both flags) | implemented (new at this tag) |
| 16 | Live input toggles are transient: `mix.record_arm`, `mix.input_monitor`, `track.set_record_to_input_only` are non-undoable, do not dirty the document and are not restored from autosave; hosted plug-ins are told offline vs realtime (VST3 `kOffline`, CLAP `clap.render`) and keep the system's load reason | `crates/engine/src/cmd/mix.rs`; `crates/engine/src/dirty.rs`; `crates/engine/src/autosave.rs`; `crates/mix/src/instances.rs`; `crates/clap-host/`, `crates/vst3-host/` | implemented (new at this tag) |

## 2. Automation-surface counts: v0.17.0 → v0.18.0

| Surface | v0.17.0 (measured) | v0.18.0 (measured) | Change |
|---|---:|---:|---|
| Engine specs | 484 (389+94+1) | **484 (389+94+1)** | unchanged |
| UI commands (`UI_COMMANDS`) | 68 | **70** | +2 (`ui.reduce_visual_effects`, `ui.undo_levels`) |
| `engine.commands` on a running app | 552 | **554** | +2 (engine list + UI list, no shared id) |
| MCP tools | 17 + 2 resources | **17 + 2** | unchanged |
| Control methods | 17 (+2 aliases) | **17 (+2)** | unchanged |
| CLI subcommands | 10 | **10** | unchanged surface; `commands --json` added |
| Built-in plug-ins | 30 (27 processors + 3 instruments) | **30** | unchanged |
| AudioSuite legacy non-plug-in names | 7 | **7** | unchanged |
| Channel formats (`ChannelFormat::ALL`) | 34 | **34** | unchanged |
| Write extensions | 6 (`wav`,`wave`,`bwf`,`aif`,`aiff`,`flac`) | **6** | unchanged |
| Menu catalog leaves | 512 | **512** | unchanged (parity 397/512 = 77.5 %) |
| Craft-libs pins | `c5a1cbfb…` (all crates) | **`c5a1cbfb…`** | unchanged |

## 3. Uncertain / not verified

- **`engine.commands` = 554 is derived, not observed.** `soundcraft-cli` is not installed on the
  authoring machine and the app bundle ships only the GUI binary, so the count comes from the code:
  484 `command_specs()` entries plus the 70 `UI_COMMANDS` that `command_list` appends, with an
  overlap check (`grep -F` for each UI id across `crates/engine/src`) finding no shared id. Confirm
  live with `soundcraft-cli commands | wc -l` (484, CLI side only) or one `engine.commands` call
  against an open app (554).
- The 68 UI-command figure for v0.17.0 was re-measured from the tag's tree with the same extraction,
  not carried from an older ledger.
- GUI behaviour was not launched; command registries, the menu catalog, docs and packaging are the
  evidence. The `git diff` line totals come from the shallow clone's v0.17.0 object, the commit
  count (91) from the round's compare-API note and is not restated as a measured value.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `docs/roadmap.md` alpha gate: device/rate/buffer chosen "by `setup.playback_engine`", "Takes held in RAM until stop" | `ui.audio_device` changes devices (`setup.playback_engine` returns `applied: false`); takes stream to WAV while recording |
| `docs/localization-parity.md` Korean row: "no Hangul font fallback" | `crates/ui-egui/src/fonts.rs` appends a system Hangul fallback |
| `docs/gaps.md` G-16 lists track-preset recall UI/browser as missing | recall commands exist (`track.save_preset` / `track.load_preset`) — the missing part is the browser/UI |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # 5ff012ab88490cdfc635ee304c1019885e1b880d
git -C <clone> diff --stat v0.17.0..HEAD | tail -1              # 108 files changed, 6468 insertions(+), 554 deletions(-)
# literal ids, multiline-aware, non-test engine sources (389):
perl -0777 -ne 'while (/cmd!\(\s*(?:\w+\s+)?"([^"]+)"/g) { print "$1\n"; }' \
  $(find crates/engine/src -name '*.rs' -not -path '*tests*') | sort -u | wc -l
for m in toggle flag radio option; do grep -rhoE "\b$m!\(" crates/engine/src/ | wc -l; done  # 17 61 6 10
grep -rc 'CommandSpec {' crates/engine/src/cmd/ | grep -v ':0$'   # 1 (plugin_state.rs)
awk '/pub fn command_specs/,/^}/' crates/engine/src/cmd.rs | grep 'v.extend(' | grep -vc panic_probe  # 32
# UI registry (70 at HEAD, 68 at v0.17.0 — same awk over each tree):
awk '/pub const UI_COMMANDS/,/^\];/' crates/ui-egui/src/menus.rs | grep -cE '^\s+\("'
git archive v0.17.0 | tar -x -C <scratch>                        # then rerun both extractions
grep -cE '^\s+tool\(' crates/automation/src/mcp.rs               # 17
grep -oE 'soundcraft://[a-z_]+' crates/automation/src/mcp.rs | sort -u   # 2 resources
grep -n 'FORMAT_VERSION' crates/model/src/session.rs             # 1
grep -n 'MAX_SESSION_BYTES\|MAX_BATCH_CALLS\|BUNDLE_LIMITS' -r crates/  # 256 MiB / 1000 / 10,000 & 1 GiB
grep -n 'ChannelFormat; 34' crates/model/src/mixer.rs            # 34 formats
wc -l crates/engine/catalog/menus.txt                            # 512 leaves
```


## Round 2026-11-07 (refresh)

- Pinned to `v0.18.0` = `5ff012ab88490cdfc635ee304c1019885e1b880d`; installed
  `soundcraft 0.18.0 (macos aarch64)`.
- Re-measured: engine 484 (unchanged — the v0.17.0 tree was extracted and compared id-for-id), UI
  commands 68 → **70**, live `engine.commands` 552 → **554**, CLI 10 subcommands, 30 plug-ins,
  34 channel formats, 6 write extensions, 512 catalog leaves.
- Re-resolved every repo path cited in `SKILL.md` against the clone: all present; no claim had to be
  deleted.
- Added rows 12–16 for the surfaces the v0.17.0 → v0.18.0 diff actually changed; rows 1, 4 and 9
  were updated in place. Rows 5–8 and 10–11 were left exactly as written.
