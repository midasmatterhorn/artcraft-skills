# MailCraft — evidence ledger (tag v0.13.0, second audit)

Audit basis: this checkout is tag **`v0.13.0`**, commit
**`240d1d42fe394cf3274402b180663ba9b43ca180`** ("Merge pull request #1419 from
UCS-Care-Group/release/0.13.0"), verified with `git rev-parse HEAD` and `git describe --tags`.
Inspection date **2026-11-15**. The pinned clone is shallow with a single commit and a single tag;
the previous pin, **v0.12.0** at `92eb10c080d2da131bde71dd448bf37413a74d03`, was cloned read-only
into a scratch folder inside this skill's own output directory for the diff and deleted afterwards.
**MailCraft is not installed on this macOS machine** (the ArtCraft Launcher opens an existing
install but does not install the unsigned macOS build), so there is no installed-binary `--version`
line and no live CLI run: every count below is derived from this tag's source. The macOS bundle
identifier in the packaging template is `io.github.billsecond.mailcraft`, minimum macOS 11.0
(`packaging/macos/Info.plist.in`).

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 343 engine command ids; 350 raw `CommandSpec::new("…")` sites incl. 7 `test.*` sites (6 ids) | `grep -rhoE 'CommandSpec::new\(\s*"[^"]+"' crates/ apps/`; fixtures in `crates/engine/src/{tests,session_tests,focus_stays_tests,store_session_tests,store_undo_body_tests,store_history_memory_tests}.rs` | implemented |
| 2 | 89 window command ids (`ui.*`), dispatchable by id like engine commands | `crates/ui-egui/src/lib.rs` `UI_COMMANDS`; dispatch fall-through in `crates/ui-egui/src/control.rs` | implemented |
| 3 | Feature catalog 332 rows, 17 out of scope, 247 of 315 in scope (78.4%) | `crates/engine/src/catalog.rs` `CATALOG` (pipe rows) + `OUT_OF_SCOPE`; matches `docs/parity-checklist.md` | implemented metric |
| 4 | 20 MCP tools (same names; `list_messages` gained `account` and a kind-taking `folder`), protocol `2025-06-18`, 1 MiB line cap | `crates/mcp/src/tools.rs` `tool(…)`; `crates/mcp/src/server.rs` `PROTOCOL_VERSION`, `MAX_LINE` | implemented |
| 5 | 20 control-channel method names; per-port key file; key proof before the bridge sends it | `crates/ui-egui/src/control.rs` `dispatch` (17 arms incl. `ui.minimize`); `apps/mailcraft/src/control_server.rs` (`auth`, `auth.challenge`); `crates/control-key/src/{lib,proof}.rs`; `docs/control-protocol.md` | implemented |
| 6 | The control key is `<settings>/control-key.local-<port>` in every packaging (was `control-key.<instance>`, Flatpak instance id) | `crates/control-key/src/lib.rs` `key_path` + module docs (#1199); `docs/control-protocol.md` "Keys"; `AGENTS.md` line 66; mode 0600 and removal in `apps/mailcraft/src/control_server.rs` `write_key_file` | implemented |
| 7 | 14 CLI subcommands, 18 long flags — unchanged at v0.13.0; `--folder` accepts folder kinds | `apps/mailcraft-cli/src/main.rs` `USAGE`, `run()` match arms, `value("--…")`/`flag("--…")`; `apps/mailcraft-cli/src/folder_kinds_tests.rs` | implemented |
| 8 | Import `.eml`, `.mbox`, `.ics`, `.vcf`; export `.mailcraft`, `.mbox`, `.eml`, `.ics`, `.vcf`; no `.ost`/`.msg`/`.olm`/`.pst` write | `crates/engine/src/io.rs` `Format::from_extension`; `crates/engine/src/cmd/file.rs`; `apps/mailcraft-cli/src/main.rs` `export_command`; `docs/gaps.md` gap 12 | implemented |
| 9 | `.pst` import of mail, contacts, calendar, tasks, notes and journal, with a report | `crates/engine/src/cmd/file.rs` `file.importPst` params; `crates/engine/src/import_pst/{item,contact,calendar,report}.rs`; `crates/pst/` | implemented (read only) |
| 10 | Mailbox form 4: record log + `<file>.blobs/` content folder + `headers-<n>.pack`; forms 1–3 read | `crates/engine/src/store_index.rs` (`VERSION = 4`, `OLDEST = 3`); `crates/engine/src/store.rs` module docs; `crates/engine/src/store_pack.rs`; `crates/model/src/headers.rs` | implemented |
| 11 | The first form-4 write keeps the old file as `<file>.before-<version>`; a v0.12.0 build refuses form 4 | `crates/engine/src/store_before.rs` module docs (`BEFORE`, `put_back`); `crates/engine/src/store.rs` | implemented |
| 12 | Import de-duplication, the local `Imported` folder for server accounts, and `mail.removeImportedDuplicates` | `crates/engine/src/cmd/file.rs`; `crates/engine/src/cmd/imported_dupes.rs` (`PARAMS`, `twins`, `kept`) | implemented |
| 13 | Snooze by command only: `mail.snooze`, `mail.unsnooze`, `mail.returnDue`; window UI deferred | `crates/engine/src/cmd/snooze.rs` (`CommandSpec` params); `crates/model/src/mailbox_snooze.rs`; `crates/ui-egui/src/snooze_tick.rs`; `docs/gaps.md` gap 17 still lists Snooze | implemented (commands) / deferred (window) |
| 14 | IMAP IDLE push plus skip-unchanged-folder Send/Receive | `crates/net/src/idle.rs`; `crates/proto/src/imap/{idle,status}.rs`; `crates/engine/src/sync_driver.rs`; `crates/ui-egui/src/idle_watch.rs` | implemented (not exercised) |
| 15 | Add Account discovery: MX, RFC 6186 SRV, autoconfig document, Mozilla ISP list; Exchange Autodiscover | `crates/net/src/discover.rs`; `crates/net/src/autoconfig.rs`; `docs/autodiscover.md`; `crates/ui-egui/src/account_setup/tests/` | implemented |
| 16 | Exchange 2010 and newer accepted; version step-down and change-key retry | `crates/ews/src/`; `crates/ews/src/exchange2010_tests.rs`; `docs/exchange-servers.md`; `docs/gaps.md` gap 5 | implemented |
| 17 | JMAP sends and takes read/flag/move/delete up; still browser-build-only | `crates/jmap/src/mail/{send,changes}.rs`; `crates/engine/src/cmd/jmap_up.rs`; `docs/jmap.md`; `docs/gaps.md` gap 5 | implemented (not exercised) |
| 18 | Accounts: local, IMAP+SMTP, Microsoft (Graph, OAuth), JMAP, Exchange Web Services; unknown kinds preserved | `crates/model/src/mailbox.rs` `AccountKind`; `crates/engine/src/cmd/account.rs` | implemented |
| 19 | Folder kinds (`inbox`, `sent`, `drafts`, `deleted`, `junk`, `archive`, `outbox`) in CLI and commands | `crates/engine/src/cmd/folder.rs`; `crates/mcp/src/tools.rs` `list_messages`; `docs/mcp.md` | implemented |
| 20 | Gmail labels shown and searched with `label:`/`labels:` | `crates/engine/src/gmail.rs`; `crates/model/src/gmail.rs`; `crates/model/src/search.rs` `KEYWORDS` | implemented |
| 21 | 8 interface languages (7 previews) + pseudo; 7 `.po` catalogues | `crates/i18n/src/lib.rs` `Lang::ALL: [Lang; 9]`; `crates/i18n/po/{de,es,fr,it,nl,ro,zh_CN}.po` | implemented |
| 22 | Close to system tray (off by default), Animations switch, Neutral/Blue grey dark theme, navigation bar at the foot | `apps/mailcraft/src/{tray,tray_unix,tray_native}.rs`; `crates/ui-egui/src/{close_to_tray,motion}.rs`; `apps/mailcraft/src/system_motion.rs`; `crates/ui-egui/src/theme/blue.rs`; `crates/engine/src/cmd/view.rs` `view.navigationBar` | implemented (not observed) |
| 23 | Memory is let go of while the window is out of sight | `crates/ui-egui/src/out_of_sight.rs`; `crates/ui-egui/src/control.rs` `ui.minimize` | implemented (not observed) |
| 24 | Phone-app packages are saved and never opened | `crates/engine/src/opening.rs`; `crates/engine/src/opening_tests.rs` | implemented |
| 25 | Android app and a UniFFI core for Kotlin/Swift exist in-tree, not in the release artifacts | `apps/mailcraft-android/`; `crates/mobile/src/lib.rs` (ADR 0023); `crates/host/src/lib.rs`; `README.md` "Platforms"; `docs/mobile-store-listing.md` | partial (in-tree, unreleased) |
| 26 | Agent gate: every command classified `safe`/`owner`/`never`; `--allow send,delete,accounts,mailbox,settings,input`; no file paths from agents; snooze is filing; `removeImportedDuplicates` safe only as `preview` | `crates/engine/src/agent.rs` (`Class`, `access`, `classify`, `NEEDS_IDS`); `crates/mcp/src/tools.rs` `exec`; `docs/mcp.md` | implemented |
| 27 | S/MIME and OpenPGP signatures are *checked*, not made; nothing signs, encrypts or decrypts; Mozilla's NSS roots stand in on Linux distributions without a mail bundle; none read on macOS | `crates/smime/src/`; `crates/openpgp/src/`; `crates/net/src/anchors_nss.rs`; `crates/engine/src/cmd/{mail,keys}.rs`; `docs/gaps.md` gap 16 | implemented (verification only) |
| 28 | HTML mail is laid out without running anything; remote pictures only on the owner's say-so, through a fetcher that sends only the address | `crates/html/src/`; `crates/net/src/pictures.rs`; `apps/mailcraft/src/picture_cache.rs`; `docs/gaps.md` gap 6 | implemented |
| 29 | Headless UI screenshots render the window offscreen | `crates/ui-egui/examples/ui_shot.rs` | implemented |
| 30 | No printing anywhere | `docs/gaps.md` gap 15; no print command among the 343 ids | not implemented (verified absent) |
| 31 | No `.ost`, `.msg` or `.olm`; no POP; JMAP browser-only; no CalDAV/CardDAV | `docs/gaps.md` gaps 12, 5 and the POP row; `crates/model/src/mailbox.rs` `AccountKind` | not implemented (verified absent) |
| 32 | Web build is CI-checked; no control channel and no sockets there | `apps/mailcraft-web/`; `docs/control-protocol.md`; `crates/net` empty on wasm (`docs/architecture.md`) | implemented (not exercised) |

## 2. Count methods and values (v0.12.0 → v0.13.0)

Set differences were computed by writing both id sets to files and running `comm -13` / `comm -23`
over them, so "added"/"removed" below are set differences, not impressions.

| Surface | Method | v0.12.0 | v0.13.0 |
|---|---|---:|---:|
| Engine commands | `CommandSpec::new("…")` literal ids in `crates/` + `apps/`, minus `test.*` fixtures | **338** | **343** (+`mail.snooze`, `mail.unsnooze`, `mail.returnDue`, `mail.removeImportedDuplicates`, `view.navigationBar`; none removed) |
| Raw command sites | same grep, unfiltered | 344 | 350 (7 `test.*` sites, 6 ids) |
| Window commands | `(  "ui.…"` rows inside `UI_COMMANDS`, `crates/ui-egui/src/lib.rs` | **85** | **89** (+`ui.closeToTray`, `ui.darkStyle`, `ui.animations`, `ui.dismissSoftwareNotice`) |
| Catalog rows / covered | pipe-separated `CATALOG` rows; covered = id in the engine id set | **331 / 246 (74.3%)** | **332 / 247 (74.4%)**; in scope 315 after 17 `OUT_OF_SCOPE` rows → **247/315 (78.4%)** |
| MCP tools | `tool(` entries in `crates/mcp/src/tools.rs` | **20** | **20** — same names; `list_messages` gained `account` + folder kinds |
| Control methods | `match req.method` arms in `crates/ui-egui/src/control.rs` + `command` alias + `auth`, `auth.challenge` | **19** | **20** (+`ui.minimize`) |
| CLI subcommands | top-level `match cmd` arms in `apps/mailcraft-cli/src/main.rs` | **14** | **14** — unchanged at v0.13.0 |
| CLI long flags | distinct `value("--…")`/`flag("--…")` options, minus `--help`/`--version` | **18** | **18** — unchanged at v0.13.0 |
| Crates / apps | directories under `crates/` / `apps/` | **23 / 3** | **28 / 4** (+`ber`, `host`, `jmap-types`, `mime-model`, `mobile`; +`apps/mailcraft-android`) |
| Mailbox file form | `VERSION` in `crates/engine/src/store_index.rs` | 3 | **4** (`OLDEST = 3`; forms 1 and 2 read by `store.rs`) |
| Interface languages | `Lang::ALL` length / `.po` catalogues | **7 / 5** (6 named + pseudo) | **9 / 7** (8 named + pseudo) |
| Search keywords | entries in `model::search::KEYWORDS` | 20 | **22** (+`label`, `labels`) |
| Shortcut specs | `.key(` in `crates/engine/src/cmd/` | **57** | **57** — unchanged at v0.13.0 |
| Composing / windows | `MAX_COMPOSING`, `MAX_WINDOWS` | 13 / 12 | 13 / 12 — unchanged |
| Fuzz targets | files in `fuzz/fuzz_targets/` | 26 | **27** |
| Tests | `#[test]` attributes in `crates/`, `apps/`, `xtask/` | 7,306 | **8,296** |
| MCP protocol / line cap | `PROTOCOL_VERSION`, `MAX_LINE` in `crates/mcp/src/server.rs` | `2025-06-18` / 1 MiB | unchanged at v0.13.0 |

## 3. Uncertain / not verified

- **No installed build.** No `--version`, no `mailcraft-cli commands --json`, no `parity` run, no
  conversion, no GUI launch. `apps/mailcraft/src/main.rs` prints
  `mailcraft {CARGO_PKG_VERSION} ({build sha})` and `apps/mailcraft-cli/src/main.rs` prints
  `mailcraft-cli {CARGO_PKG_VERSION}` with `Cargo.toml` at `0.13.0`; neither was executed.
- **GUI behaviour** (tray icon and its menu, the navigation bar's foot placement, both dark themes,
  the animations switch, the Romanian and Simplified Chinese catalogues, the reading-pane picture
  bar) is read from code and `docs/`, never observed.
- **Interoperability** is still the repo's weakest area (`docs/gaps.md` gap 1); this audit contacted
  no server. IDLE, the discovery chain, Autodiscover, Exchange 2010 step-down and JMAP send/up are
  verified as code paths with tests, not by exercise.
- **The Android app and the UniFFI core** are in-tree code with a Gradle project and ADR 0023; no
  build was attempted (no Android toolchain here) and no artifact is published.
- **Readiness percentages** (~25% real work, ~55% local viewer) are the repo's own estimates.
- **`docs/gaps.md` contradicts the code in two places** at this tag: gap 8 still calls the mailbox
  "format 3" (form 4), and gap 17 still lists Snooze although the three snooze commands exist.

## 4. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| `ROADMAP.md` headline: "338 commands · 19 crates, 3 apps" | 343 engine commands (+89 window commands) · 28 crates · 4 apps |
| `ROADMAP.md`: "246 / 314 in scope (78.3%)" | 247 / 315 in scope (78.4%) of 332 rows, 17 out of scope |
| `ROADMAP.md`: "5,401 `#[test]`s" | 8,296 `#[test]` attributes |
| `docs/parity-checklist.md`: "The registry holds 341 commands" | 343 (the ratio on the same line, 247/315, is right) |
| `docs/gaps.md` gap 8: "format 3, R6" | mailbox form 4 (`store_index.rs` `VERSION = 4`) |
| `docs/gaps.md` gap 17: Snooze listed among missing features | `mail.snooze`/`mail.unsnooze`/`mail.returnDue` exist; only the window's button is deferred |
| `docs/gaps.md` gap 14 heading: "Eight languages, seven of them previews" | agrees with the code at this tag (9 `Lang` values incl. pseudo, 7 `.po`) |
| `docs/architecture.md` crate and CLI lists | carried over from earlier releases; the CLI list omits nothing now but the crate count is short |
| `README.md` "Platforms" (desktop + web only) | agrees: the Android project is not a shipped platform |

## 5. Verification commands (read-only)

Run from the pinned checkout; `OLD` was the throwaway v0.12.0 clone, deleted afterwards.

```sh
git rev-parse HEAD                                                     # 240d1d42fe394cf3274402b180663ba9b43ca180
git describe --tags                                                    # v0.13.0
git rev-list --count HEAD                                              # 1 (shallow, single commit)
git status --porcelain                                                 # empty: the checkout was never written

# engine command ids, and the set difference against the old tag
grep -rhoE 'CommandSpec::new\(\s*"[^"]+"' crates/ apps/ \
  | sed -E 's/.*"([^"]+)"/\1/' | grep -v '^test\.' | sort -u > ids_new.txt   # 343
comm -13 ids_old.txt ids_new.txt                                        # the 5 added ids
comm -23 ids_old.txt ids_new.txt                                        # none

# window commands
python3 -c 'extract ("ui.…" rows between "pub const UI_COMMANDS" and "];" in crates/ui-egui/src/lib.rs)'  # 89

# MCP tools, control methods, CLI surface
grep -cE '^\s+tool\(' crates/mcp/src/tools.rs                          # 20
grep -oE 'tool\("[a-z_]+"' crates/mcp/src/tools.rs                      # the 20 names
grep -nE '^\s+"[a-z.]+" =>' crates/ui-egui/src/control.rs               # dispatch arms (+ui.minimize)
grep -nE 'method == "' apps/mailcraft/src/control_server.rs              # auth, auth.challenge
grep -nE '^\s+"[a-z][a-z-]*" =>' apps/mailcraft-cli/src/main.rs          # 14 subcommands
grep -oE '(value|flag)\("--[a-z-]+"\)' apps/mailcraft-cli/src/main.rs    # 18 flags

# catalog, formats, sizes
awk -F'|' 'rows of CATALOG' crates/engine/src/catalog.rs                # 332 rows, 247 covered
head -6 docs/parity-checklist.md                                        # 247 of 315, 17 out of scope
grep -n 'VERSION: u32\|OLDEST: u32' crates/engine/src/store_index.rs     # 4 / 3
ls crates | wc -l ; ls apps                                             # 28 / 4
grep -n 'pub const ALL' crates/i18n/src/lib.rs ; ls crates/i18n/po       # [Lang; 9] / 7 catalogues
grep -oE '^\s+"[a-z]+",' crates/model/src/search.rs                     # 22 keywords
grep -rhoE '\.key\(' crates/engine/src/cmd/ | wc -l                     # 57
ls fuzz/fuzz_targets | wc -l                                            # 27
grep -rhoE '#\[test\]' crates apps xtask | wc -l                        # 8296
grep -n 'control-key' crates/control-key/src/lib.rs                     # control-key.local-<port>
grep -n 'LABEL\|NONCE_LEN' crates/control-key/src/proof.rs              # challenge text and nonce bounds
grep -n 'PROTOCOL_VERSION\|MAX_LINE' crates/mcp/src/server.rs           # 2025-06-18, 1 MiB

# the diff that the delta paragraph rests on
git clone --depth 1 --branch v0.12.0 https://github.com/UCS-Care-Group/mailcraft OLD
diff -rq OLD <checkout> --exclude=.git                                  # 405 changed, 137 added, 8 removed
diff -u OLD/crates/engine/src/cmd/mod.rs <checkout>/crates/engine/src/cmd/mod.rs   # +snooze, +imported_dupes
```

## 6. What was re-measured vs carried forward

- **Re-measured at this tag, from code:** engine commands (343, with the exact five added), window
  commands (89, with the four added), catalog rows and coverage (332 / 247 / 315 in scope), MCP tools
  (20, same names, one new argument), control methods (20, +`ui.minimize`), CLI subcommands and flags (14 / 18,
  unchanged, plus the folder-kind behaviour), crates and apps (28 / 4), mailbox form (4) and the
  header-pack layout, languages (8 + pseudo, 7 catalogues), search keywords (22), shortcut specs
  (57), composing and window limits (13 / 12), fuzz targets (27), tests (8,296), MCP protocol and
  line cap, and the format extension set.
- **Re-verified as unchanged:** the import/export matrix, `.pst` read-only import, the agent gate and
  its classes, HTML mail without a script engine, the picture fetcher's rules, signature *checking*
  only, rules, the calendar and meeting workflow, notes and journal without windows, the browser
  build's reach, and the control channel's 1 MiB / 30 s / `unauthorized` limits.
- **Changed this round:** the control-key path scheme (now `control-key.local-<port>` everywhere),
  the mailbox form (3 → 4, with `<file>.before-<version>`), and the MCP/CLI `folder` arguments
  accepting folder kinds.
- **Carried forward from the v0.12.0 skill and re-checked:** every claim whose code path still
  exists at this tag; the three standing cautions (no printing, no `.ost`/`.msg`/`.olm`, one window
  and one Undo stack shared with an agent).
- **Not carried forward:** the 0.12.0 sentence that the working mailbox is form 3, and the
  `control-key.<instance>` description — both are wrong at this tag.

## 7. references/ preserved

`references/automation-surface.md` was kept and updated to this tag (20 control methods including
`ui.minimize`, 343 engine commands, 89 `ui.*` commands regrouped by their declared location, the
exact control-key path and challenge, the folder-kind arguments, and the unchanged 20 MCP tools). No
reference file was dropped, and no new one was added: no whole new automation surface appeared.

## CLI availability (measured 2026-11-15)

- Release asset: `mailcraft-cli-0.13.0-macos-universal.zip`, 20.1 MB, on
  `https://github.com/UCS-Care-Group/mailcraft/releases/download/v0.13.0/`.
- `SHA256SUMS.txt` (22 lines, all plain two-field `<sha256>  <asset>` lines; `grep -F "$ASSET"`
  matches exactly the CLI-zip line):
  `8b78129c9ae9a6138767c23f3ba27900a3f9757d4379943a7fac9451d5b9b636  mailcraft-cli-0.13.0-macos-universal.zip`
- Bundle `find`: there is no `/Applications/MailCraft.app` on the authoring machine — MailCraft is
  not installed at all — so there is no bundle to inspect and no bundle path is claimed. The
  launcher's bundle would hold only `MailCraft`; that could not be verified here.
- Ran: nothing for MailCraft. Only the release's `SHA256SUMS.txt` was fetched; no CLI was
  downloaded, installed or executed. The round's end-to-end recipe proof was run on MaterialCraft's
  11.9 MB zip and its real output is pasted in that skill's evidence file.
