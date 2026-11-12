# GridCraft — evidence ledger (tag v0.19.1)

Audit basis: this checkout is tag **`v0.19.1`**, commit **`476448d7d9f3a5f8e93fcf7d98b47fd52293fe7f`** ("Merge tested main for Flatpak update patch release"). Inspection date **2026-11-12**. The installed GridCraft bundle matches the tag: `Info.plist` `CFBundleShortVersionString` 0.19.1, `CFBundleIdentifier` `ai.storyteller.gridcraft`, and its binary prints `GridCraft 0.19.1` (run with `--version` only; the GUI was never launched). The previous release this skill described was **v0.17.0** (`a6a6a49a0415087474251b08e887a3581fab9e14`), also present in the checkout and inspected for id/count diffs.

**v0.17.0 → v0.19.1 delta (from `git diff v0.17.0..HEAD`, not release notes):** 238 files changed, +18,427/−1,483 lines. **No register change**: 385 command ids at both tags, set-diff +0/−0; catalog 281/296; 22 MCP tools; 35 control names / 30 arms; 18 UI-only ids; 72 shortcut bindings; 413 key-tips; 19 languages; 26 chart kinds; 513/523 functions — all identical. New surfaces: **`gridcraft-cli sandbox-check`** (12th subcommand) over a new **`crates/sandbox`** crate (Landlock ABI 3 + seccomp on Linux, `sandbox-exec` on macOS, canary enforcement check, layer 0 in `xtask/src/layers.rs`); **`window.gridcraft`** page API in the web build (`apps/gridcraft-web/src/api.rs`, shared `craft-web-api`); **cell reading direction** (`ReadingOrder` in `crates/model/src/style.rs`, XLSX `readingOrder` in `crates/xlsx/src/styles.rs`, `crates/ui-egui/src/text_direction.rs`); **Arabic bidi/shaping** and Arabic font fallback; **`B1`/`B2` Hijri calendar** (`crates/numfmt/src/calendar.rs`) plus Excel-exact 15-digit rounding (`crates/numfmt/src/decimal.rs`); **legacy array-formula reading** (`crates/xlsx/src/array_formula.rs`); **chart point/trendline budgets** (`crates/chart/src/resolve.rs`); **MCP 16 MB message cap** (`crates/mcp/src/server.rs`); **64 MiB SVG budget for HTML export** (`crates/engine/src/chart_svg.rs`); catalog labels SmartArt → **Diagram**, WordArt → **Decorative Text** (`docs/feature-names.md`). Groundwork that is *not* wired: `crates/core/src/region.rs` regional formats and `Workbook::region` (`crates/model/src/workbook.rs:271-276`) have no setter, UI or reader.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | **385 engine commands** at v0.19.1 (same 385 at v0.17.0, set-diff +0/−0) | `cmd!` first-literal ids reachable from `command_specs()` (`crates/engine/src/cmd.rs:160`) plus the explicit `CommandSpec { id: "review.allowEditRanges", … }` (`crates/engine/src/cmd/review.rs`); id sets compared between tags | implemented |
| 2 | **281/296 Excel catalog ids (94.9%)**, unchanged | `crates/engine/src/catalog.rs` (296 distinct ids) ∩ registered ids = 281; matches generated `docs/parity-checklist.md`; 15 missing: `insert.smartArt/screenshot/map/timeline/wordArt/signatureLine/object`, `data.fromWeb/stocks/geography/relationships/analyzeData`, `review.smartLookup/translate/showChanges` | implemented metric |
| 3 | **Cell reading direction** Context/LTR/RTL per cell, independent of sheet RTL, XLSX `readingOrder` | `crates/model/src/style.rs:354,372` (`ReadingOrder`, `Align::reading_order`), `crates/engine/src/cmd/format.rs:88` (`home.formatCells` params), `crates/xlsx/src/styles.rs:272,616-618`, `crates/ui-egui/src/dialogs/format_cells.rs:103`, `crates/ui-egui/src/text_direction.rs` (Context = first non-whitespace bidi class), `crates/ui-egui/src/formula_bar.rs:249,501-505` | implemented |
| 4 | **Arabic shaping + bidi in cells, editor and formula bar**; caret and word deletion navigate visually | egui 0.37 shaping + `unicode-bidi = "=0.3.18"` (`crates/ui-egui/Cargo.toml`), `crates/ui-egui/tests/arabic_bidi.rs`, `crates/ui-egui/tests/arabic_editing.rs`; Arabic fallbacks `crates/ui-egui/src/theme/font_fallback.rs:316-327`, craft-fonts face `crates/ui-egui/src/craft_fonts_policy.rs:27` | implemented (visual/screen-reader behaviour unverified) |
| 5 | **`B1`/`B2` calendar prefixes**: hidden, `B2` = tabular Hijri in Arabic, misplaced prefix → General and `TEXT` `#VALUE!` | `crates/numfmt/src/calendar.rs`, `crates/numfmt/src/parse.rs`, `crates/numfmt/src/lib.rs` (`invalid`), tests `crates/numfmt/src/tests.rs:944-964` | implemented |
| 6 | **Excel-exact decimal rounding** (15 significant digits, half away from zero) | `crates/numfmt/src/decimal.rs:1-30,293-294`, `crates/numfmt/tests/golden/{general,codes}.txt`, `crates/numfmt/tests/render_equality.rs` | implemented |
| 7 | **Legacy (no-`cm`) formulas read with implicit `@`**, do not spill; save adds `cm` only to genuinely dynamic formulas | `crates/xlsx/src/array_formula.rs` (`apply_legacy`, `export`), `crates/xlsx/src/read.rs:473`, `crates/xlsx/src/xls.rs:253`, `crates/xlsx/src/sheet_write.rs:655-660`; `crates/engine/tests/legacy_array_functions.rs` | implemented |
| 8 | **Lookups keep an empty target blank** (0 only as the displayed final result) | `crates/functions/src/lookup.rs` (removal of `cell_result`, #374) | implemented |
| 9 | **`crates/sandbox`**: Landlock ABI 3 + seccomp (Linux), `sandbox-exec` (macOS), canary enforcement check, cleared env but `LANG`/`LC_*`/`TZ`, launcher exit 97 when refused, layer 0 | `crates/sandbox/src/{lib,policy,canary,probe,macos,linux}.rs`, `crates/sandbox/Cargo.toml`, `xtask/src/layers.rs:33`, `docs/sandbox.md` | implemented (groundwork: no caller but `sandbox-check`) |
| 10 | **`gridcraft-cli sandbox-check`**: self-test or confined `-- PROGRAM`, `--read`/`--exec`, exit 0/1/2 | `apps/gridcraft-cli/src/sandbox_check.rs`, `apps/gridcraft-cli/src/main.rs:91`, `apps/gridcraft-cli/tests/it/sandbox.rs` | implemented |
| 11 | **`window.gridcraft`** page API: `request`, `execute`, `commands`, `docInspect`, `uiInspect`, `screenshot`; 30 s promise timeout; abandoned call released | `apps/gridcraft-web/src/api.rs`, `apps/gridcraft-web/src/main.rs:16-20,28`, `packaging/web/README.md`; the shared `craft-web-api` crate in craft-libs (`crates/web-api/src/page.rs` there: default timeout 30 s) | implemented (wasm; not exercised in a browser here) |
| 12 | **Chart budgets**: 100,000 points/series, 255 series, 2,000,000 points/chart (points clipped, no series dropped), 16 trendlines/chart | `crates/chart/src/resolve.rs:11-18`, `crates/chart/src/tests/budget.rs`, `crates/chart/src/render_perf_tests.rs` | implemented |
| 13 | **MCP stdio caps a message at 16 MB** (`-32600` invalid request, rest of the line dropped) | `crates/mcp/src/server.rs` (`read_message`, `skip_line`), `crates/mcp/src/tests.rs` | implemented |
| 14 | **Control channel requires a token**; 10 s auth, 4 KiB first line, 16 waiting; 64 MiB later lines | `apps/gridcraft/src/control_server.rs:4-5,23-29,59-73,110-140`; `crates/mcp/src/control_auth.rs:19-21` | implemented |
| 15 | **22 MCP tools** (same names at both tags), 3 resources, protocol `2025-06-18`, 30 s remote timeout | `crates/mcp/src/tools.rs`, `crates/mcp/src/server.rs:11-36,190`, `crates/mcp/src/backend.rs:21` | implemented |
| 16 | **12 CLI subcommands** (11 at v0.17.0; `sandbox-check` new) | `Some(…)` dispatch arms of `main()`: `apps/gridcraft-cli/src/main.rs:85-96` | implemented |
| 17 | **`check` compares 14 categories** with the cached-value oracle | `apps/gridcraft-cli/src/check/fidelity.rs` (14 `Diffs::new`, incl. `package`), `apps/gridcraft-cli/src/check/calc.rs`, `apps/gridcraft-cli/src/check/package.rs` | implemented |
| 18 | **35 control method names / 30 dispatch arms**, plus any command id as a method | `crates/ui-egui/src/control.rs` `handle()` + `find_command` fallthrough | implemented |
| 19 | **18 UI-only command ids** (unchanged) | the `(id, label, params)` array pushed with `"ui": true` in `crates/ui-egui/src/control.rs`; handlers in `crates/ui-egui/src/app/commands.rs` | implemented |
| 20 | **72 shortcut bindings** on command specs + 5 macOS-only overrides | non-`None` fourth `cmd!` argument; `shortcut_mac: Some(...)` ×5; `crates/ui-egui/src/keymap.rs` | implemented |
| 21 | **413 key-tip sequences** | `crates/ui-egui/src/keytips/keytips.json` `sequences` (413) = `crates/ui-egui/src/keytips/keytip_table/generated.rs` entries (413); generated by `xtask/src/keytips.rs` | implemented |
| 22 | **19 languages**, unchanged | `crates/ui-egui/src/i18n.rs` (`ALL: [Self; 19]`), `crates/ui-egui/src/i18n/` | implemented |
| 23 | **26 ChartKinds**, unchanged; 6 trendline types; doughnut = one ring per series | `crates/model/src/features.rs:428`, `crates/chart/src/render/kinds.rs`, `crates/chart/src/trend.rs` | implemented |
| 24 | **513/523 functions by name, 504 working**, unchanged | `f!` names outside `#[cfg(test)]` (491) ∪ `SPECIAL_FUNCTIONS` (33) = 515 distinct, minus `USDOLLAR`/`ECMA.CEILING` = 513; 7 CUBE + `WEBSERVICE` + `FILTERXML` are `#VALUE!`/`#N/A` stubs (9) → 504 working; 10 absent (GETPIVOTDATA, IMAGE, STOCKHISTORY, TRANSLATE, DETECTLANGUAGE, CALL, REGISTER.ID, RTD, COPILOT, PY) | implemented metric |
| 25 | **Python cells exist but never run**; no `PY` function | `crates/engine/src/cmd/python.rs` (`python.set`, `python.output`, `#BLOCKED!`), `crates/xlsx/src/python_part.rs`, `ui.pythonMode` | implemented (storage only) |
| 26 | **Equations**: LaTeX source, OMML subset, caps 4 KB / depth 32 / 2,500 matrix cells / no macros | `crates/engine/src/cmd/equation.rs`, `crates/xlsx/src/omml.rs`, `crates/math/src/lib.rs:28-38,229-232` | implemented |
| 27 | **Regional formats are groundwork only**: CLDR table + `Workbook::region`, no setter/UI/reader | `crates/core/src/region.rs`, `crates/model/src/workbook.rs:271-276`; the only other use is the re-export in `crates/core/src/lib.rs:18` — nothing sets a region and no formatter reads it (grep) | not implemented (verified absent) |
| 28 | **No `.xls`/`.xlsb`/`.ods`/`.slk` write; encryption read-only; macros never run; slicers/timelines not saved; no Power Query/data model/From Web** | `crates/engine/src/io.rs` (save refusals), `docs/gaps.md` §3/§7/§8/§12, catalog missing list (`data.fromWeb` absent) | not implemented (verified absent) |
| 29 | **Save semantics**: only `.xlsx`/`.json` clear the dirty flag | `crates/engine/src/cmd/file.rs:133-146` | implemented |
| 30 | **HTML export caps one page's chart SVG at 64 MiB** and fails rather than dropping a chart | `crates/engine/src/chart_svg.rs:13-15,34-40` | implemented |

## 2. Count ledger — v0.17.0 → v0.19.1 (method named)

| Surface | v0.17.0 (measured) | v0.19.1 (measured) | Method |
|---|---:|---:|---|
| Engine commands | 385 | **385** (unchanged; set-diff +0/−0) | `cmd!` first-literal ids reachable from `command_specs()` + explicit `CommandSpec` ids, compared as sets |
| Catalog coverage | 281 / 296 | **281 / 296** (unchanged) | distinct `crates/engine/src/catalog.rs` ids ∩ registered ids; cross-checked against `docs/parity-checklist.md` |
| MCP tools | 22 | **22** (unchanged) | `tool(` definitions in `crates/mcp/src/tools.rs`; same 22 names |
| CLI subcommands | 11 | **12** (`sandbox-check` new) | `Some(…)` arms of `main()`'s dispatch; `--version`/`-V` share `version`, `--help` is not a subcommand |
| Control method names / arms | 35 / 30 | **35 / 30** (unchanged) | `handle()` match arms in `crates/ui-egui/src/control.rs` (aliases share an arm) |
| UI-only command ids | 18 | **18** (unchanged) | entries in the `engine.commands` "ui" array |
| Shortcut bindings (command specs) | 72 | **72** (unchanged) | non-`None` 4th `cmd!` argument (+5 `shortcut_mac` overrides) |
| Key-tip sequences | 413 | **413** (unchanged) | `keytips.json` `sequences` length = generated table entries |
| Interface languages | 19 | **19** (unchanged) | `Language::ALL` |
| Chart kinds | 26 | **26** (unchanged) | `ChartKind` variants |
| Worksheet functions | 513 / 523 by name, 504 working | **513 / 523, 504 working** (unchanged) | `f!` names outside test modules ∪ `SPECIAL_FUNCTIONS` − non-Excel names; stubs subtracted |
| MCP resources | 3 | **3** (unchanged) | resource URIs in `crates/mcp/src/server.rs` |
| `check` categories | 14 | **14** (unchanged) | `Diffs::new` calls in `apps/gridcraft-cli/src/check/fidelity.rs` (13 + `package`) |
| Backstage pages | 9 | **9** (unchanged) | `Page::ALL` in `crates/ui-egui/src/backstage.rs` |
| Built-in samples | 3 | **3** (unchanged) | `SAMPLES` in `crates/engine/src/sample.rs` |
| Shape kinds | 10 | **10** (unchanged) | `ShapeKind` variants in `crates/model/src/features.rs:657` |

Deliberately **not** counted as headline numbers: formats (enumerated from `FileKind` and the save/export paths), token/queue/screenshot limits (quoted from constants), chart point budgets (quoted from constants), and the project's own estimate percentages (`docs/target-app-parity.md`: ~75% breadth, ~50% ready), which are estimates rather than measurements.

## 3. Uncertain / not verified

- **GUI behaviour is not exercised.** No window was launched; UI claims rest on command/spec/UI code and unit/integration tests, not on screenshots. Anything phrased "the dialog does X" is code-derived.
- **`window.gridcraft` was not exercised in a browser.** The wiring is in `apps/gridcraft-web/src/api.rs` and the shared crate's documentation/tests; the 30 s timeout is `craft-web-api`'s default, read in craft-libs, not observed.
- **The sandbox was not exercised on this machine.** `gridcraft-cli` is not installed (`which gridcraft-cli` found nothing), and no build was run; the claims come from `crates/sandbox` + `docs/sandbox.md`. Its behaviour on a machine without Landlock 6.2 or without `/usr/bin/sandbox-exec` is documented, not tested here.
- **Arabic rendering was not observed.** Shaping/bidi claims rest on egui's renderer, `crates/ui-egui/tests/{arabic_bidi,arabic_editing}.rs` and `crates/ui-egui/tests/cjk_baseline.rs`; physical screen-reader behaviour in bidi text is explicitly unverified (`docs/localization-parity.md`).
- **Excel-repair-free output remains unproven by the project** (`docs/gaps.md` §1): `check` validates GridCraft against itself and the file's cached values, not against Excel.
- **Accessibility tree coverage** (grid cells and ribbon not exposed) and **PDF glyph coverage** for CJK/Arabic/Devanagari/Thai are carried from the previous audit; the PDF crate did not change in this delta (`crates/pdf` is absent from the diff).
- **`.xlsb`/`.ods`/`.xls` import depth** carried from the previous audit; the readers were not re-exercised (no corpus files in the checkout). `.xls` was only re-read for the legacy-formula path.
- Chart subtype coverage ("~26 of Excel's ~60") is the previous audit's ratio; only the enum count (26) was re-measured.
- **v0.18.0 and v0.19.0 are not in this checkout** (two release tags only), so the v0.17.0 → v0.19.1 diff is the aggregate delta; intermediate release boundaries cannot be attributed.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `README.md:207`: "covers 89% of standard ribbon commands" | 281/296 = 94.9% (generated checklist) |
| `docs/target-app-parity.md:58`: "321 command ids registered" | 385 registered (384 `cmd!` + 1 `CommandSpec`) |
| `docs/gaps.md` §9: "59 command shortcuts" | 72 shortcut bindings on command specs (+5 macOS overrides) |
| `docs/function-parity.md` headline: 513/523 by name, 504 working | agrees with code |
| `docs/function-parity.md` totals row: 505/496, "18 missing, 9 stubs" | 513 present / 10 absent / 9 stubs; the row also lists PERCENTOF and TRIMRANGE as missing although both are registered |
| `docs/localization-parity.md` script paragraph | merged badly too: it says "egui uses harfrust shaping and Unicode bidi layout" and, a few lines later, "There is no complex-text shaping: Arabic and Devanagari don't join or reorder, and there is no bidirectional layout" |
| `docs/gaps.md` §5 | merged badly: an updated "Missing/Evidence" pair (Arabic shaping/bidi landed) is followed by the obsolete pair (no shaping, no bidi); the file now contradicts itself |
| `crates/core/src/region.rs` docs and `Workbook::region` comment say "(Options › Region)" and describe typing/display | no Options page, command, or reader consumes the table; every workbook is en-US |
| `ATTRIBUTION.md` row for CLDR data | accurate as attribution for the new data module, but the module is unused so far |
| `docs/parity-checklist.md` | matches code (281/296; generated by `cargo xtask parity`) |
| `docs/control-protocol.md` auth section | describes the token and limits correctly |
| `docs/sandbox.md` "Python cells don't run" | agrees with `crates/engine/src/cmd/python.rs` (`#BLOCKED!`) |

## 5. Verification (read-only, reproduced for this ledger)

All counts were produced with one script run at each tag; it uses `git show <ref>:<path>`, so nothing is checked out or modified. It is the method of record for this round:

```python
# run from the checkout root: python3 counts.py HEAD   /   python3 counts.py v0.17.0
import json, re, subprocess, sys
REF = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
def show(p):
    return subprocess.run(["git", "show", f"{REF}:{p}"], capture_output=True, text=True).stdout
def files(pre):
    out = subprocess.run(["git", "ls-tree", "-r", "--name-only", REF, "--", pre],
                         capture_output=True, text=True).stdout.split()
    return [f for f in out if f.endswith(".rs")]

ids = set()
for f in files("crates/engine/src"):
    src = show(f)
    ids |= set(re.findall(r'cmd!\s*\(\s*(?:query\s+|noundo\s+)?"([^"]+)"', src))
    ids |= set(re.findall(r'CommandSpec\s*\{\s*id:\s*"([^"]+)"', src))
print("engine commands:", len(ids))

cat = re.search(r'pub const CATALOG[^=]*=\s*&\[(.*?)\n\];', show("crates/engine/src/catalog.rs"), re.S).group(1)
cat_ids = []
for m in re.finditer(r'\(\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)"\s*\)', cat):
    if m.group(1) not in cat_ids:
        cat_ids.append(m.group(1))
print("catalog:", sum(i in ids for i in cat_ids), "/", len(cat_ids))

print("mcp tools:", len(re.findall(r'\btool\(\s*"[a-z_]+"', show("crates/mcp/src/tools.rs"))))

main = show("apps/gridcraft-cli/src/main.rs")
# A subcommand is a `Some("...")` arm of main()'s dispatch; `--version`/`-V` share the `version` arm,
# `--help`/`-h` share `help`, which is not a subcommand.
disp = re.search(r'let r = match args\.first\(\).*?\n    \};', main, re.S).group(0)
subs = set()
for arm in re.findall(r'Some\(([^)]*)\)\s*=>', disp):
    for name in re.findall(r'"([^"]+)"', arm):
        if not name.startswith("-") and name != "help":
            subs.add(name)
print("cli subcommands:", len(subs), sorted(subs))

ctl = show("crates/ui-egui/src/control.rs")
hands = ctl[ctl.index("pub fn handle("):]
arms = re.findall(r'^\s{8}((?:"[a-z][^"]*"\s*\|\s*)*"[a-z][^"]*")\s*=>', hands, re.M)
print("control names:", len({n for a in arms for n in re.findall(r'"([^"]+)"', a)}), "arms:", len(arms))
ui = ctl[ctl.index("for (id, label, params) in ["):]
print("ui-only ids:", len(re.findall(r'\(\s*"([a-z][A-Za-z.]+)"', ui[:ui.index("] {")])))

n = 0
for f in files("crates/engine/src"):
    src = show(f)
    for m in re.finditer(r'cmd!\s*\(', src):
        i = src.index("(", m.start()); d = 0; j = i
        while d or j == i:
            d += {"(": 1, ")": -1}.get(src[j], 0)
            j += 1
            if d == 0:
                break
        args, cur, depth, instr, esc = [], "", 0, False, False
        for ch in src[i + 1:j - 1]:
            if esc: cur += ch; esc = False; continue
            if ch == "\\" and instr: cur += ch; esc = True; continue
            if ch == '"': instr = not instr; cur += ch; continue
            if not instr and ch in "([{": depth += 1
            elif not instr and ch in ")]}": depth -= 1
            elif not instr and ch == "," and depth == 0: args.append(cur.strip()); cur = ""; continue
            cur += ch
        args.append(cur.strip())
        n += len(args) > 3 and args[3] != "None"
print("shortcut bindings:", n)

print("keytips:", len(json.loads(show("crates/ui-egui/src/keytips/keytips.json"))["sequences"]))
print("languages:", re.search(r'ALL: \[Self; (\d+)\]', show("crates/ui-egui/src/i18n.rs")).group(1))
ck = re.search(r'pub enum ChartKind \{(.*?)\n\}', show("crates/model/src/features.rs"), re.S).group(1)
print("chart kinds:", len([l for l in ck.splitlines() if re.match(r'\s+[A-Z][A-Za-z0-9]+,$', l)]))

fnames = set()
for f in files("crates/functions/src"):
    if "/tests" in f or f.endswith("/tests.rs"):
        continue
    src = show(f)
    cut = src.find("#[cfg(test)]\nmod tests")
    src = src[:cut] if cut != -1 else src
    fnames |= set(re.findall(r'f!\(\s*(?:volatile;\s*)?"([A-Za-z0-9._]+)"', src))
sp = re.search(r'SPECIAL_FUNCTIONS: &\[&str\] = &\[(.*?)\n\];', show("crates/calc/src/eval/special.rs"), re.S).group(1)
ours = (fnames | set(re.findall(r'"([A-Za-z0-9._]+)"', sp))) - {"USDOLLAR", "ECMA.CEILING"}
print("functions present:", len(ours), "f!:", len(fnames))
```

Output at `HEAD` (v0.19.1):

```text
engine commands: 385
catalog: 281 / 296
mcp tools: 22
cli subcommands: 12 ['cat', 'check', 'commands', 'convert', 'eval', 'functions', 'info', 'mcp', 'run', 'sandbox-check', 'send', 'version']
control names: 35 arms: 30
ui-only ids: 18
shortcut bindings: 72
keytips: 413
languages: 19
chart kinds: 26
functions present: 513 f!: 491
```

Output at `v0.17.0`:

```text
engine commands: 385
catalog: 281 / 296
mcp tools: 22
cli subcommands: 11 ['cat', 'check', 'commands', 'convert', 'eval', 'functions', 'info', 'mcp', 'run', 'send', 'version']
control names: 35 arms: 30
ui-only ids: 18
shortcut bindings: 72
keytips: 413
languages: 19
chart kinds: 26
functions present: 513 f!: 491
```

A second script compared the two id sets: `v0.17.0: 385 HEAD: 385`, `added: []`, `removed: []`.

Other spot checks (plain shell):

```sh
git -C <checkout> rev-parse HEAD                     # 476448d7d9f3a5f8e93fcf7d98b47fd52293fe7f
git -C <checkout> describe --tags                    # v0.19.1
git -C <checkout> diff --shortstat v0.17.0..HEAD     # 238 files changed, 18427 insertions(+), 1483 deletions(-)
git -C <checkout> rev-list --count v0.17.0..HEAD     # 1: one release commit per tag, so the diff is the delta evidence
"GridCraft.app/Contents/MacOS/GridCraft" --version    # GridCraft 0.19.1 (read-only)
grep -c 'Diffs::new(' apps/gridcraft-cli/src/check/fidelity.rs   # 14
grep -rn --include='*.rs' -e 'region::' -e '\.region' crates apps   # re-export + the default value only
```

## 6. Carried forward from the v0.17.0 ledger

- Control-channel limits (64 MiB line, 10,000 pointer events, 8 MiB synthetic input, 60 s UI wait, 10 s auth, 4 KiB auth line, 16 waiting), MCP error codes, the 30 s remote socket timeout and the `check` exit-code contract were re-read in code and are unchanged.
- Hard caps (512 MB XLSX part, 1 GB package, 2 GB file read, 100,001 HTML rows, 512 MiB CSV, 16M array cells) were re-read from their constants and are unchanged; the 64 MiB per-page SVG budget is new.
- Text shaping/PDF font limitations beyond Arabic, accessibility coverage, large-workbook limits and the Excel-verification gap are carried from the previous round (see §3).
- Shared-code pins were refreshed: craft-libs `6e03f65b…` (craft-update, craft-window, craft-ui, craft-print), `craft-web-host`/`craft-web-api` `fd5e2feff…`, egui 0.37 fork `6d518fc7…`. The previous `c5a1cbfb…` and `2e2312dd…` pins are superseded.
