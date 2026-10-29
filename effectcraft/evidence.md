# EffectCraft — evidence ledger (tag v0.18.0)

Audit basis: this checkout is tag **`v0.18.0`**, commit **`c3600f9b59b109da97871a43a6898683a0163cb1`**
(shallow clone plus a fetched `v0.17.0` ref for set diffs). Inspection date **2026-10-29**. Installed
`/Applications/EffectCraft.app` prints `effectcraft 0.18.0`; the GUI was never launched.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | Registry unchanged except +`text.deleteSurrounding` | id-set diff between the tags (563 → 564 unique literal ids; nothing removed); `cmd!`/`query!` call sites 697 → 678 (refactor consolidated macro sites) | implemented |
| 2 | 307 effects / 3032 params / 280 GPU / 21 categories / 0 partial | `docs/effects.md:6-10` (generated, test-enforced by `effects_doc_is_current`) | implemented |
| 3 | 36 MCP tools (27 headless + 9 bridge-only) | `crates/automation/src/tools.rs` `static TOOLS`: 36 `ToolDef {`, 9 `bridge_only: true` — identical to v0.17.0 | implemented |
| 4 | 24 control methods | `crates/ui-egui/src/control.rs` — same count and set as v0.17.0 | implemented |
| 5 | 111 UI-only ids | `crates/ui-egui/src/commands.rs` (`UI_COMMANDS`, re-exported at `menus.rs:24`) — carried count, table moved by the refactor | implemented |
| 6 | 12 CLI subcommands; `run --args-file` | `apps/effectcraft-cli/src/main.rs` | implemented |
| 7 | Timeline comp tabs with overflow menu | PR #2458; `crates/ui-egui/src/dock.rs` | implemented |
| 8 | Export encodes while the next batch renders; transparent pixels skipped | PR #2518 | implemented |
| 9 | Edit-menu keys edit a focused text field | PR #2459 | implemented |
| 10 | craft-ui shared docking; egui 0.37; software-GPU median fix | PRs #2432, #2367, #2437 | implemented |
| 11 | Startup update prompt + self-update; Windows per-user | PRs #2420, #2493 | implemented |
| 12 | 13 render-queue formats; import/export tables | `crates/project/src/render_queue.rs`; `crates/media/src/lib.rs`; `crates/interchange/src/lib.rs` | implemented |
| 13 | No `.aep` reader; no hardware codecs; no `.prproj`; no `.jsxbin` | `docs/file-format-parity.md`; `docs/gaps.md`; `docs/scripting-parity.md` | not implemented (verified absent) |

## 2. Automation-surface counts: v0.17.0 → v0.18.0

| Surface | v0.17.0 | v0.18.0 (measured) | Change |
|---|---:|---:|---|
| Engine command ids | 672 | **672 +1** | +`text.deleteSurrounding`; call sites 697 → 678 (refactor) |
| UI-only ids | 111 | **111** | unchanged |
| MCP tools | 36 (27+9) | **36 (27+9)** | unchanged |
| Control methods | 24 | **24** | unchanged |
| CLI subcommands | 12 | **12** | unchanged |
| Render-queue formats | 13 | **13** | unchanged |
| Effects / params | 307 / 3032 | **307 / 3032** | unchanged |
| Languages | 11 menus / 8 panels | **same** | unchanged |

## 3. Uncertain / not verified

- The 672 total is carried from the v0.17.0 audit's dedup method; this pass measured 564 unique
  inline literal ids (const-built ids and dedup explain the gap) and a clean +1/-0 id diff — the
  registry is authoritative via `effectcraft-cli commands --json`.
- GUI behaviour not launched; registry + docs + packaging are the evidence.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| README/docs "306 effects" | 307 (test-enforced generated doc) |
| `docs/target-app-parity.md` "411 commands" | registry far larger; `effectcraft-cli commands` is authoritative |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # c3600f9b59b109da97871a43a6898683a0163cb1
grep -rhoE '\b(cmd|query)!\(' crates/ | wc -l                   # 678 call sites
grep -rhA2 -E '\b(cmd|query)!\(' crates/ | grep -oE '"[a-z]+\.[a-zA-Z0-9]+"' | sort -u | wc -l  # 564
awk '/static TOOLS/,/^];/' crates/automation/src/tools.rs | grep -cE 'ToolDef \{'  # 36
grep -c 'bridge_only: true' crates/automation/src/tools.rs      # 9
sed -n '6,10p' docs/effects.md                                  # 307 / 3032 / 280 / 21 / 0
```
