# LightCraft — evidence ledger (tag v0.19.0)

Audit basis: this checkout is tag **`v0.19.0`**, commit **`16636c45a63bff3065a6fd31aecc22a6fc15ca53`**, release dated 2026-11-06; inspection date **2026-11-07**. Installed `/Applications/LightCraft.app` matches the tag (`CFBundleShortVersionString` 0.19.0, binary prints `lightcraft 0.19.0`); bundle id `ai.storyteller.lightcraft`; the GUI was never launched. No `references/` directory.

v0.18.0 → v0.19.0 delta: **+9 command ids, zero removed** (multiline non-test extract 379 → 388):
`app.hotPixelLimit`, `lens.databaseStatus`, `lens.downloadDatabase`, `library.refreshLensProfiles`,
`prefs.backgroundPrep`, `prefs.setBackgroundPrep`, `preset.saveRecipe`, `profiles.camera`,
`profile.deleteCamera`. `UI_COMMANDS` 195 → 194 (`modelSetup.cancel` removed); CLI gains `bench-cull`
(10 → 11); bundled camera profiles 9 → 10 (Canon EOS D60); raw coverage 559/721/129/37 (compressed
Olympus/OM ORF now decodes); process versions V1–V6 (V6 current). New surfaces: user `.dcp` camera
profiles, on-request lensfun database download (56 files, ~5 MB, pinned), built-in BM3D denoise that
needs no weights, Remove Hot Pixels on for newly imported raws, Windows monitor ICC profiles, web
page-host mode (`?host=parent`). 479 files changed, +50,232/−3,046.

