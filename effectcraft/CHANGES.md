# EffectCraft — round 2026-11-07 changes

Re-pinned: v0.21.0 (`7870b59`) -> v0.22.0 (`42e3c6a`, installed `effectcraft 0.22.0`).

## Corrected / re-measured

- **After Effects projects were a hard "will not open" and are now a documented subset.** New
  `crates/aep` crate (container, `.aepx` reader, importer, exporter) plus `file.importAep` /
  `file.exportAep`; the limitation is retracted and replaced with the real scope, the loss policy
  (`allowLosses`, `dryRun`, per-category report) and a new reference file.
- **Engine command ids 681 -> 697** (+16, nothing removed). The previous file quoted 681 in one
  place and 608 / 680 / 563-564 elsewhere, from three different extraction methods.
- **Effect parameters 2987 -> 2988** (Cryptomatte's fifth parameter); effects/GPU/categories/partial
  stay 308 / 280 / 21 / 0.
- **Targa is an output format.** The old skill said 13 render formats in its table and 14 in prose
  and never listed Targa; the code says 14 with `TargaSequence` included, at both tags.
- **Built-in presets are 76, not 54** — the 22-preset behavior library was missing from the count.
- **Workspaces are 13, not 15**; **menu/panel catalogs are 13/11, not 11/8**; the inherited
  "18 languages at v0.21.0" figure is contradicted by `CATALOG_CODES` (13) at both tags.
- **AVI imports** (partial: AVI 1.0/OpenDML, MJPEG/H.264/HEVC/uncompressed, no AVI output). The old
  limitation listed AVI as unsupported output *and* implied no import.
- **Startup/Shutdown script folders and script shortcuts exist**, so those two "scripting gaps"
  were deleted; the remaining gaps are `.jsxbin`, a Legacy ExtendScript engine mode and BridgeTalk
  messaging.
- **New surfaces added to the skill**: the Plug-in Library (`library.*`, 8 commands), external
  effect helpers (`effect.helpers.*`, 3 commands, new `crates/helper-host`), native plug-in API 2,
  `effect.plugins.install`, EXR compression/bit-depth output options, `layer.quickSetAnchor`,
  `mask.setRoundness`, and the CLI save lock.
- **Verification protocol and Sources re-dated** to v0.22.0 / `42e3c6a…` / 2026-11-07, with the
  installed bundle's real version and bundle id.
- **Doc drift re-checked**: docs still say 306 effects (five files) and "411 registered engine
  commands"; `README.md` still claims proprietary project formats are unsupported. The old
  "gap 4: no PR CI gate is stale" note is itself stale — the CI gate exists.

## Method

- 203 commits, 512 files, +85,465/−2,251 (`git diff --shortstat v0.21.0..HEAD`).
- One command-id extractor used on both tags: the unique first string argument of every `cmd!` /
  `query!` registry invocation under `crates/` and `apps/` with test trees excluded, multi-segment
  ids matched whole — 702 macro sites / 697 ids at v0.22.0, 686 / 681 at v0.21.0.
- `v0.21.0` was extracted read-only (`git archive`) so every set diff is like-for-like; the clone was
  never modified, built or tested.
- Effects and parameters read from the generated, test-enforced `docs/effects.md`; every other count
  from the literal declaration named in `evidence.md`.
- Every repo path cited by the skill was re-resolved against v0.22.0;
  `crates/ui-egui/src/commands.rs` had moved to `crates/ui-egui/src/menus/commands.rs` and is now
  cited there. Two reference files were added for the surfaces that would otherwise bloat
  `SKILL.md`.
- The installed app was **not** launched and its binary was not executed; version and bundle id come
  from `Info.plist` and the round's recorded `--version` capture.

## Unchanged

- 111 UI-only ids, 36 MCP tools (27 headless + 9 bridge-only) with 2 resources, 24 control methods
  (21 arms), 12 CLI subcommands, 14 render formats, 308 effects / 280 GPU / 21 categories / 0
  partial, 38 blend modes, 9 layer styles, 7 mask modes, 34 panel kinds (+2 parameterised),
  76 presets, 13/11 catalogs. These trees had zero diff or only additive changes that do not
  alter the sets, and each is now marked "unchanged at v0.22.0" in place instead of being left
  undated.
- All previously verified behaviour that the release did not touch (project model, `.ecprojx`,
  autosave/recovery/`repaired`, expressions, tracking, paint, render-settings surface, shortcuts).
  Paths were re-resolved and claims carried forward; none was silently re-dated.

## History folded out of SKILL.md

The v0.19.0 and earlier paragraphs that used to sit in the Overview are kept here, because the skill
now carries only the two most recent deltas:

- **v0.19.0**: SAM 2 — a new `crates/sam2` crate (Hiera backbone, FPN neck, prompt encoder, mask
  decoder, memory encoder/attention) with SAM 2.1 Tiny in the model registry, usable as a
  `MaskModel` and as the Roto Brush object tracker, with a classical fallback and
  `effectcraft-cli bench --roto`. `keys.setMuted` joined the registry (673 -> 674 over v0.18.0).
  Each open composition became a tab in the timeline group's tab row (#2458); exports encode while
  the next batch renders and skip transparent pixels (#2518); Edit-menu keys edit a focused text
  field (#2459); panels moved to craft-ui's shared docking (#2432); egui 0.37; startup update
  prompt with self-update (#2420); Windows installs per-user (#2493); adjustment layers blend in
  their blend mode (#2618); mask copy/paste between layers (#2091).
- **v0.18.0**: maintenance. The effect registry stood at 308 and the registry gained
  `text.deleteSurrounding` over v0.17.0's 672 ids.

## Known gap in this round

- The `.aep` coverage tables come from code plus `docs/aep-{import,export,format}.md`; the corpus
  tests behind them are opt-in and skip themselves without `EFFECTCRAFT_AEP_FIXTURES`, so no
  import/export round trip was executed. Render fidelity figures remain carried, not re-measured.
- The audio extension list is re-exported from the pinned FilmCraft crate, which no local checkout
  matches; it is labelled as carried in the skill rather than asserted as re-derived.
- This is a pin-and-verify refresh, not a new deep audit of every feature.
