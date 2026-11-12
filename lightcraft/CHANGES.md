# LightCraft — round 2026-11-12 changes

Re-pinned: v0.19.0 (`16636c45a63bff3065a6fd31aecc22a6fc15ca53`) -> v0.21.1 (`361e3bc0c838ffe5e5cea515b1fe5b71951989c6`, installed `lightcraft 0.21.1`).

## Corrected / re-measured

- **Method correction — engine command count.** The previous skill's **388** engine commands (and the derived **600** live commands / 628 MCP tools) came from `grep -rho 'cmd!'`, which also counts 23 `cmd!` fixtures inside `#[cfg(test)]` modules. Recounted from non-test code at both tags: **365 at v0.19.0 → 368 at v0.21.1** (+3, zero removed). The live total is **581** (368 engine + 195 UI + 18 language), not 600.
- Engine registry gains `lensBlur.brushReset`, `lensBlur.brushStroke`, `lensBlur.findSubject` (`crates/engine/src/cmd/develop.rs`); zero ids removed.
- `UI_COMMANDS` **194 → 195**, the one addition `section.lensBlur` (⌘6) (`crates/ui-egui/src/menus/ui_commands.rs`); language commands **18 unchanged**.
- MCP `tools/list` **405/628 → 385 headless / 609 connected** (17/28 helper tools + 368/581 commands; 7 resources unchanged). The helper set did not change.
- Develop controls **122 → 125 named** (`+lensBlur.amount`, `+lensBlur.boost`, `+lensBlur.transition`), **10 indexed unchanged** (8 Point Color + 2 Red Eye); sections **16 → 17** (Lens Blur) (`crates/develop/src/controls.rs`).
- Process versions **V1–V6 → V1–V8**: V7 draws film grain from crystal layers, V8 takes the Highlights/Shadows base from a detail-free log-luminance filter (`crates/develop/src/settings.rs`; `crates/pipeline/src/crystal.rs`, `crates/pipeline/src/local.rs`; `docs/process-versions.md`, `docs/grain.md`). The previous skill called V6 "current".
- Raw coverage **559 / 721 / 129 / 37 → 557 verified / 665 unverified / 187 preview-only / 37 unsupported** of 1,446, and use-weighted **~97% → ~94%** fully decode (**~86%** on a verified body unchanged). Cause: compressed Olympus/OM ORF sensor support was withdrawn pending provenance review, so those files are preview-only again (`docs/orf-compression.md`, `crates/engine/tests/it/orf_withdrawal.rs`, `docs/raw/coverage.tsv`).
- Parity summary **83.5% of 543 → 83.2% of 546 in-scope rows** (P0 97.5% of 203, P1 94.2% of 163, P2 57.0% of 179) (`docs/parity-checklist.md:58`). `ROADMAP.md` still prints 81.6% of 532 and `docs/target-app-parity.md` 83.2% of 543 — both lag the generated block.
- **Lens Blur documented as partial**, not as Lightroom parity: Apply / Amount / Boost / Transition, subject-or-mask focus, Shape, Focus/Blur brush refinement, per-mask lens blur; missing an AI depth map (Focal Range, focus picker, Visualize Depth), bokeh shapes and `crs:` XMP mapping (`docs/parity-checklist.md` LR-EDIT-LENSBLUR, 🟡 P2).
- **Lightroom catalog backup zips now import** directly (`.zip`, unpacked to a temporary folder and removed) (`crates/engine/src/lightroom_backup.rs`, `crates/engine/src/lightroom_folder.rs`, `docs/lightroom-catalog-import.md`).
- **Compressed ORF claims deleted** from the skill: the decoder file `crates/raw/src/vendor/orfc.rs` no longer exists; the raw paragraph now says compressed ORF is preview-only and that existing ORF records are rechecked in the background.
- **HEIC evidence corrected:** the installed 0.21.1 binary's Rust symbols are mangled, so `strings` alone finds no `lightcraft_heif::*` names; `nm -gU | grep -i heif` finds 10 `lightcraft_heif` symbols (e.g. `decode_thumbnail`), so HEIC is enabled in the installed build. `packaging/macos/package.sh:65` builds with `lightcraft/heif`.
- **Safety behaviour changes** noted: `mask.exportEffects` refuses a photo original or XMP sidecar and writes atomically (`crates/engine/src/cmd/mask_effect_files.rs`); user-named files are read through an opened regular file under a byte cap (`crates/engine/src/read_file.rs`); raw/HEIF read budgets were tightened (`crates/raw`, `crates/heif`).
- **Survey and grid UI:** survey tiles fit the photos' shapes, centre an incomplete row and glide to new places (`crates/ui-egui/src/panels/compare/survey.rs`); the grid header shows "N selected" and cuts rather than clips an over-wide count (`crates/ui-egui/src/panels/grid.rs`).
- Shared libraries: TIFF/IFD moved out of the repo to `craft-tiff` in craft-libs (`Cargo.toml`, rev `3b310498…`); `craft-update` moved to rev `6e03f65bf…`; `crates/tiff` is gone.

