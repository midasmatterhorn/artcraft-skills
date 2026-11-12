# DeckCraft — evidence ledger (tag v0.18.1)

Audit basis: this checkout is tag **`v0.18.1`**, commit **`7cc73ab1895ed2e30c8afbcada20c70b9ea0a440`**
— `git rev-parse HEAD` in the pinned checkout confirms it, and the tag `v0.18.1` points at it.
Inspection date **2026-11-12**. The previous release this skill described was **v0.16.0**
(`a3e2254d3de32ed1718f156f070b54a34b949b54`); v0.17.0 and v0.18.0 lie in between, so the delta below
covers all three. The clone is shallow and squashed at each tag (only `v0.16.0` and `v0.18.1` are
present), so the tag-to-tag diff is the evidence, not a commit list. The installed DeckCraft bundle
is version 0.18.1, bundle `ai.storyteller.deckcraft`, universal x86_64+arm64, Developer ID signed
and notarized; its binary prints `deckcraft 0.18.1`. The GUI was never launched; only `--version`
and `--help` were run, and both exit before eframe starts (`apps/deckcraft/src/main.rs`).

v0.16.0 → v0.18.1: **121 files changed, +2 939/−7 950** (`git diff --shortstat v0.16.0..HEAD`).
No id set moved: 329 command ids, 57 engine shortcuts, 52 UI commands, 12 CLI subcommands, 25
control methods (+2 aliases), 25 MCP tools, 49 transition rows, 107 animation entries, 8 themes,
11 layouts + `Custom`, 183 shape presets, 28 chart types, 45/9/17 SmartArt, 6 starters, 70 icons,
40 warps, 48/54 patterns, 28/62–12/12/15 3-D presets are identical at both tags. The delta is
architecture and behaviour: four media crates removed in favour of craft-libs, the web
`window.deckcraft` page API, stricter `shape.adjust`/`quickStyle`/`format.paragraph` validation,
body/group 3-D XML and unconnected SmartArt text preserved, over-budget charts kept verbatim,
photo-album edit refusal, MCP batch caps, a 16-decoder video cap, and undo/logging/spelling/font
hardening.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 329 engine commands, ids unique, 329 `cmd!` sites (identical set at v0.16.0) | `cmd!(` extraction under `crates/engine/src/cmd/`; id sets diffed between tags = 0 added, 0 removed | implemented |
| 2 | Kind split 234 ordinary / 57 `noundo` / 38 `query` | kind prefix of each `cmd!` site | implemented |
| 3 | 57 commands carry a shortcut; 56 distinct strings; one collision (`Cmd+Shift+V`) | shortcut argument of each `cmd!`; `edit.pasteText` and `format.painterApply` both declare it | implemented |
| 4 | 52 `UI_COMMANDS` rows, 15 with shortcuts | `crates/ui-egui/src/lib.rs::UI_COMMANDS` (unchanged file) | implemented |
| 5 | 25 MCP tools, same names at both tags | `tool(` name arguments in `crates/mcp/src/tools.rs`; name diff between tags empty | implemented |
| 6 | 25 control methods + aliases `ui.menu.invoke`, `command` | top-level arms of `match req.method.as_str()` in `crates/ui-egui/src/control.rs` (unchanged file) | implemented |
| 7 | 12 CLI subcommands | `SUBCOMMANDS` in `apps/deckcraft-cli/src/help.rs` (unchanged file) | implemented |
| 8 | Workspace is 20 crates + 3 apps + `xtask` (was 24) | `crates/` directories + `Cargo.toml` members; `crates/{opus,ogg,isobmff,matroska}` are gone, `crates/media/Cargo.toml` uses craft-audio/craft-media | implemented |
| 9 | Web build exposes `window.deckcraft` with request/execute/commands/docInspect/uiInspect/screenshot promises | `apps/deckcraft-web/src/api.rs` (`PageApi::new(APP, Methods::default(), request)`), `packaging/web/README.md` §"Driving it from the page" | implemented |
| 10 | Web API calls reject after 30 s; at most 64 wait at once | `packaging/web/README.md` (30 s); shared contract in the craft-libs `web-api` crate README (64 in flight) — shared crate not audited here | implemented (repo doc + shared contract) |
| 11 | `shape.adjust`/`shape.quickStyle` reject a negative or fractional `index` | `crates/engine/src/cmd/shape/appearance.rs` (`opt_usize_param`) | implemented |
| 12 | `format.paragraph`/`format.paragraphDialog` reject an unknown `align` and accept `centre`/`justifyLow`; `format.align` still falls back to left | `crates/engine/src/cmd/format/paragraph.rs::paragraph`, `paragraph_dialog`, `parse_align`; `align` (lenient) | implemented |
| 13 | `shape.lock` applies a group+child pair once | `crates/engine/src/cmd/shape.rs::lock` (dedupe + descendant filter) | implemented |
| 14 | `file.save`/`file.saveAs`/`run --save` refuse `.png`/`.jpg`/`.jpeg` | `crates/engine/src/cmd/file.rs::save_bytes` returns "saving a presentation as a single image isn't supported; use file.export" | implemented |
| 15 | Handout `perPage` must be 1/2/3/4/6/9 | `crates/engine/src/cmd/file.rs::pdf_options` (`opt_usize_param` + list check) | implemented |
| 16 | Native `presentation.json` capped at 256 MiB; notes page clamped to slide-size bounds | `crates/format/src/lib.rs` (`MAX_MANIFEST`, `SLIDE_SIDE`) | implemented |
| 17 | Save writes a hidden `.deckcraft.<pid>.<n>.saving`, checked against the write root | `crates/engine/src/io.rs::write_file` | implemented |
| 18 | PPTX keeps text-body/group 3-D XML (`a:scene3d`, `a:sp3d`, `a:flatTx`, group `p:grpSpPr`), 64 KiB and element-name validated | `crates/model/src/text.rs::BodyProps.raw3d`; `crates/pptx/src/read/{dml,shapes}.rs`; `crates/pptx/src/write/{dml,shapes}.rs::valid_raw3d` | implemented |
| 19 | SmartArt with no parent-child `cxn` keeps node text in `ptLst` order | `crates/pptx/src/dgm.rs::outline_ids` + tests | implemented |
| 20 | A chart over the presentation budgets is kept verbatim and written back whole, shown empty | `crates/model/src/chart.rs::Chart.verbatim`; `crates/pptx/src/read/chart.rs::frame_chart` (4 000 000 points, 256 MiB decode); `crates/pptx/src/write/chart.rs::chart_xml` | partial (kept, not editable) |
| 21 | Photo-album editor seeds within 48 items / 32 MiB per picture / 64 MiB total and refuses to replace a bigger album | `crates/engine/src/cmd/insert/album.rs` (`ALBUM_MAX_ITEMS`, `ALBUM_MAX_BYTES`, `ALBUM_MAX_TOTAL`, `items_from_slides`, `photo_album_edit`) | implemented |
| 22 | MCP `batch` and JSON-RPC batches cap at 1 000 entries and 64 MiB of results | `crates/mcp/src/server.rs` (`MAX_BATCH_ITEMS`, `MAX_BATCH_BYTES`), `crates/mcp/src/tools.rs` ("batch"), `crates/mcp/tests/it/batch_budget.rs` | implemented |
| 23 | UI holds at most 16 live video decoders; a refused video plays sound only and retries on its next play or seek | `crates/ui-egui/src/media.rs` (`MAX_VIDEO_FEEDS`, `new_feed`) + tests | implemented |
| 24 | Undo memory accounting counts notes, comments, tags and kept XML | `crates/engine/src/lib.rs` (`text_cost`, `comments_cost`, `slide_extra_cost`) | implemented |
| 25 | 49 transitions / 107 animations (24/17/23/40/3) | `TRANSITIONS`, `ANIMATIONS` in `crates/model/src/anim.rs` (unchanged file) | implemented |
| 26 | 8 themes x 4 variants / 11 layouts + `Custom` / 183 presets in 9 categories / 40 warps / 70 icons | `crates/model/src/theme.rs`, `LayoutType` in `crates/model/src/lib.rs`, `crates/geom/src/{preset/catalog,warp}.rs`, `crates/engine/src/icon_data.rs` | implemented |
| 27 | 28 chart types / 45-9-17 SmartArt / 6 starters / 48-54 patterns / 13 date formats | `crates/model/src/chart.rs::ChartType`; `crates/engine/src/cmd/smartart.rs::{LAYOUTS,STYLES,COLORS}`; `crates/engine/src/templates.rs`; `crates/ui-egui/src/panels/fillui.rs`; `crates/engine/src/cmd/insert/text_fields.rs::DATE_FORMATS` | implemented |
| 28 | English only, no string catalogue | no `locales/` directory, no i18n crate or dependency in `Cargo.toml` | not implemented (verified absent) |
| 29 | No `.ppt`/`.odp`/macros/password/MP4 export; PDF artwork raster; SVG not drawn | `crates/engine/src/cmd/file.rs::open_other`; `crates/pdf/src/lib.rs`; `crates/engine/src/cmd/insert/picture.rs` (accepts `image/svg+xml`, no decoder) | not implemented (verified absent) |
| 30 | Media formats unchanged but Opus/Ogg/MP4/MOV/Matroska now come from craft-libs | `crates/media/Cargo.toml` (craft-media, craft-audio `opus-decode`); `Cargo.toml` pins `75895c03…`; `docs/architecture.md` status row | implemented |
| 31 | Spelling: compound tails memoised, affix counts bounded, aliased dictionaries share a parse, 256-language cache | `crates/engine/src/spell.rs` (`compounded(..., failed)`, `MAX_CACHED_LANGS`, `by_files`) | implemented |
| 32 | Log lines escape control characters and mark continuation lines | `apps/deckcraft/src/logging.rs::format_line` + tests | implemented |
| 33 | Updates report installing/ready/installed/failed and install at exit; Flatpak grants the updater host access | `crates/ui-egui/src/dialogs/updates_ui.rs`, `apps/deckcraft/src/main.rs::on_exit` calling `start_pending_update`, `packaging/linux/flatpak/*.yml` (`--talk-name=org.freedesktop.Flatpak`) | implemented |
| 34 | Table cell commands refuse malformed `cells` and out-of-table cells (≤100 000) | `crates/engine/src/cmd/table.rs::cell_param`, `target_cells`, `MAX_CELLS` | implemented |
| 35 | `slide.reuse` scales content to the destination size and imports custom table styles | `crates/engine/src/cmd/reuse.rs::scale_shapes`/`scale_master`/`import_table_styles` | implemented |

