# FilmCraft — evidence ledger (tag v0.18.0)

Audit basis: this checkout is tag **`v0.18.0`**, commit **`015d5b3ea37e1202a529e6245d3cc021c8c16ffd`** ("Release 0.18.0"); the previous skill was pinned at v0.17.0 = `eb59ec09daaea519c9c8fffa404a594ae50d00e0`. Installed bundle: `/Applications/FilmCraft.app`, `--version` → `filmcraft 0.18.0`, `Info.plist` CFBundleShortVersionString `0.18.0`, CFBundleIdentifier `ai.storyteller.filmcraft`. Inspection date **2026-11-07**. The GUI was never launched; the bundle was only asked for its version string and plist values.

Round shape: `git rev-list --count v0.17.0..HEAD` = **1** (the checkout squashes the release), so the round is measured as a tree diff — `git diff --shortstat v0.17.0..HEAD` = **308 files changed, 14 708 insertions, 1 517 deletions**. No commit count is quoted anywhere in the skill.

## 1. Capability claims → evidence → tier

| # | Claim (v0.18.0 unless stated) | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | New engine command `presets.scan`; no id removed | `crates/engine/src/presets.rs` (`commands()` list of 8 `presets.*` specs); id-set diff v0.17.0→v0.18.0 (method in §2) | implemented |
| 2 | Premiere `.prfpset` (plain/gzip XML) and FilmCraft `.json` effect presets import; auto-scanned folder | new `crates/engine/src/prfpset.rs`; `is_preset_file` / `parse_file_detailed` in `crates/engine/src/presets.rs`; `file.import` preset branch in `crates/engine/src/commands.rs` | implemented |
| 3 | H.264 High 10 (10-bit 4:2:0) and High 10 Intra encode from the built-in encoder | `crates/export/src/settings.rs` (`H264Profile::High10`), `crates/export/src/encoders.rs` (`Profile::High10`), `crates/export/src/mxf_out.rs:52` (`profile_idc` 110), `crates/h264enc/src/lib.rs` (345 changed lines) | implemented |
| 4 | Two new built-in presets, 42 → 44 | `crates/export/src/presets.rs` (`high10()` helper; "H.264 High 10 Master"/"Intra"); `p(` count 44 vs 42 at v0.17.0 | implemented |
| 5 | `h264Profile` / `h264IntraOnly` export params; APV profiles `4444-10|4444-12|400-10` | `crates/engine/src/commands.rs` (`file.exportMedia` params string) | implemented |
| 6 | `timeline.move` accepts a time object and refuses a bad entry by index | `crates/engine/src/commands.rs` (`move_clips`), `docs/control-protocol.md` | implemented |
| 7 | `clip.speedDuration` gained `maintainPitch`; `sequence.inspect` reports it | `crates/engine/src/commands.rs` (params + handler), `crates/engine/src/linked_speed_tests.rs` | implemented |
| 8 | Image-sequence export returns first still as `path`, plus `lastPath`/`basePath`; CLI prints "first to last" | `crates/engine/src/export_tools.rs:590`, `apps/filmcraft-cli/src/main.rs` (`written_paths`), `docs/agents.md` | implemented |
| 9 | Caption export warnings name dropped/replaced characters; TTML/DFXP write `xml:lang`; import takes `name`/`language` | `docs/captions.md`; `crates/engine/src/captions.rs` (`captions.import` params, `captions.export`) | implemented |
| 10 | Unreadable clip explains why; Apple Intermediate Codec named | `crates/codecs/src/lib.rs:120-135`, `crates/codecs/src/mp4/tests.rs` (`icod` sample entry) | implemented |
| 11 | A key chord matches only with exactly its modifiers | `crates/ui-egui/src/app/keys.rs:216`, `crates/ui-egui/src/menus.rs:1131` | implemented |
| 12 | Effect names resolve through an alias table (AE/Premiere/Spanish) | `crates/engine/src/commands.rs` (`resolve_effect_alias`) | implemented |
| 13 | Interchange: AAF `Usage_TopLevel`, EDL Align Timecode relink, name-only EDL clip is missing, OTIO sample rate, export reports name omitted video tracks, `bitDepth` 16/24 | `crates/engine/src/aaf_omf.rs`; `crates/interchange/src/{aaf,edl,otio,omf}/`; `crates/engine/src/interchange.rs` | implemented |
| 14 | 17 MCP tools + 2 resources, unchanged; only a bounded parse-error queue | `crates/automation/src/server.rs` (`MAX_QUEUED_PARSE_ERRORS = 64`, 17 `#[tool(`) | implemented |
| 15 | 24 control methods incl. `ui.docking`, unchanged | `crates/ui-egui/src/control.rs` dispatch arms; file not in the round diff | implemented |
| 16 | 13 CLI subcommand words, unchanged | `apps/filmcraft-cli/src/main.rs` (HELP block + dispatch incl. `"version"` at the subcommand position) | implemented |
| 17 | 10 built-in workspaces, 28 panel kinds, chords 1–8 + 0 | `crates/ui-egui/src/dock.rs` (`WORKSPACES: [&str; 10]`, `PanelKind::ALL: [PanelKind; 28]`), `crates/ui-egui/src/panels/keyboard.rs`, `crates/ui-egui/src/menus.rs` | implemented |
| 18 | 17 UI languages (16 catalogues + English) | `crates/ui-egui/src/i18n/*.tsv` (16 files) | implemented |
| 19 | Project schema 17, unchanged | `crates/format/src/lib.rs` (`assert_eq!(SCHEMA_VERSION, 17)`); `crates/format` not in the diff | implemented |
| 20 | 21 export formats, unchanged | `crates/export/src/format.rs` (`Format` enum, 21 variants) | implemented |
| 21 | 7 caption formats, 27 blend modes, 10 log curves | `crates/captions/src/lib.rs` (`Format::ALL: [Format; 7]`); `BLEND_MODES` in `crates/project/src/effect.rs`; `LogCurve::ALL: [LogCurve; 10]` in `crates/color/src/log.rs` | implemented |
| 22 | No `.prproj`, no plug-ins, AV1 has no encoder, DNG-only raw, STT/Kokoro off in releases | `docs/gaps.md`; `crates/export/src/lib.rs` format availability; packaging scripts pass no features | not implemented (verified absent) |

