# Craft Anything — evidence ledger (tag v0.2.0)

Audit basis: this checkout is tag **`v0.2.0`**, commit **`b09b99aaa7985ebbc3d0fef467c4b688d4727cc1`**
("Release 0.2.0", 2026-11-01; shallow clone of the release tag). Inspection date **2026-11-02**; the
v0.1.0 ref was fetched for set diffs. Installed `/Applications/Craft Anything.app` prints
`craft-anything 0.2.0` (bundle id `ai.storyteller.craft-anything`); the GUI was never launched.

v0.1.0 → v0.2.0 delta: engine tool surface unchanged — `docs/tools.md` byte-identical
(298 tools / 17 toolsets; `grep -c '^- '` = 298 both tags), MCP prompts 6, CLI subcommands 13.
Changes are in the agent/AI layer: OpenCode adapter (`crates/ai/src/cli_agents/adapters/opencode.rs`,
invokes `opencode run`), failure log (`failure_log.rs`), rebuild activity feed
(`rebuild/activity.rs`), resume journal (`journal.rs`), deadlock watchdog, Windows npm agents,
LM Studio boolean-subschema compat, CJK release fonts, doctor model-probe.
**Corrections vs the v1.1.0 skill** (wrong at v0.1.0 too — the skill had copied the stale
`docs/file-formats.md`): version constants are `MANIFEST_VERSION` = 2 (`workspace.rs:63`),
`SETTINGS_VERSION` = 3 (`settings.rs:217`), `FORMAT_VERSION` = 1 (`project.rs:22`), proven by the
compile-time step-count assertions (`MANIFEST_STEPS` has 2 steps, `SETTINGS_STEPS` 3); the
`docs/file-formats.md` table (manifest 1 / settings 2) lags the code — repo-doc drift; versioned-file
rows in that doc count **11** (the old skill said 12).

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 298 engine tools in 17 toolsets; each an MCP tool + CLI command | `docs/tools.md` (generated, 298 `- ``id`` ` rows, byte-identical v0.1.0 → v0.2.0); `crates/engine/src/tool_list.rs` `MIN_TOOLS = 271` and `report()` | implemented |
| 2 | Toolsets and sizes | `docs/tools.md` section headers: core 34, native 55, apple 14, formats 36, managed 8, android 14, java 6, adb 24, browser 22, javascript 11, runtime 14, frida 9, application 17, database 1, projects 18, setup 9, build 6 | implemented |
| 3 | README's "284 tools" is stale | README "Agent-ready" vs generated `docs/tools.md` 298 | doc drift |
| 4 | MCP server: Essentials + enabled toolsets, `--all-tools`, `--inbox` | `apps/craft-anything-cli/src/main.rs` `Command::Mcp`; `crates/mcp/src/lib.rs` `tools_list` | implemented |
| 5 | 6 guided MCP prompts with discipline rules | `crates/mcp/src/prompts.rs` `PROMPTS` (6 entries), `DISCIPLINE` (6 rules) | implemented |
| 6 | CLI subcommands incl. tool pass-through | `apps/craft-anything-cli/src/main.rs` `Command` (13 named + `Tool(Vec<String>)`) | implemented |
| 7 | `rebuild` flags: rounds default 2, backend, unattended, project-folder, continue-in/resume, deep/clean-room | `apps/craft-anything-cli/src/rebuild_cmd.rs` `RebuildArgs` | implemented |
| 8 | Clean room vs Deep; deep refuses look-inside in Clean room | `README.md` "Clean room or Deep"; `crates/engine/src/tools/deep.rs`; `crates/engine/src/clean_room.rs` | implemented |
| 9 | Claude Code first-class builder; Codex and (new at v0.2.0) OpenCode adapters unverified | `README.md` "AI"; `docs/claude-code.md`; `crates/ai/src/cli_agents/adapters/opencode.rs` (`opencode run`) | implemented / partial (codex, opencode) |
| 10 | Versioned project files; newer files never downgraded | `docs/file-formats.md` table (11 rows); `crates/engine/src/versioned.rs` | implemented |
| 11 | Version constants: manifest 2, settings 3, .cany 1 (code; docs table is stale) | `crates/engine/src/workspace.rs:63`, `crates/engine/src/settings.rs:217`, `crates/engine/src/project.rs:22`; step-list assertions `MANIFEST_STEPS`/`SETTINGS_STEPS`/`FORMAT_STEPS` | implemented |
| 12 | External engines detected (Ghidra, Cutter, rizin, GDB, Frida, adb, jadx, CDP) | `crates/engines/src/` modules; `doctor` command | implemented |
| 13 | macOS bundle contains no CLI | `/Applications/Craft Anything.app/Contents/MacOS/` listing | verified absent |
| 14 | No DRM/login/anti-cheat bypass; responsible-use rule | `README.md` "Responsible use" | policy (by design) |
| 15 | v0.2.0 agent layer: failure log, activity feed, resume journal, deadlock watchdog | `crates/ai/src/failure_log.rs`; `crates/ai/src/rebuild/activity.rs`; `crates/engine/src/journal.rs` | implemented |

## 2. Counts

| Surface | v0.1.0 (measured) | v0.2.0 (measured) |
|---|---:|---:|
| Engine tools / toolsets | 298 / 17 | 298 / 17 (unchanged) |
| Tool floor `MIN_TOOLS` | 271 | 271 |
| MCP prompts | 6 | 6 |
| CLI subcommands | 13 named + tool pass-through | 13 named + tool pass-through |
| Versioned file formats (doc rows) | 11 | 11 |
| Workspace crates / apps | 13 / 3 | 13 / 3 |
| Interface languages | n/a (English-first at this tag) | n/a (release builds ship CJK fonts, UI still English-first) |

## 3. Uncertain / not verified

- GUI behaviour never launched; Simple/Advanced workbench claims come from README + screenshots
  (`docs/images/`) + the UI crate layout.
- Tool-level availability on this machine (which toolsets light up) depends on installed engines;
  `craft-anything-cli capabilities` is the live answer.
- The Codex and OpenCode adapters are unverified upstream and were not exercised here.

## 4. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                  # b09b99aaa7985ebbc3d0fef467c4b688d4727cc1
grep -c '^- `' docs/tools.md                                   # 298
grep -oE '\(`[a-z]+`, [0-9]+\)' docs/tools.md | wc -l          # 17
grep -n 'MIN_TOOLS' crates/engine/src/tool_list.rs             # 271
grep -cE 'name: "' crates/mcp/src/prompts.rs                   # 6 prompts
grep -cE '^\| `' docs/file-formats.md                          # 11 versioned files
grep -n 'pub const MANIFEST_VERSION' crates/engine/src/workspace.rs   # 2
grep -n 'pub const SETTINGS_VERSION' crates/engine/src/settings.rs    # 3
grep -n 'pub const FORMAT_VERSION' crates/engine/src/project.rs       # 1
```
