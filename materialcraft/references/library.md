# MaterialCraft — library, formats and presets index (v0.4.1)

Measured at tag `v0.4.1` (`65f7bfd3e5f40d695d03162285879f0f8079ff6c`). Counts are parsed from the
code paths named in each heading; `evidence.md` records the method.

## Main-graph catalog — 29 entries

24 `Atomic nodes` + 5 `Graph items`, from `crates/nodes/src/atomic/catalog.rs::defs()` and the
`ATOMIC` / `GRAPH_ITEMS` constant in each `node(...)` call. No SBS-library node has a Rust
reimplementation; SBS nodes live in SBS graphs and appear through `library.tree`.

| id | label | category |
|---|---|---|
| `bitmap` | Bitmap | Atomic nodes |
| `blend` | Blend | Atomic nodes |
| `blur` | Blur | Atomic nodes |
| `channels_shuffle` | Channels shuffle | Atomic nodes |
| `curve` | Curve | Atomic nodes |
| `directional_blur` | Directional blur | Atomic nodes |
| `directional_warp` | Directional warp | Atomic nodes |
| `distance` | Distance | Atomic nodes |
| `emboss` | Emboss | Atomic nodes |
| `fx_map` | FX-Map | Atomic nodes |
| `gradient_dynamic` | Gradient (Dynamic) | Atomic nodes |
| `gradient_map` | Gradient map | Atomic nodes |
| `grayscale_conversion` | Grayscale conversion | Atomic nodes |
| `hsl` | HSL | Atomic nodes |
| `levels` | Levels | Atomic nodes |
| `normal` | Normal | Atomic nodes |
| `pixel_processor` | Pixel processor | Atomic nodes |
| `sharpen` | Sharpen | Atomic nodes |
| `svg` | SVG | Atomic nodes |
| `text` | Text | Atomic nodes |
| `transformation` | Transformation 2D | Atomic nodes |
| `uniform` | Uniform color | Atomic nodes |
| `value_processor` | Value processor | Atomic nodes |
| `warp` | Warp | Atomic nodes |
| `dot` | Dot | Graph items |
| `input_color` | Input color | Graph items |
| `input_grayscale` | Input grayscale | Graph items |
| `input_value` | Input value | Graph items |
| `output` | Output | Graph items |

`motion_blur` was deleted between v0.2.0 and v0.4.1; v0.2.0 had 30 entries (25 + 5).
`materialcraft-cli nodes --category "Atomic nodes"` is the live listing.

## Function operations — 85

From `crates/nodes/src/function/catalog.rs::FUNCTIONS` (85 entries, 85 unique ids). The category is
the operation menu's group.

| Category | n | ids |
|---|---:|---|
| Constant | 10 | `const_float1` `const_float2` `const_float3` `const_float4` `const_int1` `const_int2` `const_int3` `const_int4` `const_bool` `const_string` |
| Vector | 14 | `vector2` `vector3` `vector4` `swizzle1` `swizzle2` `swizzle3` `swizzle4` `ivector2` `ivector3` `ivector4` `iswizzle1` `iswizzle2` `iswizzle3` `iswizzle4` |
| Variables | 12 | `set` `get_float1` `get_float2` `get_float3` `get_float4` `get_integer1` `get_integer2` `get_integer3` `get_integer4` `get_bool` `get_string` `isdefined` |
| Samplers | 2 | `samplelum` `samplecol` |
| Cast | 8 | `tofloat` `tofloat2` `tofloat3` `tofloat4` `toint1` `toint2` `toint3` `toint4` |
| Operator | 8 | `add` `sub` `mul` `mulscalar` `div` `neg` `mod` `dot` |
| Logical | 3 | `and` `or` `not` |
| Comparison | 6 | `eq` `noteq` `gt` `gteq` `lr` `lreq` |
| Function | 18 | `abs` `floor` `ceil` `cos` `sin` `tan` `atan2` `cartesian` `sqrt` `log` `exp` `log2` `pow2` `pow` `lerp` `min` `max` `rand` |
| Control | 4 | `sequence` `ifelse` `while` `passthrough` |

