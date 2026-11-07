# MaterialCraft — evidence map (v0.2.0, re-pinned audit)

Audit basis: tag `v0.2.0`, commit `a1bbd4a83f62365d90f085e5f1ad61410f9cf11c`, inspected 2026-11-07.
Supersedes the v0.1.0 map (`cedabf02030a3c662fda99b197ceb3ed12790ee7`, 2026-11-04).
Every count below names how it was measured in this checkout; none is copied from the app's docs.

**Round 2026-11-07.** Delta measured from `git diff v0.1.0..HEAD` (493 files, +28 806/−13 724). The
document format, the node library and the `.mcmat` manifest all moved, so rows 1–5, 7–9, 12, 14–19 and
the count table were re-derived; the untouched rows are carried forward because the code path is the same
file and the same shape. Unexercised UI behaviour stays labeled, not upgraded.

| # | Claim | Evidence | Tier |
|---:|---|---|---|
| 1 | 86 engine command ids (was 68 at v0.1.0) | `crates/engine/src/commands.rs` `command_specs()` aggregates 19 modules; literal ids via `cmd!(\s*"id"` — graph 53, edit 13, file 10, view 8, library 1, session 1 | implemented |
| 2 | 11 CLI subcommands — unchanged at v0.2.0 | `apps/materialcraft-cli/src/main.rs` `SUBCOMMANDS` (flags gained `--size`, `--displacement`, `--automation-*`-root aliases) | implemented |
| 3 | 20 MCP tools (was 19; the old "21" counted `#[tool_router]`/`#[tool_handler]` attributes) | `crates/automation/src/server/material_craft_mcp.rs` — `#[tool(...)]` followed by `async fn` | implemented |
| 4 | 12 JSON-lines methods (adds `material.export`; `methods` existed at v0.1.0 too) | `crates/automation/src/rpc.rs` `METHODS` | implemented |
| 5 | Control channel requires `auth` on the first request; one attempt per connection within 10 s; refusal closes it; ≤16 connections; 8 MiB request cap | `crates/automation/src/security.rs` (`AUTH_TIMEOUT`, `MAX_CONNECTIONS`, `MAX_REQUEST_BYTES`), `apps/materialcraft/src/control_server.rs` | implemented |
| 6 | Token: `MATERIALCRAFT_CONTROL_TOKEN` or a fresh random owner-only file `<temp>/materialcraft-control-<port>.token` (0600 on Unix) written after bind | `crates/automation/src/security.rs` `token_file`, `generate_token`, `server_token`; `docs/control-protocol.md` | implemented |
| 7 | Native document is SBS XML `.sbs`; `.mcraft` support removed | `crates/formats/src/sbs/sbs_reader.rs`, `sbs_writer.rs`; `file.save` param doc "saves native SBS"; zero `.mcraft` occurrences under `crates/`; `docs/atomic-workflow.md` "Files and execution" | implemented |
| 8 | `.mcmat` = zip `material.json` (`format: "craft-material"`, **version 2**) + `maps/<usage>.png` + **`source.sbs`**; version-1 archives rejected | `crates/formats/src/material/archive.rs` (`FORMAT`, `VERSION = 2`, `SOURCE = "source.sbs"`, read-path version check) | implemented |
| 9 | `.mcmat` map usages (9) — unchanged at v0.2.0 | `crates/formats/src/material/map_entry.rs` `usage` doc: baseColor, normal, roughness, metallic, height, ambientOcclusion, emissive, opacity, specular | implemented |
| 10 | Map color spaces: 8-bit sRGB for colour usages, 16-bit linear otherwise, OpenGL normals | `crates/formats/src/material/archive.rs` `srgb_usage`; `docs/control-protocol.md` | implemented |
| 11 | Export formats PNG/JPEG/TGA/TIFF/BMP/WebP/EXR/HDR at 8/16/32 bit — unchanged at v0.2.0 | `crates/formats/src/lib.rs` `IMAGE_EXTENSIONS` (11 extensions); `file.export` format list | implemented |
| 12 | 3 templates (`empty`, `pbr`, `atomics`) — was 12 | `crates/engine/src/samples.rs` `TEMPLATES`; `apps/materialcraft-cli/src/main.rs` USAGE | implemented |
| 13 | 7 3D scenes + custom mesh — unchanged at v0.2.0 | `crates/render/src/preview.rs` scene list (`rounded_cube`, `cube`, `sphere`, `cylinder`, `plane`, `torus`, `material_ball`); `view.3d.loadMesh` for OBJ/glTF/GLB | implemented |
| 14 | 30 catalog entries: 25 `Atomic nodes` + 5 `Graph items` — replaces the retired "227 nodes" | `crates/nodes/src/atomic/catalog.rs` `defs()`; `crates/nodes/src/catalog.rs` delegates to it | implemented |
| 15 | 85 function operations | `crates/nodes/src/function/catalog.rs` `FUNCTIONS` (85 entries, 85 unique ids) | implemented |
| 16 | 4 pattern nodes (Quadrant, Switch, Iterate, Dot) — new at v0.2.0; v0.1.0 had one `fx_map` atomic node | `crates/nodes/src/pattern/catalog.rs` `definitions()`, `crates/core/src/pattern_node_kind.rs` `ALL` | implemented |
| 17 | 2 UI locales, English and Arabic (RTL) — the old "English only" gap is closed | `crates/ui-egui/src/i18n.rs` language table; `crates/ui-egui/src/i18n/ar.rs` | implemented |
| 18 | `material_export` MCP tool + `material.export` method: a sandboxed agent can write a `.mcmat` below its write root | `crates/automation/src/server/material_craft_mcp.rs`; `crates/automation/src/rpc.rs` | implemented |
| 19 | Headless path confinement: files only below the read/write roots; path-taking `file.*` refused through `command.run` | `crates/automation/src/{rpc.rs,workspace.rs,filesystem.rs}`; `docs/control-protocol.md` | implemented |
| 20 | `--hq` beauty render (displaced mesh, ray-traced AO, shadowed key light, 3×3 supersampling); `--displacement` sets depth | `apps/materialcraft-cli/src/main.rs` USAGE; `crates/automation/src/render_options.rs` | implemented |
| 21 | Export `size?` (larger side px, 16..8192, power-of-two floor, proportions kept) and colliding-filename rejection | `crates/engine/src/file_cmds.rs` `file.export` param doc + duplicate-name error | implemented |
| 22 | 3D view controls: four environments, exposure/envRotation, heightScale/heightLevel, transparency, alphaView, normalYFlip | `crates/engine/src/view_cmds.rs` `view.3d` param doc; `crates/render/src/preview.rs`; `crates/ui-egui/src/view3d.rs` | implemented |
| 23 | No GPU 3D view; CPU renderer with parallax only | `crates/render/src/preview.rs`; `docs/gaps.md` #2 (historical header) | claimed |
| 24 | No mesh-based generators or bakers | `docs/atomic-workflow.md`; no baker module under `crates/` | claimed |
| 25 | SBS import is not lossless for arbitrary files; unsupported parameters warn, missing nodes become placeholders | `docs/atomic-workflow.md` "Current limits"; `crates/core/src/missing_node.rs`; `crates/formats/src/sbs/sbs_reader.rs` | claimed |
| 26 | Reference-app reopen and numerical parity unverified | `ROADMAP.md`; `docs/atomic-workflow.md` "Current limits" | claimed |
| 27 | No function loops / reusable functions; one graph at a time; fixed shortcuts, no keymap editor | `docs/gaps.md` #5, #8, #9 (document still current on these; its library counts are historical) | claimed |
| 28 | No signed/notarized public release | `docs/gaps.md` #10; `.github/workflows/release.yml` exists | claimed |
| 29 | `ui.screenshot` may time out on the capture callback | `docs/gaps.md` #7 — not retested this round | claimed |
| 30 | Text uses a built-in stroke font; external fonts error; SVG is vector geometry only | `docs/atomic-workflow.md`; `crates/nodes/src/atomic/{text.rs,svg.rs}` | claimed |

