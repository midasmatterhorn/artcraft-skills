# DesignCraft — round 2026-11-12 changes

Re-pinned: v0.18.0 (`58ac6d2`) -> v0.20.1 (`33a4678`, installed `designcraft 0.20.1`; the bundled
`designcraft-cli` prints `designcraft-cli 0.20.1`). Clone HEAD verified at
`33a467872268c98536231491865b4011b0275b17`; `Info.plist` `DesignCraftBuildCommit` matches.
`git diff --shortstat v0.18.0..HEAD` = 146 files, +8007 / −658.

## Corrected / re-measured

- **The engine registry did not move: 555 command ids at both tags, none added or removed.** This
  round is a fix-and-hardening wave, unlike v0.18.0; new behaviour ships under existing ids. The
  same is true of the **190** `UI_COMMANDS` rows, **26** MCP tools, and **11** CLI subcommands.
  Say "unchanged at v0.20.1" rather than leaving the old sentence undated.
- **Control dispatch: 28 arms / 31 accepted method strings**, not 27. The 29 top-level match lines
  in `handle_request` include one guarded duplicate of `ui.menu.invoke`; the patterns name 30
  dotted methods plus the legacy `command` alias. `crates/ui-egui/src/control.rs` and
  `apps/designcraft/src/control_server.rs` are byte-identical to v0.18.0, so the surface itself
  did not change — the earlier absolute figure was an undercount and is replaced.
- **Localization corrected.** `crates/ui-egui/src/i18n.rs` `LANGUAGES` lists **15 non-English
  interface languages** (de, fr, es, ja, zh, ar, pt-br, it, uk, ru, cs, pl, ka, hu, sv). Brazilian
  Portuguese is now **2,936 of 2,939 strings (~100%)**, up from 1,933 (`ROADMAP.md` progress log
  2026-11-04; `docs/localization-parity.md`), and Russian is listed at 1,855 (63%). The old
  "Czech/Polish 99%, Georgian 100%" sentence came from pre-2,939 catalogue counts; the same
  2026-11-04 report now gives Czech 69%, Polish 64%, Georgian 98%, Swedish 98%, Italian 68%,
  Ukrainian 65%, Hungarian 65%. Percentages are the maintainers' report, not re-run here.
- **Scripts are bounded** (`crates/engine/src/script.rs`): nesting depth 8 (`MAX_SCRIPT_DEPTH`),
  100,000 steps across nested scripts (`MAX_SCRIPT_STEPS`), 16 MiB per `${…}` interpolation
  (`MAX_INTERPOLATED_BYTES`), 64 MiB per `$N.path` copy (`MAX_REFERENCED_BYTES`), 256 MiB per
  resolved step parameter tree (`MAX_STEP_PARAM_BYTES`). Previously undocumented.