## 2. Count methods used this round

| Surface | v0.17.0 | v0.18.0 | Method |
|---|---:|---:|---|
| Engine command ids | full set | **+1 (`presets.scan`)**, 0 removed | Same extraction at both tags: first string literal of every `cmd!(`/`query!(` invocation, plus first-argument literals in each engine module that builds `CommandSpec` (test files excluded); set difference. `camera_keys!` unchanged at one site (9 cameras × 2 ids) |
| MCP tools / resources | 17 / 2 | **17 / 2** | `grep -c '#\[tool('` in `crates/automation/src/server.rs`; resources at the server builder |
| Control methods | 24 | **24** | Dispatch arms in `crates/ui-egui/src/control.rs`; the file is not in the round diff |
| CLI subcommand words | 13 | **13** | HELP block + dispatch words in `apps/filmcraft-cli/src/main.rs` |
| Export formats | 21 | **21** | `Format` enum in `crates/export/src/format.rs` |
| Built-in presets | 42 | **44** | `p(` entries inside `builtin_presets` in `crates/export/src/presets.rs` |
| Panels / workspaces | 28 / 10 | **28 / 10** | `PanelKind::ALL: [PanelKind; 28]`, `WORKSPACES: [&str; 10]` in `crates/ui-egui/src/dock.rs` |
| UI languages | 17 | **17** | `ls crates/ui-egui/src/i18n/*.tsv` = 16 + English |
| Project schema | 17 | **17** | `SCHEMA_VERSION = MIGRATIONS.len() + 1` with `assert_eq!(SCHEMA_VERSION, 17)` |
| Caption formats | 7 | **7** | `Format::ALL: [Format; 7]` in `crates/captions/src/lib.rs` |
| Blend modes / log curves | 27 / 10 | **27 / 10** | `BLEND_MODES` (27 entries) and `LogCurve::ALL: [LogCurve; 10]` |
| Transitions | 84 + 21 | **84 + 21** (+7 obsolete) | `tr(` definitions in `crates/project/src/vtransition.rs`: 112 total = 84 current across 10 folders + 21 Legacy + 7 Obsolete |
| Shortcut presets | 4 | **4** | `crates/engine/src/shortcuts.rs` preset name constants |

## 3. Carried forward, not re-derived

