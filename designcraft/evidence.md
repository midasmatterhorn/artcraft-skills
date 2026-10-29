# DesignCraft — evidence ledger (tag v0.14.0)

Audit basis: this checkout is tag **`v0.14.0`**, commit **`7da69c16ce221f46e8f27cb41e0c88167c8be416`**
("Release 0.14.0", 2026-10-28; shallow clone plus a fetched `v0.13.0` ref for set diffs). Inspection
date **2026-10-29**. Installed `/Applications/DesignCraft.app` prints `designcraft 0.14.0`; the GUI
was never launched.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 542 engine `cmd!` ids (was 537) | `git grep -o 'cmd!' HEAD -- crates/engine/src \| wc -l` = 542; v0.13.0 = 537 | implemented |
| 2 | +5 engine: `file.info`, `ink.separations`, `note.split`, `text.deleteSurrounding`, +1 const-built | string-set diff of command-id literals between the tags; `file.info` = File Info dialog (PR #1712), `ink.separations` = Separations Preview (PR #1375), `note.split` = Split Note (PR #1783) | implemented |
| 3 | 176 UI commands (was 172): +`help.checkForUpdates`, `ui.dock`, `view.storyEditorDepthRuler`, `window.shortcutSets` | `crates/ui-egui/src/menus/ui_commands.rs:14` `pub const UI_COMMANDS`; clean id-set diff vs `v0.13.0:crates/ui-egui/src/menus.rs` (4 added, 0 removed) | implemented |
| 4 | 26 MCP tools, set unchanged | single-line tool-name rows identical between the tags (24 + 2 multi-line) | implemented |
| 5 | Control methods +`ui.docking`, none removed | arm-set diff `v0.13.0:crates/ui-egui/src/control.rs` vs HEAD: only `ui.docking` added | implemented |
| 6 | 10 CLI subcommands unchanged | `apps/designcraft-cli/src/main.rs` subcommand enum | implemented |
| 7 | PDF/X-1a:2003 export via the craft-prepress flattener | `crates/pdf/src/lib.rs:31` ("PDF/X-1a:2003 is the PDF/X-4 print file flattened by craft-prepress"); `crates/pdf/src/export.rs:61` `craft_prepress::InkSet`; PRs #1384, #1374 | implemented |
| 8 | Separations Preview shows the exported PDF's plates, spot included; one sheet per frame on the UI thread | `crates/pdf/src/inks.rs` module doc; PRs #1375, #1853 | implemented |
| 9 | `note.split`; note/footnote caret fixes | `crates/engine/src/cmd/editorial.rs`; PRs #1783, #1780, #1785, #1775 | implemented |
| 10 | `file.info` + PDF export writes title/author/description/keywords | PR #1712; `crates/engine/src/cmd/file.rs` | implemented |
| 11 | Story Editor depth ruler + View toggle | `crates/ui-egui/src/story_editor.rs`; `view.storyEditorDepthRuler`; PR #1795 | implemented |
| 12 | Shortcuts on craft-keymap: panel shortcuts, editable tool keys, Keyboard Shortcuts dialog with sets | `crates/ui-egui/src/menus/keys.rs`; `window.shortcutSets`; PRs #1298, #1410, #1854 | implemented |
| 13 | Tables gradient cell fills (screen + PDF); column rules ascent→descent; ruler 10× tick step | PRs #1768, #1802, #1808 | implemented |
| 14 | Format version 4 unchanged; atomic writes | `crates/format/src/lib.rs:29` `VERSION: u32 = 4` | implemented |
| 15 | MCP answers a parse error on non-UTF-8 lines | PR #1803; `crates/mcp/src/server.rs` | implemented |
| 16 | Startup update prompt; Windows per-user install; egui 0.37 + shared docking | PRs #1817, #1896, #1810, #1311; craft pins in `Cargo.toml` | implemented |
| 17 | Placed-PDF layer choices applied on export; IDML graphic-layer options retained, not rendered | `crates/engine/src/cmd/pdflayers.rs`; `crates/pdf/src/optional_content.rs`; `docs/graphic-layer-options.md` | implemented / partial |
| 18 | No ExtendScript/UXP, no plug-in model, no AI, no PDF font repair | `docs/gaps.md` §§22, 23, 28 | not implemented (verified absent) |

## 2. Automation-surface counts: v0.13.0 → v0.14.0

| Surface | v0.13.0 | v0.14.0 (measured) | Change |
|---|---:|---:|---|
| Engine `cmd!` ids | 537 | **542** | +5 (four named above; one const-built) |
| UI commands | 172 | **176** | +4 (id-set diff clean) |
| MCP tools | 26 | **26** | unchanged |
| Control methods | 26 (29 arm strings) | **+`ui.docking`** | nothing removed |
| CLI subcommands | 10 | **10** | unchanged |
| Format version | 4 | **4** | unchanged |

## 3. Uncertain / not verified

- The fifth new engine id is const-built (not a string literal near its `spec!`/`cmd!` site) — the
  live registry (`designcraft-cli commands`) is authoritative.
- GUI behaviour not launched; registry + docs + packaging are the evidence.
- INDD/INDT and IDML fidelity on real files remains unmeasured by the project (`docs/gaps.md` §§2-4).

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `docs/target-app-parity.md` "~200 commands" / "446 engine + 99 UI" | 542 `cmd!` ids + 176 UI commands measured here |
| `docs/agents.md` / `SCRIPT_HELP` "most commands ignore unknown parameters" | CLI, MCP and control channel reject unknown params (`crates/engine/src/cmd/params.rs`) |
| `crates/pdf/src/lib.rs` header once said "Not yet: tagged PDF, bookmarks…" | all wired; PDF/X-1a joined this release |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # 7da69c16ce221f46e8f27cb41e0c88167c8be416
git grep -o 'cmd!' HEAD -- crates/engine/src | wc -l            # 542
git grep -o 'cmd!' v0.13.0 -- crates/engine/src | wc -l         # 537
awk '/pub const UI_COMMANDS/,/^];/' crates/ui-egui/src/menus/ui_commands.rs | grep -oE '"[a-z]+\.[a-zA-Z]+"' | sort -u | wc -l   # 169 unique (176 entries with const-built rows)
sed -n '29p' crates/format/src/lib.rs                           # VERSION: u32 = 4
grep -n 'x1a\|X-1a' crates/pdf/src/lib.rs | head -2             # PDF/X-1a flattener note
grep -n 'API_VERSION\|ui.docking' crates/ui-egui/src/control.rs | head -2
```
