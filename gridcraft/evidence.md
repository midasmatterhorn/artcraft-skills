# GridCraft — evidence ledger (tag v0.14.2)

Audit basis: this checkout is tag **`v0.16.0`**, commit **`85e51e009c24fad47575f04d3c08f12342615d82`** ("Release 0.15.0", 2026-11-01; the v0.14.2 ref was fetched for id diffs). Inspection date **2026-11-02**. Installed `/Applications/GridCraft.app` matches the tag and prints `GridCraft 0.15.0`.

v0.14.2 → v0.16.0 delta: **no registry change** — 363 non-test `(cmd|spec)!` ids at both tags, zero added/removed; MCP tools 22 = 22 (`tools.rs` changed only for `write_range`: `parse` passthrough + doc); CLI subcommands, control dispatch, UI commands, 19 languages unchanged. Compatibility wave: .xls cell formatting + font family/charset (#2495/#3052), xlsx `_xlfn.` prefixes STOCKHISTORY/TRANSLATE/DETECTLANGUAGE (#2793), workbook view settings kept (#3062), Google Sheets DUMMYFUNCTION unwrap (#3075), per-column CSV date-order detection (#3043), YEARFRAC/MOD/NUMBERVALUE/PERCENTRANK Excel edge cases (#2657/#2979/#2980), `range.setValues` parse:false + converted report (#3042/#2255), locked-cell edit refusal (#3040), per-window ribbon tab (#3041), Alt,H,B keytips (#3077), Esc in file view (#3050), Intel wgpu shader skip (#3039), Dock-quit asking window (#3083), Merge & Center split-button label (#3024). ⚠️ The generated `docs/parity-checklist.md` reads **276/292 (94.5%) and is byte-identical at v0.14.2 and v0.16.0** — the previous ledger's 275/291 did not match its own pinned tag.
(shallow clone plus a fetched `v0.12.1` ref for set diffs). Inspection date **2026-10-29**. Installed
`/Applications/GridCraft.app` still prints `GridCraft 0.13.0` (bundle lags the tag); the GUI was never launched.

v0.13.0 → v0.14.2 delta: +9 engine commands (`macro.*`), macro recorder/step-editor UI,
macros persisted into xlsx, CSV export `values:true`, encrypted-xlsx integrity-key fix,
Ctrl+Arrow data-edge jumps, checkbox-cell printing, control-channel token deadline enforcement,
function-parity wave (YEARFRAC/MOD/NUMBERVALUE/PERCENTRANK/IMSQRT/HYPERLINK/UNICHAR/distributions).
MCP tools, control methods, CLI subcommands, catalog coverage: unchanged (re-counted).

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 354 engine `cmd!` ids (was 353); +`window.close`, `window.list` | grep count; id-string diff between the tags names exactly these two | implemented |
| 2 | One native window per workbook window; `view.newWindow` shares the workbook; `view.arrangeAll` tiles; drafts stay per workbook | `crates/engine/src/cmd/extra.rs:167-169` (`view.newWindow` spec: "opens another window on the active workbook (the same workbook: saving from either window saves it)"; `view.arrangeAll` present); PRs #2616–#2619 | implemented |
| 3 | **Control channel requires a token**: first line must authenticate; bad connections closed; token from `--control-token`/`GRIDCRAFT_CONTROL_TOKEN` or an auto-written user-only token file whose path is printed to stderr (`gridcraft-cli` reads it) | `apps/gridcraft/src/control_server.rs:4-5,26-42` (`make_token`, `control_auth`); PR #783 | implemented |
| 4 | 22 MCP tools (+`list_windows`), set otherwise unchanged | `crates/mcp/src/tools.rs` — 22 `tool(` calls; name-set diff vs `v0.12.1` = +`list_windows` only | implemented |
| 5 | 276/292 catalog ids (94.5%); 19 languages unchanged | `docs/parity-checklist.md` (byte-identical v0.14.2→v0.16.0; prev. ledger said 275/291 — stale); `ls crates/ui-egui/src/i18n/` = 19 | implemented metric |
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
| Catalog coverage | 275/291 | **276/292** (generated file says this at v0.13.0+; the v1.0.7 ledger's "275/291 at v0.14.2" was stale) | +1/+1 |
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
git -C <clone> rev-parse HEAD                                   # 85e51e009c24fad47575f04d3c08f12342615d82
grep -rho 'cmd!' crates/engine/src/ | wc -l                     # 354
grep -cE '^\s+tool\(' crates/mcp/src/tools.rs                   # 22
sed -n '4,5p;26,42p' apps/gridcraft/src/control_server.rs       # token auth + make_token
grep -oE '276 / 292|94\.5%' docs/parity-checklist.md | head -2
ls crates/ui-egui/src/i18n/ | wc -l                             # 19
```


## Round 2026-11-04 (refresh)

- Pinned to `v0.16.0` = `85e51e009c24fad47575f04d3c08f12342615d82` (installed `GridCraft 0.16.0`).
- +7 command ids (the `data.solver*` family, `insert.equation`/`equation.edit`, `python.set`/`python.output`); 320 ids.
- Id sets were diffed between the two tags with the same extraction method as the claims above; counts here are the new ones.
