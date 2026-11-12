# TextureCraft — automation surfaces at v0.6.1

Read this when you need the exact method/tool/flag names. Every table was read from the tag's code,
not from prose docs; the counts are re-derived in `evidence.md`.

Surface summary: **177 engine command ids**, **15 control methods** (+`auth`), **22 MCP tools**,
**17 serve methods**, **10 CLI subcommands**, **59/59 live menu items**.

## Control channel (`texturecraft --control <port>`)

Loopback TCP, one JSON object per line, 8 MiB request cap (`crates/automation/src/security.rs`).
The first request on every connection must authenticate:
`{"id":0,"method":"auth","params":{"token":"…"}}`. The token comes from
`TEXTURECRAFT_CONTROL_TOKEN` or from `<temp>/texturecraft-control-<port>.token` (owner-only, also
printed to stderr). One auth attempt, 10 s deadline, 16 concurrent connections, 600 s idle, then the
connection closes (`apps/texturecraft/src/control_server.rs`).

| Method | Params | Result |
|---|---|---|
| `ping` | | `"pong"` |
| `command.run` | `{id, params?}` | the command's JSON result |
| `command.list` | `{filter?}` | `[{id, label, menu, shortcut, params, enabled}]` |
| `session.inspect` | | project, mesh, texture sets, layers, tool, view, `bakePreview`, camera, display, history, memory |
| `ui.inspect` | | UI state, viewport rect, fps, `baking` (0..1 or null), `bakeStatus`, `bakePreview`, toasts, `titleBar` |
| `ui.menu.list` | | `{menu, submenu, label, id, shortcut, implemented, enabled}` per item |
| `ui.menu.invoke` | `{id}` | behaves like a menu click (may open a window) |
| `ui.bake.start` | `{ts?: index \| [indices]}` (default: sets ticked in Bake mode) | `bake.preview` state; errors if a bake is already running or no set is selected |
| `ui.bake.cancel` | | `null`; the set being baked keeps its maps, finished sets stay applied, the previous view returns |
| `ui.set` | fields of the UI state (`layout`, `dock`, `prefs`, `keymap`, …) | `null` |
| `viewport.screenshot` | `{view?: "3d" \| "2d"}` | `{width, height, png}` base64 |
| `ui.screenshot` | | whole-window PNG after the next frame |
| `ui.resize` | `{width, height}` points 640–7680 | `null`, leaves maximized |
| `debug.paintTest` | `{from: [x,y], to: [x,y], frames?: 120}` | `null`; paints through the real frame loop |
| `debug.frames` | | frame timing since the last call, with `strokeEnd` |

`ui.set` `prefs` fields used in this skill: `language`, `brightness` (`dark`, `mediumDark`,
`mediumLight`, `light`), `accent` (7 colours), `system_title_bar`, `project_open_limit_gib`
(1..=u32::MAX, default 8, applies before the next control request), `reserved_cores`,
`save_ram_percent`. The `prefs` value replaces the whole prefs object and omitted fields take their
defaults (`Prefs` is `#[serde(default)]`, `crates/ui-egui/src/state.rs`), so send every pref you
need to keep.

## MCP server (`texturecraft-cli mcp`)

stdin/stdout MCP. Headless mode confines files to `--read-root` / `--write-root`; bridged mode
(`--bridge <port>`) forwards to the running app and cannot touch files itself.

| Tool | Params | Notes |
|---|---|---|
| `session_inspect` | | the whole session as JSON |
| `command_list` | `{filter?}` | id, label, menu, shortcut, params, enabled |
| `command_run` | `{id, params?}` | refuses `file.*` (except `file.close`, `file.removeUnused`, `file.reimportMesh` without `path`) and any `path`/`dir`, at top level or in `files` |
| `command_batch` | `{steps: [{id, params?}]}` | stops at the first error, ≤256 steps |
| `project_new` | `{mesh?, resolution?, name?, template?}` | 9 built-ins incl. `udim_plane`; default resolution 1024 |
| `project_open` | `{path}` | `.tcraft` or a mesh file, below the read root |
| `project_save` | `{path?}` | `.tcraft` appended if missing; omit to save in place |
| `mesh_import` | `{path, resolution?}` | one texture set per material |
| `mesh_reimport` | `{path?, preserveStrokes?}` | no path = the project's own copy; `preserveStrokes` off by default |
| `mesh_export` | `{path, format?}` | obj, glb, usda, usdc, usdz |
| `bake_mesh_add` | `{path, cage?}` | high poly, or the cage when `cage: true` |
| `resource_import` | `{path}` | image resource; then `layer.add.image`, `tool.stencil`, or `textureSet.meshMap.set` |
| `material_save` | `{path, layer?, name?}` | `.tcmat` |
| `material_load` | `{path}` | `.tcmat`, MaterialCraft `.mcmat`, `.mcraft` |
| `textures_export` | `{dir, preset?, ts?, format?, padding?, size?}` | returns the written files |
| `bake` | `{ts?, resolution?, maps?, cpu?}` | all maps in one pass, no preview |
| `paint_stroke` | `{points, viewport?, color?, roughness?, metallic?, height?, size?, hardness?}` | viewport pixels, same space as `viewport_render` |
| `viewport_render` | `{view?, width?, height?, yaw?, pitch?, samples?, bounces?, cpu?}` | PNG ≤2048 px; `samples` 1–4096 path traces |
| `viewport_screenshot` | `{view?}` | bridge only |
| `ui_screenshot` | | bridge only |
| `ui_inspect` | | bridge only |
| `ui_menu_invoke` | `{id}` | bridge only |

