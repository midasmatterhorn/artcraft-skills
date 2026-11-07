# WordCraft — evidence ledger (tag v0.16.0)

Audit basis: this checkout is tag **`v0.16.0`**, commit **`02a802cbafe45b5c8fecc00490c8f6b78c5ba251`**
("Release 0.16.0", 2026-11-06), shallow clone; the `v0.15.1` ref
(`08afab50b6a1ed19f9af55bb9f74d18f5e17bfa0`) is fetched for set diffs. Inspection date
**2026-11-07**. The installed bundle (`/Applications/WordCraft.app`, bundle id
`ai.storyteller.wordcraft`) is **0.16.0** and its binary prints `wordcraft 0.16.0 (02a802cb)`
(`--version` and `-h` run read-only; the GUI was never launched). `wordcraft-cli` is **not** inside
the bundle, and no CLI binary was available on this machine, so every count below is derived from
code; the live evidence is limited to the app binary's `--version`/`--help`.

## Round 2026-11-07 (refresh)

- Re-pinned v0.15.1 → **v0.16.0** = `02a802cbafe45b5c8fecc00490c8f6b78c5ba251`; installed
  `wordcraft 0.16.0 (02a802cb)`.
- Code diff `v0.15.1..HEAD`: **475 files, +50,297 / −4,226** (`git diff --shortstat`). The clone's
  history is squashed (one commit per tag), so commit *counts* from the GitHub compare page (258)
  are context, not a measurement.
- Counts re-measured at the new tag: commands **652 → 656** production ids (658 `CommandSpec::new`
  sites incl. 2 test fixtures added in `crates/engine/src/tests.rs`); catalog **505/520 → 506/521**;
  control methods **21 → 22**; `OPEN_EXTS` **21 → 23**, `SAVE_EXTS` **14 → 16**; MCP tools,
  CLI subcommands/flags, interface languages, built-in proofing languages, shortcut specs and
  dialog names unchanged.
- Paths: every repo-relative path in the published `SKILL.md` was re-resolved. One was dead —
  `crates/proof/src/lang.rs` (proofing moved to craft-libs `craft-proof` in the previous release;
  the local table is now `crates/ui-egui/src/ribbon/language.rs`, the pack names in
  `crates/ui-egui/src/language_packs.rs`). Everything else resolved at this tag.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 656 live command ids; 658 `CommandSpec::new(` sites incl. 2 test fixtures | `grep -rhoE 'CommandSpec::new\(\s*"[^"]+"' crates/ apps/ \| sort -u \| wc -l` = 658; minus the 2 in `crates/engine/src/tests.rs` (`test.boom`, `test.outer`) = 656 | implemented |
