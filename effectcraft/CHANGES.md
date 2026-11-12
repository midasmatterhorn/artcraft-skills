# EffectCraft — round 2026-11-12 changes

Re-pinned: v0.22.0 (`42e3c6a`) -> v0.24.1 (`582344d`, installed `effectcraft 0.24.1`).

## Corrected / re-measured

- **Engine command ids are 703, not 697.** The 697 quoted last round was the count of ids the
  `cmd!`/`query!` extractor can see; the registry also builds three commands from literal
  `CommandSpec { … }` values (`engine.batch` in `crates/engine/src/cmd/batch.rs`,
  `contentFill.generate` and `layer.newContentAwareFill` in `crates/engine/src/cmd/content_fill.rs`),
  so v0.22.0's registry was 700. At v0.24.1 the macro extractor sees 698 ids and five more come
  from outside it (the three above plus `journal.export` and `help.exportRepro` in
  `crates/engine/src/cmd/journal.rs`): **703 total, +3 this release, nothing removed**
  (`layer.unprecompose`, `journal.export`, `help.exportRepro`). `app.capabilities` and
  `effectcraft-cli info` print `command_specs().len()`, which is the registry figure.
- **CLI subcommands are 13, not 12**: `replay SCRIPT.jsonl [--keep-going]` was added
  (`apps/effectcraft-cli/src/main.rs`, `crates/engine/src/replay.rs`). The usage string lists 12
  of them; `bench` is the thirteenth and is documented in the usage body.
- **Workspaces are 15, not 13** (a correction of last round). `WORKSPACES` in
  `crates/ui-egui/src/dock.rs` has 15 entries at both tags; the earlier figure counted the
  `workspace_root` arms instead of the constant.
- **The WebAssembly plug-in ABI is 2, not 1.** `WASM_API_VERSION = 2` and
  `MIN_WASM_API_VERSION = 1` in `crates/effects/src/plugin.rs`: a module still declares
  `ec_api_version` 1 (`ec_render`) or 2 (`ec_render2`, which also receives the layer's previous
  and next frames). The Plug-in Library accepts releases for either ABI
  (`runs_here` in `crates/engine/src/system/library.rs`). The native plug-in API stays 2.
- **72 effect display names were renamed** and their ids kept. The mapping is `RENAMED` in
  `crates/effects/src/display_names.rs`, mirrored by `docs/feature-naming.md`: 69 former `CC …`
  effects, `Lumetri Color` -> `Color Grading`, `Mocha shape` -> `Tracked Shape Matte`,
  `Key Light` -> `Screen Color Key`. Effect ids,
  parameter ids, command ids, enum values, panel ids and serialized names are unchanged, and every
  old display name remains a case-insensitive lookup and search alias
  (`lookup`/`name_matches` in `crates/effects/src/lib.rs`), so old scripts and muscle memory still
  resolve. The renderer is now labelled **GPU Acceleration** / **Software Rendering**, and the
  **Lumetri Scopes** panel's title is **Video Scopes** (its id stays `LumetriScopes`).
- **New replay surface.** `crates/engine/src/replay.rs` (new) defines a JSON-lines repro script
  with `start`/`command`/`expect`/`expect_error`/`expect_no_error` steps; `journal.export` and
  `help.exportRepro` (new `crates/engine/src/cmd/journal.rs`) export the session journal as one;
  `effectcraft-cli replay` runs one headless; `tests/repros/*.jsonl` are replayed by
  `crates/host/tests/it/repros.rs`; the last-resort panic guard drops a crash repro into
  `Repros/`. Documented in `docs/agents.md` §Repro scripts.
- **Un-precompose landed** (`layer.unprecompose {layer?, force?, dryRun?}`, Layer ▸ Un-precompose,
  `crates/engine/src/cmd/layer.rs` + `crates/ui-egui/src/panels/unprecompose.rs`): every reason it
  would change the picture is an error unless `force`, and `dryRun` returns the warnings only.
