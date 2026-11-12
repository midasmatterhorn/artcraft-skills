# MailCraft — evidence ledger (tag v0.12.0, first audit)

Audit basis: this checkout is tag **`v0.12.0`**, commit
**`92eb10c080d2da131bde71dd448bf37413a74d03`** ("Merge pull request #1127 from
UCS-Care-Group/release/0.12.0", 2026-11-12T02:46:48+01:00), verified with `git rev-parse HEAD` and
`git tag --points-at HEAD`. Inspection date **2026-11-12**. The clone is shallow with a single
commit and a single tag, so no earlier release was available to diff. **MailCraft is not installed
on this machine** (no bundle in the applications folder; the ArtCraft Launcher opens an existing
install but does not install the unsigned macOS build), so there is no installed-binary `--version`
line and no live CLI run: every count below is derived from this tag's source. The macOS bundle
identifier in the packaging template is `io.github.billsecond.mailcraft`, minimum macOS 11.0
(`packaging/macos/Info.plist.in`).

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 338 live engine command ids; 344 raw `CommandSpec::new("…")` sites incl. 6 `test.*` fixtures | `grep -rhoE 'CommandSpec::new\(\s*"[^"]+"' crates/ apps/ \| sort -u` = 344; `test.*` ids = 6 (`crates/engine/src/{tests,session_tests,focus_stays_tests,store_session_tests,store_undo_body_tests}.rs`) | implemented |
| 2 | 85 window command ids (`ui.*`), dispatchable by id like engine commands | `crates/ui-egui/src/lib.rs` `UI_COMMANDS` (lines 1107–1508); dispatch fall-through in `crates/ui-egui/src/control.rs` | implemented |
| 3 | Feature catalog 246 / 331 (74.3%) | `crates/engine/src/catalog.rs` `CATALOG` + `parity()`; recomputed by matching each row's id against the engine id set; `docs/parity-checklist.md` prints the same 246/331 | implemented metric |
| 4 | 20 MCP tools, protocol `2025-06-18`, 1 MiB line cap | `crates/mcp/src/tools.rs` `tool_definitions()`; `crates/mcp/src/server.rs` `PROTOCOL_VERSION`, `MAX_LINE` | implemented |
| 5 | 19 control-channel method names; per-window key file; key proof before the bridge sends it | `crates/ui-egui/src/control.rs` `dispatch`; `apps/mailcraft/src/control_server.rs` (`auth`, `auth.challenge`); `crates/control-key/src/lib.rs`; `docs/control-protocol.md` | implemented |
| 6 | 14 CLI subcommands, 18 long flags (+`--help`, `--version`) | `apps/mailcraft-cli/src/main.rs` `USAGE`, `run()` match arms, `value("--…")`/`flag("--…")` lists | implemented |
| 7 | Import `.eml`, `.mbox`, `.ics`, `.vcf`; export `.mailcraft`, `.mbox`, `.eml`, `.ics`, `.vcf` | `crates/engine/src/io.rs` `Format::from_extension`; `crates/engine/src/cmd/file.rs` (`file.import`, `file.exportMessage`, `file.exportFolder`, `file.exportCalendar`, `file.exportContacts`); `apps/mailcraft-cli/src/main.rs` `export_command` | implemented |
| 8 | `.pst` import of mail, contacts, calendar, tasks, notes and journal, with a report; no `.pst` write | `crates/engine/src/cmd/file.rs` `file.importPst` params; `crates/engine/src/import_pst/{item,contact,calendar,report}.rs`; `crates/pst/src/`; `docs/gaps.md` gap 12 | implemented (read only) |
| 9 | Mailbox form 3: log of records + `<file>.blobs` content folder; forms 1 and 2 read | `crates/engine/src/store.rs` module docs (layout, save, open); `crates/engine/src/store_index.rs` (`VERSION = 3`, record kinds) | implemented |
| 10 | Accounts: local, IMAP+SMTP, Microsoft (Graph, OAuth), JMAP, Exchange Web Services; unknown kinds preserved | `crates/model/src/mailbox.rs` `AccountKind`; `crates/engine/src/cmd/account.rs` (`account.add` param doc, kinds) | implemented |
| 11 | S/MIME and OpenPGP signatures are *checked* in the reading pane and exposed read-only to agents; keys can be listed/imported/removed | `crates/smime/src/{verify,chain,cert,import}.rs`; `crates/openpgp/src/{check,mime,keys}.rs`; `crates/engine/src/cmd/mail.rs` `mail.digitalSignature`; `crates/engine/src/cmd/keys.rs` | implemented (verification only) |
| 12 | Nothing signs, encrypts or decrypts a message yet | `docs/gaps.md` gap 16 ("nothing signs with them yet"); no signing path in `crates/smime/src` or `crates/openpgp/src` | not implemented (verified absent) |
| 13 | Gmail categories (Primary/Social/Promotions/Updates/Forums) as folders, tabs, alerts and `gmail:` search | `crates/engine/src/gmail.rs`; `crates/model/src/gmail.rs`; `crates/ui-egui/src/gmail_tabs.rs`; `crates/model/src/search.rs` (`gmail` keyword) | implemented |
| 14 | Agent gate: every command classified `safe`/`owner`/`never`; `--allow send,delete,accounts,mailbox,settings,input`; no file paths from agents | `crates/engine/src/agent.rs` (`Class`, `access`, `check`, `file_param`); `crates/mcp/src/tools.rs` `exec`; `docs/mcp.md` | implemented |
| 15 | Attachment previews (PDF via PdfCraft, images via PhotoCraft) off by default, never for agents | `crates/ui-egui/src/attachment_preview.rs` (`Format`, `MAX_INPUT_BYTES` 16 MiB, `MAX_PAGES` 10,000, `MAX_SIDE` 3,072); `apps/mailcraft/src/attachment_render.rs` (`MAILCRAFT_PDFCRAFT_CLI`, `MAILCRAFT_PHOTOCRAFT_CLI`); `ui.previewAttachment` in `crates/ui-egui/src/lib.rs` | implemented |
| 16 | HTML mail is laid out without running anything; remote pictures only on the owner's say-so, through a fetcher that sends only the address | `crates/html/src/`; `crates/net/src/pictures.rs` `fetch`; `apps/mailcraft/src/picture_cache.rs`; `docs/gaps.md` gap 6 | implemented |
| 17 | Report a Problem: GitHub form by default, relay send only by the owner's own click | `crates/ui-egui/src/report_problem.rs`; `ui.reportProblem` param doc in `crates/ui-egui/src/lib.rs` | implemented |
| 18 | Automatic bulleted/numbered lists on `* `, `- `, `1. `, `1) ` with their own undo step, switchable in Options | `crates/engine/src/cmd/format.rs` (`format.type` `autoList`, `s.auto_lists`); `crates/model/src/rich/body.rs` `auto_list`; `crates/ui-egui/src/compose/editor.rs` | implemented |
| 19 | Pictures written into a message are carried in replies and forwards | `crates/engine/src/cmd/compose.rs` (`PICTURE_CID`, quoted pictures copied as parts) | implemented |
| 20 | Headless UI screenshots render the window offscreen | `crates/ui-egui/examples/ui_shot.rs` (documented script lines, fixed clock) | implemented |
| 21 | Six interface languages (five previews) + pseudo | `crates/i18n/src/lib.rs` `Lang::ALL: [Lang; 7]`; `crates/i18n/po/{de,es,fr,it,nl}.po` | implemented |
| 22 | No printing anywhere | `docs/gaps.md` gap 15; no print command among the 338 ids | not implemented (verified absent) |
| 23 | No `.ost`, `.msg` or `.olm`; no POP; JMAP read-only and browser-only | `docs/gaps.md` gaps 12, 5 and the POP row; `crates/model/src/mailbox.rs` `AccountKind` | not implemented (verified absent) |
| 24 | Web build is CI-checked; no control channel and no sockets there | `apps/mailcraft-web/`; `docs/control-protocol.md` ("The browser build has no control channel"); `crates/net` empty on wasm (`docs/architecture.md`) | implemented (not exercised) |

## 2. Count methods and values (v0.12.0)

| Surface | Method | Value |
|---|---|---:|
| Engine commands | `CommandSpec::new("…")` literal ids in `crates/engine/src/cmd/**`, minus `test.*` fixtures | **338** |
| Raw command sites | same grep across `crates/` and `apps/` (includes 6 test fixtures) | 344 |
| Window commands | `"ui.…"` literals inside `UI_COMMANDS` (`crates/ui-egui/src/lib.rs:1107-1508`) | **85** |
| Catalog rows / covered | `CATALOG` rows of four fields; covered = id in the engine id set | **331 / 246 (74.3%)** |
| MCP tools | `tool(` entries in `crates/mcp/src/tools.rs` | **20** |
| Control methods | `match req.method` arms in `crates/ui-egui/src/control.rs` + `command` alias + `auth`, `auth.challenge` | **19** |
| CLI subcommands | `match cmd` arms in `apps/mailcraft-cli/src/main.rs` | **14** |
| CLI long flags | distinct `"--…"` option strings in `main.rs`, minus `--help`/`--version` | **18** |
| Crates / apps | directories under `crates/` / `apps/` | **23 / 3** |
| Shortcut specs | `.key(` in `crates/engine/src/cmd/` | **57** |
| Interface languages | `Lang` variants (6 named + pseudo) / `.po` catalogues | **7 / 5** |
| Fuzz targets | files in `fuzz/fuzz_targets/` | **26** |
| Tests | `#[test]` attributes in `crates/`, `apps/`, `xtask/` | **7,306** |
| Search keywords | entries in `model::search::KEYWORDS` | 20 |

## 3. Uncertain / not verified

- **No installed build.** No `--version`, no `mailcraft-cli commands --json`, no `parity` run, no
  conversion. `apps/mailcraft/src/main.rs` prints `mailcraft 0.12.0 (<build sha>)`, and
  `apps/mailcraft-cli/src/main.rs` prints `mailcraft-cli 0.12.0`, but neither was executed here.
- **No diff.** One commit, one tag: the release-wave features (S/MIME, OpenPGP, Gmail categories,
  `.pst` notes/journal, report relay, attachment previews, account colours, automatic lists,
  pictures in replies) are verified as present code paths, not as a change against an earlier
  release.
- **GUI behaviour** (ribbon modes, reading-pane layout, Gmail tabs, preview rendering, colours) is
  read from code and `docs/`, never observed.
- **Interoperability** is the repo's own weakest area (`docs/gaps.md` gap 1: one Microsoft 365
  mailbox in daily use, other providers and platforms still need acceptance); this audit did not
  contact any server.