| 2 | 4 new commands this release | `crates/engine/src/cmd/font.rs:26` (`font.missing`), `crates/engine/src/cmd/format.rs:142` (`format.emphasisMark`), `crates/engine/src/cmd/canvas.rs:77` (`select.member`), `crates/engine/src/cmd/smart_art.rs:133` (`smartArt.itemColor`) | implemented |
| 3 | 17 MCP tools; the document tools take `doc` | `crates/mcp/src/tools.rs` `tool_definitions()` — 17 `tool(` calls, names read | implemented |
| 4 | 22 control methods, incl. new `file.closeDocument {id?, force?}` | `crates/ui-egui/src/control/handler.rs` dispatch; strings extracted and diffed against v0.15.1 (21) | implemented |
| 5 | 10 CLI subcommands / 21 flags (+help, version) | `apps/wordcraft-cli/src/main.rs:74` `SUBCOMMANDS`; option strings in `apps/wordcraft-cli/src/*.rs` | implemented |
| 6 | Catalog 506/521 (97.1%) | `CATALOG` in `crates/engine/src/catalog.rs` (521 `Tab\|Group\|Feature\|id` rows) against the registry id set; committed `docs/parity-checklist.md` still prints 505/520 | implemented metric |
| 7 | ODT full open/edit/save; `.ott`, `.fodt`; password-protected ODT | `crates/engine/src/io.rs:9-36` (OPEN_EXTS/SAVE_EXTS), `crates/engine/src/cmd/file.rs` (`can_encrypt` error names .odt/.ott), `crates/formats/src/odt/`, `docs/file-format-parity.md` (~90% self-estimate) | implemented (fidelity estimate is not measured) |
| 8 | `file.printPdf` gains `pagesPerSheet` (n-up, booklets) | `crates/engine/src/cmd/file.rs:131` param string; `crates/pdf/src/imposition.rs`; `crates/ui-egui/src/print_page.rs` | implemented |
| 9 | 28 interface languages; `craft-i18n.rev` moved | `crates/ui-egui/src/i18n.rs` `LANGUAGES: [LangInfo; 28]`; `craft-i18n.rev` = `1e515422afdda2f317af430c1f9d68a5f83935b4` (was `9d6d54d6…`) | implemented |
| 10 | 16 built-in proofing languages | `crates/ui-egui/src/ribbon/language.rs` `PROOFING_LANGUAGES: [(&str,&str); 16]` | implemented |
| 11 | 166 `.key()` shortcut specs | `grep -rho '\.key(' crates/engine/src/cmd/ \| wc -l` = 166 (same at v0.15.1) | implemented |
| 12 | 91 distinct dialog names | `pub fn name(&self)` match arms across `crates/ui-egui/src/dialogs.rs` + `crates/ui-egui/src/dialogs/dialogs_*.rs` (91 unique) | implemented |
| 13 | Pictures: PNG/JPEG/GIF/WebP/BMP/TIFF + WMF/EMF; not SVG/ICO/HEIC | `crates/engine/src/cmd/insert/objects.rs:105` `image_ext`; fallback message at `:132`; metafile sizing `wordcraft_render::metafile_size` | implemented |
| 14 | MHT/MHTML open, saving MHT remains missing | `crates/engine/src/io.rs:21-22`; `crates/formats/src/mht.rs`; `docs/gaps.md` gap 26 | implemented (read only) |
| 15 | `.doc` read-only; no PDF Reflow/Works/WordPerfect | `docs/gaps.md` gap 14, gap 23, gap 26; `crates/docbin` | not implemented (verified absent) |
| 16 | No VBA execution; charts/SmartArt from Word read-only; no AI | `docs/gaps.md` gaps 13, 22, 25; `.docm` keeps macros | not implemented (verified absent) |
| 17 | Control key file `<settings>/control-key.<instance>`, 0600, removed on exit | `crates/control-key/src/lib.rs:2,39-45` (path); `apps/wordcraft/src/control_server.rs:94` (0600), `:32` (removed) | implemented |
| 18 | Web build: `?webgl`, `?sample`, `?host=parent`, page host `data-host="page"` | `apps/wordcraft-web/src/{main.rs,host.rs}` | implemented (not exercised) |
| 19 | Fonts not installed are listed with their substitutes and `metricCompatible` | `crates/engine/src/cmd/font.rs:26,165-183` (`missing_fonts`) | implemented |
| 20 | `file.closeDocument` refuses unsaved work unless `force` | `crates/ui-egui/src/control/handler.rs` `close_refused`/`close_refused_for`; `crates/engine/src/cmd/file.rs:147` | implemented |

## 2. Count method and values (v0.15.1 → v0.16.0)

All counts are extracted from this checkout at both refs with the same commands; a set that is
unchanged is labelled "unchanged at v0.16.0" in `SKILL.md`.

| Surface | Method | v0.15.1 | v0.16.0 |
|---|---|---:|---:|
| Engine commands | `CommandSpec::new(` literal-id sites, minus test fixtures in `crates/engine/src/tests.rs` | 652 (0 fixtures) | **656** (658 sites − 2) |
| Catalog coverage | `CATALOG` rows in `crates/engine/src/catalog.rs`; live = id present in the registry set | 505 / 520 | **506 / 521** |
| MCP tools | `tool(` entries in `crates/mcp/src/tools.rs` | 17 | 17 (unchanged) |
| Control methods | distinct `"[a-z]+\.[a-zA-Z]+"` strings in `crates/ui-egui/src/control/handler.rs` | 21 | **22** |
| CLI subcommands | `SUBCOMMANDS` array | 10 | 10 (unchanged) |
| CLI flags | distinct long options in `apps/wordcraft-cli/src/*.rs`, excluding help/version and typo-suggestion strings in tests | 21 | 21 (unchanged) |
| Interface languages | `LANGUAGES` array length (declared and listed) | 28 | 28 (unchanged) |
| Built-in proofing | `PROOFING_LANGUAGES` array length | 16 | 16 (unchanged) |
| Shortcut specs | `grep -rho '\.key(' crates/engine/src/cmd/` | 166 | 166 (unchanged) |
| Open / save extensions | `OPEN_EXTS` / `SAVE_EXTS` string literals (open includes the compound `wcraft.json`) | 21 / 14 | **23 / 16** |
| Dialog names | `Dialog::name` arms, unique | 91 | 91 (unchanged) |

## 3. Uncertain / not verified