There is no MCP tool for `ui.bake.start`/`ui.bake.cancel`; use the control channel for the live bake
preview.

## Headless JSON-lines server (`texturecraft-cli serve`)

`{"id", "method", "params"}` per line, on stdio or on `127.0.0.1:<port>` with a token (same auth and
limits as the control channel). Methods, unchanged at v0.6.1:

`ping`, `methods`, `session.inspect`, `command.list`, `command.run`, `command.batch`,
`project.open`, `project.save`, `mesh.import`, `mesh.reimport`, `mesh.export`, `bake.mesh.add`,
`resource.import`, `material.save`, `material.load`, `textures.export`, `render`.

## CLI (`texturecraft-cli`)

Hand-rolled parser; positional order matters (input first, `-o` last).

| Subcommand | Flags | What it does |
|---|---|---|
| `info <input>` | | texture sets, layers, triangles, materials, UV report as JSON |
| `commands` | `--filter` | list engine commands |
| `run <input> <command-id> [params-json]` | `-o` | run one command, print its JSON result |
| `batch <script.json>` | | step list or `{open, steps, save}` |
| `bake <input>` | `-o`, `--resolution`, `--maps` | bake every texture set (all maps at once) |
| `export <input> <dir>` | `--preset`, `--format`, `--padding`, `--size` | export textures |
| `render <input> <out.png>` | `--size`, `--view`, `--camera`, `--yaw`, `--pitch`, `--samples`, `--bounces`, `--cpu` | viewport or path-traced PNG |
| `new <mesh \| builtin:<id>> <out.tcraft>` | `--resolution`, `--sample` | new project; `--sample` bakes and applies a smart material |
| `mcp` | `--bridge`, `--token`, `--read-root`, `--write-root`, `--automation-read-root`, `--automation-write-root` | MCP on stdio |
| `serve` | `--port`, `--read-root`, `--write-root`, `--automation-read-root`, `--automation-write-root` | JSON lines on stdio or TCP |

The macOS app bundle ships only `TextureCraft`; `texturecraft-cli` is a separate download/build.

## Engine command families (177 ids)

`layer` 26, `tool` 21, `camera` 17, `textureSet` 16, `effect` 16, `bake` 14, `viewport` 11, `file` 11,
`mask` 10, `material` 8, `project` 5, `export` 5, `resource` 4, `brush` 4, `edit` 3, `path` 2,
`text` 1, `filter` 1, `display` 1, `alpha` 1. Discover the live set with
`texturecraft-cli commands --filter <text>` rather than hard-coding ids.

## New or changed at v0.6.1

| Id / method | Params | Effect |
|---|---|---|
| `bake.preview` | `{show?: follow\|material\|map:<id>}` | read or pin what the live bake shows; `{active:false}` with no bake |
| `ui.bake.start` | `{ts?}` | start the app's streaming bake |
| `ui.bake.cancel` | | stop it |
| `textureSet.meshMap.import` | `{files: [{path, map?}]}` | up to 512 images by file name, 2 GiB total, desktop only, one undo step |
| `tool.fillSelection` | `{hitTest?: intersection\|containedCenter, visibleOnly?}` | box-fill behaviour |
| `tool.fillMode` | `{mode: triangle\|polygon\|uvIsland\|mesh}` | polygon-fill granularity; `polygon` is new at v0.6.1 |
| `tool.click` | `{x,y}`, `{x0,y0,x1,y1}`, `{uv}`, `{uv0,uv1}` | box and 2D-view fills |
| `tool.swapMaskValue` | `{}` | mask value becomes 1 − value (shortcut X) |
| `effect.set` | `filter?: id from filter.list` | swaps a filter's type in place |
| `effect.colorSelection.pick` | `{effect?, x?, y?, viewport?, uv?, index?}` | samples an ID-map colour |
| `tool.brush` | `symmetryOn`, `symmetryOffset`, `symmetryAxis`, `symmetryAngleSpan` | movable symmetry plane, axis, span |
| `tool.path` | `{points?\|uvPoints?, closed?, fill?, commit?, clear?}` | draft a path, commit it to a path sublayer |