- **After Effects import grew again.** `crates/aep/src/import/lumetri.rs` (Lumetri Color: master
  RGB curve, Hue vs Sat, colour wheels, ~62 mapped controls), `crates/aep/src/import/puppet.rs`
  (Puppet without meshes/pins, reported per mesh), the 2026-11-05 quick-win block (HDR Highlight
  Compression, Echo, Linear Wipe, Offset, Color Stabilizer), the third-party block (CC Color
  Neutralizer, EXtractoR, IDentifier), keyed/exposed Orientation, placed `.ai`/`.pdf` framed by
  its ArtBox, image sequences without a prefix, and a per-category `unlisted` count in the losses
  report (`crates/aep/src/import/report.rs`). `file.import` now takes `.aep`/`.aepx` (and
  `.ecproj`/`.ecprojx`) and returns them under `projects`; the menus say **Adobe After Effects
  Project…**.
- **Render/GPU behaviour**: `memory.gpuFramesInFlight` (`auto|1|2|3`, `EFFECTCRAFT_GPU_INFLIGHT`)
  sizes the GPU frames in flight from measured memory (`docs/preferences.md`); a saved frame-rate
  override is clamped to the supported rates and says so, and an output module's Crop/Resize is
  capped at 30 000 px per side (`crates/project/src/render_queue.rs`); a decoded footage picture
  uploads once and is shared by every layer that shows it (`crates/gpu/src/upload.rs`, new); the
  disk cache stores the files each cached frame read and re-checks them
  (`crates/render/src/disk_cache/entry_files.rs`, new); CPU is still the reference.
- **Limits and behaviour**: time stretch is held to ±1 % … ±9900 %
  (`crates/project/src/limits.rs`), a numbering gap in an image sequence holds the previous frame
  (`crates/project/src/sequence.rs`), and a text layer's name follows its text until renamed
  (`crates/project/src/layer.rs`, 40 characters on `.aep` import).
- **Control channel while a render waits**: `engine.execute` of `renderQueue.render` and a
  scripted `renderQueue.render()` keep the window responsive; only a whitelist of methods answers
  meanwhile (`ui.inspect`, `ui.elements`, command/menu listings, resize, focus, and the queries in
  the doc), the rest error, and the **Stop Render** button is the automation id `scriptRender.stop`
  (`crates/ui-egui/src/app/frame.rs`, `docs/control-protocol.md`). The transport's 60 s request
  timeout still applies.
- **Confined automation is tighter**: a confined batch step cannot take its params from a
  `$N` reference, and a render refuses an output folder holding a symbolic link that leads outside
  the write roots, including numbered sequence folders (`crates/automation/src/confine.rs`).
- **Doc drift re-checked** (code wins): five docs still say **306 effects**
  (`docs/architecture.md`, `docs/roadmap.md`, `docs/gaps.md`, `docs/hardware-parity.md`,
  `docs/target-app-parity.md`); `docs/target-app-parity.md` still says "411 registered engine
  commands"; `README.md` still says proprietary project formats are unsupported although `.aep`
  interchange landed in v0.22.0; `docs/gaps.md` still rates "Opening existing After Effects work
  ≈ 0% … `.aep` can't be read"; and the `PARITY` string in `crates/engine/src/cmd/query.rs` (what
  `app.capabilities` returns) still says "307 registered" effects where the registry has 308.
- **Verification protocol, Sources and both reference files** re-dated to v0.24.1 / `582344d…` /
  2026-11-12, with the installed bundle's real version and bundle id.

## Method

- Local tree diff `git diff --shortstat v0.22.0..HEAD`: **476 files changed, +35,892/−4,162**.
  The checkout is a two-commit shallow clone, so it carries no commit count; the upstream compare
  API lists 258 commits but caps its file list at 300, which is why the file count here comes from
  the local diff instead.
