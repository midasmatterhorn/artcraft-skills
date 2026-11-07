---
name: craft-anything
description: >-
  Craft Anything is ArtCraft's open-source, pure-Rust reverse-engineering and rebuilding workbench:
  point it at a website, desktop app, phone app, game or file, and it studies the original with real
  inspection tools (disassembler, decompiler, archives, browsers, databases, packet captures),
  has a coding agent (Claude Code first) build a new project in the stack you name, compares the
  result against the original at three screen widths or via the built program's own self-test, and
  refines until it matches. Trigger this skill whenever the user mentions Craft Anything (or
  `craft-anything-cli`, `craft.json`, `.cany`, "rebuild this website/app/game", "how does X work
  under the hood"), asks to inspect or reverse-engineer software they own, wants an agent-driven
  study→build→check pipeline, asks about its 301-tool engine, its MCP server, Clean room vs Deep
  mode, or its project folder layout — and equally when they never name it but describe the job
  ("figure out how this site is built", "make me a clone of this app", "disassemble this binary and
  tell me what it does"). Do not assume Ida-Pro-style or Ghidra-style behaviour: read this first.
---

# Craft Anything

**Audit basis.** Refreshed 2026-11-07 against tag **v0.5.0**, commit **`622d023cdfdb91c00df8b9a37c486a2a18fb0917`** — `git rev-parse HEAD` in the pinned checkout confirms, and the installed bundle matches (`Info.plist` `CFBundleShortVersionString` 0.5.0, bundle id `ai.storyteller.craft-anything`; its `craft-anything-cli --version` prints `craft-anything-cli 0.5.0`). The previous release this skill described was v0.3.0 (`e6280b5`).

**v0.3.0 → v0.5.0 delta.** 481 files changed in the tree diff. Engine tools 299 → **301** in the same 17 toolsets: `core` 34 → 35 (`core_finding_edit`) and `projects` 19 → 20 (`project_plan_fold`), with `MIN_TOOLS` still 271 (`docs/tools.md`; `crates/engine/src/tool_list.rs`). The installed `craft-anything-cli commands` lists **321** commands — the 20 AI/setup-layer tools on top (`rebuild_*`, `assets_key_*`, `ai_model*`, `setup_*`) — so 321 is not the engine count. MCP gained a shared-host mode: `mcp --restricted` drops and refuses machine-acting and network tools, `--allow-web` / `--allow-capture` re-enable those classes, and `--target` passes desktop target metadata (`apps/craft-anything-cli/src/main.rs`; `crates/mcp/src/lib.rs`). Coding-agent adapters went 3 → 6 — `copilot`, `dsh` (DeepSeek Harness) and `maki` joined `antigravity`, `hermes` and `opencode` (`crates/ai/src/cli_agents/adapters.rs`; `docs/copilot.md`, `docs/opencode.md`); Claude Code remains the first-class builder, README says only Maki among the ACP agents has been run live, and Codex is still unverified. New projects in Python, Go, .NET, Maven, Gradle and Make now build, test and launch through the same catalogue as Rust and Node.js (`crates/engine/src/toolchains.toml`, 8 toolchains; `docs/STATUS.md`). UI languages 5 → 15 (`crates/ui-egui/src/i18n.rs` `LANGUAGES`, `crates/ui-egui/src/i18n/*.tsv`). Versioned files grew to 12 rows with `inbox/build-progress.json`, `pin.json` version 2 and `feed.json` version 5 (`docs/file-formats.md`; `crates/engine/src/workspace/progress.rs`, `crates/engine/src/pins.rs`, `crates/engine/src/feed.rs`). Public installers are now published, and the README now states that Clean room is not an OS sandbox and that dependency installs run code.

**v0.2.0 → v0.3.0 delta.** 135 files changed. Engine tools 298 → **299** (the `projects` toolset 18 → 19). The macOS bundle **does** ship `craft-anything-cli` — the previous skill said it did not, and `packaging/macos/package.sh` copies, signs and version-checks it. CLI: `--build-with` and `--generate-assets` added, `--resume` requires `--continue-in` and ignores the request, `--rounds` defaults to 2. Repo docs are stale against the generated `docs/tools.md` (README says 314/298 at that tag).

v0.1.0 → v0.2.0: the **engine tool surface is unchanged** (299 tools / 17 toolsets, `docs/tools.md` byte-identical). The wave is in the **agent/AI layer**: an **OpenCode adapter** (`crates/ai/src/cli_agents/adapters/opencode.rs` — invokes `opencode run`, without `run` OpenCode reads its first argument as a folder to open), npm-installed coding agents start on Windows, local model servers (LM Studio et al.) accept the tools because boolean sub-schemas are sent as objects, failed agent runs are explained with a keepable log (`failure_log.rs`), the build activity feed shows what the build is doing now and how long it has been quiet (`crates/ai/src/rebuild/activity.rs`), **"Try again" resumes where a build stopped** (`crates/engine/src/journal.rs`), deadlocks are stopped as they form with a lock watchdog, crashing programs are named by their error instead of the last stack line, CJK scripts render in release builds (fonts and licences ship), a builder writing `/app/…` paths builds the app instead of being refused, `doctor` calls a local AI server reachable only when it answers with its models (and no longer offers another program squatting on the model-server port), agent checks that only probed the version say so, and the coding agent's cost is labelled an estimate. Claude Code remains the first-class, verified builder; Codex and OpenCode adapters exist but are unverified.

**Verify against your installed version** — the ArtCraft Launcher auto-updates, so a newer build may differ; every count quoted here was re-measured at this tag, and code paths that moved were re-cited. The measurement method for each count is in `evidence.md`.

## Overview

Craft Anything is "See how any website, app or game works, then have AI build your own version" — an open-source, clean-room engine in pure Rust by the ArtCraft/storytold project (`README.md`, MIT OR Apache-2.0). It works in four steps — **Study → Build → Check → Ready** — asking the person question/approval cards when a decision is theirs (`README.md` "How it works"). Two UI modes drive the same engine: **Simple** (a project page with the four steps) and the **Advanced** workbench (functions, pseudo-C, disassembly, hex, call graphs, evidence ledger, agent console). **Clean room** (default) inspects only what a visitor can see — screenshots, visible text, measured layout, colours, fonts — and refuses look-inside tools; **Deep** reads code and files with the built-in engines and Ghidra when installed (`README.md` "Clean room or Deep"; `crates/engine/src/tools/deep.rs`). Building needs a coding agent signed in on your machine — **Claude Code** is supported first (your own unmodified `claude`, your own sign-in); Codex, Copilot (ACP), OpenCode, DeepSeek Harness and other ACP agents are built but unverified — README says only Maki among the ACP agents has been run live (README "AI"; `docs/claude-code.md`, `docs/copilot.md`). **Status: early alpha** — website rebuilds with three-width checks and game rebuilds in Unity/Unreal/Godot work today; app/game behaviour checks are partial; some engine tools are tested only against stand-ins (`README.md` Status; `docs/STATUS.md`; `docs/tool-status.md`). Source: GitHub `storytold/craft-anything`.

## Capabilities (verified)

### One tool registry, three surfaces

- **301 engine tools in 17 toolsets** at this tag, generated into `docs/tools.md` by `cargo xtask tools` and kept honest by a test floor (`MIN_TOOLS = 271`, unchanged at v0.5.0; `crates/engine/src/tool_list.rs:9`). Each tool is simultaneously an **MCP tool**, a **CLI command** (`craft-anything-cli <id with dashes>`) and a callable tool for the coding agent; the AI and setup layers add 20 more on top (`rebuild_*` 9, `assets_key_*` 3, `ai_model*` 4, `setup_*` 4), so `craft-anything-cli commands` prints **321**, not 301. Toolsets: `core` 35, `native` 55, `apple` 14, `formats` 36, `managed` (.NET) 8, `android` 14, `java` 6, `adb` 24, `browser` 22, `javascript` 11, `runtime` 14, `frida` 9, `application` 17, `database` 1, `projects` 20, `setup` 9, `build` 6 (`docs/tools.md`). The README's "320 tools (300 in the engine)" is stale — trust the generated list.
- **Results are evidence, not answers**: every result carries confidence, coverage and limitations; big ones come back as a summary and page with `core_evidence_browse`. The discipline rules (predict-then-check, cite evidence ids, absence is not proof) are appended to every guided prompt (`crates/mcp/src/prompts.rs` `DISCIPLINE`).
- **MCP server** (`craft-anything-cli mcp`): stdio JSON-RPC; tools default to Essentials plus enabled toolsets, `--all-tools` lists everything; `--inbox DIR` posts `core_person_ask`/`core_action_approve` cards for the desktop app to answer; `--target <json>` takes desktop target metadata (`apps/craft-anything-cli/src/main.rs` `Mcp`). On a shared host use **`--restricted`**: it omits and refuses tools that act on the machine or reach the network, with `--allow-web` and `--allow-capture` to turn those classes back on (`crates/mcp/src/lib.rs` `restricted_refusal`). **6 guided prompts**, unchanged at v0.5.0 (`crates/mcp/src/prompts.rs` `PROMPTS`).
- **CLI subcommands** (`apps/craft-anything-cli/src/main.rs` `Command`): **12 named** — `mcp`, `setup`, `doctor`, `uninstall`, `commands`, `capabilities`, `triage <path>`, `report [--html] [--out] [--no-evidence]`, `chat`, `rebuild`, `ai`, and the hidden `builder-notes` hook (`--help` shows the first 11) — plus **`Tool(Vec<String>)` pass-through** so every engine tool id is a subcommand (the 12 named subcommands are unchanged at v0.5.0). Unknown flags are refused.
- **Rebuild from the terminal** (questions asked in the terminal): `craft-anything-cli rebuild <target|"-" for none> "<request>"` with `--rounds N` (default 2), `--backend`, `--unattended`, `--projects-dir`, `--project-folder` + `--existing edit|start-from`, `--continue-in` + `--resume`, `--deep` / `--clean-room` (`apps/craft-anything-cli/src/rebuild_cmd.rs`); this flag set is unchanged at v0.5.0.

### Study (the inspection engine)

- Its own pure-Rust **decoders, disassembler and decompiler** work without outside programs; Deep mode additionally uses **Ghidra** when installed (`README.md` "Under the hood"). Native programs (ELF/Mach-O/PE), .NET (incl. IL2CPP, bundles), Java (with decompilation), Android (adb, APK/AXML/ARSC signing), Apple (runtime, codesign, CAR), Electron (asar, fuse, runtime), JavaScript/JS bundles, websites (CDP browser automation), firmware, packet captures, databases, game archives — one toolset each (`crates/engine/src/tools/`, `crates/formats/src/`).
- External engines are optional and detected: Ghidra, Cutter, rizin, GDB, Frida, adb, jadx, JEB, tshark, apktool and CDP browsers (`crates/engines/src/`; `engines_*` tools in `docs/tools.md`); `craft-anything-cli doctor` checks the install, registrations, engines, AI backends and the MCP server.
- "Just look inside" opens a target for questions without building anything (Deep mode).

### Build, check, refine

- The builder is **your own Claude Code** (first-class; Codex adapter built but unverified). **GitHub Copilot** can be used through ACP after `copilot login`, and other ACP agents (Gemini CLI, Qwen Code, opencode, goose, Hermes, Maki) are switchable per backend — README says only Maki among them has been run live (`README.md` "AI"; `docs/copilot.md`, `docs/opencode.md`, `crates/ai/src/cli_agents/adapters.rs`). Craft Anything never sees your account; generated pictures and 3D models are opt-in with your own fal.ai key.
- **Checks**: websites are compared at three screen widths; games run the generated program's own `--self-test` against `checks/round-N/self-test.json`; app runs are compared; each round writes into `checks/` and the agent refines what doesn't match (`README.md` Status; `crates/engine/src/self_test.rs`; `docs/file-formats.md`). New projects in Python, Go, .NET, Maven, Gradle and Make are built, tested and launched from one catalogue (`crates/engine/src/toolchains.toml` — 8 toolchains with Rust and Node.js; `docs/STATUS.md` "New-project toolchains").
- **Plugins**: MCP servers, and WASM components in builds with the `wasm-plugins` option (`crates/engine/src/plugins.rs`; `crates/engines/src/wasm_plugin.rs`).

### Project folder and file formats (all versioned, migration steps on open)

- New projects go to `Documents/Craft Anything` (Settings → General) unless `--project-folder`. Layout: `craft.json` (request, target, status, history), `capture/`, `app/` (the generated project), `checks/`, `investigation.cany/` (evidence ledger), `inbox/` (open questions and `build-progress.json`) (`README.md` "Get started").
- Version constants in code: `craft.json` `MANIFEST_VERSION` **2** (`crates/engine/src/workspace.rs`), `config.toml` `SETTINGS_VERSION` **3** (`crates/engine/src/settings.rs`), `investigation.cany/project.toml` `FORMAT_VERSION` **1** (`crates/engine/src/project.rs`) — each with a compile-time assertion that the migration-step list has one step per version. The `docs/file-formats.md` table now has **12 rows**: the three constants above, `transcript.json`, `usage.json`, `questions.json`, `mechanics.json`, `standin.json` and `self-test.json` (all 1), plus `pin.json` **2** (`crates/engine/src/pins.rs`), `feed.json` **5** (`crates/engine/src/feed.rs`) and `inbox/build-progress.json` **1** (`crates/engine/src/workspace/progress.rs`). Newer files: `craft.json` = read-only, saving refused; `project.toml` = refused with "update Craft Anything"; `build-progress.json` = the build stops and leaves the record unchanged. **A newer file is never downgraded or overwritten.** ⚠️ **Repo-doc drift:** the same table still shows manifest 1 / settings 2 — it lags the constants (measured in code at v0.1.0, v0.3.0 and v0.5.0 alike); trust the constants.

## Known limitations and not-implemented

Do not assign these at v0.5.0:

- **Only Claude Code is the first-class, verified builder.** The Codex, Copilot and other ACP adapters are built but unverified; README says only Maki among the ACP agents has been run live (`README.md` "AI", "Status").
- **Behaviour checks for apps and games are partial**; website checks are the mature path.
- **Some engine tools are tested only against stand-ins** (`crates/engine/src/tools/standin_tools.rs`; `docs/tool-status.md` marks each tool).
- **Clean room is not an OS sandbox**: it is a rule about which tools Craft Anything offers and refuses. A coding agent you run still acts as you, with its own permissions (`README.md` "Clean room or Deep").
- **Installing dependencies runs code**: npm install scripts, Rust build scripts and Python source packages execute on your machine. Craft Anything asks before a command kind it has not seen in the project; "always allow" then covers every later command of that kind, so grant it only for trusted dependencies (`README.md` "Responsible use").
- The managed tier is still "next"; public installers are published, and the browser build is a viewer, not the full workbench (`apps/craft-anything-web`; `README.md` Status).
- It **never bypasses DRM, logins or anti-cheat**, and the builder is told not to copy logos/photos/text without confirmation of ownership — respect that when writing requests (`README.md` "Responsible use").

## How to operate

- GUI: `open -a "Craft Anything"`; the app binary is `Contents/MacOS/craft-anything`. **The macOS bundle ships `craft-anything-cli` beside it** (`Contents/MacOS/craft-anything-cli`, 0.5.0) — no separate install is needed on a launcher install; on another machine get it from the release assets or `cargo install --path apps/craft-anything-cli --locked`, and keep versions matched. Do not launch the GUI just to run a CLI command.
- Mode: switch Clean room/Deep in the title bar or Settings, `settings_set deep_mode true`, or `--deep`/`--clean-room` per CLI run.
- Typical agent flow:
  ```sh
  craft-anything-cli doctor                      # what's missing (agents, engines, AI)
  craft-anything-cli capabilities                # toolsets, availability, engines
  craft-anything-cli triage ./target.bin         # first look, evidence records
  craft-anything-cli rebuild https://example.com "Recreate this website" --rounds 2
  craft-anything-cli rebuild - "A snake game in Rust"
  craft-anything-cli rebuild https://example.com "Make the header blue" --continue-in "<folder>"
  craft-anything-cli report --out report.md      # readable report from the ledger
  ```
- Settings live in `config.toml` (`engine::settings::config_dir()`, version 3); `LIGHTCRAFT`-style env overrides are not a thing here — check `craft-anything-cli doctor` output for paths.

## Working with an AI agent

- **You are also the builder Craft Anything drives.** When its coding-agent bridge launches you, read the inbox/notes flow: the person's answers arrive via the `builder-notes` hook; approval-required actions go through `core_action_approve` rather than being assumed.
- **Study first, honestly**: keep the investigation memory current (`core_investigation_show`, `core_brief_write`, `core_plan_update`, `core_hypothesis_record`, `core_finding_record`, `core_handoff_write`) — the MCP prompts enforce this discipline and it makes your answers auditable.
- **Respect the mode.** In Clean room the look-inside tools refuse; don't try to work around them. Switching to Deep is the person's decision.
- **Prepare inputs** in formats the toolsets open (archives, binaries, captures, DB dumps); use `core_archive_extract` rather than shelling out, so evidence lands in the ledger.
- **Verify rebuilds** from `checks/` outputs and the per-round comparison reports; a "Ready" step is a claim — open the result and re-check before telling the person it matches.
- **What not to attempt:** bypassing DRM/logins/anti-tamper (refused by design), promising Codex/Copilot builds, editing `craft.json`/`.cany` by hand while a run is active, quoting the README's 320-tool number, assuming Ghidra is present (check `doctor`), or serving MCP to a shared host without `--restricted`.

## Verification protocol

1. **Round-trip on a throwaway target first**: rebuild a tiny known website with `--rounds 1`, then read `craft.json`, `checks/round-1/` and `app/` before real work.
2. **Cite evidence ids** for every claim about the original; absence is not proof.
3. **Version your project folders** (copy the whole folder; every file carries a version and a newer file refuses saves).
4. **One project per run**: never edit a project folder while a rebuild is active; `--resume` exists for continuation.
5. **Update between projects**: this skill is pinned to v0.5.0; re-run `doctor` after updates.

## Sources & evidence

- Repo: https://github.com/storytold/craft-anything — inspected at tag **v0.5.0**, commit `622d023cdfdb91c00df8b9a37c486a2a18fb0917` ("Release 0.5.0", 2026-11-06), inspection date **2026-11-07**; the previous tag v0.3.0 (`e6280b5dc518b9f3266c82d794a4e2f0367d9a53`) was diffed against it for the delta. Apache-2.0 and MIT (`LICENSE-APACHE`/`LICENSE-MIT`).
- Installed `/Applications/Craft Anything.app`: `CFBundleShortVersionString` 0.5.0, `CFBundleIdentifier` `ai.storyteller.craft-anything`; the bundled `craft-anything-cli --version` prints `craft-anything-cli 0.5.0`. The GUI was never launched and the app binary was not executed.
- Read: `README.md`, `Cargo.toml`, `docs/{tools,STATUS,tool-status,claude-code,copilot,opencode,file-formats,pitfalls,extending,tool-ids,localization}.md`, `apps/craft-anything-cli/src/{main,rebuild_cmd,setup_cmd,ai_cmd}.rs`, `crates/engine/src/{tool_list,registry,project,settings,self_test,plugins,pins,feed,workspace,versioned}.rs`, `crates/engine/src/workspace/progress.rs`, `crates/engine/src/toolchains.toml`, `crates/engine/src/tools/` (list), `crates/mcp/src/{lib,prompts}.rs`, `crates/ai/src/cli_agents/adapters.rs` and its adapters, `crates/ui-egui/src/i18n.rs`, `crates/engines/src/` (list), `crates/formats/src/` (list).
- Counts recomputed from source at v0.5.0: **301 engine tools in 17 toolsets** (`docs/tools.md` generated list, 301 ids; `MIN_TOOLS = 271`), **321 `commands` entries** (301 + 20 AI/setup extras), 6 MCP prompts (unchanged at v0.5.0), **12 named CLI subcommands** (unchanged at v0.5.0) + hidden/external pass-through, **12 versioned-file rows** in `docs/file-formats.md`, **15 UI languages** (`LANGUAGES` in `crates/ui-egui/src/i18n.rs`), 8 toolchains in `crates/engine/src/toolchains.toml`; version constants from code: `MANIFEST_VERSION`/`FORMAT_VERSION`/`SETTINGS_VERSION` = 2/1/3 (⚠️ `docs/file-formats.md`'s table still shows manifest 1 / settings 2 — stale repo doc).
- Workspace: 13 crates (`ai`, `analysis`, `disasm`, `engine`, `engines`, `evidence`, `formats`, `js`, `mcp`, `platform`, `setup`, `testkit`, `ui-egui`) + 3 apps (desktop, CLI, web), unchanged at v0.5.0.
- Evidence table: `evidence.md` next to this file.
