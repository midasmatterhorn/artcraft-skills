# MaterialCraft — round 2026-11-07 changes

Re-pinned **v0.1.0** (`cedabf02030a3c662fda99b197ceb3ed12790ee7`, first audit) → **v0.2.0**
(`a1bbd4a83f62365d90f085e5f1ad61410f9cf11c`); the installed bundle's own binary prints
`MaterialCraft 0.2.0 (a1bbd4a 2026-11-06)`, and `git rev-parse HEAD` in the pinned checkout
matches the tag commit. Delta measured from `git diff v0.1.0..HEAD` (493 files, +28 806/−13 724).

## Corrected / re-measured

- **The native document is `.sbs`, not `.mcraft`.** v0.2.0 saves and opens native SBS XML
  (`crates/formats/src/sbs/sbs_reader.rs`, `sbs_writer.rs`; `file.save` doc: "saves native SBS").
  `.mcraft` read/write support is gone from the code — zero `.rs` occurrences of the string in
  the tree; `docs/architecture.md` and `docs/atomic-workflow.md` say so, while
  `docs/file-format-parity.md` and `docs/releasing.md` still describe `.mcraft` (stale docs, not
  code). The SKILL's format section, description and round-trip protocol were rewritten.
- **The Rust node library was replaced by native primitives.** The old "227 nodes, all tileable"
  claim and the "node library 45 %, ≈67 % parity" roadmap figures are retired: `ROADMAP.md`
  states earlier estimates and node counts are superseded. Measured now: **30 catalog entries**,
  25 nodes in the `Atomic nodes` category + 5 `Graph items` (`crates/nodes/src/atomic/catalog.rs` `defs()`),
  **85 function operations** (`crates/nodes/src/function/catalog.rs` `FUNCTIONS`), **4 pattern
  nodes** — Quadrant, Switch, Iterate, Dot (`crates/nodes/src/pattern/catalog.rs`).
  `crates/nodes/src/catalog.rs` now just re-exports `atomic::defs`. `ROADMAP.md`'s "26 primitives and
  four graph items" split is off by one against the code's categories (measured 25 + 5; Dot is a graph
  item) — the total of 30 agrees, and the drift is recorded in `evidence.md`.
- **`.mcmat` is manifest version 2**, not 1: maps + `material.json` + **`source.sbs`**
  (`crates/formats/src/material/archive.rs` `VERSION = 2`, `SOURCE = "source.sbs"`), and archives
  with any other version are rejected (`archive.rs` read path).
- **The MCP gap closed.** `material_export` is a real tool now
  (`crates/automation/src/server/material_craft_mcp.rs`), and the JSON-lines server gained
  `material.export` (`crates/automation/src/rpc.rs` `METHODS`). The previous "a sandboxed agent
  cannot hand a material to TextureCraft" limitation is deleted.
- **MCP tool count was wrong in the last round.** The old "21 tools" counted `#[tool` attributes
  including `#[tool_router]`/`#[tool_handler]`. Re-measured: **19 tool functions at v0.1.0**
  (`crates/automation/src/server.rs`) → **20 at v0.2.0**, the addition being `material_export`.
- **JSON-lines methods: 11 → 12.** `METHODS` is a literal slice; `material.export` is new.
  (`methods` was already in the v0.1.0 list, so the old "11" was right for that release.)
- **Engine command ids: 68 → 86.** The registry was split from six `*_cmds.rs` files into **19
  modules** aggregated by `command_specs()` (`crates/engine/src/commands.rs`): the count is
  `cmd!(` literal ids across exactly those modules — graph 53, edit 13, file 10, view 8,
  library 1, session 1. New ids include `graph.wire.insertDot/swap/delete`,
  `file.newAtomicSample`, `graph.templates`, plus alignment/frame/annotation/comment/function/
  pattern/value-input command modules.
- **Templates: 12 → 3.** `crates/engine/src/samples.rs` `TEMPLATES` is now `empty`, `pbr`,
  `atomics`; the material presets (bricks, wood, lava, marble, …) are gone. `docs/
  control-protocol.md` still lists the old template ids for `file.new` — that is doc drift.
- **Languages: 2, not 1.** `crates/ui-egui/src/i18n.rs` registers `en` and `ar` (Arabic, with
  RTL handling); the old "English-only UI" gap is now "no keymap editor".
- **Control channel hardening** (v0.2.0): random 256-bit token, token file created owner-only
  (0600 on Unix) after bind, one authentication attempt within 10 s, refusal closes the
  connection, 16 connections max, 8 MiB request cap (`apps/materialcraft/src/control_server.rs`,
  `crates/automation/src/security.rs`). The SKILL's auth paragraph was rewritten.
