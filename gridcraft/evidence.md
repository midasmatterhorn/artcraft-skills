# GridCraft — evidence ledger (tag v0.17.0)

Audit basis: this checkout is tag **`v0.17.0`**, commit **`a6a6a49a0415087474251b08e887a3581fab9e14`** ("Release 0.17.0"). Inspection date **2026-11-07**. The installed GridCraft.app bundle matches the tag: `Info.plist` `CFBundleShortVersionString` 0.17.0, `CFBundleIdentifier` `ai.storyteller.gridcraft`, and its binary prints `GridCraft 0.17.0` (run with `--version` only; the GUI was never launched). The previous release this skill described was **v0.16.0** (`85e51e009c24fad47575f04d3c08f12342615d82`), also present in the checkout and inspected for id/count diffs.

**v0.16.0 → v0.17.0 delta (from `git diff v0.16.0..HEAD`, not release notes):** 237 files changed, +15,905/−1,370 lines. +13 register ids, none removed: `control.assign`, `control.format`, `control.list`, `control.press`, `control.setValue`, `insert.button`, `insert.slider`, `insert.spinButton`, `range.move`, `selection.nextCorner`, `view.showSheetTabs`, `view.showHorizontalScrollBar`, `view.showVerticalScrollBar`. New surfaces: form controls (model `ControlKind` + `crates/xlsx/src/controls.rs` + `crates/ui-egui/src/form_controls.rs`), one object selection with eight resize handles (`crates/ui-egui/src/objects.rs`), SYLK import (`crates/engine/src/io/sylk.rs`), HTML-table import (`read_html_table` in `crates/engine/src/io.rs`), clipboard picture paste (`crates/ui-egui/src/app/clipboard.rs`), active-row highlight (`crates/ui-egui/src/grid/active_row.rs`), web page host mode (`apps/gridcraft-web/src/{host.rs,hostmode.rs}`, `craft-web-host`). Key-tip sequences 367 → 413; shortcut bindings 71 → 72; UI-only ids 17 → 18. Registry 372 → 385; catalog 277/292 → 281/296.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | **385 engine commands** at v0.17.0 (372 at v0.16.0), +13/−0 this release | 384 distinct `cmd!("id"` first literals reachable from `command_specs()` (`crates/engine/src/cmd.rs`) + the one explicit `CommandSpec { id: "review.allowEditRanges", … }` (`crates/engine/src/cmd/review.rs:33-44`); id sets diffed between tags | implemented |
| 2 | **281/296 Excel catalog ids (94.9%)** | `crates/engine/src/catalog.rs` (296 distinct ids) ∩ registered ids = 281; matches generated `docs/parity-checklist.md`; 15 missing ids: `insert.smartArt/screenshot/map/timeline/wordArt/signatureLine/object`, `data.fromWeb/stocks/geography/relationships/analyzeData`, `review.smartLookup/translate/showChanges` | implemented metric |
| 3 | **Form controls**: buttons, sliders, spin buttons; Assign Action, Format Control; XLSX round trip | `crates/engine/src/cmd/controls.rs` (`insert.button/slider/spinButton`, `control.list/format/assign/setValue/press`), `crates/model/src/features.rs:759` (`ControlKind`), `crates/xlsx/src/controls.rs` (new file), `crates/ui-egui/src/form_controls.rs` (new file) | implemented |
| 4 | **One object selection**, eight resize handles, one undo step per drag, `ui.object.select` | `crates/ui-egui/src/objects.rs:8-30` (`Handle::ALL: [Handle; 8]`), `crates/ui-egui/src/control.rs` (`ui.object.select` arm), `ui.inspect` reports the selected object | implemented |
| 5 | **SYLK `.slk` import only** (values, R1C1→A1 formulas, formats, widths; save refused) | `crates/engine/src/io/sylk.rs`, `crates/engine/src/io.rs:40` (`"slk"`), `:323` (open), `:514` (save refusal message) | implemented |
| 6 | **HTML table import** lands: a saved page's table opens as a sheet | `crates/engine/src/io.rs:300,371-430` (`read_html_table`, sniffed on `<!doctype html`, `<html`, `<table`, `<head`, `<body`, `<meta`; header cells bold); `file.exportHtml` writes one sheet (`:748`, 100,001-row cap) | implemented |
| 7 | **Control channel requires a token**; 10 s auth, 4 KiB first line, 16 waiting; 64 MiB later lines | `apps/gridcraft/src/control_server.rs:4-5,23-29,59-73`; `crates/mcp/src/control_auth.rs` (`MIN_TOKEN_LEN = 16`, `token_path`, `client_token`) | implemented |
| 8 | **22 MCP tools, unchanged**; 3 resources; protocol 2025-06-18; 30 s remote timeout | `crates/mcp/src/tools.rs` (22 `tool(` calls, same name set at both tags), `crates/mcp/src/server.rs:11,34-36` (protocol version, resource URIs), `crates/mcp/src/backend.rs:21`; `prompts/list` empty (`server.rs:190`) | implemented |
| 9 | **11 CLI subcommands**, unchanged; `.slk` readable by `convert` | `apps/gridcraft-cli/src/main.rs:68-88` (dispatch), `:242-575` (per-subcommand flags) | implemented |
| 10 | **`check`**: 14 round-trip categories, cached-value oracle, volatile + `fullCalcOnLoad` skipped | `apps/gridcraft-cli/src/check/fidelity.rs:90-185` (13 categories + `package` in `round_trip`), `apps/gridcraft-cli/src/check/calc.rs`, `apps/gridcraft-cli/src/check/package.rs:148-171` | implemented |
| 11 | **35 control method names / 30 dispatch arms**, unchanged; any command id works as a method | `crates/ui-egui/src/control.rs` `handle()` match + `other if gridcraft_engine::find_command(other)` fallthrough | implemented |
| 12 | **18 UI-only command ids** (17 at v0.16.0; +`options.highlightActiveRow`) | the `(id, label, params)` array pushed with `"ui": true` in `crates/ui-egui/src/control.rs`; handlers in `crates/ui-egui/src/app/commands.rs` | implemented |
| 13 | **72 shortcut bindings** on command specs (71) + 5 macOS-only overrides; wider keymap table | fourth `cmd!` argument ≠ `None`; `shortcut_mac: Some(...)` ×5; `crates/ui-egui/src/keymap.rs` | implemented |
| 14 | **413 key-tip sequences** (367), including Excel 2003 menu paths | `crates/ui-egui/src/keytips/keytips.json` `sequences` (413) = generated `crates/ui-egui/src/keytips/keytip_table/generated.rs` entries (413); generated by `xtask/src/keytips.rs` | implemented |
| 15 | **19 languages, unchanged** | `crates/ui-egui/src/i18n.rs:59` (`ALL: [Self; 19]`), `crates/ui-egui/src/i18n/` (18 modules + English) | implemented |
| 16 | **26 ChartKinds, unchanged**; doughnut = one ring per series | `crates/model/src/features.rs:404-431`; `crates/chart/src/render/kinds.rs:265-268` | implemented |
| 17 | **513/523 functions by name, 504 working, unchanged** | `f!` names outside `#[cfg(test)]` modules (491) ∪ `SPECIAL_FUNCTIONS` (33) = 515 distinct, minus `USDOLLAR` and `ECMA.CEILING` (not on Microsoft's list) = 513 against Excel's 523; 7 CUBE + `WEBSERVICE` + `FILTERXML` are error stubs (9) → 504 working. 10 absent: GETPIVOTDATA, IMAGE, STOCKHISTORY, TRANSLATE, DETECTLANGUAGE, CALL, REGISTER.ID, RTD, COPILOT, PY | implemented metric |
| 18 | **Python cells exist but never run**; no `PY` function | `crates/engine/src/cmd/python.rs` (`python.set`, `python.output`, `#BLOCKED!` for new/changed code), `crates/xlsx/src/python_part.rs`, `ui.pythonMode` in `crates/ui-egui/src/app/commands.rs` | implemented (storage only) |
| 19 | **Equations exist**: LaTeX source, OMML round trip for a common subset | `crates/engine/src/cmd/equation.rs`, `crates/xlsx/src/omml.rs`, `crates/xlsx/src/drawing.rs:148-523` | implemented |
| 20 | **Analysis ToolPak: all 19 tools** | `crates/engine/src/cmd/analysis.rs:44-66` (`TOOLS`, 19 entries) | implemented |
| 21 | **No `.xls`/`.xlsb`/`.ods`/`.slk` write; encryption read-only; macros never run; slicers/timelines not saved; no Power Query/data model/From Web** | `crates/engine/src/io.rs:494-515` (save refusals), `docs/gaps.md` §3 (unmodelled parts), §7 (legacy/encryption), §8 (slicers/timelines), §12 (Power Query/data model), `crates/xlsx/src/read.rs` (encrypted open), catalog missing list (`data.fromWeb` absent) | not implemented (verified absent) |
| 22 | **Save semantics**: only `.xlsx`/`.json` clear the dirty flag | `crates/engine/src/cmd/file.rs:109-146` (`matches!(kind, Some(FileKind::Xlsx | FileKind::Json))`) | implemented |

## 2. Count ledger — v0.16.0 → v0.17.0 (method named)

| Surface | v0.16.0 (measured) | v0.17.0 (measured) | Method |
|---|---:|---:|---|
| Engine commands | 372 | **385** | `cmd!` first-literal ids reachable from `command_specs()` + explicit `CommandSpec` ids; diffed as sets. (The previous text's 363 is 372 minus the nine `macro.*` ids it listed separately.) |
| Catalog coverage | 277 / 292 | **281 / 296** (94.9%) | distinct `crates/engine/src/catalog.rs` ids ∩ registered ids; cross-checked against generated `docs/parity-checklist.md` |
| MCP tools | 22 | **22** (unchanged) | `tool(` definitions in `crates/mcp/src/tools.rs`; name sets identical |
| CLI subcommands | 11 | **11** (unchanged) | `main()` dispatch (`info convert eval cat run check commands functions mcp send version`) |
| Control method names / arms | 35 / 30 | **35 / 30** (unchanged) | `handle()` match arms in `crates/ui-egui/src/control.rs` (aliases share an arm) |
| UI-only command ids | 17 | **18** | entries in the `engine.commands` "ui" array |
| Shortcut bindings (command specs) | 71 | **72** | non-`None` 4th `cmd!` argument (+5 `shortcut_mac` overrides) |
| Key-tip sequences | 367 | **413** | `crates/ui-egui/src/keytips/keytips.json` `sequences` length = generated table entries |
| Interface languages | 19 | **19** (unchanged) | `Language::ALL` |
| Chart kinds | 26 | **26** (unchanged) | `ChartKind` variants |
| Worksheet functions | 513 / 523 by name, 504 working | **513 / 523, 504 working** (unchanged) | `f!` names outside test modules ∪ `SPECIAL_FUNCTIONS` − non-Excel names; stubs subtracted |
| MCP resources | 3 | **3** (unchanged) | resource URIs in `crates/mcp/src/server.rs` |
| `check` categories | 14 | **14** (unchanged) | `diff_workbooks` list + `package` |
| Backstage pages | 9 | **9** (unchanged) | `Page::ALL` in `crates/ui-egui/src/backstage.rs` |
| Built-in samples | 3 | **3** (unchanged) | `SAMPLES` in `crates/engine/src/sample.rs` |
| Shape kinds | 10 | **10** (unchanged) | `ShapeKind` variants in `crates/model/src/features.rs` |

Deliberately **not** counted as headline numbers: formats (enumerated from `FileKind` and the save/export paths), token/queue limits (quoted from constants), and the project's own estimate percentages (`docs/target-app-parity.md`: ~75% breadth, ~50% ready), which are estimates rather than measurements.

## 3. Uncertain / not verified

- **GUI behaviour is not exercised.** No window was launched; UI claims rest on the command/spec/UI code, not on screenshots. Anything phrased "the dialog does X" is code-derived.
- **Excel-repair-free output remains unproven by the project** (`docs/gaps.md` §1): `check` validates GridCraft against itself and the file's cached values, not against Excel.
- **Accessibility tree coverage** (grid cells and ribbon not exposed) is carried from the previous audit: AccessKit is enabled and a few widgets set node labels (`crates/ui-egui/src/tabs.rs:412`, `crates/ui-egui/src/ribbon/home.rs:635`), but no grid accessibility tree was found. Carried, not re-measured.
- **PDF glyph coverage** for CJK/Arabic/Devanagari/Thai is carried from the previous audit; the non-embedded CID font path is unchanged and no new shaping code was introduced this release.
- **`.xlsb`/`.ods`/`.xls` import depth** carried from the previous audit; the readers were not re-exercised (no corpus files in the checkout).
- Chart subtype coverage ("~26 of Excel's ~60") is the previous audit's ratio; only the enum count (26) was re-measured.
- **v0.14.2 and v0.15.0 are not in this checkout** (two release tags only), so historical delta paragraphs in `SKILL.md` are recorded history, not re-verified here; only the v0.16.0 → v0.17.0 diff was measured.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `README.md`: "covers 89% of standard ribbon commands" | 281/296 = 94.9% (generated checklist) |
| `docs/target-app-parity.md:58`: "321 command ids registered" | 385 registered (384 `cmd!` + 1 `CommandSpec`) |
| `docs/function-parity.md` headline: 513/523 by name, 504 working | agrees with code |
| `docs/function-parity.md` totals row: 505/496, "18 missing, 9 stubs" | 513 present / 10 absent / 9 stubs; the row also lists PERCENTOF and TRIMRANGE as missing although both are registered (`crates/functions/src/math/`, `crates/calc/src/eval/special.rs`) |
| `docs/gaps.md` §9: "59 command shortcuts" | 72 shortcut bindings on command specs (+5 macOS overrides) |
| `docs/control-protocol.md` auth section | now describes the token correctly (the previous skill's "does not yet describe the token" note is stale) |
| `docs/parity-checklist.md` | matches code (281/296; generated by `cargo xtask parity` from `crates/engine/src/catalog.rs`) |
| Release notes: "Form controls … XLSX round trip" | confirmed in model, engine, UI and `crates/xlsx/src/controls.rs` |
| Previous skill: "Opening a saved workbook without recalculating it is supported" | false — `file.open` uses `DocState::new`, which calls `Calc::recalc_all` (`crates/engine/src/lib.rs:295-299`); the non-evaluating `DocState::from_saved` is used only by `crates/engine/src/tests.rs:5861`. Claim removed |
| Previous skill: `.slk` opens as "(imported).xlsx" | false — the imported title covers only Ods/Xlsb/Xls (`crates/engine/src/cmd/file.rs:70-79`); a `.slk` keeps its name/path, so Save is refused (SYLK import-only) |

## 5. Verification (read-only, reproduced for this ledger)

All counts were produced with one script run against the checkout at each tag (`HEAD` and `v0.16.0`); it uses `git show <ref>:<path>` so nothing is checked out or modified. The script is the method of record for this round:

```python
# run from the checkout root: python3 counts.py HEAD   /   python3 counts.py v0.16.0
import json, re, subprocess, sys
REF = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
show = lambda p: subprocess.run(["git", "show", f"{REF}:{p}"], capture_output=True, text=True).stdout
files = lambda pre: [f for f in subprocess.run(["git", "ls-tree", "-r", "--name-only", REF, "--", pre],
                                               capture_output=True, text=True).stdout.split() if f.endswith(".rs")]

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
print("cli subcommands:", len(set(re.findall(r'Some\("(info|convert|eval|cat|run|check|commands|functions|mcp|send|version)"\)', main))) + 1)

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

Output at `HEAD`: `engine commands 385`, `catalog 281 / 296`, `mcp tools 22`, `cli subcommands 11`, `control names 35 arms 30`, `ui-only ids 18`, `shortcut bindings 72`, `keytips 413`, `languages 19`, `chart kinds 26`, `functions present 513 f! 491`. Output at `v0.16.0`: `372`, `277 / 292`, `22`, `11`, `35 / 30`, `17`, `71`, `367`, `19`, `26`, `513 / 491`.

Other spot checks (plain shell):

```sh
git -C <clone> rev-parse HEAD              # a6a6a49a0415087474251b08e887a3581fab9e14
git -C <clone> describe --tags             # v0.17.0
git -C <clone> diff --shortstat v0.16.0..HEAD   # 237 files changed, 15905 insertions(+), 1370 deletions(-)
git -C <clone> rev-list --count v0.16.0..HEAD   # 1: the checkout keeps one release commit per tag,
                                                # so the diff — not a commit count — is the delta evidence
"GridCraft.app/Contents/MacOS/GridCraft" --version   # GridCraft 0.17.0 (read-only; bundle in the system Applications folder)
```

## 6. Carried forward from the v0.16.0 ledger

- Control-channel limits (64 MiB line, 10,000 pointer events, 8 MiB synthetic input, 60 s UI wait, 10 s auth, 4 KiB auth line, 16 waiting), MCP error codes, the 30 s remote socket timeout and the `check` exit-code contract were re-read in code and are unchanged.
- Hard caps (512 MB XLSX part, 1 GB package, 2 GB file read, 100,001 HTML rows, 512 MiB CSV, 16M array cells) were re-read from their constants and are unchanged.
- Text shaping / PDF font limitations, accessibility coverage, large-workbook limits and the Excel-verification gap are carried from the previous round (see §3).
- Shared-code pins were refreshed: craft-libs `c5a1cbfb…` (craft-update, craft-window, craft-ui, craft-print, craft-i18n), `craft-web-host` `2e2312dd…`, egui 0.37 fork `6d518fc7…`. The previous ledger's single `92d392cf…` pin is superseded.
