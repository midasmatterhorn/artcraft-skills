# DesignCraft — evidence ledger (tag v0.18.0)

Audit basis: this checkout is tag **`v0.18.0`**, commit
**`58ac6d29b260e033f4291afc4318b507cfd90fd9`** ("Release 0.18.0", 2026-11-06). Inspection date
**2026-11-07**. Installed `/Applications/DesignCraft.app`: `CFBundleShortVersionString 0.18.0`,
`DesignCraftBuildCommit 58ac6d29…`, `CFBundleIdentifier ai.storyteller.designcraft`; the CLI inside
the bundle prints `designcraft-cli 0.18.0`. The GUI was never launched. The previous pin was
v0.17.0 = `e79d682e02dc66f14370958b193bfa46072b2f41`; that ref, present in the same checkout, is the
diff base for every set comparison below.

v0.17.0 → v0.18.0 delta (from `git diff`, not release notes; 214 files, +10830/−1032): +8 engine
command ids and +3 UI commands, none removed. New: **Export Layouts and Versions**
(`file.exportBatch` and its preset commands), alternate-layout duplicate/delete/options, duplicate
parent spread, `app.parentOptions`/`app.alternateLayoutOptions` dialogs. Behavioural: PDF and PPTX
exports warn about overset text (#1465); IDML round-trips hyperlinks (#1446); MCP schemas are closed
and all four hints are emitted; the native reader stops charging stored assets against the deflate
budget (#2166); the macOS app bundles the CLI. Typography: mojikumi consecutive punctuation, Danish
hyphenation, Esperanto as a text language. Formatted/binary formats unchanged (version 4).

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | **555** engine command ids (v0.17.0 = 547; +8, none removed) | id-set extraction of `cmd!(` (optional `query`/`noundo`) over `crates/engine/src` at both tags: 547 → 555 unique; live cross-check `designcraft-cli commands` = 555 entries | implemented |
| 2 | New ids: `file.exportBatch`, `file.exportPresets`, `file.saveExportPreset`, `file.deleteExportPreset`, `layout.alternate.duplicate`/`.delete`/`.options`, `layout.parents.duplicate` | `crates/engine/src/cmd/export_batch.rs:171-182`; `crates/engine/src/cmd/liquid.rs:208-226`; `crates/engine/src/cmd/layout/registry.rs:224` | implemented |
| 3 | **190** UI command rows (v0.17.0 = 187; +3) | `crates/ui-egui/src/menus/ui_commands.rs:14` `UI_COMMANDS`, row count at both tags; the older 176 figure did not reproduce at its own tag | implemented |
| 4 | Export Layouts and Versions: several alternate layouts × up to 24 versions, PDF/PNG/JPEG, folder per version, `{document}/{layout}/{version}/{date}`, ≤ 5 000 files, 100 saved presets | `crates/engine/src/cmd/export_batch.rs` module doc and `cmd!` spec; `MAX_FILES`, `MAX_VERSIONS`, `MAX_PRESETS` consts | implemented |
| 5 | 26 MCP tools, set unchanged; every schema closed (`additionalProperties: false`) and all four hints emitted | `crates/mcp/src/tools.rs` `tool_definitions`; `obj()` adds `additionalProperties: false`; `NON_DESTRUCTIVE`/`IDEMPOTENT` sets; `crates/mcp/src/server.rs` `check_arguments`; `docs/mcp.md` | implemented |
| 6 | 27 control methods, set unchanged | arm strings in `crates/ui-egui/src/control.rs`, identical sets at both tags (incl. `ui.docking`, `ui.dialog.open`) | implemented |
| 7 | 11 CLI subcommands, `thumbnail` new | `apps/designcraft-cli/src/main.rs` `USAGE` and dispatch arms (`thumbnail` at `Main`), installed `--help` lists the same 11 | implemented |
| 8 | macOS CLI now bundled inside the app | `docs/mcp.md` "Where the CLI is" table and macOS example; `ROADMAP.md` changelog line; `DesignCraft.app/Contents/MacOS/designcraft-cli` present, prints `0.18.0` | implemented |
| 9 | `validate-pdf [--standard x4|x1a]` prints `{path, standard, valid, issues, warnings}`, defaults to the file's `GTS_PDFXVersion`, PDF/X-1a checks included | `apps/designcraft-cli/src/main.rs` `validate_pdf`; `crates/pdf/src/pdfx1a.rs` | implemented |
| 10 | `thumbnail FILE.designcraft OUT.png [SIZE]` writes the saved preview (no render) and refuses an output naming the input | `apps/designcraft-cli/src/main.rs` `thumbnail`, `names_the_same_file`; `crates/format` `read_preview` | implemented |
| 11 | PDF and PPTX exports warn about text the pages had no room for | `crates/engine/src/cmd/export/pdf.rs:110`, `crates/engine/src/cmd/export/formats.rs:114` → `crates/engine/src/cmd/preflight.rs:186` `overset_warnings` | implemented |
| 12 | IDML export writes a document's hyperlinks; import keeps a page-item/text-run hyperlink; a hyperlink can target a text anchor | `crates/idml/src/export.rs` (`Hyperlink`, `HyperlinkPageDestination`, `HyperlinkPageItemSource`); `crates/idml/src/import.rs`; #1446 | implemented |
| 13 | Format version 4 unchanged; stored assets no longer charged against the deflate budget; JSON 256 MiB, 100 000 entries | `crates/format/src/lib.rs:29` `VERSION: u32 = 4`; `Limits`, `read_entry` (stored branch, #2166) | implemented |
| 14 | Hyphenation bundled for English, Danish, Dutch, French, German (2006), Greek, Italian, Norwegian, Portuguese, Spanish; spelling English only | `crates/compose/src/hyphen.rs` module doc and `Lang::for_language`; `docs/gaps.md` §13, `docs/localization-parity.md` | implemented |
| 15 | Esperanto is a text language (`eo`) with no hyphenation | `crates/doc/src/attrs/language.rs:91`; `docs/localization-parity.md` (#1201) | implemented / partial |
| 16 | PDF/X-1a:2003 export via the craft-prepress flattener; PDF/X-4 checks | `crates/pdf/src/lib.rs`; `crates/pdf/src/export.rs` `craft_prepress::InkSet`; `crates/pdf/src/pdfx.rs`, `pdfx/fonts.rs`; `"x1a"` accepted in `file.exportPdf` tests | implemented |
| 17 | Placed-PDF layer choices are applied on export; IDML graphic-layer options retained, not rendered | `crates/engine/src/cmd/pdflayers.rs`; `crates/pdf/src/optional_content.rs`; `docs/graphic-layer-options.md` | implemented / partial |
| 18 | No ExtendScript/UXP, no plug-in model, no media playback, no `.joboptions`, no PDF font repair | `docs/gaps.md` §§9, 10, 17, 22, 23, 28 | not implemented (verified absent) |

## 2. Automation-surface counts: v0.17.0 → v0.18.0

| Surface | v0.17.0 | v0.18.0 (measured) | Change |
|---|---:|---:|---|
| Engine command ids | 547 | **555** | +8 (none removed) |
| UI `UI_COMMANDS` rows | 187 | **190** | +3 (none removed) |
| MCP tools | 26 | **26** | unchanged |
| Control methods | 27 | **27** | unchanged |
| CLI subcommands | 10 | **11** | +`thumbnail` |
| Format version | 4 | **4** | unchanged |
| Hyphenation languages | 9 | **10** | +Danish |

The published v0.17.0 round quoted 542 engine / 176 UI / 10 CLI subcommands. Re-measured at v0.17.0
with the methods above, the engine set is 547 and the UI table is 187 rows; neither published figure
reproduced at its own tag. Both are corrected here rather than carried.

## 3. Uncertain / not verified

- Export Layouts and Versions was read from its command spec and implementation, not run on a
  document; its output folders, name template and preset round-trip are unexercised.
- GUI behaviour not launched; registry + code + docs + packaging are the evidence. Whether a given
  dialog is reachable over `ui.dialog.open` remains per-dialog unverified.
- INDD/INDT and IDML fidelity on real files remains unmeasured by the project (`docs/gaps.md` §§2-4);
  IDML hyperlink round-trip is covered by the project's own tests, not by a real-file sample here.
- The alternate-layout model is documented from the command specs (`layout.createAlternate`,
  `layout.alternate.*`); how faithfully objects follow the liquid rules on complex pages was not
  measured.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `docs/target-app-parity.md` "~200 commands" / "446 engine + 99 UI" | 555 engine ids + 190 UI rows measured here |
| `docs/agents.md` / CLI `SCRIPT_HELP` "most commands ignore unknown parameters" | CLI, MCP and control channel reject unknown params (`crates/engine/src/cmd/params.rs`, `crates/mcp/src/server.rs`) |
| `apps/designcraft-cli/src/main.rs` module doc: `perf [--pages N] [--frames N] [--chars N] [--images N] …` | the `USAGE` const and the parser take `--pages`, `--runs`, `--strict` only |
| `docs/gaps.md` §13 lists hyphenation without Danish in the older text | Danish is bundled (`crates/compose/src/hyphen.rs`); the §13 edit at v0.18.0 adds it |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # 58ac6d29b260e033f4291afc4318b507cfd90fd9
git -C <clone> diff --shortstat v0.17.0..HEAD                   # 214 files, +10830/-1032
git grep -o 'cmd!' v0.17.0 -- crates/engine/src | wc -l         # 547
git grep -o 'cmd!' HEAD -- crates/engine/src | wc -l            # 555
<app>/Contents/MacOS/designcraft-cli --version                  # designcraft-cli 0.18.0
<app>/Contents/MacOS/designcraft-cli commands | python3 -c 'import json,sys;print(len(json.load(sys.stdin)))'  # 555
awk '/pub const UI_COMMANDS/,/^\];/' crates/ui-egui/src/menus/ui_commands.rs | grep -cE '^\s*\('   # 190 rows
sed -n '29p' crates/format/src/lib.rs                           # VERSION: u32 = 4
plutil -p <app>/Contents/Info.plist | grep -E 'Version|BuildCommit'
```

## Round 2026-11-04 (historical note, superseded)

Pinned to `v0.17.0` = `e79d682…` (installed `designcraft 0.17.0`). It reported +1 command id
(`layout.parentPageSize`) and 542 engine / 176 UI / 26 MCP / 10 CLI; the registry figures from that
round are superseded by the re-measurement above.

## Round 2026-11-07 (this refresh)

- Re-pinned to `v0.18.0` = `58ac6d2…`; installed `designcraft 0.18.0`, bundled CLI `0.18.0`.
- Re-measured: engine ids 547 → 555, UI rows 187 → 190, CLI subcommands 10 → 11, hyphenation
  languages 9 → 10. Explicitly unchanged: **26 MCP tools**, **27 control methods**, **format
  version 4**.
- Corrected: the CLI-is-not-in-the-app claim (it is), the 542/176 counts, the "old" hyphenation
  language list, `validate-pdf`'s report shape, the native-format read limits, and the
  verification-protocol pin string.
- Paths: every repo-relative path in `SKILL.md` and `references/agent-surfaces.md` was expanded
  against this checkout and exists; no cited path had to be dropped.
