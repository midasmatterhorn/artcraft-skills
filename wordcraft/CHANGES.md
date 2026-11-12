# WordCraft — round 2026-11-12 changes

Re-pinned: v0.16.0 (`02a802c`) -> v0.18.1 (`079f478`, installed `wordcraft 0.18.1 (079f478b)`).

## Corrected / re-measured

- Engine commands 656 -> **671** live ids (+15). Additions: nine paragraph tools (`para.convertBreaks`, `para.blankBetween`, `para.separateParagraphs`, `para.removeBlank`, `para.trimLeadingSpaces`, `para.removeExtraSpaces`, `para.spacesToIndent`, `para.indentToSpaces`, `para.removeLineBreaks`), `text.deleteSentenceBack`, `view.paperColor`, `view.arrangeAll`, `view.sideBySide`, `view.syncScroll`, and `file.strictReport`. No ids were removed. Raw `CommandSpec::new` sites: 673 at this tag, 658 at v0.16.0; two are test fixtures in `crates/engine/src/tests.rs` at both tags.
- Catalog coverage 506/521 -> **509/521 (97.7%)**. Three catalog rows became live — `view.arrangeAll`, `view.sideBySide`, `view.syncScroll` — and no row was added or removed. The generated `docs/parity-checklist.md` still prints 508/520, one row and one live id behind the code (recorded as drift).
- Control-channel methods stayed **22**; the set is unchanged at v0.18.1. Behaviour changed around it: a request still queued after 60 s is now cancelled and can never run, one that had started reports an unknown outcome, unauthenticated connections are capped at 64, and `ui.inspect` gained a `windows` field (`apps/wordcraft/src/control_server.rs`, `crates/ui-egui/src/control/handler.rs`).
- MCP tools 17 -> **18**: `insert_table` inserts a filled table in one call (backed by `insert.spreadsheet`; 1–1000 rows, 1–63 cells a row, optional `header` and `style`) (`crates/mcp/src/tools.rs`, `crates/engine/src/cmd/tools/actions.rs`). The bridged backend also changed: a mutation whose delivery or reply is unknown is **never retried** and returns `outcome unknown`; only `document.inspect`, `engine.commands`, `ui.inspect`, `ui.parity` and path-less `ui.render`/`ui.screenshot` retry (`crates/mcp/src/backend.rs`).
- CLI flags 21 -> **22** (plus `-h/--help`, `--version`): `--strict` on `convert` and `render` refuses to write a PDF or PNG that would drop a character or picture, exits 3, and prints the report on stderr (`apps/wordcraft-cli/src/main.rs`, `apps/wordcraft-cli/tests/it/strict.rs`). Subcommands are **10**, unchanged.
- Open / save extensions **23 / 16**, unchanged; `crates/engine/src/io.rs` changed only to carry the `strict` export flag and to open packages through the regular-file guard.
- Dialog names 91 -> **92** (+`dateTime`, the Date and Time dialog, `crates/ui-egui/src/dialogs/dialogs_insert/date_time.rs`). Shortcut `.key()` sites 166 -> **167** (one new binding, `text.deleteSentenceBack` = `Mod+Shift+Backspace`; three of the sites are diff-helper calls in `crates/engine/src/cmd/tools/compare.rs`, so the binding count is 164).
- Interface languages **28** and built-in proofing languages **16** are unchanged; `craft-i18n.rev` did not move this round (`1e515422…` at both tags).
- Personal templates: `file.newFromTemplate` now takes `data` (base64 bytes for a non-Unicode path), `password` (a protected template) and `replaceBlank`; a template opened from the file manager (macOS "Open with", Explorer's New) starts a new document and is never written over (#3433) (`crates/engine/src/cmd/tools/specs.rs`, `crates/engine/src/cmd/file.rs`, `crates/ui-egui/src/documents.rs`).
- Format fidelity estimates refreshed from the repo's own table: HTML ~60% -> **~65%**, RTF stays **~50%** but now reads and writes footnotes, endnotes and comments (#1053) (`crates/formats/src/rtf/{reader,export}.rs`, `docs/file-format-parity.md`).
- The "catalog features with no command" list drops the three window commands: 15 rows / 14 distinct features -> **12 rows / 11 distinct** (`insert.inkEquation` is still listed twice).
- Web build: the page API `window.wordcraft` (`request`, `execute`, `commands`, `docInspect`, `uiInspect`, `screenshot` as promises) drives the same control requests from a page; no TCP control channel in the browser (`apps/wordcraft-web/src/api.rs`).
- New verification surface replaces hand-waving about silent export loss: `file.strictReport` returns the schema-1 report of missing glyphs and pictures, and `file.save`/`file.saveAs`/`file.exportPdf`/`file.exportPng` take `strict` (`crates/engine/src/strict.rs`, `crates/engine/src/cmd/file.rs`).

## Method

- `git rev-parse HEAD` = `079f478bd85df7bcc567e3bafa7d7219096f9c3c`, tag `v0.18.1`; `git diff --shortstat v0.16.0..HEAD` = **358 files, +23,251 / −1,410**. The shallow checkout carries only the `v0.16.0` and `v0.18.1` tag objects, so the delta is the cumulative diff across the two intermediate releases, not a per-release diff.
- Command ids: `grep -rhoE 'CommandSpec::new\(\s*"[^"]+"' crates/ apps/ | sort -u`, minus the two `test.*` fixtures in `crates/engine/src/tests.rs`; the set was diffed against the same extraction run on the `v0.16.0` tree with `git grep`.
- Catalog: the `CATALOG` pipe table in `crates/engine/src/catalog.rs` (521 rows) checked id by id against the command-id set; missing rows counted, not estimated.
- MCP tools: `tool(` entries in `crates/mcp/src/tools.rs`; control methods: distinct `"<ns>.<name>"` strings in `crates/ui-egui/src/control/handler.rs`; CLI subcommands: `SUBCOMMANDS` in `apps/wordcraft-cli/src/main.rs`, flags from the `OptionSpec` tables plus `apps/wordcraft-cli/src/automation_args.rs`; dialogs: unique `=> "…"` arms of the five `Dialog::name` methods; shortcuts: `.key(` sites in `crates/engine/src/cmd/`; languages/proofing: array lengths.
- The installed bundle's binary was run read-only for `--version` and `--help` (`wordcraft 0.18.1 (079f478b)`); the GUI was never launched. `wordcraft-cli` is not in the bundle and no CLI artifact was on the machine, so every count is code-derived.
- Every repo-relative path cited in the previous `SKILL.md` was re-resolved in this checkout; all resolved (no moved or deleted citations this round).

## Unchanged

- MCP protocol revision `2025-06-18`, resources `wordcraft://document` and `wordcraft://commands`, and the 22 control methods (names and params).
- CLI subcommands **10**, script caps (4 MiB, 100,000 commands, 64 outputs), control-key scheme (`<settings>/control-key.<instance>`, mode 0600, removed on exit), 1 MiB request line, 30 s first-request window.
- Open / save extension sets **23 / 16**; `.doc` still read-only, MHT still opens but cannot be saved, no VBA execution, no SVG/ICO/HEIC pictures.
- Interface languages **28**, built-in proofing **16**, `craft-i18n.rev` pinned at the same commit.
- Zotero commands and flags, recovery cadence (10 s, per document, desktop only), printing options (`pagesPerSheet`, `paper`), automation read/write roots applying to the headless server only.
- Older history (v0.13.2 -> v0.14.0 and earlier) leaves `SKILL.md`; the two most recent historical delta paragraphs (v0.15.1 -> v0.16.0 and v0.14.0 -> v0.15.1) are kept there, and the earlier rounds' own CHANGES files hold their records.

## Known gap in this round

- No `wordcraft-cli` on the authoring machine and none in the bundle, so `commands --json`, `parity --markdown`, `convert --strict` and a real conversion could not be executed; the strict-export behaviour is read from `crates/engine/src/strict.rs`, `apps/wordcraft-cli/src/main.rs` and the README example, not observed.
- GUI-only changes (window tiling and Side by Side, paper colours, the Date and Time dialog, the text-hinting work) were not launched or seen; they are cited to code and docs only.
- The checkout's history is squashed to one commit per tag, so per-release (v0.17.0, v0.18.0) attribution of individual changes is not available; the delta is stated as cumulative.
- `docs/gaps.md` gap 7 still says 61 modal dialogs, gap 24 says 140/158 shortcuts, `docs/parity-checklist.md` prints 508/520, `README.md` says 422 commands and `ROADMAP.md` says 433 commands / 493-508 — all stale against the code values re-measured here.
