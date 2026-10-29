# FigCraft — evidence ledger (tag v0.12.1)

Audit basis: this checkout is tag **`v0.12.1`**, commit **`ef9721c5b9d0f1cc19a74449cbe175fc06bf8efa`**
("Release 0.12.1", shallow clone). Inspection date **2026-10-29**. Installed `/Applications/FigCraft.app`
reports 0.12.1 and its binary prints the same full SHA; the GUI was never launched.

The v0.11.2 → v0.12.1 wave is large (598 commits): Sketch import, `.fig` export/import improvements,
five new Dev Mode code targets, boards growth (9 → 19 commands), plugin API 4, `command.batch` named
steps, the `window.figcraft` web control channel, mobile layout, four new locales, and the startup
update prompt.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 616 `spec!(` registration sites; some ids const-built (live count via CLI) | `crates/engine/src/cmd.rs:57` `macro_rules! spec` (`$id:expr` — consts legal); `grep -rho 'spec!(' crates/engine/src \| wc -l` = 616 (was 597) | implemented |
| 2 | 212/212 menu items | `docs/parity-checklist.md` "**212 / 212 menu items (100.0%)**" | implemented |
| 3 | 159 keymap bindings, 12 groups | `crates/engine/src/keymap.rs:160` `pub static KEYS` — 159 `k(` rows between `KEYS` and `GESTURES:345`; `Group::ALL [Group; 12]` at `:45` | implemented |
| 4 | 9 CLI subcommands; `--help` anywhere; dash-prefixed filenames | `apps/figcraft-cli/src/main.rs` USAGE (`info export convert render run commands mcp plugin perf`); PRs #954, #4063-equivalent | implemented |
| 5 | 17 control methods | `crates/ui-egui/src/control.rs` — 16 direct arms + `ui.menu.invoke` at `:1390` | implemented |
| 6 | 18 MCP tools, set unchanged; 2 resources + 2 templates; 4 prompts | `crates/mcp/src/tools.rs:86` `TOOL_NAMES` (18); `resources.rs`; `prompts.rs` | implemented |
| 7 | 19 `board.*` commands (was 9); timer/voting/templates/tables/reattach/curved connectors/dot grid | grep `"board\.[a-z]+"` in `crates/engine/src/` — sticky shape connector ink stamp label editText nextSticky setColor setStyle reattach table tableEdit template templates timer timerState vote voteResults; `crates/engine/src/boards/board_templates.rs:27` `TEMPLATES: &[BoardTemplate]` (5) | implemented |
| 8 | 21 `collab.*` commands (set unchanged); `branch.*` commands now work inside live sessions | grep `"collab\.[a-zA-Z]+"` in `crates/engine/src/` = 21; PR #1367 | implemented |
| 9 | Plugin API version 4; widgets take text input + property menu; `saveFile` permission | `crates/plugin/src/manifest.rs:11` `pub const API_VERSION: u32 = 4`; PRs #1365, #698 | implemented |
| 10 | 22 locale catalogs (+it, ko, th, vi) | `ls crates/ui-egui/locales/` = 22 `.toml` (was 19) | implemented |
| 11 | `.sketch` import (Sketch 48+) | `crates/engine/src/sketch_import_tests.rs` (mod at `lib.rs:447`); PR #1021 | implemented (best-effort) |
| 12 | `.fig` export Figma imports, with component set properties; import coverage note; large files keep layers + library links | PRs #1152, #951, #989; `crates/format/src/fig/export.rs` | implemented (experimental) |
| 13 | Dev Mode code targets: CSS/HTML/React/Vue/Leptos/SwiftUI/Compose/ArkUI + React+Tailwind page + Tailwind theme + Dart constants + Android Vector Drawable | `crates/engine/src/dev/codegen/{arkui,compose,css,html,swift}.rs`, `crates/engine/src/dev/tailwind.rs`, `crates/engine/src/dev/component_codegen.rs`, tests `vue_codegen_tests.rs`/`html_codegen_tests.rs`/`component_codegen_tests.rs`; PRs #1011, #664, #726, #840, #1202 | implemented |
| 14 | `command.batch` named steps (`as`/`$ref`), paths in `field`, errors name the failing step | PRs #1003, #1340; `docs/mcp.md` | implemented |
| 15 | `window.figcraft` web control channel; downloads for Save/Export | `apps/figcraft-web/src/query.rs`; PRs #824, #1010 | implemented |
| 16 | 8 design templates + 5 board templates; 5 examples; 3 example plugins | `crates/engine/src/content/templates.rs:72` (8); `crates/engine/src/boards/board_templates.rs` (5); `examples/`; `plugins/examples/` | implemented |
| 17 | Save guardrails: no overwrite of externally-changed file or unloaded-image file; NaN/inf → 0 | PRs #1374, #1314, #959; `crates/engine/src/cmd/file.rs` `save_to` | implemented |
| 18 | LCH/OKLCH picker; JIS X 4051 kinsoku; truncated-text fills last line; Thai backspace; font discovery incl. Adobe Fonts | PRs #827, #990, #1378, #1242, #661, #1309, #1294; `crates/engine/src/fonts.rs` | implemented |
| 19 | Startup update prompt + self-update; Windows per-user install | PRs #1328, #1399; `Cargo.toml` craft pins | implemented |
| 20 | No Figma plugin compat, no AI, no spell check, no `.jam`/`.deck`/HEIC/video | `docs/gaps.md` 6, 11, 19; `docs/file-format-parity.md` | not implemented (verified absent) |