- Effect catalogue totals: **93 video effects / 16 folders** and **53 audio effects**. The defining modules
  (`crates/project/src/effect.rs`, `crates/project/src/effect/`) are **not** in the round diff, so the
  totals were carried after a path check; only blend modes and transitions were re-counted as spot checks.
- Deep feature prose (multicam, trimming, Essential Sound, proxies, Project Manager, ingest, GPU/CPU
  parity, export ranges) was path-verified and carried; this was a pin-and-verify refresh, not a new
  feature audit.
- The limitation list was checked against `docs/gaps.md` at this tag; the H.264 row was updated because
  the code gained High 10.

## 4. Uncertain / not verified

- **Static registry totals are not quoted.** The registry is assembled from ~15 engine modules that each
  build `CommandSpec`, and the previous skill's "662 engine ids / 215 UI-only ids" could not be
  reproduced by any method at this tag. The skill quotes the measured **delta** (+1 id, none removed)
  and defers to the runtime list. The UI-only ids are `uic!` declarations in `crates/ui-egui` (223
  occurrences repo-wide, 147 in `crates/ui-egui/src/menus.rs`); no `uic!` entry was added this round.
- **No runtime enumeration.** The macOS bundle ships only the GUI binary, so `filmcraft-cli commands`,
  `describe` and MCP `command_list` were not run.
- **GUI behaviour not observed.** Workspace/panel behaviour, dialogs and the Open-Project save prompt are
  read from code and docs, not seen.
- One new dotted literal in the id diff, `json.unreadable`, is a backup-file suffix
  (`crates/engine/src/presets.rs`), not a command id — excluded from the delta.

## 5. Doc-vs-code drift found at this tag (code wins)

| Doc / previous-skill statement | Code reality |
|---|---|
| README "26 blend modes", "around 30 transitions" | 27 blend modes; 84 transitions + 21 Legacy |
| README ">650 engine commands" | Registry total not statically reproducible from this repo layout; +1 this round |
| `docs/roadmap.md` M6 "24 built-in presets" | 44 built-in presets |
| Previous skill body: schema 15, languages 12, workspaces 9, CLI 12, control 23 | 17, 17, 10, 13, 24 |
| Previous skill body: craft-libs at `92d392cf…`; `references/formats.md`: `f0ad6c1e…` | One pin, `c5a1cbfb…`, for `craft-docpath`/`craft-media`/`craft-ui`/`craft-update` |
| Previous skill body: `Alt+Shift+1..8` workspaces | Correct for the range: 1–8 map to Editing…Review, `Alt+Shift+0` resets, Vertical/All Panels have no chord |
| Previous skill: H.264 exports are 8-bit only | High 10 / High 10 Intra (10-bit 4:2:0) from the built-in encoder |
| Previous skill: no Premiere interop beyond XML/AAF/OTIO | `.prfpset` effect presets import (new) |

## 6. Verification commands (read-only, re-runnable)

```sh
git -C <clone> rev-parse HEAD                                  # 015d5b3ea37e1202a529e6245d3cc021c8c16ffd
git -C <clone> diff --shortstat v0.17.0..HEAD                  # 308 files changed, +14708/-1517
grep -c '#\[tool(' crates/automation/src/server.rs             # 17
grep -c 'uic!(' crates/ui-egui/src/menus.rs                    # 147 (UI-only ids)
grep -n 'WORKSPACES: \[&str' crates/ui-egui/src/dock.rs        # [&str; 10]
grep -n 'PanelKind; 28' crates/ui-egui/src/dock.rs             # 28 panel kinds
ls crates/ui-egui/src/i18n/*.tsv | wc -l                       # 16 catalogues (+English)
grep -n 'assert_eq!(SCHEMA_VERSION' crates/format/src/lib.rs   # 17
grep -n 'pub enum Format' crates/export/src/format.rs          # 21 variants follow
grep -n 'H264Profile::High10' crates/export/src/{encoders,mxf_out}.rs
grep -n 'FILMCRAFT_CONTROL_TOKEN' apps/filmcraft/src/args.rs apps/filmcraft/src/control_server.rs
grep -oE 'rev = "[0-9a-f]{8}' Cargo.toml | sort -u             # one craft-libs rev, c5a1cbfb
"/Applications/FilmCraft.app/Contents/MacOS/FilmCraft" --version   # filmcraft 0.18.0 (version query only)
```
