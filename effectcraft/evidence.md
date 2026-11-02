# EffectCraft — evidence ledger (tag v0.19.0)

Audit basis: this checkout is tag **`v0.20.0`**, commit **`720c67117ea232ef01631a368bb617012f4c63d6`** ("Release 0.20.0", 2026-11-01; inspection 2026-11-02; the v0.19.0 ref was fetched for id diffs; installed bundle matches at 0.20.0)

v0.19.0 → v0.20.0 delta: **+1 command** — `comp.deleteAllMarkers` (#2169; `(cmd|query)!` multiline non-test id extract 680 → 681, nothing removed) and **+1 interface language** — `sv` (#1541; 17 → 18 in `crates/ui-egui/src/i18n.rs`). Effects: generated `docs/effects.md` says **308 effects / 2987 params / 280 GPU at both v0.19.0 and v0.20.0** — the previous ledger's "307 effects / 3032 params" did not match its own pinned tag; the test-enforced generated doc wins. MCP 36 tools, control 24 methods, CLI 12 subcommands, UI_COMMANDS 111: zero diff files. Behaviour: disk cache drops pre-adjustment-blend frames (#2666), tools-bar flyout cycling (#2684), all-four workspace menu (#2690), AE-named 3D views in Japanese + comp camera label (#2691), channel-button colours (#2692), Fast Previews placement (#2694), floating-Timeline drops (#2700), web tab title (#2710), floating-panel ≡ menu (#2711), Expression Reference target exists (#2712), `frame_position` rate guard (#2693).
(shallow clone plus a fetched `v0.17.0` ref for set diffs). Inspection date **2026-10-29**. Installed
`/Applications/EffectCraft.app` prints `effectcraft 0.18.0`; the GUI was never launched.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | Registry unchanged except +`text.deleteSurrounding` | id-set diff between the tags (563 → 564 unique literal ids; nothing removed); `cmd!`/`query!` call sites 697 → 678 (refactor consolidated macro sites) | implemented |
| 2 | 308 effects / 2987 params / 280 GPU / 21 categories / 0 partial | `docs/effects.md:6-10` (generated, test-enforced by `effects_doc_is_current`; identical at v0.19.0 and v0.20.0) | implemented |
| 3 | 36 MCP tools (27 headless + 9 bridge-only) | `crates/automation/src/tools.rs` `static TOOLS`: 36 `ToolDef {`, 9 `bridge_only: true` — identical to v0.17.0 | implemented |
| 4 | 24 control methods | `crates/ui-egui/src/control.rs` — same count and set as v0.17.0 | implemented |
| 5 | 111 UI-only ids | `crates/ui-egui/src/menus/commands.rs` (`UI_COMMANDS`) — carried count, table moved by the refactor | implemented |
| 6 | 12 CLI subcommands; `run --args-file` | `apps/effectcraft-cli/src/main.rs` | implemented |
| 7 | Timeline comp tabs with overflow menu | PR #2458; `crates/ui-egui/src/dock.rs` | implemented |
| 8 | Export encodes while the next batch renders; transparent pixels skipped | PR #2518 | implemented |
| 9 | Edit-menu keys edit a focused text field | PR #2459 | implemented |
| 10 | craft-ui shared docking; egui 0.37; software-GPU median fix | PRs #2432, #2367, #2437 | implemented |
| 11 | Startup update prompt + self-update; Windows per-user | PRs #2420, #2493 | implemented |
| 12 | 13 render-queue formats; import/export tables | `crates/project/src/render_queue.rs`; `crates/media/src/lib.rs`; `crates/interchange/src/lib.rs` | implemented |
| 13 | No `.aep` reader; no hardware codecs; no `.prproj`; no `.jsxbin` | `docs/file-format-parity.md`; `docs/gaps.md`; `docs/scripting-parity.md` | not implemented (verified absent) |

## 2. Automation-surface counts: v0.18.0 → v0.19.0

Delta: +1 engine command (`keys.setMuted`, `crates/engine/src/cmd/prop.rs:1487`; four ids re-wrapped
multiline, none removed); new `crates/sam2` crate (SAM 2.1 Tiny as MaskModel + Roto Brush tracker);
adjustment-layer blend-mode compositing; background Premiere Pro export pre-render; render-queue
output-name collision fixes; automation tool catalogue re-diffed in `crates/automation/src/tools.rs` (set unchanged).

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
| README/docs "306 effects" | 308 (test-enforced generated doc) |
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