## 2. Automation-surface counts: v0.16.0 → v0.18.1

| Surface | v0.16.0 | v0.18.1 | Change |
|---|---:|---:|---|
| Engine commands | 329 | **329** | unchanged |
| `cmd!` sites | 329 | **329** | unchanged |
| Command kinds (ordinary/noundo/query) | 234/57/38 | **234/57/38** | unchanged |
| Engine shortcuts | 57 | **57** | unchanged (56 distinct strings; `Cmd+Shift+V` twice) |
| UI commands | 52 | **52** | unchanged (15 with shortcuts) |
| Control methods | 25 (+2 aliases) | **25 (+2)** | unchanged (27 accepted strings) |
| MCP tools | 25 | **25** | unchanged names |
| CLI subcommands | 12 | **12** | unchanged |
| Transitions | 49 | **49** | unchanged |
| Animations | 107 | **107** | unchanged |
| Chart types | 28 | **28** | unchanged (7 `chartEx` + `RegionMap`) |
| SmartArt / starters / icons / warps / patterns | 45-9-17 / 6 / 70 / 40 / 48-54 | same | unchanged |
| Themes x variants / layouts | 8x4 / 11+`Custom` | same | unchanged |
| Shape presets (9 categories) | 183 | **183** | unchanged |
| 3-D presets | 28-62 / 12 / 12 / 15 | same | unchanged |
| Date/time formats | 13 | **13** | unchanged |
| UI languages | 1 | **1** | unchanged |
| Workspace crates | 24 | **20** | −4 (`opus`, `ogg`, `isobmff`, `matroska`) |
| craft-libs pin | `c5a1cbfb…` (+ web `2e2312dd…`) | `75895c03…` (media/audio), `6e03f65b…` (pdf/update/ui), web `fd5e2fef…` | moved |