## Pattern nodes (FX-Map) — 4

`crates/nodes/src/pattern/catalog.rs`; kinds in `crates/core/src/pattern_node_kind.rs::ALL`.

| id | label | role |
|---|---|---|
| `paramset` | Quadrant | root of a new FX-Map |
| `markov2` | Switch | branch switch |
| `addnode` | Iterate | repeat the branch |
| `passthrough` | Dot | vertical pass-through |

Iterative traversal, cycle detection and node/execution budgets apply; a shared child in a DAG is
legal and an exhausted budget is an error (`docs/atomic-workflow.md` "Files and execution").

## Reusable SBS functions — 171

`assets/sbs/functions.sbs` holds **171 function graphs / 2 334 function nodes** (asserted in
`crates/formats/tests/function_library.rs`). The library loads once per process from the library
folder (`assets/sbs`, or `MATERIALCRAFT_SBS_DIR`); installed and browser builds embed it
(`docs/architecture.md`). Discover with `library.functions {filter?}` or `library.tree {canvas?}`,
insert with `library.function.add {graph, package?, function?, at?}`. Library aliases are
read-only save destinations; an edited library is saved to a local path.

## Formats

| Direction | Extensions | Code |
|---|---|---|
| Native project | `.sbs` (XML + adjacent `resources/`) | `crates/formats/src/sbs/` |
| Native project archive | `.mcraft` (ZIP: one root SBS, conventionally `package.sbs`, + `resources/`) | `crates/formats/src/project.rs` |
| Portable material | `.mcmat` (manifest v2 + `maps/` + `source.sbs`) | `crates/formats/src/material/` |
| Bitmap import | `dds webp gif hdr exr jpg jif jpeg jpe pgm png tif tiff tga targa bmp` | `BITMAP_EXTENSIONS`, `crates/formats/src/image.rs` |
| Vector import | `svg` | `VECTOR_EXTENSIONS`, `crates/formats/src/svg.rs` |
| Map export | `png jpg tga bmp webp exr hdr` at 8/16/32 bit | `EXPORT_FORMATS`, `encode` |
| Mesh for the 3D view | `obj glb gltf` | `MESH_EXTENSIONS`, `crates/formats/src/mesh.rs` |

TIFF is import-only. DDS uses its own decoder and loads the first surface at the largest mip; GIF
loads its first frame (`docs/architecture.md` "Files"). SVG is vector geometry only; fonts are not
loaded.

## Portable material map usages — 9

`crates/formats/src/material/map_entry.rs`: `baseColor`, `normal`, `roughness`, `metallic`,
`height`, `ambientOcclusion`, `emissive`, `opacity`, `specular`. Colour usages are written 8-bit
sRGB, data 16-bit linear, normals OpenGL-style; `source.sbs` rides along so a consumer can re-cook.

## Presets and views

- Templates for `file.new`: `empty`, `pbr`, `atomics` (`crates/engine/src/samples.rs::TEMPLATES`).
- 3D scenes: `cube`, `cylinder`, `plane`, `sphere`, `material_ball`, `rounded_cube`, `torus`, plus
  `custom` after `view.3d.loadMesh` (`crates/engine/src/view_cmds.rs::SCENES`).
- 3D environments: `studio`, `sunset`, `overcast`, `night` (`view.3d` environment ids). The IBL
  module builds six named environments in all — "Studio Soft", "Studio Contrast", "Overcast",
  "Sunset", "Warehouse", "Night" (`crates/render/src/ibl.rs`) — but `view.3d` accepts only the four
  ids, mapping `studio` to "Studio Soft".
- UI locales: `en`, `ar` (right-to-left) — `crates/ui-egui/src/i18n.rs`.
