# AniCraft — round 2026-11-12 changes

**First audit.** No AniCraft skill existed before this round, so nothing was re-pinned from an
older skill: this skill is authored at **AniCraft v0.2.1**, commit
`d0beaf253274948b55ee9e1107749f9491bff880` (tag `v0.2.1`, released 2026-11-12), inspected
2026-11-12. The installed bundle is **AniCraft 0.2.1** (`ai.storyteller.anicraft`);
`AniCraft --version` prints `AniCraft 0.2.1 (early alpha)` and the bundled
`anicraft-cli --version` prints `anicraft-cli 0.2.1`. It supersedes no prior skill; the app
release it follows is 0.2.0.

## Corrected / re-measured

All headline numbers are new (there was no previous skill to carry forward). Re-measured at the
tag, on 2026-11-12:

* **Engine commands: 240** in **33 namespaces**, of which **52** carry a default shortcut and
  **165** mutate the document. Read live from `anicraft-cli commands` (JSON), and backed by the
  registry at `crates/engine/src/lib.rs` (`commands()`, 35 `specs()` groups). The GUI About box
  also prints the registry length (`src/app.rs`).
* **MCP tools: 5** (`anicraft_commands`, `anicraft_run`, `anicraft_run_script`,
  `anicraft_document`, `anicraft_render`) over **3 protocol revisions** (2025-06-18, 2025-03-26,
  2024-11-05). Confirmed by a live `initialize` + `tools/list` handshake against the installed
  server, and by `crates/cli/src/mcp.rs`.
* **CLI subcommands: 11** (`info`, `render`, `render-seq`, `gif`, `commands`, `run`, `exec`,
  `new`, `bench`, `serve`, `mcp`) plus the `help`/`--version` aliases. Source:
  `crates/cli/src/lib.rs` `USAGE` and `run()`. The README workspace map lists only nine and is
  stale.
* **Publish formats: 9** (`html`, `gif`, `video`, `lottie`, `sprite_sheet`, `png_sequence`,
  `png`, `svg`, `audio`) from `crates/doc/src/publish.rs` `PublishFormat::ALL`.
* **Filter kinds: 7** (Blur, Drop Shadow, Glow, Bevel, Gradient Glow, Gradient Bevel,
  Adjust Color) from `crates/doc/src/filter.rs`.
* **Blend modes: 14** from `crates/doc/src/lib.rs` `BlendMode`.
* **Colour-effect styles: 5 including None** (Brightness, Tint, Advanced, Alpha) from
  `crates/doc/src/color_effect.rs`.
* **Easing presets: 8** plus the Classic slider and arbitrary cubic Bézier
  (`crates/doc/src/easing.rs` `Easing::PRESETS`).
* **Native format: version 3**, which also opens v1 and v2 documents and refuses newer ones
  (`crates/engine/src/format.rs`).
* **Crates: 13**, not the 9 listed in the README workspace map; the map omits `actions`,
  `audio`, `gpu` and `plugins`.
* **ADRs: 59** files (`0001`–`0060`, with `0037` reserved in `docs/adr/README.md`).
* **Tests: 1,088 `#[test]` functions** across the workspace by grep. `docs/roadmap.md` still
  says "133 tests" — stale by roughly an order of magnitude.
* **Localisation:** the shell has keyed `tr!`/`trn!` strings, a pseudo-locale and **35 locale
  codes marked ready** (`src/i18n/mod.rs` `READY`), but no AniCraft catalog is shipped, so the
  0.2.1 release is English-only. The skill says so rather than claiming 35 languages.
* **Import/export matrix** re-derived from command params and extension checks, not README
  prose: open `.anicraft`, `.fla`, `.xfl`; import `.svg`, `.png`, `.jpg`/`.jpeg`, `.wav`,
  `.ogg`, `.mp3`; export PNG, PNG sequence, SVG, GIF, sprite sheet + JSON, Lottie, self-contained
  HTML canvas, MP4/WebM through the user's ffmpeg, and WAV.

