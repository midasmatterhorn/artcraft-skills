# DeckCraft — evidence ledger (tag v0.16.0)

Audit basis: this checkout is tag **`v0.16.0`**, commit **`a3e2254d3de32ed1718f156f070b54a34b949b54`**
— `git rev-parse HEAD` in the pinned checkout confirms, and the tag `v0.16.0` points at it. The clone
is shallow and squashed (one `Release 0.16.0` commit), so the tag-to-tag diff, not the commit list, is
the evidence for the delta. Inspection date **2026-11-07**. The installed DeckCraft bundle prints
`deckcraft 0.16.0` (bundle `ai.storyteller.deckcraft`, version 0.16.0, universal, notarized and
stapled); it matches the tag. The GUI was never launched; only `--version` and `--help` were run, and
both exit before eframe starts (`apps/deckcraft/src/main.rs::main` handles `Startup::Help`/`Version`
first).

v0.15.0 → v0.16.0: **144 files changed, +6 733/−717** (`git diff --shortstat v0.15.0..HEAD`). No id set
moved: 329 command ids, 57 engine shortcuts, 52 UI commands, 12 CLI subcommands, 25 control methods
(+2 aliases), 25 MCP tools, 49 transition rows, 107 animation entries, 8 themes, 11 layouts + `Custom`,
183 shape presets, 28 chart types, 45/9/17 SmartArt, 6 starters, 70 icons, 40 warps, 48/54 pattern
fills, 28/62 3-D cameras, 12 bevels, 12 materials, 15 light rigs — identical at both tags. The delta is
behaviour: `file.save` refuses image formats, stricter parameter validation (`file.export` `perPage`,
`view.slideMaster`, table `cells`, `comment.next`/`prev`, `shape.connect`), `shape.flip` refused on
SmartArt, custom-show pruning on slide delete, scaled `slide.reuse` with custom table styles, outline
placeholder omission, evaluated PDF text fields, a 256 MiB native manifest cap, a renamed hidden save
sibling checked against the write root, a large PPTX round-trip set, the restored system clipboard,
a previous-slide transition preview, See All Slides in the presenter window, and the web `?host=parent`
bridge.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 329 engine commands, ids unique, 329 `cmd!` sites (identical set at `v0.15.0`) | `crates/engine/src/cmd/*.rs` `cmd!(` extraction; `git diff` of the id sets between tags = 0 added, 0 removed | implemented |
| 2 | Kind split 234 ordinary / 57 `noundo` / 38 `query` | `cmd!`, `cmd!(noundo …`, `cmd!(query …` counts over the same sites | implemented |
| 3 | 57 commands carry a shortcut; 56 distinct strings; one collision (`Cmd+Shift+V`) | shortcut argument of each `cmd!`; `edit.pasteText` and `format.painterApply` both declare it | implemented |
| 4 | 52 `UI_COMMANDS` rows, 15 with shortcuts | `crates/ui-egui/src/lib.rs` `UI_COMMANDS` tuple starts (50 single-line + 2 multi-line) | implemented |
| 5 | 25 MCP tools, set identical to v0.15.0 | `tool(` name arguments in `crates/mcp/src/tools.rs`; name diff between tags empty | implemented |
| 6 | 25 control methods + aliases `ui.menu.invoke`, `command` | top-level arms of `match req.method.as_str()` in `crates/ui-egui/src/control.rs`; diff between tags empty | implemented |
| 7 | 12 CLI subcommands | `SUBCOMMANDS` in `apps/deckcraft-cli/src/help.rs`; `apps/deckcraft-cli/` has no diff between tags | implemented |
| 8 | `file.save` refuses `.png`/`.jpg`/`.jpeg` | `crates/engine/src/cmd/file.rs::save_bytes` returns "saving a presentation as a single image isn't supported; use file.export"; `format_for_path` still maps the extensions, so the refusal is at encode time | implemented |
| 9 | `file.export` handout `perPage` must be 1/2/3/4/6/9 | `crates/engine/src/cmd/file.rs::pdf_options` (`opt_usize_param` + list check) | implemented |
| 10 | `view.slideMaster` rejects invalid `master`/`layout` | `crates/engine/src/cmd/design/master_view.rs` (`opt_usize_param`, `crates/engine/src/cmd.rs:323`) | implemented |
| 11 | Table commands refuse malformed `cells` and out-of-table cells (≤100 000) | `crates/engine/src/cmd/table.rs::cell_param`, `target_cells`, `MAX_CELLS` | implemented |
| 12 | `shape.flip` refused on SmartArt | `crates/engine/src/cmd/shape/size.rs::flip` walks the tree for `diagram` | implemented |
| 13 | `shape.connect`/`shape.sites` reach grouped shapes; unknown id is an error | `crates/engine/src/cmd/shape/freeform.rs`, `crates/engine/src/connect.rs::sites_of` | implemented |
| 14 | `comment.next`/`comment.prev` reject a malformed `index` with no selection change | `crates/engine/src/cmd/review.rs::neighbour` + its test | implemented |
| 15 | Deleting a slide prunes custom shows, undoably | `crates/engine/src/cmd/slide.rs::delete` + `deleting_slide_prunes_every_custom_show_in_one_undo_step` | implemented |
| 16 | `slide.reuse` scales content to the destination size and imports custom table styles | `crates/engine/src/cmd/reuse.rs::scale_shapes`/`scale_master`/`import_table_styles` + tests | implemented |
| 17 | Outlines (txt/md), RTF and the outline view omit footer/date/slide-number placeholders | `crates/format/src/lib.rs::slides_to_outline`, `crates/format/src/rtf.rs::slides_to_rtf`, `crates/ui-egui/src/sorter.rs` | implemented |
| 18 | PDF text layer uses evaluated field values and one clock reading | `crates/pdf/src/lib.rs` (`run.content()`, `RenderOpts { now }`, `place_slide_with`) | implemented |
| 19 | Native `presentation.json` capped at 256 MiB; notes page clamped to slide-size bounds | `crates/format/src/lib.rs` (`MAX_MANIFEST`, `SLIDE_SIDE`) | implemented |
| 20 | Save writes a hidden `.deckcraft.<pid>.<n>.saving`, checked against the write root | `crates/engine/src/io.rs::write_file` + tests | implemented |
| 21 | PPTX round-trips text overflow, `compatLnSpc`, `normalizeH`, `thaiDist`, point-sized bullets, RTL tables, `altLang`, reflection transforms, hidden media controls, parent-delay placement | `crates/model/src/{text,style,table,anim}.rs`; `crates/pptx/src/{read,write}/{dml,shapes,timing}.rs`, `crates/pptx/src/{read,write}.rs` | implemented |
| 22 | Desktop Ctrl+C/X/V use the system clipboard again | `apps/deckcraft/Cargo.toml` adds eframe's `clipboard` feature; `crates/ui-egui/src/app/clipboard.rs` (browser Copy Image handling) | implemented |
| 23 | Transition Preview plays from the previous slide; See All Slides opens in the presenter window | `crates/ui-egui/src/show.rs::start_transition_preview`; `crates/ui-egui/src/presenter.rs` (`grid`, `Command::Goto`) | implemented |
| 24 | Web build has a same-origin host bridge (`?host=parent`, `data-host="page"`, `&author=`) | `apps/deckcraft-web/src/host.rs`; `craft-web-host` pin in `apps/deckcraft-web/Cargo.toml` | implemented |
| 25 | 49 transitions / 107 animations (24/17/23/40/3) | `TRANSITIONS`, `ANIMATIONS` in `crates/model/src/anim.rs`; rows counted at both tags | implemented |
| 26 | 8 themes × 4 variants / 11 layouts + `Custom` / 183 presets in 9 categories / 40 warps | `crates/model/src/theme.rs::builtin_themes`/`theme_variants`; `LayoutType` in `crates/model/src/lib.rs`; `CATALOG` in `crates/geom/src/preset/catalog.rs`; `CATALOG` in `crates/geom/src/warp.rs` | implemented |
| 27 | 28 chart types / 45-9-17 SmartArt / 6 starters / 70 icons / 48-54 patterns / 13 date formats | `crates/model/src/chart.rs::ChartType`; `crates/engine/src/cmd/smartart.rs::{LAYOUTS,STYLES,COLORS}`; `crates/engine/src/templates.rs`; `crates/engine/src/icon_data.rs`; `crates/ui-egui/src/panels/fillui.rs`; `crates/engine/src/cmd/insert/text_fields.rs::DATE_FORMATS` | implemented |
| 28 | English only, no string catalogue | no `locales/` directory, no i18n crate or dependency in `Cargo.toml`; `docs/gaps.md` states it | not implemented (verified absent) |
| 29 | No `.ppt`/`.odp`/macros/password/MP4 export; PDF raster artwork; SVG not drawn | `crates/engine/src/cmd/file.rs::open_other`; `crates/pdf/src/lib.rs`; `crates/engine/src/cmd/insert/picture.rs` (accepts `image/svg+xml`, no decoder) | not implemented (verified absent) |
| 30 | The #74 media-playback set is still lost (volume, autoplay, loop, media rewind, play-across-slides, hide-while-not-playing, full screen); trim, fades, bookmarks and show-media-controls round-trip; animation rewind round-trips | `crates/model/src/lib.rs::MediaClip` vs `crates/pptx/src/write/shapes.rs`; `docs/gaps.md` #74; `crates/pptx/src/{read,write}/timing.rs` (`fill="remove"`) | partial |

