# MailCraft — skill change log

## 2026-11-15b — CLI availability and install

Round v2.1.0: every ArtCraft skill must teach an agent to find the headless CLI and install it when
the launcher's app install did not include one. MailCraft is not installed on the authoring machine
and the Launcher does not install its unsigned macOS builds, so there is no bundle to inspect: the
skill now says the launcher's bundle holds only `MailCraft` and that this could not be verified
here, instead of claiming a bundle path. The CLI is a separate release asset,
`mailcraft-cli-0.13.0-macos-universal.zip` (20.1 MB, SHA-256 `8b78129c…`, from the release's
22-line `SHA256SUMS.txt`), so `## How to operate` gained the canonical *Getting the CLI* block
(PATH check → bundle check documented as unverifiable → download → checksum → unzip →
`install -m 0755` into `~/.local/bin` → `--version`), and the `cargo run --release -p mailcraft-cli`
route is now labelled a developer path instead of the first instruction. Nothing was downloaded or
run for MailCraft; only the release's `SHA256SUMS.txt` was fetched. The
`<settings>/control-key.local-<port>` agent model is unchanged. No pin, count, section heading or
audit-basis line changed.

## 2026-11-15 — re-pin to v0.13.0

Re-pinned: **v0.12.0 → v0.13.0**. The checkout is tag **`v0.13.0`**, commit
**`240d1d42fe394cf3274402b180663ba9b43ca180`** ("Merge pull request #1419 from
UCS-Care-Group/release/0.13.0"), inspected **2026-11-15**. The release this round supersedes is
**v0.12.0**, commit `92eb10c080d2da131bde71dd448bf37413a74d03`, which the previous skill was pinned
to. **MailCraft is still not installed on the authoring machine**: the ArtCraft Launcher opens an
existing MailCraft install but does not install its unsigned macOS builds, so there is still no
installed-bundle `--version` line and no live CLI run — every number below is derived from the
source at this tag, and the skill says so in its audit basis.

The delta was computed as a real tree diff against a shallow clone of the previous tag, not read
off the release notes: 405 files changed, 137 added, 8 removed between the two trees.

## Re-measured — what moved

- **Engine commands: 338 → 343.** Five ids added, none removed:
  `mail.snooze`, `mail.unsnooze`, `mail.returnDue` (`crates/engine/src/cmd/snooze.rs`),
  `mail.removeImportedDuplicates` (`crates/engine/src/cmd/imported_dupes.rs`) and
  `view.navigationBar` (`crates/engine/src/cmd/view.rs`). Method unchanged: literal
  `CommandSpec::new("…")` ids across `crates/` and `apps/`, minus the `test.*` fixtures (7 sites,
  6 ids, in `crates/engine/src/{tests,session_tests,focus_stays_tests,store_session_tests,store_undo_body_tests,store_history_memory_tests}.rs`).
- **Window commands: 85 → 89.** Four `ui.*` ids added, none removed: `ui.closeToTray`,
  `ui.darkStyle`, `ui.animations`, `ui.dismissSoftwareNotice` (`UI_COMMANDS`,
  `crates/ui-egui/src/lib.rs`).
- **Control-channel methods: 19 → 20.** `ui.minimize` is new (`crates/ui-egui/src/control.rs`);
  the other 19 names are the same, so the method is now 17 dispatched names, the `command` alias
  and `auth` / `auth.challenge`.
- **Feature-catalog coverage: 246/331 → 247/332 rows.** 17 of the 332 rows are out of scope
  (`OUT_OF_SCOPE`), so the shipped figure is **247 of 315 in scope (78.4%)**
  (`docs/parity-checklist.md`, `crates/engine/src/catalog.rs`).
- **Crates / apps: 23/3 → 28/4.** Five crates are new — `ber` (its bounded BER reader moved out of `crates/model`), `host`, `jmap-types`, `mime-model` (split out of `crates/mime`) and
  `mobile` — and one app is new: `apps/mailcraft-android`.
- **Mailbox file form: 3 → 4.** `crates/engine/src/store_index.rs` now writes `VERSION: u32 = 4`
  (`OLDEST = 3`), so a message's header lines nothing reads by name travel as content of their own
  and are packed into `headers-<n>.pack` files inside `<file>.blobs/`
  (`crates/engine/src/store_pack.rs`, `crates/model/src/headers.rs`). A v0.12.0 build refuses a
  form-4 mailbox, which is why the first open of this version keeps the old file beside it as
  `<file>.before-<version>` (`crates/engine/src/store_before.rs`).
- **Interface languages: 6 → 8** (English plus seven previews: French, German, Spanish, Italian,
  Dutch, **Romanian**, **Simplified Chinese**) and still a pseudo language — 9 `Lang` values, 7
  `.po` catalogues (`crates/i18n/src/lib.rs`, `crates/i18n/po/{ro,zh_CN}.po` new).
- **Search keywords: 20 → 22.** `label` and `labels` joined `KEYWORDS`
  (`crates/model/src/search.rs`), for Gmail labels (`crates/engine/src/gmail.rs`,
  `crates/model/src/gmail.rs`).
- **Fuzz targets: 26 → 27** (`fuzz/fuzz_targets/`). **Tests: 7,306 → 8,296** `#[test]`
  attributes across `crates/`, `apps/`, `xtask/`.
- **Control-key file naming changed.** It is now always `<settings>/control-key.local-<port>`
  (`crates/control-key/src/lib.rs` `key_path`), where it used to be `control-key.<instance>` with
  `local-<port>` only outside Flatpak. Inside Flatpak the name held the instance id, which differs
  for every `flatpak run`, so a bridge running as its own instance never found the app's key
  (#1199). The skill now states the path, the port scheme, the 0600 mode, the HMAC challenge and
  the settings folders exactly as that crate implements them.

## Unchanged at v0.13.0

- **MCP tools: 20** — the same 20 names and one argument change: `list_messages` gained an
  `account` filter and its `folder` now takes a kind (`crates/mcp/src/tools.rs`),
  protocol revision **`2025-06-18`** and 1 MiB line cap (`crates/mcp/src/server.rs`). The one
  behaviour change behind an unchanged signature: `folder` arguments (MCP `list_messages`, CLI
  `--folder`) now accept a folder *kind* — `inbox`, `sent`, `drafts`, `deleted`, `junk`, `archive`,
  `outbox` — in any mailbox language, not only an id or a path.
- **CLI: 14 subcommands and 18 long flags** (`apps/mailcraft-cli/src/main.rs`) — the same names and
  the same flags.
- **Shortcut specs: 57** `.key(...)` calls in `crates/engine/src/cmd/`. **Composing limit: 13**
  messages (`crates/engine/src/composing.rs`). **Windows: 12**
  (`crates/ui-egui/src/windows.rs`).
- Formats were re-verified and did not move: read `.eml`, `.mbox`, `.ics`, `.vcf`, a folder tree of
  mboxes and Outlook `.pst`; write `.mailcraft`, `.mbox`, `.eml`, `.ics`, `.vcf`; still no `.ost`,
  `.msg`, `.olm` and no `.pst` write (`crates/engine/src/io.rs`, `docs/gaps.md` gap 12).

## Corrected

- The previous skill said **the mailbox is form 3** with forms 1–2 read. At this tag the working
  mailbox is **form 4**; formats 1, 2 and 3 are still read and are rewritten as 4 on the first
  changed save. `docs/gaps.md` gap 8 still calls it "format 3", so the code wins.
- The previous skill described the control key as `control-key.<instance>`. That was true at
  v0.12.0 outside Flatpak and is wrong at v0.13.0: see above.
- The repository's own prose drifted further behind its code this round: `ROADMAP.md` prints
  "338 commands · 19 crates, 3 apps", "246 / 314 in scope (78.3%)" and "5,401 `#[test]`s", and the
  generated `docs/parity-checklist.md` prints "The registry holds 341 commands" — the code answers
  **343** engine commands, **28** crates, **4** apps, **247/315** and **8,296** tests.

## Carried forward

- Every capability the v0.12.0 skill verified whose code path is unchanged: the import/export
  matrix, `.pst` import, the agent gate and its classes, HTML mail without a script engine, the
  picture fetcher's rules, S/MIME and OpenPGP *checking* only (still nothing signs, encrypts or
  decrypts — `docs/gaps.md` gap 16), Gmail categories, rules, the calendar and meeting workflow,
  notes and journal without windows, and the browser build's JMAP-only reach.
- The three standing cautions: no printing (`docs/gaps.md` gap 15), no `.ost`/`.msg`/`.olm`, and
  one window with one Undo stack shared by the owner and an agent.

## Known gap in this round

- **No installed bundle, so no live evidence.** No `--version`, no `mailcraft-cli commands --json`,
  no `parity` run and no conversion was executed. `apps/mailcraft/src/main.rs` prints
  `mailcraft 0.13.0 (<build sha>)` and `apps/mailcraft-cli/src/main.rs` prints
  `mailcraft-cli 0.13.0`; both were read, neither was run.
- **The phone apps are code, not a release.** `apps/mailcraft-android` (a Gradle project) and
  `crates/mobile` (a UniFFI `Core` for Kotlin and Swift) exist at this tag, but the release
  artifact table lists only Windows, macOS, Linux, FreeBSD and the web, so the skill documents
  them as unreleased in-tree work, never as an installable app.
- **No GUI observation.** Tray behaviour, the navigation bar's foot placement, both dark themes,
  the new animations switch and the Romanian/Chinese catalogues are documented from code and
  `docs/`, not from a running window.

## Method

- `git -C <checkout> rev-parse HEAD` → `240d1d42fe394cf3274402b180663ba9b43ca180`;
  `git describe --tags` → `v0.13.0`. The pinned checkout is still a single-commit shallow clone.
- The previous tag is not in that clone, so **v0.12.0 was cloned read-only into a scratch folder
  inside this skill's own output directory** (`git clone --depth 1 --branch v0.12.0`), and the two
  trees were compared with `diff -rq` and per-file `diff`. The scratch clone was deleted after the
  counts and the delta paragraph were taken; nothing was written into the pinned checkout, which
  `git status --porcelain` showed clean at the end. Nothing was built, launched or committed.
- Every count was re-derived with the same `grep`/`awk`/`python3` extraction recorded in
  `evidence.md` §5, on both trees where a delta was claimed, so "added"/"removed" are set
  differences, not impressions.

## v0.12.0 → first audit (2026-11-12), previous round

- First audit: no MailCraft skill existed before it, so nothing was re-pinned and no installed
  binary line existed to compare. Pinned to tag `v0.12.0`, commit
  `92eb10c080d2da131bde71dd448bf37413a74d03`, inspected 2026-11-12.
- Numbers quoted then, all source-derived: 338 engine commands, 85 window commands, 246/331 catalog
  coverage, 20 MCP tools, 19 control methods, 14 CLI subcommands and 18 flags, 23 crates + 3 apps,
  mailbox form 3, 6 interface languages, 57 shortcut specs, 26 fuzz targets, 7,306 tests.
- Drift recorded then: `ROADMAP.md` printed 295 commands / 19 crates / 227–328 catalog / 5,401
  tests; `docs/parity-checklist.md` printed a 327-command registry; `docs/architecture.md` printed
  21 crates and a twelve-subcommand CLI.