## Headline count table

| Count | v0.1.0 | v0.2.0 | Method |
|---|---:|---:|---|
| Engine command ids | 68 | **86** | `cmd!(` literal ids over the modules in `command_specs()` |
| CLI subcommands | 11 | **11** (unchanged) | `SUBCOMMANDS` |
| MCP tools | 19 | **20** | `#[tool(…)] async fn` in the MCP module |
| JSON-lines methods | 11 | **12** | `rpc.rs` `METHODS` |
| Catalog entries | — (227 "nodes" was a different, retired library) | **30** (25 atomic + 5 graph items) | `crates/nodes/src/atomic/catalog.rs::defs()` |
| Function operations | — | **85** | `crates/nodes/src/function/catalog.rs::FUNCTIONS` |
| Pattern nodes | 1 (`fx_map` atomic node) | **4** pattern kinds | `crates/nodes/src/pattern/catalog.rs::definitions()` |
| Templates | 12 | **3** | `crates/engine/src/samples.rs::TEMPLATES` |
| 3D scenes | 7 | **7** (unchanged) | `crates/render/src/preview.rs` scene list |
| `.mcmat` map usages | 9 | **9** (unchanged) | `crates/formats/src/material/map_entry.rs` usage doc |
| `.mcmat` manifest version | 1 | **2** | `crates/formats/src/material/archive.rs::VERSION` |
| Export formats / image extensions | 8 / 10 | **8 / 11** (`svg` added) | `IMAGE_EXTENSIONS` + `file.export` |
| UI locales | 1 | **2** | `crates/ui-egui/src/i18n.rs` |

