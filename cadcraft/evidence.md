# CADCraft — evidence ledger (tag v0.18.0)

Audit basis: this checkout is tag **`v0.18.0`**, commit **`32238e83c2c8bf643994132883e94bc96961f649`**
("Release 0.18.0", 2026-11-06; shallow clone of the release tag). Inspection date **2026-11-07**; the
v0.17.0 ref (`f389d6a72e3fc160ea125b4f264d68f64cbe2aba`) was used for the id-set and file diffs. The
installed 0.18.0 bundle (id `ai.storyteller.cadcraft`) prints
`cadcraft 0.18.0 (32238e83c2c8bf643994132883e94bc96961f649)`, so it matches the tag; the GUI was never
launched, and the bundle ships no `cadcraft-cli` (its `Contents/MacOS/` holds only `CADCraft`), so no
live catalog could be read.

v0.17.0 → v0.18.0 delta (measured with `git diff v0.17.0..HEAD`: **308 files, +24,334/−1,327**, 60 added,
248 modified, 0 deleted): **six command ids added, none removed** — `dview`, `image`, `imageattach`,
`minsert`, `xclip`, `xclipframe`; **XCLIP/XCLIPFRAME** narrower xref/block clipping (`crates/engine/src/cmd/blocks/xclip.rs`,
`crates/io/src/dxf_clip.rs`); **raster IMAGEATTACH/IMAGE** (`crates/engine/src/cmd/image.rs`, `crates/io/src/raster.rs`,
`crates/ui-egui/src/canvas/images.rs`); **SHX shape/big/unifont fonts** (`crates/fonts/src/shx/`); **DVIEW and view
twist** (`crates/engine/src/cmd/view/dview.rs`); **MINSERT** (`crates/engine/src/cmd/blocks.rs`); the **round-trip
harness** (`crates/io/src/roundtrip.rs`, `apps/cadcraft-cli/src/roundtrip.rs`, `xtask/src/main.rs`); **DWG in a child
process** plus acadrust 0.6.6 (`crates/dwg/src/worker.rs`, `crates/dwg/Cargo.toml`); **autosave locks, failure
notice and crash recovery** and a **UI panic guard** (`crates/engine/src/autosave.rs`, `crates/ui-egui/src/fault.rs`);
the **Find and Replace window (Cmd+F)** and **Edit Text window** (`crates/ui-egui/src/finddlg.rs`,
`crates/ui-egui/src/textdlg.rs`) with FIND's new `types`/`handles` (`crates/engine/src/cmd/utility.rs`); **PLOT format
from the path extension** and render `background`/`plot_style` (`crates/engine/src/cmd/plotters.rs`,
`crates/mcp/src/tools.rs`); **Georgian** (`crates/ui-egui/src/i18n/ka.tsv`); the web **page-host mode**
(`apps/cadcraft-web/src/host.rs`); and `SECURITY.md`.

