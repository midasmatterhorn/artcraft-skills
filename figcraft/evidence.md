# FigCraft — evidence ledger (tag v0.16.0)

Audit basis: this checkout is tag **`v0.16.0`**, commit **`f45b261687880e56d1bad11ec82b45131e57ef8b`**
(`git rev-parse HEAD`, release 2026-11-06). Inspection date **2026-11-07**. Installed
`/Applications/FigCraft.app` matches the release — `Contents/Info.plist` `CFBundleShortVersionString`
0.16.0, `CFBundleIdentifier` `ai.storyteller.figcraft` — and prints `FigCraft 0.16.0
(f45b261687880e56d1bad11ec82b45131e57ef8b)`; the GUI was never launched, and the macOS bundle ships
no CLI, so nothing was executed from it on this machine.

v0.15.0 → v0.16.0 delta: **133 files changed** (+4156/−545), measured with `git diff
v0.15.0..HEAD`. Automation-surface **id sets are unchanged** — MCP `TOOL_NAMES`, `board.*`,
`collab.*`, the locale directory, clap `Command` variants, control dispatch and plugin `API_VERSION`
are identical at both tags. Exactly **one engine id is new: `text.wrapStyle`** (Wrap style: auto /
balance / pretty), the only added `spec!(` line (`crates/engine/src/cmd/text.rs:312`), so `spec!`
sites move 636 → 637 engine-wide and 487 → 488 in `crates/engine/src/cmd/`. Feature work: glass
rebuilt to the reference tool's optics (thick-lens bend toward the core, bevel light line, 8-step
dispersion, variables accepted, frost 0–100; `crates/render/src/glass.rs`, `backdrop.rs`), the Bend
tool curving a sharp point on a click (`crates/engine/src/canvas/vectoredit/pointer.rs`), and the web
build's embedding host bridge (`?host=parent`, `data-host="page"`, host file handed back on Save;
`apps/figcraft-web/src/host.rs`, `hostmode.rs`, `packaging/web/README.md`). Hardening: fractional
`index` rejected in `proto.interaction.remove`/`set` and `layout.setTrack`, invalid `dashes` rejected
in `node.set` (`crates/engine/src/cmd/proto.rs`, `crates/layout/src/lib.rs`), HTML export cannot be
escaped out of its generated `<style>` element (`crates/engine/src/dev/codegen/html.rs`), plugin
`text.preview` held to the permissions of the command it previews, plugin-offered files written
through the confined helper, MCP prompt placeholders rendered in one pass
(`crates/mcp/src/prompts.rs`).

