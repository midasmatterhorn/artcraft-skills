# GridCraft — evidence ledger (tag v0.13.0)

Audit basis: this checkout is tag **`v0.13.0`**, commit **`43284377d2466037628e57d8ad0c891778fdb45c`**
(shallow clone plus a fetched `v0.12.1` ref for set diffs). Inspection date **2026-10-29**. Installed
`/Applications/GridCraft.app` prints `GridCraft 0.13.0`; the GUI was never launched.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 354 engine `cmd!` ids (was 353); +`window.close`, `window.list` | grep count; id-string diff between the tags names exactly these two | implemented |
| 2 | One native window per workbook window; `view.newWindow` shares the workbook; `view.arrangeAll` tiles; drafts stay per workbook | `crates/engine/src/cmd/extra.rs:167-169` (`view.newWindow` spec: "opens another window on the active workbook (the same workbook: saving from either window saves it)"; `view.arrangeAll` present); PRs #2616–#2619 | implemented |
| 3 | **Control channel requires a token**: first line must authenticate; bad connections closed; token from `--control-token`/`GRIDCRAFT_CONTROL_TOKEN` or an auto-written user-only token file whose path is printed to stderr (`gridcraft-cli` reads it) | `apps/gridcraft/src/control_server.rs:4-5,26-42` (`make_token`, `control_auth`); PR #783 | implemented |
| 4 | 22 MCP tools (+`list_windows`), set otherwise unchanged | `crates/mcp/src/tools.rs` — 22 `tool(` calls; name-set diff vs `v0.12.1` = +`list_windows` only | implemented |
| 5 | 275/291 catalog ids (94.5%) unchanged; 19 languages unchanged | `docs/parity-checklist.md`; `ls crates/ui-egui/src/i18n/` = 19 | implemented metric |
| 6 | Open a saved workbook without recalculating | PR #2512 | implemented |
| 7 | AutoSum row total to the right; Options ▸ Formulas Max Iterations/Max Change; Chart Type stacked/100% stacked in Format Chart Area | PRs #2561, #2493, #2605 | implemented |
| 8 | SheetId kept across XLSX rewrite; faster XLSX save; skipped-drawing warnings; note/comment thread kept; sparklines removed with row/col | PRs #2513, #2749, #2555, #2515, #2551 | implemented |
| 9 | Formula fixes (PERCENTRANK, MINVERSE, ISOWEEKNUM/WEEKNUM 21, YEARFRAC basis 0, IMSQRT, repeated-sheet ranges); datetime past 9999 → None | PRs #2417, #2428, #2443, #2463, #2457, #2473, #2528 | implemented |
| 10 | Web `?chrome=` iframe option; XWayland drag-and-drop default on Wayland | PRs #2444, #165 | implemented |
| 11 | Startup update prompt + self-update; Windows per-user; egui 0.37 | PRs #2566, #2704, #2543 | implemented |
| 12 | Craft-libs crates at one rev | `Cargo.toml` / `apps/gridcraft/Cargo.toml` → `92d392cf…` | implemented |
| 13 | No `.xls`/`.xlsb`/`.ods` write; encryption read-only; macros never run; slicers/timelines not saved; no Power Query/data model | `docs/gaps.md`; `crates/xlsx/src/` | not implemented (verified absent) |

## 2. Automation-surface counts: v0.12.1 → v0.13.0

| Surface | v0.12.1 | v0.13.0 (measured) | Change |
|---|---:|---:|---|
| Engine commands | 353 | **354** | +`window.close`, +`window.list` |
| MCP tools | 21 | **22** | +`list_windows` |
| Control methods | 31 documented + aliases | **same set** | **now token-authenticated** |
| CLI subcommands | 11 | **11** | unchanged |
| Catalog coverage | 275/291 | **275/291** | unchanged |
| UI-only command ids | 15 | **same shape** | unchanged |
| Shortcut bindings | 70 | **70** | unchanged (no new shortcuts this wave) |
| Languages | 19 | **19** | unchanged |
| Chart kinds / functions | 26 / 513-504 of 523 | **same** | unchanged |
| Craft-libs pins | `d27646a5` (craft-print) | **`92d392cf…`** | unified |

## 3. Uncertain / not verified

- Shortcut-binding count carried from the baseline metric (no release PR adds one; the two new
  window commands carry none in their specs as read).
- GUI behaviour not launched; registry + docs + packaging are the evidence.
- Excel-repair-free output remains unproven by the project (`docs/gaps.md` §1).

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| README "89% of standard ribbon commands" | generated checklist 275/291 = 94.5% |
| `docs/target-app-parity.md` 274/290, "313 command ids" | 275/291, 354 `cmd!` ids |
| `docs/control-protocol.md` (no token) | the server requires a token since #783 |
| Baseline "One OS window; `view.newWindow` clones the workbook; `view.arrangeAll` does nothing" | **resolved this release** — window per workbook window, shared workbook, arrangeAll works |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # 43284377d2466037628e57d8ad0c891778fdb45c
grep -rho 'cmd!' crates/engine/src/ | wc -l                     # 354
grep -cE '^\s+tool\(' crates/mcp/src/tools.rs                   # 22
sed -n '4,5p;26,42p' apps/gridcraft/src/control_server.rs       # token auth + make_token
grep -oE '275 / 291|94\.5%' docs/parity-checklist.md | head -2
ls crates/ui-egui/src/i18n/ | wc -l                             # 19
```