Older delta history (v0.15.0 – v0.16.0) is folded into `CHANGES.md`.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | **457 registered engine commands** (439 unique literal ids + 18 `gc!`/`dc!` macro ids, no duplicate ids); the generated checklist reads 449 from its 2026-11-01 run | `crates/engine/src/cmd.rs` (specs aggregation), `crates/engine/src/cmd/constraints.rs` (macros), `docs/parity-checklist.md` | implemented (derived; checklist stale) |
| 2 | **59 UI-only commands**, including `ui.dialog.find` (Cmd+F, new) | `crates/ui-egui/src/menus.rs` (`UI_COMMANDS`) | implemented |
| 3 | **15 MCP tools** (12 headless + 3 app-only), unchanged; `render` gained `background` and `plot_style` | `crates/mcp/src/tools.rs`, `crates/mcp/src/backend.rs` | implemented |
| 4 | **27 control methods app / 12 headless**; per-session token auth unchanged; `ui.render` gained `window`/`background`/`plot_style` | `crates/ui-egui/src/control.rs`, `crates/mcp/src/backend.rs`, `crates/mcp/src/control_token.rs`, `apps/cadcraft/src/control_server.rs` | implemented |
| 5 | **8 CLI verbs** (`info`, `convert`, `run`, `commands`, `mcp`, `perf`, `sample`, `roundtrip`) | `apps/cadcraft-cli/src/args.rs`, `apps/cadcraft-cli/src/lib.rs` | implemented |
| 6 | XCLIP/XCLIPFRAME: rectangle/polygon/closed-polyline boundaries, invert, on/off/delete/polyline, frame mode 0/1/2, extents cut, kept through DXF/DWG as `SPATIAL_FILTER` | `crates/engine/src/cmd/blocks/xclip.rs`, `crates/doc/src/xclip.rs`, `crates/io/src/dxf_clip.rs`, `crates/render/src/clip.rs` | implemented (gaps F2 keeps only xref in-place editing) |
| 7 | Raster images: IMAGEATTACH (`iat`) PNG/JPEG/BMP/TIFF, IMAGE (`im`) listing, tiled display and PNG output, pixels never stored in the drawing | `crates/engine/src/cmd/image.rs`, `crates/io/src/raster.rs`, `crates/ui-egui/src/canvas/images.rs`, `crates/render/src/raster.rs` | partial (no PDF/SVG image output, no IMAGECLIP/IMAGEADJUST, brightness/contrast not applied — gaps FF10) |
| 8 | SHX shape fonts, big fonts and unifonts parsed and drawn for text, attributes, dimensions and tables; linetype shapes drawn; search beside the drawing, `CADCRAFT_SHXPATH`, font map, web upload | `crates/fonts/src/shx/mod.rs`, `crates/render/src/linetype_text.rs` | implemented, with the limits listed in gaps FF8 |
| 9 | DVIEW twists the model view or active layout viewport (2D options); twist kept through DXF/DWG (group 51) | `crates/engine/src/cmd/view/dview.rs`, `crates/doc/src/entity/layout.rs` | partial (CAmera/TArget/Distance/POints/CLip/Hide refuse — gaps F1) |
| 10 | MINSERT: rows/columns and spacings along the reference's own axes | `crates/engine/src/cmd/blocks.rs`, `crates/doc/src/array.rs` | implemented |
| 11 | Round-trip harness: open → save → reopen → diff, Markdown + JSON report; `cadcraft-cli roundtrip`, `cargo xtask corpus` | `crates/io/src/roundtrip.rs`, `apps/cadcraft-cli/src/roundtrip.rs`, `xtask/src/main.rs` | implemented (corpus lives in a separate repo) |
| 12 | DWG read/write in a child process; acadrust 0.6.6 | `crates/dwg/src/worker.rs`, `crates/dwg/src/lib.rs`, `crates/dwg/Cargo.toml` | implemented (worker has no memory limit — `SECURITY.md`) |
| 13 | Autosave: `.sv$` DXF copies, per-folder lock, owner-only files, failure notice, recovery at next start; UI panic autosaves and writes `crash-reports/` | `crates/engine/src/autosave.rs`, `crates/ui-egui/src/autosave.rs`, `crates/ui-egui/src/fault.rs` | implemented (desktop only) |
| 14 | Find and Replace window over FIND (`types`, `handles`, match snippets); Edit Text window for TEXT/MTEXT/attdef/dimension text (double-click keeps in-place editing) | `crates/ui-egui/src/finddlg.rs`, `crates/ui-egui/src/textdlg.rs`, `crates/engine/src/cmd/utility.rs` | implemented |
| 15 | PLOT takes PNG/SVG/PDF from the path extension, refuses an unknown extension and several sheets for PNG/SVG | `crates/engine/src/cmd/plotters.rs`, `crates/engine/src/cmd/layout.rs` | implemented |
| 16 | 19 interface languages, Georgian (`ka`) new; `docs/localization.md` lists 18 and omits `vi` | `crates/ui-egui/src/i18n.rs`, `crates/ui-egui/src/i18n/ka.tsv`, `docs/localization.md` | implemented; doc drift |
| 17 | Web page-host mode (`?host=parent`, `data-host="page"`) via `craft-web-host` | `apps/cadcraft-web/src/host.rs`, `apps/cadcraft-web/Cargo.toml` | implemented (web only) |
| 18 | 23 built-in hatch patterns (SOLID, ANSI31–38, LINE, NET, NET3, DOTS, DASH, BRICK, SQUARE, CROSS, EARTH, GRASS, HONEY, ZIGZAG, AR-CONC, AR-SAND) | `crates/doc/src/library.rs` (`standard_patterns`) | implemented |
| 19 | 14 object snaps, object snap tracking, FROM/M2P/TK and point filters | `crates/engine/src/snap.rs` (`mode::ALL` has 14 entries), `crates/engine/src/pointmod.rs` | implemented |
| 20 | Large-file handling: 512 MiB per directly opened drawing, 512 MiB DWG with a 1 GiB DXF rendition, 100 million DXF group codes, `CADCRAFT_MAX_DXF_TAGS` override | `crates/engine/src/cmd/file.rs`, `crates/dwg/src/lib.rs`, `crates/dxf/src/lib.rs` | implemented |
| 21 | macOS bundle has no `cadcraft-cli` | the installed bundle's `Contents/MacOS/` lists only `CADCraft` | verified absent |