Prior deltas, kept for history: v0.13.1 → v0.15.0 changed the automation surface by one CLI verb,
one MCP tool and one control method and otherwise fixed code export, comment thread-id parsing and
number fields; v0.12.1 → v0.13.1 added `comment.prompt` and `file.fontReport`, `connect publish`,
clap parsing with completions/man pages, FigJam `.jam` boards as boards, comment mentions, colour
variables calculated from others, and locales 22 → 24.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 637 `spec!(` registration sites engine-wide, 488 in the command directory (636/487 at v0.15.0); one new id `text.wrapStyle`; some ids const-built (live count via CLI) | `crates/engine/src/cmd.rs:57` `macro_rules! spec` (`$id:expr` — consts legal); `crates/engine/src/cmd/text.rs:312`; `grep -rho 'spec!(' crates/engine/src \| wc -l` = 637 | implemented |
| 2 | 212/212 menu items (unchanged) | `docs/parity-checklist.md` "**212 / 212 menu items (100.0%)**"; `docs/target-app-parity.md` › Headline | implemented |
| 3 | 163 keymap bindings, 12 groups (was recorded as 159 — stale) | `crates/engine/src/keymap.rs:160` `pub static KEYS` — 163 `k(` rows between `KEYS` and `GESTURES:352`; `Group::ALL` is 12 groups | implemented |
| 4 | 10 CLI subcommands, incl. `connect publish` and `plugin publish`; `--help` anywhere; dash-prefixed filenames | `apps/figcraft-cli/src/args.rs` `enum Command` (`info export convert render run commands mcp plugin connect perf`); `clap` parsing; `docs/cli.md` | implemented |
| 5 | 17 control methods dispatched by the app channel | `crates/ui-egui/src/control.rs` — 16 match arms in `handle()` + `ui.screenshot` in `route_queued`; `events.poll` is documented (`docs/control-protocol.md`) but only `crates/mcp/src/headless.rs` implements it | implemented (17, not 18) |
| 6 | 19 MCP tools (set unchanged); 3 resources + 2 templates; 4 prompts | `crates/mcp/src/tools.rs:86` `TOOL_NAMES` (19, incl. `wait_for_changes`); `resources.rs` (`document`, `commands`, `comments`; `node/{id}`, `command/{id}`); `prompts.rs` (4) | implemented |
| 7 | 21 `board.*` commands (set unchanged at v0.16.0); timer/voting/templates/tables/reattach/reshape/curved connectors/dot grid/addConnected | 19 ids registered one-per-line in `crates/engine/src/boards/` plus `board.label` and `board.templates` in one-line `spec!` form = 21; `board.editText` is a UI request, not a command; `crates/engine/src/boards/board_templates.rs:27` `TEMPLATES: &[BoardTemplate]` (5) | implemented |
| 8 | 21 `collab.*` commands (set unchanged) | `grep -rho '"collab\.[a-zA-Z]*"' crates/engine/src/ \| sort -u` = 22 strings, one of them the bare prefix: 21 ids | implemented |
| 9 | Plugin API version **6**; widgets take text input + property menu (4), open the plugin panel (5), draw lines and SVG pictures (6); `saveFile` permission | `crates/plugin/src/manifest.rs:11` `pub const API_VERSION: u32 = 6` (identical at v0.15.0); `docs/plugins.md` API 4/5/6 notes | implemented |
| 10 | 24 locale catalogs (unchanged at v0.16.0) | `ls crates/ui-egui/locales/` = 24 `.toml` (`ar bn bs cs de en es-419 es fi fr id it ja ka ko nl pl pt-BR ru sv th tr vi zh-Hans`) | implemented |
| 11 | `.sketch` import (Sketch 48+) | `crates/format/src/sketch.rs`, `crates/engine/src/sketch_import_tests.rs` | implemented (best-effort) |
| 12 | `.fig` export Figma imports, with component set properties; large files keep layers and library links | `crates/format/src/fig/export.rs`, `crates/format/src/fig/kiwi.rs`; `docs/file-format-parity.md` › Export to `.fig` | implemented (experimental) |
| 13 | Dev Mode code targets: CSS/HTML/React/Vue/Leptos/SwiftUI/Compose/ArkUI + React+Tailwind page + Tailwind theme + Dart constants + Android Vector Drawable | `crates/engine/src/dev/codegen/{arkui,compose,css,html,swift}.rs`, `crates/engine/src/dev/tailwind.rs`, `crates/engine/src/dev/component_codegen.rs`, tests `vue_codegen_tests.rs`/`html_codegen_tests.rs`/`component_codegen_tests.rs` | implemented |
| 14 | `command.batch` named steps (`as`/`$ref`), paths in `field`, errors name the failing step | `crates/engine/src/cmd/`, `docs/mcp.md` | implemented |
| 15 | `window.figcraft` web control channel; **host bridge (`?host=parent`, `data-host="page"`)**; downloads for Save/Export, host-opened file saved under the host's name | `apps/figcraft-web/src/query.rs`, `apps/figcraft-web/src/host.rs`, `apps/figcraft-web/src/hostmode.rs`, `crates/ui-egui/src/host_save_tests.rs`, `packaging/web/README.md` | implemented |
| 16 | 8 design templates + 5 board templates; 5 examples; 3 example plugins (unchanged) | `crates/engine/src/content/templates.rs:72` `TEMPLATES` (8); `crates/engine/src/boards/board_templates.rs` (5); `examples/` (5); `plugins/examples/` (3) | implemented |
| 17 | Save guardrails: no overwrite of externally-changed file or unloaded-image file; NaN/inf → 0; predecessor replaced with the same permissions | `crates/engine/src/cmd/file.rs` `save_to`; `crates/format/src/lib.rs` (`staging_tests.rs`, `large_tests.rs`) | implemented |
| 18 | LCH/OKLCH picker; JIS X 4051 kinsoku; truncated-text fills last line; Thai backspace; font discovery incl. Adobe Fonts | `crates/engine/src/fonts.rs`, `crates/text/src/layout.rs`; `docs/ui-parity.md` | implemented |
| 19 | Text **wrap style** (Auto/Balance/Pretty) on a whole layer; saved line breaks still win; per-paragraph, text styles and `.fig` mapping not included | `crates/engine/src/cmd/text.rs:312` `text.wrapStyle`; `node.set wrapStyle`/`textWrap`; `docs/ui-parity.md` (§ Text: wrap style) | implemented (partial tail) |
| 20 | **Glass**: variables accepted, thick-lens bend toward the core, light line on the 1-unit bevel, splay toward the centre, 8 dispersion steps, frost 0–100 | `crates/render/src/glass.rs` (`glass::tests::*`), `crates/render/src/backdrop.rs` (`backdrop_tests::splay_turns_the_bend_towards_the_centre`), `docs/target-app-parity.md` change log 2026-11-02 | implemented |
| 21 | **Bend tool**: a click on a sharp point curves it, handles along the line between its neighbours | `crates/engine/src/canvas/vectoredit/pointer.rs`; test `a_bend_click_curves_a_sharp_point_between_its_neighbours` (`crates/engine/src/canvas/vectoredit/tests.rs:148`); `docs/ui-parity.md` | implemented |
| 22 | Startup update prompt + self-update; Windows per-user install | `Cargo.toml` craft pins (craft-update); `docs/` packaging notes | implemented |
| 23 | No Figma plugin compat, no AI, no spell check, no `.deck`/HEIC/video, `.jam` import only as boards | `docs/gaps.md` 6, 11, 19; `docs/file-format-parity.md`; `docs/boards-parity.md` | not implemented (verified absent) |

