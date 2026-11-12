# Craft Anything — evidence ledger (tag v0.6.1)

Audit basis: this checkout is tag **`v0.6.1`**, commit **`48a9c5a60ff83ff620f98661339be6281a7debc6`**
("Merge tested main for v0.6.1", 2026-11-11; shallow clone of the release tag). Inspection date
**2026-11-12**. The previous tag **`v0.5.0`** = `622d023cdfdb91c00df8b9a37c486a2a18fb0917` is the
other shallow root and was diffed for the delta. The installed bundle is 0.6.1
(`CFBundleIdentifier` `ai.storyteller.craft-anything`); its bundled `craft-anything-cli --version`
prints `craft-anything-cli 0.6.1`; the GUI was never launched.

v0.5.0 → v0.6.1 delta (tree diff, 499 files, +51,694/−3,455): engine tools **301 → 303** in the
same 17 toolsets (`core` 35 → 36 for `core_text_read`; `projects` 20 → 21 for
`project_approvals_set`); `MIN_TOOLS` stays 271. A per-project **approval policy** landed for seven
builder action kinds (allow/ask/refuse, unset following Auto mode); `craft.json` 2 → 5
(`approvals`, `agent_session_deep`, `capture_deep`), `build-progress.json` 1 → 2 (`checked`) and
`transcript.json` 1 → 2 (`deep`). Coding-agent built-ins 9 → 12 (Aider, Grok Build, Devin) with a
new grants table, and the known CLI list 11 → 14. UI languages 15 → 17 (Thai, Estonian). The
installed CLI prints **323** commands (303 + 20 AI/setup). **Doc drift, still uncorrected:**
README says "320 tools (300 in the engine)" and `docs/STATUS.md` says "300 engine tools (320 with
the AI and setup layers')" against 303/323 in the generated list; `docs/file-formats.md`'s
`config.toml` row says `SETTINGS_VERSION` = 2 while the code constant is 3.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 303 engine tools in 17 toolsets; each an MCP tool + CLI command + agent tool | `docs/tools.md` (generated, 303 tool rows); `crates/engine/src/tool_list.rs` `MIN_TOOLS = 271` and `report()` | implemented |
| 2 | Toolset sizes: core 36, native 55, apple 14, formats 36, managed 8, android 14, java 6, adb 24, browser 22, javascript 11, runtime 14, frida 9, application 17, database 1, projects 21, setup 9, build 6 | `docs/tools.md` section headings (sums to 303) | implemented |
| 3 | The CLI's `commands` list is 323, not 303: 20 AI/setup tools on top (`rebuild_*` 9, `assets_key_*` 3, `ai_model*` 4, `setup_*` 4) | installed `craft-anything-cli commands` (323 rows) diffed against the 303 ids in `docs/tools.md`; `apps/craft-anything-cli/src/main.rs` `make_engine` (adds `craft_anything_ai::tools()` and `craft_anything_setup::tools::specs()`); `crates/ai/src/rebuild/tools.rs`, `model_tools.rs`, `key_tools.rs`; `crates/setup/src/tools.rs` | implemented |
| 4 | 12 named CLI subcommands, 11 shown by `--help`, hidden `builder-notes`, plus the external tool pass-through | `apps/craft-anything-cli/src/main.rs` `Command` (12 variants + `Tool(Vec<String>)`); installed `--help` | implemented |
| 5 | MCP lists 323 tools in Deep `--all-tools` and 108 in Clean room `--all-tools`; 6 guided prompts | live `tools/list` and `prompts/list` against the installed CLI; `crates/mcp/src/lib.rs` `listed`/`tools_list`; `crates/mcp/src/prompts.rs` `PROMPTS` (6); `crates/engine/src/clean_room.rs` `TOOLS` (108 ids) | implemented |
| 6 | Shared-host MCP mode: `--restricted`, `--allow-web`, `--allow-capture`, `--inbox`, `--target` | `apps/craft-anything-cli/src/main.rs` `Command::Mcp`; `crates/mcp/src/lib.rs` `restricted_refusal` — unchanged at v0.6.1 | implemented |
| 7 | `core_text_read` (new): paged text read, UTF-8 / BOM'd UTF-16, 200 lines default, 2,000 max, 256 KiB a page, 64 MiB a file, binary refused, runs nothing; Deep-only | `crates/engine/src/tools/text_tools.rs`; `docs/tools.md` `core` list; `docs/tool-status.md` "15 new"; absent from `crates/engine/src/clean_room.rs` | implemented; unit-tested, not in the 2026-10-16 functional audit |
| 8 | `project_approvals_set` (new): seven kinds, allow/ask/refuse/default, Auto-mode defaults; an agent's call can only tighten | `crates/engine/src/tools/project_tools.rs`; `crates/engine/src/workspace.rs` `ACTION_KINDS`, `Manifest::approval`, `Agent` caller check; `crates/engine/src/clean_room.rs` (allowed); `docs/claude-code.md` | implemented |
| 9 | Approval policy recorded per project in `craft.json` `approvals`; Auto on allows web/commands/outside_files and refuses the other four; Auto off asks for all but web | `crates/engine/src/workspace.rs` `ACTION_KINDS` rows `auto`/`manual`; `docs/schemas/craft.schema.json` `approvals`; `docs/file-formats.md` manifest 5 | implemented |
| 10 | 12 built-in coding-agent adapters (9 with their own module) and 14 known agent CLIs; Aider, Grok Build and Devin added | `crates/ai/src/cli_agents/adapters.rs` `built_in` (12 `Arc::new`), `crates/ai/src/cli_agents/adapters/*.rs` (9 files), `crates/ai/src/cli_agents/mod.rs` `KNOWN` (14) | implemented; declarations only — no live run here |
| 11 | Grants table: Claude Code, Copilot (ACP) and Grok (ACP) get tool server + approvals; Codex, OpenCode and DeepSeek Harness get the server without our approvals; Devin's print path gets neither, while its ACP build path hands over the server and approvals; Gemini CLI, Antigravity, Hermes, Maki and Aider get neither | `crates/ai/src/cli_agents/grants.rs` `DECLARED`; `crates/ai/src/cli_agents/adapters/devin.rs` ACP note | implemented (typed declarations checked by tests) |
| 12 | Deep Claude Code builders may start subagents; Clean room leaves `Agent` out | `crates/ai/src/cli_agents/adapters.rs:459` and `crates/ai/src/cli_agents/mod.rs:1932`; `docs/claude-code.md` | implemented |
| 13 | Clean room vs Deep; only 108 tools run/list in Clean room; Clean room is a rule, not an OS sandbox | `crates/engine/src/clean_room.rs`; `crates/mcp/src/lib.rs` `listed`; `README.md` "Clean room or Deep" | implemented |
| 14 | Versioned project files, newer files never downgraded; manifest 5, settings 3, `.cany` 1, transcript 2, build-progress 2, pin 2, feed 5; docs table has 12 rows | `docs/file-formats.md`; `crates/engine/src/workspace.rs:83`; `crates/engine/src/settings.rs:222`; `crates/engine/src/project.rs:22`; `crates/ai/src/context.rs:22`; `crates/engine/src/workspace/progress.rs:21`; `crates/engine/src/pins.rs:37`; `crates/engine/src/feed.rs:19`; `crates/engine/src/versioned.rs` | implemented; settings row of the doc is stale (says 2) |
| 15 | Mode is recorded with the work: `agent_session_deep`, `capture_deep`, transcript `deep`; a pre-v4 session and pre-v5 capture migrate as Deep, a capture with no recorded mode is studied again, and a transcript without `deep` resumes only in Deep | `crates/engine/src/workspace.rs` `manifest_v3_to_v4`/`manifest_v4_to_v5`; `crates/ai/src/rebuild/study.rs` `capture_deep`; `crates/ai/src/rebuild/mod.rs` `capture_in_mode`; `crates/ai/src/context.rs` `TRANSCRIPT_VERSION` 2; `docs/file-formats.md` | implemented |
| 16 | A fully passing check round is kept in `build-progress.json` `checked` and stands while its inputs are unchanged | `crates/ai/src/rebuild/kept_check.rs`; `crates/engine/src/workspace/progress.rs` `CheckedBuild`; `docs/schemas/build-progress.schema.json` | implemented |
| 17 | `rebuild` flags unchanged (`--rounds` default 2, `--backend`, `--unattended`, `--projects-dir`, `--project-folder`, `--existing`, `--continue-in`, `--resume`, `--deep`/`--clean-room`, `--build-with`, `--generate-assets`); a folder already holding a project becomes a follow-up and refuses the new-project-only flags | `apps/craft-anything-cli/src/rebuild_cmd.rs` `RebuildArgs`; installed `rebuild --help`; `crates/ai/src/rebuild/project.rs` `has_project`/`attached_request` | implemented |
| 18 | 8 new-project toolchains (Rust, Node.js, Python, Go, .NET, Maven, Gradle, Make) | `crates/engine/src/toolchains.toml` (8 `[[toolchain]]`); `docs/STATUS.md` "New-project toolchains" | implemented / unchanged |
| 19 | 17 UI languages (Thai and Estonian added) | `crates/ui-egui/src/i18n.rs` `LANGUAGES` (17 entries); `crates/ui-egui/src/i18n/{th,et}.tsv`; `docs/localization.md` | implemented |
| 20 | Codex CLI discovered inside ChatGPT.app/Codex.app after PATH; Settings → AI Check runs `--version`/sign-in status on a worker without a prompt | `crates/ai/src/cli_agents/mod.rs:165` (bundle locations); `docs/codex.md`; `docs/STATUS.md` "Local Codex discovery and sign-in" | implemented; fixture-tested, no live Codex run |
| 21 | `requests_per_minute` paces every request on an API backend | `crates/ai/src/pace.rs`; `crates/ai/src/config.rs` `requests_per_minute`; `crates/ai/src/lib.rs` paced model | implemented |
| 22 | `ai add --acp`, `ai key --forget`, `ai test`, and the `ai model`, `effort`, `builder`, `extractor`, `program` and `folder` subcommands | `apps/craft-anything-cli/src/ai_cmd.rs` `AiCommand`; installed `ai --help` | implemented |
| 23 | README's 320/300 and `docs/STATUS.md`'s 300/320 are stale; quote 303/323 | `README.md:89`, `README.md:190`, `docs/STATUS.md:267` vs `docs/tools.md` and the live `commands`/`capabilities` count | doc drift |
| 24 | No DRM/login/anti-cheat bypass; dependency installs run code and are consent-gated | `README.md` "Responsible use", "Clean room or Deep" | policy (by design) |
| 25 | macOS bundle ships `craft-anything-cli` beside the app | bundle `Contents/MacOS/` listing (two executables); `craft-anything-cli --version` → 0.6.1 | verified present |
| 26 | `setup` writes the plain `mcp` command, so re-running it over an `--all-tools` entry drops the full tool list; `--dry-run` changes nothing | `crates/setup/src/plan.rs` `default_command` (`[cli, "mcp"]`); `crates/setup/src/skill.md` warning | implemented |

