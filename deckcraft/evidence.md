# DeckCraft — evidence ledger (tag v0.12.0)

Audit basis: this checkout is tag **`v0.12.0`**, commit **`29f0f7772c47aa2bfb74fcbb0c4d3b1503300849`**
(shallow clone plus a fetched `v0.11.1` ref for set diffs). Inspection date **2026-10-29**. Installed
`/Applications/DeckCraft.app` prints `deckcraft 0.12.0`; the GUI was never launched.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 328 engine `cmd!` blocks (was 326) | `grep -rho 'cmd!' crates/engine/src/ \| wc -l` = 328; `git grep -o 'cmd!' v0.11.1` = 326 | implemented |
| 2 | +`format.languageAll`, +`slide.selectRange`; nothing removed | id-string diff between the tags: exactly these two new ids | implemented |
| 3 | 25 MCP tools, set identical | `crates/mcp/src/tools.rs` — 25 `tool(` calls; name list read and matched to the baseline's 25 | implemented |
| 4 | Control dispatch set unchanged (26 names) | arm-string diff `v0.11.1` vs HEAD: 0 added, 0 removed | implemented |
| 5 | 51 UI_COMMANDS rows (+1) | `crates/ui-egui/src/lib.rs` `UI_COMMANDS` awk count | implemented |
| 6 | 12 CLI subcommands | `apps/deckcraft-cli/src/help.rs` names | implemented |
| 7 | Reuse Slides slide chooser; whole-presentation proofing language; Ctrl+Shift+click range; units preference; Ctrl+wheel show zoom | PRs #1109, #1118, #1107, #1336, #1331; `slide.selectRange`/`format.languageAll` specs | implemented |
| 8 | RTF outline fixes; PDF web/mail links only + backdrop reuse; parameter-validation wave; media decoder hardening; H.264 clamp | PRs #1315, #1317, #1319, #1351, #1221, #1461, #1189–#1358, #1285, #1246 | implemented |
| 9 | Startup update prompt + self-update; Windows per-user; egui 0.37 + craft-ui ComboBox; shortcut icon fix | PRs #1377, #1434, #1350, #1457, #1391 | implemented |
| 10 | Craft-libs crates at one rev | `Cargo.toml` (craft-media, craft-pdf → `92d392cf…`, was `f0ad6c1e`/`9f75d3dc`) | implemented |
| 11 | No `.ppt`/`.odp`/macros/password/MP4 export; PDF raster artwork; SVG not drawn | `docs/gaps.md`; `crates/engine/src/cmd/file.rs`; `crates/render/src/images.rs` | not implemented (verified absent) |

## 2. Automation-surface counts: v0.11.1 → v0.12.0

| Surface | v0.11.1 | v0.12.0 (measured) | Change |
|---|---:|---:|---|
| Engine commands | 326 | **328** | +`format.languageAll`, +`slide.selectRange` |
| MCP tools | 25 | **25** | unchanged |
| Control methods | 26 dispatch names | **26** | set unchanged |
| UI commands | 50 | **51** | +1 |
| CLI subcommands | 12 | **12** | unchanged |
| Transitions / animations / themes / layouts / presets / charts / SmartArt / starters / icons / warps | 49 / 107 / 8×4 / 11+Custom / 183 / 28 / 45-9-17 / 6 / 70 / 40 | **same** | unchanged (wave is fixes; the v0.11.1 audit's methods cover these) |
| Craft-libs pins | per-crate revs | **one rev `92d392cf…`** | unified |

## 3. Uncertain / not verified

- The +1 UI command id was not named (row count only); the live registry is authoritative.
- GUI behaviour not launched; registry + docs + packaging are the evidence.
- PPTX fidelity on real corporate decks remains unmeasured by the project (`docs/gaps.md`).

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `docs/control-protocol.md` "16 MiB request line" | 256 MiB in code |
| `docs/animation-parity.md` "14 exit effects" | 23 |
| `docs/architecture.md` "320 commands" | 328 |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # 29f0f7772c47aa2bfb74fcbb0c4d3b1503300849
grep -rho 'cmd!' crates/engine/src/ | wc -l                     # 328
git grep -o 'cmd!' v0.11.1 -- crates/engine/src | wc -l         # 326
grep -cE '^\s+tool\(' crates/mcp/src/tools.rs                   # 25
awk '/pub (static|const) UI_COMMANDS/,/^\];/' crates/ui-egui/src/lib.rs | grep -cE '^\s+\('   # 51
grep -oE '"(info|render|render-transition|convert|run|commands|describe|app|mcp|bench|links|version)"' apps/deckcraft-cli/src/help.rs | sort -u | wc -l   # 12
```