- **Moved paths re-resolved.** `crates/automation/src/server.rs` →
  `crates/automation/src/server/material_craft_mcp.rs`; `crates/formats/src/material.rs` →
  `crates/formats/src/material/{archive,manifest,map_entry,…}.rs`; `crates/core/src/function.rs`
  → `crates/nodes/src/function/` (evaluation) with document types in
  `crates/core/src/function_graph.rs` / `function_node.rs`. Those citations were fixed.
- **3D view grew view controls**: `transparency`, `alphaView`, `normalYFlip` (DirectX normal
  maps), `heightLevel`, `target` (`crates/engine/src/view_cmds.rs` `view.3d` param doc;
  `crates/render/src/preview.rs`). The "no light setups" wording was wrong even at v0.1.0 —
  `environment`/`exposure`/`envRotation` existed then — so the limitation now says CPU-only, no
  GPU tessellation.
- **Export gained a resolution option**: `file.export` takes `size?` (larger side in px, 16..8192,
  power-of-two floor, proportions kept) and refuses colliding output filenames
  (`crates/engine/src/file_cmds.rs`).
- **`docs/gaps.md` is now marked historical** by its own header ("predates the 2026-11-05
  primitive rewrite"); its gap #1/#2 counts are no longer usable as current evidence.
  `docs/atomic-workflow.md` "Current limits" is the current not-implemented source.

## Method

Read-only: `git show`/`git diff` against the pinned checkout, plus the installed bundle's
`--version` and `--help`. Counts by source parse, never from docs:

| Count | How |
|---|---|
| 86 engine commands | regex `cmd!\(\s*"id"` over the 19 modules named in `commands.rs::command_specs()`, deduped |
| 20 MCP tools | `#[tool(...)]` immediately followed by `async fn` in `crates/automation/src/server/material_craft_mcp.rs` (router/handler attributes excluded) |
| 12 JSON-lines methods | literal entries of `rpc.rs` `METHODS` |
| 11 CLI subcommands | `SUBCOMMANDS` slice in `apps/materialcraft-cli/src/main.rs` |
| 30 / 85 / 4 catalog, function, pattern entries | entries in `crates/nodes/src/atomic/catalog.rs::defs()`, `crates/nodes/src/function/catalog.rs::FUNCTIONS`, `crates/nodes/src/pattern/catalog.rs::definitions()` |
| 3 templates, 7 scenes, 9 map usages, 2 locales | `samples.rs` `TEMPLATES`; `crates/render/src/preview.rs` built-in scene list; `crates/formats/src/material/map_entry.rs` usage doc; `crates/ui-egui/src/i18n.rs` language table |
| 8 export formats / 11 image extensions | `crates/formats/src/lib.rs` `IMAGE_EXTENSIONS` + `file.export` format list |

## Unchanged

- 11 CLI subcommands — same 11 ids at v0.2.0 (`info`, `commands`, `nodes`, `run`, `batch`, `new`,
  `cook`, `export`, `render`, `mcp`, `serve`); flags were added, no subcommand.
- 8 map-export formats (PNG/JPEG/TGA/TIFF/BMP/WebP/EXR/HDR at 8/16/32 bit) and 9 `.mcmat` map
  usages — unchanged at v0.2.0; only the container version moved.
- 7 built-in 3D scenes (`rounded_cube`, `cube`, `sphere`, `cylinder`, `plane`, `torus`,
  `material_ball`) — unchanged at v0.2.0.
- The 8 app-only control methods (`ui.inspect`, `ui.menu.list`, `ui.menu.invoke`, `ui.set`,
  `ui.input`, `view.screenshot`, `ui.screenshot`, `ui.resize`) — unchanged at v0.2.0.
- Headless path confinement (`--read-root`/`--write-root`, now also spelled
  `--automation-read-root`/`--automation-write-root`), `MATERIALCRAFT_NO_PREFS=1`, the token env
  var name, and the `.mcmat` → TextureCraft contract.
- Browser/WebAssembly build and the macOS/Windows/Linux/FreeBSD targets.

## Known gap in this round

No GUI and no build: the Arabic RTL layout, the levels histogram, 4K preview, wire selection and
the Android-normal 3D flip are verified by code paths only, never exercised. `docs/gaps.md` #7
(`ui.screenshot` times out on the test machine) was not retested — it stays labeled as the repo's
claim. SBS import fidelity and numerical parity with the reference application are the repo's own
admissions, not measurements here. The installed bundle ships only the GUI binary — no separate
`materialcraft-cli` — so the CLI counts come from source, and only `--version`/`--help` were run.