## 2. Automation-surface counts: v0.15.0 → v0.16.0

| Surface | v0.15.0 | v0.16.0 | Change |
|---|---:|---:|---|
| Engine commands | 329 | **329** | unchanged |
| `cmd!` sites | 329 | **329** | unchanged |
| Command kinds (ordinary/noundo/query) | 234/57/38 | **234/57/38** | unchanged |
| Engine shortcuts | 57 | **57** | unchanged (56 distinct strings; `Cmd+Shift+V` twice) |
| UI commands | 52 | **52** | unchanged; the published v0.15.0 skill's 51 was a miscount |
| Control methods | 25 (+2 aliases) | **25 (+2)** | unchanged; the published skill's "26 names" matched neither count |
| MCP tools | 25 | **25** | unchanged |
| CLI subcommands | 12 | **12** | unchanged |
| Transitions | 49 | **49** | unchanged |
| Animations | 107 | **107** | unchanged (107 rows; `customPath` is written multi-line) |
| Shape presets (9 categories) | 183 | **183** | unchanged (183 `p!(` rows; one is written multi-line) |
| Themes × variants / layouts / charts / SmartArt / starters / icons / warps / patterns / 3-D | 8×4 / 11+Custom / 28 / 45-9-17 / 6 / 70 / 40 / 48-54 / 28-62-12-12-15 | same | unchanged |
| UI languages | 1 | **1** | unchanged |
| craft-libs pin | `c5a1cbfb…` | **`c5a1cbfb…`** | unchanged (web app adds `craft-web-host` at `2e2312dd…`) |

