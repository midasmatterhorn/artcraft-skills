# DesignCraft — round 2026-11-07 changes

Re-pinned: v0.17.0 (`e79d682`) -> v0.18.0 (`58ac6d2`, installed `designcraft 0.18.0`; the bundled
`designcraft-cli` prints `designcraft-cli 0.18.0`). Clone HEAD verified at
`58ac6d29b260e033f4291afc4318b507cfd90fd9`; `Info.plist` `DesignCraftBuildCommit` matches.

## Corrected / re-measured

- **Control methods: 27 distinct dispatch arms at both tags** (`crates/ui-egui/src/control.rs`),
  set unchanged. The earlier prose said "26 + `ui.docking`"; the arm set is 27 at v0.17.0 as well,
  so the absolute figure is restated and the "did not move" claim is what matters.
- **Engine registry: 555 ids** at v0.18.0 (v0.17.0 = 547; +8, nothing removed):
  `file.exportBatch`, `file.exportPresets`, `file.saveExportPreset`, `file.deleteExportPreset`,
  `layout.alternate.duplicate` / `.delete` / `.options`, `layout.parents.duplicate`. The published
  skill said 542; the same extraction at v0.17.0 gives 547, so that figure was already stale at its
  own tag and is replaced, not carried.
- **UI command rows: 190** (v0.17.0 = 187; +3: `app.exportBatch`, `app.parentOptions`,
  `app.alternateLayoutOptions`). The published count of 176 did not reproduce at its own tag (187
  rows there); the row count of `UI_COMMANDS` is the reproducible number.
- **CLI subcommands: 11**, not 10 — `thumbnail FILE.designcraft OUT.png [SIZE]` is new. `validate-pdf`
  gained `--standard x4|x1a` (defaults to the file's own `GTS_PDFXVersion`) and now reports
  `warnings` separately from `issues`; its report is `{path, standard, valid, issues, warnings}`,
  not `{valid, issues}`. `perf` takes `--pages/--runs/--strict` only (the module doc in
  `apps/designcraft-cli/src/main.rs` still lists `--frames/--chars/--images`; the `USAGE` const and
  the parser are authoritative).
- **The macOS CLI now ships inside the app bundle** at
  `DesignCraft.app/Contents/MacOS/designcraft-cli` (`docs/mcp.md` §Where the CLI is; `ROADMAP.md`
  changelog "CLI bundled with the macOS app"). Three sentences that said the `.app` holds only the
  desktop app were wrong at this tag; the CLI ZIP is now an alternative, not the only route.
- **Hyphenation languages corrected** to English, Danish, Dutch, French, German (2006 reform), Greek,
  Italian, Norwegian, Portuguese, Spanish (`crates/compose/src/hyphen.rs` module doc and `Lang`
  table). The old "English, Spanish, Portuguese, Norwegian and Greek only" list was already stale at
  v0.17.0; Danish is new this release. **Esperanto** is a text language (`eo`, quotes/locale) but is
  not hyphenated (`docs/localization-parity.md`, #1201).
- **Native-format read limits**: a *stored* asset (placed images are stored) no longer counts
  against the 1 GiB asset cap / 4 GiB deflate budget; it is read at its size in the archive and
  charged to the archive's own size, so a saved document opens at any placed-image size (#2166,
  `crates/format/src/lib.rs` `Limits`). Version stays 4; JSON is still capped at 256 MiB and the
  archive at 100 000 entries.
- Stale "new this release" markers from the v0.17.0 round were de-dated (`note.split`, Story Editor
  depth ruler, separations preview, shortcut sets, PDF/X-1a "new this release").
- Verification-protocol step 4 quoted "0.15.2, commit `7e70203…`"; replaced with this pin
  (0.18.0, `58ac6d2…`).

## Method

- `git rev-parse HEAD` = `58ac6d29b260e033f4291afc4318b507cfd90fd9`, tag `v0.18.0`;
  `git diff --shortstat v0.17.0..HEAD` = 214 files, +10830 / -1032.
- Engine ids: regex for `cmd!(` with an optional `query`/`noundo` modifier over every `.rs` file of
  `crates/engine/src` at each tag via `git show`; unique sets diffed. Live cross-check: the installed
  `designcraft-cli 0.18.0 commands` returned 555 entries (fresh `--version`, `--help`, `commands`).
- UI ids: `UI_COMMANDS` rows in `crates/ui-egui/src/menus/ui_commands.rs`, diffed between tags.
- MCP tools: `tool("…")` names in `crates/mcp/src/tools.rs` — 26 at both tags. Control methods: arm
  strings in `crates/ui-egui/src/control.rs` — the same 27 at both tags.
- `crates/format/src/lib.rs` `VERSION: u32 = 4`; `plutil -p` on the installed `Info.plist`
  (`CFBundleShortVersionString 0.18.0`, `CFBundleIdentifier ai.storyteller.designcraft`).
- Every repo-relative path cited in `SKILL.md` and `references/agent-surfaces.md` was expanded and
  tested against the clone; all resolve at this tag (the `crates/pdf/src/{lib,pdfx,pdfx/fonts,…}.rs`
  brace form now points at files that exist).
- The delta paragraph was derived from `git diff v0.17.0..HEAD` over the changed areas the context
  file lists (`crates/engine`, `ui-egui`, `mcp`, `format`, `idml`, `compose`, `doc`, `fonts`,
  `apps/designcraft-cli`), reading the code and command specs, not the release notes. Docs were read
  only to find claims to check; where docs and code disagreed, the code is recorded.

## Unchanged

- **26 MCP tools** and **27 control methods**: set diff empty in both directions at v0.18.0. The MCP
  *behaviour* moved (closed schemas, four hints, nested-key errors) but no tool was added or removed.
- **Format version 4**, and the `.designcraft` zip layout (`mimetype`, `document.json`, `assets/`,
  `meta.json`, optional `preview.png`): unchanged.
- The seven-section body, the limitations, the recipes, the document/window and coordinate model,
  the script syntax and the shortcut-import boundaries were path-verified and carried forward; the
  only edits are the ones the delta or a re-measurement forced. Older v0.15.0–0.15.2 history was
  folded out of `SKILL.md` (two most recent historical deltas kept) and lives here.

## Known gap in this round

- Pin-and-verify refresh, not a new deep audit: IDML/INDD real-file fidelity, EPUB/PPTX rendering
  and the GUI were not exercised (no GUI launch, no builds). The new **Export Layouts and Versions**
  command is documented from its command spec and implementation; it was not run on a document.
  Counts for UI rows and command ids are source-derived and cross-checked against the installed CLI
  where the CLI exposes them.
