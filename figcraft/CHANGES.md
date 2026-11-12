# FigCraft — round 2026-11-12 changes

Re-pinned: v0.16.0 (`f45b261`) -> **v0.18.1** (`4acc293c2ec9`, installed `FigCraft 0.18.1 (4acc293c2ec941ac1400837ee7e3ab51780399f8)`).

## Corrected / re-measured

- `spec!` command registrations 637 -> **646** engine-wide, 488 -> **493** in
  `crates/engine/src/cmd/`; **641 distinct literal ids**. Nine ids are new, **none removed**:
  `board.mindMap`, `board.mindMapAdd`, `collab.reconnect`, `selection.createColorStyle`,
  `text.direction`, `text.directionAuto`, `text.directionLtr`, `text.directionRtl`, `tool.crosshair`.
- **`board.*` 21 -> 23** (mind maps), **`collab.*` 21 -> 22** (`collab.reconnect`), **locales 24 ->
  25** (`zh-Hant` added).
- Menu breadth: `docs/parity-checklist.md` still says **212 / 212** but was generated 2026-10-21,
  before `Text ▸ Text direction`; a static count of `catalog::MENU` minus `OWN`/`collab.*` at this
  tag gives **214** items (the new Text direction rows add two counted items; `text.directionAuto` is in `OWN`).
  Four ids (`object.rotate180`, `view.zoom50|100|200`) are not literal `spec!` ids and may be
  const-built — re-run `cargo xtask parity` in a build to confirm.
- Shortcut rows **136 documented / 135 bound** (`docs/ui-parity.md`), not the baseline's 129/128.
  Keymap stays **163** `k(` binding rows in **12** groups, with **47** gesture rows.
- Example plugins are **four** (`counter`, `export-names`, `swatch-grid`, `tidy-names`), not three.
  The previous skill and `docs/architecture.md` ("two") were both wrong.
- `MAX_UNPACKED` is **6 GiB** on 64-bit and **2 GiB** on 32-bit (per-open total, unchanged since
  v0.16.0). The baseline's "4 GiB/1 GiB unpacked" was really `MAX_DOCUMENT`.
- Control methods: **17** by the app (16 `handle()` arms + `ui.screenshot`). `events.poll` remains
  documented (18 sections) but only the MCP bridge implements it; the app answers `unknown method`.
- MCP **19** tools, **3 + 2** resources/templates, **4** prompts; CLI **10** subcommands; plugin
  **API 6** — all unchanged sets, verified by diffing the id sets between the two tags.
- New capability text this round: mind maps (step 1, command-only), per-paragraph text direction,
  Selection colors' `selection.createColorStyle` and library rows, Suggest auto layout's nested
  frames, the placement crosshair, export `colorProfile`/`quality`, `.fig` Scale-tool instance
  fixes, the Developer Mode rename, the `craft-web-api` page API, `collab.reconnect` pacing, and
  Penpot 2.x import/export (previously present but not described in the skill).
- `agents/openai.yaml` short description now names prototyping and boards (mind maps) and drops the
  comparative "Figma-style" wording for the app's own "interface design tool" phrasing
  (`docs/feature-names.md`); the display name is unchanged.

## Method

- 448 files changed, +22,803/-1,969, from `git diff v0.16.0..HEAD` in the pinned checkout
  (HEAD `4acc293c2ec941ac1400837ee7e3ab51780399f8` = tag `v0.18.1`; the shallow clone holds one
  squashed commit between the tags).
- Counts re-extracted with the greps recorded in `evidence.md` §5, then run again at `v0.16.0`
  (`git show`, `git grep`, `git ls-tree`) to separate round drift from baseline error. Id sets
  (command literals, `board.*`, `collab.*`, locales, MCP tools, CLI verbs, plugin API) were diffed
  between the tags.
- Installed bundle read only through `Info.plist` (`CFBundleShortVersionString 0.18.1`,
  `CFBundleIdentifier ai.storyteller.figcraft`) and a `--version` run that prints and returns
  before creating a window. The GUI was never launched; the bundle carries no CLI.
- Every repo-relative path cited in `SKILL.md` and `evidence.md` was re-resolved against the clone;
  moved or vanished paths were fixed or the claim was dropped.
- Delta facts were taken from the code diff and the repo's own parity documents, never from the
  release notes (which were used only to know where to look).

## Unchanged

- CLI 10 verbs (incl. `connect publish`, `plugin publish`, `perf`), MCP 19 tools, 3 resources + 2
  templates + 4 prompts, control 17 methods, plugin API 6, keymap 163 bindings, 8 design templates,
  5 board templates, 5 example documents, `.figcraft` format/version and member layout.
- Parity headline in `docs/target-app-parity.md`: 212/212 (stale total), feature breadth ~85%
  (core ~94%), ready ~53%, essentials ~59%, mainstream ~50%.
- Prototype counts (10 triggers, 11 actions, 8 transitions, 13 easings/springs), Developer Mode code
  targets, boards' non-mind-map command set, `.fig` export surface.
- Verification-protocol steps carried forward; each was path-checked at this tag and none was
  silently re-dated.

## Known gap in this round

- Pin-and-verify refresh, not a new deep audit: the GUI was not exercised, no build or CLI run was
  permitted, and `.fig`/`.jam`/`.sketch`/REST/Penpot fidelity remains best-effort and unproven
  against real files. The menu total and the four unmatched view/zoom ids need a `cargo xtask
  parity` run to settle. The public `figcraft-server` deployment path (`packaging/server/`) was
  noted but not exercised.