Doc drift recorded (details in `evidence.md`):

* README "What's missing" still lists **audio layers** and **a GPU renderer**; both exist
  (`crates/audio`, `crates/gpu`, with `gpu-stage` on by default in `Cargo.toml`).
* README's workspace map omits `actions`, `audio`, `gpu` and `plugins`, and its CLI line omits
  `gif` and `bench`.
* `docs/roadmap.md` "Tests: 133" is stale against 1,088 `#[test]` functions.
* `docs/requirements.md` lists SWF export as optional; `docs/roadmap.md` says SWF bytecode is
  not planned and no code implements it. Treated as **not implemented**.
* `docs/roadmap.md`'s interactivity row still says "Not yet: … keyboard events, variables" while
  ADR 0052 and `crates/actions/src/as3` implement variables and keyboard listeners. The
  roadmap clause is stale; the skill follows the code.

## Method

* Pinned the checkout: `git rev-parse HEAD` → `d0beaf253274948b55ee9e1107749f9491bff880`,
  `git tag --points-at HEAD` → `v0.2.1`, clean worktree.
* Read the repo brief, addendum, context file and AGENTS.md; then the README, `docs/roadmap.md`,
  `docs/mcp.md`, `docs/plugins.md`, `docs/web.md`, `docs/localisation.md`,
  `docs/accessibility.md`, and ADRs 0004, 0016, 0019, 0024, 0028, 0036, 0040, 0052, 0054, 0055,
  0056, 0057, 0058, 0059, 0060 where the release delta points.
* Re-measured counts from the installed, read-only CLI where one exists: `anicraft-cli
  --version`, `anicraft-cli --help`, `anicraft-cli commands` (JSON), `anicraft-cli info
  --sample`, and an MCP `initialize` + `tools/list` exchange on stdin. No GUI launch.
* Counted enum variants and `ALL` arrays in source for filters, blend modes, colour styles,
  publish formats and easing presets; counted `#[test]` attributes, ADR files and crates with
  `grep`/`ls`.
* Verified every cited repo-relative path exists at the tag.
* Derived the v0.2.0 → v0.2.1 delta from the ADR files and modules present in the v0.2.1 tree
  (ADR 0052 and 0055–0060) because the checkout is a **single-commit shallow tag**: there is no v0.2.0
  tree to diff. The attribution to this release is code + ADR + CHANGELOG agreement, not a
  two-tree diff.

## Unchanged

Not applicable — this is the first AniCraft skill, so no claim is a carry-forward from a
previous AniCraft round. Within this round, the following were checked and left as stated
because the code agrees: the 5 MCP tools, the 3 protocol revisions, the three-tier
confirmation model in ADR 0004, and the MCP/CLI frame-base split (commands and MCP are 0-based;
CLI flags are 1-based).

## Known gap in this round

* **No two-tree diff.** The source checkout has one commit (shallow tag), so the delta paragraph
  names the surfaces added by v0.2.1 from ADR/module evidence rather than a `git diff v0.2.0..v0.2.1`.
* **No GUI run, by rule.** Every UI statement is from `src/` code and docs, not observation.
  The `--screenshot` flag exists (`src/main.rs`) but was not used.
* **No build, test run or export writes.** Counts are static plus read-only CLI output; render,
  GIF, video, Lottie, HTML and publish paths were read, not executed. Performance budgets in
  `docs/performance.md` are quoted as documentation, not re-measured.
* **Web build not exercised.** The wasm build path (`scripts/build-web.sh`, `docs/web.md`) and
  its browser limitations are documented from source; no browser or wasm build was run.
* **Accessibility and localisation not exercised at runtime.** Screen-reader names, high
  contrast and pseudo-locale are code/doc claims; no manual assistive-technology pass was made.
* **macOS packaging caveat.** The README says the app is "verified on Windows so far" while a
  signed macOS 0.2.1 bundle is installed here; the skill records the bundle it audited and does
  not generalize from it.
