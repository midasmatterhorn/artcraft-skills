# LightCraft — evidence ledger (tag v0.15.0)

Audit basis: this checkout is tag **`v0.15.0`**, commit **`e381c1ae6b2006ce627b243fe41697ce0d9608e0`** (shallow clone
holding exactly this commit). Inspection date **2026-10-29**. Installed `/Applications/LightCraft.app`:
`CFBundleShortVersionString` 0.15.0, `LightCraftBuildCommit` = the same SHA, binary prints `lightcraft 0.15.0`, bundle
id `ai.storyteller.lightcraft`; the GUI was never launched. No `references/` directory.

The v0.14.0 → v0.15.0 wave is small (238 commits): egui 0.37 + craft-ui shared docking (side panels in dock columns),
a startup update prompt with self-update (craft-update), a new Sony ILCE-7RM5 camera profile, HEIC and raw-decoder
hardening, faster full-size exports, Windows per-user install policy, and the shared-module refactor that moved the
command registry from `crates/engine/src/cmd/mod.rs` to `crates/engine/src/cmd.rs`.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | Library is a folder: `catalog.snap` + `catalog.log` (CRC-32 JSON-lines, torn-append repair) | `crates/engine/src/library.rs:1-22`; `crates/catalog/src/journal.rs:1-40` | implemented |
| 2 | Single-writer `catalog.lock`; Windows hard link to an original counts as the original | `crates/catalog/src/lock.rs:86`; PR #3020 | implemented |
| 3 | 39 importable extensions, support decided by extension then decoder | `crates/engine/src/import/files.rs` `EXTENSIONS` (39 quoted entries counted) | implemented |
| 4 | Raw coverage measured: 551 verified / 656 unverified / 202 preview / 37 unsupported of 1,446 | `docs/raw/coverage.tsv` awk sums on the `class` column (generated, test-enforced) — identical to v0.14.0 | implemented metric |
| 5 | HEIC decodes behind the `heif` feature, on in official packaging; hostile-container hardening | `packaging/macos/package.sh:65`; `crates/codecs/Cargo.toml` comment (stale); PR #2770 | implemented (feature-gated) |
| 6 | Lightroom catalog import with open/new destination choice | `crates/ui-egui/src/lightroom_destination.rs:1-30`; `docs/lightroom-catalog-import.md:87` | implemented (one-way, approximate) |
| 7 | 122 named develop sliders + 10 indexed (8 Point Color, 2 Red Eye); 16 sections | `crates/develop/src/controls.rs` `controls!` rows (122 `"id" => ` rows) + `INDEXED` (10 `ControlSpec`) | implemented |
| 8 | 41 built-in presets; 22 develop profiles | `crates/engine/src/presets.rs` (41 `"id", "` rows; `PROFILES` at `:476`, 22 rows) | implemented |
| 9 | **9 bundled camera profiles** (+Sony ILCE-7RM5 this release) | `crates/engine/src/camera_profiles.rs:27` `BUNDLED` — 9 tuple entries, `"ILCE-7RM5"` present | implemented |
| 10 | 52 spectral camera matrices | `crates/raw/src/spectral_table.rs` (52 `Camera {`) | implemented |
| 11 | 10 export formats; validated `ExportOptions` | `crates/engine/src/export/options.rs:5` `enum ExportFormat` (10 variants); `crates/engine/src/export.rs` | implemented |
| 12 | `.lcprint` print templates; contact sheet; slideshow PDF/JPEG/AV1 export | `crates/engine/src/print/template.rs:34`; `crates/engine/src/contact_sheet.rs:87-92`; `crates/engine/src/slideshow_export.rs:40-42` | implemented |
| 13 | XMP sidecars with foreign-namespace preservation; `lc:settings` | `crates/meta/src/xmp.rs:18`; `docs/xmp-interop.md` | implemented |
| 14 | **375 engine command specs** (unchanged) | `grep -rho 'cmd!' crates/engine/src/cmd/` = 375 (multi-line `cmd!(` counted); 39 `specs()` wiring sites in `crates/engine/src/cmd.rs` | implemented |
| 15 | **191 UI commands (+`app.checkForUpdates`) + 18 language = 209; 584 live** | `crates/ui-egui/src/menus/ui_commands.rs`: 209 `("…"` rows; clean table diff vs v0.14.0 `menus.rs` shows +`app.checkForUpdates` only, nothing removed | implemented |
| 16 | Control channel loopback, no auth, 16 connections, 4 MiB lines; 24 arms / 29 method names (set unchanged) | `apps/lightcraft/src/control_server.rs:24-77`; `crates/ui-egui/src/control.rs` match arms | implemented |
| 17 | MCP: 17 headless / 28 connected helpers, 7 resources, generated `cmd_*` per command (392/612 `tools/list`) | `crates/mcp/src/tools.rs:78` `helper_tools`: 17 `tool(` calls before the `if has_ui` block + 11 inside it; `crates/mcp/src/server.rs` 7 `lightcraft://` resources | implemented |
| 18 | 10 CLI subcommands; `render`/`merge`/`snapshot`/`calibrate`/`denoise-serve` behaviour | `apps/lightcraft-cli/src/main.rs` USAGE (10 `lightcraft-cli <sub>` forms) | implemented |
| 19 | Headless CPU UI snapshots (`ui.settle`, `--size`, `--scale`) | `docs/control-protocol.md` "Headless rendering"; `apps/lightcraft-cli/src/main.rs` | implemented |
| 20 | Startup update prompt + self-update via craft-update (new) | `Cargo.toml` `craft-update` pin rev `92d392cf…`; PR #2933; `app.checkForUpdates` UI command | implemented |
| 21 | Web automation `lightcraft.command(id, params)`; OPFS library | `apps/lightcraft-web/index.html:39-40`; `docs/web.md` | implemented |
| 22 | No document format (no `CFBundleDocumentTypes`); no desktop in-app backup | `/Applications/LightCraft.app/Contents/Info.plist`; backup commands wired to platform service only | implemented (absence verified) |
| 23 | AI masks are classical except Object/Describe (optional SAM 3, not bundled, empty mirror list); denoise needs user ONNX | `docs/ai-masks.md`; `docs/denoise.md`; `docs/gaps.md:22,28` | partial (by design) |

