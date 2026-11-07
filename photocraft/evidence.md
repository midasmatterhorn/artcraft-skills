# PhotoCraft — evidence ledger (tag v0.21.0)

Audit basis: this checkout is tag **`v0.21.0`**, commit **`efb7ebd0c0dab1fc108ee4642aa47c22694271a8`** ("Release 0.21.0", 2026-11-06; inspection 2026-11-07; the v0.20.1 tree `327c4cc82e737a3e0af7c147a477126d77525495` was read for the delta and for counting both sides of it; installed bundle matches at 0.21.0 and its `photocraft-cli` prints `photocraft-cli 0.21.0 (efb7ebd0c, 2026-11-06)`; the GUI was never launched).

Previous round's delta (v0.18.0 → v0.20.1; numbers were current at that pin and are kept for lineage): **engine registry gains the `smart_svg_cmds` family** (edit embedded vectors with original-format save-back through VectorCraft, PR #8571; `cmd.rs` wires `smart_svg_cmds::specs()`) and `edit.clear` is reworked inline; MCP (26 tools), control (28 methods), CLI (8 subcommands + help) and headless serve (19 methods): **zero diff files**. **Live registry: 953 commands** — measured with `photocraft-cli commands | wc -l` on the installed bundle that matches this tag. Locale catalogs 26 = 26 (the notes' Finnish/Norwegian Bokmål PRs were already in v0.18.0's set — verified against both tag trees). Features: PSD font metadata survives text edits (#6169), Move-tool huge-layer drag without per-frame copies (#6985), .atn steps switch documents (#7621) + export hardening (#8371), Pattern Fill in Layer Panel Footer (#7716), advanced-selection shortcuts (#8015), paragraph overflow port (#8311), TIFF >2^30 px row-group decode (#8536), multi-layer transform handles (#8623), Fill/Stroke popover + full Color Picker (#8725), colour-channel-set editing (#9274), live picker previews (#9757), brush-state survival (#10288), 18-PR integration batch (#10145).
Prior audits are retained below; the v0.20.1 numbers above are the current basis. No `references/` directory
ships — SKILL.md carries the body, this file carries the per-claim evidence.

## 1. Capability claims → evidence → tier

