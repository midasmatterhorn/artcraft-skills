# MailCraft — round 2026-11-12 changes

Re-pinned: **first audit** — no MailCraft skill existed before this round (the baseline directory was
empty), so nothing is re-pinned and no installed-binary line exists to compare. The skill is pinned to
tag **v0.12.0**, commit **`92eb10c080d2da131bde71dd448bf37413a74d03`**, inspected **2026-11-12**.
**MailCraft is not installed on the authoring machine** (the ArtCraft Launcher opens an existing
MailCraft install but does not install its unsigned macOS builds), so there is no `--version` string
from a bundle: every number below is derived from the source at this tag.

## Corrected / re-measured

There was no earlier text to correct, so this section records the numbers the new skill quotes and
where the repository's own prose disagrees with its code.

- **Engine commands: 338** live ids. Method: `CommandSpec::new("…")` literal-id sites in
  `crates/engine/src/cmd/**` (338) — the 344 raw sites in the tree include six `test.*` fixtures in
  `crates/engine/src/{tests,session_tests,focus_stays_tests,store_session_tests,store_undo_body_tests}.rs`.
  Drift: `ROADMAP.md` headline (2026-10-31) prints "295 commands"; `docs/parity-checklist.md` prints
  "The registry holds 327 commands".
- **Window commands: 85** `ui.*` ids in `UI_COMMANDS` (`crates/ui-egui/src/lib.rs`), dispatchable
  through `engine.execute` like engine ids. No repo document counts them.
- **Catalog coverage: 246 of 331 (74.3%)** — independently re-derived by matching each
  `crates/engine/src/catalog.rs` row's command id against the engine id set; it matches the committed
  `docs/parity-checklist.md` ratio, while `ROADMAP.md` still prints 227/328 (69.2%). The registry-size
  line in the same checklist (327) is stale by eleven.
- **MCP tools: 20** (`crates/mcp/src/tools.rs`), protocol revision `2025-06-18`
  (`crates/mcp/src/server.rs`), 1 MiB line cap. Measured at this tag; there is no earlier count.
- **Control channel: 19 method names** — 16 dispatched in `crates/ui-egui/src/control.rs`
  (`engine.execute`, `engine.commands`, `mailbox.inspect`, `ui.inspect`, `app.status`, `ui.parity`,
  `ui.alerts`, `ui.click`, `ui.move`, `ui.drag`, `ui.key`, `ui.text`, `ui.screenshot`, `ui.resize`,
  `ui.focus`, `app.quit`), the `command` alias for `engine.execute`, and `auth` / `auth.challenge`
  handled in `apps/mailcraft/src/control_server.rs`; any other name is taken as a command id.
- **CLI: 14 subcommands, 18 long flags** (`apps/mailcraft-cli/src/main.rs`). Drift:
  `docs/architecture.md` lists twelve subcommands — it omits `import-pst` and `detect`.
- **Crates: 23** plus 3 apps and `xtask`. Drift: `docs/architecture.md` says 21, `ROADMAP.md` says 19.
- **Formats.** Read: `.eml`, `.mbox`, `.ics`, `.vcf` (`crates/engine/src/io.rs`), a folder tree of
  mbox files (`file.importFolderTree`), and Outlook `.pst` (`file.importPst`, `crates/engine/src/import_pst/`).
  Written: `.mailcraft`, `.mbox`, `.eml`, `.ics`, `.vcf`. No `.ost`, `.msg`, `.olm`, `.pst` write
  (`docs/gaps.md` gap 12).
- **Mailbox form: 3** — a log of records plus a `<file>.blobs` content folder; formats 1 (one JSON
  file) and 2 (JSON + content folder) are still read and rewritten as 3 on the first changed save
  (`crates/engine/src/store.rs`, `crates/engine/src/store_index.rs`).
- **Interface languages: 6** (English, plus French, German, Spanish, Italian and Dutch previews) and
  a pseudo language: 7 `Lang` values, 5 `.po` catalogues (`crates/i18n/src/lib.rs`,
  `crates/i18n/po/`). `docs/gaps.md` gap 14 agrees.
- **Shortcut specs: 57** `.key(...)` calls in the engine registry. **Tests: 7,306** `#[test]`
  attributes across `crates/`, `apps/`, `xtask/` (`ROADMAP.md` still prints 5,401). **Fuzz targets:
  26** (`fuzz/fuzz_targets/`).

## Method

- `git rev-parse HEAD` in the pinned checkout returned `92eb10c080d2da131bde71dd448bf37413a74d03`,
  and `git tag --points-at HEAD` returned `v0.12.0`. The checkout is a **single-commit shallow clone**
  (`git rev-list --count HEAD` = 1, one tag), so no diff against an earlier release could be computed
  and the delta paragraph in `SKILL.md` is a set of code landmarks at this tag, not a diff.
- Every count was extracted with `grep`/`awk` over the source (the exact commands are in
  `evidence.md` §5), then cross-checked against the repo's generated or hand-written docs; where they
  disagree the code wins and the drift is recorded above and in `evidence.md` §4.
- Catalog coverage was recomputed in a small script that parses the `CATALOG` string, keeps rows of
  four fields, and tests each id against the engine id set — the same rule `catalog::parity` uses.
- Nothing was built, launched, committed or written into the checkout. No GUI was started (there is
  no install to start). No test ran.

## Unchanged

- Nothing is carried forward: this is the skill's first audit, so there is no earlier skill text,
  count or citation to confirm as unchanged.
- Within the tag, the surfaces the repository's own documents and the code agree on are the catalog
  ratio (246/331), the six interface languages, the mailbox format numbers (1, 2, 3) and the MCP
  protocol revision — each measured once here and quoted with its method.

## Known gap in this round

- **No installed bundle.** The strongest live evidence an ArtCraft skill usually has — the app
  binary's `--version`, and a read-only `mailcraft-cli commands --json` / `parity` run — was not
  available, because MailCraft is not installed on this machine and no release artifact was on it.
  All counts are code-derived; the CLI usage text and command specs were read, never executed.
- **No diff.** The single-commit checkout holds no earlier tag, so the v0.12.0 release-wave features
  (S/MIME and OpenPGP checking, Gmail categories, `.pst` calendar/tasks/notes/journal, Report a
  Problem's relay, attachment previews, account colours, automatic lists, pictures in replies) are
  verified as code paths with file citations, not by exercising them or by reading a diff.
- **No GUI observation.** Window behaviour (ribbon modes, reading-pane layout, Gmail category tabs,
  attachment preview rendering) is documented from code and `docs/`, not from a running window.
- The release notes in the round's context file were used only to know which surfaces to look for;
  no claim in `SKILL.md` rests on them.