## 2. Automation-surface counts: v0.15.0 → v0.16.0

| Surface | v0.15.0 (re-extracted) | v0.16.0 (measured) | Change |
|---|---:|---:|---|
| `spec!` registration sites (engine / command dir) | 636 / 487 | **637 / 488** | +1 (`text.wrapStyle`) |
| Menu items live | 212/212 | **212/212** | unchanged |
| Keymap bindings | 163 | **163** | unchanged at v0.16.0 |
| CLI subcommands | 10 | **10** | unchanged set |
| Control methods (app channel) | 17 | **17** | unchanged set |
| MCP tools | 19 | **19** | unchanged set |
| MCP resources/templates | 3 + 2 | **3 + 2** | unchanged |
| MCP prompts | 4 | **4** | unchanged |
| `collab.*` commands | 21 | **21** | unchanged set |
| `board.*` commands | 21 | **21** | unchanged set |
| Board templates | 5 | **5** | unchanged |
| Plugin API | 6 | **6** | unchanged |
| Locale catalogs | 24 | **24** | unchanged at v0.16.0 |
| Design templates / examples / example plugins | 8 / 5 / 3 | **8 / 5 / 3** | unchanged |

## 3. Uncertain / not verified

- The exact per-command id list behind the 637 registration sites (const-built ids) — the live registry
  is `figcraft-cli commands --json`.
- GUI behaviour not launched; registry + docs + packaging are the evidence.
- `.fig`/`.sketch`/REST fidelity is best-effort and unproven against real files (`docs/gaps.md`).
- Penpot: `crates/format/src/penpot.rs` (`import`) and the CLI's `--format penpot` export exist but were
  not audited this round; not described in `SKILL.md`.