- **"Shared calendars" is ambiguous in the repo.** `docs/gaps.md` gap 5 and
  `docs/calendar-parity.md` ("Later") still list shared calendars as missing, while
  `calendar.openShared` / `calendar.removeShared` / `ui.allowSharedCalendars` and shared mailboxes'
  calendars exist in code (`crates/engine/src/cmd/calendar_opened.rs`,
  `crates/engine/src/cmd/shared.rs`, `crates/ui-egui/src/shared_calendars.rs`). The two may mean
  different things (Outlook's Shared Calendars group versus a shared mailbox's calendar or a
  calendar opened by address); `SKILL.md` claims only what the commands do.
- Readiness percentages (~25% real work, ~55% local viewer) are the repo's own estimates, not
  measurements.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `ROADMAP.md` headline (2026-10-31): "227 / 328 (69.2%)" catalog coverage | 246 / 331 (74.3%) |
| `ROADMAP.md`: "295 commands · 19 crates" | 338 engine commands (+85 window commands) · 23 crates |
| `ROADMAP.md`: "5,401 `#[test]`s" | 7,306 `#[test]` attributes |
| `docs/parity-checklist.md`: "The registry holds 327 commands" | 338 |
| `docs/architecture.md`: "21 crates" | 23 (its own revision log reaches 21 with `openpgp`/`assuan`; `smime` landed after) |
| `docs/architecture.md` CLI row lists `info, folders, list, show, import, export, convert, run, sync, commands, parity, mcp` | 14 subcommands — `import-pst` and `detect` are missing from the list |
| `docs/gaps.md` gap 16 heading: "No signing or encryption" | Accurate for signing/encryption, but S/MIME and OpenPGP signatures *are* checked in this build — the heading is broader than the body |

