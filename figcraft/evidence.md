# FigCraft — evidence ledger (tag v0.18.1)

Audit basis: this checkout is tag **`v0.18.1`**, commit
**`4acc293c2ec941ac1400837ee7e3ab51780399f8`** (`git rev-parse HEAD`, release 2026-11-12).
Inspection date **2026-11-12**. The installed `FigCraft.app` matches the release —
`Info.plist` `CFBundleShortVersionString` 0.18.1, `CFBundleIdentifier`
`ai.storyteller.figcraft` — and its binary prints `FigCraft 0.18.1
(4acc293c2ec941ac1400837ee7e3ab51780399f8)` for `--version`, which returns before any window or
GPU context is created. The GUI was never launched, and the macOS bundle ships no CLI, so no
`figcraft-cli` command was executed on this machine (none is installed either).

v0.16.0 → v0.18.1 delta: **448 files changed** (+22,803/−1,969), measured with `git diff
v0.16.0..HEAD` (the shallow clone holds one squashed commit between the tags). Automation-surface
**id sets** were diffed between the two tags: nine command ids are new and **none removed** —
`board.mindMap`, `board.mindMapAdd`, `collab.reconnect`, `selection.createColorStyle`,
`text.direction`, `text.directionAuto`, `text.directionLtr`, `text.directionRtl`, `tool.crosshair`.
`spec!` sites move 637 → **646** engine-wide and 488 → **493** in `crates/engine/src/cmd/`
(641 distinct literal ids; a few ids are const-built). `board.*` commands 21 → **23**,
`collab.*` 21 → **22**, locale catalogs 24 → **25** (`crates/ui-egui/locales/zh-Hant.toml` added). MCP `TOOL_NAMES`, CLI
`Command` variants, control dispatch and plugin `API_VERSION` are byte-identical in membership.
Feature work: mind maps step 1 (`crates/doc/src/board_mindmap.rs` `mind_layout`,
`crates/engine/src/boards/board/mindmap.rs`, `crates/engine/src/board_mindmap_tests.rs`); per-
paragraph text direction (`crates/engine/src/cmd/text.rs`, `crates/format/src/fig/text_direction_tests.rs`);
selection colour styles (`crates/engine/src/selection/selection_colors.rs`,
`crates/ui-egui/src/panels/selection_colors.rs`); Suggest auto layout
(`crates/engine/src/cmd/structure/suggest.rs`, `crates/engine/src/layout_suggest_tests.rs`);
placement crosshair (`crates/engine/src/cmd/view.rs`, `crates/engine/src/place_crosshair_tests.rs`);
export colour profile and JPG quality (`crates/engine/src/export_profile_tests.rs`,
`crates/engine/src/jpg_export_tests.rs`, `crates/mcp/tests/it/export_profile.rs`); `.fig` scale
handling (`crates/format/src/fig/export/scale.rs`, `crates/format/src/fig/scale_factor_tests.rs`);
Developer Mode naming (`docs/feature-names.md`, `crates/ui-egui/src/naming_tests.rs`,
`crates/mcp/tests/display_names.rs`); the `craft-web-api` page API
(`apps/figcraft-web/src/api.rs`); reconnect pacing (`crates/collab-net/src/throttle.rs`,
`crates/collab-net/src/driver.rs`). Hardening: terminal-escape-safe CLI output
(`apps/figcraft-cli/src/files.rs`), import id collisions
(`crates/engine/src/cmd/file/import_ids.rs`), ICU4X word breaks (`crates/text/src/breaks.rs`),
SVG `color()`/`color-mix()` import (`crates/svg/src/import/css_color.rs`), pending-update install
on quit (`apps/figcraft/src/main.rs`).

