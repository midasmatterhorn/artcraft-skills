# Craft Anything — evidence ledger (tag v0.5.0)

Audit basis: this checkout is tag **`v0.5.0`**, commit **`622d023cdfdb91c00df8b9a37c486a2a18fb0917`**
("Release 0.5.0", 2026-11-06; shallow clone of the release tag). Inspection date **2026-11-07**; the
previous tag **`v0.3.0`** = `e6280b5dc518b9f3266c82d794a4e2f0367d9a53` was the other shallow root,
diffed for the delta. The installed bundle is 0.5.0 (`CFBundleIdentifier`
`ai.storyteller.craft-anything`); its bundled `craft-anything-cli --version` prints
`craft-anything-cli 0.5.0`; the GUI was never launched.

v0.3.0 → v0.5.0 delta (tree diff, 481 files): engine tools **299 → 301** in the same 17 toolsets
(`core` 34 → 35 for `core_finding_edit`; `projects` 19 → 20 for `project_plan_fold`). A shared-host
MCP mode (`mcp --restricted`, with `--allow-web`/`--allow-capture`, plus `--target`) was added.
Coding-agent adapters grew 3 → 6 (`copilot`, `dsh`, `maki` added). New-project toolchains landed
(`crates/engine/src/toolchains.toml`, 8 entries; the file was absent at v0.3.0). UI languages 5 → 15.
Versioned files 11 → 12 rows (`inbox/build-progress.json` added; `pin.json` 2, `feed.json` 5).
**Doc drift, corrected here:** README's banner now says "320 tools (300 in the engine)" against 301 in
the generated list; `docs/file-formats.md`'s table still shows manifest 1 / settings 2 while the code
constants are 2 / 3 (unchanged drift from the previous two audits).

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 301 engine tools in 17 toolsets; each an MCP tool + CLI command | `docs/tools.md` (generated, 301 tool rows); `crates/engine/src/tool_list.rs` `MIN_TOOLS = 271` and `report()` | implemented |
| 2 | Toolsets and sizes | `docs/tools.md` section headers: core 35, native 55, apple 14, formats 36, managed 8, android 14, java 6, adb 24, browser 22, javascript 11, runtime 14, frida 9, application 17, database 1, projects 20, setup 9, build 6 | implemented |
| 3 | README's "320 tools (300 in the engine)" is stale | README "Agent-ready" / "Under the hood" vs generated `docs/tools.md` 301 | doc drift |
| 4 | MCP server: Essentials + enabled toolsets, `--all-tools`, `--inbox`, `--target`; shared-host `--restricted` with `--allow-web`/`--allow-capture` | `apps/craft-anything-cli/src/main.rs` `Command::Mcp`; `crates/mcp/src/lib.rs` `restricted_refusal` | implemented |
| 5 | 6 guided MCP prompts with discipline rules | `crates/mcp/src/prompts.rs` `PROMPTS` (6 entries), `DISCIPLINE` (6 rules) — unchanged | implemented |
| 6 | CLI subcommands incl. tool pass-through | `apps/craft-anything-cli/src/main.rs` `Command` (12 named + hidden `builder-notes` + `Tool(Vec<String>)`); installed `commands` prints 321 = 301 engine + 20 AI/setup extras | implemented |
| 7 | `rebuild` flags: rounds default 2, backend, unattended, project-folder, continue-in/resume, deep/clean-room, build-with, generate-assets | `apps/craft-anything-cli/src/rebuild_cmd.rs` `RebuildArgs` — unchanged | implemented |
| 8 | Clean room vs Deep; deep refuses look-inside in Clean room; Clean room is a tool rule, not an OS sandbox | `README.md` "Clean room or Deep"; `crates/engine/src/tools/deep.rs`; `crates/engine/src/clean_room.rs` | implemented |
| 9 | Claude Code first-class builder; ACP/Copilot/Codex/OpenCode/DeepSeek Harness adapters built but unverified (Maki run live per README) | `README.md` "AI"; `docs/claude-code.md`, `docs/copilot.md`, `docs/opencode.md`; `crates/ai/src/cli_agents/adapters.rs` (6 adapters) | implemented / partial (non-Claude builders) |
| 10 | Versioned project files; newer files never downgraded | `docs/file-formats.md` table (12 rows); `crates/engine/src/versioned.rs` | implemented |
| 11 | Version constants: manifest 2, settings 3, .cany 1 (code; docs table stale) | `crates/engine/src/workspace.rs:81`, `crates/engine/src/settings.rs:222`, `crates/engine/src/project.rs:22`; `crates/engine/src/pins.rs:37` (2), `crates/engine/src/feed.rs:19` (5), `crates/engine/src/workspace/progress.rs:21` (1) | implemented |
| 12 | External engines detected (Ghidra, Cutter, rizin, GDB, Frida, adb, jadx, JEB, tshark, apktool, CDP) | `crates/engines/src/` modules; `engines_*` tools in `docs/tools.md`; `doctor` command — unchanged | implemented |
| 13 | macOS bundle ships `craft-anything-cli` | bundle `Contents/MacOS/` listing (two executables); `craft-anything-cli --version` → 0.5.0 | verified present |
| 14 | No DRM/login/anti-cheat bypass; dependency installs run code and are consent-gated | `README.md` "Responsible use" | policy (by design) |
| 15 | v0.5.0 agent layer: restricted MCP mode, new Copilot/DSH/Maki adapters, model tools (`ai_models_list`, `ai_model_set`), 8 project toolchains, 15 UI languages | `crates/mcp/src/lib.rs`; `crates/ai/src/{model_tools,providers}.rs`; `crates/engine/src/toolchains.toml`; `crates/ui-egui/src/i18n.rs` | implemented |

