# FilmCraft — evidence ledger (tag v0.14.0)

Audit basis: this checkout is tag **`v0.14.0`**, commit **`a2d8e9ce269aba9c399e36262522e11456df6fbf`**
(shallow clone at the release tag). Inspection date **2026-10-29**. Installed
`/Applications/FilmCraft.app` prints `filmcraft 0.14.0`; the GUI was never launched.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | No command added or removed this release | release PR list contains no registry PR; `camera_keys!` generation site intact at `crates/engine/src/multicam.rs:132` (9 generated ids) | implemented (unchanged) |
| 2 | 17 MCP tools + 2 resources, unchanged | `crates/automation/src/server.rs` — 17 `#[tool(` annotations (the 8 `tool_router` hits are refs/imports), resources at the server builder | implemented |
| 3 | 23 control methods; token auth unchanged | `crates/ui-egui/src/control.rs` (method strings); `apps/filmcraft/src/control_server.rs:8` ("without a configured credential the listener stays closed"); `apps/filmcraft/src/args.rs:12` (`FILMCRAFT_CONTROL_TOKEN`) | implemented |
| 4 | 12 CLI subcommand words | `apps/filmcraft-cli/src/main.rs` HELP/dispatch | implemented |
| 5 | `effects.apply` answers applied instances `{clip, index, effect}` | PR #1841; `crates/engine/src/commands.rs` (`effects.apply` also names graphic layers' dedicated commands in its error) | implemented |
| 6 | `effects.setParam` reports parameter and accepted value | PR #3281 | implemented |
| 7 | Export `maxThreads` CPU cap; H.264 export ~20 % faster byte-identical | PRs #1870, #3456; `crates/export/src/{format,run}.rs` | implemented |
| 8 | Uncompressed QuickTime decode (raw 24-bit RGB, 2vuy, v210) | PR #2415; `crates/codecs/src/{video,mp4}.rs` | implemented |
| 9 | Trim Mode linked audio; Alt-drag side trim; Alt-selected side enable; Unlink mixed selection; move-plan duplicate rejection | PRs #3224, #3301, #3235, #2011, #1915 | implemented |
| 10 | Mask vertex marquee/Shift multi-select + move | PR #3209 | implemented |
| 11 | Close Gap all-gaps; `clip.audioChannels` no-reset; Lift/Extract clipboard; Transform auto-center | PRs #2008, #2483, #3211, #2597 | implemented |
| 12 | OTIO nested-sequence limit; TTML/DFXP overflow fix; MCC bound; FCPXML empty-ref fix | PRs #2287, #2394, #3307, #2653; `crates/interchange/src/lib.rs`; `crates/captions/src/lib.rs` | implemented |
| 13 | 10-bit Y'CbCr per-code normalisation; Counting Leader beeps by source rate; `.cube` TITLE `#`; previews folder only when needed | PRs #3216, #1950, #2427, #2387 | implemented |
| 14 | PNG Sequence RGB when alpha off; IME preedit on video; French complete | PRs #1869, #3340, #3226; `crates/ui-egui/src/i18n/` (11 catalogs + English) | implemented |
| 15 | Startup update prompt; Windows per-user; XWayland DnD; AV1 grain validation; egui 0.37 + craft-ui | PRs #3298, #3419, #634, #2888, #3249, #2549, #3445 | implemented |
| 16 | Craft-libs crates at one rev | `Cargo.toml`: `craft-docpath/media/ui/update` → `92d392cf…` | implemented |
| 17 | No `.prproj`; no plug-ins; AV1 no encoder; DNG-only raw; no Productions; STT off in releases | `docs/gaps.md` | not implemented (verified absent) |

## 2. Automation-surface counts: v0.13.0 → v0.14.0

| Surface | v0.13.0 | v0.14.0 (measured) | Change |
|---|---:|---:|---|
| Engine command ids | 662 static (literals + 9 `camera_keys!`) | **unchanged set** | the refactor moved declarations between macro forms; no registry PR; `filmcraft-cli commands` is the authority |
| MCP tools | 17 + 2 resources | **17 + 2** | unchanged |
| Control methods | 23 | **23** | unchanged; token auth unchanged |
| CLI subcommand words | 12 | **12** | unchanged |
| Export formats | 21 | **21** | unchanged (+`maxThreads` option, faster H.264) |
| Presets / caption formats / panels / workspaces / languages / schema | 39 / 7 / 28 / 9 / 12 / 15 | **same** | French completed; no schema bump |
| Craft-libs pins | split revs | **one rev `92d392cf…`** | unified |

## 3. Uncertain / not verified

- Static id enumeration across tags is not byte-comparable this round (the shared-module refactor
  changed macro forms); the unchanged-registry claim rests on the release PR list, the intact
  `camera_keys!` site, and the CLI being the runtime authority.
- Schema version 15 carried (no migration PR this release).
- GUI behaviour not launched; registry + docs + packaging are the evidence.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| README "26 blend modes" / "around 30 transitions" | 27 / 84+21 |
| README upload-destination alt text | one destination: `export.destination.mediaFile` |
| Older gap lists (work area, mixer commands) | implemented since 0.13.0 |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # a2d8e9ce269aba9c399e36262522e11456df6fbf
grep -c '#\[tool(' crates/automation/src/server.rs              # 17
grep -n 'camera_keys!' crates/engine/src/multicam.rs            # 1 generation site (9 ids)
grep -n 'FILMCRAFT_CONTROL_TOKEN' apps/filmcraft/src/args.rs apps/filmcraft/src/control_server.rs
grep -oE 'rev = "[0-9a-f]{8}' Cargo.toml | sort -u              # one craft-libs rev
ls crates/ui-egui/src/i18n/*.tsv | wc -l                        # 11 catalogs (+English)
```