Prior delta, kept for history: v0.15.0 → v0.16.0 changed 133 files with exactly one new command id
(`text.wrapStyle`), glass optics, the Bend tool click and the web host bridge; older rounds are in
`CHANGES.md`.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 646 `spec!` registration sites engine-wide, 493 in the command directory (637/488 at v0.16.0); 641 distinct literal ids; 9 new ids, none removed | `crates/engine/src/cmd.rs:57` `macro_rules! spec`; `grep -rho 'spec!(' crates/engine/src \| wc -l` = 646; literal-id parse = 641 | implemented |
| 2 | Menu coverage is 100% by the last generated check (212/212, generated 2026-10-21); the live catalog now counts **214** items minus `OWN`/`collab.*` | `docs/parity-checklist.md:7`; `crates/engine/src/catalog.rs` `MENU`, `OWN` (6 ids), `parity()`; static count 214 | implemented (doc stale for the total) |
| 3 | 163 keymap binding rows, 12 groups, 47 gesture rows; docs track 136 documented shortcut rows, 135 bound | `crates/engine/src/keymap.rs` `KEYS` (163 `k(` rows), `GESTURES` (47 rows), `enum Group` (12); `docs/ui-parity.md` › Documented shortcuts | implemented |
| 4 | 10 CLI subcommands; `mcp --attach --timeout` 1–600 s; `--help` anywhere; export lacks colour-profile/quality flags | `apps/figcraft-cli/src/args.rs` `enum Command` (`info export convert render run commands mcp plugin connect perf`), `--timeout` parsing tests | implemented |
| 5 | 17 control methods dispatched by the app channel; `events.poll` documented but only MCP implements it | `crates/ui-egui/src/control.rs` — 16 match arms + `ui.screenshot` routed in `route_queued`; `crates/mcp/src/{headless,tools}.rs`; `docs/control-protocol.md` lists 18 method sections including `events.poll` | implemented (17, not 18) |
| 6 | 19 MCP tools (set unchanged); 3 resources + 2 templates; 4 prompts | `crates/mcp/src/tools.rs` `TOOL_NAMES` (19); `crates/mcp/src/resources.rs` (`document`, `commands`, `comments`; `node/{id}`, `command/{id}`); `crates/mcp/src/prompts.rs` (4) | implemented |
| 7 | 23 `board.*` commands incl. `board.mindMap`/`board.mindMapAdd`; `board.editText` is a UI request, not a command | `crates/engine/src/boards/` `spec!` ids; `crates/engine/src/boards/board/mindmap.rs`; `crates/ui-egui/src/app/commands.rs:135` handles `board.editText` | implemented |
| 8 | 22 `collab.*` commands, incl. new `collab.reconnect` | `crates/engine/src/sharing/live/join.rs:223`; `grep -rho '"collab\.[a-zA-Z]*"' crates/engine/src \| sort -u` = 23 strings, one the bare prefix | implemented |
| 9 | Plugin API version **6**; `saveFile` permission; four example plugins | `crates/plugin/src/manifest.rs:11` `API_VERSION: u32 = 6`; `plugins/examples/{counter,export-names,swatch-grid,tidy-names}` | implemented |
| 10 | **25** locale catalogs, `zh-Hant` added at this tag | `ls crates/ui-egui/locales/` = 25 `.toml`; `git diff` adds `crates/ui-egui/locales/zh-Hant.toml` | implemented |
| 11 | Mind maps: root + up to 20 children on curved branch connectors; child/sibling add; relayout from root; 2,000-node and depth-64 caps; 88/48 spacing; no toolbar/shortcut/`+`/reparent yet | `crates/engine/src/boards/board/mindmap.rs`; `crates/doc/src/board_mindmap.rs` (`MIND_MAX_NODES`, `MIND_MAX_DEPTH`, `MIND_GAP_X`, `MIND_GAP_Y`, `MIND_MAX_STARTERS`); `docs/boards-parity.md` › Mind maps | implemented (partial, step 1) |
| 12 | Per-paragraph text direction with `auto|ltr|rtl`, `node.set textDirection`, inspect fields, CSS `direction`, `.fig` `sourceDirectionality` | `crates/engine/src/cmd/text.rs:457-475`; `docs/ui-parity.md` › Text direction; `crates/format/src/fig/text_direction_tests.rs` | implemented (not in text styles) |
| 13 | Selection colors: shared paint list, one-undo edits, style/variable apply/detach, per-row library styles, `selection.createColorStyle` | `crates/engine/src/selection/selection_colors.rs:135`; `crates/ui-egui/src/panels/selection_colors.rs`; `docs/ui-parity.md` › Selection colors | implemented (partial tail) |
| 14 | Suggest auto layout splits into rows/columns, wraps bands in hugging nested frames, returns warnings | `crates/engine/src/cmd/structure/suggest.rs:226`; `crates/engine/src/layout_suggest_tests.rs` | implemented |
| 15 | Placement crosshair: arrows show/move it with a shape/frame tool, Enter places (`tool.place`) | `crates/engine/src/cmd/view.rs:543`; `crates/engine/src/place_crosshair_tests.rs`; `docs/ui-parity.md` | implemented |
| 16 | Export colour profile (`sameAsFile|srgb|displayP3`) for PNG/JPG/WebP and JPG `quality` 1–100 (default 90), on `file.export`, export settings and MCP `export`; SVG/PDF/XML always sRGB | `crates/engine/src/cmd/file.rs` `file.export` params; `crates/engine/src/export_profile_tests.rs`; `crates/engine/src/jpg_export_tests.rs`; `crates/mcp/src/tools.rs` export schema | implemented |
| 17 | Developer Mode is the UI name (ids `view.devMode`/`dev.*`, saved fields unchanged; "Dev Mode" search alias) | `docs/feature-names.md`; `crates/engine/src/catalog.rs` `SEARCH_ALIASES`; `crates/ui-egui/src/naming_tests.rs`; `crates/mcp/tests/display_names.rs` | implemented |
| 18 | Web page API: `request`, `execute`, `commands`, `docInspect`, `uiInspect`, `screenshot` from `craft-web-api`, plus `inspect`, `openFile`, `captureDownloads`, `files`, `readFile`; 30 s timeout and cancellation | `apps/figcraft-web/src/api.rs`; `docs/control-protocol.md` › In the browser | implemented |
| 19 | Live sessions reconnect until leave, merge offline edits on rejoin, and expose `collab.reconnect`; paced queues per connection | `crates/engine/src/sharing/live/join.rs`; `crates/collab-net/src/{throttle,driver}.rs`; `docs/collaboration-parity.md` | implemented (preview feature) |
| 20 | `.penpot` (Penpot 2.x) import and export, offline on desktop/CLI/MCP/WASM; `.jam` imports as a board, export unsupported | `crates/format/src/penpot.rs`; `crates/engine/src/cmd/file/{load,export}.rs`; `docs/penpot.md`; `docs/file-format-parity.md` | implemented (Penpot best effort) |
| 21 | `.figcraft` bounds: ≤100 versions, ≤100 branches, 16× document ratio within 512 MiB member, 4 GiB/1 GiB document cap, 6 GiB/2 GiB per-open unpack, images 20k/4 GiB | `crates/format/src/lib.rs` `MAX_VERSIONS`, `MAX_BRANCHES`, `DOCUMENT_RATIO`, `MAX_MEMBER`, `MAX_DOCUMENT`, `MAX_UNPACKED`, `IMAGE_BUDGET` | implemented |
| 22 | Export formats: png, jpg, svg, pdf, webp, xml (Android Vector Drawable), fig, penpot; JSON only through CLI `convert`/`run --out` | `crates/doc/src/props.rs` `ExportFormat::{ALL,from_ext}`; `crates/engine/src/cmd/file/export.rs`; `apps/figcraft-cli/src/files.rs` | implemented |
| 23 | No Figma plugins, no AI, no spell check, no HEIC/video, no `.deck`; `.fig` unproven on real files | `docs/gaps.md` 1, 3, 6, 11, 19; `docs/file-format-parity.md`; `docs/plugins.md` | not implemented (verified absent) |