## 2. Counts (same method at both tags)

| Surface | v0.17.0 (measured) | v0.18.0 (measured) | Change |
|---|---:|---:|---|
| Registered engine commands (439 literal ids + 18 macro ids) | **451** | **457** | +6 / −0 |
| Registered commands per generated checklist | 449 (dated 2026-11-01) | 449 (file unchanged; stale) | not regenerated |
| Static `CommandSpec::new(` sites | **435** | **441** | +6 |
| Unique literal `CommandSpec` ids | **433** | **439** | +6 / −0 |
| `gc!` / `dc!` invocations | 12 / 6 | **12 / 6** | unchanged |
| UI-only `UI_COMMANDS` entries | **58** | **59** | +1 (`ui.dialog.find`) |
| Menu breadth per checklist | 298/491 (61 %) | 298/491 (61 %) | not regenerated |
| MCP tools | 15 (12 + 3) | **15 (12 + 3)** | unchanged (render params added) |
| Control methods | 27 app / 12 headless | **27 / 12** | unchanged (ui.render params added) |
| CLI verbs | 7 | **8** | +`roundtrip` |
| Drawing formats read / written | 4 / 6 | **4 / 6** | unchanged |
| Raster image formats decoded | 0 | **4** (png, jpeg, bmp, tiff) | new capability |
| Interface languages | 18 | **19** | +`ka` |
| Built-in hatch patterns | 23 | **23** | unchanged |
| Object snaps | 14 | **14** | unchanged |
| craft-libs pins | `92d392cf…` | `92d392cf…` + `2e2312dd…` (`craft-web-host`) | +1 revision |
| acadrust (DWG bridge) | 0.6.5 | **0.6.6** | +1 |
| egui / eframe | 0.37 | **0.37** | unchanged |

The previous ledger recorded 433 static sites, 431 unique ids, 57 UI-only commands, 16 interface languages
and 23 hatch patterns for v0.17.0. Re-measured at the *same* v0.17.0 tag with the method below, those read
**435 / 433 / 58 / 18 / 23**. Only the hatch-pattern count was right; the other four were stale (the 57
UI-only entries date from the v0.13.0 audit).

## 3. Uncertain / not verified

- **No live catalog.** No `cadcraft-cli` is installed and the bundle ships none, so `cadcraft-cli commands |
  jq length`, `--help` and headless runs were not possible. 457 is a source derivation (439 unique literal
  ids + 18 macro-expanded ids, zero duplicates); it is cross-checked by the same method at v0.17.0 (451) and
  by the checklist's +6 id delta. Expect this to be exact, but re-derive before quoting.
- **No GUI launch**, so menu behaviour, the Find/Edit Text windows and raster display are code-read only.
- **Menu breadth 298/491** is carried from the 2026-11-01 checklist; it was not regenerated at this tag.
- **Georgian coverage (1,458 rows)** is taken from `docs/localization.md`; the translation was not reviewed.
- **`notSaved` behaviour through DWG** is code-read (the field name is verified in `crates/ui-egui/src/save_loss.rs`); no DWG was written (nothing was modified).

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `README.md`: SHX fonts "aren't read yet" | `crates/fonts/src/shx/` reads shape, big and unifont files; `docs/gaps.md` FF8 documents it |
| `ROADMAP.md` (2026-10-21): "no XCLIP", "no REFEDIT" | XCLIP is implemented (`crates/engine/src/cmd/blocks/xclip.rs`); REFEDIT exists (`crates/engine/src/cmd/blocks/refedit.rs`) and gaps F2 says so |
| `docs/parity-checklist.md`: 449 commands, 298/491 | generated 2026-11-01, before the v0.17.0 tag (2026-11-02); the registry derives to 451 then, 457 now |
| `docs/file-format-parity.md`, DWG section: "with the `acadrust` 0.6.3 crate" | `crates/dwg/Cargo.toml` pins **0.6.6** |
| `docs/localization.md` language lists: 18 languages | `crates/ui-egui/src/i18n.rs` registers 19 (`vi` is missing from the doc) |
| `README.md` tagline "2D and 3D" | no 3D (`docs/gaps.md`); DVIEW's 3D options refuse |
| `docs/roadmap.md` alpha gate: "no FROM/M2P/TK or typed snap overrides" | `crates/engine/src/pointmod.rs` implements FROM/M2P/MTP, point filters and the typed `END`/`MID`/`CEN`/`NON` overrides |
| `apps/cadcraft-cli/src/args.rs` help for `--view current`: "a freshly opened drawing's view is its extents plus a 10% margin" | `crates/engine/src/session/files.rs` now opens on the saved view (`$VIEWCTR`/`$VIEWSIZE`) and falls back to extents |

