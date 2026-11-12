# DesignCraft — evidence ledger (tag v0.20.1)

Audit basis: this checkout is tag **`v0.20.1`**, commit
**`33a467872268c98536231491865b4011b0275b17`** ("Merge tested main for v0.20.1", 2026-11-11).
Inspection date **2026-11-12**. The installed `DesignCraft.app` bundle reports
`CFBundleShortVersionString 0.20.1`, `DesignCraftBuildCommit 33a467872268c98536231491865b4011b0275b17`
and `CFBundleIdentifier ai.storyteller.designcraft`; its bundled CLI prints
`designcraft-cli 0.20.1`, the desktop binary `designcraft 0.20.1`. The GUI was never launched. The
previous pin was v0.18.0 = `58ac6d29b260e033f4291afc4318b507cfd90fd9`; that ref is present in the
same shallow checkout and is the diff base for every set comparison below.

v0.18.0 → v0.20.1 delta (from `git diff`, not release notes; 146 files, +8007/−658): no registry
change (555 engine ids / 190 UI rows at both tags, 26 MCP tools, 11 CLI subcommands, format 4).
Behaviour: anchored text frames keep their own stories and ids through copy/paste/duplicate/
release/delete; the Links panel checks statuses on a worker thread and reuses a size+time
fingerprint kept with the document; `preflight.run` gained the `whiteOverprint` kind;
`layout.pages.delete`/`applyParent` validate indices and return `{deleted}`/`{applied}`; scripts
are bounded in depth, steps and resolved bytes; table commands accept `story?`/`table?` without a
table selection; GREP refuses subroutine calls; whole-file reads refuse devices/FIFOs and cap at
4 GiB; hyperlink and data-merge ranges follow story edits; pt-BR is ~100% translated; the canvas
draws a spread spine (screen only); the updater installs at exit and the Flatpak manifests grant
its update permissions.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | **555** engine command ids, unchanged at v0.20.1 | Python scan of `cmd!(` in `crates/engine/src` (skipping `query`/`noundo`, first string literal), unique set 555 at `v0.18.0` and HEAD; live `designcraft-cli commands` = 555 entries | implemented |
| 2 | **190** UI command rows, unchanged | `crates/ui-egui/src/menus/ui_commands.rs` `UI_COMMANDS`, row count 190 at both tags | implemented |
| 3 | **26** MCP tools, unchanged | `crates/mcp/src/tools.rs` `tool_definitions` (26 `tool(` calls) and the dispatch names; `crates/mcp/src/server.rs` | implemented |
| 4 | **28** control dispatch arms / **31** accepted method strings; source unchanged | `crates/ui-egui/src/control.rs` `handle_request` top-level arms (29 lines, one guarded duplicate of `ui.menu.invoke`); 30 dotted names + `command` alias; `apps/designcraft/src/control_server.rs` byte-identical to v0.18.0 | implemented |
| 5 | **11** CLI subcommands, unchanged | `apps/designcraft-cli/src/main.rs` `USAGE` and dispatch; installed `--help` lists `run, commands, describe, script, app, mcp, perf, bench, validate-pdf, thumbnail, links` | implemented |
| 6 | Native format **version 4**, unchanged; stored assets read at archive size | `crates/format/src/lib.rs:29` `VERSION: u32 = 4`; `Limits`, `read_entry` | implemented |
| 7 | **10** hyphenation languages (English, Danish, Dutch, French, German 2006, Greek, Italian, Norwegian, Portuguese, Spanish) | `crates/compose/src/hyphen.rs` module doc and `Lang::for_language`; unchanged file | implemented |
| 8 | **15** non-English interface languages; pt-BR ~100% | `crates/ui-egui/src/i18n.rs:26` `LANGUAGES`; `crates/ui-egui/src/i18n/pt_br.rs`; `ROADMAP.md` language table and 2026-11-04 progress-log line; `docs/localization-parity.md` | implemented (percentages doc-derived) |
| 9 | Anchored text frames keep stories and ids through copy, paste (also cross-document), duplicate, release, delete; nesting ≤ 64 | `crates/doc/src/anchored.rs` module doc, `NESTING: usize = 64`, `fix_anchored_text_frames`, `adopt_anchored`; `crates/engine/src/cmd/anchored.rs` release and tests | implemented |
| 10 | `preflight.run` reports `whiteOverprint` for white/[Paper] fills, strokes, gaps, ruby and kenten | `crates/engine/src/cmd/preflight.rs:1` module doc; `crates/engine/src/cmd/preflight/white_overprint.rs:24` `KIND`; #2401 | implemented |
| 11 | `layout.pages.delete` → `{deleted}`, `layout.pages.applyParent` → `{applied}`; an index past the last page is refused | `crates/engine/src/cmd/layout/registry.rs:841` `page_indices`, `distinct_pages`; command specs at :88 and :170 | implemented |
| 12 | Scripts bounded: depth 8, 100 000 steps, 16 MiB interpolation, 64 MiB reference, 256 MiB step params | `crates/engine/src/script.rs:115,125,130,242,245` | implemented |
| 13 | Table commands with `story?`/`table?` run without a table selection; a missing/foreign table is an error | `crates/engine/src/cmd/table/target.rs` `target`, `table_story`; `crates/engine/src/cmd.rs` `named_table`; `docs/mcp.md` §Tables without a selection | implemented |
| 14 | Links panel checks on a worker thread; document keeps a per-asset size+time fingerprint so an unchanged link is not re-read | `crates/ui-egui/src/links_worker.rs` (`REFRESH_MIN`, `MAX_WORKERS`, `SUPERSEDE_AFTER`); `crates/engine/src/cmd/links.rs` `loaded_fingerprint`, `loaded_unchanged`, `status_cached`; `crates/doc/src/assets.rs` `link_fingerprint`; #1444 | implemented |
| 15 | Hyperlink and data-merge source ranges adjust on story edits | `crates/doc/src/edit.rs:834` `adjust_text_ranges`; `crates/engine/tests/hyperlink_offsets.rs`; #1219 | implemented |
| 16 | GREP refuses subroutine calls/recursion; empty-match scanning is bounded | `crates/compose/src/grep.rs` (`contains_subroutines` check, `SEARCHES_PER_MATCH`); a `find.change` run with `find: "(a\g<1>)"` errors "GREP: subroutine calls and recursion are not supported" | implemented (new error) |
| 17 | Whole-file reads refuse non-regular files (devices, FIFOs) and cap at 4 GiB; recovery entries refuse links | `crates/engine/src/io.rs:62` `MAX_FILE_BYTES`, `read_whole`, `open_read`; `crates/engine/src/recovery.rs` `read_entry_file` | implemented |
| 18 | Package copies the loaded bytes and refuses a changed font destination | `crates/engine/src/cmd/package.rs` `OutputRoot::copy`, `same_contents` | implemented |
| 19 | Canvas draws a spread spine hairline where pages meet; never exported | `crates/doc/src/page.rs:440` `page_seams`; `crates/ui-egui/src/canvas/page_decor.rs:92` `draw_spine`; #1838 | implemented (screen only) |
| 20 | Updater installs at exit, reports installing/ready/installed/failed; Flatpak manifests grant network + host update helper | `crates/ui-egui/src/updates_ui.rs`; `crates/ui-egui/tests/flatpak_updates.rs`; `packaging/linux/flatpak/*.yml` (0.20.1 release note: Flatpak update repair) | implemented |
| 21 | Placed-PDF layer choices render; IDML/PSD graphic-layer options are retained but not rendered | `crates/engine/src/cmd/pdflayers.rs`; `crates/pdf/src/optional_content.rs`; `docs/graphic-layer-options.md`, `docs/pdf-layer-visibility.md` | implemented / partial |
| 22 | No ExtendScript/UXP, no plug-in model, no media playback, no `.joboptions`, no PDF font repair | `docs/gaps.md` §§9, 10, 17, 22, 23, 28 | not implemented (verified absent) |

