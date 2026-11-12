# PhotoCraft — evidence ledger (tag v0.23.1)

Audit basis: this checkout is tag **`v0.23.1`**, commit **`45066c48292e92229ada3459a83453439514c83d`** ("Merge tested main for v0.23.1", 2026-11-11), inspected 2026-11-12. The installed bundle matches: `Contents/MacOS/PhotoCraft --version` prints `photocraft 0.23.1 (45066c482, 2026-11-12)` and `Contents/MacOS/photocraft-cli --version` prints `photocraft-cli 0.23.1 (45066c482, 2026-11-12)`; `Contents/Info.plist` says 0.23.1 and bundle id `ai.storyteller.photocraft`. The GUI was never launched; the CLI was run read-only.

Previous pin for the delta: **v0.21.0** = `efb7ebd0c0dab1fc108ee4642aa47c22694271a8`, still reachable in this shallow checkout, so every "was" number below was counted at both tags with one method (`git show v0.21.0:<path>`). No `references/` directory ships — SKILL.md carries the body, this file carries the per-claim evidence.

## 1. Capability claims → evidence → tier

Tier legend: **implemented** = code path exists and is wired into UI/CLI/automation; **partial** = code exists with a named gap; **claimed-only** = said in docs/README but absent or contradicted by code.

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 664/664 Photoshop menu items dispatch a command | `docs/parity-checklist.md:5`; guard `FLOOR = 663` at `crates/ui-egui/src/menus/parity.rs:10` (a lower bound, one behind the generated count) | implemented |
| 2 | 69 tools; Star is the new one | `crates/ui-egui/src/state/tool.rs:74` `Star` (shape flyout's Star Tool, live polygon with star ratio), `:84` `pub const ALL: [Tool; 69]` | implemented |
| 3 | 16 adjustment-layer kinds, each also a destructive `image.adjustments.*` command | `crates/engine/src/cmd.rs:1209` `const ADJ` (16 tuples); `photocraft-cli commands \| grep -c '^layer\.newAdjustmentLayer\.'` = 16, `^image\.adjustments\.` = 23 (22 kinds + `image.adjustments.colorLookup.list`) | implemented |
| 4 | 10 layer-effect kinds | `crates/doc/src/effects.rs` `pub enum Effect`; `crates/engine/src/layer_style.rs` | implemented |
| 5 | 34 blend modes (PassThrough + 27 PS + 6 Paint.NET) | `crates/color/src/blend.rs` `pub enum BlendMode` | implemented |
| 6 | 124 live `filter.*` ids = 47 gallery + 64 pairwise + 13 workspace/lifecycle | `photocraft-cli commands \| grep -c '^filter\.'` = 124, `^filter\.gallery\.` = 47, `^filter\.blurGallery\.` = 5, 8 single-token ids → 13; remainder pairwise | implemented |
| 7 | PDF import: every page becomes one raster artboard | `crates/io/src/pdf_import.rs` (module doc; `MAX_PAGES: usize = 16` at `:51`, `MAX_UNION_PIXELS` 200 M at `:55`, 2 GiB default pixel budget at `:58`); routed at `crates/io/src/lib.rs:571`; live: `convert probe.pdf probe.pcraft --pdf-dpi 96` → one artboard group holding one pixel layer | implemented (raster) |
| 8 | Experimental editable PDF import (paths → shape layers, embedded-font text → text layers), per-page raster fallback with a warning | `crates/io/src/pdf_editable.rs` module doc; feature `pdf-editable` (`crates/io/Cargo.toml:21`) enabled only by `apps/photocraft-cli/Cargo.toml:36`; live `--pdf-editable` printed the font-change warning | partial (experimental, CLI-only) |
| 9 | PDF import options are not in the GUI: `file.open` passes `ImportOptions::default()` (300 DPI, all pages, raster) | `crates/engine/src/cmd/file_cmds/open.rs:41`; CLI-only fields at `crates/io/src/lib.rs:622-631`, set in `apps/photocraft-cli/src/document.rs:49-55` | implemented (CLI-only knobs) |
| 10 | `.ai` files that start with `%PDF-` take the PDF importer | `crates/io/src/lib.rs:571` comment and `pdf_import::is_pdf`; `an_ai_with_pdf_content_takes_the_pdf_importer` test at `crates/io/src/lib.rs:1648` | implemented |
| 11 | PDF write stays one flattened page, spot channels as overprinting `/Separation` plates, `pdfSpotPlates: false` leaves them out | `crates/io/src/pdf.rs` module doc; `crates/engine/src/cmd/file_cmds.rs` save params | implemented |
| 12 | 23 codec formats; PCX/XPM/DICOM read-only, JPEG XL export-only, AVIF write-only (feature), HEIF read-only (feature) | `crates/codecs/src/format.rs:110` `ALL: [Format; 23]`; `ASYMMETRIC_EXCEPTIONS` at `:75`; `Format::Avif`/`Jxl` caps at `:279`/`:287` | implemented |
| 13 | HEIC decoding now comes from the shared `craft-heif` crate; `crates/heif` is deleted | `Cargo.toml` workspace dependency `craft-heif` (rev `081078bb…`); `crates/codecs/Cargo.toml` `heif = ["dep:craft-heif"]`; `git diff --name-status v0.21.0..HEAD` shows `D crates/heif/*` | implemented |
| 14 | Import-only layered readers: PDN, KRA/KRZ, XCF/XCF.GZ, Affinity, SVG; writable targets refused | `crates/io/src/lib.rs` `import_stages`/`export_stages` | implemented |
| 15 | PSD/PSB read+write with enforced corpus floors 148/170, 249/309, 190/258 | `crates/io/tests/it/corpus.rs:151,155,159`; totals grew one file each for io and psd-tools, floors unchanged | implemented, fidelity partial (G1) |
| 16 | Camera raw: DNG (incl. lossy and JPEG XL), CR2, TIFF/EP, Nikon NEF, Sony cRAW, RW2, ORF, Fujifilm RAF (now compressed too), Hasselblad 3FR/FFF; CR3 preview only | `crates/raw/src/lib.rs` module doc ("decoded today" list) and `mod rafc`, `mod hasselblad`; CR3 decision in `docs/gaps.md` G14 | implemented (partial: CR3) |
| 17 | Camera Raw `.xmp` sidecars load/auto-fill/save, and a sidecar's crop crops the opened raw | `crates/io/src/camera_raw_xmp.rs`; `docs/file-format-parity.md` change note 2026-11-08 | implemented |
| 18 | `file.openAsSmartObject` opens a file as one embedded smart-object layer in a new untitled document | `crates/engine/src/cmd/file_cmds/open_as_smart_object.rs`; id at `crates/engine/src/cmd/file_cmds.rs:299`; live in `photocraft-cli commands` | implemented |
| 19 | `layer.copyCSS` writes Photoshop-shaped CSS for the selected layers | `crates/engine/src/cmd/layer_css_cmds.rs:38` `ID: &str = "layer.copyCSS"` (module doc lists written and unwritten properties) | implemented |
| 20 | `layer.layerMask.moveTo` moves a layer mask to another layer/group, copy or replace | `crates/engine/src/cmd.rs:831`; `crates/engine/src/cmd/ops.rs:104` | implemented |
| 21 | `path.intersectWithSelection` joins the add/subtract/intersect path-to-selection trio | `crates/engine/src/cmd/vector_cmds.rs:235`; test at `crates/engine/src/cmd/vector_cmds/tests.rs:578` | implemented |
| 22 | 27 `actions.*` ids, including Menu Item, Insert Menu Item, Insert Path, Record Again, Allow Tool Recording, Duplicate Action | `photocraft-cli commands \| grep -c '^actions\.'` = 27; `crates/engine/src/cmd/atn_cmds/menu_item.rs:33`; `crates/engine/src/cmd/actions_edit_cmds.rs:31,128,413,433`; `crates/engine/src/cmd/actions_edit_cmds/insert_path.rs` | implemented |
| 23 | 206 rows in the `.atn` `EVENTS` table (109 macro rows + 97 `Event {` literals; 204 at v0.21.0) | `crates/engine/src/cmd/atn_cmds/events.rs:390`; counted with the row pattern in §5 at both tags | implemented |
| 24 | Wasm plug-in ABI v1 only: 5 commands, wasmi sandbox, no WASI/fs/net/clock, 32 MiB module, 512 MiB memory, 50 M instructions + 4,000 per sample, 60 s | `crates/plugins/src/runtime.rs:14` `ABI_VERSION: i32 = 1`; `docs/plugins.md` limits table; `plugin.{list,install,remove,reload,run}` | implemented |
| 25 | Automation is fail-closed for the same 14 filesystem commands; desktop additionally refuses `image.mode.*` | `crates/automation/src/workspace/tests.rs:644` `filesystem_commands_fail_closed` (14 ids) | implemented |
| 26 | One command registry drives UI, CLI, control channel and MCP | `crates/engine/src/cmd.rs` `fn build()`; `docs/parity-checklist.md` generated from the same registry | implemented |
| 27 | Bridge authentication offers `auth.challenge` (HMAC-SHA256 over both nonces) and still accepts the legacy `auth {token}` frame | `crates/automation/src/security.rs:20` `CHALLENGE_METHOD`, `:136-161` proof roles, `:185` `ServerHandshake`; `docs/control-protocol.md` "Challenge authentication" | implemented |
| 28 | Multiple ordered read roots; one write root | `crates/automation/src/args.rs` (`Vec<PathBuf>`), `crates/automation/src/workspace.rs:49` `with_read_roots`; `docs/mcp.md` semantics (first existing file, only a miss falls through) | implemented |
| 29 | 35 UI languages, catalogs in storytold/craft-i18n | `crates/ui-egui/src/i18n.rs:90` `LANGUAGE_COUNT: usize = 35`, `:94` `LANGUAGES`; `craft-i18n.rev` (`e02939ef…`); `crates/ui-egui/build.rs` `CRAFT_I18N_DIR` | implemented (engine messages English; Hindi partial) |
| 30 | Raw workspace is named RAW Develop while the ids stay `filter.cameraRaw` | `docs/feature-names.md`; `crates/ui-egui/src/menu_catalog.rs:574` "RAW Develop Filter…", `:171` "RAW Defaults…" | implemented |
| 31 | Puppet Warp PSD smart filter maps both ways (mesh imported, template kept) | `crates/io/src/puppet_map.rs` module doc; `docs/file-format-parity.md` 2026-11-08 note | implemented |
| 32 | Print through in-process IPP, Linux portal, Windows spooler or PDF | `crates/engine/src/cmd/print_cmds.rs`; `crates/ipp`; `docs/printing.md` | implemented |
| 33 | Startup self-update prompt; no periodic recheck while open | `crates/engine/src/cmd/updates_cmds.rs`; craft-update pin; `docs/scorecard.md` DIST rows | implemented (no periodic recheck) |
| 34 | Dead preferences 8 of 199 | `docs/scorecard.md:215` (generated by the prefs audit); `docs/gaps.md` header still says 11 of 183 | implemented metric |

## 2. Automation-surface counts: v0.21.0 → v0.23.1

Every row was counted at both tags with the method named; sets were diffed **as sets**, not counts. The v0.23.1 figures are the current ones.

| Surface | v0.21.0 | v0.23.1 (measured) | Method |
|---|---:|---:|---|
| Engine commands (live) | 993 | **1009** | `"$CLI" commands \| wc -l` on the installed bundle |
| Photoshop menu items live | 660/660 | **664/664** | `sed -n '5p' docs/parity-checklist.md`; `FLOOR = 663` at `crates/ui-egui/src/menus/parity.rs:10` |
| Tools | 68 | **69** (+Star) | `[Tool; N]` at `crates/ui-egui/src/state/tool.rs:84`; `Tool::Star` at `:74` |
| Codec formats | 23 | **23 (unchanged)** | `[Format; 23]` at `crates/codecs/src/format.rs:110` |
| `filter.*` live ids | 124 | **124 (unchanged)** | `commands \| grep -c '^filter\.'`; prefix split |
| `actions.*` live ids | 21 | **27** | `commands \| grep -c '^actions\.'`; new ids in `crates/engine/src/cmd/actions_edit_cmds.rs`, `crates/engine/src/cmd/atn_cmds/menu_item.rs` |
| `.atn` event rows | 204 | **206** | macro rows + `Event {` literals inside `const EVENTS` (`events.rs:390`) |
| Adjustment-layer kinds | 16 | **16 (unchanged)** | `layer.newAdjustmentLayer.*` count = 16 |
| Layer effects | 10 | **10 (unchanged)** | `crates/doc/src/effects.rs` |
| Blend modes | 34 | **34 (unchanged)** | `pub enum BlendMode` variants |
| MCP tools / resources | 26 / 2 | **26 / 2 (unchanged)** | `grep -c '#\[tool(' crates/automation/src/server.rs`; `crates/automation/src/server/conventions.rs` |
| Control-channel methods | 28 | **28 (unchanged)** | `pub(super) const METHODS` at `crates/ui-egui/src/control.rs:186`, diffed: zero diff |
| Headless `serve` methods | 19 | **19 (unchanged)** | `pub const METHODS` at `crates/automation/src/rpc.rs:42`, diffed: zero diff |
| CLI subcommands / export flags | 8 / 12 | **8 / 14** | `enum Command`; `#[arg]` count in `ExportArgs` |
| Fail-closed filesystem commands | 14 | **14 (unchanged)** | `crates/automation/src/workspace/tests.rs:644` |
| Locale catalogs | 27 tsv files (non-English) | **34 non-English catalogs, 35 languages incl. English** | `LANGUAGE_COUNT` at `i18n.rs:90`; catalogs in craft-i18n at `craft-i18n.rev` |
| Dead preferences | 10 of 192 | **8 of 199** | `docs/scorecard.md:215` (generated) |
| Plug-in ABI | v1, 5 commands | **v1, 5 (unchanged)** | `ABI_VERSION` at `runtime.rs:14` |
| Corpus floors | 148/169, 249/308, 190/258 | **148/170, 249/309, 190/258** | `crates/io/tests/it/corpus.rs:151-159` (floors unchanged, totals +1 each) |
| Files changed in the delta | 276 (v0.20.1→v0.21.0) | **1347** | `git diff --name-only v0.21.0..HEAD \| wc -l`; `--stat` +140,005/−122,246 |

New command ids at v0.23.1 (live): `file.openAsSmartObject`, `layer.copyCSS`, `layer.layerMask.moveTo`, `path.intersectWithSelection`, `actions.menuItem`, `actions.insertMenuItem`, `actions.insertPath`, `actions.allowToolRecording`, `actions.recordAgain`, `actions.duplicate`. The other six of the sixteen-command growth are not literal id declarations in the modules scanned (generated rows account for them); the CLI total stays the authority.

## 3. Things that could not be verified (stated as uncertain in SKILL.md)

- **Exact engine command count.** Table macros expand per row; a static count of registration sites stays uncertain by a few dozen. Authoritative live count: `photocraft-cli commands | wc -l`.
- **PDF renderer bounds.** The 8192 px side / 64 M px page bounds come from `craft-pdf`'s `raster` module (external crate, read from its public API in `crates/io/src/pdf_import.rs:93`), not re-derived here; the importer's own limits (16 pages, 200 M union pixels, 2 GiB default budget) were read in this repo.
- **ROADMAP percentages** were measured at 0.6.0 and are not re-computed — never presented as current.
- **Open-issue counts** in `docs/gaps.md` G3 are dated checkpoints, not live data.
- **`.atn` "supported events"** has no single number: the code table has 206 rows, `docs/file-format-parity.md` quotes 145 supported event kinds, `docs/scorecard.md` AUTO-219-2 still says 90. Only the 206 was re-measured.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `docs/gaps.md` G10: "Photoshop PDF read" missing | PDF read landed 2026-11-07 (`docs/file-format-parity.md` row + `crates/io/src/pdf_import.rs`); the gaps file was last updated 2026-11-10 and did not fold it in |
| `docs/gaps.md` G6: "Missing (0 of 68)" tools | `Tool::Star` makes it 69 (`crates/ui-egui/src/state/tool.rs:84`) |
| `docs/gaps.md` header: "11 of 183 preferences do nothing" | `docs/scorecard.md:215`: 8 of 199 |
| `README.md` "500+ commands"; `docs/architecture.md` "~700" | live registry is 1009; use `photocraft-cli commands` |
| `crates/io/src/pdf_import.rs` module doc: "editable text and vector import … is not part of this importer" | `crates/io/src/pdf_editable.rs` exists behind the `pdf-editable` feature and is wired into `pdf_import.rs` (`opts.pdf_editable`); the comment predates it |
| `docs/localization-parity.md` summary: "2 absent (Hindi, Vietnamese)" | both are registered in `LANGUAGES` (`hi` with `complete_menus: false`, `vi` complete); the summary is stale |
| `docs/scorecard.md` AUTO-219-2: "90 Photoshop events map" | 206 rows in `EVENTS`; the scorecard counts something else |

## 5. Verification commands (read-only, reproduce the counts)

```sh
git -C <clone> rev-parse HEAD                                   # 45066c48292e92229ada3459a83453439514c83d (tag v0.23.1)
git -C <clone> diff --stat v0.21.0..HEAD                        # 1347 files, +140005/-122246
<installed bundle>/Contents/MacOS/photocraft-cli --version      # photocraft-cli 0.23.1 (45066c482, 2026-11-12)
<installed bundle>/Contents/MacOS/photocraft-cli commands | wc -l              # 1009
<installed bundle>/Contents/MacOS/photocraft-cli commands | grep -c '^actions\.'  # 27
<installed bundle>/Contents/MacOS/photocraft-cli commands | grep -c '^filter\.'   # 124
sed -n '5p' docs/parity-checklist.md                            # 664 of 664 menu items live
grep -an 'const ALL: \[Tool' crates/ui-egui/src/state/tool.rs   # [Tool; 69] (-a: the file has non-UTF-8 bytes)
grep -n 'const ALL: \[Format' crates/codecs/src/format.rs       # [Format; 23]
grep -c '#\[tool(' crates/automation/src/server.rs              # 26 MCP tools
sed -n '/pub const METHODS/,/^];/p' crates/automation/src/rpc.rs | grep -c '^\s*"'   # 19
awk '/const EVENTS/,/^];/' crates/engine/src/cmd/atn_cmds/events.rs \
  | grep -cE '^    (ev|stylize_event|adjustment_event|clipping_event|selection_event|target_event)!|^    Event \{'   # 206
awk '/struct ExportArgs/,/^}/' apps/photocraft-cli/src/args.rs | grep -c '#\[arg'   # 14
grep -n 'LANGUAGE_COUNT' crates/ui-egui/src/i18n.rs             # 35
grep -n 'Dead\|do nothing' docs/scorecard.md                     # "8 of 199"
```

A throwaway `convert probe.pdf probe.pcraft --pdf-dpi 96` + `info` in a temp directory (not the repo) confirmed the new PDF importer on the installed bundle; `--pdf-pages 4` on a one-page PDF was refused by name; `--pdf-editable` warned about embedded fonts. No GUI launch, no build, no writes to the checkout.

## 6. Files read for this audit

`README.md`, `ROADMAP.md`, `docs/{gaps,scorecard,parity-checklist,file-format-parity,control-protocol,mcp,plugins,printing,atn,feature-names,localization-parity,localization}.md`, `Cargo.toml`, `craft-i18n.rev`,
`apps/photocraft/src/launch_args.rs`, `apps/photocraft-cli/{Cargo.toml,src/args.rs,src/document.rs}`,
`crates/engine/src/{cmd,actions_record,memory_gate,scratch,shell_commands,build_info}.rs`,
`crates/engine/src/cmd/{file_cmds,file_cmds/open,file_cmds/open_as_smart_object,layer_css_cmds,vector_cmds,actions_edit_cmds,gallery_cmds,export_preset_cmds,web_cmds,cutout_cmds,updates_cmds,print_cmds}.rs`,
`crates/engine/src/cmd/atn_cmds/{events,menu_item}.rs`, `crates/engine/src/filters{,_ext}.rs`,
`crates/ui-egui/src/{state/tool,menus/parity,menu_catalog,control,i18n}.rs`, `crates/ui-egui/src/control/dispatch.rs`,
`crates/doc/src/effects.rs`, `crates/color/src/blend.rs`, `crates/algo/src/{artistic,matting}.rs`,
`crates/codecs/src/format.rs`, `crates/io/src/{lib,pdf,pdf_import,pdf_editable,camera_raw_xmp,tiff_layers,puppet_map}.rs`,
`crates/io/src/smart_map/import.rs`, `crates/io/tests/it/corpus.rs`, `crates/format/src/manifest.rs`, `crates/raw/src/lib.rs`,
`crates/automation/src/{server,server/conventions,rpc,security,budgets,args,workspace}.rs`, `crates/automation/src/workspace/tests.rs`,
`crates/plugins/src/runtime.rs`, `crates/vector/src/shapes.rs`, plus the installed bundle's `Contents/Info.plist` and CLI (read only; no GUI launch).

Shared libraries: `storytold/craft-libs`, pinned in `Cargo.toml` — `craft-ui`, `craft-print`, `craft-pdf`, `craft-docpath`, `craft-jpeg`, `craft-i18n`, `craft-update` at rev `6e03f65bf45181db77ba6229716e6624db9eb25b`; `craft-heif` at `081078bb1b44aeedfa5bef3d4f13d978dc77510a`; `craft-pcraft-format` at `b8f7d93b00dfb8f172938f3d2d796ae62dcfe123` (`FORMAT_VERSION: u32 = 1`). Only format/API facts needed above were consulted there.

## Round 2026-11-12 (refresh)

- Pinned to `v0.23.1` = `45066c48292e92229ada3459a83453439514c83d`; installed bundle prints `photocraft 0.23.1 (45066c482, 2026-11-12)`; delta 1347 files, +140,005/−122,246.
- The round's real capability change is **PDF reading** (raster artboards, 16-page cap, CLI DPI/page/editable knobs) plus ten new command ids, one tool and the automation-security work (ordered read roots, challenge handshake). Everything else is fixes and internal hardening; the command registry grew 993 → 1009, menus 660 → 664, tools 68 → 69, actions 21 → 27, ATN rows 204 → 206.
- Unchanged at v0.23.1, re-verified rather than assumed: 23 codecs, 124 filter ids, 16 adjustment kinds, 10 effects, 34 blend modes, 26 MCP tools + 2 resources, 28 control methods, 19 serve methods, 14 fail-closed commands, plug-in ABI v1, PSD corpus floors, `.pcraft` `format_version` 1, automation budgets.
- Citations were re-resolved; moved line numbers were refreshed (events 378→390, `ADJ` 1093→1209, tools 82→84, fail-closed test 375→644, scorecard 212→215).