## 2. Automation-surface counts: v0.11.2 → v0.12.1

| Surface | v0.11.2 | v0.12.1 (measured) | Change |
|---|---:|---:|---|
| `spec!` registration sites | 597 | **616** | +19 (some ids const-built; live count `figcraft-cli commands --json`) |
| Menu items live | 212/212 | **212/212** | unchanged |
| Keymap bindings | 159 | **159** | unchanged count |
| CLI subcommands | 9 | **9** | unchanged |
| Control methods | 17 | **17** | unchanged set |
| MCP tools | 18 | **18** | unchanged set |
| MCP resources/templates | 2 + 2 | **2 + 2** | unchanged |
| MCP prompts | 4 | **4** | unchanged |
| `collab.*` commands | 21 | **21** | set unchanged; branches now work inside live sessions |
| `board.*` commands | 9 | **19** | +reattach, table, tableEdit, template, templates, timer, timerState, vote, voteResults, dot grid |
| Board templates | — | **5** | new |
| Plugin API | 3 | **4** | widgets text input + property menu; `saveFile` permission |
| Locale catalogs | 19 | **22** | +it, ko, th, vi |
| Design templates / examples | 8 / 5 | **8 / 5** | unchanged (templates moved to `content/templates.rs`) |

## 3. Uncertain / not verified

- The exact per-command id list behind the 616 registration sites (const-built ids) — the live registry
  is `figcraft-cli commands --json`.
- GUI behaviour not launched; registry + docs + packaging are the evidence.
- `.fig`/`.sketch`/REST import fidelity is best-effort and unproven against real files (`docs/gaps.md`).

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| README "about 49%" vs measured table ~53% ready / ~85% breadth | both are self-assessments; the measured table is the closer number |
| `docs/parity-checklist.md` may lag the registry | count with `figcraft-cli commands --json` |
| `docs/architecture.md` "two example plugins" | `plugins/examples/` holds three |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # ef9721c5b9d0f1cc19a74449cbe175fc06bf8efa
grep -rho 'spec!(' crates/engine/src/ | wc -l                   # 616
grep -E '212' docs/parity-checklist.md | head -1                # 212 / 212 menu items
awk 'NR>=160 && NR<345' crates/engine/src/keymap.rs | grep -cE '^\s+k\('   # 159
awk '/pub const TOOL_NAMES/,/];/' crates/mcp/src/tools.rs | grep -oE '"[a-z_]+"' | wc -l  # 18
grep -rho '"board\.[a-zA-Z]*"' crates/engine/src/ | sort -u | grep -c board\.  # 19 (+1 prefix-only string)
grep -rho '"collab\.[a-zA-Z]*"' crates/engine/src/ | sort -u | wc -l       # 21 (22nd match is the bare prefix)
ls crates/ui-egui/locales/ | wc -l                              # 22
grep -n 'API_VERSION' crates/plugin/src/manifest.rs             # u32 = 4
ls crates/engine/src/dev/codegen/                               # arkui compose css html swift
```
