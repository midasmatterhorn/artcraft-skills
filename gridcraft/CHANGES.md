# GridCraft — round 2026-11-07 changes

Re-pinned: v0.16.0 (`85e51e0`) -> v0.17.0 (`a6a6a49`, installed `GridCraft 0.17.0`).

## Corrected / re-measured

- Engine commands: the previous text said 363 at v0.16.0, which equals the full **372 minus the nine `macro.*` ids it documented separately**; the full registry at that tag is 372. v0.17.0 registers **385** (384 `cmd!` ids plus the one explicit `CommandSpec` literal `review.allowEditRanges`). **+13 names, none removed**: `control.assign`, `control.format`, `control.list`, `control.press`, `control.setValue`, `insert.button`, `insert.slider`, `insert.spinButton`, `range.move`, `selection.nextCorner`, `view.showSheetTabs`, `view.showHorizontalScrollBar`, `view.showVerticalScrollBar`.
- Catalog: **281/296 (94.9%)**, not 276/292; v0.16.0 measures 277/292, and the previous 276 is that count without `review.allowEditRanges` — the one command registered as a `CommandSpec` literal rather than through `cmd!` — so the old number was one short. The generated `docs/parity-checklist.md` agrees with code.
- Key tips: **413** sequences (365 in the previous text; the v0.16.0 JSON holds 367, so the old figure was two short). Shortcut bindings on command specs: **72** (70 before; v0.16.0 measured 71). UI-only command ids: **18** (15 before; v0.16.0 measured 17) — the previous list also omitted `app.checkForUpdates` and `ui.pythonMode`, and `options.highlightActiveRow` is the new one.
- Control methods: the "31 documented methods / 34 dispatch arms" sentence was replaced with the measured shape — **35 method names in 30 match arms** (unchanged this release) plus passthrough for any engine command id.
- Functions: **513 present by name, 10 absent, 9 stubs, 504 working** (unchanged at v0.17.0). The previous "18 of Excel's 523 names are absent" contradicted its own 513/523; the absent list is GETPIVOTDATA, IMAGE, STOCKHISTORY, TRANSLATE, DETECTLANGUAGE, CALL, REGISTER.ID, RTD, COPILOT, PY. `docs/function-parity.md`'s totals row is stale in the other direction (505/496, "18 missing", and PERCENTOF/TRIMRANGE listed as missing although both are registered).
- **HTML is no longer export-only**: opening a saved page now imports its table as a sheet (`read_html_table`, `crates/engine/src/io.rs`). The previous "falls through to the CSV/TSV reader" limitation was deleted.
- **Python cells and equations exist** and the previous "groundwork, not a feature / no Python-in-cells / no equation editor" bullet was wrong: `python.set`/`python.output` plus `ui.pythonMode` store Python code (never executed — new code shows `#BLOCKED!`), and `insert.equation`/`equation.edit` edit LaTeX equations that round-trip as OMML.
- Analysis ToolPak: **all 19 tools** (`TOOLS` in `crates/engine/src/cmd/analysis.rs`), not "13 of 19".
- "Opening a saved workbook without recalculating it" was **false** and was removed: `file.open` builds documents with `DocState::new`, which calls `Calc::recalc_all` (`crates/engine/src/lib.rs:295-299`), and the non-evaluating `from_saved` constructor is used only by a test. `.slk` opens keep their own name and path (no "(imported).xlsx" title), so Save is refused until Save As `.xlsx`.
- New surfaces added to the skill: form controls (`insert.button/slider/spinButton`, `control.*`, XLSX `<controls>`/`ctrlProp`/VML), one object selection with eight resize handles and `ui.object.select`, clipboard picture paste, per-workbook sheet-tab/scroll-bar visibility, active-row highlight, SYLK `.slk` import, `Ctrl+.` next corner, web `data-host="page"` host mode, R1C1/page-margin/remove-personal-information round trips, precision-as-displayed rounding, doughnut one-ring-per-series.
- Shape kinds corrected to **10** (`ShapeKind` now includes equation). Solver reports corrected to **Answer, Sensitivity and Limits**. Pivot limits corrected: filter items by label set exist; conditional/value filters do not.
- `--version` example was stale (`0.14.2` → **`GridCraft 0.17.0`**). The previous file's audit basis said v0.16.0 while its Sources section still said v0.15.0; both now say v0.17.0 with the full SHA and the 2026-11-07 inspection date.
- Shared-code pins: the single craft-libs rev was superseded — desktop crates at `c5a1cbfb…`, `craft-web-host` at `2e2312dd…`, egui 0.37 fork at `6d518fc7…`.
- Stale-prose list refreshed: README still says 89%, `docs/target-app-parity.md` still says 321 command ids, `docs/gaps.md` still says 59 shortcuts, `docs/control-protocol.md` now documents token authentication (the previous "not described" note was removed).

