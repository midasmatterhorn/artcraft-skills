# CADCraft — round 2026-11-07 changes

Re-pinned: v0.17.0 (`f389d6a`) -> v0.18.0 (`32238e8`, installed `cadcraft 0.18.0 (32238e83c2c8bf643994132883e94bc96961f649)`, bundle id `ai.storyteller.cadcraft`).

## Corrected / re-measured

- Six command ids added, none removed: `dview`, `image`, `imageattach`, `minsert`, `xclip`, `xclipframe`. Registry re-derived to **457** commands (439 unique literal ids + 18 `gc!`/`dc!` macro ids), 451 at v0.17.0 by the same method; the generated checklist is a 2026-11-01 snapshot (449) and was not regenerated.
- The previous ledger's absolute counts were stale at its own tag: static `CommandSpec::new(` sites **435 → 441**, unique literal ids **433 → 439**, UI-only commands **58 → 59** (`ui.dialog.find`, Cmd+F), interface languages **18 → 19** (+Georgian), CLI verbs **7 → 8** (+`roundtrip`). Re-measuring with this method at v0.17.0 gives 435 / 433 / 58 / 18 / 7, so the ledger's published 433 / 431 / 57 / 16 were already off before this release.
- Hatch patterns stay **23**, object snaps **14**, MCP tools **15** (12 headless + 3 app-only), control methods **27 app / 12 headless**, drawing formats **4 read / 6 written** — all re-measured and unchanged; `render` and `ui.render` gained `background`/`plot_style`/`window` parameters, so their descriptions changed while the sets did not.
- New capability rows in the body: XCLIP/XCLIPFRAME, IMAGEATTACH/IMAGE raster images (PNG/JPEG/BMP/TIFF), SHX shape/big/unifont fonts, DVIEW and view twist, MINSERT, the round-trip harness (`cadcraft-cli roundtrip`, `cargo xtask corpus`), DWG read/write in a child process (acadrust **0.6.5 → 0.6.6**), autosave locks/failure notice/crash recovery and the UI panic guard, Find and Replace and Edit Text windows, PLOT format from the path extension, and the web page-host mode.
- Behaviour change recorded for agents: a drawing now opens on the saved view (`$VIEWCTR`/`$VIEWSIZE`) instead of the extents, so `convert --view current` and `run --export` start from that view; the CLI's `--view current` help still says "extents plus a 10% margin" (stale, recorded as drift).
- Limitations rewritten where the code moved: XCLIP and SHX moved from "missing" to implemented-with-limits; raster images are display-and-PNG only; a DWG worker has no memory limit; attached images are external files; SHX text metrics need the font file. Two new cautions added for agents (keep image files with the drawing, keep `.shx` beside it or on `CADCRAFT_SHXPATH`).
- Sources section corrected: v0.17.0 is "Release 0.17.0", dated 2026-11-02 (the old section labelled it "Release 0.16.0", 2026-11-01); the installed bundle id and the absence of a CLI in the bundle are now stated; craft-libs now has a second pin (`2e2312dd…` for `craft-web-host`).

## Method

- Diffed `v0.17.0..HEAD`: **308 files**, +24,334/−1,327, 60 added / 248 modified / 0 deleted.
- Command ids: multiline-aware `CommandSpec::new("id")` extraction at both tags plus the 18 `gc!`/`dc!` invocations; the id diff is +6/−0.
- Counts re-derived from source, not docs: `UI_COMMANDS` (`crates/ui-egui/src/menus.rs`), `LANGUAGES` (`crates/ui-egui/src/i18n.rs`), `METHODS`/`HEADLESS_METHODS` (`crates/ui-egui/src/control.rs`, `crates/mcp/src/backend.rs`), the CLI `Command` enum (`apps/cadcraft-cli/src/args.rs`), `Format::READ`/`WRITE` (`crates/doc/src/format.rs`), `standard_patterns()` (`crates/doc/src/library.rs`), `mode::ALL` (`crates/engine/src/snap.rs`), `tool_definitions(has_ui)` (`crates/mcp/src/tools.rs`).
- No `cadcraft-cli` is installed and the bundle ships none, so the registry is **derived**, not executed; `evidence.md` records this and the arithmetic. The only execution was the installed binary's `--version`.
- Behaviour claims were cross-checked against the changed code, then against `docs/{gaps,file-format-parity,control-protocol,mcp,localization}.md`; where a doc disagreed with code, the code went in and the drift was recorded.
- Every repo-relative path cited in `SKILL.md` and `evidence.md` was re-resolved against the tag (brace/glob citations avoided; a basename like `props/dash_units.rs` is ambiguous in this tree and is cited by full path).

## Unchanged

- Drawing, modify, annotation, parametric, AutoLISP and layout/plotting command surfaces; control-channel token auth and its resource limits (16 connections, 256 MiB line, 512 MiB total, 64 queued, 60 s reply, 10 min idle, 30 s write); MCP tool set; CLI verbs other than `roundtrip`; drawing formats read/written; web build without DWG or autosave; packaging targets; the engine shortcut set apart from the new Cmd+F.
- `agents/openai.yaml` kept as is — the display name and one-line description are still accurate.

## Earlier history (folded out of SKILL.md)

- **v0.15.0 – v0.16.0:** `CHPROP` and `SOLID`, PEDIT Multiple, BEDIT block switching, `CHANGE`, `-ARRAY`, `-UNITS`, Vietnamese (`vi`), DXF code-page saves, `.bak` on overwrite and MCP/control buffer bounds. The v0.16.0 → v0.17.0 paragraph stays in `SKILL.md` as the second-most-recent delta.
- The previous body's "Release delta vs v0.13.0" paragraph was dropped rather than carried: its numbers were not re-measured in this round and conflict with the counts measured at v0.17.0.

## Known gap in this round

- No live catalog was read: with no CLI on the machine and a bundle that ships none, the 457-command figure and the 59 UI-only entries are source derivations, not `cadcraft-cli commands | jq length`. The menu-breadth figure (298/491) is carried from the 2026-11-01 checklist because it cannot be regenerated without a build.
- The prose was refreshed against the diff and re-verified path-by-path, but it is a pin-and-verify refresh, not a new deep audit of every feature; GUI-only behaviour (the Find/Edit Text windows, raster display, autosave notices, panic guard) is code-read, not observed.
