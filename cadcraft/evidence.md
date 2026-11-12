# CADCraft — evidence ledger (tag v0.20.1)

Audit basis: this checkout is tag **`v0.20.1`**, commit **`7526dc62c14e71b3c8d46e73bbf1fa29ef506af1`**
(“Merge tested main for Flatpak update patch release”, 2026-11-11; shallow clone of the release tag).
Inspection date **2026-11-12**. The installed 0.20.1 bundle (id `ai.storyteller.cadcraft`) prints
`cadcraft 0.20.1 (7526dc62c14e71b3c8d46e73bbf1fa29ef506af1)` for `--version`, so it matches the tag.
The GUI was never launched; `--version` and `--help` were the only app-binary runs. The bundle ships no
`cadcraft-cli` (its `Contents/MacOS/` holds only `CADCraft`) and no `cadcraft-cli` is installed on the
authoring machine, so no live command catalog could be read. The previous audit described
**v0.18.0** = `32238e83c2c8bf643994132883e94bc96961f649` (“Release 0.18.0”, 2026-11-06); the v0.17.0
ref (`f389d6a72e3fc160ea125b4f264d68f64cbe2aba`) is carried from the previous ledger because only
the two release tags are present in this shallow checkout.

v0.18.0 → v0.20.1 delta (measured with `git diff v0.18.0..HEAD`: **146 files, +8,144/−856**, 14
added, 132 modified, 0 deleted): **no engine command id was added or removed** — the multiline-aware
literal set is identical at both tags (439 ids), and the 12 `gc!` + 6 `dc!` invocations are
unchanged, so the registry stays **457**. The only new catalog id is **UI-only `ui.shortcuts`**:
Tools ▸ Customize ▸ Keyboard Shortcuts... lets any command take a shortcut, the user's choice wins
over the built-in one, the command that had the key loses it (and the dialog says so), and the
clipboard keys, Delete and Cmd+Q stay fixed (`crates/ui-egui/src/keys.rs`,
`crates/ui-egui/src/menus.rs`, `crates/ui-egui/src/lib.rs`). Other changed surfaces:
**ALIASEDIT aliases now persist in the user profile** across restarts (desktop and web; the
headless CLI has no profile, so aliases last for the run) and a `.pgp` file now *replaces* the user
alias set; the Command Aliases dialog gained **Import...** with a `.pgp` picker
(`crates/engine/src/cmd/file/pgp.rs`, `crates/ui-egui/src/aliasdlg.rs`, `crates/ui-egui/src/options.rs`);
**Right-Click Customization** in Options ▸ User Preferences (`rightClickDuration` 100–2000 ms,
`rightClickDefault`/`rightClickEdit` = `menu`|`repeat`, `rightClickCommand` =
`menu`|`enter`|`menuWithOptions`) (`crates/ui-egui/src/options.rs`,
`crates/ui-egui/src/options/dialog.rs`, `crates/ui-egui/src/context_menu.rs`); **TEXTEDIT and
double-click on an existing MTEXT open the in-place editor with its contents and formats** (#842),
and **multileader text is editable** by double-click, TEXTEDIT and the Properties palette’s Contents
field (#1081), with relative `\H2x;` heights kept and over-long texts refused by the editor and
handed to the command line instead of being truncated (`crates/engine/src/mtext_edit.rs`,
`crates/engine/src/cmd/modify2/textedit.rs`, `crates/ui-egui/src/mtext_editor.rs`,
`crates/ui-egui/src/canvas/pick.rs`); the **Properties palette shows one type’s properties for
several selected objects** and `*VARIES*` where values differ, memoised per drawing revision and
selection (`crates/ui-egui/src/palettes.rs`); **DWG saves preserve other applications’ registered
entities and objects as proxies of their own classes** (class numbers 500+, hard-owned null-owner
objects kept, failures isolated and named in the read notes) (`crates/dwg/src/proxy_transport.rs`,
`crates/dwg/src/lib.rs`, `crates/io/src/dxf_raw.rs`); the browser build installs the shared
**`window.cadcraft` page API** (`request`, `execute`, `commands`, `docInspect`, `uiInspect`,
`screenshot`) over the same control channel (`apps/cadcraft-web/src/api.rs`,
`apps/cadcraft-web/src/main.rs`, and `storytold/craft-libs` `craft-web-api` at pin
`fd5e2feff6ea25bed371a99cc732b3968d621505`); the MCP bridge now sends the control token **only to
the exact peer `127.0.0.1:PORT`** and refuses token files that are symlinks, non-plain or readable by
other users, with no shared-temp-dir fallback (`crates/mcp/src/backend.rs`,
`crates/mcp/src/control_token.rs`); the web `ui.screenshot` returns an **inline PNG** because there
is no file system (`crates/ui-egui/src/control.rs`); **macOS file dialogs are sheets** shown without
blocking the event loop, one at a time, and the answer lands on the drawing that asked
(`apps/cadcraft/src/sheet.rs`, `apps/cadcraft/src/main.rs`, `crates/ui-egui/src/lib.rs`); and the
**Flatpak manifests gained `--talk-name=org.freedesktop.Flatpak`** so update checks and self-updates
work, guarded by a test (`packaging/linux/flatpak/ai.storyteller.cadcraft.yml`,
`packaging/linux/flatpak/ai.storyteller.cadcraft.bundle.yml`, `crates/ui-egui/tests/flatpak_updates.rs`).
The rest of the diff is hardening and performance (allocation-free NURBS derivatives up to degree 10,
banded spline solves, region candidate-pair budgets, MTEXT atom caps, LISP callback/string budgets, a table
outline fallback; `crates/geom/src/nurbs.rs`, `crates/geom/src/spline.rs`, `crates/geom/src/region.rs`,
`crates/fonts/src/mtext.rs`, `crates/engine/src/lisp/`, `crates/render/src/table.rs`).

Older delta history (v0.16.0 and earlier) is folded into `CHANGES.md`.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | **457 registered engine commands** = 439 unique literal ids + 18 `gc!`/`dc!` macro ids, zero duplicates; unchanged at v0.20.1 (also 457 at v0.18.0) | `crates/engine/src/cmd.rs`, `crates/engine/src/cmd/constraints.rs`; derived, no live CLI | implemented (source-derived) |
| 2 | **60 UI-only commands**, including new `ui.shortcuts` (Keyboard Shortcuts...) and `ui.dialog.find` (Cmd+F) | `crates/ui-egui/src/menus.rs` (`UI_COMMANDS`) | implemented |
| 3 | **15 MCP tools** (12 headless + 3 app-only), unchanged at v0.20.1; `render` still takes `background`/`plot_style` | `crates/mcp/src/tools.rs`, `crates/mcp/src/backend.rs` | implemented |
| 4 | **27 app / 12 headless control methods**, unchanged sets; token auth now hardened (exact-peer check, no symlink on Unix, owner-only file, no temp-dir fallback) | `crates/ui-egui/src/control.rs`, `crates/mcp/src/backend.rs`, `crates/mcp/src/control_token.rs`, `apps/cadcraft/src/control_server.rs` | implemented |
| 5 | **8 CLI verbs** (`info`, `convert`, `run`, `commands`, `mcp`, `perf`, `sample`, `roundtrip`) unchanged at v0.20.1 | `apps/cadcraft-cli/src/args.rs`, `apps/cadcraft-cli/src/lib.rs` | implemented |
| 6 | **Keyboard Shortcuts dialog**: any command gets a shortcut; the user's choice wins; conflicts reassign and are reported; clipboard/Delete/Cmd+Q fixed; at most 1,000 stored, 64-char limit; malformed prefs keep the current set; JSON `{set, reset}` | `crates/ui-egui/src/keys.rs`, `crates/ui-egui/src/lib.rs` (`prefs_json`), `crates/ui-egui/src/menus.rs` (`ui.shortcuts`) | implemented (code-read) |
| 7 | **ALIASEDIT aliases persist** in the user profile (desktop/web); a `.pgp` load replaces the user alias set; `set`/`remove`/`clear`; Command Aliases dialog Import... asks before replacing; REINIT re-reads the file | `crates/engine/src/cmd/file/pgp.rs`, `crates/ui-egui/src/aliasdlg.rs`, `crates/ui-egui/src/options.rs` | implemented (code-read; persistence tests exist) |
| 8 | **Right-Click Customization**: hold duration 100–2000 ms (default 250); Default/Edit modes `menu`/`repeat`; Command mode `menu`/`enter`/`menuWithOptions`; stored in the profile | `crates/ui-egui/src/options.rs`, `crates/ui-egui/src/options/dialog.rs`, `crates/ui-egui/src/context_menu.rs` | implemented (code-read) |
| 9 | **MTEXT in-place editing of existing text** (TEXTEDIT/double-click) keeps contents and formats; relative `\H2x;` heights stay relative; text past 100,000 chars / 20,000 paragraphs / 1,000 kept codes is refused by the editor and falls back to the command line; unchanged text adds no undo step | `crates/engine/src/mtext_edit.rs` (`fits`, `leaves_unchanged`), `crates/engine/src/cmd/modify2/textedit.rs`, `crates/ui-egui/src/mtext_editor.rs` | implemented (code-read; tests) |
| 10 | **Multileader text editing**: TEXTEDIT, double-click and the Properties Contents field edit a multileader that has text; a block-content multileader has none; locked layers refused | `crates/engine/src/cmd/modify2/textedit.rs`, `crates/ui-egui/src/canvas/pick.rs`, `crates/ui-egui/src/palettes.rs`, `crates/engine/tests/it/mleader_text_edit.rs` | implemented (code-read; tests) |
| 11 | **Properties palette, several objects of one type**: type properties, `*VARIES*`, values compared past display rounding, memoised per revision/selection; several dynamic-block references show the block name | `crates/ui-egui/src/palettes.rs` | implemented (code-read) |
| 12 | **DWG proxy preservation**: registered entities of another application’s class become proxy entities on read; unknown application objects become proxy objects; class numbers are 500 + their place in CLASSES; a hard-owned null-owner object is kept; a class that is missing/ambiguous or a record that cannot be split is named in the read notes | `crates/dwg/src/proxy_transport.rs`, `crates/dwg/src/lib.rs`, `crates/io/src/dxf_raw.rs`, `crates/io/tests/registered_proxy.rs`, `crates/io/tests/hard_owned_objects_kept.rs` | implemented (code-read; synthetic tests, no real DWG run) |
| 13 | **Web page API** `window.cadcraft`: `request(method,params)`, `execute(command,params)`, `commands()`, `docInspect(params)`, `uiInspect(params)`, `screenshot(params)`; promise with timeout; existing functions are kept; web only | `apps/cadcraft-web/src/api.rs`, `apps/cadcraft-web/src/main.rs`, `apps/cadcraft-web/Cargo.toml`; shared `craft-web-api` at `fd5e2fef…` | implemented (code-read; no browser run) |
| 14 | **macOS file dialogs as sheets**: shown without a modal loop (the #1527 crash); one at a time; answer applied to the drawing that asked; synchronous pickers elsewhere | `apps/cadcraft/src/sheet.rs`, `apps/cadcraft/src/main.rs`, `crates/ui-egui/src/lib.rs` (`pick_then`), `crates/ui-egui/src/closing.rs`, `crates/ui-egui/src/exchange.rs` | implemented (code-read; GUI not launched) |
| 15 | **Flatpak update permission**: `--talk-name=org.freedesktop.Flatpak` in both source and bundle manifests, with a test that requires it and matching permissions | `packaging/linux/flatpak/ai.storyteller.cadcraft.yml`, `packaging/linux/flatpak/ai.storyteller.cadcraft.bundle.yml`, `crates/ui-egui/tests/flatpak_updates.rs` | implemented (code-read; not built) |
| 16 | XCLIP/XCLIPFRAME: rectangle/polygon/closed-polyline boundaries, invert, on/off/delete/polyline, frame mode 0/1/2, extents cut, kept through DXF/DWG as `SPATIAL_FILTER` (unchanged at v0.20.1) | `crates/engine/src/cmd/blocks/xclip.rs`, `crates/doc/src/xclip.rs`, `crates/io/src/dxf_clip.rs`, `crates/render/src/clip.rs` | implemented |
| 17 | Raster images: IMAGEATTACH (`iat`) PNG/JPEG/BMP/TIFF, IMAGE (`im`) listing, on-screen and PNG output, pixels never stored in the drawing (unchanged at v0.20.1) | `crates/engine/src/cmd/image.rs`, `crates/io/src/raster.rs`, `crates/ui-egui/src/canvas/images.rs`, `crates/render/src/raster.rs` | partial (no PDF/SVG image output, no IMAGECLIP/IMAGEADJUST, brightness/contrast not applied) |
| 18 | SHX shape fonts, big fonts and unifonts parsed and drawn for text, attributes, dimensions, tables and linetype shapes; searched beside the drawing, via `CADCRAFT_SHXPATH`, a font map or the web upload (unchanged at v0.20.1) | `crates/fonts/src/shx/mod.rs`, `crates/fonts/src/shx/table.rs`, `crates/render/src/linetype_text.rs` | implemented with the limits in gaps FF8 |
| 19 | Round-trip harness: open → save → reopen → diff, Markdown + JSON report; `cadcraft-cli roundtrip`, `cargo xtask corpus` (unchanged at v0.20.1) | `crates/io/src/roundtrip.rs`, `apps/cadcraft-cli/src/roundtrip.rs`, `xtask/src/main.rs` | implemented (corpus lives in a separate repo) |
| 20 | Autosave/recovery: `.sv$` DXF copies, per-folder lock, owner-only files, failure notice, recovery at start; UI panic autosaves and writes `crash-reports/` (unchanged at v0.20.1) | `crates/engine/src/autosave.rs`, `crates/ui-egui/src/autosave.rs`, `crates/ui-egui/src/fault.rs` | implemented (desktop only) |

## 2. Counts (same method at both tags)

| Surface | v0.18.0 (measured) | v0.20.1 (measured) | Change |
|---|---:|---:|---|
| Registered engine commands (439 literal + 18 macro) | **457** | **457** | unchanged |
| Static `CommandSpec::new(` sites | **441** | **441** | unchanged |
| Unique literal `CommandSpec` ids | **439** | **439** | unchanged (identical set) |
| `gc!` / `dc!` invocations | 12 / 6 | **12 / 6** | unchanged |
| UI-only `UI_COMMANDS` entries | **59** | **60** | +1 (`ui.shortcuts`) |
| App-level catalog (engine + UI) | 516 | **517** | +1 |
| Menu breadth per checklist | 298/491 (2026-11-01) | 298/491 (file unchanged; stale) | not regenerated |
| MCP tools | 15 (12 + 3) | **15 (12 + 3)** | unchanged |
| Control methods | 27 app / 12 headless | **27 / 12** | unchanged sets; behaviour hardened |
| CLI verbs | 8 | **8** | unchanged |
| Drawing formats read / written | 4 / 6 | **4 / 6** | unchanged |
| Raster image formats decoded | 4 (png, jpeg, bmp, tiff) | **4** | unchanged |
| Interface languages | 19 | **19** | unchanged |
| Built-in hatch patterns | 23 | **23** | unchanged |
| Object snaps | 14 | **14** | unchanged |
| craft-libs pins | `92d392cf…` + `2e2312dd…` (web) + `c5a1cbf…` (update) | `92d392cf…` + `fd5e2fef…` (web) + `6e03f65…` (update) | two pins moved |
| acadrust (DWG bridge) | 0.6.6 | **0.6.6** | unchanged |
| egui / eframe | 0.37 | **0.37** | unchanged |

Every v0.18.0 figure in this table was re-run this round with the same `git show v0.18.0:<path>` and
grep/perl commands, not carried from the old ledger, except the menu-breadth row (the checklist file
is unchanged and was not regenerated). The only new headline count is the UI-only 60
(and the derived app catalog 517). `README.md`/`ROADMAP.md` percentages are not used here.

## 3. Uncertain / not verified

- **No live catalog.** No `cadcraft-cli` is installed and the bundle ships none, so
  `cadcraft-cli commands | jq length`, the CLI `--help` and headless runs were not possible. 457 is a
  source derivation (439 literal + 18 macro, zero duplicates), cross-checked by the same method at
  v0.18.0.
- **No GUI launch**, so the Keyboard Shortcuts dialog, alias Import, Right-Click Customization, the
  in-place MTEXT/multileader editors, the Properties palette’s multi-selection and the macOS sheet
  dialogs are code-read, not observed. Their in-repo tests were not run.
- **No browser run**, so `window.cadcraft` is code-read (app wiring plus the shared crate’s API
  description). Its 30 s default timeout and 64-in-flight limit come from the `craft-web-api`
  crate's `page.rs` in `storytold/craft-libs` at pin `fd5e2fef…`, not from this checkout.
- **No real third-party DWG was opened or saved.** The proxy claims rest on
  `crates/dwg/src/proxy_transport.rs`, `crates/dwg/src/lib.rs`, and the synthetic tests
  `crates/io/tests/registered_proxy.rs` / `hard_owned_objects_kept.rs`; the `notSaved`/read-note
  wording is code-read.
- **Menu breadth 298/491** is carried from the 2026-11-01 checklist; it was not regenerated at
  either tag.
- **Flatpak** manifests were read, not built or installed; the 0.20.1 self-update fix is verified only
  by the manifest permission and its test.
- **MTEXT shaping**: the bidi/Lam-Alef/`\W` fixes are code-read; no Arabic-script drawing was
  rendered.
- **SpaceMouse** behaviour on Windows/Linux (2D pan/zoom via raw HID per `docs/gaps.md`) was not
  tested on a device.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `README.md`: SHX fonts “aren't read yet” | `crates/fonts/src/shx/` reads shape, big and unifont files; gaps FF8 documents it |
| `README.md` tagline “2D and 3D” | no 3D (`docs/gaps.md`); DVIEW’s 3D options refuse |
| `ROADMAP.md` (2026-10-24): “dynamic blocks can't be authored and xrefs can't be edited in place” | accurate; but its old “no XCLIP” / “no REFEDIT” claims are gone and must not be repeated |
| `docs/parity-checklist.md`: 449 commands, 298/491 | generated 2026-11-01, before both tags; the registry derives to 457 |
| `docs/file-format-parity.md` line 54/93: proxy objects “not measured”, “other kinds are dropped by DWG save” | `crates/dwg/src/proxy_transport.rs` now preserves registered proxies/objects with their classes; the doc table lags |
| `docs/file-format-parity.md` historical note “measured with 0.6.3” | the actual pin is `acadrust = "0.6.6"` (`crates/dwg/Cargo.toml`); the note is historical |
| `docs/localization.md` used to omit Vietnamese | fixed this tag: it lists all 19 languages, `vi` included |
| `docs/ui-parity.md` shortcut section: 28 entries + 23 command `.key()`s, no user dialog | `crates/ui-egui/src/keys.rs` adds user shortcuts, `ui.shortcuts`, and the dialog; the static count is no longer the whole story |
| `apps/cadcraft-cli/src/args.rs` help for `--view current`: “extents plus a 10% margin” | `crates/engine/src/session/files.rs` opens on the saved view (`$VIEWCTR`/`$VIEWSIZE`) and falls back to extents |
| `docs/plotters.md` (before this tag): model-space PDF plots don't apply the paper's margins | `crates/io/src/pdf.rs` applies `margins` to a model-space plot at both tags; the doc was corrected at this tag, so this was doc drift, not a code change |
| `docs/customization.md`: driving CADCraft “from outside” lists the control channel, MCP and CLI | the web build now also exposes `window.cadcraft` (`apps/cadcraft-web/src/api.rs`), which the doc does not mention |

## 5. Verification commands (read-only, run at the tag)

```sh
git -C <checkout> rev-parse HEAD                                   # 7526dc62c14e71b3c8d46e73bbf1fa29ef506af1
git -C <checkout> diff --shortstat v0.18.0..HEAD                   # 146 files, 8144 insertions(+), 856 deletions(-)
git -C <checkout> diff --name-status v0.18.0..HEAD | cut -f1 | sort | uniq -c   # 14 A, 132 M, 0 D
git grep -o 'CommandSpec::new(' HEAD -- '*.rs' | wc -l             # 441 sites (2 are macro bodies)
perl -0777 -ne 'while (/CommandSpec::new\(\s*"([^"]+)"/g) { print lc "$1\n"; }' \
  $(find crates apps -name '*.rs') | sort -u | wc -l               # 439 literal ids
grep -cE '^\s+gc!\("' crates/engine/src/cmd/constraints.rs         # 12
grep -cE '^\s+dc!\("' crates/engine/src/cmd/constraints.rs         # 6
awk '/pub const UI_COMMANDS/,/^];/' crates/ui-egui/src/menus.rs | grep -cE '^\s+\("ui\.'   # 60
grep -c '"name": "' crates/mcp/src/tools.rs                        # 15
sed -n '/^const METHODS: &\[(&str/,/^\];/p' crates/ui-egui/src/control.rs | grep -cE '^\s+\("[a-z_.]+"'   # 27
sed -n '/^const HEADLESS_METHODS/,/^\];/p' crates/mcp/src/backend.rs | grep -cE '^\s+\("[a-z_.]+"'       # 12
sed -n '/pub(crate) enum Command/,/^}/p' apps/cadcraft-cli/src/args.rs | grep -cE '^\s+[A-Z][A-Za-z]+\(' # 8
grep -oE 'code: "[A-Za-z-]+"' crates/ui-egui/src/i18n.rs | sort -u | wc -l                # 19
sed -n '/pub fn standard_patterns/,/^}/p' crates/doc/src/library.rs | grep -c 'name: "'  # 23
grep -n 'ALL: \[(u32, &str); 14\]' crates/engine/src/snap.rs        # 14 object snaps
grep -n 'pub const READ\|pub const WRITE' crates/doc/src/format.rs  # 4 read / 6 written
grep -n 'acadrust = ' crates/dwg/Cargo.toml                        # acadrust = "0.6.6"
head -12 docs/parity-checklist.md                                  # 449 commands, 298/491 (2026-11-01)
# id sets at both tags (multiline-aware; re-wrapped registrations defeat single-line greps):
for t in v0.18.0 HEAD; do git ls-tree -r --name-only $t | grep '\.rs$' | \
  while read -r f; do git show "$t:$f"; done | \
  perl -0777 -ne 'while (/CommandSpec::new\(\s*"([^"]+)"/g) { print lc "$1\n"; }' | sort -u; done
# installed bundle, read-only:
#   <installed CADCraft bundle>/Contents/MacOS/CADCraft --version
#   <installed CADCraft bundle>/Contents/MacOS/CADCraft --help
```

## Round 2026-11-12 (refresh)

- Re-pinned to **v0.20.1** = `7526dc62c14e71b3c8d46e73bbf1fa29ef506af1` (installed
  `cadcraft 0.20.1 (7526dc62c14e71b3c8d46e73bbf1fa29ef506af1)`, bundle id
  `ai.storyteller.cadcraft`). Previous audit v0.18.0 = `32238e83c2c8bf643994132883e94bc96961f649`.
- Re-derived and found **unchanged**: 457 engine commands (439 + 18), 441 static sites, 15 MCP
  tools, 27/12 control methods, 8 CLI verbs, 19 languages, 23 hatch patterns, 14 snaps, 4/6 formats
  plus 4 raster formats, acadrust 0.6.6, egui 0.37. **Changed**: UI-only **59 → 60** (`ui.shortcuts`).
- New behaviour documented from the diff: Keyboard Shortcuts dialog and preference store; alias
  persistence and `.pgp` Import; Right-Click Customization; in-place MTEXT editing of existing text
  and multileader text editing; Properties palette for several objects of one type; DWG proxy
  preservation; the `window.cadcraft` web page API; control-token hardening; macOS sheet dialogs;
  Flatpak update permission.
- Corrected previous drift: `docs/localization.md` now lists Vietnamese (resolved);
  `docs/file-format-parity.md` now states acadrust 0.6.6 in its main text (historical 0.6.3 note
  remains); ROADMAP no longer says “no XCLIP”/“no REFEDIT”; polyline offsets recompute arc bulges;
  `docs/plotters.md` no longer claims model-space PDF plots ignore the paper margins (the code
  applied them at both tags). README’s SHX and “2D and 3D” statements remain wrong.
- Every repo-relative path cited in `SKILL.md` and this ledger was re-resolved against v0.20.1. There
  were no `references/*.md` files to preserve; `agents/openai.yaml` is unchanged because the display
  name and one-line description still fit.
- Carried forward, not re-measured: the v0.17.0 figures (451 commands) because that tag is absent
  from the shallow checkout; menu breadth 298/491 because it needs a build; the “88 synthetic file
  tests” in `docs/gaps.md` because test execution is out of scope.
