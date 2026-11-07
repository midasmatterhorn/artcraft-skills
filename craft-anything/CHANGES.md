# Craft Anything — round 2026-11-07 changes

Re-pinned: v0.3.0 (`e6280b5`) -> v0.5.0 (`622d023`, installed `craft-anything-cli 0.5.0`).

## Corrected / re-measured

- Engine tools 299 -> **301** (17 toolsets unchanged): `core` 34 -> 35 (`core_finding_edit`), `projects` 19 -> 20 (`project_plan_fold`). `MIN_TOOLS` stays 271.
- The installed CLI's `commands` list is **321**, not 301: 20 AI/setup-layer tools ride on top (`rebuild_*` 9, `assets_key_*` 3, `ai_model*` 4, `setup_*` 4). The generated `docs/tools.md` lists 301 engine tools and says the AI/setup layers add their own on top; the old skill implied the CLI list and the engine count were the same.
- README tool numbers moved but are still stale: 314/298 -> **320/300**, against **301** in the generated list. Quote 301.
- MCP server gained a shared-host mode: `mcp --restricted` removes and refuses machine-acting and network tools; `--allow-web` / `--allow-capture` turn those classes back on; `--target` shares desktop target metadata.
- Coding-agent adapters 3 -> **6** (`copilot`, `dsh` for DeepSeek Harness, `maki` added; `antigravity`, `hermes`, `opencode` kept). Claude Code is still the first-class builder; README says only Maki among the ACP agents has been run live; Codex is still unverified.
- UI languages 5 -> **15** (`crates/ui-egui/src/i18n.rs` `LANGUAGES`; 10 new catalogs under `crates/ui-egui/src/i18n/`).
- Versioned files: `docs/file-formats.md` table 11 -> **12** rows (`inbox/build-progress.json` added); `pin.json` is now version 2 and `feed.json` version 5. `craft.json` 2, `config.toml` 3, `project.toml` 1 still stand; the doc's manifest 1 / settings 2 row is still stale.
- CLI named subcommands: corrected to **12** (11 shown by `--help` plus hidden `builder-notes`) plus the external tool pass-through. The old skill said 13 named.
- The macOS bundle **does** ship `craft-anything-cli` (re-confirmed; `--version` prints `craft-anything-cli 0.5.0`). The old "How to operate" line still claimed it did not.
- `config.toml` settings version corrected to **3** in "How to operate" (it said 2 there but 3 in the formats section).
- Removed the stale claim that README's clone URL says `craftanything`; it has said `storytold/craft-anything` since v0.3.0.
- New at v0.5.0: new projects in Python, Go, .NET, Maven, Gradle, Make (plus Rust and Node.js) build and run from `crates/engine/src/toolchains.toml` (8 toolchains). Public installers are now published, so "first public release is next" was removed.
- Added the README's Clean room caveat (a rule about what is offered, not an OS sandbox) and the dependency-install consent caveat.

## Method

- `git rev-parse HEAD` in the pinned checkout: `622d023cdfdb91c00df8b9a37c486a2a18fb0917`; tag `v0.5.0`. Tree diff `v0.3.0..HEAD`: **481 files changed**, +117215/-3544. The round context's "300 files" is an API file-list cap, not a tree measurement; the checkout's history is shallow, so no commit count is derived locally.
- Tool ids: `grep -c '^- \`' docs/tools.md` = 301 and the id set diffed against the installed CLI's `craft-anything-cli commands` JSON (`jq -r '.[].tool'`) = 321, with the 20 extras listed above. Toolset sizes from the generated `docs/tools.md` heading counts.
- `grep -cE 'name: "' crates/mcp/src/prompts.rs` = 6; `Command` enum in `apps/craft-anything-cli/src/main.rs` = 12 named + `Tool`; `LANGUAGES` entries in `crates/ui-egui/src/i18n.rs` = 15; `grep -cE '^\| \`' docs/file-formats.md` = 12.
- Installed bundle inspected read-only: `Info.plist` 0.5.0 / `ai.storyteller.craft-anything`, `Contents/MacOS/` listing, `craft-anything-cli --version` and `--help`. The GUI was never launched and the app binary was not executed.
- Every repo-relative path cited in the skill was re-checked with a loop over the clone; all resolve. `apps/craft-anything-cli/src/main.rs`, `crates/mcp/src/lib.rs`, `crates/engine/src/{workspace,settings,project,pins,feed}.rs`, `crates/engine/src/workspace/progress.rs`, `crates/ui-egui/src/i18n.rs`, `crates/ai/src/cli_agents/adapters.rs`, `crates/engine/src/toolchains.toml` were read at the new tag.

## Unchanged

- 17 toolsets; `MIN_TOOLS` = 271; 6 MCP prompts; 13 crates + 3 apps; workspace layout; `rebuild` flags and their defaults (`--rounds` 2, `--continue-in`/`--resume`, `--build-with`, `--generate-assets`); version constants `MANIFEST_VERSION` = 2, `SETTINGS_VERSION` = 3, `FORMAT_VERSION` = 1; the website three-width / game self-test / app-run check model; 11 of the 12 versioned-file rows.
- The v0.2.0 -> v0.3.0 and v0.1.0 -> v0.2.0 delta paragraphs were kept as the two most recent historical deltas; nothing in the code contradicts them.

## Known gap in this round

- Pin-and-verify, not a fresh deep audit: the prose was not re-derived for every one of the 301 tools. Tool-level availability on a given machine still depends on installed engines (`craft-anything-cli capabilities` is the live answer), and the GUI was not launched, so Simple/Advanced UI behaviour is documented from code and README only.