## 3. Re-measured vs carried forward

- **Re-measured at v0.16.0 (2026-11-07):** every row of §2 — engine command ids and kinds, shortcuts and
  the collision, UI commands, control methods, MCP tools, CLI subcommands, transitions, animations,
  themes and variants, layouts, shape presets per category, charts, SmartArt, starters, icons, warps,
  pattern gallery/names, 3-D camera/bevel/material/light sets, date formats, and the absence of a
  locale catalogue. Each was parsed from the registry named in §1 at `HEAD` and again at `v0.15.0` with
  the same script; the two extractions were diffed, which is how "unchanged" is known rather than
  assumed.
- **Carried forward after re-reading the code:** the file-format bounds (PNG scale clamp, GIF 16–3840 px
  / 0.1–600 s / ≤500 frames / ≤200M pixels, PDF dpi 200 clamped 36–600 and the 64M-pixel raster cap,
  native load budgets other than the new manifest cap), the media codec lists, and the MCP protocol
  revisions/resources — all re-read at `HEAD` and found unchanged, so no number moved.
- **Carried forward unverified:** the previous round's v0.14.1→v0.15.0 delta and its `ee39ff6` base —
  this shallow clone carries only the `v0.15.0` and `v0.16.0` tags, so that range cannot be re-diffed here.
- **Confirmed rather than corrected:** animations stay **107** and shape presets stay **183** — a naive
  line count reports 106 and 182 because one row in each registry (`customPath`, `accentBorderCallout3`)
  is written across several lines.
