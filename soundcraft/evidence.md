# SoundCraft — evidence ledger (tag v0.16.0)

Audit basis: this checkout is tag **`v0.16.0`**, commit **`db51dd17398852ba70919c5a560d1c8ed9e3e6c6`**
(shallow clone of the release tag; the v0.15.0 ref was fetched for id diffs). Inspection date
**2026-11-02**. Installed `/Applications/SoundCraft.app` prints `SoundCraft 0.16.0 (macos aarch64)`;
the GUI was never launched.

v0.15.0 → v0.16.0 delta: **+1 command** — `view.zoom_toggle_cancel` (Cancel Zoom Toggle, Alt+Shift+E /
Alt-click, PR #1101; the previous ledger credited this to v0.15.0 — compare-log tail trap, the
registration exists only at v0.16.0). Literal non-test `cmd!(` ids 388 → 389, none removed; helper
macros unchanged (toggle 17 / flag 61 / radio 6 / option 10); MCP tools + resources, control methods,
CLI subcommands unchanged (zero diff files under those trees). Behaviour: clip menu acts on the whole
edit selection (#1196), Mix clamps clip-FX gain and send-level automation (#1126), `transport.play
{from}` honours the requested position (#1075), `range_param` defaults to the selection start (#1214),
`AutoParam::parse` keeps parameter-id case (#1227), plus an overflow/hardening wave (#1215, #1216,
#1220–#1222, #1200–#1202, #1211, #1212, #1226, #1229). **Correction:** the previous ledger's total
"482 = 397+94+1" omitted the 10 `option!` ids its own breakdown listed, and its "397 literal" scope
counted test-file registrations; the reproducible non-test decomposition is 389 + 94 + 1 = **484**.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | **484 engine command specs, +1 over v0.15.0** | 389 non-test literal `cmd!(` ids (+`view.zoom_toggle_cancel`) + helper macros `toggle!` 17 / `flag!` 61 / `radio!` 6 / `option!` 10 + 1 direct `CommandSpec` = 484 (multiline-aware re-extract at v0.16.0; previous 482 omitted `option!`) | implemented (+1) |
| 2 | 17 MCP tools + 2 resources, unchanged | `crates/automation/src/mcp.rs` — 17 `tool(` entries; resources `soundcraft://session`, `soundcraft://commands` | implemented |
| 3 | 17 control methods (2 aliases) | `crates/ui-egui/src/control.rs` method strings | implemented |
| 4 | 10 CLI subcommands; `script --keep-going` exit status reports failures | `apps/soundcraft-cli/src/args.rs`; fix(cli): report kept-going script errors | implemented |
| 5 | Send-fader moves write send-level automation | PR #1146; `crates/engine/src/cmd/edit.rs` send-level automation write path | implemented |
| 6 | Zoom Toggle cancellable via the new `view.zoom_toggle_cancel` (Alt+Shift+E / Alt-click) | `crates/engine/src/cmd/zoom_toggle.rs` `cancel` + registration (v0.16.0 only); `crates/ui-egui/` binding | implemented (moved to this tag) |
| 7 | MCP replies Invalid Request to empty batches / non-object messages | `crates/automation/src/mcp.rs` envelope validation | implemented |
| 8 | `.scgrp` import refuses absolute audio paths and `..` | `crates/engine/src/clip_group_file.rs` path validation | implemented |
| 9 | Score/MusicXML output byte-budgeted; overflow fixes (H.264 POC, CAF/BWF/WAV/FLAC caps, MIDI-import flood bounds, VST3 bus-layout limits) | `crates/engine/src/score.rs`; `crates/audio-io/src/`; `crates/video/src/`; `crates/vst3-host/src/` | implemented |
| 10 | `setup.playback_engine` still a stored-only command (`applied: false`) | `crates/engine/src/cmd/setup_more.rs` doc comment + result JSON | verified absent (still) |
| 11 | No MIDI hardware I/O; no Pro Tools interchange; no compressed export; video decode-only; no ADM/Atmos; no control surfaces | `docs/gaps.md` | not implemented (verified absent) |

## 2. Automation-surface counts: v0.14.0 → v0.15.0

| Surface | v0.14.0 | v0.15.0 (measured) | Change |
|---|---:|---:|---|
| Engine specs | 482 (397+94+1, arithmetic omitted option!) | **484 (389+94+1)** | +1 (`view.zoom_toggle_cancel`) |
| UI commands | 67 | **67** (count carried) | unchanged |
| MCP tools | 17 + 2 resources | **17 + 2** | unchanged |
| Control methods | 17 | **17** | unchanged |
| CLI subcommands | 10 | **10** | unchanged surface |
| Built-in plug-ins / AudioSuite names | 30 / 10 | **30 / 10** | unchanged |
| Craft-libs pins | `92d392cf…` + `04aa1703…` | **`c5a1cbfb…` (all craft-libs crates)** | unified, moved |

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
git -C <clone> rev-parse HEAD                                   # db51dd17398852ba70919c5a560d1c8ed9e3e6c6
grep -rhoE '\bcmd!\(' crates/engine/src/ | wc -l                # 398 textual (389 non-test literal ids + defs/tests)
# multiline-aware id extract (re-wrapped registrations defeat line greps):
perl -0777 -ne 'while (/cmd!\(\s*(?:\w+\s+)?"([^"]+)"/g) { print "$1\n"; }' $(find crates/engine/src -name '*.rs' -not -path '*tests*') | sort -u
for m in toggle flag radio option; do grep -rhoE "\b$m!\(" crates/engine/src/ | wc -l; done   # 17 61 6 10
grep -cE '^\s+tool\($|^\s+tool\("' crates/automation/src/mcp.rs # 17
grep -cE 'CommandSpec \{' crates/engine/src/cmd/ -r             # 1 direct spec
grep -oE 'craft-[a-z]+ = \{[^}]*rev = "[0-9a-f]{8}' Cargo.toml  # all craft-libs at c5a1cbfb
```
