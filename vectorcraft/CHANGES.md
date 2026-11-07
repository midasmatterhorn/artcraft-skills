# VectorCraft — round 2026-11-07 changes

Re-pinned: v0.21.0 (`11862f6`) -> v0.22.0 (`654749c`, installed `vectorcraft 0.22.0`).

## Corrected / re-measured

- Engine command specs **886 -> 908 ids** (+22, zero removed): `addon.shapes.*` (box3d, configure, ellipse, polygon, rectangle, spiral, star), `addon.contour.set`, `addon.color.fillToStroke` / `strokeToFill`, `addon.document.batchTraceFolder`, `addon.select.byArtboards` / `byLinkStatus`, `addon.type.releasePath` / `textTweaker`, `document.move`, `select.globalEditExclude`, `select.same.textFillAndStrokeColor`, `stroke.weightUp` / `weightDown`, `text.glyphAlternates` / `setGlyphAlternate`.
- UI commands **410 -> 427**; interface languages **27 -> 28** (new `hi.tsv`; Hindi is a machine-assisted draft with plural rows and no native review; Arabic still has no catalogue).
- `document.save` gained `precision: 0..9` (path anchors/handles rounded to that many decimals; colours, transforms and type stay exact). `vectorcraft-cli run` and `convert` gained `--ppi N`; raster export now defaults to the document's raster-effects resolution when neither `ppi` nor `scale` is given.
- Numbers the body quoted that the code contradicts, fixed: `SAVE_FORMATS` is **7** (adds `eps`), not 6; the format catalogue is **21 formats (19 readable, 20 writable)**, not 24/22; `OPEN_EXTS` is **43** and `PLACE_EXTS` **47**, not 31/34; `ICON_PANELS` is **44**, not 36; MCP exposes **4** URI templates, not 5; the native file `VERSION` is still **4** and the document model `FORMAT_VERSION` is **3**.
- Known-limitation corrections: JPEG 2000 (`.jp2/.jpx/.jpf/.j2k/.j2c/.jpc`), PCX, Pixar and Word 97-2003 `.doc` (Place) are read, so they left the "not supported at all" list (`OPEN_EXTS`, `DOC_EXTS`, `crates/engine/src/cmd/fileio/{jp2read,pcxread,pxrread}.rs`).

## Method

- `git rev-parse HEAD` = `654749c16eb20b6d3182a96defb66e11d1a9649a` (tag `v0.22.0`); `git diff --stat v0.21.0..HEAD` = 858 files changed, +97,302 / -5,778.
- Command ids parsed from every `cmd!(... "id" ...)` literal (both `cmd!` and `query cmd!` forms) at both tags, then set-diffed; the counts quoted are the new sets. UI commands from `UI_COMMANDS`; MCP tools from the `tool(...)` definitions; control arms from `crates/ui-egui/src/control.rs`; formats, effects and languages from their source arrays — the extraction the previous round used.
- Every repo-relative path cited in `SKILL.md` was re-resolved against the clone; only line references moved (`formats.rs:473 -> :509`, `state.rs:160 -> :168`). No build, no test run, no GUI launch; the installed bundle was read (`Info.plist`, `--version` only).
- The older v0.18.0 -> v0.19.0 paragraph was folded out of `SKILL.md` (at most two historical deltas stay there). Its summary: a UX/parity wave with no registry change — Add-ons ▸ Arrange Tools, Smooth section smoothing, Optical kerning, JPEG 2000 import, Export for Screens single-PDF, Intertwine by id/nearest, Eyedropper Shift-click pattern/mesh sampling, Symbols/Brushes delete confirm, PDF/EPS pattern-tile flattening, Batch data-set naming and Objects on Path options.

## Unchanged

- MCP tools (33), control methods (29 canonical / 30 accepted strings), CLI subcommands (7), browser API (9), open/place/save extension sets, the format catalogue (21/19/20), Photoshop-style filters (57), effect catalogue (116), tool ids (94), panels (44) and the native file version (4). Each is dated "unchanged at v0.22.0" in the skill.

## Known gap in this round

- This is a pin-and-verify refresh, not a fresh deep audit: feature sentences outside the delta were path-checked and carried forward, not re-derived from scratch. Parity percentages and localization scores remain project self-assessments.
