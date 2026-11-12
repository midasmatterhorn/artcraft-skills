# GridCraft — round 2026-11-12 changes

Re-pinned: v0.17.0 (`a6a6a49`) -> v0.19.1 (`476448d`, installed `GridCraft 0.19.1`).

## Corrected / re-measured

- **CLI subcommands: 11 -> 12.** `sandbox-check` is new (`apps/gridcraft-cli/src/sandbox_check.rs`, dispatch in `apps/gridcraft-cli/src/main.rs`). The previous count listed the eleven known names inside the regex; it could not see a new subcommand. The count is now taken from the `Some(…)` dispatch arms of `main()` (12: `info`, `convert`, `eval`, `cat`, `run`, `check`, `sandbox-check`, `commands`, `functions`, `mcp`, `send`, `version`), and the script prints the names so the set is auditable.
- **Every other headline count re-measured and unchanged at v0.19.1:** 385 engine commands (id sets compared between tags: +0/−0), 281/296 catalog ids, 22 MCP tools (same 22 names), 35 control method names in 30 arms, 18 UI-only ids, 72 shortcut bindings (+5 macOS overrides), 413 key-tip sequences, 19 languages, 26 chart kinds, 513/523 worksheet functions (504 working), 3 MCP resources, 14 `check` categories, 9 Backstage pages, 3 samples, 10 shape kinds. Each sentence in `SKILL.md` now says "unchanged at v0.19.1" rather than leaving the v0.17.0 figure undated.
- **Text section rewritten.** The previous "no complex shaping (Arabic, Devanagari, Thai) and no bidi; text stays LTR inside its box" is now false for Arabic and other right-to-left text: cells carry a per-cell reading direction (`ReadingOrder`), egui shapes with harfrust and lays out with `unicode-bidi`, and Arabic faces joined the fallbacks. New text distinguishes what landed (Arabic bidi/shaping, editing navigation, cell direction, CJK baseline) from what did not (no Arabic UI catalog or mirrored shell, Devanagari/Thai unverified, PDF still has no Arabic glyphs and no bidi).
- **New surfaces added to the skill:** `crates/sandbox` and `gridcraft-cli sandbox-check` (Landlock ABI 3 + seccomp on Linux, `sandbox-exec` on macOS, canary check, exit 0/1/2, launcher exit 97); `window.gridcraft` page API in the web build (`request`/`execute`/`commands`/`docInspect`/`uiInspect`/`screenshot`, 30 s timeout); cell reading direction via `home.formatCells`; `B1`/`B2` calendar prefixes (Hijri) and Excel-exact 15-significant-digit rounding; legacy array formulas read with implicit `@`; lookup onto a blank target kept blank (#374); chart budgets (100,000 points/series, 2,000,000 per chart, 16 trendlines); MCP 16 MB message cap; 64 MiB SVG budget for one HTML page's charts; equations' input caps.
- **Regional formats deliberately not claimed.** `crates/core/src/region.rs` (CLDR separators, month names, date order, currency) and `Workbook::region` exist, but no Options page, command or format path reads them; the skill lists this as groundwork and warns against promising localized typing/display. Its `(Options › Region)` comments describe a page that does not exist.
- **Catalog labels corrected in the model:** pending SmartArt and WordArt entries are labelled **Diagram** and **Decorative Text** while keeping the ids `insert.smartArt`/`insert.wordArt` (`docs/feature-names.md`). No count changes.
- **`.xls` import re-read:** every `.xls` formula is legacy and now goes through the implicit-`@` reading; duplicate sheet names are refused; a shared formula whose text exceeds the text budget stops shared-formula expansion for the workbook. The documented import depth (values, formulas, formats, merges, sizes, names, display settings; no fonts/fills/borders/charts/pictures/comments/CF/validation/hyperlinks/freeze panes) is unchanged.
- **Stale-prose list refreshed:** README still says 89%, `docs/target-app-parity.md:58` still says 321 command ids, `docs/gaps.md` still says 59 shortcuts, and `docs/gaps.md` §5 now carries both an updated and an obsolete "Missing/Evidence" pair after the Arabic merge; `docs/control-protocol.md` still documents token authentication correctly.
- **`--version` example updated** from `GridCraft 0.17.0` to **`GridCraft 0.19.1`**; the audit basis, Sources section and shared-code pins were re-pinned (craft-libs `6e03f65b…`, `craft-web-host`/`craft-web-api` `fd5e2feff…`, egui fork unchanged at `6d518fc7…`).
- **Two older delta paragraphs kept, one folded.** `SKILL.md` now carries v0.17.0 → v0.19.1 plus the v0.16.0 → v0.17.0 and v0.15.0 → v0.16.0 history; the v0.14.2 → v0.15.0 paragraph moved to the folded history below.

## Method

- `git diff v0.17.0..HEAD` in the read-only checkout: **238 files changed, +18,427/−1,483 lines** (the checkout keeps one release commit per tag, so the diff — not a commit count — is the delta evidence). HEAD verified as `476448d7d9f3a5f8e93fcf7d98b47fd52293fe7f` = tag `v0.19.1`; the installed bundle's `Contents/Info.plist` and `--version` output match 0.19.1.
- One count script (embedded in `evidence.md` §5) run at `HEAD` and at `v0.17.0` via `git show <ref>:<path>`: engine `cmd!` ids plus explicit `CommandSpec` ids, catalog ids ∩ registered ids, `tool(` calls, the `main()` dispatch arms, `handle()` arms, the "ui" array, non-`None` shortcut arguments, `keytips.json`, `Language::ALL`, `ChartKind`, and the `f!` ∪ `SPECIAL_FUNCTIONS` name set. Its output is reproduced verbatim in `evidence.md`.
- Command id sets were compared between the tags with the same extraction, so "+0/−0" is a set operation, not an impression. MCP tool names were compared the same way (22 identical names).
- New claims were traced into the delta, not taken from release notes: the sandbox (`crates/sandbox/`, `docs/sandbox.md`, `xtask/src/layers.rs`), `window.gridcraft` (`apps/gridcraft-web/src/api.rs`, `packaging/web/README.md`), reading direction (`crates/model/src/style.rs`, `crates/xlsx/src/styles.rs`, `crates/ui-egui/src/text_direction.rs`), Hijri and rounding (`crates/numfmt/src/{calendar,decimal}.rs`), legacy arrays (`crates/xlsx/src/array_formula.rs`), chart budgets (`crates/chart/src/resolve.rs`), MCP cap (`crates/mcp/src/server.rs`), SVG budget (`crates/engine/src/chart_svg.rs`).
- Every repo-relative path cited in `SKILL.md` was resolved against the checkout; one malformed reference (`:xls.rs:253`) was fixed to `crates/xlsx/src/xls.rs:253`. The regional-format claim was demoted after a grep found no consumer of `Workbook::region`.
- Read-only discipline: `git show`/`git diff`/`git grep`, file reads, and the installed binary's `--version`. No build, no GUI launch, no checkout modification.

## Unchanged

- **385 engine commands**, **281/296 catalog ids**, **22 MCP tools**, **3 MCP resources**, `prompts/list` empty, protocol `2025-06-18`, 30 s remote timeout.
- **35 control method names / 30 arms**, the token requirement (≥16 characters, 10 s, 4 KiB first line, 16 waiting, 64 MiB lines) and the queue/UI limits.
- **18 UI-only ids**, **72 shortcut bindings** (+5 macOS overrides), **413 key-tips**, **19 interface languages**, **26 chart kinds**, **513/523 functions (504 working)**, 9 error stubs, 9 Backstage pages, 3 samples, 10 shape kinds, 14 `check` categories.
- Hard caps (512 MB part, 1 GB package, 2 GB read, 100,001 HTML rows, 512 MiB CSV, 16M array cells) and save semantics (only `.xlsx`/`.json` clear the dirty flag; `.xls/.xlsb/.ods/.slk` writes refused).
- Import depth for `.xls`/`.xlsb`/`.ods`/`.slk`, encryption read-only, macros never executed, Python cells storage-only, slicers/timelines not saved, no Power Query/data model, chart/pivot gaps, accessibility coverage.
- Sections whose code path and counts did not move were path-verified at this tag and carried forward; no claim was silently re-dated.

## Known gap in this round

- No GUI was launched, so dialog/visual behaviour is code-derived, not observed. No Excel run and no real-world corpus: "opens in Excel without a repair prompt" remains unproven.
- `gridcraft-cli` is not installed on this machine, so `sandbox-check`, `check` and `run` were not executed; the sandbox claims rest on `crates/sandbox` and `docs/sandbox.md`, and the CLI claims on the dispatch code.
- `window.gridcraft` was not exercised in a browser; the shared `craft-web-api` default (30 s timeout) was read in craft-libs, not observed.
- Arabic shaping/bidi was not observed on screen; it rests on the renderer, the bidi/editing tests and `docs/localization-parity.md`. Screen-reader behaviour in bidi text is unverified by the project itself.
- The checkout carries only the v0.17.0 and v0.19.1 tags, so the intermediate v0.18.0/v0.19.0 boundaries cannot be attributed; the diff is the aggregate delta.
- Accessibility-tree coverage, PDF glyph coverage beyond the new Arabic note, and `.xlsb`/`.ods` import depth were carried from the previous audit rather than re-exercised.
- Formats are enumerated from `FileKind` and the save/export paths rather than counted as a headline number; UI-only ids are counted from the advertised list, not from every handler in `crates/ui-egui/src/app/commands.rs`.

## Folded history

### v0.14.2 → v0.15.0 (folded out of `SKILL.md` this round)

A compatibility wave with no command-registry change: `.xls` files give up cell formatting but keep font family and charset; xlsx writes `_xlfn.` prefixes for STOCKHISTORY/TRANSLATE/DETECTLANGUAGE; workbook view settings survive an open + save; a Google Sheets `_xlfn._xlws.DUMMYFUNCTION` wrapper opens as the original formula; CSV/text detect each column's date order; formula edges match Excel (YEARFRAC basis 0, MOD, NUMBERVALUE, PERCENTRANK); `range.setValues` takes `parse: false` with a `converted` report; a locked cell's edit is refused before a draft can block Save.

### v0.14.0 → v0.14.2 (folded in the previous round)

A macro system landed: Automate ▸ Record Macro (name, one-letter shortcut alone or after Ctrl+Shift, description), a Macros dialog with Trust Scripts for file-loaded scripts, a macro step editor with a debug bar and grid overlays, the `macro.*` engine commands, macros persisted into `.xlsx`, a save that refuses a macro that skipped the check, dry-run journaling and undo-group rollback. Also in that wave: CSV export `values: true` writes raw values, password-protected workbooks open again (hash-size integrity key), Ctrl+Arrow data-edge jumps during formula pointing, print outputs checkbox cells as boxes, structured references print as `@`-prefixed columns in double brackets, a status-bar statistic copies its value on click, the control channel enforces its 10 s token deadline and caps waiting connections, and a large function-parity wave (YEARFRAC basis 0, MOD, NUMBERVALUE, PERCENTRANK, IMSQRT, HYPERLINK, UNICHAR, base conversions, F/T/BINOM/BETA edges).
