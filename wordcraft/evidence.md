# WordCraft — evidence ledger (tag v0.18.1)

Audit basis: this checkout is tag **`v0.18.1`**, commit **`079f478bd85df7bcc567e3bafa7d7219096f9c3c`**
("Merge tested main for v0.18.1", 2026-11-11), shallow clone. Inspection date **2026-11-12**.
The installed bundle (bundle id `ai.storyteller.wordcraft`, `CFBundleShortVersionString` 0.18.1)
prints **`wordcraft 0.18.1 (079f478b)`** from `--version`;
`--help` was run read-only too, and the GUI was never launched. `wordcraft-cli` is **not** inside
the bundle and no CLI artifact was available on this machine, so every count below is derived from
code; live evidence is limited to the app binary's `--version`/`--help`.

## Round 2026-11-12 (refresh)

- Re-pinned v0.16.0 (`02a802cbafe45b5c8fecc00490c8f6b78c5ba251`) -> **v0.18.1**
  (`079f478bd85df7bcc567e3bafa7d7219096f9c3c`); installed `wordcraft 0.18.1 (079f478b)`.
- Code diff `v0.16.0..HEAD`: **358 files, +23,251 / −1,410** (`git diff --shortstat`). The checkout
  carries only the `v0.16.0` and `v0.18.1` tag objects, so this is the cumulative diff over the two
  intermediate releases; commit-count comparisons are not used as a measurement.
- Counts re-measured at the new tag: commands **656 -> 671**; catalog **506/521 -> 509/521**;
  MCP tools **17 -> 18**; control methods **22** (unchanged); CLI flags **21 -> 22**; CLI
  subcommands **10** (unchanged); open/save extensions **23/16** (unchanged); interface languages
  **28** and proofing **16** (unchanged); shortcut `.key()` sites **166 -> 167**; dialog names
  **91 -> 92**.
- Paths: every repo-relative path cited in the published `SKILL.md` was re-resolved against this
  checkout. All resolved; no citation had moved or been deleted this round.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 671 live command ids (673 `CommandSpec::new` sites minus 2 test fixtures) | `grep -rhoE 'CommandSpec::new\(\s*"[^"]+"' crates/ apps/ \| sort -u \| wc -l` = 673; `crates/engine/src/tests.rs` holds `test.boom`, `test.outer` | implemented |
