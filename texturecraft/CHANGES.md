# TextureCraft — round 2026-11-12 changes

Re-pinned: v0.4.0 (`16e9d21516434a63ac457f49ffd09005f649c02f`) -> v0.6.1
(`34a196190fe2daa2f43017a0f32b254cca4836f2`, installed `TextureCraft 0.6.1 (34a1961 2026-11-12)`).

## Corrected / re-measured

- Engine registry **172 -> 177** command ids. The five added are `bake.preview`, `effect.colorSelection.pick`, `textureSet.meshMap.import`, `tool.fillSelection` and `tool.swapMaskValue`; none were removed (same `cmd!`/`query!` extractor at both tags, tests excluded).
- Menu parity **58/58 -> 59/59**; the new item is Help > Check for Updates (`ui.help.checkForUpdates`, `docs/parity.md`, `crates/ui-egui/src/updates_ui.rs`).
- Control channel **13 -> 15 methods**: `ui.bake.start` and `ui.bake.cancel` are new, and `ui.inspect` now also reports `baking`, `bakeStatus` and `bakePreview` (`crates/ui-egui/src/control.rs`). `auth` is still separate.
- Everything else re-measured and unchanged at v0.6.1: CLI 10 subcommands, MCP 22 tools, serve 17 methods, 31 library filters, 24 smart masks, 72 procedural + 21 smart materials, 23 procedurals, 6 environments, 67 brush alphas, 18 brush presets, 21 channels, 32 blend modes, 10 baked maps, 10 export presets, 8 texture formats, 12 mesh import / 5 mesh export formats, 9 built-in meshes, 10 UI languages, project `format_version` 2. Each is now stated with that date instead of an undated sentence.
- Body counts were re-derived, not carried: the v0.4.0 numbers in the published skill were right for that tag, so this round changed only 177 / 59 / 15 and re-dated the rest.
- New capabilities documented from the diff: live bake preview (streamed, one map at a time, painting paused), bake-mode setup visualization (high poly, cage, UV seams, low poly, missed rays), curvature baked from the mesh by default plus normal-map curvature that follows the surface and curvature-generator detail sizes, batch mesh-map import by file name, movable symmetry plane with axis and angle span, path-tool drafts and editable points, four polygon-fill modes with box selection and 2D-view fills, X inverts the mask paint value, `effect.set` filter swap, ID-color picking, asynchronous layer thumbnails, `ui.json` UI-state storage with RON migration, project open-size budget and parallel project save.
- Doc drift recorded in `evidence.md` §3 (the skill body follows the code, not the docs): `docs/features.md` still lists polygon fill as "triangle, UV island or the whole mesh" (code has triangle / polygon / UV island / mesh) and its symmetry line predates the movable plane and angle span; `ROADMAP.md` still says 63 procedural materials, 30 filters and 19 channels (code: 72 / 31 / 21) and its "Current focus" still talks about releasing v0.1.0.
- Historical delta handling: the v0.3.0 -> v0.4.0 paragraph stays in `SKILL.md` as the single older delta; the v0.2.0 -> v0.3.0 paragraph is folded into this file (below) instead of being carried as a third delta.

## Method

- `git diff --stat v0.4.0..HEAD`: **322 files changed, +30,258/-4,287**. Changed areas: `crates/ui-egui` 130 files, `crates/engine` 83, `crates/bake` 21, `crates/formats` 20, `crates/render` 15, `crates/paint` 9, `crates/core` 8, `crates/compose` 7, `crates/automation` 3, plus apps, packaging, docs and CI. The checkout is a shallow clone with one commit and both release trees, so the diff is reproducible but the commit list is not.
- Id and count sets were extracted from code at both tags: `cmd!`/`query!` ids, `FILTERS` `def(` rows, `SMART_MASKS`, `m(`/`sm(` materials, `ProceduralKind::ALL`, `ENVIRONMENTS`, alpha shapes + glyphs, `PRESETS`, `Channel::ALL`, `BlendMode` variants, `BakedMap::ALL`, `#[tool(` entries, `METHODS`, `SUBCOMMANDS`, `builtin_presets`, `MESH_EXTENSIONS`, `MESH_EXPORT_FORMATS`, `BUILTINS`, `LANGUAGES`; never README/ROADMAP numbers.
- Control methods were counted from the dispatch arms in `crates/ui-egui/src/control.rs` plus the deferred `ui.screenshot`; the v0.4.0 set was extracted from `git show v0.4.0:crates/ui-egui/src/control.rs` with the same rule.
- Every repo-relative path cited in `SKILL.md` was re-resolved against this checkout; all cited paths from the previous skill still exist at v0.6.1, and new citations were checked file by file.
- Installed bundle inspected read-only: `Info.plist` (0.6.1, `ai.storyteller.texturecraft`), `Contents/MacOS` (only `TextureCraft`), `--version` and `--help` only. The GUI was never launched; no build and no test run happened in the checkout.

## Unchanged

- CLI 10 subcommands with the same flags; MCP 22 tools with the same names; serve 17 methods; path confinement and reply budgets (8 MiB JSON, 5 MiB PNG, 256 batch steps); 31 filters; 24 smart masks; 72 procedural + 21 smart materials; 23 procedurals; 6 environments; 67 brush alphas (31 shapes + 36 glyphs); 18 brush presets; 21 channels; 32 blend modes; 10 baked maps; 10 export presets; 8 texture formats with the same per-format depths; 12 mesh import / 5 mesh export formats; 9 built-in meshes; 10 UI languages; `format_version` 2.
- Bake settings model (`model` / `patch` / `preserveEnabled` / `ts`), per-tile `bake.tile.set`, cage and skew paint, and the absence of auto-rebake are all as v0.4.0 described.
- No auto-rebake was added in this release: `bake.run` is still the only batch bake command, and the new preview path belongs to the app's background bake only.

## Known gap in this round

- Pin-and-verify refresh plus a code-diff delta; not a new deep audit. The GUI was not launched, the control channel was not exercised live, and the repo's GPU multipliers (~12x bake, ~25x path tracer) remain unbenchmarked claims.
- The intermediate tags between v0.4.0 and v0.6.1 are not in the shallow checkout, so the delta is measured as one range; individual releases inside it are not attributed.
- The v0.2.0 -> v0.3.0 history below is the previous round's published text, not re-measured (that tag is not in the clone). The v0.3.0 -> v0.4.0 paragraph in `SKILL.md` is likewise carried from the previous round: v0.4.0's id set was re-extracted here, but v0.3.0 is not in the clone, so its 162 ids, 216-file diff and 86-commit compare were not re-derived.

## Older history (folded from SKILL.md)

- **v0.2.0 -> v0.3.0.** 168 files changed; the engine command set grew 135 -> 162 ids (+27: `bake.autoRebake*`, `bake.skew.*`, `brush.preset.*`, `effect.copy/cut/duplicate/histogram/move`, ...), none removed then. Menu parity 55/55. The control channel hardened: owner-only token file, 10 s auth deadline, one attempt per connection, 16-connection cap, 600 s idle.
