# LightCraft — evidence ledger (tag v0.21.1)

Audit basis: this checkout is tag **`v0.21.1`**, commit **`361e3bc0c838ffe5e5cea515b1fe5b71951989c6`**, release dated **2026-11-12**; inspection date **2026-11-12**. The previous skill described **v0.19.0** (`16636c45a63bff3065a6fd31aecc22a6fc15ca53`). The installed bundle matches the tag (`CFBundleShortVersionString`/`CFBundleVersion` 0.21.1, binary prints `lightcraft 0.21.1`); bundle id `ai.storyteller.lightcraft`; the GUI was never launched. No `references/` directory.

v0.19.0 -> v0.21.1 delta: **235 files changed, +9,525/−3,929**. Engine registry **365 -> 368** `cmd!` specs, **+3, zero removed**: `lensBlur.brushReset`, `lensBlur.brushStroke`, `lensBlur.findSubject`. `UI_COMMANDS` **194 -> 195** (`+section.lensBlur`, ⌘6); language commands 18 unchanged. New **Lens Blur** develop section (3 controls, 3 commands, shape/brush refinement, per-mask block) is P2 partial. Process versions extend to **V7** (crystal-layer film grain) and **V8** (detail-free Highlights/Shadows base). Lightroom catalog backup `.zip` files import directly. Compressed Olympus/OM ORF sensor support was **withdrawn** pending provenance review: raw coverage becomes **557 / 665 / 187 / 37** of 1,446 (use-weighted ~94%). Survey tiles fit photo shapes and glide; `mask.exportEffects` refuses originals/sidecars; TIFF moved to `craft-tiff` in craft-libs.