## 2. Automation-surface counts: v0.14.0 → v0.15.0

| Surface | v0.14.0 | v0.15.0 (measured) | Change |
|---|---:|---:|---|
| Engine command specs | 375 | **375** | unchanged; registry file moved `cmd/mod.rs` → `cmd.rs` (39 wiring sites, was 37) |
| UI commands | 190 | **191** | +`app.checkForUpdates` (update prompt); nothing removed |
| Language commands | 18 | **18** | unchanged |
| Total live commands | 583 | **584** | 375 + 209 |
| MCP helpers | 17 headless / 28 connected | **17 / 28** | unchanged set; `tools.rs` structure verified |
| MCP resources | 7 | **7** | unchanged |
| `tools/list` | 392 / 611 | **392 / 612** | headless = 17+375; connected = 28+584 |
| Control methods | 24 arms / 29 names | **same set** | `ui.dropFiles` etc. all present |
| CLI subcommands | 10 | **10** | unchanged |
| Import extensions | 39 | **39** | unchanged |
| Export formats | 10 | **10** | unchanged; enum moved to `export/options.rs` |
| Develop controls | 122 + 10 | **122 + 10** | unchanged |
| Built-in presets | 41 | **41** | unchanged |
| Develop profiles | 22 | **22** | unchanged |
| Bundled camera profiles | 8 | **9** | +Sony ILCE-7RM5 (#3022) |
| Spectral matrices | 52 | **52** | unchanged |
| Interface languages | 18 | **18** | unchanged |
| Raw coverage tiers | 551/656/202/37 of 1,446 | **same** | generated table unchanged |

## 3. Uncertain / not verified

- MCP totals derived statically, not from a running `tools/list`.
- GUI behaviour not launched; registry + docs + packaging are the evidence.
- Render fidelity vs Lightroom remains unmeasured by the project itself (`docs/gaps.md:20`).

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `docs/gaps.md:18`, `docs/raw-parity.md` "5 bundled profiles" | 9 in `camera_profiles.rs` `BUNDLED` |
| `docs/raw-parity.md:20-21` headline 201 preview / 38 unsupported | generated `docs/raw/coverage.tsv`: 202 / 37 |
| `ROADMAP.md` / `docs/target-app-parity.md` 81.6% of 532 | generated `docs/parity-checklist.md:58`: 83.5% of 543 |
| `crates/codecs/Cargo.toml` "releases don't ship heif" | `packaging/macos/package.sh:65` passes the feature; installed binary has the symbols |
| `docs/gaps.md:38` "Vietnamese absent" | ships in `crates/ui-egui/src/i18n.rs` |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # e381c1ae6b2006ce627b243fe41697ce0d9608e0
grep -rho 'cmd!' crates/engine/src/cmd/ | wc -l                 # 375
grep -c 'specs()' crates/engine/src/cmd.rs                      # 39 wiring sites
awk '/const UI_COMMANDS/,/^\];/' crates/ui-egui/src/menus/ui_commands.rs | grep -cE '^\s+\("'   # 191
awk '/const LANGUAGE_COMMANDS/,/^];/' crates/ui-egui/src/menus/ui_commands.rs | grep -cE '^\s+\("'  # 18
sed -n '78,345p' crates/mcp/src/tools.rs | grep -cE '^\s+tool\($'  # 17 headless helpers (+11 in if has_ui)
awk '/pub const BUNDLED/,/^];/' crates/engine/src/camera_profiles.rs | grep -cE '^\s+\("'  # 9
awk '/pub const EXTENSIONS/,/^];/' crates/engine/src/import/files.rs | grep -oE '"[a-z0-9]+"' | wc -l  # 39
awk '/pub enum ExportFormat/,/^}/' crates/engine/src/export/options.rs | grep -cE '^\s+[A-Z]'  # 10
grep -cE '^\s+"[a-z]+\.[a-zA-Z.]+" => ' crates/develop/src/controls.rs   # 122 named controls
awk -F'\t' 'NR>2 {v[$5]++} END {for (k in v) print k, v[k]}' docs/raw/coverage.tsv  # 202/37/656/551
```
