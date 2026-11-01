# Craft Anything — evidence ledger (tag v0.1.0)

Audit basis: this checkout is tag **`v0.1.0`**, commit **`c316051c9e01e1bf9863f3c802a805179afa4663`**
("Release 0.1.0", 2026-10-31; shallow clone of the release tag). Inspection date **2026-11-01**.
Installed `/Applications/Craft Anything.app` prints `craft-anything 0.1.0` (bundle id
`ai.storyteller.craft-anything`); the GUI was never launched.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 298 engine tools in 17 toolsets; each an MCP tool + CLI command | `docs/tools.md` (generated, 298 `- ``id`` ` rows); `crates/engine/src/tool_list.rs` `MIN_TOOLS = 271` and `report()` | implemented |
| 2 | Toolsets and sizes | `docs/tools.md` section headers: core 34, native 55, apple 14, formats 36, managed 8, android 14, java 6, adb 24, browser 22, javascript 11, runtime 14, frida 9, application 17, database 1, projects 18, setup 9, build 6 | implemented |
| 3 | README's "284 tools" is stale | README "Agent-ready" vs generated `docs/tools.md` 298 | doc drift |
| 4 | MCP server: Essentials + enabled toolsets, `--all-tools`, `--inbox` | `apps/craft-anything-cli/src/main.rs` `Command::Mcp`; `crates/mcp/src/lib.rs` `tools_list` | implemented |
| 5 | 6 guided MCP prompts with discipline rules | `crates/mcp/src/prompts.rs` `PROMPTS` (6 entries), `DISCIPLINE` (6 rules) | implemented |
| 6 | CLI subcommands incl. tool pass-through | `apps/craft-anything-cli/src/main.rs` `Command` (13 named + `Tool(Vec<String>)`) | implemented |
| 7 | `rebuild` flags: rounds default 2, backend, unattended, project-folder, continue-in/resume, deep/clean-room | `apps/craft-anything-cli/src/rebuild_cmd.rs` `RebuildArgs` | implemented |
| 8 | Clean room vs Deep; deep refuses look-inside in Clean room | `README.md` "Clean room or Deep"; `crates/engine/src/tools/deep.rs`; `crates/engine/src/clean_room.rs` | implemented |
| 9 | Claude Code first-class builder; Codex adapter unverified | `README.md` "AI"; `docs/claude-code.md`; `crates/ai/` | implemented / partial (codex) |
| 10 | Versioned project files; newer files never downgraded | `docs/file-formats.md` table (12 rows); `crates/engine/src/versioned.rs` | implemented |
| 11 | Version constants: manifest 1, settings 2, .cany 1 | `docs/file-formats.md`; `crates/engine/src/{workspace,settings,project}` | implemented |
| 12 | External engines detected (Ghidra, Cutter, rizin, GDB, Frida, adb, jadx, CDP) | `crates/engines/src/` modules; `doctor` command | implemented |
| 13 | macOS bundle contains no CLI | `/Applications/Craft Anything.app/Contents/MacOS/` listing | verified absent |
| 14 | No DRM/login/anti-cheat bypass; responsible-use rule | `README.md` "Responsible use" | policy (by design) |

## 2. Counts: first audit (no previous skill)

| Surface | v0.1.0 (measured) |
|---|---:|
| Engine tools / toolsets | 298 / 17 |
| Tool floor `MIN_TOOLS` | 271 |
| MCP prompts | 6 |
| CLI subcommands | 13 named + tool pass-through |
| Versioned file formats | 12 |
| Workspace crates / apps | 13 / 3 |
| Interface languages | n/a (English-first at this tag) |

## 3. Uncertain / not verified

- GUI behaviour never launched; Simple/Advanced workbench claims come from README + screenshots
  (`docs/images/`) + the UI crate layout.
- Tool-level availability on this machine (which toolsets light up) depends on installed engines;
  `craft-anything-cli capabilities` is the live answer.
- The Codex adapter is unverified upstream and was not exercised here.

## 4. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                  # c316051c9e01e1bf9863f3c802a805179afa4663
grep -c '^- `' docs/tools.md                                   # 298
grep -oE '\(`[a-z]+`, [0-9]+\)' docs/tools.md | wc -l          # 17
grep -n 'MIN_TOOLS' crates/engine/src/tool_list.rs             # 271
grep -cE 'name: "' crates/mcp/src/prompts.rs                   # 6 prompts
grep -cE '^\| `' docs/file-formats.md                          # 12 versioned files
```
