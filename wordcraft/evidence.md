# WordCraft — evidence ledger (tag v0.12.0)

Audit basis: this checkout is tag **`v0.12.0`**, commit **`3de6ff95af86c19d67030cd96dba15cd6a45a25e`**
("Release 0.12.0", 2026-10-28; shallow clone plus a fetched `v0.11.0` ref for set diffs). Inspection
date **2026-10-29**. Installed `/Applications/WordCraft.app` prints `wordcraft 0.12.0 (3de6ff95)`;
the GUI was never launched.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 648 `CommandSpec::new(` sites (was 643) | `grep -rho 'CommandSpec::new(' crates/ apps/ \| wc -l` = 648; v0.11.0 = 643 (baseline) | implemented |
| 2 | Multi-document: one native window per document; File ▸ New adds; View ▸ New Window; per-doc recovery | `crates/ui-egui/src/windows.rs:1` ("One native window per open document"); PRs #4388–#4391 | implemented |
| 3 | Doc addressing: every MCP tool takes `"doc"`; control `engine.execute`/`document.inspect`/`ui.render` take `doc`; `file.closeDocument {doc}` | `crates/mcp/src/tools.rs:54,216`; `crates/ui-egui/src/control.rs:16`; new id `file.closeDocument` | implemented |
| 4 | 17 MCP tools (+`list_documents`) | `crates/mcp/src/tools.rs` — 17 `tool(` calls; name list read | implemented |
| 5 | 21 control methods (+`file.close`, `file.exportPng`) + command-id fallthrough | `crates/ui-egui/src/control.rs` header + `control/handler.rs` method strings (21 counted) | implemented |
| 6 | Standard (AES) encryption decrypt for .docx; agile unchanged | `crates/docx/src/crypt.rs:12` (agile), `:54,:95,:150` (`decrypt_standard`, MS-OFFCRYPTO §2.3.4.5–§2.3.4.9); PR #2628 | implemented |
| 7 | Catalog 505/520 (97.1%) | `docs/parity-checklist.md:5` | implemented metric |
| 8 | 167 `.key()` shortcut specs | `grep -rho '\.key(' crates/engine/src/cmd/ \| wc -l` = 167 (was 164) | implemented |
| 9 | Regex Replace expands capture groups; AutoFormat double-space period; style-size scale; style sets keep own styles | PRs #4201, #3318, #2620, #4013 | implemented |
| 10 | Arabic letter numbering (arabicAlpha/arabicAbjad) drawn; Arabic-Indic digits kept | PRs #4218, #3329 | implemented |
| 11 | Custom Document Properties dialog | PR #2997; `crates/ui-egui/src/dialogs*.rs` | implemented |
| 12 | Task panes on craft_ui::panes; Styles docks/floats | PRs #3109, #4386 | implemented |
| 13 | Zotero bridge loopback-only, same-user check on Linux | PR #3876; `crates/zotero/` | implemented |
| 14 | Hardening wave + PDF export ~24% faster | PRs #3866–#3877, #4381–#4384, #4602 | implemented |
| 15 | Startup update prompt + self-update; per-user Windows installer; egui 0.37 | PRs #4298, #2560/#4492, #4241; `Cargo.toml` craft pins | implemented |
| 16 | Control key file scheme unchanged (`control-key.<instance>`, 0600, removed on exit) | `crates/control-key/src/lib.rs:38` | implemented |
| 17 | No VBA execution; .doc read-only; charts/SmartArt from Word read-only; no AI | `docs/gaps.md`; `crates/docbin/src/lib.rs:1-8` | not implemented (verified absent) |

## 2. Automation-surface counts: v0.11.0 → v0.12.0

| Surface | v0.11.0 | v0.12.0 (measured) | Change |
|---|---:|---:|---|
| Engine commands | 643 | **648** | +5 (named: `file.closeDocument`, `view.stylesPaneDock`, `view.switchWindows`; remaining additions in other namespaces) |
| Catalog coverage | 504/520 | **505/520** | +1 row |
| MCP tools | 16 | **17** | +`list_documents`; all tools take `doc` |
| Control methods | 19 | **21** | +`file.close`, `file.exportPng`; `doc` on three methods |
| CLI subcommands / flags | 10 / 21 | **10 / 21** | unchanged |
| Shortcut-bearing specs | 164 | **167** | +3 |
| Proofing variants | 15 | **15** | unchanged |
| Languages | 27 | **27** | unchanged; `craft-i18n.rev` advanced |
| Open/save extensions | 19/14 | **19/14** | unchanged |

## 3. Uncertain / not verified

- The full five-command addition list: three named via id-string diff; the other two live in
  namespaces outside the diff's prefix filter or are const-built — `wordcraft-cli commands --json`
  is authoritative.
- Dialog-name total not re-derived this pass (baseline method counted `Dialog::name` arms across
  five files); the Custom Document Properties dialog is new this line.
- GUI behaviour not launched; registry + docs + packaging are the evidence.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| README "422 commands"; ROADMAP 493/508/433; `docs/mcp.md` "over 270" | 648 `CommandSpec::new(` sites; 17 MCP tools |
| `docs/gaps.md`/`docs/ui-parity.md` "60/62 modal dialogs" | 89 distinct `Dialog::name` values at v0.11.0 (code wins) |
| Baseline "one document per window, no tabs" | **resolved this release** — several documents, one window each, `doc` addressing |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # 3de6ff95af86c19d67030cd96dba15cd6a45a25e
grep -rho 'CommandSpec::new(' crates/ apps/ | wc -l             # 648
sed -n '5p' docs/parity-checklist.md                            # 505 of 520
grep -cE '^\s+tool\($|^\s+tool\("' crates/mcp/src/tools.rs      # 17
grep -rhoE '"[a-z]+\.[a-zA-Z]+"' crates/ui-egui/src/control/handler.rs | sort -u | wc -l  # 21
grep -n 'decrypt_standard' crates/docx/src/crypt.rs             # Standard encryption
grep -rho '\.key(' crates/engine/src/cmd/ | wc -l               # 167
head -1 craft-i18n.rev                                          # 9205108c…
```