- **Corrected in this round:** UI commands 51 → **52**; control methods "26 names" → **25 (+2 aliases)**; command-id note
  "234 ids / 306 `cmd!` sites" → **329 ids / 329 sites** (234 was the ordinary-kind subset); media
  "#77 animation rewind not written back" → animation rewind **does** round-trip, and the #74 media gap
  is narrower than stated (trim, fades, bookmarks, show-media-controls now round-trip); `perPage` "1–9 clamped" → **1/2/3/4/6/9 only**; `file.save` image trap "writes zip
  bytes" → **refused**; `.saving` sibling name → **`.deckcraft.<pid>.<n>.saving`**; automation roots
  "a repeated flag is an error" → **both flags and both spellings repeat**.

## 4. Uncertain / not verified

- No live command registry: `deckcraft-cli` is not installed on this machine and is not inside the
  `.app`, so every count is parsed from code, not read back from `deckcraft-cli commands`. The
  installed app's `--version`/`--help` were the only executions.
- GUI behaviour was not exercised (no window was opened). Presenter, slide-show and clipboard behaviour
  is code and documentation evidence plus the ROADMAP/gaps notes.
- PPTX fidelity on real corporate decks remains unmeasured by the project (`docs/gaps.md`).
- External image paste on Windows (#1414) is still open and was not tested here.

## 5. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `docs/control-protocol.md` "16 MiB request line" | 256 MiB (`apps/deckcraft/src/control_server.rs::Limits::default`) |
| `docs/animation-parity.md` "14 exit effects" | 23 (`crates/model/src/anim.rs::ANIMATIONS`) |
| `docs/architecture.md` "320 commands"; `docs/target-app-parity.md` "the registry is 328" | 329 |
| `ROADMAP.md` "226 commands at d556ff9" | 329 now (the note says it was not re-measured) |
| `format.align` parameter doc "left\|center\|right\|justify\|justifyLow\|distributed" | also accepts `thaiDist` (`crates/engine/src/cmd/format/paragraph.rs`) |
| `docs/gaps.md` SmartArt counts | 45 layouts / 9 styles / 17 colour sets |
| `docs/gaps.md` #74 "media playback options" | still open, but narrower: trim/fades/bookmarks and the show-media-controls flag round-trip (`crates/pptx/src/write/shapes.rs`, `crates/pptx/src/write.rs`) |

## 6. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # a3e2254d3de32ed1718f156f070b54a34b949b54
git -C <clone> diff --shortstat v0.15.0..HEAD                   # 144 files changed, 6733 insertions(+), 717 deletions(-)
grep -rho 'cmd!' crates/engine/src/cmd/ --include='*.rs' | wc -l  # 329
grep -rho 'noundo "' crates/engine/src/cmd/ | wc -l                # 57 noundo
grep -rho 'query "'  crates/engine/src/cmd/ | wc -l                # 38 query (the rest of 329 are ordinary)
awk '/pub const UI_COMMANDS/,/^\];/' crates/ui-egui/src/lib.rs | grep -cE '^    (\(|")'  # 52
grep -cE '^\s+tool\(' crates/mcp/src/tools.rs                   # 25
grep -c 'name: "' apps/deckcraft-cli/src/help.rs                # 12 subcommands
awk '/pub static TRANSITIONS/,/^\];/' crates/model/src/anim.rs | grep -cE '^\s+\("'   # 49
awk '/pub static ANIMATIONS/,/^\];/' crates/model/src/anim.rs | grep -c 'AnimClass::'  # 107
awk '/pub static CATALOG/,/^\];/' crates/geom/src/preset/catalog.rs | grep -c 'p!('     # 183
awk '/pub const CATALOG/,/^\];/' crates/geom/src/warp.rs | grep -c 'Preset { id:'       # 40
grep -c 'Icon {' crates/engine/src/icon_data.rs                  # 70
<DeckCraft.app>/Contents/MacOS/DeckCraft --version                # deckcraft 0.16.0
```

The counts in §2 were produced by a small Python parse of the same sites (`cmd!` id literals with
their kind prefix, `tool(` name literals, the `match req.method` arms, the `UI_COMMANDS` tuple starts,
and each `pub static`/`pub const` registry between its declaration and its closing `];`), run against
both tags; the shell forms above are the reproducible equivalents for a spot check.