## 2. Automation-surface counts: v0.18.0 → v0.20.1

| Surface | v0.18.0 | v0.20.1 (measured) | Change |
|---|---:|---:|---|
| Engine command ids | 555 | **555** | none |
| UI `UI_COMMANDS` rows | 190 | **190** | none |
| MCP tools | 26 | **26** | none |
| Control dispatch arms / method strings | 28 / 31 (re-measured) | **28 / 31** | source byte-identical; earlier "27" corrected |
| CLI subcommands | 11 | **11** | none |
| Format version | 4 | **4** | none |
| Hyphenation languages | 10 | **10** | none |
| Non-English UI languages | 15 | **15** | none (pt-BR coverage changed) |

The published v0.18.0 round quoted 27 control methods. Re-measured at both tags with the method in
§5, the dispatch has 28 unique arms and 31 accepted method strings (`command` included); the count
was an undercount and is corrected here rather than carried. No other surface moved.

Carried forward rather than re-derived: the seven-section body, CLI flags and export-extension
routing, export command parameters, the coordinate/text-offset model, placed-PDF layer options,
shortcut import and the sample recipes. Each was path-checked against this checkout; only claims the
diff or a re-measurement contradicted were edited.

## 3. Uncertain / not verified

- No GUI launch and no builds: the Links worker/panel, the canvas spine and the updater dialog were
  read from code and unit tests, not seen on screen.