## 1. Capability claims -> evidence -> tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | Library is a folder: `catalog.snap` + `catalog.log` (CRC-32 JSON-lines, torn-append repair) | `crates/engine/src/library.rs:1-22`; `crates/catalog/src/journal.rs:1-40` | implemented |
| 2 | Single-writer `catalog.lock`; one process per library | `crates/catalog/src/lock.rs:86` | implemented |
| 3 | 39 importable extensions; support decided by extension, then decoder | `crates/engine/src/import/files.rs` `EXTENSIONS` (39 quoted entries, unchanged at v0.21.1) | implemented |
| 4 | Raw coverage measured per model: 557 verified / 665 unverified / 187 preview / 37 unsupported of 1,446; compressed ORF is preview-only | `docs/raw/coverage.tsv` (column-5 sums); `docs/raw-parity.md:18-24`; `docs/orf-compression.md`; `crates/engine/tests/it/orf_withdrawal.rs` | implemented metric |
| 5 | HEIC decodes in the official packaging behind the `heif` feature | `packaging/macos/package.sh:65` passes `lightcraft/heif`; `nm -gU` on the installed 0.21.1 binary shows 10 `lightcraft_heif` symbols (e.g. `…16decode_thumbnail`); `crates/codecs/Cargo.toml:43-46` still says releases don't ship it (stale) | implemented (feature-gated) |
| 6 | Lightroom catalog import with open/new destination choice, plus direct `.zip` backup import | `crates/engine/src/lightroom_backup.rs`; `crates/engine/src/lightroom_folder.rs`; `crates/engine/src/cmd/library/specs.rs` (`library.importLightroom` params); `docs/lightroom-catalog-import.md:170-200` | implemented (one-way, approximate) |
| 7 | 125 named develop controls + 10 indexed (8 Point Color, 2 Red Eye); 17 sections | `crates/develop/src/controls.rs` (`controls!` rows incl. 3 `lensBlur`; `INDEXED` ids; `enum Section`) | implemented |
| 8 | 41 built-in presets; 22 develop profiles | `crates/engine/src/presets.rs` (41 `p(` rows; `PROFILES` at `:500`, 22 `ProfileInfo`) | implemented |
| 9 | 10 bundled camera profiles | `crates/engine/src/camera_profiles.rs:27` `BUNDLED` (10 tuples; Canon EOS D60 present) | implemented |
| 10 | 52 spectral camera matrices | `crates/raw/src/spectral_table.rs` (52 `Camera {`) | implemented |
| 11 | 10 export formats; validated `ExportOptions` | `crates/engine/src/export/options.rs:5-24` `enum ExportFormat` (10 variants); `crates/engine/src/export.rs` | implemented |
| 12 | `.lcprint` print templates; contact sheet; slideshow PDF/JPEG/AV1 export | `crates/engine/src/print/template.rs:34`; `crates/engine/src/contact_sheet.rs:87-92`; `crates/engine/src/slideshow_export.rs:39-42` | implemented |
| 13 | XMP sidecars with foreign-namespace preservation; `lc:settings`; lens blur is *not* mapped | `crates/meta/src/xmp.rs:18`; `docs/xmp-interop.md` (not-mapped list at `:206`) | implemented (lens blur unmapped) |
| 14 | **368 engine command specs** (+3, zero removed) | non-test `cmd!` ids in `crates/engine/src/cmd/**/*.rs`; 39 `specs()` extend calls in `crates/engine/src/cmd.rs` | implemented |
| 15 | **195 UI commands + 18 language = 213 UI entries; 581 live** | `crates/ui-egui/src/menus/ui_commands.rs` (`UI_COMMANDS`, `LANGUAGE_COMMANDS`); `crates/ui-egui/src/control.rs` `all_commands` | implemented |
| 16 | **Lens Blur**: 3 controls, subject/mask focus, Shape, Focus/Blur brush, per-mask block; partial | `crates/pipeline/src/lens_blur.rs`; `crates/engine/src/cmd/develop.rs:489-631`; `crates/develop/src/settings.rs:1298-1335`; `crates/ui-egui/src/panels/edit/lens_blur.rs`; `crates/ui-egui/src/panels/masking.rs:420-432`; `docs/parity-checklist.md` LR-EDIT-LENSBLUR | partial (no depth map / bokeh shapes / XMP) |
| 17 | **Film grain from crystal layers** (process V7); **V8** detail-free Highlights/Shadows base | `crates/pipeline/src/crystal.rs`; `crates/pipeline/src/local.rs`; `crates/develop/src/settings.rs:81-110`; `docs/grain.md`; `docs/process-versions.md` | implemented |
| 18 | Control channel: loopback, no auth, 16 connections, 4 MiB lines; **29 callable method names** | `apps/lightcraft/src/control_server.rs:22-26`; `crates/ui-egui/src/control.rs` dispatch; `docs/control-protocol.md:1-40` | implemented |
| 19 | MCP: 17 headless / 28 connected helpers, 7 resources, generated `cmd_*` per command (385/609 `tools/list`) | `crates/mcp/src/tools.rs:79` `helper_tools` (17 `tool(` before `if has_ui`, 11 inside); `crates/mcp/src/server.rs:34-40` (7 URIs) | implemented |
| 20 | **11 CLI subcommands**, unchanged; `render`/`merge`/`snapshot`/`calibrate`/`denoise-serve` behaviour | `apps/lightcraft-cli/src/main.rs` dispatch (11 arms) and `USAGE`; file unchanged since v0.19.0 | implemented |
| 21 | Headless CPU UI snapshots (`ui.settle`, `--size`, `--scale`) | `docs/control-protocol.md` "Headless rendering"; `apps/lightcraft-cli/src/main.rs` | implemented |
| 22 | Startup update prompt + self-update via `craft-update`; a ready update installs at exit | `Cargo.toml` `craft-update` rev `6e03f65bf…`; `app.checkForUpdates`; `apps/lightcraft/src/main.rs:201-207` | implemented |
| 23 | Web automation `lightcraft.command(id, params)`; OPFS library; page-host mode | `apps/lightcraft-web/index.html:39-40`; `apps/lightcraft-web/src/automation.rs`; `docs/web.md` | implemented |
| 24 | No document format (no `CFBundleDocumentTypes`); no desktop in-app backup | installed bundle `Info.plist` (key absent); `crates/ui-egui/src/menus.rs:75-77` (backup only when the platform supplies it) | implemented (absence verified) |
| 25 | AI masks are classical except Object/Describe (optional SAM 3, not bundled, empty default mirror list) | `docs/ai-masks.md`; `crates/segment/src/fetch.rs:42` `DEFAULT_MIRRORS: &[]`; `docs/gaps.md` #5 | partial (by design) |
| 26 | User's own DNG camera profiles (`.dcp`) import; none ship | `crates/raw/src/dcp.rs`; `crates/engine/src/cmd/dcp_profiles.rs`; `docs/file-format-parity.md` | implemented |
| 27 | Lensfun database offered on first launch, downloaded on request; pinned per photo | `crates/engine/src/lensfun_download.rs`; `crates/engine/src/cmd/lens_refresh.rs`; `docs/lens-profiles.md` | implemented |
| 28 | Built-in BM3D denoiser needs no weights; GPU-accelerated; ONNX models optional | `crates/denoise-core/src/bm3d.rs`; `crates/gpu/src/bm3d.rs`; `docs/denoise.md` | implemented |
| 29 | Remove Hot Pixels on for newly imported raws, bounded by `app.hotPixelLimit` (default 0.2 %) | `crates/develop/src/lib.rs` `removes_hot_pixels`; `crates/engine/src/cmd/query.rs` `app.hotPixelLimit` | implemented |
| 30 | Export Effect Presets refuses originals/sidecars and writes atomically | `crates/engine/src/cmd/mask_effect_files.rs` (`mask.exportEffects`); `docs/whats-new.md` "Export Effect Presets" | implemented |