## Method

- `git diff v0.16.0..HEAD` in the read-only checkout: **237 files changed, +15,905/−1,370 lines** (the checkout keeps one release commit per tag, so the diff — not a commit count — is the delta evidence). HEAD verified as `a6a6a49a0415087474251b08e887a3581fab9e14` = tag `v0.17.0`; the installed bundle's `Contents/Info.plist` and `--version` output match 0.17.0.
- One count script (embedded in `evidence.md` §5) run at `HEAD` and at `v0.16.0` via `git show <ref>:<path>`: engine `cmd!` ids plus explicit `CommandSpec` ids, catalog ids ∩ registered ids, `tool(` calls, CLI dispatch, `handle()` arms, the "ui" array, non-`None` shortcut arguments, `crates/ui-egui/src/keytips/keytips.json`, `Language::ALL`, `ChartKind`, and the `f!` ∪ `SPECIAL_FUNCTIONS` name set. Its output is reproduced verbatim in `evidence.md`.
- Command/tool/control id sets were diffed between the tags with the same extraction, so "+13, none removed" and "same set" are set operations, not impressions.
- Every repo-relative path cited in `SKILL.md` was resolved against the clone (all exist; moved references re-cited, e.g. the token code moved to `apps/gridcraft/src/control_server.rs:59-73`). Docs, README and release notes were read but never used as the source of a number.
- Read-only discipline: `git show`/`git grep`/`git diff`, file reads, and the installed binary's `--version`. No build, no GUI launch, no clone modification.

## Unchanged

- **22 MCP tools** (same name set at both tags), **3 MCP resources**, `prompts/list` empty, protocol `2025-06-18`, 30 s remote timeout.
- **11 CLI subcommands** with the same flags; `check` still compares 14 categories with schema `gridcraft-check/1`.
- **35 control method names / 30 arms**, the token requirement (≥16 characters, 10 s, 4 KiB first line, 16 waiting, 64 MiB lines) and the queue/UI limits.
- **19 interface languages**, **26 ChartKinds**, **513/523 functions (504 working)**, 9 Backstage pages, 3 samples, 9 error stubs.
- Hard caps (512 MB part, 1 GB package, 2 GB read, 100,001 HTML rows, 512 MiB CSV, 16M array cells) and save semantics (only `.xlsx`/`.json` clear the dirty flag; `.xls/.xlsb/.ods/.slk` writes refused).
- Sections whose code path and counts did not move were path-verified at this tag and carried forward; no claim was silently re-dated.

## Known gap in this round

- No GUI was launched, so dialog/visual behaviour is code-derived, not observed. No Excel run and no real-world corpus: "opens in Excel without a repair prompt" remains unproven.
- The checkout carries only the v0.16.0 and v0.17.0 tags, so the v0.14.2→v0.15.0 paragraph is recorded history, not re-measured here.
- Accessibility-tree coverage, PDF glyph shaping, and `.xls`/`.xlsb`/`.ods` import depth were carried from the previous audit rather than re-exercised.
- Formats are enumerated from `FileKind` and the save/export paths rather than counted as a headline number; UI-only ids are counted from the advertised list, not from every handler in `crates/ui-egui/src/app/commands.rs`.
- Older history: the v0.14.0–0.14.2 macro-system paragraph was folded out of `SKILL.md` (which now keeps only the two most recent historical deltas) and is preserved below.

## Folded history (v0.14.0–0.14.2)

A macro system landed: Automate ▸ Record Macro (name, one-letter shortcut alone or after Ctrl+Shift, description), a Macros dialog with Trust Scripts for file-loaded scripts, a macro step editor with a debug bar and grid overlays, the `macro.*` engine commands, macros persisted into `.xlsx`, a save that refuses a macro that skipped the check, dry-run journaling and undo-group rollback. Also in that wave: CSV export `values: true` writes raw values, password-protected workbooks open again (hash-size integrity key), Ctrl+Arrow data-edge jumps during formula pointing, print outputs checkbox cells as boxes, structured references print as `@`-prefixed columns in double brackets, a status-bar statistic copies its value on click, the control channel enforces its 10 s token deadline and caps waiting connections, and a large function-parity wave (YEARFRAC basis 0, MOD, NUMBERVALUE, PERCENTRANK, IMSQRT, HYPERLINK, UNICHAR, base conversions, F/T/BINOM/BETA edges).
