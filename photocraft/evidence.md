# PhotoCraft — evidence ledger (tag v0.17.0)

Audit basis: this checkout is tag **`v0.17.0`**, commit **`b8c3f3aa8e2918032cadc0e042664414a03be333`** ("Release 0.17.0";
the clone is shallow and holds exactly this commit, so tag-to-tag diffs were unavailable and every delta below was
re-measured here and compared against the previous skill (v0.16.0) and the repo's own revision histories). Inspection
date **2026-10-29**. Installed `/Applications/PhotoCraft.app` = 0.17.0 (`CFBundleShortVersionString` — current this
wave, not stale), bundle id `ai.storyteller.photocraft`, min macOS 11.0; binary prints
`photocraft 0.17.0 (b8c3f3aa8, 2026-10-28)`; the GUI was never launched. No `references/` directory ships — SKILL.md
carries the body, this file carries the per-claim evidence.

## 1. Capability claims → evidence → tier

Tier legend: **implemented** = code path exists and is wired into UI/CLI/automation; **partial** = code exists with a
named gap; **claimed-only** = said in docs/README but absent or contradicted by code.

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 631/631 Photoshop menu items dispatch a command | `docs/parity-checklist.md:5` ("631 of 631 … 100.0%"); floor at `crates/ui-egui/src/menus/parity.rs` | implemented |
| 2 | 68 tools; every classic tool present; Art History Brush new and partial | `crates/ui-egui/src/state/tool.rs:82` `pub const ALL: [Tool; 68]`; `Tool::ArtHistoryBrush` at `:51`,`:125`; `docs/gaps.md` header: "G6: Art History Brush landed as partial, TOOL-213-20, #1610, so no toolbar tool is missing" | implemented (tool partial) |
| 3 | 16 adjustment-layer kinds, each also a destructive `image.adjustments.*` command | `crates/engine/src/cmd.rs:1093` `const ADJ: &[(&str, &str, &str)]` — 16 tuples counted | implemented |
| 4 | 10 layer-effect kinds | `crates/doc/src/effects.rs`; `crates/engine/src/layer_style.rs` | implemented |
| 5 | 34 blend modes (PassThrough + 27 PS + 6 Paint.NET) | `crates/color/src/blend.rs` | implemented |
| 6 | 130 `filter.*` command ids = 66 pairwise (32 `filters.rs` + 34 `filters_ext.rs`) + 47 gallery + 17 literal workspace/lifecycle ids | `grep -oE '"filter\.[a-zA-Z.]+"'` per file: `crates/engine/src/filters.rs`=32, `filters_ext.rs`=34; engine-wide unique literals=83; gallery rows=47 (`crates/algo/src/artistic.rs:38` `gallery!`, rows counted by ` = "` + `r#`); gallery ids are macro-built (no `"filter.coloredPencil"` literal — verified) | implemented |
| 7 | 53 PSD smart-filter classes map one-to-one to 53 distinct commands | `crates/io/src/smart_map/import.rs` `const KNOWN: [Known; 53]`; 53 `Known {` entries minus the struct def; 53 unique `command:` values | implemented |
| 8 | 114 Photoshop action-event mappings; nesting to 16 levels | `crates/engine/src/cmd/atn_cmds/events.rs:185` `pub(super) const EVENTS: &[Event]`, 114 rows counted by the `ev!/adjustment_event!/clipping_event!/Event {` pattern | implemented |
| 9 | 16 `actions.*` commands; Save As/Close actions work | `crates/engine/src/cmd/actions_cmds.rs`; `docs/gaps.md` G11 change note | implemented |
| 10 | `.pcraft` = manifest `format_version` 1 + content-addressed zstd tiles/blobs, atomic save; oversized manifests refused | `crates/format/src/manifest.rs` (`FORMAT_VERSION`), `atomic.rs`, `migrate.rs`; #8893 refusal | implemented |
| 11 | 22 codec formats; read-only PCX, XPM, DICOM; IFF now read+write; AVIF write-only (feature); HEIF read-only (feature) | `crates/codecs/src/format.rs:107` `ALL: [Format; 22]`; `caps()`: `Iff => … alpha: true` (base read/write), exceptions list holds only Xpm/Dicom/Pcx/Avif/Heif; IFF writer "24-bit ILBM" (release PR #9080) | implemented |
| 12 | TIFF alpha and spot channels as extra samples, read+write; global layer mask block written | `crates/codecs/src/codecs/tiff/bands.rs` (`extra_samples`); `crates/io/src/tiff_layers.rs`; `docs/gaps.md` G10 change note (#7415) | implemented |
| 13 | Import-only layered readers: PDN, KRA/KRZ, XCF/XCF.GZ, Affinity, SVG; writable targets refused | `crates/io/src/lib.rs` `import_stages`/`export_stages` refusals | implemented |
| 14 | PSD/PSB read+write with enforced corpus floors 148/169, 249/308, 190/258 | `crates/io/tests/it/corpus.rs:151,155,159` — unchanged from v0.16.0 | implemented, fidelity partial (G1) |
| 15 | Camera-raw `.xmp` settings sidecars load/auto-fill/save; lossy DNG (JPEG XL) decodes | `crates/io/src/camera_raw_xmp.rs` module doc ("the same reader fills the dialog from a raw file's sidecar … and the writer keeps it"); `crates/raw/src/lib.rs:31` (lossy-JPEG **and JPEG XL** DNG), `:54 mod jxl`, `:80 embedded_jxl_preview` | implemented |
| 16 | CR3 preview only; clean-room CRX assessed as not feasible | `crates/raw/src/cr3.rs`; `docs/gaps.md` G14 change note | partial (documented decision) |
| 17 | Export As = 6 formats; Save for Web = 5 | `crates/engine/src/cmd/export_preset_cmds.rs:13` `const FORMATS: [&str; 6]`; `crates/engine/src/cmd/web_cmds.rs` | implemented |
| 18 | 8 CLI subcommands, 9 export flags, exit codes 0/1/2 | `apps/photocraft-cli/src/args.rs:31-40` (`enum Command`), `ExportArgs` 9 `#[arg]`s | implemented |
| 19 | 26 MCP tools + 2 MCP resources | `crates/automation/src/server.rs`: 26 `#[tool(` entries (the 27th `#[tool` hit is `#[tool_router]`); `crates/automation/src/server/conventions.rs` resources | implemented |
| 20 | 28 control-channel methods, auth-first | `crates/ui-egui/src/control/dispatch.rs` handler chain (5 handlers); 28 distinct method arms counted | implemented |
| 21 | Headless `serve`/`rpc` exposes 19 methods | `crates/automation/src/rpc.rs:42-62` `pub const METHODS` read in full (19 entries) | implemented |
| 22 | Automation budgets: 8 MiB reply, 5 MiB PNG, 2048 preview side, 64 M pixels, 256 batch steps | `crates/automation/src/budgets.rs`; `crates/automation/src/security.rs` | implemented |
| 23 | Wasm plug-in ABI v1: 5 commands; duplicate manifest params refused | `crates/plugins/src/runtime.rs`; `crates/engine/src/cmd/plugin_cmds.rs`; #9441 | implemented |
| 24 | Automation is fail-closed for the same 14 filesystem commands; desktop also refuses `image.mode.*` | `crates/automation/src/workspace/tests.rs:315` `filesystem_commands_fail_closed` (14 ids listed); `crates/automation/src/workspace.rs` authorization | implemented |
| 25 | Token handling: no flag → generated; missing *value* → launch fails | `crates/automation/src/security.rs:183-209` `server_token` ("With no supplied token or file, a fresh token is returned"); `apps/photocraft/src/launch_args.rs` #6429 comments | implemented |
| 26 | Print through in-process IPP, portal, spooler or PDF | `crates/engine/src/cmd/print_cmds.rs`; `crates/ipp`; `docs/printing.md` | implemented |
| 27 | Select Subject/Remove Background/Refine Edge are classical (guided-filter matting; local linear models) | `crates/algo/src/matting.rs` module doc (guided filter, He/Sun ECCV 2010); `crates/engine/src/cmd/cutout_cmds.rs` (Remove Background one history step) | implemented (classical only) |
| 28 | Type on a path follows path edits; PSD `Txt2` round trip | `crates/psd/src/tiff.rs` (`Txt2`); `docs/gaps.md` G8 change note (#7962) | implemented |
| 29 | Startup self-update prompt; update check delegated to craft-update | `crates/engine/src/cmd/updates_cmds.rs`; `Cargo.toml` `craft-update` pin | implemented (no periodic recheck) |
| 30 | Dead preferences 12 of 181 | `docs/scorecard.md:203` (generated count) | implemented metric |

## 2. Automation-surface counts: previous skill (v0.16.0) → this tag (v0.17.0)

Every row was re-measured from this checkout.

| Surface | v0.16.0 | v0.17.0 (measured) | Change / how measured |
|---|---:|---:|---|
| Tools | 67 | **68** | +ArtHistoryBrush (`tool.rs:82`, `[Tool; 68]`); partial per `docs/gaps.md` G6 |
| Menu items live | 631/631 | **631/631** | unchanged; `docs/parity-checklist.md:5` |
| `filter.*` command ids | 124 | **130** | pairwise 63→66 (filters.rs 30→32, filters_ext 33→34; Stylize/Pixelate entries per #6303), gallery 47 unchanged, workspace/lifecycle literals 83−66=17 (was ~14) |
| PSD smart-filter classes → commands | 54 → 49 | **53 → 53 (one-to-one)** | `smart_map/` is a directory now; `KNOWN: [Known; 53]`, all command values distinct |
| Action event mappings | 114 | **114** | unchanged; `cmd/atn_cmds/events.rs:185` |
| MCP tools | 26 | **26** | set identical; `#[tool(` count |
| MCP resources | 2 | **2** | unchanged; `server/conventions.rs` |
| Control-channel methods | 28 | **28** | set identical; `control/dispatch.rs` (file moved into `control/`) |
| Headless `serve`/rpc methods | 19 | **19** | set identical; `rpc.rs:42` |
| CLI subcommands / export flags | 8 / 9 | **8 / 9** | unchanged; `args.rs:31`, `ExportArgs` |
| Codec formats | 22 | **22** | IFF moved from read-only to read+write; `ASYMMETRIC_EXCEPTIONS` now Xpm/Dicom/Pcx/Avif/Heif |
| Adjustment-layer commands | 16 (+16) | **16 (+16)** | unchanged; `cmd.rs:1093` |
| Corpus floors (PSD) | 148/169, 249/308, 190/258 | **same** | `corpus.rs:151-159` |
| Fail-closed filesystem commands | 14 | **14** | same 14 ids; test moved to `workspace/tests.rs:315` |
| Dead preferences | 20 of 177 | **12 of 181** | `docs/scorecard.md:203` |
| Craft-libs pins | per-crate revs | **one rev `92d392cf…` for all, + `craft-update`** | `Cargo.toml` |
| Engine source layout | `crates/engine/src/*.rs` flat | **`cmd.rs` + `cmd/` submodules; `filters.rs`/`filters_ext.rs` at root with `tests/` dirs** | `ls crates/engine/src` |

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
| `docs/file-format-parity.md` PSD row previously said "53 smart filters mapped" | 53 classes / 53 commands in `smart_map/import.rs` (now exactly matches — coincidence of the split) |
| Baseline skill said "only Art History Brush is missing (G6)" | landed this release as partial; `[Tool; 68]` |

## 5. Verification commands (read-only, reproduce the counts)

```sh
git -C <clone> rev-parse HEAD                         # b8c3f3aa8e2918032cadc0e042664414a03be333
grep -n 'const ALL: \[Tool' crates/ui-egui/src/state/tool.rs        # [Tool; 68]
sed -n '5p' docs/parity-checklist.md                                # 631 of 631 menu items live
grep -c '#\[tool(' crates/automation/src/server.rs                  # 26 MCP tools
awk 'NR>=185,/^];/' crates/engine/src/cmd/atn_cmds/events.rs | grep -cE '(ev!|adjustment_event!|clipping_event!|Event \{)'   # 114
grep -c ' = "' crates/algo/src/artistic.rs                          # 47 gallery rows (within gallery!)
grep -c 'Known {' crates/io/src/smart_map/import.rs                 # 54 (53 entries + struct def)
awk '/const KNOWN/,/^];/' crates/io/src/smart_map/import.rs | grep -oE 'command: "[^"]+"' | sort -u | wc -l   # 53
sed -n '107p' crates/codecs/src/format.rs                           # pub const ALL: [Format; 22]
sed -n '/pub const METHODS/,/^];/p' crates/automation/src/rpc.rs | grep -c '^\s*"'   # 19
awk '/struct ExportArgs/,/^}/' apps/photocraft-cli/src/args.rs | grep -c '#\[arg'    # 9
sed -n '151,159p' crates/io/tests/it/corpus.rs                       # floors 148/169, 249/308, 190/258
grep -n 'filesystem_commands_fail_closed' crates/automation/src/workspace/tests.rs   # 14-id list at :315
photocraft-cli commands | wc -l                                      # authoritative engine command count
```

## 6. Files read for this audit

`README.md`, `docs/{gaps,scorecard,parity-checklist,control-protocol,mcp,file-format-parity,plugins,printing,batch-naming}.md`, `Cargo.toml`,
`apps/photocraft/src/launch_args.rs`, `apps/photocraft-cli/src/args.rs`,
`crates/engine/src/{commands,cmd,cmd/gallery_cmds,cmd/atn_cmds/events,cmd/cutout_cmds,cmd/updates_cmds,cmd/export_preset_cmds,filters,filters_ext}.rs`,
`crates/ui-egui/src/state/tool.rs`, `crates/ui-egui/src/menus/parity.rs`, `crates/ui-egui/src/control/dispatch.rs`,
`crates/doc/src/effects.rs`, `crates/color/src/blend.rs`, `crates/algo/src/{artistic,matting}.rs`,
`crates/codecs/src/format.rs`, `crates/codecs/src/codecs/{iff.rs,tiff/}`, `crates/io/src/{lib,camera_raw_xmp,tiff_layers}.rs`,
`crates/io/src/smart_map/import.rs`, `crates/io/tests/it/corpus.rs`, `crates/format/src/manifest.rs`,
`crates/raw/src/lib.rs`, `crates/automation/src/{server,server/conventions,rpc,security,budgets}.rs`,
`crates/automation/src/workspace{,/tests.rs}`, `crates/plugins/src/runtime.rs`, `/Applications/PhotoCraft.app/Contents/Info.plist` (read only; no GUI launch).

Shared libraries were not cloned: `storytold/craft-libs` is pinned in `Cargo.toml` — all craft crates (craft-ui,
craft-print, craft-docpath, craft-jpeg, craft-update) at rev `92d392cff132eaf53e13afff77f38b5c11b73aa0`; no
shared-library behaviour is claimed here.
