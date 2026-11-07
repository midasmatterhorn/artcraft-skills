# LightCraft — round 2026-11-07 changes

Re-pinned: v0.18.0 (`32d569a`) -> v0.19.0 (`16636c45a63bff3065a6fd31aecc22a6fc15ca53`, installed `lightcraft 0.19.0`).

## Corrected / re-measured

- Engine command registry **388** `cmd!` specs (v0.18.0: 379): **+9, zero removed** — `app.hotPixelLimit`, `lens.databaseStatus`, `lens.downloadDatabase`, `library.refreshLensProfiles`, `prefs.backgroundPrep`, `prefs.setBackgroundPrep`, `preset.saveRecipe`, `profiles.camera`, `profile.deleteCamera`.
- `UI_COMMANDS` **195 → 194** (`modelSetup.cancel` removed); 18 language commands unchanged; live total **600** (388 + 194 + 18). The previous skill's 191 UI / 584 total / 375–380 engine numbers were internally contradictory and stale — it had carried the UI count from v0.15.0 while its own round note reported a different command count.
- MCP `tools/list` **405 headless / 628 connected** (17/28 helper tools + 388/600 commands; 7 resources unchanged).
- CLI subcommands **10 → 11**: `bench-cull` added (`apps/lightcraft-cli/src/main.rs` dispatch).
- Bundled camera profiles **9 → 10**: Canon EOS D60 added (`crates/engine/src/camera_profiles.rs` `BUNDLED`).
- Raw coverage **551 / 656 / 202 / 37 → 559 verified / 721 unverified / 129 preview / 37 unsupported** of 1,446 (`docs/raw/coverage.tsv` column sums), because compressed Olympus/OM ORF now decodes from sensor data (`crates/raw/src/vendor/orfc.rs`). Use-weighted **~94% → ~97%** fully decode, **~85% → ~86%** on a verified body.
- Parity summary **83.5% of 543 → 83.1% of 544** (`docs/parity-checklist.md:58`); `ROADMAP.md` still prints 81.6% of 532 (doc drift; the generated block was followed).
- Process versions are **V1–V6** with V6 current, not "V1 + V2" — the develop paragraph was re-stated (`crates/develop/src/settings.rs`).
- Contradicted baseline claims fixed: the lensfun database is now **offered and downloaded on request** (not only `LIGHTCRAFT_LENSFUN_DIR`); the user's own `.dcp` camera profiles **import** (baseline called `.dcp` deliberately unsupported); **Windows WCS monitor profiles are implemented** (`crates/wincolor`); AI Denoise has a **built-in BM3D default** that needs no weights.
- Moved paths re-cited: `crates/ui-egui/src/lightroom_destination.rs` → `crates/ui-egui/src/dialogs/lightroom_destination.rs`; `crates/merge/src/pano/mod.rs` → `crates/merge/src/pano.rs`; `crates/engine/src/presets.rs:476` → `:500`.
- The Sources section was still pinned to v0.16.0 / commit `cdf00cc` after the previous round; it now matches the v0.19.0 audit basis.

## Method

- `git diff --stat v0.18.0..HEAD`: **479 files changed, +50,232/−3,046**. The context file's compare-API summary said 300 files / +None; the tree diff is the truth and the larger figure is reported.
- Command ids extracted with `perl -0777 -ne 'while(/cmd!\(\s*(?:query\s*)?\s*"([^"]+)"/g)'` over `crates/engine/src/cmd/**/*.rs` at `v0.18.0` (via `git show`) and at HEAD, then diffed with `comm`; UI ids extracted the same way from `UI_COMMANDS`; counts cross-checked with the awk methods named in `evidence.md`.
- Other counts: import extensions and export formats from their enum/const tables, develop controls from `controls!` rows, presets from `p(` entries, profiles from `PROFILES`, camera profiles from `BUNDLED`, spectral matrices from `Camera {` entries, languages from `LANGUAGE_COMMANDS`, MCP helpers from `helper_tools` (17 before the `has_ui` block, 11 inside it), CLI subcommands from the dispatch arms.
- Installed bundle inspected read-only: `Info.plist` 0.19.0, `--version` prints `lightcraft 0.19.0`, bundle id `ai.storyteller.lightcraft`, HEIC symbols present, no `CFBundleDocumentTypes`. The bundle contains no `lightcraft-cli` and none is on `PATH`, so live CLI counts were unavailable; all counts are source measurements at the tag.
- Every repo-relative path cited in `SKILL.md` was re-resolved by an existence check against the clone (101 paths; the 2 moved paths were fixed). Line anchors that shifted were re-grepped.

## Unchanged

- Import extensions 39; export formats 10; develop controls 122 + 10; built-in presets 41; develop profiles 22; spectral matrices 52; interface languages 18; MCP helper tools 17/28 and resources 7; control channel 24 arms / 29 method names; the catalog, import, XMP, print, slideshow and merge surfaces the delta did not touch.
- There is no `references/` directory in this skill; `agents/openai.yaml` display name and short description remain accurate.

## Known gap in this round

- This is a pin-and-verify refresh, not a fresh deep audit: untouched capability claims were carried forward after path and id checks. The GUI was not launched (round rule). The new `.dcp` import, lens-database download and built-in BM3D claims are read from code and the project's own docs, not exercised on sample files. The film negative-conversion crate landed as maths only — no engine command, UI or CLI path references it — so it is not documented as a capability.
