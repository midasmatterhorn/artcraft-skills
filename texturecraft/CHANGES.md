# TextureCraft — round 2026-11-07 changes

Re-pinned: v0.3.0 (`85475143fa4d219cc7d60cd039923f57b6c2209c`) -> v0.4.0
(`16e9d21516434a63ac457f49ffd09005f649c02f`, installed `TextureCraft 0.4.0 (16e9d21 2026-11-06)`).

## Corrected / re-measured

- Re-derived every headline count at both tags with one method (see `evidence.md` §2). The published body was stale: it said 82 engine ids, 53/53 menus, 28 filters, 48 materials, 22 procedurals and 9 languages, while v0.3.0 code already had 162 / 55 / 31 / 72 / 23 / 10. Its 18 smart masks were right for v0.3.0. At v0.4.0: **172 engine ids, 58/58 menus, 31 filters, 24 smart masks, 72 procedural + 21 smart materials, 23 procedurals, 10 languages**.
- Baked maps **12 → 10**: `ColorMap` and `WorldDirection` removed; the skill no longer lists them and warns that `colorMap`/`worldDirection` requests are invalid at v0.4.0.
- New bake surface documented: nested per-map `BakeSettings`; `bake.settings` `model`/`patch`/`preserveEnabled`/`ts` targets; `bake.run` returns `{baked, tracer}`; `bake.tile.set`; `bake.cage.paint`/`bake.cage.reset`.
- Removed the auto-rebake claim: `bake.autoRebake`/`bake.autoRebake.run` no longer exist, so the skill now says to call `bake.run` yourself.
- Documented project recovery (`format_version` 2, unreadable bake settings/maps defaulted with a log warning), `file.reimportMesh` marking the project modified, the every-neighbourhood-filter evaluation change, and working-tile baked-map export sampling.
- Fixed CLI examples that could not run as written: `export` needs an output directory, `render` needs an output PNG, `run` shows the input→command→`-o` order, and `mesh_reimport` now shows `preserveStrokes: true` (the default does not re-project paint).

## Method

- `git diff --stat v0.3.0..HEAD`: **216 files changed, +14,040/−5,788** (the GitHub compare lists 86 commits; the shallow clone holds one commit). Changed areas include `crates/{ui-egui,core,engine,bake}` (45/42/41/40 files) and `crates/formats` (12).
- Id and count sets were extracted from code at both tags — `cmd!`/`query!` ids, `FILTERS` `def(` rows, `SMART_MASKS`, `m(`/`sm(` materials, `ProceduralKind::ALL`, `ENVIRONMENTS`, alpha shapes+glyphs, `PRESETS`, `Channel::ALL`, `BlendMode` variants, `BakedMap::ALL`, `#[tool(` entries, `METHODS`, `SUBCOMMANDS`, `builtin_presets`, `MESH_EXTENSIONS`, `MESH_EXPORT_FORMATS`, `LANGUAGES` — never README/ROADMAP numbers.
- Every repo-relative path cited in `SKILL.md` was re-resolved against the checkout; moved files were re-cited (`crates/core/src/bake/`, `crates/engine/src/bake/`, `crates/formats/src/project_file/recovery.rs`), and the old `crates/bake/src/{maps,rays}.rs` paths are gone.
- Installed bundle inspected read-only: `Info.plist` (0.4.0, `ai.storyteller.texturecraft`), `Contents/MacOS` (no CLI), `--version`/`--help` only. GUI never launched.

## Unchanged

- CLI 10 subcommands; MCP 22 tools; serve 17 methods; control 13 methods + `auth`; path confinement and reply budgets; 31 filters; 21 channels; 32 blend modes; 72 + 21 materials; 23 procedurals; 6 environments; 67 brush alphas; 18 brush presets; 10 export presets; 8 texture formats; 12 mesh import / 5 mesh export formats; 9 built-in meshes; 10 UI languages — all unchanged at v0.4.0 and now stated with that date.

## Known gap in this round

- This is a pin-and-verify refresh plus a code-diff delta, not a new deep audit of every feature. The GUI was not launched, the control channel was not exercised live, and the repo's GPU performance multipliers (~12× bake, ~25× path tracer) remain unbenchmarked claims.
- The v0.2.0 -> v0.3.0 historical paragraph was kept as published; the v0.2.0 tag is not in the shallow clone, so it was not re-measured.