- **Page commands validate and count.** `layout.pages.delete` returns `{deleted}` and
  `layout.pages.applyParent` returns `{applied}`; both refuse an index past the last page
  (`crates/engine/src/cmd/layout/registry.rs` `page_indices`, #2460). The old behaviour dropped a
  bad index silently.
- **Table commands can be targeted without a table selection**: commands whose params list
  `story?`/`table?` accept the id `table.insert`/`table.get` return, and default to the whole table
  when no cell range is given (`crates/engine/src/cmd/table/target.rs`, `docs/mcp.md` §Tables
  without a selection).
- **Anchored text frames are now first-class stories.** Copy, paste (also into another document,
  with placed graphics), duplicate, release and delete keep their own story and ids
  (`crates/doc/src/anchored.rs`, `crates/engine/src/cmd/anchored.rs`); nesting is bounded at 64.
- **Links checks moved off the UI thread** (`crates/ui-egui/src/links_worker.rs`: 2 s minimum
  poll, at most 4 workers, supersede after 200 ms) and the document keeps each link's size and
  time (`Asset::link_fingerprint`, `crates/doc/src/assets.rs`), so an unchanged graphic is not
  re-read on a network share (#1444). The `links.list` command is still synchronous and its result
  shape is unchanged.
- **Preflight reports `whiteOverprint`** for white or [Paper] fills, strokes, stroke gaps, ruby and
  kenten set to overprint (`crates/engine/src/cmd/preflight/white_overprint.rs`, #2401).
- **GREP refuses subroutine calls and recursion** (`\g<name>`, `\g<1>`, `\g<-1>`) instead of
  compiling them, and bounds empty-match scanning (`crates/compose/src/grep.rs`). A GREP style
  that used them now errors.
- **Whole-file reads refuse non-regular files and cap at 4 GiB** (`crates/engine/src/io.rs`
  `MAX_FILE_BYTES`, `read_whole`): a device such as the zero device, a FIFO and other endless
  sources return an error instead of hanging. Recovery entries refuse links
  (`crates/engine/src/recovery.rs`).
- **Hyperlink and data-merge source ranges follow story edits** (`crates/doc/src/edit.rs`
  `adjust_text_ranges`, `crates/engine/tests/hyperlink_offsets.rs`); previously an edit could leave
  a hyperlink pointing at the wrong bytes.
- **Package copies the bytes it loaded** rather than reopening a path that may have been swapped,
  and refuses to overwrite a font destination that changed after loading
  (`crates/engine/src/cmd/package.rs`).
- **Verification-protocol pin** moved from 0.18.0/`58ac6d2…` to 0.20.1/`33a4678…`.
- **Path and count corrections inside the skill**: the reference file's non-existent `cmd/mod.rs`
  citation is now `crates/engine/src/cmd.rs`; `references/agent-surfaces.md` §11 no longer says 542
  engine / 176 UI commands (it is 555 / 190) and §4 no longer says 26 control arms.

## Method

- `git rev-parse HEAD` = `33a467872268c98536231491865b4011b0275b17`, tag `v0.20.1`; the shallow
  checkout carries both `v0.18.0` (`58ac6d29b260e033f4291afc4318b507cfd90fd9`) and HEAD, so every
  set diff is against the previous pin.
- Engine ids: a Python scan for every `cmd!(` in `crates/engine/src`, skipping the optional
  `query`/`noundo` modifier and taking the first string literal; 555 unique at both tags, no
  duplicates. Live cross-check: the installed `designcraft-cli 0.20.1 commands` returned 555
  entries.
- UI ids: `UI_COMMANDS` in `crates/ui-egui/src/menus/ui_commands.rs`, 190 rows at both tags.
- MCP tools: `tool(` calls in `crates/mcp/src/tools.rs` (26, two of them on one line) and the
  dispatch names in the same file — unchanged set.
- Control: top-level match arms at eight-space indentation in `handle_request`
  (`crates/ui-egui/src/control.rs`), merged for the guarded duplicate; method strings extracted
  from the patterns; file byte-identical between tags.
- CLI: subcommands parsed from the `USAGE` const and confirmed with the installed `--help` and
  `--version` (11 + `--version`); `apps/designcraft-cli/src/main.rs` is unchanged between tags.
- Format: `VERSION: u32 = 4` (`crates/format/src/lib.rs`). Hyphenation: the `hyphen.rs` module doc
  and `Lang` table (10 languages), file unchanged between tags.
- Localization: `LANGUAGES` in `crates/ui-egui/src/i18n.rs` (15 non-English); percentages from
  `ROADMAP.md` and `docs/localization-parity.md` (maintainers' 2026-11-04 `i18n-report`, not
  re-run).
- The delta was derived from `git diff v0.18.0..HEAD` over `crates/{doc,engine,ui-egui,compose,
  geom,format,textimport,pdf,images}`, `apps/designcraft`, `packaging/linux/flatpak`, `docs/` and
  `ROADMAP.md`, reading code and command specs; release notes were not used as evidence.
- Installed bundle inspected read-only: `plutil -p` on `Contents/Info.plist`, the bundled CLI's
  `--version`/`--help`/`commands`/`describe`, and the desktop binary's `--version`
  (`designcraft 0.20.1`). The GUI was not launched.

## Unchanged

- **555 engine / 190 UI / 26 MCP tools / 11 CLI subcommands / format version 4 / 10 hyphenation
  languages**, all re-measured and explicitly unchanged at v0.20.1.
- The seven-section body, the document/window and coordinate model, the export formats and their
  parameters, placed-PDF layer options, shortcut import, the CLI flags and the sample recipes were
  path-verified and carried forward; only the delta or a re-measurement forced an edit.
- Older history folded out of `SKILL.md`:
  - **v0.16.0 → v0.17.0** (78 files): +1 engine id (`layout.parentPageSize`), none removed. Export
    wave: text-variable markers dropped from Text Only and RTF story export, hidden-group children
    skipped in EPUB/HTML, placed-SVG `font-family` matched against legacy family and full names, and
    XML-forbidden control characters stripped from math SVG (`crates/textimport/src/export.rs`).
    PDF/X-1a:2003 joined PDF/X-4 and PDF/A-2b as a real export standard.
  - **v0.15.2 → v0.17.0**: fix wave with no registry change (engine ids, 26 MCP tools, CLI
    subcommands and the control dispatch set all unchanged). Type menu separates CJK commands from
    Insert Math Expression; File ▸ Quit joins the in-window menu on Windows/Linux; spellcheck
    squiggles follow frame rotation; macOS Finder opens `.indd`/`.indt`; parent-page fixes; xref
    end-tag parsing skips quoted attributes; `file.importXml` keeps nested inline text; placed
    rasters that would decode past 1 GiB of RGBA are refused; EPUB/HTML character styles keep
    underline, strikethrough, caps and tracking; the toolbar's Alt/Option-click cycles the flyout
    group; the Rectangle dialog sizes in ruler units; cross-references keep edited text; Import
    warnings ▸ Show selects the frame a story warning is about.

## Known gap in this round

- Pin-and-verify refresh, not a new deep audit: no GUI launch, no builds, no project test-suite
  runs (only read-only installed-CLI `--version`/`--help`/`commands`/`describe` and a handful of
  headless command runs, including one synthetic `whiteOverprint` check). The Links worker and
  panel, anchored text frames through a real clipboard round-trip, and the Flatpak self-update were
  read from code and the project's tests, not exercised. IDML/INDD real-file fidelity, EPUB/PPTX
  rendering and print output remain unmeasured. Localization percentages are the maintainers'
  report. The control-method count is source-derived; no live control session was opened.