## 2. Headline counts: v0.19.0 -> v0.21.1

| Surface | v0.19.0 (measured) | v0.21.1 (measured) | Change |
|---|---:|---:|---|
| Engine command specs | 365 | **368** | +3, zero removed (`lensBlur.brushReset/brushStroke/findSubject`) |
| UI commands | 194 | **195** | +`section.lensBlur` |
| Language commands | 18 | **18** | unchanged |
| Total live commands | 577 | **581** | 368 + 195 + 18 |
| MCP helpers | 17 headless / 28 connected | **17 / 28** | unchanged |
| MCP resources | 7 | **7** | unchanged |
| `tools/list` | 382 / 605 | **385 / 609** | headless = 17+368; connected = 28+581 |
| Control methods | 29 names | **29 names** | unchanged |
| CLI subcommands | 11 | **11** | unchanged |
| Import extensions | 39 | **39** | unchanged at v0.21.1 |
| Export formats | 10 | **10** | unchanged at v0.21.1 |
| Develop controls | 122 + 10 | **125 + 10** | +3 Lens Blur controls |
| Develop sections | 16 | **17** | +LensBlur |
| Built-in presets | 41 | **41** | unchanged at v0.21.1 |
| Develop profiles | 22 | **22** | unchanged at v0.21.1 |
| Bundled camera profiles | 10 | **10** | unchanged at v0.21.1 |
| Spectral matrices | 52 | **52** | unchanged at v0.21.1 |
| Interface languages | 18 | **18** | unchanged at v0.21.1 |
| Process versions | V1–V6 | **V1–V8** | +V7 grain, +V8 Highlights/Shadows |
| Raw coverage tiers | 559/721/129/37 | **557/665/187/37** of 1,446 | compressed ORF withdrawn |
| Use-weighted full decode | ~97% / ~86% verified | **~94% / ~86%** | `docs/raw-parity.md:23-24` |
| Parity summary | 83.5% of 543 (previous skill) | **83.2% of 546** | generated block |

Note: the previous skill's 388 engine / 600 live / 405/628 MCP numbers used the raw `grep -rho 'cmd!'` count, which includes 23 test-only `cmd!` fixtures. The non-test count at v0.19.0 was 365, so the same extraction gives 365 -> 368 here.

## 3. Uncertain / not verified