- The installed bundle's CLI does not exist (`wordcraft-cli` is not bundled), and no release-artifact
  CLI was on the machine, so no live `commands --json`, `parity` or conversion run was possible.
  The repo's CLI code and `--help`/`USAGE` text were read instead.
- ODT fidelity (~90%) and the readiness percentages (~60/55/63) are the repo's own estimates, not
  measurements by this audit; they are labelled as estimates in `SKILL.md`.
- The new-command list comes from id-set diffing; the four ids are named. Two further
  `CommandSpec::new` sites are test fixtures, not registry ids — a naive site count prints 658.
- GUI behaviour (modal dialogs, Read Mode colours, Arabic RTL, AccessKit guard, mini-toolbar
  preview) is release-wave information corroborated by changed files, not launched and observed.
- PDF/print field freshness (SEQ/STYLEREF/REF) from the release notes was **not** re-derived from
  code and is deliberately not claimed in `SKILL.md`.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `README.md` "422 commands"; `ROADMAP.md` "433 commands", "493 / 508" | 656 live command ids; catalog 506/521 |
| `docs/mcp.md` "over 270" commands for `list_commands` | 656 commands |
| `docs/parity-checklist.md` "505 of 520" | 521 rows, 506 live — one row stale (`Home › Font › Emphasis Mark`) |
| `docs/gaps.md` gap 7 "61 modal dialogs" | 91 distinct `Dialog::name` values |
| `docs/gaps.md` gap 24 "140 (macOS) / 158 (Linux/Windows)" shortcuts | 166 `.key()` specs in the registry |
| `docs/gaps.md` migration record "27 WordCraft languages" | 28 in `LANGUAGES` |
| Previous `SKILL.md` "Open / save extensions 19 / 14" | 21 / 14 at v0.15.1 (the old count was two entries short); 23 / 16 now |
| Previous `SKILL.md` "No MHT" | MHT/MHTML open at v0.15.1 already (`crates/engine/src/io.rs`); saving MHT remains missing |
| Previous `evidence.md` said the installed app matched and printed `wordcraft 0.14.0 (08afab58)` while the same round's `SKILL.md` said it was 0.12.0 (`3de6ff95`) | Neither held; this round the bundle is 0.16.0 and prints `wordcraft 0.16.0 (02a802cb)` |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # 02a802cbafe45b5c8fecc00490c8f6b78c5ba251
git -C <clone> diff --shortstat v0.15.1..HEAD                   # 475 files changed, 50297 insertions(+), 4226 deletions(-)
grep -rhoE 'CommandSpec::new\(\s*"[^"]+"' crates/ apps/ | sort -u | wc -l   # 658 sites
grep -c 'CommandSpec::new(' crates/engine/src/tests.rs          # 2 (test fixtures, not registry ids)
grep -cE '^\s+tool\($|^\s+tool\("' crates/mcp/src/tools.rs      # 17
grep -rhoE '"[a-z]+\.[a-zA-Z]+"' crates/ui-egui/src/control/handler.rs | sort -u | wc -l  # 22
grep -n 'const SUBCOMMANDS' apps/wordcraft-cli/src/main.rs       # 10 names
grep -rho '\.key(' crates/engine/src/cmd/ | wc -l               # 166
sed -n '9,36p' crates/engine/src/io.rs                          # OPEN_EXTS 23, SAVE_EXTS 16
grep -n 'LANGUAGES: \[LangInfo;' crates/ui-egui/src/i18n.rs     # 28
grep -n 'PROOFING_LANGUAGES' crates/ui-egui/src/ribbon/language.rs  # 16
grep -n 'MAX_LINE\|FIRST_REQUEST' apps/wordcraft/src/control_server.rs    # 1 MiB line, 30 s first request
grep -n '0o600' apps/wordcraft/src/control_server.rs                  # key file mode
head -1 craft-i18n.rev                                          # 1e515422…
"<bundle>/Contents/MacOS/WordCraft" --version                   # wordcraft 0.16.0 (02a802cb); bundle = the installed WordCraft.app
```

## 6. Prior ledger carried forward (v0.15.1 method, still the basis)

The previous round's claim table and threshold values (MCP/control/CLI byte-identical checks,
`craft-i18n.rev` movement, the AES/Standard encryption paths, the removal of `crates/proof` into
craft-libs) remain the reference for those areas; this round re-checked the sets above and did not
re-derive the GUI-only claims. The previous delta line "648 sites at both tags" was an extraction
that missed four command sites and was corrected to 648 → 652 in that round's own note; this round's
count starts from 652.