## 2. Automation-surface counts: v0.16.0 → v0.18.1

| Surface | v0.16.0 | v0.18.1 (measured) | Change |
|---|---:|---:|---|
| `spec!` registration sites (engine / command dir) | 637 / 488 | **646 / 493** | +9 / +5 |
| Distinct literal command ids | 632 | **641** | +9, none removed |
| Menu items counted by `catalog::parity` | 212 | **214** static (doc still 212) | +2 counted `Text direction` rows (`Auto` is in `OWN`) |
| Keymap binding rows / groups / gestures | 163 / 12 / — | **163 / 12 / 47** | bindings unchanged |
| CLI subcommands | 10 | **10** | unchanged set |
| Control methods (app channel) | 17 | **17** | unchanged set |
| MCP tools | 19 | **19** | unchanged set |
| MCP resources/templates | 3 + 2 | **3 + 2** | unchanged |
| MCP prompts | 4 | **4** | unchanged |
| `collab.*` commands | 21 | **22** | +`collab.reconnect` |
| `board.*` commands | 21 | **23** | +`board.mindMap`, `board.mindMapAdd` |
| Board templates | 5 | **5** | unchanged |
| Plugin API | 6 | **6** | unchanged |
| Locale catalogs | 24 | **25** | +`zh-Hant` |
| Design templates / examples / example plugins | 8 / 5 / 4 | **8 / 5 / 4** | unchanged (baseline said 3 plugins: wrong) |