- MCP totals are derived statically from `helper_tools` and the measured command counts, not captured from a running `tools/list`.
- GUI behaviour was not launched; the command registry, control protocol, parity checklist and packaging are the evidence.
- Lens Blur, crystal grain and process V8 were read from code and docs, not rendered or compared against Lightroom. The project itself marks Lens Blur 🟡 P2.
- HEIC availability is confirmed by `packaging/macos/package.sh:65` and by mangled `lightcraft_heif` symbols in the installed 0.21.1 binary (`nm -gU | grep -i heif`, 10 matches, e.g. `decode_thumbnail`); a source build without the feature does not decode HEIC/HEIF.
- Render fidelity vs Lightroom remains unmeasured by the project (`docs/gaps.md` #1, #3).
- Whether a specific raw variant decodes can only be settled file-by-file; `docs/raw/coverage.tsv` is evidence, not a guarantee for every body that writes the container.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `ROADMAP.md:15` 81.6% of 532 | generated `docs/parity-checklist.md:58`: 83.2% of 546 |
| `docs/target-app-parity.md:15` 83.2% of 543 | generated checklist: 546 in-scope rows |
| `crates/codecs/Cargo.toml:43-46` "releases don't ship heif yet" | `packaging/macos/package.sh:65` builds with `--features lightcraft/heif`; the installed binary has `lightcraft_heif` symbols |
| `docs/gaps.md` #21 says Vietnamese is absent | `crates/ui-egui/src/menus/ui_commands.rs` ships `app.language.vietnamese` |
| `docs/raw-parity.md:25` "9 bundled profiles" | `crates/engine/src/camera_profiles.rs:27` `BUNDLED` has 10 |
| `docs/parity-checklist.md` LRC-DEV-PROCESS row lists process versions only to V7 | `crates/develop/src/settings.rs` defines V8 (latest) and `docs/process-versions.md` documents it |

## 5. Verification commands (read-only)

```sh
git rev-parse HEAD                                              # 361e3bc0c838ffe5e5cea515b1fe5b71951989c6
git diff --stat v0.19.0..HEAD                                   # 235 files, +9,525/−3,929
# engine ids (non-test): cut each cmd file at #[cfg(test)], then extract cmd! ids
# (perl -0777 -ne 'while(/cmd!\(\s*(?:query\s*)?"([^"]+)"/g)')  # 368 at HEAD, 365 at v0.19.0
grep -c 'v.extend(' crates/engine/src/cmd.rs                    # 39 specs() extend calls
awk '/const UI_COMMANDS/,/^\];/' crates/ui-egui/src/menus/ui_commands.rs | grep -cE '^\s+\("'      # 195
awk '/const LANGUAGE_COMMANDS/,/^];/' crates/ui-egui/src/menus/ui_commands.rs | grep -cE '^\s+\("'  # 18
awk '/pub const BUNDLED/,/^\];/' crates/engine/src/camera_profiles.rs | grep -cE '^\s+\("'           # 10
awk '/pub const EXTENSIONS/,/^\];/' crates/engine/src/import/files.rs | grep -oE '"[a-z0-9]+"' | wc -l  # 39
awk '/pub enum ExportFormat/,/^}/' crates/engine/src/export/options.rs | grep -cE '^\s+[A-Z]'       # 10
grep -oE '"[a-z][a-zA-Z0-9]*\.[a-zA-Z0-9.]+" => ' crates/develop/src/controls.rs | wc -l             # 125
awk -F'\t' 'NR>2 {v[$5]++} END {for (k in v) print k, v[k]}' docs/raw/coverage.tsv                   # 557/665/187/37
sed -n '170,200p' apps/lightcraft-cli/src/main.rs | grep -cE '^\s+Some\("'   # 13 = 11 subcommands + version/help
```

## Round 2026-11-12 (refresh)

- Pinned to `v0.21.1` = `361e3bc0c838ffe5e5cea515b1fe5b71951989c6` (installed `lightcraft 0.21.1`).
- Re-measured every headline count at the new tag with the extraction methods above; corrected the previous engine/UI/live/MCP totals after finding the test-fixture overcount.
- Diffed the engine and UI id sets against v0.19.0: only `lensBlur.brushReset`, `lensBlur.brushStroke`, `lensBlur.findSubject` and `section.lensBlur` were added; nothing removed.
- Re-resolved every cited path (129 tokens): removed the dead `crates/raw/src/vendor/orfc.rs` citation with the ORF withdrawal, added `docs/grain.md`, `crates/engine/src/lightroom_backup.rs`, `crates/pipeline/src/{crystal,lens_blur,local}.rs` and `crates/engine/src/read_file.rs`.
- Carried forward untouched capability claims after path/id checks; no fresh file-level or pixel-level exercise of the new features was possible under the round rules.