| 2 | 15 new commands; none removed | id-set diff `v0.16.0..HEAD`: nine `para.*` tools (`crates/engine/src/cmd/para.rs`, `crates/engine/src/cmd/para/tools.rs`), `text.deleteSentenceBack` (`crates/engine/src/cmd/text/delete.rs`), `view.paperColor` / `view.arrangeAll` / `view.sideBySide` / `view.syncScroll` (`crates/engine/src/cmd/view.rs`), `file.strictReport` (`crates/engine/src/cmd/file.rs`) | implemented |
| 3 | Strict export: `strict` on save/export, exit 3 from the CLI, JSON report | `crates/engine/src/strict.rs`, `crates/layout/src/strict.rs`, `crates/layout/src/missing.rs`, `crates/doc/src/missing.rs`, `crates/engine/src/cmd/file.rs:122,375,462`, `apps/wordcraft-cli/src/main.rs` (`Failure::Strict`, `--strict`), `apps/wordcraft-cli/tests/it/strict.rs` | implemented |
| 4 | 18 MCP tools, `insert_table` new | `crates/mcp/src/tools.rs` (`tool_definitions()`: 18 `tool(` entries; `insert_table` dispatches `insert.spreadsheet`) | implemented |
| 5 | `insert_table` limits and one-call fill | `crates/mcp/src/tools.rs:255`; `crates/engine/src/cmd/tools/actions.rs:345–365` (1–1000 rows, 1–63 cells, rectangular, explicit `null` `values` is a parameter error); `crates/engine/src/cmd/tools/specs.rs:216` | implemented |
| 6 | 22 control methods; queue timeout cancels, started work reports unknown | `crates/ui-egui/src/control/handler.rs` (22 distinct method strings), `apps/wordcraft/src/control_server.rs` (`REPLY_WAIT` 60 s, `waiter.cancel()`, `MAX_UNAUTHENTICATED` 64) | implemented |
| 7 | `ui.inspect` carries `windows`; window commands and `view.switchWindows {window}` | `crates/ui-egui/src/control/handler.rs:20–24`, `crates/engine/src/cmd/view.rs` (`Windows`, `view.arrangeAll`, `view.sideBySide`, `view.syncScroll`), `crates/ui-egui/src/windows/arrange.rs` | implemented (desktop only) |
| 8 | 10 CLI subcommands / 22 flags (+help, version) | `apps/wordcraft-cli/src/main.rs:81` `SUBCOMMANDS`; `OptionSpec` tables and `apps/wordcraft-cli/src/automation_args.rs`; `apps/wordcraft-cli/src/main.rs:372` `Failure::Strict` = exit 3 | implemented |
| 9 | `--strict` needs a `.pdf` or `.png` output and checks only what the output draws | `apps/wordcraft-cli/src/main.rs:492–513`, `crates/engine/src/cmd/file.rs:462`, `docs/file-format-parity.md` (2026-11-08 status line) | implemented |
| 10 | Catalog 509/521 (97.7%); 12 missing rows / 11 distinct features | `CATALOG` in `crates/engine/src/catalog.rs` (521 rows) against the registry set; missing ids: `addins.get`, `draw.inkToMath`, `insert.inkEquation` (twice), `insert.model3d`, `insert.onlinePicture`, `insert.screenshot`, `insert.video`, `review.blockAuthors`, `review.translate`, `tools.dictate`, `view.readLayout`; committed `docs/parity-checklist.md` prints 508/520 | implemented metric |
| 11 | `file.newFromTemplate` gains `data`, `password`, `replaceBlank`; a platform-opened template is never written over | `crates/engine/src/cmd/tools/specs.rs:125–129`, `crates/engine/src/cmd/file.rs:283–330`, `crates/ui-egui/src/documents.rs:135–155` | implemented |
| 12 | MCP bridge never replays a mutation with an unknown outcome | `crates/mcp/src/backend.rs` (`Failure::{NotSent,Unknown}`, `is_read_only`), `docs/mcp.md` "Delivery failures" | implemented |
| 13 | RTF reads and writes footnotes, endnotes and comments; RTF sections written | `crates/formats/src/rtf/reader.rs:174–200`, `crates/formats/src/rtf/export.rs:75–79,194–216,407–425`; `docs/gaps.md` gap 19 | implemented |
| 14 | ODT gap-19 batch: frames with several picture formats, heading text of another size, column shares, per-script font size, styles turning things off, custom styles with an outline level, picture size, frame page, default font, language | `crates/formats/src/odt/{import,styles,frames,package,kept}.rs`, `crates/formats/src/odt/tests_more/`; `docs/file-format-parity.md` `.odt` row (~90% self-estimate) | implemented (fidelity estimate is not measured) |
| 15 | DOCX Strict Open XML shapes, text boxes, groups and canvases open | `crates/docx/tests/it/strict_drawings.rs`; `docs/file-format-parity.md` Strict row | implemented (read) |
| 16 | 92 distinct dialog names | `Dialog::name` match arms in `crates/ui-egui/src/dialogs.rs` and `crates/ui-egui/src/dialogs/dialogs_{review,layout,refs,insert}.rs` (92 unique; `dateTime` new) | implemented |
| 17 | 167 `.key()` sites, 164 command bindings | `grep -rho '\.key(' crates/engine/src/cmd/ \| wc -l` = 167; three are helper calls in `crates/engine/src/cmd/tools/compare.rs`; new binding `text.deleteSentenceBack` in `crates/engine/src/cmd/text.rs:39` (implementation in `crates/engine/src/cmd/text/delete.rs`) | implemented metric |
| 18 | 28 interface languages, 16 built-in proofing languages, `craft-i18n.rev` unmoved | `crates/ui-egui/src/i18n.rs:73` (`[LangInfo; 28]`), `crates/ui-egui/src/ribbon/language.rs:4` (`[(&str,&str); 16]`), `craft-i18n.rev` = `1e515422afdda2f317af430c1f9d68a5f83935b4` | implemented |
| 19 | Web build gains `window.wordcraft` page API, no TCP control channel | `apps/wordcraft-web/src/api.rs` (`craft-web-api` over `ControlRequest`), `apps/wordcraft-web/src/main.rs:24` | implemented (not exercised) |
| 20 | Pictures PNG/JPEG/GIF/WebP/BMP/TIFF + WMF/EMF; not SVG/ICO/HEIC | `crates/engine/src/cmd/insert/objects.rs:105–134` `image_ext` and the refusal message; `crates/geom/src/picture.rs` (TIFF compression gate) | implemented |
| 21 | Strict report reasons and caps | `crates/doc/src/missing.rs` (`MAX_MISSING_PICTURES` 256, reason codes), `crates/layout/src/missing.rs` (`MAX_MISSING_GLYPHS` 256), `crates/engine/src/strict.rs` (`SCHEMA` 1) | implemented |
| 22 | Personal templates remain `.dotx`/`.dotm`, 500 entries, 64 categories, network folders refused | `crates/engine/src/cmd/user_templates.rs:19–35,39–42` | implemented |

