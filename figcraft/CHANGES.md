# FigCraft — round 2026-11-07 changes

Re-pinned: v0.15.0 (`02c38a6`) -> v0.16.0 (`f45b261`, installed `FigCraft 0.16.0 (f45b261687880e56d1bad11ec82b45131e57ef8b)`).

## Corrected / re-measured

- `spec!(` command registrations 636 -> **637** engine-wide, 487 -> **488** in `crates/engine/src/cmd/`; the one net new id is **`text.wrapStyle`** (`auto|balance|pretty`), the only added `spec!(` line in the `v0.15.0..v0.16.0` engine diff. The published skill said 630 / 481; that was stale — the same grep at `v0.15.0` already gives 636 / 487.
- Keymap bindings **163** (baseline said 159) — the baseline figure was stale; `crates/engine/src/keymap.rs` is byte-identical at v0.15.0 and v0.16.0. Unchanged at v0.16.0.
- Control methods **17**, not 18: 16 match arms in `crates/ui-egui/src/control.rs::handle` plus `ui.screenshot`, routed in `route_queued`. `events.poll` is documented in `docs/control-protocol.md` but only the MCP headless bridge implements it (`crates/mcp/src/headless.rs`); the app channel answers `unknown method`.
- MCP tools **19**, set unchanged (`crates/mcp/src/tools.rs` `TOOL_NAMES` identical at both tags); the baseline prose listed only 18 and omitted `wait_for_changes`. Resources are **3** (`document`, `commands`, `comments`) + 2 templates, not 2 + 2 (`crates/mcp/src/resources.rs`).
- `board.*` commands **21**, not 19: the baseline list counted `board.editText` (a UI request, not a command) and missed `board.label`, `board.templates`, plus the newer `board.addConnected`, `board.grid` and `board.reshape`. Set unchanged at v0.16.0.
- Locale catalogs **24** (baseline limitation said 22) — unchanged at v0.16.0, `crates/ui-egui/locales/` identical at both tags.
- Plugin API is **6**, not 4 (`crates/plugin/src/manifest.rs` `API_VERSION: u32 = 6`, identical at both tags): widgets gained fields/property menus at 4, panel opening at 5, line/SVG drawing at 6 (`docs/plugins.md`).
- CLI **10** subcommands and locales/keymap/board set all **unchanged at v0.16.0**.

## Method

- 133 files changed, +4156/-545, from `git diff v0.15.0..HEAD` in the pinned clone (HEAD `f45b261687880e56d1bad11ec82b45131e57ef8b` = tag `v0.16.0`).
- Counts re-extracted with the same greps as the published `evidence.md`, then run again at `v0.15.0` (`git show v0.15.0:<path>`, `git grep`) to separate round drift from baseline error. Id sets (MCP tools, `board.*`, `collab.*`, locales) diffed between the two tags — all empty.
- Installed bundle read only through `Contents/Info.plist` (`CFBundleShortVersionString 0.16.0`, `CFBundleIdentifier ai.storyteller.figcraft`) and the recorded `--version` string; the GUI was never launched and the bundle carries no CLI.
- Every repo-relative path cited in `SKILL.md` re-resolved against the clone; no cited path moved or vanished, so none was re-cited.

## Unchanged

- Automation-surface shapes: CLI 10 verbs (incl. `connect publish`), MCP 19 tools, MCP 3 resources + 2 templates + 4 prompts, control 17 methods, plugin API 6, 24 locales, 163 keymap bindings, 212/212 menu items, 8 design templates, 5 board templates, 5 examples, 3 example plugins, `.figcraft` format/version bounds.
- Parity headline in `docs/target-app-parity.md`: 212/212 menu items, feature breadth ~85% (core ~94%), ready ~53%.
- Verification-protocol steps carried forward; they were path-checked at this tag, and no claim was silently re-dated.

## Known gap in this round

- Pin-and-verify refresh, not a new deep audit: GUI behaviour was not exercised, and `.fig`/`.sketch`/REST/Penpot fidelity remains best-effort and unproven against real files. The `.penpot` archive path (`crates/format/src/penpot.rs`, `figcraft-cli export --format penpot`) is real but was not re-audited this round; it is not yet described in `SKILL.md`.
