# SoundCraft — evidence ledger (tag v0.15.0)

Audit basis: this checkout is tag **`v0.15.0`**, commit **`a97ce7556c5362718e8bcab5349477381ff3fb65`**
(shallow clone of the release tag). Inspection date **2026-11-01**. Installed
`/Applications/SoundCraft.app` prints `SoundCraft 0.15.0 (macos aarch64)`; the GUI was never launched.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | **482 engine command specs, identical to v0.14.0** | 397 literal `cmd!(` ids + helper macros `toggle!` 17 / `flag!` 61 / `radio!` 6 / `option!` 10 + 1 direct `CommandSpec` = 482 (re-grepped at v0.15.0) | implemented (unchanged) |
| 2 | 17 MCP tools + 2 resources, unchanged | `crates/automation/src/mcp.rs` — 17 `tool(` entries; resources `soundcraft://session`, `soundcraft://commands` | implemented |
| 3 | 17 control methods (2 aliases) | `crates/ui-egui/src/control.rs` method strings | implemented |
| 4 | 10 CLI subcommands; `script --keep-going` exit status reports failures | `apps/soundcraft-cli/src/args.rs`; fix(cli): report kept-going script errors | implemented |
| 5 | Send-fader moves write send-level automation | PR #1146; `crates/engine/src/cmd/edit.rs` send-level automation write path | implemented |
| 6 | Zoom Toggle cancellable (Alt+Shift+E / Alt-click keep current view) | `crates/ui-egui/src/` zoom-toggle handling | implemented |
| 7 | MCP replies Invalid Request to empty batches / non-object messages | `crates/automation/src/mcp.rs` envelope validation | implemented |
| 8 | `.scgrp` import refuses absolute audio paths and `..` | `crates/engine/src/clip_group_file.rs` path validation | implemented |
| 9 | Score/MusicXML output byte-budgeted; overflow fixes (H.264 POC, CAF/BWF/WAV/FLAC caps, MIDI-import flood bounds, VST3 bus-layout limits) | `crates/engine/src/score.rs`; `crates/audio-io/src/`; `crates/video/src/`; `crates/vst3-host/src/` | implemented |
| 10 | `setup.playback_engine` still a stored-only command (`applied: false`) | `crates/engine/src/cmd/setup_more.rs` doc comment + result JSON | verified absent (still) |
| 11 | No MIDI hardware I/O; no Pro Tools interchange; no compressed export; video decode-only; no ADM/Atmos; no control surfaces | `docs/gaps.md` | not implemented (verified absent) |

## 2. Automation-surface counts: v0.14.0 → v0.15.0

| Surface | v0.14.0 | v0.15.0 (measured) | Change |
|---|---:|---:|---|
| Engine specs | 482 (397+94+1) | **482 (397+94+1)** | unchanged |
| UI commands | 67 | **67** (count carried) | unchanged |
| MCP tools | 17 + 2 resources | **17 + 2** | unchanged |
| Control methods | 17 | **17** | unchanged |
| CLI subcommands | 10 | **10** | unchanged surface |
| Built-in plug-ins / AudioSuite names | 30 / 10 | **30 / 10** | unchanged |
| Craft-libs pins | `92d392cf…` (all) | **`92d392cf…` docpath/media/ui; `04aa1703…` craft-update** | craft-update moved |

## 3. Uncertain / not verified

- The 67 UI-command count was carried from the v0.14.0 audit. The engine registry, MCP and control
  counts were re-measured at v0.15.0.
- GUI behaviour not launched; registry + docs + packaging are the evidence.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `docs/roadmap.md` alpha gate "no input device choice" / "takes held in RAM" | `ui.audio_device` works; takes stream to WAV while recording |
| `docs/localization-parity.md` denies a Hangul fallback | `crates/ui-egui/src/fonts.rs` appends one |
| `docs/gaps.md` G-16 "no track-preset recall" | recall commands exist (`track.save_preset`/`track.load_preset`) |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # a97ce7556c5362718e8bcab5349477381ff3fb65
grep -rhoE '\bcmd!\(' crates/engine/src/ | wc -l                # 397 literal ids
for m in toggle flag radio option; do grep -rhoE "\b$m!\(" crates/engine/src/ | wc -l; done   # 17 61 6 10
grep -cE '^\s+tool\($|^\s+tool\("' crates/automation/src/mcp.rs # 17
grep -cE 'CommandSpec \{' crates/engine/src/cmd/ -r             # 1 direct spec
grep -oE 'craft-[a-z]+ = \{[^}]*rev = "[0-9a-f]{8}' Cargo.toml  # docpath/media/ui 92d392cf, update 04aa1703
```