## 2. Counts

| Surface | v0.5.0 (measured then) | v0.6.1 (measured now) |
|---|---:|---:|
| Engine tools / toolsets | 301 / 17 | **303 / 17** |
| Tool floor `MIN_TOOLS` | 271 | 271 (unchanged) |
| CLI `commands` entries | 321 | **323** (303 + 20 AI/setup) |
| Named CLI subcommands | 12 | 12 (unchanged) |
| MCP tools (Deep, `--all-tools`) | not captured | **323** |
| MCP tools (Clean room, `--all-tools`) | not captured | **108** |
| MCP prompts | 6 | 6 (unchanged) |
| Versioned file formats (doc rows) | 12 | 12 (versions changed) |
| UI languages (`LANGUAGES`) | 15 | **17** |
| Project toolchains | 8 | 8 (unchanged) |
| Built-in agent adapters / modules / known CLIs | 9 / 6 / 11 | **12 / 9 / 14** |
| Approval kinds | 0 | **7** |
| Workspace crates / apps | 13 / 3 | 13 / 3 (unchanged) |

## 3. Uncertain / not verified

- GUI behaviour never launched; Simple/Advanced workbench claims come from README + screenshots
  (`docs/images/`) + the UI crate layout. The new approval-policy UI is documented from code and
  `docs/claude-code.md`, not observed on screen.