## Drift notes

- `ROADMAP.md` says "26 native primitives and four graph input/output items"; the code's categories are
  **25 `Atomic nodes` + 5 `Graph items`** (Dot is a graph item, not a primitive). The total (30) agrees, the
  split does not — the measured split is what the skill and the tables above use.
- `docs/file-format-parity.md` and `docs/releasing.md` still describe `.mcraft` as a supported package
  format; the code has no `.mcraft` handling and `docs/architecture.md`/`docs/atomic-workflow.md` say it was
  removed. Code wins.
- `docs/control-protocol.md` lists the old template ids for `file.new` (`bricks`, `stone_tiles`, `wood`, …);
  the `TEMPLATES` table is `empty`, `pbr`, `atomics`.
- `docs/gaps.md` carries its own historical-warning header ("predates the 2026-11-05 primitive rewrite"); its
  counts (227 nodes, ~400 reference) cannot be used as current evidence, though its #5/#8/#9/#10 items still
  match the code.
- `ROADMAP.md` retires all earlier percentage estimates; the skill no longer quotes a parity percentage.
- `crates/nodes/src/function/` is now the evaluation home; `crates/core/src/function.rs` (cited at v0.1.0) no longer exists — document types are `crates/core/src/function_graph.rs` and `function_node.rs`.
- `crates/formats/src/material.rs` became a directory (`material/`), and `crates/automation/src/server.rs`
  became `crates/automation/src/server/material_craft_mcp.rs`; both citations were re-resolved.

## Not measured

- Runtime behaviour (cook times, render quality, UI states, RTL layout, wire selection) — no GUI or build was
  run; only the bundle's `--version`/`--help` were executed.
- The installed bundle ships no separate `materialcraft-cli`, so CLI counts come from source.
- The SBS library assets (`assets/sbs/all_nodes.sbs`: 321 `sbs://` dependency references, 35 `<filter>`
  entries) were counted but not exercised.