- Glass optics were checked by the repo's own tests against synthetic files only; no live comparison
  was performed here.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `docs/control-protocol.md` documents `events.poll` as a control method | the app channel has no such arm (16 `handle()` arms + `ui.screenshot`); only `crates/mcp/src/headless.rs` implements `events.poll` |
| README "about 49%" vs measured table ~53% ready / ~85% breadth / ~94% core | both are self-assessments; the measured table is the closer number |
| `docs/parity-checklist.md` may lag the registry | count with `figcraft-cli commands --json` |
| `docs/architecture.md` "two example plugins" | `plugins/examples/` holds three |
| previous skill's "API 4", "159 bindings", "22 catalogs", "19 `board.*`", "2 resources", "18 methods" | API 6, 163, 24, 22, 3 + 2, 17 at both v0.15.0 and v0.16.0 |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # f45b261687880e56d1bad11ec82b45131e57ef8b
grep -rho 'spec!(' crates/engine/src/ | wc -l                   # 637
grep -rho 'spec!(' crates/engine/src/cmd/ | wc -l               # 488
grep -E '212' docs/parity-checklist.md | head -1                # 212 / 212 menu items
awk 'NR>=160 && NR<352' crates/engine/src/keymap.rs | grep -cE '^\s+k\('   # 163
awk '/pub const TOOL_NAMES/,/];/' crates/mcp/src/tools.rs | grep -oE '"[a-z_]+"' | wc -l  # 19
grep -rhoE 'spec!\(\s*"board\.[a-zA-Z]+"|^\s+"board\.[a-zA-Z]+",' crates/engine/src/ | grep -oE '"board\.[a-zA-Z]+"' | sort -u | wc -l  # 21
grep -rho '"collab\.[a-zA-Z]*"' crates/engine/src/ | sort -u | wc -l     # 22 (one is the bare prefix)
ls crates/ui-egui/locales/ | wc -l                              # 24
grep -n 'API_VERSION' crates/plugin/src/manifest.rs             # u32 = 6
grep -nE '"(engine|document|node|ui|window|app)\.[a-zA-Z.]+"' crates/ui-egui/src/control.rs | wc -l
grep -n 'enum Command' -A 20 apps/figcraft-cli/src/args.rs      # 10 variants
git diff --name-only v0.15.0..HEAD | wc -l                      # 133
```

## Round 2026-11-07 (refresh)

- Pinned to `v0.16.0` = `f45b261687880e56d1bad11ec82b45131e57ef8b` (installed `FigCraft 0.16.0
  (f45b2616…)`, bundle id `ai.storyteller.figcraft`). GUI not launched; no CLI in the bundle.
- Re-measured: `spec!` sites 636 → **637** / 487 → **488**; everything else in the count table was
  re-extracted and is **unchanged at v0.16.0**, with the id sets (MCP tools, `board.*`, `collab.*`,
  locales, CLI verbs, plugin API) diffed between the two tags — all diffs empty.
- Corrected stale carried-forward figures by measuring both tags: keymap **163** (not 159), control
  **17** (not 18; `events.poll` drift recorded above), `board.*` **21** (not 19), locales **24** (not
  22), plugin **API 6** (not 4), MCP **3 resources + 2 templates** (not 2 + 2), CLI list now names
  `connect publish` as the 10th verb and the MCP list names `wait_for_changes`.
- Every cited repo-relative path was re-resolved against this clone; none had moved, so none was
  re-cited. Docs read at this tag: `docs/{cli,mcp,control-protocol,file-format-parity,gaps,
  target-app-parity,ui-parity,boards-parity,dev-mode-parity,prototyping-parity,components-parity,
  collaboration-parity,localization-parity,hardware-parity,auto-layout-parity,plugins,
  parity-checklist,architecture}.md` plus `packaging/web/README.md`.