The v0.17.0 → v0.18.0 wave was correctness-only with **+4 ids, zero removed**: `keyword.setShortcut`,
`keyword.shortcut`, `keyword.toggleShortcut`, `photo.clearLabel`; "Integration r3" (178 PRs), an
accessibility pass, Auto Import concurrency (#3409), ≥2×-source Develop exports (#3281), faster person
look-alikes (#3286), folder-rename protection (#3276), crop-ratio box (#3235), EXIF/HTTP hardening.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | Library is a folder: `catalog.snap` + `catalog.log` (CRC-32 JSON-lines, torn-append repair) | `crates/engine/src/library.rs:1-22`; `crates/catalog/src/journal.rs:1-40` | implemented |
| 2 | Single-writer `catalog.lock`; Windows hard link to an original counts as the original | `crates/catalog/src/lock.rs:86`; PR #3020 | implemented |
| 3 | 39 importable extensions, support decided by extension then decoder | `crates/engine/src/import/files.rs` `EXTENSIONS` (39 quoted entries counted) | implemented |
| 4 | Raw coverage measured: 559 verified / 721 unverified / 129 preview / 37 unsupported of 1,446; compressed ORF now decodes | `docs/raw/coverage.tsv` awk sums on the `class` column (generated, test-enforced); `crates/raw/src/vendor/orfc.rs`; `docs/raw-parity.md:12-17` | implemented metric |
| 5 | HEIC decodes behind the `heif` feature, on in official packaging; hostile-container hardening | `packaging/macos/package.sh:65` passes `lightcraft/heif`; installed 0.19.0 binary has 5 `lightcraft_heif` symbols; `crates/codecs/Cargo.toml` comment is stale | implemented (feature-gated) |
| 6 | Lightroom catalog import with open/new destination choice | `crates/ui-egui/src/dialogs/lightroom_destination.rs`; `docs/lightroom-catalog-import.md:87` | implemented (one-way, approximate) |
| 7 | 122 named develop sliders + 10 indexed (8 Point Color, 2 Red Eye); 16 sections | `crates/develop/src/controls.rs` `controls!` rows (122 `"id" => ` rows) + `INDEXED` (10 `ControlSpec`) | implemented |
| 8 | 41 built-in presets; 22 develop profiles | `crates/engine/src/presets.rs` (41 `p(` preset entries; `PROFILES` at `:500`, 22 `ProfileInfo` rows) | implemented |
| 9 | **10 bundled camera profiles** (+Canon EOS D60) | `crates/engine/src/camera_profiles.rs:27` `BUNDLED` — 10 tuple entries, `"Canon EOS D60"` present | implemented |
| 10 | 52 spectral camera matrices | `crates/raw/src/spectral_table.rs` (52 `Camera {`) | implemented |
| 11 | 10 export formats; validated `ExportOptions` | `crates/engine/src/export/options.rs:5` `enum ExportFormat` (10 variants); `crates/engine/src/export.rs` | implemented |
| 12 | `.lcprint` print templates; contact sheet; slideshow PDF/JPEG/AV1 export | `crates/engine/src/print/template.rs:34`; `crates/engine/src/contact_sheet.rs:87-92`; `crates/engine/src/slideshow_export.rs:40-42` | implemented |
| 13 | XMP sidecars with foreign-namespace preservation; `lc:settings` | `crates/meta/src/xmp.rs:18`; `docs/xmp-interop.md` | implemented |
| 14 | **388 engine command specs** (+9, zero removed) | `grep -rho 'cmd!' crates/engine/src/cmd/` = 388 (multi-line `cmd!(` counted); 41 `specs()` wiring sites in `crates/engine/src/cmd.rs` | implemented |
| 15 | **194 UI commands + 18 language = 212; 600 live** | `crates/ui-egui/src/menus/ui_commands.rs`: 194 + 18 `("…"` rows; id diff vs v0.18.0 removes `modelSetup.cancel` only | implemented |
| 16 | Control channel loopback, no auth, 16 connections, 4 MiB lines; 24 arms / 29 method names (set unchanged) | `apps/lightcraft/src/control_server.rs:24-77`; `crates/ui-egui/src/control.rs` match arms | implemented |
| 17 | MCP: 17 headless / 28 connected helpers, 7 resources, generated `cmd_*` per command (405/628 `tools/list`) | `crates/mcp/src/tools.rs:79` `helper_tools`: 17 `tool(` calls before the `if has_ui` block + 11 inside it; `crates/mcp/src/server.rs` 7 `lightcraft://` resources | implemented |
| 18 | **11 CLI subcommands**, incl. `bench-cull`; `render`/`merge`/`snapshot`/`calibrate`/`denoise-serve` behaviour | `apps/lightcraft-cli/src/main.rs` dispatch (11 arms) and USAGE | implemented |
| 19 | Headless CPU UI snapshots (`ui.settle`, `--size`, `--scale`) | `docs/control-protocol.md` "Headless rendering"; `apps/lightcraft-cli/src/main.rs` | implemented |
| 20 | Startup update prompt + self-update via `craft-update` | `Cargo.toml` `craft-update` pin rev `a231e517…`; `app.checkForUpdates` UI command | implemented |
| 21 | Web automation `lightcraft.command(id, params)`; OPFS library; page-host mode | `apps/lightcraft-web/index.html:39-40`; `apps/lightcraft-web/src/host.rs` (`?host=parent`); `docs/web.md` | implemented |
| 22 | No document format (no `CFBundleDocumentTypes`); no desktop in-app backup | `/Applications/LightCraft.app/Contents/Info.plist` (plist key absent); backup commands wired to platform service only | implemented (absence verified) |
| 23 | AI masks are classical except Object/Describe (optional SAM 3, not bundled, empty mirror list) | `docs/ai-masks.md`; `docs/gaps.md:22` | partial (by design) |
| 24 | User's own DNG camera profiles (`.dcp`) import as camera profiles; none ship | `crates/raw/src/dcp.rs`; `crates/engine/src/cmd/dcp_profiles.rs` (`profiles.camera`, `profile.deleteCamera`); `docs/file-format-parity.md:51` | implemented |
| 25 | Lensfun database offered on first launch, downloaded on request; pinned per photo | `crates/engine/src/lensfun_download.rs`; `crates/engine/src/cmd/lens_refresh.rs` (`lens.databaseStatus`, `lens.downloadDatabase`, `library.refreshLensProfiles`); `docs/lens-profiles.md` | implemented |
| 26 | Built-in BM3D denoiser needs no weights; GPU-accelerated; ONNX models optional | `crates/denoise-core/src/{builtin,bm3d}.rs`; `crates/gpu/src/bm3d.rs`; `docs/denoise.md:8-40` | implemented |
| 27 | Remove Hot Pixels on for newly imported raws, bounded by `app.hotPixelLimit` (default 0.2 %) | `crates/develop/src/lib.rs` `removes_hot_pixels`; `crates/engine/src/cmd/query.rs` `app.hotPixelLimit` | implemented |

## 2. Headline counts: v0.18.0 → v0.19.0

| Surface | v0.18.0 (measured) | v0.19.0 (measured) | Change |
|---|---:|---:|---|
| Engine command specs | 379 | **388** | +9, zero removed |
| UI commands | 195 | **194** | −`modelSetup.cancel` |
| Language commands | 18 | **18** | unchanged |
| Total live commands | 592 | **600** | 388 + 194 + 18 |
| MCP helpers | 17 headless / 28 connected | **17 / 28** | unchanged |
| MCP resources | 7 | **7** | unchanged |
| `tools/list` | 396 / 620 | **405 / 628** | headless = 17+388; connected = 28+600 |
| Control methods | 24 arms / 29 names | **same set** | unchanged |
| CLI subcommands | 10 | **11** | +`bench-cull` |
| Import extensions | 39 | **39** | unchanged |
| Export formats | 10 | **10** | unchanged |
| Develop controls | 122 + 10 | **122 + 10** | unchanged |
| Built-in presets | 41 | **41** | unchanged |
| Develop profiles | 22 | **22** | unchanged |
| Bundled camera profiles | 9 | **10** | +Canon EOS D60 |
| Spectral matrices | 52 | **52** | unchanged |
| Interface languages | 18 | **18** | unchanged |
| Raw coverage tiers | 551/656/202/37 | **559/721/129/37** of 1,446 | compressed ORF decoded |
| Use-weighted full decode | ~94% / ~85% verified | **~97% / ~86%** | `docs/raw-parity.md:20-25` |

## 3. Uncertain / not verified

- MCP totals derived statically, not from a running `tools/list`.
- GUI behaviour not launched; registry + docs + packaging are the evidence.
- Render fidelity vs Lightroom remains unmeasured by the project itself (`docs/gaps.md:18`).
- `.dcp` import, lens-database download and BM3D quality were read from code/docs, not exercised on files.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `ROADMAP.md:15` 81.6% of 532 | generated `docs/parity-checklist.md:58`: 83.1% of 544 |
| `crates/codecs/Cargo.toml` "releases don't ship heif" | `packaging/macos/package.sh:65` passes the feature; installed 0.19.0 binary has the symbols |
| `docs/gaps.md:38` "Vietnamese absent" | ships in `crates/ui-egui/src/i18n.rs` |

The previous round's raw-parity drift (201/38 vs 202/37) and PSD-write drift are gone: the raw
headline now prints 559/721/129/37, and `docs/file-format-parity.md:21` marks PSD export ✅.

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # 16636c45a63bff3065a6fd31aecc22a6fc15ca53
grep -rho 'cmd!' crates/engine/src/cmd/ | wc -l                 # 388
grep -c 'specs()' crates/engine/src/cmd.rs                      # 41 wiring sites
awk '/const UI_COMMANDS/,/^\];/' crates/ui-egui/src/menus/ui_commands.rs | grep -cE '^\s+\("'   # 194
awk '/const LANGUAGE_COMMANDS/,/^];/' crates/ui-egui/src/menus/ui_commands.rs | grep -cE '^\s+\("'  # 18
awk '/pub const BUNDLED/,/^\];/' crates/engine/src/camera_profiles.rs | grep -cE '^\s+\("'  # 10
awk '/pub const EXTENSIONS/,/^\];/' crates/engine/src/import/files.rs | grep -oE '"[a-z0-9]+"' | wc -l  # 39
awk '/pub enum ExportFormat/,/^}/' crates/engine/src/export/options.rs | grep -cE '^\s+[A-Z]'  # 10
grep -cE '^\s+"[a-z]+\.[a-zA-Z.]+" => ' crates/develop/src/controls.rs   # 122 named controls
awk -F'\t' 'NR>2 {v[$5]++} END {for (k in v) print k, v[k]}' docs/raw/coverage.tsv  # 559/721/129/37
grep -nE '^\s+Some\("' apps/lightcraft-cli/src/main.rs | wc -l   # 11 subcommands
```

## Round 2026-11-07 (refresh)

- Pinned to `v0.19.0` = `16636c45a63bff3065a6fd31aecc22a6fc15ca53` (installed `lightcraft 0.19.0`).
- Re-measured every headline count above with the extraction methods in this file; the engine, UI, MCP, CLI, camera-profile and raw-coverage numbers moved, the rest were explicitly re-measured as unchanged.
- Id sets were diffed between the two tags with the same extraction as the claims above; fixed two moved paths and the stale v0.16.0 Sources pin.