## 2. Counts

| Surface | v0.3.0 (measured) | v0.5.0 (measured) |
|---|---:|---:|
| Engine tools / toolsets | 299 / 17 | **301 / 17** |
| Tool floor `MIN_TOOLS` | 271 | 271 (unchanged) |
| MCP prompts | 6 | 6 (unchanged) |
| CLI `commands` entries | not captured | 321 (301 engine + 20 AI/setup) |
| Named CLI subcommands | 12 | 12 (unchanged) |
| Versioned file formats (doc rows) | 11 | **12** |
| UI languages (`LANGUAGES`) | 5 | **15** |
| Project toolchains | 0 (file absent) | **8** |
| Coding-agent adapters | 3 | **6** |
| Workspace crates / apps | 13 / 3 | 13 / 3 (unchanged) |

## 3. Uncertain / not verified

- GUI behaviour never launched; Simple/Advanced workbench claims come from README + screenshots
  (`docs/images/`) + the UI crate layout.
- Tool-level availability on this machine (which toolsets light up) depends on installed engines;
  `craft-anything-cli capabilities` is the live answer.
- Codex, Copilot and the other ACP adapters were not exercised here; their live status is the
  README's claim, not a measurement.

## 4. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                  # 622d023cdfdb91c00df8b9a37c486a2a18fb0917
grep -c '^- `' docs/tools.md                                   # 301
grep -oE '\(`[a-z]+`, [0-9]+\)' docs/tools.md | wc -l          # 17
grep -n 'MIN_TOOLS' crates/engine/src/tool_list.rs             # 271
grep -cE 'name: "' crates/mcp/src/prompts.rs                   # 6 prompts
grep -cE '^\| `' docs/file-formats.md                          # 12 versioned files
grep -cE 'LangInfo \{ code:' crates/ui-egui/src/i18n.rs        # 15 UI languages
grep -c '\[\[toolchain\]\]' crates/engine/src/toolchains.toml  # 8 toolchains
<installed bundle>/Contents/MacOS/craft-anything-cli commands | jq 'length'   # 321
grep -n 'pub const MANIFEST_VERSION' crates/engine/src/workspace.rs   # 2
grep -n 'pub const SETTINGS_VERSION' crates/engine/src/settings.rs    # 3
grep -n 'pub const FORMAT_VERSION' crates/engine/src/project.rs       # 1
```

## Round 2026-11-04 (refresh)

- Pinned to `v0.3.0` = `e6280b5dc518b9f3266c82d794a4e2f0367d9a53` (installed `craft-anything 0.3.0`).
- Engine tools 298 → **299** (`projects` 18 → 19). The macOS bundle does ship `craft-anything-cli` — corrected.
- Id sets were diffed between the two tags with the same extraction method as the claims above; counts here are the new ones.

## Round 2026-11-07 (pin-and-verify refresh to v0.5.0)

- Re-pinned to `v0.5.0` = `622d023cdfdb91c00df8b9a37c486a2a18fb0917`; installed bundle 0.5.0, bundled CLI `craft-anything-cli 0.5.0` (read-only `--version`/`--help`/`commands`; GUI not launched).
- **Re-measured:** 301 tool ids in `docs/tools.md` and 17 toolsets (heading counts); 321 entries from the installed CLI's `commands` JSON, with the 20 extras (`rebuild_*` 9, `assets_key_*` 3, `ai_model*` 4, `setup_*` 4) diffed against the generated list; 6 prompts; 13 `Command` variants (12 named + the external tool pass-through); 12 format rows; 15 `LANGUAGES` entries; 8 toolchains; 13 crates + 3 apps. Constants re-read from source: 2 / 3 / 1 plus pin 2, feed 5, build-progress 1.
- **Unchanged at v0.5.0:** 17 toolsets, `MIN_TOOLS` 271, 6 MCP prompts, 12 named CLI subcommands, 13 crates / 3 apps, the `rebuild` flag set and defaults, the three-width website check, game self-test and app-run comparison model, 11 of the 12 versioned-file rows.
- **Corrected:** CLI subcommands had been described as "13 named"; the bundle's CLI presence had been corrected in prose but contradicted later in "How to operate"; `config.toml` settings version had been given as 2 in one place (3 is correct); README tool numbers are now 320/300 against 301, and the old `craftanything` clone-URL claim no longer applies.
- **Path check:** every repo-relative path cited in `SKILL.md`/`evidence.md` was re-resolved against the clone; all exist. `packaging/macos/package.sh`, `crates/engine/src/tools/standin_tools.rs`, `crates/mcp/src/{lib,prompts}.rs`, `crates/ai/src/cli_agents/adapters.rs` and `crates/ui-egui/src/i18n.rs` were confirmed at the new tag.