Tier legend: **implemented** = code path exists and is wired into UI/CLI/automation; **partial** = code exists with a
named gap; **claimed-only** = said in docs/README but absent or contradicted by code.

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 660/660 Photoshop menu items dispatch a command | `docs/parity-checklist.md:5` ("660 of 660 … 100.0%"); floor `FLOOR = 660` at `crates/ui-egui/src/menus/parity.rs:10` (631 at v0.20.1) | implemented |
| 2 | 68 tools; every classic tool present; Art History Brush new and partial | `crates/ui-egui/src/state/tool.rs:82` `pub const ALL: [Tool; 68]`; `Tool::ArtHistoryBrush` at `:51`,`:125`; `docs/gaps.md` header: "G6: Art History Brush landed as partial, TOOL-213-20, #1610, so no toolbar tool is missing" | implemented (tool partial) |
| 3 | 16 adjustment-layer kinds, each also a destructive `image.adjustments.*` command | `crates/engine/src/cmd.rs:1093` `const ADJ: &[(&str, &str, &str)]` — 16 tuples counted | implemented |
| 4 | 10 layer-effect kinds | `crates/doc/src/effects.rs`; `crates/engine/src/layer_style.rs` | implemented |
| 5 | 34 blend modes (PassThrough + 27 PS + 6 Paint.NET) | `crates/color/src/blend.rs` | implemented |
| 6 | 124 live `filter.*` command ids = 64 pairwise + 47 gallery + 13 workspace/lifecycle ids | Counted from the registry: `photocraft-cli commands | grep -c '^filter\.'` = 124; `^filter\.gallery\.` = 47 (gallery rows at `crates/algo/src/artistic.rs` `gallery!`); 5 `filter.blurGallery.*` + 8 single-token ids (`filter.{adaptiveWideAngle,cameraRaw,convertForSmartFilters,filterGallery,lastFilter,lensCorrection,liquify,vanishingPoint}`) = 13; remaining 64 are pairwise. The previous 130 counted string literals in `filters.rs`/`filters_ext.rs`, which over-counts declared-but-unregistered ids | implemented |
| 7 | 53 PSD smart-filter classes map one-to-one to 53 distinct commands | `crates/io/src/smart_map/import.rs` `const KNOWN: [Known; 53]`; 53 `Known {` entries minus the struct def; 53 unique `command:` values | implemented |
| 8 | 204 `.atn` event rows (167 at v0.20.1 by the same count); nesting to 16 levels | `crates/engine/src/cmd/atn_cmds/events.rs:378` `pub(super) const EVENTS: &[Event]`; rows counted as top-level macro invocations (`ev!` 56, `adjustment_event!` 14, `stylize_event!` 12, `selection_event!` 11, `target_event!` 14, `clipping_event!` 2) plus `Event {` literals (95) = 204. The previous 114 came from a line-offset slice that started inside the table | implemented |
| 9 | 16 `actions.*` commands; Save As/Close actions work | `crates/engine/src/cmd/actions_cmds.rs`; `docs/gaps.md` G11 change note | implemented |
| 10 | `.pcraft` = manifest `format_version` 1 + content-addressed zstd tiles/blobs, atomic save; oversized manifests refused | `crates/format/src/manifest.rs` (`FORMAT_VERSION`), `atomic.rs`, `migrate.rs`; #8893 refusal | implemented |
| 11 | 23 codec formats; read-only PCX, XPM, DICOM; **JPEG XL export-only**; AVIF write-only (feature); HEIF read-only (feature) | `crates/codecs/src/format.rs:110` `ALL: [Format; 23]`; `Format::Jxl => FormatCaps { read: false, … }` at `:287`; exception text at `:90` ("Lossless JPEG XL export uses the pure-Rust zune-jpegxl encoder; JPEG XL reading … not yet available"); `ASYMMETRIC_EXCEPTIONS` holds Xpm/Dicom/Pcx/Avif/[Jxl]/Heif | implemented |
| 12 | TIFF alpha and spot channels as extra samples, read+write; global layer mask block written | `crates/codecs/src/codecs/tiff/bands.rs` (`extra_samples`); `crates/io/src/tiff_layers.rs`; `docs/gaps.md` G10 change note (#7415) | implemented |
| 13 | Import-only layered readers: PDN, KRA/KRZ, XCF/XCF.GZ, Affinity, SVG; writable targets refused | `crates/io/src/lib.rs` `import_stages`/`export_stages` refusals | implemented |
| 14 | PSD/PSB read+write with enforced corpus floors 148/169, 249/308, 190/258 | `crates/io/tests/it/corpus.rs:151,155,159` — unchanged from v0.16.0 | implemented, fidelity partial (G1) |
| 15 | Camera-raw `.xmp` settings sidecars load/auto-fill/save; lossy DNG (JPEG XL) decodes | `crates/io/src/camera_raw_xmp.rs` module doc ("the same reader fills the dialog from a raw file's sidecar … and the writer keeps it"); `crates/raw/src/lib.rs:31` (lossy-JPEG **and JPEG XL** DNG), `:54 mod jxl`, `:80 embedded_jxl_preview` | implemented |
| 16 | CR3 preview only; clean-room CRX assessed as not feasible | `crates/raw/src/cr3.rs`; `docs/gaps.md` G14 change note | partial (documented decision) |
| 17 | Export As = 6 formats; Save for Web = 6 | `crates/engine/src/cmd/export_preset_cmds.rs:13` `const FORMATS: [&str; 6] = ["png","jpg","webp","tif","tga","ico"]`; `crates/engine/src/cmd/web_cmds.rs` `"format":"gif|png8|png24|jpeg|wbmp|webp"` — the previous round counted 5 and missed `webp`, which was already in the v0.20.1 tree | implemented |
| 18 | 8 CLI subcommands, 12 export flags, exit codes 0/1/2 | `apps/photocraft-cli/src/args.rs` (`enum Command`; `ExportArgs` 12 `#[arg]`s — `--tiff-transparency`, `--tiff-pyramid`, `--pcraft-full-composite` are new at v0.21.0) | implemented |
| 19 | 26 MCP tools + 2 MCP resources | `crates/automation/src/server.rs`: 26 `#[tool(` entries (the 27th `#[tool` hit is `#[tool_router]`); `crates/automation/src/server/conventions.rs` resources | implemented |
| 20 | 28 control-channel methods, auth-first | `crates/ui-egui/src/control/dispatch.rs` handler chain (5 handlers); 28 distinct method arms counted | implemented |
| 21 | Headless `serve`/`rpc` exposes 19 methods | `crates/automation/src/rpc.rs:42-62` `pub const METHODS` read in full (19 entries) | implemented |
| 22 | Automation budgets: 8 MiB reply, 5 MiB PNG, 2048 preview side, 64 M pixels, 256 batch steps | `crates/automation/src/budgets.rs`; `crates/automation/src/security.rs` | implemented |
| 23 | Wasm plug-in ABI v1: 5 commands; duplicate manifest params refused | `crates/plugins/src/runtime.rs`; `crates/engine/src/cmd/plugin_cmds.rs`; #9441 | implemented |
| 24 | Automation is fail-closed for the same 14 filesystem commands (unchanged at v0.21.0); desktop also refuses `image.mode.*` | `crates/automation/src/workspace/tests.rs:375` `filesystem_commands_fail_closed` (14 ids listed); `crates/automation/src/workspace.rs` authorization | implemented |
| 25 | Token handling: no flag → generated; missing *value* → launch fails | `crates/automation/src/security.rs:183-209` `server_token` ("With no supplied token or file, a fresh token is returned"); `apps/photocraft/src/launch_args.rs` #6429 comments | implemented |
| 26 | Print through in-process IPP, portal, spooler or PDF | `crates/engine/src/cmd/print_cmds.rs`; `crates/ipp`; `docs/printing.md` | implemented |
| 27 | Select Subject/Remove Background/Refine Edge are classical (guided-filter matting; local linear models) | `crates/algo/src/matting.rs` module doc (guided filter, He/Sun ECCV 2010); `crates/engine/src/cmd/cutout_cmds.rs` (Remove Background one history step) | implemented (classical only) |
| 28 | Type on a path follows path edits; PSD `Txt2` round trip | `crates/psd/src/tiff.rs` (`Txt2`); `docs/gaps.md` G8 change note (#7962) | implemented |
| 29 | Startup self-update prompt; update check delegated to craft-update | `crates/engine/src/cmd/updates_cmds.rs`; `Cargo.toml` `craft-update` pin | implemented (no periodic recheck) |
| 30 | Dead preferences 10 of 192 | `docs/scorecard.md:212` (generated by the prefs audit; `docs/gaps.md` header prose still says 11 of 183 — the generated line wins) | implemented metric |

## 2. Automation-surface counts: v0.16.0 → v0.17.0 (historical — superseded by §2b for the current tag)

Delta (re-diffed between tags): registry shape unchanged; `photocraft-cli` bundled into the macOS app
(PR #4742); multi-page-TIFF video-frames import; strip-compositor smart-object sources; 4-stage Cutout;
locale catalogs 21 → 26 (+Finnish); startup report; root-alias resolution in automation.

Every row was re-measured from the v0.17.0 checkout. The values are that pin's, not the current ones; §2b carries the v0.21.0 measurements.

| Surface | v0.16.0 | v0.17.0 (measured) | Change / how measured |
|---|---:|---:|---|
| Tools | 67 | **68** | +ArtHistoryBrush (`tool.rs:82`, `[Tool; 68]`); partial per `docs/gaps.md` G6 |
| Menu items live | 631/631 | **631/631** | unchanged; `docs/parity-checklist.md:5` |
| `filter.*` command ids | 124 | **130** | pairwise 63→66 (filters.rs 30→32, filters_ext 33→34; Stylize/Pixelate entries per #6303), gallery 47 unchanged, workspace/lifecycle literals 83−66=17 (was ~14) |
| PSD smart-filter classes → commands | 54 → 49 | **53 → 53 (one-to-one)** | `smart_map/` is a directory now; `KNOWN: [Known; 53]`, all command values distinct |
| Action event mappings | 114 | **114** | unchanged; `cmd/atn_cmds/events.rs:185` |
| MCP tools | 26 | **26** | set identical; `#[tool(` count |
| MCP resources | 2 | **2** | unchanged; `server/conventions.rs` |
| Control-channel methods | 28 | **28** | set identical; `crates/ui-egui/src/control/dispatch.rs` (file moved into `control/`) |
| Headless `serve`/rpc methods | 19 | **19** | set identical; `rpc.rs:42` |
| CLI subcommands / export flags | 8 / 9 | **8 / 9** | unchanged; `args.rs:31`, `ExportArgs` |
| Codec formats | 22 | **22** | IFF moved from read-only to read+write; `ASYMMETRIC_EXCEPTIONS` now Xpm/Dicom/Pcx/Avif/Heif |
| Adjustment-layer commands | 16 (+16) | **16 (+16)** | unchanged; `cmd.rs:1093` |
| Corpus floors (PSD) | 148/169, 249/308, 190/258 | **same** | `corpus.rs:151-159` |
| Fail-closed filesystem commands | 14 | **14** | same 14 ids; test moved to `workspace/tests.rs:315` |
| Dead preferences | 20 of 177 | **12 of 181** | `docs/scorecard.md:203` |
| Craft-libs pins | per-crate revs | **one rev `92d392cf…` for all, + `craft-update`** | `Cargo.toml` |
| Engine source layout | `crates/engine/src/*.rs` flat | **`cmd.rs` + `cmd/` submodules; `filters.rs`/`filters_ext.rs` at root with `tests/` dirs** | `ls crates/engine/src` |

## 2b. Surface counts re-measured at v0.21.0 (2026-11-07)

Method column names the exact command; automation sets were diffed **as sets** against the v0.20.1 tree.

| Surface | v0.20.1 (previous skill) | v0.21.0 (measured) | Method |
|---|---:|---:|---|
| Engine commands (live) | 953 | **993** | `photocraft-cli commands \| wc -l` on the installed 0.21.0 bundle |
| Photoshop menu items live | 631/631 | **660/660** | `sed -n '5p' docs/parity-checklist.md`; `FLOOR = 660` in `crates/ui-egui/src/menus/parity.rs:10` |
| Tools | 68 | **68 (unchanged)** | `grep -n 'const ALL: \[Tool' crates/ui-egui/src/state/tool.rs` → `[Tool; 68]` |
| Codec formats | 22 | **23** (+JPEG XL, export-only) | `grep -n 'const ALL: \[Format' crates/codecs/src/format.rs` → `[Format; 23]`, `Format::Jxl … read: false` |
| `filter.*` live ids | 130 (static literals) | **124** (47 gallery + 64 pairwise + 13 workspace) | `photocraft-cli commands \| grep -c '^filter\.'` and prefix split |
| Adjustment-layer kinds | 16 | **16 (unchanged)** | 16 tuples between `const ADJ` and `];` in `crates/engine/src/cmd.rs` |
| Layer effects | 10 | **10 (unchanged)** | `crates/doc/src/effects.rs` |
| Blend modes | 34 | **34 (unchanged)** | `awk '/pub enum BlendMode/,/^}/' crates/color/src/blend.rs \| grep -cE '^\s+[A-Z]'` |
| `.atn` event rows | 114 published / 167 re-counted | **204** | top-level macro invocations + `Event {` lines inside `const EVENTS` (`crates/engine/src/cmd/atn_cmds/events.rs:378`) |
| `actions.*` ids | 17 | **21** | `photocraft-cli commands \| grep -c '^actions\.'` |
| MCP tools / resources | 26 / 2 | **26 / 2 (unchanged)** | `grep -c '#\[tool(' crates/automation/src/server.rs`; tool-name set diff = no removals |
| Control-channel methods | 28 | **28 (unchanged)** | method-id set extracted from `crates/ui-egui/src/control/dispatch.rs`, diffed against the v0.20.1 tree: zero diff |
| Headless `serve` methods | 19 | **19 (unchanged)** | `pub const METHODS` in `crates/automation/src/rpc.rs`, diffed: zero diff |
| CLI subcommands / export flags | 8 / 9 | **8 / 12** | `enum Command` in `apps/photocraft-cli/src/args.rs`; `#[arg]` count in `ExportArgs` |
| Fail-closed filesystem commands | 14 | **14 (unchanged)** | `crates/automation/src/workspace/tests.rs:375` |
| Dead preferences | 12 of 181 | **10 of 192** | `docs/scorecard.md:212` (generated) |
| Locale catalogs | 26 | **27** | `ls crates/ui-egui/src/i18n/*.tsv` (both tags; `bs.tsv` new) |
| Plug-in ABI | v1, 5 `plugin.*` commands | **v1, 5 (unchanged)** | `ABI_VERSION: i32 = 1` at `crates/plugins/src/runtime.rs:14` |
| PSD corpus floors | 148/169, 249/308, 190/258 | **same** | `crates/io/tests/it/corpus.rs` `MIXED`/`PSD_TOOLS`/`PHOTOSHOP` rows |
| Files changed in the delta | 276 | **916** | `git diff --name-only v0.20.1..HEAD \| wc -l`; `--stat` +127,407/−6,129 |

New command families at v0.21.0 (live ids): `layer.frame.{set,setContent,fit,convert,info}` (5), `type.openType.numerals.*` (9), `type.openType.stylisticSets.set1…set20` (20), `file.approveMemory`, and `actions.{createSingleHistoryState,pauseSeconds,performance,setHistory,setPlayback}`.

## 3. Things that could not be verified (stated as uncertain in SKILL.md)

- **Exact engine command count.** Table macros expand per row; the static count remains uncertain by a few dozen.
  Authoritative live count: `photocraft-cli commands | wc -l`.
- **ROADMAP percentages** (~76% breadth / ~45% readiness) were measured at 0.6.0 and are not re-computed — never
  presented as current.
- **Open-issue counts** in `docs/gaps.md` G3 are dated checkpoints, not live data.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `README.md` "500+ commands"; `docs/architecture.md` "~700" | static registration-site count is higher and uncertain; use `photocraft-cli commands` |
| `docs/gaps.md` older change notes say "112 `.atn` events" | 114 rows in `cmd/atn_cmds/events.rs` |
| `docs/file-format-parity.md` PSD row previously said "53 smart filters mapped" | 53 classes / 53 commands in `crates/io/src/smart_map/import.rs` (now exactly matches — coincidence of the split) |
| Baseline skill said "only Art History Brush is missing (G6)" | landed this release as partial; `[Tool; 68]` |

## 5. Verification commands (read-only, reproduce the counts)

```sh
git -C <clone> rev-parse HEAD                                   # efb7ebd0c0dab1fc108ee4642aa47c22694271a8 (tag v0.21.0)
<installed bundle>/Contents/MacOS/photocraft-cli commands | wc -l          # 993 engine commands
<installed bundle>/Contents/MacOS/photocraft-cli commands | grep -c '^filter\.'   # 124 live filter ids
sed -n '5p' docs/parity-checklist.md                            # 660 of 660 menu items live
grep -n 'const ALL: \[Tool' crates/ui-egui/src/state/tool.rs   # [Tool; 68]
grep -n 'const ALL: \[Format' crates/codecs/src/format.rs      # [Format; 23]
grep -c '#\[tool(' crates/automation/src/server.rs             # 26 MCP tools
sed -n '/pub const METHODS/,/^];/p' crates/automation/src/rpc.rs | grep -c '^\s*"'   # 19
awk '/const EVENTS/,/^];/' crates/engine/src/cmd/atn_cmds/events.rs \
  | grep -cE '^    (ev|stylize_event|adjustment_event|clipping_event|selection_event|target_event)!|^    Event \{'   # 204
awk '/struct ExportArgs/,/^}/' apps/photocraft-cli/src/args.rs | grep -c '#\[arg'   # 12
grep -n 'fn filesystem_commands_fail_closed' crates/automation/src/workspace/tests.rs   # :375, 14 ids
grep -n 'Dead\|do nothing' docs/scorecard.md                    # "Settings that do nothing: 10 of 192"
ls crates/ui-egui/src/i18n/*.tsv | wc -l                        # 27 locale catalogs
```

## 6. Files read for this audit

`README.md`, `docs/{gaps,scorecard,parity-checklist,control-protocol,mcp,file-format-parity,plugins,printing,batch-naming}.md`, `Cargo.toml`,
`apps/photocraft/src/launch_args.rs`, `apps/photocraft-cli/src/args.rs`,
`crates/engine/src/{cmd,cmd/gallery_cmds,cmd/atn_cmds/events,cmd/cutout_cmds,cmd/updates_cmds,cmd/export_preset_cmds,filters,filters_ext}.rs`,
`crates/ui-egui/src/state/tool.rs`, `crates/ui-egui/src/menus/parity.rs`, `crates/ui-egui/src/control/dispatch.rs`,
`crates/doc/src/effects.rs`, `crates/color/src/blend.rs`, `crates/algo/src/{artistic,matting}.rs`,
`crates/codecs/src/format.rs`, `crates/codecs/src/codecs/{iff.rs,tiff/}`, `crates/io/src/{lib,camera_raw_xmp,tiff_layers}.rs`,
`crates/io/src/smart_map/import.rs`, `crates/io/tests/it/corpus.rs`, `crates/format/src/manifest.rs`,
`crates/raw/src/lib.rs`, `crates/automation/src/{server,server/conventions,rpc,security,budgets}.rs`,
`crates/automation/src/workspace{,/tests.rs}`, `crates/plugins/src/runtime.rs`, the installed bundle's `Contents/Info.plist` (read only; no GUI launch).

Shared libraries were not cloned: `storytold/craft-libs` is pinned in `Cargo.toml` — all craft crates (craft-ui,
craft-print, craft-docpath, craft-jpeg, craft-update) at rev `92d392cff132eaf53e13afff77f38b5c11b73aa0`; no
shared-library behaviour is claimed here.


## Round 2026-11-07 (refresh)

- Pinned to `v0.21.0` = `efb7ebd0c0dab1fc108ee4642aa47c22694271a8` (installed `photocraft-cli 0.21.0 (efb7ebd0c, 2026-11-06)`); delta 916 files, +127,407/−6,129.
- Re-measured from the registry, not from literals: 993 commands (953 at the previous pin) and 124 `filter.*` ids. The previous skill's 130 filter ids and 114 event mappings were both extraction artifacts, corrected here; the `actions.*` count moved 17 → 21 and the event table 167 → 204 when both tags are counted the same way.
- Capability changes the code proves: JPEG XL joined the codec list as export-only (22 → 23 formats); the CLI gained `--tiff-transparency`, `--tiff-pyramid`, `--pcraft-full-composite` (9 → 12 export flags) and `--approve-high-memory`; OpenType Numerals + Stylistic Sets 1–20 closed the G8 submenu gap the previous skill listed as missing; the Frame tool family and memory supervision (`file.approveMemory`, `memory_gate`, `scratch`) are new.
- Unchanged at v0.21.0, re-verified rather than assumed: 68 tools, 16 adjustment kinds, 10 layer effects, 34 blend modes, 26 MCP tools + 2 resources, 28 control methods, 19 serve methods, 14 fail-closed commands, plug-in ABI v1, PSD corpus floors, `.pcraft` `format_version` 1.
- Citations: every repo-relative path was re-resolved; `crates/engine/src/commands.rs` no longer exists (the registry builder is `fn build()` in `crates/engine/src/cmd.rs`), and the baseline's line numbers for `crates/ui-egui/src/menus/parity.rs`, `crates/automation/src/workspace/tests.rs`, `docs/scorecard.md` and `crates/engine/src/cmd/atn_cmds/events.rs` were refreshed.
- Doc drift recorded, not resolved: `docs/gaps.md` says 11 of 183 dead preferences (scorecard: 10 of 192) and quotes 128 supported / 89 unmapped ATN events — a Photoshop-event-kind tally that is not the 204 mapped table rows. `docs/gaps.md`'s own "updated 2026-11-05" header replaced the 2026-10-27 date the previous skill quoted.

## Round 2026-11-04 (refresh)

- Pinned to `v0.20.1` = `327c4cc82e737a3e0af7c147a477126d77525495` (installed `photocraft 0.20.1 (327c4cc82, 2026-11-03)`).
- 78 engine command ids at both tags; `actions.*` is now 17 ids (`actions.newSet`), and `.atn` I/O gained `actions.record {set}`, `actions.load {encoding}`, `actions.save {skipUnsupported}`.
- Id sets were diffed between the two tags with the same extraction method as the claims above; counts here are the new ones.