## Method

- `git diff --stat v0.19.0..HEAD`: **235 files changed, +9,525/−3,929** (the shallow checkout still carries the v0.19.0 tree, so the tree diff is authoritative; the compare-API summary in the context file said 235 files).
- Engine ids: for every `crates/engine/src/cmd/**/*.rs` file at each tag, cut the content at the first `#[cfg(test)]`, then extract `cmd!(` ids with `perl -0777 -ne 'while(/cmd!\(\s*(?:query\s*)?"([^"]+)"/g)'`; sort and `comm` the two sets. 365 -> 368, only the three `lensBlur.*` ids added. 39 `specs()` extend calls.
- UI ids: `UI_COMMANDS` rows in `crates/ui-egui/src/menus/ui_commands.rs` extracted with `^\s+\("([^"]+)"`; 194 -> 195. Language rows counted the same way (18).
- MCP helpers: `crates/mcp/src/tools.rs` `helper_tools` — 17 `tool(` calls before `if has_ui`, 11 inside; resources counted from the seven `lightcraft://` constants in `crates/mcp/src/server.rs`.
- CLI: 11 dispatch arms (excluding `--version`/`--help`) in `apps/lightcraft-cli/src/main.rs`; `git diff` shows the file unchanged since v0.19.0.
- Other counts: import extensions from `EXTENSIONS` (39), export formats from `enum ExportFormat` (10), named controls from `controls!` rows including the three one-line `lensBlur` rows (125), indexed controls from `INDEXED` ids (10), presets from `p(` rows (41), develop profiles from `ProfileInfo` rows (22), camera profiles from `BUNDLED` (10), spectral matrices from `Camera {` (52), sections from `enum Section` (17), raw coverage from sums of `docs/raw/coverage.tsv` column 5 (557/665/187/37 = 1,446), parity from the generated `<!-- /parity:summary -->` line.
- Every path cited by the previous SKILL.md was existence-checked against HEAD (129 backtick tokens): only `crates/raw/src/vendor/orfc.rs` was really gone. Line anchors that moved were re-grepped.
- Installed bundle read-only: `Info.plist` `CFBundleShortVersionString`/`CFBundleVersion` 0.21.1, bundle id `ai.storyteller.lightcraft`, no `CFBundleDocumentTypes`; `--version` prints `lightcraft 0.21.1`; no `lightcraft-cli` inside the bundle or on `PATH`. The GUI was never launched.

## Unchanged

- Import extensions **39**, export formats **10**, built-in presets **41**, develop profiles **22**, bundled camera profiles **10**, spectral matrices **52**, interface languages **18** — all explicitly re-measured at v0.21.1 (`git diff` shows those source files unchanged since v0.19.0).
- MCP helper tools **17 headless / 28 connected**, resources **7**; control channel **29 callable method names**, loopback/no-auth, 16 connections, 4 MiB lines; CLI subcommands **11** (`run`, `mcp`, `render`, `snapshot`, `commands`, `merge`, `synth-merge`, `controls`, `denoise-serve`, `calibrate`, `bench-cull`).
- The catalog/journal/lock model, import modes, XMP sidecars, print `.lcprint` templates, contact sheet, slideshow PDF/JPEG/AV1 export, merge (HDR/pano), Apple Photos, face/focus models and the web build's automation surface were not changed by this delta and were carried forward after path checks.
- No `references/` directory (the skill is one file); `agents/openai.yaml` display name and short description remain accurate.

## Known gap in this round

- This is a pin-and-verify refresh, not a fresh deep audit: untouched claims were carried forward after path and id checks. The GUI was not launched (round rule).
- Lens Blur, crystal grain, process V8 and the Lightroom backup import were read from code and the project's own docs, not exercised on files or pixels. Lens Blur is P2 partial by the project's own checklist; do not present it as a depth-map bokeh tool.
- MCP totals are derived statically from `helper_tools` and the measured command counts, not captured from a running `tools/list`.
- Whether a specific raw decodes can only be settled file-by-file; the per-model table is evidence, not a guarantee. Compressed ORF is now preview-only, and the withdrawal note says edits may look different when the camera JPEG replaces sensor data.