## 2. Count method and values (v0.16.0 → v0.18.1)

All counts are extracted from this checkout at both refs with the same commands; a set that is
unchanged is labelled "unchanged at v0.18.1" in `SKILL.md`.

| Surface | Method | v0.16.0 | v0.18.1 |
|---|---|---:|---:|
| Engine commands | `CommandSpec::new(` literal-id sites, minus test fixtures in `crates/engine/src/tests.rs` | 656 (658 − 2) | **671** (673 − 2) |
| Catalog coverage | `CATALOG` rows in `crates/engine/src/catalog.rs`; live = id present in the registry set | 506 / 521 | **509 / 521 (97.7%)** |
| MCP tools | `tool(` entries in `crates/mcp/src/tools.rs` | 17 | **18** |
| Control methods | distinct `"<ns>.<name>"` strings in `crates/ui-egui/src/control/handler.rs` | 22 | 22 (unchanged) |
| CLI subcommands | `SUBCOMMANDS` array | 10 | 10 (unchanged) |
| CLI flags | `OptionSpec` names plus `automation_args.rs`, excluding help/version and typo strings in tests | 21 | **22** (`--strict`) |
| Interface languages | `LANGUAGES: [LangInfo; N]` | 28 | 28 (unchanged) |
| Built-in proofing | `PROOFING_LANGUAGES` array length | 16 | 16 (unchanged) |
| Shortcut sites | `grep -rho '\.key(' crates/engine/src/cmd/` | 166 | **167** (164 bindings) |
| Open / save extensions | `OPEN_EXTS` / `SAVE_EXTS` literals (`wcraft.json` counted once) | 23 / 16 | 23 / 16 (unchanged) |
| Dialog names | `Dialog::name` arms, unique | 91 | **92** |
| Missing catalog rows | catalog rows whose id is absent from the registry | 15 rows / 14 ids | **12 rows / 11 ids** |

## 3. Uncertain / not verified

- The CLI is absent from the bundle and no release-artifact CLI was on the machine, so no live
  `commands --json`, `parity`, `convert --strict` or conversion run was possible. The strict
  behaviour is read from code and the README example, not observed.
- The strict report's practical value depends on installed fonts and on the picture formats the
  build decodes; that dependency is stated in `README.md` and `crates/engine/src/strict.rs`, and is
  labelled as a host dependency in `SKILL.md`.