- One command-id extractor on both tags (the unique first string argument of every `cmd!` /
  `query!` registry invocation under `crates/` and `apps/`, test trees excluded, multi-segment ids
  matched whole): 702 macro sites / 697 ids at v0.22.0, 703 / 698 at v0.24.1. Added to that, the
  five ids built without those macros at HEAD (three literal `CommandSpec` values, two from
  `journal.rs`'s `spec()` helper) and the three at v0.22.0 give 700 -> 703.
- `v0.22.0` was extracted read-only with `git archive` into a temp directory so every set and
  count diff is like-for-like; the clone was never modified, built or tested.
- Effects and parameters read from the generated, test-enforced `docs/effects.md`; every other
  count from the literal declaration named in `evidence.md`.
- Every repo path cited by the skill and both references was re-resolved against v0.24.1; no cited
  path had moved. New paths were added for the replay, un-precompose, naming, AEP and confinement
  surfaces.

## Unchanged

- 111 UI-only ids (`crates/ui-egui/src/menus/commands.rs`), 36 MCP tools (27 headless + 9
  bridge-only) with 2 resources, 24 control methods over 21 arms, 14 Render Queue formats,
  308 effects / 2988 parameters / 280 GPU / 21 categories / 0 partial, 38 blend modes, 9 layer
  styles, 7 mask modes, 34 panel kinds (+2 parameterised), 76 built-in presets (8/23/23/22),
  13 menu / 11 panel catalogs, 8 `library.*`, 3 `effect.helpers.*`, 3 `effect.plugins.*`
  commands, helper protocol v1 and native plug-in API 2. Each is marked "unchanged at v0.24.1" in
  place in `SKILL.md`.
- Previously verified behaviour the release did not touch: the project model and `.ecprojx`,
  autosave/`repaired`, expressions, tracking/roto/paint, render settings surface, shortcut data,
  import format lists (stills 17, video 7, models 5, data 3, interchange 6). Paths were re-resolved
  and claims carried forward; none was silently re-dated.

## History folded out of SKILL.md

The skill now carries only the two most recent deltas. The v0.19.0 -> v0.21.0 paragraph that used
to sit there is kept here:

- **v0.21.0**: `comp.deleteAllMarkers` joined the registry (which the macro extractor put at 681
  ids); shortcut scopes (panel and context, one chord per scope); a `colr` atom in ProRes MOV
  exports; a bounded encryption pre-scan after each PDF trailer; Japanese catalog rows.
- **v0.19.0**: SAM 2 — a new `crates/sam2` crate (Hiera backbone, FPN neck, prompt encoder, mask
  decoder, memory encoder/attention) with SAM 2.1 Tiny in the model registry, usable as a
  `MaskModel` and as the Roto Brush object tracker, with a classical fallback and
  `effectcraft-cli bench --roto`. `keys.setMuted` joined the registry. Each open composition
  became a tab in the timeline group's tab row; exports encode while the next batch renders and
  skip transparent pixels; panel docking moved to craft-ui's shared model; egui 0.37; startup
  update prompt with self-update; Windows installs per-user; adjustment layers blend in their
  blend mode; mask copy/paste between layers.

## Known gap in this round

- **No `effectcraft-cli` binary exists on the authoring machine** (the macOS `.app` ships only the
  app binary), so `command_specs().len()`, `info --json`, `commands --json` and `app.capabilities`
  were **not executed**. The 703 figure is a static count of the registry's ids with the method
  above; run `effectcraft-cli info --json` on a real install to confirm it.
- The `.aep` coverage tables come from code plus `docs/aep-{import,export,format}.md`; the corpus
  tests behind them are opt-in and skip themselves without `EFFECTCRAFT_AEP_FIXTURES`, so no
  import/export round trip was executed.
- Render fidelity figures remain carried from `docs/fidelity/README.md`, not re-measured; the
  audio extension list is still re-exported from the pinned FilmCraft crate and labelled as
  carried.
- This is a pin-and-verify refresh, not a new deep audit of every feature.