- `whiteOverprint` was exercised once on the sample: a [Paper]-filled frame with
  `object.attributes {overprintFill:true}` produced
  `{kind:"whiteOverprint", severity:"warning", message:"White or [Paper] fill set to overprint will not print", item, page}`.
  Its exclusions (text, [None], gradients, spot inks above a 0% tint) are read from
  `white_overprint.rs`, not each exercised.
- Anchored text frames were verified from code and the project's tests (copy/paste across
  documents, delete takes the story), not through a real clipboard round-trip.
- Localization percentages come from the maintainers' 2026-11-04 `i18n-report` (2,939 strings);
  `cargo xtask i18n-report` was not run. The pt-BR catalogue's own entry count was not used as a
  coverage measure.
- INDD/INDT and IDML fidelity on real files remains unmeasured by the project (`docs/gaps.md`
  §§2–4); IDML round-trip, EPUB/PPTX rendering and print were not re-tested.
- Control-method counts are source-derived; no control session was opened.
- The v0.18.0 checkout is shallow (two commits); the release-by-release split between v0.19.0 and
  v0.20.0 was not reconstructed — the delta is the whole v0.18.0 → v0.20.1 range.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `docs/target-app-parity.md:45` "446 engine commands … + 99 UI commands"; :461 "~200 commands" | 555 engine ids + 190 UI rows measured here |
| `docs/agents.md:29` and `apps/designcraft-cli/src/main.rs:69` (SCRIPT_HELP) "most commands ignore parameters they don't know" | CLI, MCP and control channel reject unknown params (`crates/engine/src/cmd/params.rs`, `crates/mcp/src/server.rs`) |
| `docs/localization-parity.md` "Other shipped languages" still prints Czech 99%, Polish 99%, Georgian ~100% | `ROADMAP.md`'s 2026-11-04 report over 2,939 strings gives Czech 69%, Polish 64%, Georgian 98%; the percentages in the older table were computed against a smaller catalogue |
| `ROADMAP.md:255` "alpha, ~0% and ~15–25 h away" | `ROADMAP.md:3` and `docs/gaps.md` §0 still say ~5–7 h; the two lines disagree |
| `docs/target-app-parity.md` Localization row says "15 translations beyond English" | `crates/ui-egui/src/i18n.rs` `LANGUAGES` lists 15 non-English languages — consistent |

## 5. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                   # 33a467872268c98536231491865b4011b0275b17
git -C <clone> diff --shortstat v0.18.0..HEAD                   # 146 files, +8007/-658
# engine ids: Python scan of cmd!( [query|noundo] "id" over crates/engine/src at both tags (method in §1)
<app>/Contents/MacOS/designcraft-cli --version                  # designcraft-cli 0.20.1
<app>/Contents/MacOS/designcraft-cli commands | python3 -c 'import json,sys;print(len(json.load(sys.stdin)))'  # 555
awk '/pub const UI_COMMANDS/,/^\];/' crates/ui-egui/src/menus/ui_commands.rs | grep -cE '^\s*\('   # 190
grep -cE '^\s+tool\(' crates/mcp/src/tools.rs                   # 26
sed -n '29p' crates/format/src/lib.rs                           # VERSION: u32 = 4
plutil -p <app>/Contents/Info.plist | grep -E 'Version|BuildCommit'
```

## Round 2026-11-07 (historical note, superseded)

Pinned to `v0.18.0` = `58ac6d2…` (installed `designcraft 0.18.0`). It reported +8 engine ids (547 →
555), +3 UI rows (187 → 190), `thumbnail` as the 11th CLI subcommand, Danish hyphenation, and
`file.exportBatch`. Those figures reproduced at v0.18.0 and are carried only where the v0.20.1
measurement confirms them.

## Round 2026-11-12 (this refresh)

- Re-pinned to `v0.20.1` = `33a4678…`; installed `designcraft 0.20.1`, bundled CLI `0.20.1`.
- Re-measured: engine ids 555 → 555, UI rows 190 → 190, MCP 26 → 26, CLI 11 → 11, format 4 → 4,
  hyphenation 10 → 10, control 28 arms / 31 strings (corrected from 27), non-English UI languages
  15.
- Corrected: the control-method figure; the Czech/Polish/Georgian localization percentages and
  pt-BR's rise to ~100%; the script limits (newly documented); the page-command result shapes; the
  table-without-selection targeting; the GREP subroutine refusal; the reference file's stale
  command counts and the non-existent `cmd/mod.rs` citation.
- Paths: every repo-relative path in `SKILL.md` and `references/agent-surfaces.md` was expanded
  against this checkout and exists.
