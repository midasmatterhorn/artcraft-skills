# SoundCraft — evidence ledger (tag v0.14.0)

Audit basis: this checkout is tag **`v0.14.0`**, commit **`c6befe57afd0dc35fc4b86a01b2a19011ae1df1e`**
(shallow clone of the release tag). Inspection date **2026-10-29**. Installed
`/Applications/SoundCraft.app` prints `SoundCraft 0.14.0`; the GUI was never launched.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | **482 engine command specs, identical to v0.13.1** | 397 literal `cmd!(` ids (same grep as the v0.13.1 evidence used) + helper macros `toggle!` 17 / `flag!` 61 / `radio!` 6 / `option!` 10 (identical counts) + 1 direct `CommandSpec` = 482; the release PR list contains no registry change | implemented (unchanged) |
| 2 | 17 MCP tools + 2 resources, unchanged | `crates/automation/src/mcp.rs` `tool_definitions()` — 17 `tool(` entries; resources `soundcraft://session`, `soundcraft://commands` | implemented |
| 3 | 17 control methods (2 aliases) | `crates/ui-egui/src/control.rs` method strings | implemented |
| 4 | 10 CLI subcommands, now clap-parsed (RFC-0012) | PR #1136; `apps/soundcraft-cli/src/args.rs` | implemented |
| 5 | Mix bounce ~20 % faster, byte-identical | PR #1144 | implemented |
| 6 | Meters keep every block's peak until the UI takes it | PR #1045 | implemented |
| 7 | Tracks/Groups and Clips full-height dock columns | PR #1088; `crates/ui-egui/src/docking.rs` | implemented |
| 8 | Auto Pan keeps the stereo image; paste + Strip Silence fixes | PR #1060; `crates/dsp/src/plugins/auto_pan.rs` | implemented |
| 9 | Startup update prompt + self-update; Windows per-user; XWayland DnD; egui 0.37 | PRs #1073, #1124, #150, #1063 | implemented |
| 10 | Craft-libs crates at one rev | `Cargo.toml`: `craft-docpath/media/update/ui` → `92d392cf…` (was `16fb3d46…`) | implemented |
| 11 | No MIDI hardware I/O; no Pro Tools interchange; no compressed export; video decode-only; no ADM/Atmos; no control surfaces | `docs/gaps.md` | not implemented (verified absent) |

## 2. Automation-surface counts: v0.13.1 → v0.14.0

| Surface | v0.13.1 | v0.14.0 (measured) | Change |
|---|---:|---:|---|
| Engine specs | 482 (397+94+1) | **482 (397+94+1)** | unchanged |
| UI commands | 67 | **67** (count carried; table moved modules) | unchanged |
| MCP tools | 17 + 2 resources | **17 + 2** | unchanged |
| Control methods | 17 | **17** | unchanged |
| CLI subcommands | 10 | **10** | unchanged surface; clap parser (RFC-0012) |
| Built-in plug-ins / AudioSuite names | 30 / 10 | **30 / 10** | unchanged |
| Craft-libs pins | `16fb3d46…` | **`92d392cf…`** | unified |

## 3. Uncertain / not verified

- The 67 UI-command count was carried from the v0.13.1 audit (its table moved modules in the
  shared-module refactor; the exact re-count needs the new table shape). The engine registry, MCP
  and control counts were re-measured.
- GUI behaviour not launched; registry + docs + packaging are the evidence.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `docs/roadmap.md` alpha gate "no input device choice" / "takes held in RAM" | `ui.audio_device` works; takes stream to WAV while recording |
| `docs/localization-parity.md` denies a Hangul fallback | `crates/ui-egui/src/fonts.rs` appends one |
| `docs/gaps.md` G-16 "no track-preset recall" | recall commands exist (`track.save_preset`/`track.load_preset`) |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # c6befe57afd0dc35fc4b86a01b2a19011ae1df1e
grep -rhoE '\b(cmd|query)!\(' crates/ | wc -l                   # 397 literal ids
for m in toggle flag radio option; do grep -rhoE "\b$m!\(" crates/engine/src/ | wc -l; done   # 17 61 6 10
grep -cE '^\s+tool\($|^\s+tool\("' crates/automation/src/mcp.rs # 17
grep -cE 'CommandSpec \{' crates/engine/src/cmd/ -r             # 1 direct spec
grep -oE 'rev = "[0-9a-f]{8}' Cargo.toml | sort -u              # one craft-libs rev
```
