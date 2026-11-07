# DeckCraft — round 2026-11-07 changes

Re-pinned: v0.15.0 (`3e178d8f5a59c787a6a53a7ed0f052b3e4a1489f`) -> v0.16.0 (`a3e2254d3de32ed1718f156f070b54a34b949b54`, installed `deckcraft 0.16.0`).

## Corrected / re-measured

- Counts corrected: UI commands 51 -> **52** (15 with shortcuts); control methods "26 names" -> **25 canonical + 2 aliases** (27 accepted strings). Re-measured and confirmed unchanged: **107** animation entries (24/17/23/40/3) and **183** shape presets — a naive per-line count reports 106 and 182 because `customPath` and `accentBorderCallout3` are each written across several lines.
- The previous round's note "234 ids; 306 `cmd!` sites" was a miscount: it is **329 ids on 329 `cmd!` sites** at both tags (234 is the ordinary-kind subset). Command set unchanged; nothing added or removed between the tags.
- `file.save`/`file.saveAs`/`run --save` for `.png`/`.jpg`/`.jpeg` is now **refused** by `save_bytes` ("use file.export") instead of writing native zip bytes under the image name; the caution is rewritten, and the remaining fall-through for other unmapped extensions is now called out.
- Handout `perPage` is **exactly 1/2/3/4/6/9** (no longer clamped 1–9); `view.slideMaster` rejects an invalid `master`/`layout`; table cell commands reject malformed `cells` and out-of-table cells; `comment.next`/`prev` reject a malformed `index`.
- Save temporary sibling renamed to a hidden **`.deckcraft.<pid>.<n>.saving`** beside the target and checked against the automation write root; native `presentation.json` capped at **256 MiB**; notes page clamped to the slide-size bounds.
- Fixed a wrong caution: **animation rewind does round-trip** (`fill="remove"`). The remaining media gap (#74) is narrower than the old text said: trim, fades, bookmarks and the document-level show-media-controls flag round-trip; volume, autoplay, loop, rewind, play-across-slides, hide-while-not-playing and full-screen stay model-only.
- Fixed a second wrong claim: **OMML is read and written** (`RunKind::Math` → `a14:m`) though not authored or typeset — the Equation dialog still inserts pretty-printed text. Corrected the Windows packaging note too: the MSI declares `perUserOrMachine`, so the launcher chooses the scope.
- Re-cited the four moved paths that the v0.15.0 reference named wrongly: the command registry is `crates/engine/src/cmd.rs`, the PPTX readers and writers are `crates/pptx/src/read.rs` and `crates/pptx/src/write.rs`, and the pattern gallery is `crates/ui-egui/src/panels/fillui.rs`. Automation roots: both flags and both spellings repeat (the old "a repeated flag is an error" was wrong).
- Doc drift refreshed: `docs/architecture.md` 320 and `docs/target-app-parity.md` 328 commands vs the code's 329; `format.align`'s parameter doc omits its new `thaiDist` value; the control-protocol, animation-parity, gaps and ROADMAP staleness list is unchanged and still accurate.

## Method

- 144 files changed, +6 733/−717 between `v0.15.0` and `HEAD`; the pinned checkout is shallow and squashed, so the tag-to-tag diff is the delta evidence.
- Every set was extracted twice, at `v0.15.0` and at `HEAD`, with the same parser, then diffed: `cmd!` id literals and their kind prefixes (329/234-57-38), shortcut arguments, `tool(` names in `crates/mcp/src/tools.rs`, the `match req.method` arms in `crates/ui-egui/src/control.rs`, `UI_COMMANDS` tuple starts, `SUBCOMMANDS` in `apps/deckcraft-cli/src/help.rs`, `TRANSITIONS`/`ANIMATIONS`, `CATALOG` in `crates/geom/src/preset/catalog.rs` and `crates/geom/src/warp.rs`, the theme/chart/SmartArt/starter/icon/pattern/date-format/3-D registries, and the workspace for any locale catalogue. Nothing was taken from README or release notes.
- The installed bundle was inspected read-only (`Info.plist`, `codesign`, `spctl`, `stapler`) and its binary was run with `--version` and `--help` only, both of which return before eframe starts. No GUI was launched, nothing was built, and the clone was not modified.
- Every repo-relative path cited in `SKILL.md` and `references/commands-and-formats.md` was re-resolved against this checkout; the four that no longer exist were re-cited.

## Unchanged

- The automation registry is identical id-for-id at both tags: 329 engine commands, 57 shortcuts, 25 MCP tools, 25 control methods, 12 CLI subcommands. So are the 49 transitions, 8 themes × 4 variants, 11 layouts + `Custom`, 28 chart types, 45/9/17 SmartArt, 6 starters, 70 icons, 40 warps, 48/54 pattern fills, 28/62 cameras, 12 bevels, 12 materials, 15 light rigs, 13 date formats and the single (English) UI language.
- File-format bounds carried forward after re-reading the code: PNG scale clamp 0.01–16, GIF 16–3840 px / 0.1–600 s / ≤500 frames / ≤200M pixels, PDF dpi 200 clamped 36–600 with a 64M-pixel raster cap, and the native 2 GiB per-entry / 4 GiB total / 100 000-item budgets.
- craft-libs stays at `c5a1cbfb5f9049f9270955caffb5bee5997aebf7` (the web app adds `craft-web-host` at `2e2312dd…`).
- Folded out of `SKILL.md` (older than the two kept historical delta paragraphs): the v0.13.0–v0.13.1 fix/UX wave — Format ▸ Fill's Slide background fill, drawn Shadow/Glow/Soft-Edges preset tiles, PowerPoint preset ids for Darken/Desaturate, scrolling Add Animation menu, cursor-visible show setup, off-thread presenter preview, PDF transparent-pixel backdrop, spelling bounds, variable-font Windows family names, `tickLblPos: none`, and the invalid-slide-index rejections in `file.export`/`file.render`/`slide.colorAt`/`animation.clear`/`design.applyIdea`/transition commands; and the v0.11.1-era `format.languageAll`/`slide.selectRange`/Reuse Slides chooser/units preference/Ctrl+wheel zoom/RTF fixes/PDF links/media hardening wave. All were verified as history, not current behaviour changes.

## Known gap in this round

- `deckcraft-cli` is not installed on this machine and is not inside the `.app`, so the live registry (`deckcraft-cli commands`) could not be read back: every count is parsed from code at the tag, and only `--version`/`--help` were executed. No GUI was launched, so presenter, slide-show and clipboard behaviour is code and documentation evidence, not observed behaviour, and PPTX fidelity on real corporate decks remains unmeasured by the project.
