# MaterialCraft — evidence map (v0.1.0, first audit)

Audit basis: tag `v0.1.0`, commit `cedabf02030a3c662fda99b197ceb3ed12790ee7`, inspected 2026-11-04.
Every count below names how it was measured in this checkout; none is copied from the app's docs.

| # | Claim | Evidence | Tier |
|---:|---|---|---|
| 1 | 68 engine command ids | `crates/engine/src/{file,material,edit,graph,node,view}_cmds.rs` — literal first arguments of `cmd!(` in non-test source (8+4+10+28+11+7) | implemented |
| 2 | 11 CLI subcommands | `apps/materialcraft-cli/src/main.rs` `SUBCOMMANDS` | implemented |
| 3 | 21 MCP tools | `crates/automation/src/server.rs` — `#[tool` attributes on the tool router | implemented |
| 4 | 11 JSON-lines methods | `crates/automation/src/rpc.rs` `METHODS` | implemented |
| 5 | Control channel requires `auth` on the first request | `docs/control-protocol.md`; token from `MATERIALCRAFT_CONTROL_TOKEN` or `<temp>/materialcraft-control-<port>.token` | implemented |
| 6 | Headless path confinement | `crates/automation/src/rpc.rs`, `docs/control-protocol.md` (`--read-root`/`--write-root`; path-taking `file.*` refused through `command.run`) | implemented |
| 7 | `.mcraft` = zip with `package.json` + embedded resources | `crates/formats/src/lib.rs` | implemented |
| 8 | `.mcmat` = zip `material.json` + `maps/<usage>.png` + `source.mcraft`, format `craft-material`, version 1 | `crates/formats/src/material.rs` `Manifest`, `FORMAT`, `VERSION` | implemented |
| 9 | `.mcmat` map usages (9) | `crates/formats/src/material.rs` `MapEntry.usage` doc: baseColor, normal, roughness, metallic, height, ambientOcclusion, emissive, opacity, specular | implemented |
| 10 | Map color spaces: 8-bit sRGB for colour, 16-bit linear otherwise, OpenGL normals | `crates/formats/src/material.rs` module doc | implemented |
| 11 | Export formats PNG/JPEG/TGA/TIFF/BMP/WebP/EXR/HDR at 8/16/32 bit | `crates/formats/src/lib.rs` `IMAGE_EXTENSIONS`; CLI `--format`, `--depth` | implemented |
| 12 | 12 templates | `crates/engine/src/samples.rs` (`empty`, `pbr`, `bricks`, `stone_tiles`, `wood`, `metal_plates`, `rusty_metal`, `lava`, `marble`, `wicker`, `fabric`, `ground`) | implemented |
| 13 | 7 3D scenes + custom mesh | `crates/render/src/preview.rs` (`rounded_cube`, `cube`, `sphere`, `cylinder`, `plane`, `torus`, `material_ball`); `view.3d.loadMesh` for OBJ/glTF/GLB | implemented |
| 14 | 227 nodes, all tileable | `ROADMAP.md` headline (the repo's own count); live enumeration is `materialcraft-cli nodes` | claimed |
| 15 | Node library is 45 % of the target; ≈67 % overall parity | `ROADMAP.md` "By area" | claimed |
| 16 | No GPU 3D view (CPU parallax only) | `docs/gaps.md` #2; `crates/render/src/preview.rs` | claimed |
| 17 | No mesh-based generators or bakers | `docs/gaps.md` #3 | claimed |
| 18 | `.mcmat` cannot be exported through MCP (no tool; path commands refused) | `docs/gaps.md` #4 + tool list in `server.rs` | implemented (gap) |
| 19 | No function loops; one graph at a time; English only | `docs/gaps.md` #5, #8, #9 | claimed |
| 20 | `--hq` beauty render (displacement, ray-traced AO, key light, 3×3 supersampling) | `apps/materialcraft-cli/src/main.rs` USAGE; `crates/automation` `RenderOptions` | implemented |
| 21 | Templates/scenes are command parameters, not separate code paths | `file.new` / `graph.templates`, `view.3d` params in `docs/control-protocol.md` | implemented |

## Drift notes

- `docs/control-protocol.md` documents `file.new` as the new-package command; the registry id is `file.newPackage` (both exist). Trust `commands`/`command_list`.
- The ROADMAP's per-area table is hand-maintained; the node count (227) is the only headline number quoted here, and it is labeled claimed.

## Not measured

- Runtime behaviour (cook times, render quality) — no GUI or build was run.
- Preset/library counts inside the bundled assets — not enumerated.