## 5. Verification commands (read-only)

```sh
git -C <checkout> rev-parse HEAD                                  # 92eb10c080d2da131bde71dd448bf37413a74d03
git -C <checkout> tag --points-at HEAD                             # v0.12.0
git -C <checkout> rev-list --count HEAD                            # 1 (shallow, no diff base)
grep -rhoE 'CommandSpec::new\(\s*"[^"]+"' crates/ apps/ | sort -u | wc -l   # 344 sites
grep -rhoE 'CommandSpec::new\(\s*"[^"]+"' crates/ apps/ | sed -E 's/.*"([^"]+)"/\1/' | grep -c '^test\.'  # 6
awk 'NR>=1107 && NR<=1508' crates/ui-egui/src/lib.rs | grep -oE '"ui\.[a-zA-Z]+"' | sort -u | wc -l  # 85
awk -F'|' 'NF==4 && $4 ~ /^[a-z]/' crates/engine/src/catalog.rs | wc -l    # 331 rows
grep -cE '^\s+tool\(' crates/mcp/src/tools.rs                      # 20
grep -nE '^\s+"[a-z-]+" =>' apps/mailcraft-cli/src/main.rs         # 14 subcommands
grep -rhoE '\.key\(' crates/engine/src/cmd/ | wc -l                # 57
grep -rn 'pub const MAX_COMPOSING' crates/engine/src/composing.rs  # 13
grep -rn 'pub const MAX_WINDOWS' crates/ui-egui/src/windows.rs      # 12
grep -rhoE '#\[test\]' crates apps xtask | wc -l                   # 7306
ls fuzz/fuzz_targets | wc -l                                       # 26
grep -n 'PROTOCOL_VERSION\|MAX_LINE' crates/mcp/src/server.rs       # 2025-06-18, 1 MiB
grep -n 'VERSION: u32' crates/engine/src/store_index.rs            # 3
```

## 6. What was re-measured vs carried forward

- **First audit: nothing carried forward.** Every claim in `SKILL.md` was written from this tag's
  code; the baseline skill directory was empty.
- Re-measured once, from code: commands (338 + 85), catalog (246/331), MCP tools (20), control
  methods (19), CLI (14 subcommands, 18 flags), crates (23), shortcuts (57), languages (6 + pseudo),
  fuzz targets (26), tests (7,306), mailbox format (3), format extensions.
- Cross-checked against the repo's own documents: catalog ratio and interface languages agree; the
  command count, crate count, test count, registry size and CLI list in the docs are stale (see §4).
