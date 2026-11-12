# VectorCraft — round 2026-11-12 changes

Re-pinned: v0.22.0 (`654749c16eb20b6d3182a96defb66e11d1a9649a`) -> v0.24.1 (`f4922aa7ac99a4f6d56fc68a83a44945207ec610`, installed `vectorcraft 0.24.1`).

## Corrected / re-measured

- Engine command specs **908 -> 955 ids** (+47, zero removed): `script.run`/`stop`/`engines`/`engine.drop`/`console`/`console.clear`/`listInstalled`, `svgFilter.apply`/`define`/`delete`/`import`/`list`, the eight `text.spelling.*` commands, four `type.compositeFonts.*`, `type.dynamicText`, `text.setPathHandle`, `assets.add3D`/`export3D`/`set3DFormat`, `plugin.clearCache`/`safeMode`/`setEnabled`, `prefs.export`/`import`, `document.compare`, `edit.newDocumentFromState`, `engine.apiReference`, `actionSet.read`, `artboard.rename`/`switchOrientation`, `object.setPixelAligned`/`select.object.notAlignedToPixelGrid`, `effect.deferredStatus`/`refreshDeferred`, `symbol.instance.resetTransform`/`selectPart`/`sortByName`.
- UI commands **427 -> 453**; panels (`ICON_PANELS`) **44 -> 47** (Color Wheel, 3D and Materials, Script Console).
- Browser API **9 -> 11** calls: the shared `PageApi` now installs `docInspect` and `uiInspect` beside `request`, `execute`, `commands` and `screenshot`; the app adds `inspect`, `openFile`, `captureDownloads`, `files`, `readFile`.
- MCP fixed resources **3 -> 4** (`vectorcraft://commands/reference`, Markdown from `engine.apiReference`); URI templates stay **4**. Prompts **5 -> 8** (+`check-spelling`, `variables-bind`, `path-tools`). The previous list (`poster, brief, palette, text, subject`) was wrong: `brief`, `palette`, `text` and `subject` are arguments of the `poster` prompt. The five that carried over are `poster`, `icon-set`, `recolor`, `trace-and-style`, `export-set`.
- Open extensions **43 -> 46**, place extensions **47 -> 50**: `.heic`, `.heif` (HEVC stills) and `.jxl` (JPEG XL first frame) are now read.
- Format catalogue restated: `FORMATS` holds **29 entries** at this tag — 21 `Format { … }` blocks plus 8 read-only one-line `reader(…)` entries — of which **27 read and 20 write**, plus `plugin.<id>` importers/exporters. The old row "21 (19 read, 20 write)" counted the blocks only and omitted the six `reader()` entries that already existed at v0.22.0; measured the same way, v0.22.0 is 27 (25 read, 20 write).
- Effect catalogue **116 -> 118**: 91 direct entries (82 quoted ids + 9 shared constants: the four 3D types, `CLASSIC_EXTRUDE`, Trap, Crop Marks, Rasterize and `SVG_FILTER`) + 15 warp styles + 12 Pathfinder effects. Illustrator effects are now **50/50** (`docs/effects-parity.md`) because the SVG Filters submenu is implemented, not a stub.
- Feature claims the code contradicts, corrected: reference-app scripting is still not supported, but **JavaScript scripts do run** through a new ES5.1/E4X engine (`crates/js`, `crates/engine/src/script/`, `script.run`); PSD/PSB now **open with layers** (place stays merged); HEIC/HEIF and JPEG XL are read; **3D assets export** as OBJ/glTF/USDA/USDZ; **spell check**, Auto Spell Check and the custom dictionary ship (the Check Spelling dialog is still a stub); plug-ins gained **API level 2** host imports, permissions/grants, importers and command calls. The previous "artboard background colours are left out of exports" limitation was stale: exports draw them behind the art by default (`includeArtboardFill`, `crates/engine/src/cmd/fileio/export.rs`).
- Doc/code drift found: `docs/mcp.md` still advertises "Three fixed resources" (code: 4); `docs/file-format-parity.md` still has a summary row saying HEIC/HEIF and PS are missing while its detail rows say they are read; `docs/effects-parity.md`'s header says 49/50 while its table says 50/50; `README.md` "What's missing" still lists scripting; `ROADMAP.md` and `docs/target-app-parity.md` lag the code at 348/353 menu items, 89/92 tools and 46/50 effects.

## Method

- `git rev-parse HEAD` = `f4922aa7ac99a4f6d56fc68a83a44945207ec610` (tag `v0.24.1`, 2026-11-11); `git diff --shortstat v0.22.0..HEAD` = 1,304 files changed, +242,142 / -11,521. The shallow checkout has only the two release snapshots, so the local diff — not the compare API's commit count — is the evidence.
- Command ids parsed from every `cmd!(…)` and `query cmd!(…)` literal under `crates/engine/src/` at both tags and set-diffed; UI commands from the 453 four-tuples in `UI_COMMANDS`; MCP tools from 31 multi-line `tool(` blocks plus `undo`/`redo`; prompts from the 8 top-level `PromptDef` entries; resources/templates from `list()`/`TEMPLATES`; control methods from the `match` arms; formats from `FORMATS`, `OPEN_EXTS`, `PLACE_EXTS`, `SAVE_FORMATS`; effects from `effect_catalog()`, `WARP_STYLES`, `PATHFINDER_EFFECTS`, `PIXEL_EFFECTS`; panels, tools and languages from their source arrays.
- No build, no test run, no GUI launch; the installed bundle was only read (`Info.plist`, `--version`). Every path cited in `SKILL.md` was re-resolved against this checkout.
- The older v0.19.0 -> v0.21.0 delta paragraph was folded out of `SKILL.md` (at most the two most recent historical deltas stay there); its gist is the Add-ons Arrange/Cleanup wave, nearest-swatch snapping, dash expansion, symbol lifecycle commands, DXF ellipse/line fixes and the opacity-mask/gradient-mesh fixes.

## Unchanged

- MCP tools **33**, control methods **29 canonical / 30 accepted strings**, CLI subcommands **7**, save formats **7**, Photoshop-style filters **57**, tool ids **94**, interface languages **28** (27 `.tsv` + English), native file `VERSION` **4** and document `FORMAT_VERSION` **3**. Each is dated "unchanged at v0.24.1" in the skill.

## Known gap in this round

- This is a pin-and-verify refresh, not a fresh deep audit: feature sentences outside the delta were path-checked and carried forward, not re-derived from scratch; parity percentages and localization scores remain project self-assessments.
- The JavaScript engine is documented from its command/limits code and CLI test, not exercised against a live app. Reference-app `.jsx` scripts still lack the Illustrator document object model, so most will fail even though the static checker understands them.
- The block-only "21 formats" figure was corrected here; other rounds may still quote it.