## 5. Verification commands (read-only, run at the tag)

```sh
git -C <checkout> rev-parse HEAD                                   # 32238e83c2c8bf643994132883e94bc96961f649
git -C <checkout> diff --stat v0.17.0..HEAD | tail -1              # 308 files changed, 24334 insertions(+), 1327 deletions(-)
git grep -o 'CommandSpec::new(' HEAD -- '*.rs' | wc -l             # 441 sites (2 are macro bodies)
git grep -h -o 'CommandSpec::new("[^"]*"' HEAD -- '*.rs' | sed 's/.*new("//; s/"$//' | tr 'A-Z' 'a-z' | sort -u | wc -l   # 439 literal ids
grep -cE '^\s+gc!\("' crates/engine/src/cmd/constraints.rs         # 12
grep -cE '^\s+dc!\("' crates/engine/src/cmd/constraints.rs         # 6
sed -n '/pub const UI_COMMANDS/,/^];/p' crates/ui-egui/src/menus.rs | grep -c '("ui\.'   # 59
grep -oE 'code: "[A-Za-z-]+"' crates/ui-egui/src/i18n.rs | sort -u | wc -l                # 19
grep -c '"name": "' crates/mcp/src/tools.rs                        # 15
sed -n '/^const METHODS: &\[(&str/,/^\];/p' crates/ui-egui/src/control.rs | grep -cE '^\s+\("[a-z_.]+"'       # 27
sed -n '/^const HEADLESS_METHODS/,/^\];/p' crates/mcp/src/backend.rs | grep -cE '^\s+\("[a-z_.]+"'           # 12
sed -n '/pub(crate) enum Command/,/^}/p' apps/cadcraft-cli/src/args.rs | grep -cE '^\s+[A-Z][A-Za-z]+\('     # 8
sed -n '/pub fn standard_patterns/,/^}/p' crates/doc/src/library.rs | grep -c 'name: "'                     # 23
grep -n 'ALL: \[(u32, &str); 14\]' crates/engine/src/snap.rs        # 14 object snaps
grep -n 'pub const READ\|pub const WRITE' crates/doc/src/format.rs  # 4 read / 6 written
grep -n 'acadrust = ' crates/dwg/Cargo.toml                        # acadrust = "0.6.6"
sed -n '7p' docs/parity-checklist.md                               # 449 registered commands (2026-11-01 snapshot)
# id sets, both tags (multiline-aware; re-wrapped registrations defeat single-line greps):
perl -0777 -ne 'while (/CommandSpec::new\(\s*"([^"]+)"/g) { print lc "$1\n"; }' $(find crates -name '*.rs') | sort -u
```

## Round 2026-11-07 (refresh)

- Re-pinned to `v0.18.0` = `32238e83c2c8bf643994132883e94bc96961f649` (installed `cadcraft 0.18.0 (32238e83c2c8bf643994132883e94bc96961f649)`, bundle id `ai.storyteller.cadcraft`).
- Registry re-derived: **457** commands (439 literal ids + 18 macro ids); six ids added, none removed; the generated checklist (449) was not regenerated.
- Re-measured: UI-only commands 59 (+1), control methods 27/12 and MCP tools 15 (surface unchanged, parameters added), CLI verbs 8 (+`roundtrip`), languages 19 (+`ka`), formats 4/6 plus 4 raster image formats, hatch patterns 23, object snaps 14.
- Corrected from the previous ledger: static sites 435→441, unique literal ids 433→439, UI-only 58→59, languages 18→19 (the ledger's 433/431/57/16 were stale).
- New capabilities documented: XCLIP/XCLIPFRAME, IMAGEATTACH/IMAGE raster images, SHX fonts, DVIEW/view twist, MINSERT, the round-trip harness, DWG worker process, autosave/panic recovery, Find and Replace and Edit Text windows, PLOT format from the extension, web page-host mode.
- Every cited repo path in `SKILL.md` and this file was re-resolved against the tag; no `references/` files existed to preserve, and `agents/openai.yaml` was kept unchanged (the app's display name and one-line description are still right).