## 3. Re-measured vs carried forward

- **Re-measured at v0.18.1 (2026-11-12):** every row of §2. Command ids and kinds and MCP tool names
  were extracted at both tags with the same parser and diffed; the other registries were re-read at
  `HEAD` and their files are unchanged between the tags (`git diff --stat v0.16.0..HEAD` lists none
  of `crates/model/src/anim.rs`, `crates/model/src/theme.rs`, `crates/model/src/lib.rs`,
  `crates/geom/src/preset/catalog.rs`, `crates/geom/src/warp.rs`, `crates/engine/src/icon_data.rs`,
  `crates/engine/src/cmd/smartart.rs`, `crates/engine/src/templates.rs`,
  `crates/ui-egui/src/panels/fillui.rs`, `crates/ui-egui/src/lib.rs`,
  `apps/deckcraft-cli/src/help.rs`, `crates/ui-egui/src/control.rs`). The workspace crate count and
  the craft-libs pins were read from `crates/` and `Cargo.toml` at `HEAD`.
- **Carried forward after re-reading the code:** file-format bounds (PNG scale clamp 0.01–16, GIF
  16–3840 px / 0.1–600 s / ≤500 frames / ≤200M pixels, PDF dpi clamped 36–600 and 64M-pixel raster
  cap, native 256 MiB manifest / 2 GiB per entry / 4 GiB total / 100 000 items), the media codec
  lists, MCP protocol revisions (2025-06-18, also 2025-03-26 and 2024-11-05) and the 16 MiB MCP
  frame/reply caps, and the slide-show key map. All were checked at `HEAD` and no number moved.