- ODT (~90%), RTF (~50%), HTML (~65%), MHT (~60%), DOCX (~65%), Word 2003 XML (~55%) and Flat OPC
  (~65%) are the repo's own estimates in `docs/file-format-parity.md`, not measurements by this
  audit.
- GUI-only changes (window tiling, Side by Side, paper colours, the Date and Time dialog, text
  hinting, the Arabic mirrored dialogs) were not launched or observed; they are cited to code.
- The delta is cumulative because the shallow clone has only the two tag objects; per-release
  (v0.17.0, v0.18.0) attribution is not available from this checkout.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `README.md` "422 commands"; `ROADMAP.md` "433 commands", "493 / 508" | 671 live command ids; catalog 509/521 |
| `docs/mcp.md` "over 270" commands for `list_commands` | 671 commands |
| `docs/parity-checklist.md` "508 of 520" | 521 rows, 509 live — one row/live id behind |
| `docs/gaps.md` gap 7 "61 modal dialogs" | 92 distinct `Dialog::name` values |
| `docs/gaps.md` gap 24 "140 (macOS) / 158 (Linux/Windows)" shortcuts | 167 `.key()` sites / 164 bindings; `docs/ui-parity.md` uses yet another measure (152 commands, 172 combinations) |
| Previous `SKILL.md` HTML "~60%" | the `.htm/.html` row of `docs/file-format-parity.md` now estimates ~65%; a fresher self-estimate, not a measurement |
| Previous `SKILL.md` "catalog features with no command: 15 rows, 14 distinct" | 12 rows / 11 distinct at this tag (three window commands landed) |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # 079f478bd85df7bcc567e3bafa7d7219096f9c3c
git -C <clone> diff --shortstat v0.16.0..HEAD                   # 358 files changed, 23251 insertions(+), 1410 deletions(-)
grep -rhoE 'CommandSpec::new\(\s*"[^"]+"' crates/ apps/ | sort -u | wc -l   # 673 sites
grep -c 'CommandSpec::new(' crates/engine/src/tests.rs          # 2 test fixtures
grep -cE '^\s+tool\(' crates/mcp/src/tools.rs                   # 18
grep -rhoE '"[a-z]+\.[a-zA-Z]+"' crates/ui-egui/src/control/handler.rs | sort -u | wc -l  # 22
grep -n 'const SUBCOMMANDS' apps/wordcraft-cli/src/main.rs       # 10 names
grep -rho '\.key(' crates/engine/src/cmd/ | wc -l               # 167
sed -n '9,36p' crates/engine/src/io.rs                          # OPEN_EXTS 23, SAVE_EXTS 16
grep -n 'LANGUAGES: \[LangInfo;' crates/ui-egui/src/i18n.rs     # 28
grep -n 'PROOFING_LANGUAGES' crates/ui-egui/src/ribbon/language.rs  # 16
grep -n 'REPLY_WAIT\|MAX_UNAUTHENTICATED' apps/wordcraft/src/control_server.rs  # 60 s, 64
grep -n '0o600' apps/wordcraft/src/control_server.rs            # key file mode
head -1 craft-i18n.rev                                          # 1e515422…
"<bundle>/Contents/MacOS/WordCraft" --version                   # wordcraft 0.18.1 (079f478b)
```

## 6. Prior ledger carried forward (method and older claims)

The previous round's claim table (v0.15.1 -> v0.16.0) remains the reference for claims this round
did not re-derive: AES/Standard encryption paths, the ODT password path, control-key details,
the `.doc` reader, Zotero's loopback rule, recovery cadence and the printing options. This round
re-checked their paths and the set counts above; it did not re-run GUI behaviour. The earlier
command-count correction (652 at v0.15.1) and the older interface-language, proofing and shortcut
corrections remain as recorded in the previous ledger.