- Tool-level availability on this machine depends on installed engines; the live `capabilities`
  run found adb, a Chromium browser, LLDB, Java and objdump, and no Ghidra/JADX/Apktool/Frida/tshark.
  `craft-anything-cli capabilities` remains the live answer.
- Codex, Copilot, Grok, Devin, Aider and the other adapters were not exercised here; their status is
  the README's claim plus the typed grants table, not a live measurement.
- The 15 new tools in `docs/tool-status.md` are unit/smoke-tested rather than part of the
  2026-10-16 real-input audit; `core_text_read` is among them.
- `docs/file-formats.md` still says `SETTINGS_VERSION` = 2; the code and its migration list say 3.
  This drift has persisted across the v0.1.0, v0.3.0, v0.5.0 and v0.6.1 audits.

## 4. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                  # 48a9c5a60ff83ff620f98661339be6281a7debc6
git -C <clone> describe --tags --exact-match                   # v0.6.1
grep -c '^- `' docs/tools.md                                   # 303
grep -oE '\(`[a-z]+`, [0-9]+\)' docs/tools.md | wc -l          # 17 toolsets
grep -n 'MIN_TOOLS' crates/engine/src/tool_list.rs             # 271
grep -cE 'name: "' crates/mcp/src/prompts.rs                   # 6 prompts
grep -cE '^\| `' docs/file-formats.md                          # 12 versioned files
grep -cE 'LangInfo \{ code:' crates/ui-egui/src/i18n.rs        # 17 UI languages
grep -c '\[\[toolchain\]\]' crates/engine/src/toolchains.toml  # 8 toolchains
sed -n '/pub fn built_in/,/^        }/p' crates/ai/src/cli_agents/adapters.rs | grep -c 'Arc::new'   # 12 built-in adapters
ls crates/ai/src/cli_agents/adapters/*.rs | wc -l              # 9 adapter modules
grep -c '^    ("' crates/ai/src/cli_agents/mod.rs              # 14 known agent CLIs
sed -n '/const ACTION_KINDS/,/^];/p' crates/engine/src/workspace.rs | grep -c 'KindRow {'   # 7 approval kinds
<installed bundle>/Contents/MacOS/craft-anything-cli --version # craft-anything-cli 0.6.1
<installed bundle>/Contents/MacOS/craft-anything-cli commands | jq 'length'        # 323
<installed bundle>/Contents/MacOS/craft-anything-cli capabilities | jq '.tools'    # 323
# MCP tools/list with --all-tools: 323 with --deep, 108 without (Clean room)
# MCP prompts/list: 6
grep -n 'pub const MANIFEST_VERSION' crates/engine/src/workspace.rs   # 5
grep -n 'pub const SETTINGS_VERSION' crates/engine/src/settings.rs    # 3
grep -n 'pub const FORMAT_VERSION' crates/engine/src/project.rs        # 1
grep -n 'pub const TRANSCRIPT_VERSION' crates/ai/src/context.rs        # 2
grep -n 'pub const BUILD_PROGRESS_VERSION' crates/engine/src/workspace/progress.rs  # 2
grep -n 'pub const PIN_VERSION' crates/engine/src/pins.rs              # 2
grep -n 'pub const FEED_VERSION' crates/engine/src/feed.rs             # 5
```

## Round 2026-11-04 (refresh)

- Pinned to `v0.3.0` = `e6280b5dc518b9f3266c82d794a4e2f0367d9a53` (installed `craft-anything 0.3.0`).
- Engine tools 298 → **299** (`projects` 18 → 19). The macOS bundle does ship `craft-anything-cli` — corrected.
- Id sets were diffed between the two tags with the same extraction method as the claims above; counts here are the new ones.

## Round 2026-11-07 (pin-and-verify refresh to v0.5.0)

- Re-pinned to `v0.5.0` = `622d023cdfdb91c00df8b9a37c486a2a18fb0917`; installed bundle 0.5.0, bundled CLI `craft-anything-cli 0.5.0` (read-only `--version`/`--help`/`commands`; GUI not launched).
- **Re-measured:** 301 tool ids in `docs/tools.md` and 17 toolsets (heading counts); 321 entries from the installed CLI's `commands` JSON; 6 prompts; 13 `Command` variants (12 named + the external tool pass-through); 12 format rows; 15 `LANGUAGES` entries; 8 toolchains; 13 crates + 3 apps. Constants re-read from source: 2 / 3 / 1 plus pin 2, feed 5, build-progress 1.
- **Corrected:** CLI subcommands had been described as "13 named"; the bundle's CLI presence had been corrected in prose but contradicted later in "How to operate"; `config.toml` settings version had been given as 2 in one place (3 is correct); README tool numbers were 320/300 against 301.

## Round 2026-11-12 (pin-and-verify refresh to v0.6.1)

- Re-pinned to `v0.6.1` = `48a9c5a60ff83ff620f98661339be6281a7debc6`; installed bundle 0.6.1 (`Info.plist`), bundled CLI `craft-anything-cli 0.6.1` (read-only `--version`/`--help`/`commands`/`capabilities`/tool `--help`; GUI not launched).
- **Re-measured:** 303 tool ids / 17 toolsets (sizes above sum to 303); 323 `commands` entries with the 20 extras diffed against the generated list; 12 `Command` variants; 6 prompts (also live over `prompts/list`); 12 format rows; 17 `LANGUAGES`; 8 toolchains; 12 built-in adapters / 9 modules / 14 known CLIs; 7 approval kinds; 13 crates + 3 apps. Live MCP `tools/list`: 323 in Deep `--all-tools`, 108 in Clean room (matches `clean_room::TOOLS`).
- **Corrected:** the v0.5.0 delta's "adapters 3 → 6" was counting adapter *module files*, not the built-in registry (which held 9); both bases are now stated. The new MCP mode filter (Deep 323 / Clean room 108) is documented for the first time. `docs/file-formats.md` now documents manifest 5, progress 2 and transcript 2, but still says settings 2 against the code's 3.
- **Unchanged at v0.6.1:** 17 toolsets, `MIN_TOOLS` 271, 6 MCP prompts, 12 named CLI subcommands, 12 versioned-file rows, 8 toolchains, 13 crates / 3 apps, the `rebuild` flag set and defaults, the three-width website check and game self-test model, the `--restricted` MCP mode, `pin.json` 2 and `feed.json` 5.
- **Path check:** every repo-relative path cited in `SKILL.md`/`evidence.md` was re-resolved against the clone; all exist. `crates/engine/src/tools/{text_tools,project_tools,interaction_tools}.rs`, `crates/ai/src/cli_agents/{adapters,grants}.rs`, `crates/ai/src/{pace,context}.rs`, `crates/ai/src/rebuild/{kept_check,study}.rs`, `crates/setup/src/plan.rs`, `crates/setup/src/skill.md`, `crates/ui-egui/src/i18n.rs`, `crates/engine/src/{workspace,settings,project,pins,feed}.rs`, `crates/engine/src/workspace/progress.rs` were read at the new tag.
