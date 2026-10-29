# PdfCraft — evidence ledger (tag v0.15.0)

Audit basis: this checkout is tag **`v0.15.0`**, commit **`75360d1d7db06fed974f48c914d4c04132757187`**
(shallow clone plus a fetched `v0.14.0` ref for set diffs). Inspection date **2026-10-29**. Installed
`/Applications/PdfCraft.app` prints `pdfcraft 0.15.0`; the GUI was never launched.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 179 automation tools, set unchanged | `crates/automation/src/tools.rs`: 153 inline `t("name"` + 26 `^\s+t\($` multi-line entries = 179; name set unchanged from v0.14.0 | implemented |
| 2 | 205 registry commands, set unchanged | `crates/engine/src/commands.rs:165` `COMMANDS` — 205 `c(` entries; id diff vs `v0.14.0` = 0/0 | implemented |
| 3 | 17 UI control methods unchanged | `crates/ui-egui/src/control/requests.rs` method strings (17) | implemented |
| 4 | 35 interface languages (+Persian) | `crates/ui-egui/src/i18n/` — 34 `.tsv` catalogs incl. `fa.tsv` + English; PR #4558 | implemented |
| 5 | CLI 14 documented subcommands + internal `check-one` | subcommand name strings in `apps/pdfcraft-cli/src/main.rs` (15) | implemented |
| 6 | Page tools menu in the Pages panel | `crates/ui-egui/src/panels/pages.rs`; PR #4583 | implemented |
| 7 | Page-image export on worker threads (~80% less wall time) | `crates/render/src/raster/work_queue.rs`; PR #5026 | implemented |
| 8 | XFA: static form with thousands of filled fields opens in seconds; signature fields named by SOM path; round checkbox highlight | PRs #4638, #4507, #4512; `crates/xfa/src/{lib,layout}.rs` | implemented |
| 9 | Redaction F-008/F-011: vector paths behind clipping not retained; unused Type 3 glyph programs/fonts unlinked | PRs #4577, #4579; `crates/redact/src/` | implemented |
| 10 | Word export keeps an italic run in its paragraph; NeedAppearances `/MK` captions; opening-destination page in Document Properties | PRs #4411, #4454, #4574 | implemented |
| 11 | XFDF empty field clears; FDF pop-up on page; DeviceCMYK luminosity mask per ISO 10.4.2; FormCalc overflow/decode fixes | PRs #4483, #4493, #4423, #4508, #4592, #4586 | implemented |
| 12 | Native macOS menus from craft-menu; craft-ui task panes + ComboBox; startup update prompt; Windows per-user | PRs #4752, #4606, #4988, #4654, #4892 | implemented |
| 13 | OCR models fetched from ONNX URLs | PR #5039 | implemented (packaging) |
| 14 | Craft-libs split pins | `Cargo.toml`: `e11f9d9a…`, `6d518fc7…`, `a517b384…` | implemented |
| 15 | No Office import; OCR en-only; no PDF/X or PDF/UA; attachments one-way; no timestamp server | `docs/gaps.md` | not implemented (verified absent) |

## 2. Automation-surface counts: v0.14.0 → v0.15.0

| Surface | v0.14.0 | v0.15.0 (measured) | Change |
|---|---:|---:|---|
| Automation tools | 179 | **179** | unchanged |
| Registry commands | 205 | **205** | unchanged (id diff clean) |
| Control methods | 17 | **17** | unchanged |
| CLI subcommands | 14 + `check-one` | **same** | unchanged |
| Languages | 34 | **35** | +`fa` |
| MCP tools / compact entries | 179 / 17 | **same** | unchanged |
| MCP resources | 4 templates + 2 | **same** | unchanged |
| Convertible / Office / form-data / page-image | 12 / 4(5) / 8(6) / 3 | **same** | unchanged (page-image export now worker-threaded) |

## 3. Uncertain / not verified

- GUI behaviour not launched; registry + docs + packaging are the evidence.
- The `ToolDef::command` mapped-tool count (71) was carried, not re-derived this pass.
- Office export fidelity remains lossy by the project's own account.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| Several docs "141 automation tools / 184 commands" | 179 / 205 |
| README MCP compact "about ten" | 15 core + `tool_search` + `tool_call` = 17 |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # 75360d1d7db06fed974f48c914d4c04132757187
grep -oE '\bt\("[a-z_][a-z0-9_.]*"' crates/automation/src/tools.rs | sort -u | wc -l   # 153
grep -cE '^\s+t\($' crates/automation/src/tools.rs              # 26  (153 + 26 = 179)
grep -cE '^\s+c\("|^\s+c\($' crates/engine/src/commands.rs      # 205
grep -oE '"[a-z]+\.[a-zA-Z.]+"' crates/ui-egui/src/control/requests.rs | sort -u | wc -l  # 17
ls crates/ui-egui/src/i18n/*.tsv | wc -l                        # 34 catalogs (+English = 35)
```