- **Carried forward unverified:** the v0.15.0→v0.16.0 and v0.14.1→v0.15.0 delta paragraphs. This
  checkout no longer carries the `v0.15.0` tag, so those ranges cannot be re-diffed here; they are
  history and are labelled as carried in `SKILL.md`.
- **Confirmed rather than corrected:** animations stay **107** and shape presets stay **183** — a
  naive line count still reports 106 and 182 because `customPath` and `accentBorderCallout3` are
  each written across several lines.
- **Corrected in this round:** workspace "24 crates" → **20**; the media implementation note (Opus,
  Ogg, MP4/MOV, Matroska now craft-libs) replaces "pure-Rust decoders in `crates/media`,
  `crates/opus`"; `shape.adjust`/`quickStyle` index handling is now strict; `format.paragraph` no
  longer silently left-aligns an unknown align; a chart's round-trip behaviour past the budgets is
  new.

## 4. Uncertain / not verified

- No live command registry: `deckcraft-cli` is not installed on this machine and is not inside the
  `.app`, so every count is parsed from code, not read back from `deckcraft-cli commands`. Only the
  app binary's `--version`/`--help` were executed.
- GUI behaviour was not exercised (no window was opened). Presenter, slide-show, clipboard, updater
  and web-page behaviour is code and documentation evidence.
- The web `window.deckcraft` API was not called in a browser; the 30 s timeout and 64 in-flight cap
  come from `packaging/web/README.md` and the shared craft-libs `web-api` crate README, which was
  not audited in depth.
- PPTX fidelity on real corporate decks remains unmeasured by the project (`docs/gaps.md`).
- External image paste on Windows (#1414) is still open and was not tested here.

## 5. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `docs/architecture.md` "202k lines of Rust in 24 crates" and "320 commands" | 20 crates and 329 commands |
| `docs/control-protocol.md` "16 MiB per request line" | 256 MiB (`apps/deckcraft/src/control_server.rs::Limits::default`) |
| `docs/animation-parity.md` "14 exit effects" | 23 (`crates/model/src/anim.rs::ANIMATIONS`) |
| `docs/target-app-parity.md` "the registry is 328"; `ROADMAP.md` "226 commands" | 329 |
| `docs/mcp.md` `batch` description | omits the 1 000-command / 64 MiB caps (`crates/mcp/src/{tools,server}.rs`) |
| `format.align` parameter doc "left\|center\|right\|justify\|justifyLow\|distributed" | also accepts `thaiDist`; `format.paragraph` accepts `centre`/`justifyLow` too |
| `docs/gaps.md` SmartArt counts | 45 layouts / 9 styles / 17 colour sets |
| `docs/gaps.md` #74 media playback options | still open but narrower: trim/fades/bookmarks and show-media-controls round-trip |

## 6. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # 7cc73ab1895ed2e30c8afbcada20c70b9ea0a440
git -C <clone> diff --shortstat v0.16.0..HEAD                   # 121 files changed, 2939 insertions(+), 7950 deletions(-)
grep -rho 'cmd!' crates/engine/src/cmd/ --include='*.rs' | wc -l  # 329
grep -rho 'noundo "' crates/engine/src/cmd/ | wc -l                # 57 noundo
grep -rho 'query "'  crates/engine/src/cmd/ | wc -l                # 38 query
awk '/pub const UI_COMMANDS/,/^\];/' crates/ui-egui/src/lib.rs | grep -cE '^    (\(|")'  # 52
grep -cE '^\s+tool\(' crates/mcp/src/tools.rs                   # 25
grep -oE 'name: "[a-z-]+"' apps/deckcraft-cli/src/help.rs | sort -u | wc -l  # 12
awk '/pub static TRANSITIONS/,/^\];/' crates/model/src/anim.rs | grep -cE '^\s+\("'   # 49
awk '/pub static ANIMATIONS/,/^\];/' crates/model/src/anim.rs | grep -c 'AnimClass::'  # 107
awk '/pub static CATALOG/,/^\];/' crates/geom/src/preset/catalog.rs | grep -c 'p!('     # 183
awk '/pub const CATALOG/,/^\];/' crates/geom/src/warp.rs | grep -c 'Preset { id:'       # 40
grep -c 'Icon {' crates/engine/src/icon_data.rs                  # 70
ls -d crates/*/ | wc -l                                          # 20 crates
<DeckCraft.app>/Contents/MacOS/DeckCraft --version               # deckcraft 0.18.1
```

The counts in §2 were produced by a small Python parse of the same sites (`cmd!` id literals with
their kind prefix at both tags, `tool(` name literals at both tags, the `match req.method` arms,
the `UI_COMMANDS` tuple starts, the CLI `SUBCOMMANDS` names, and each `pub static`/`pub const`
registry between its declaration and its closing `];`), run against `HEAD`; the shell forms above
are the reproducible equivalents for a spot check.