## 3. What was re-measured, carried forward, and how

Re-measured at this tag (method in §5): every row of the count table; the full command-id set diff
against `v0.16.0`; `board.*`, `collab.*` and locale directory set diffs; the MCP tool name array;
CLI `Command` variants; control dispatch arms; plugin `API_VERSION`; keymap row/group/gesture counts;
templates, examples and plugin-example directories; prototype enums (`Trigger` 10, `Action` 11,
`Transition` 8, `Easing` 13 in `crates/doc/src/proto.rs`); `crates/format/src/lib.rs` limits. The
installed bundle's version string was read from `--version` and `Info.plist`.

Carried forward after a path check (code unchanged or change irrelevant to the claim): frames/
shapes/text/vector/component/design-system/Developer Mode capability prose; `.figcraft` member
layout; `.fig`/REST/Sketch import behaviour; live-session command groups other than reconnect;
server subcommands. The `docs/` statements behind those claims were re-read where the diff touched
them.

Deliberately **not** claimed: any live GUI behaviour, any `.fig` fidelity against real Figma files,
or any `figcraft-cli commands --json` output — no build or CLI binary was available, and the
addendum forbids builds.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `docs/parity-checklist.md` "212 / 212 menu items" (generated 2026-10-21) | `catalog::MENU` minus `OWN`/`collab.*` = **214**; the three `Text ▸ Text direction` rows postdate the generated file. `text.directionAuto` is in `OWN`, so only two are counted |
| README "about 49%" vs measured table ~53% ready / ~85% breadth / ~94% core | both are self-assessments; the measured table is the closer number |
| `docs/control-protocol.md` documents `events.poll` as a control method (18 sections) | the app channel has no such arm (16 `handle()` arms + `ui.screenshot` = 17); only `crates/mcp/src/headless.rs` implements `events.poll` |
| `docs/architecture.md` "two example plugins" | `plugins/examples/` holds **four** (counter, export-names, swatch-grid, tidy-names); the baseline skill's "three" was also wrong |
| Baseline skill said `MAX_UNPACKED` 4 GiB/1 GiB | `MAX_DOCUMENT` is 4 GiB/1 GiB; `MAX_UNPACKED` is **6 GiB/2 GiB** (unchanged since v0.16.0) |
| Baseline skill said 129 documented shortcut rows / 128 bound | `docs/ui-parity.md` now says **136 / 135** |
| Release notes say "mind maps in the document and engine (#2226, step 1)" | correct, but partial: command-only, no toolbar/shortcuts; `docs/boards-parity.md` is the accurate status |
| `docs/feature-names.md` calls the rename complete | ids, preference keys and saved fields intentionally keep `devMode`; "Dev Mode" survives as an Actions-palette search alias |
| MCP `open_file`'s tool description lists only `.figcraft`, `.json`, `.fig`, `.sketch`, `.svg` and images | the handler forwards to `file.open`, which also reads `.jam` (as a board) and `.penpot`; the description lags the code |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # 4acc293c2ec941ac1400837ee7e3ab51780399f8
git -C <clone> describe --tags --exact-match HEAD               # v0.18.1
git diff --name-only v0.16.0..HEAD | wc -l                      # 448
grep -rho 'spec!(' crates/engine/src | wc -l                    # 646
grep -rho 'spec!(' crates/engine/src/cmd/ | wc -l               # 493
grep -rhoE '"board\.[a-zA-Z]+"' crates/engine/src | sort -u | wc -l   # 24 strings (1 is a UI request) -> 23 commands
grep -rho '"collab\.[a-zA-Z]*"' crates/engine/src | sort -u | wc -l   # 23 strings (1 bare prefix) -> 22 commands
ls crates/ui-egui/locales/ | wc -l                              # 25
awk '/pub const TOOL_NAMES/,/^\];/' crates/mcp/src/tools.rs | grep -oE '"[a-z_]+"' | wc -l  # 19
grep -n 'API_VERSION' crates/plugin/src/manifest.rs             # u32 = 6
grep -cE '^\s+k\(' crates/engine/src/keymap.rs                  # 163 binding rows
awk '/pub static GESTURES/,0' crates/engine/src/keymap.rs | grep -cE '^\s+\('   # 47
grep -n '212 / 212' docs/parity-checklist.md                # stale generated total (2026-10-21)
"FigCraft.app/Contents/MacOS/FigCraft" --version                # FigCraft 0.18.1 (4acc293c2ec9…)
```

## 6. Uncertain / not verified

- The exact live command count behind the 646 `spec!` sites (const-built ids): the registry is
  `figcraft-cli commands --json`, which this round could not build or run.
- Whether all 214 catalog items resolve to a command: a static scan leaves four ids
  (`object.rotate180`, `view.zoom50|100|200`) unmatched as literal `spec!` ids; they may be
  const-built. Re-run `cargo xtask parity`.
- GUI behaviour was not exercised; registry, docs and packaging are the evidence.
- `.fig`/`.jam`/`.sketch`/REST/Penpot fidelity is best-effort and unproven against real files
  (`docs/gaps.md`).
- Mind-map layout numbers (88/48) and caps were read from code and mirrored in `docs/boards-parity.md`,
  not measured against the incumbent.
- The server's public-hosting tail (Caddyfile, owner tokens, idle expiry) was not exercised.

## Round 2026-11-12 (refresh)

- Pinned to `v0.18.1` = `4acc293c2ec941ac1400837ee7e3ab51780399f8` (installed `FigCraft 0.18.1
  (4acc293c2ec9…)`, bundle id `ai.storyteller.figcraft`). GUI not launched; no CLI in the bundle.
- Re-measured: `spec!` sites 637 → **646** / 488 → **493**; command-id diff **+9 / −0**;
  `board.*` **23**; `collab.*` **22**; locales **25**; MCP **19**; CLI **10**; control **17**;
  keymap **163** bindings, **12** groups, **47** gestures; plugin API **6**; templates **8 + 5**;
  examples **5**; example plugins **4** (baseline's 3 corrected).
- Corrected stale figures by measuring both tags: menu total 212 → **214** static (generated doc
  stale), shortcut rows **136/135** (not 129/128), `MAX_UNPACKED` **6 GiB/2 GiB** (baseline
  conflated it with `MAX_DOCUMENT`), example plugins **4** (not 3).
- Added this round to `SKILL.md`: mind maps, text direction, selection colour styles, Suggest auto
  layout, placement crosshair, export colour profile/JPG quality, Developer Mode naming, the
  `craft-web-api` page API, reconnect, Penpot import/export, ICU4X word breaks and the CLI's
  terminal-escape hardening. Every cited repo-relative path was re-resolved against this clone.
