# SolidCraft — evidence ledger (tag v0.29.0)

Audit basis: this checkout is tag **`v0.29.0`**, commit **`3a5195b0a0aa359f6ebf10d890c1f887c70144b1`**
("Release 0.29.0", 2026-11-01; shallow clone of the release tag). Inspection date **2026-11-01**.
Installed `/Applications/SolidCraft.app` prints `solidcraft 0.29.0` and ships `solidcraft-cli 0.29.0`
(bundle id `io.tangencylabs.solidcraft`); the GUI was never launched.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | 539 engine commands, dotted ids, ~210 `cmd/` modules | `grep -rhoE 'CommandSpec::new\("[a-z0-9_.]+"'` over `crates/engine/src` = 539 unique ids; `crates/engine/src/cmd/mod.rs` module list | implemented |
| 2 | One planned command: `surface.fillet` | `crates/engine/src/cmd/mod.rs` `planned!` macro (refuses with issue id) | implemented (refusal) |
| 3 | 20 MCP tools incl. `skill_reference`, `undo`/`redo` | `crates/mcp/src/tools.rs` `tool_definitions` (18 inline `tool(` + `undo`/`redo` named) | implemented |
| 4 | MCP protocol revisions 2025-06-18 / 2025-03-26 / 2024-11-05 | `docs/mcp.md` header; `crates/mcp/src/server.rs` | implemented |
| 5 | Control channel default 127.0.0.1:27878 (→27893), token auth, `control/current.port` discovery | `docs/control-protocol.md` "Finding the port"/"Token"; `crates/engine/src/control_auth.rs` | implemented |
| 6 | App listens by default; Preferences ▸ Assistant toggle | `docs/mcp.md` "The app listens by default" | implemented |
| 7 | Sketch commands return `created: {points, curves, constraints, dimensions}` | `crates/engine/src/cmd/mod.rs` `created_doc!` | implemented |
| 8 | CLI verbs (16 listed + 6 unlisted) | `apps/solidcraft-cli/src/main.rs` `Command { name: …, listed: … }` table | implemented |
| 9 | Scripts: JSON `{"commands": [{command, params}]}` | `docs/scripts.md`; `solidcraft-cli run X --out Y` | implemented |
| 10 | Formats: STEP/IGES/3MF/STL/OBJ/glTF/PLY/URDF/DXF; `.sc`/`.solidcraft`/`.solvecraft`/JSON designs | `crates/io/src/lib.rs` `DESIGN_EXT`/`DESIGN_EXTS` test at :1149; `crates/io/src/{formats,dxf,gltf_in,obj}.rs` | implemented |
| 11 | Oracle 90/90 pass (69 analytic, 21 FreeCAD); README says "75 of 76" | `docs/oracle.md` generated table vs `README.md`/`docs/capabilities.md` | implemented (doc drift) |
| 12 | 17 in-repo agent skills; modelling ones embedded, served via `skill_reference` | `skills/README.md` table; `crates/mcp/src/skill_reference.rs` | implemented |
| 13 | Async render jobs (`render.preflight/start/status/cancel/export`) | `docs/mcp.md` intro; `docs/render-jobs.md` | implemented |
| 14 | Independent clean-room; no CAD-vendor affiliation | `README.md` Disclaimer; `NOTICE`; `DISCLAIMER.md` | policy |
| 15 | macOS bundle signed/notarized; Windows unsigned; **CLI inside the macOS bundle** | `README.md` Download; `/Applications/SolidCraft.app/Contents/MacOS/` listing | verified |

## 2. Counts: first audit (no previous skill)

| Surface | v0.29.0 (measured) |
|---|---:|
| Engine commands | 539 (1 planned) |
| `cmd/` modules | ~210 |
| MCP tools | 20 |
| CLI verbs | 16 listed + 6 unlisted |
| Design extensions | `sc`, `solidcraft`, `solvecraft` (+ JSON) |
| Interchange formats | STEP, IGES, 3MF, STL, OBJ, glTF/GLB, PLY, DXF, URDF |
| In-repo agent skills | 17 |
| docs pages | 118 |
| Oracle cases | 90/90 pass (69 analytic / 21 FreeCAD) |
| Control port | 27878 default (→27893) |
| Workspace crates | ~11 (`derive doc engine geom gpu io kernel mcp render sketch` + apps) |

## 3. Uncertain / not verified

- GUI behaviour never launched; the modelling claims come from `docs/capabilities.md` and the
  command registry, not from driving the solver.
- Typed `describe_command` contracts cover "every new command and more of the older ones as they
  are converted" — which specific commands lack contracts is not enumerated here.
- Browser build (`solidcraft.io/app`) and its `docs/browser-api.md`/`web-runtime.md` were read at
  doc level only; the desktop MCP surface is the reference implementation upstream says so.

## 4. Verification commands (read-only)

```sh
git -C <clone> rev-parse HEAD                                                     # 3a5195b0…
grep -rhoE 'CommandSpec::new\("[a-z0-9_.]+"' crates/engine/src | sort -u | wc -l   # 539
grep -rhoE 'planned!\("[a-z0-9_.]+"' crates/engine/src | sort -u                  # surface.fillet
awk '/pub fn tool_definitions/,/^\}/' crates/mcp/src/tools.rs | grep -cE '^\s+tool\($|^\s+tool\("'  # 20
grep -n 'DESIGN_EXT' crates/io/src/lib.rs                                         # "sc"
grep -cE '^\| \[' skills/README.md                                                # 17 skills
awk -F'|' 'NR>3 {print $3}' docs/oracle.md | grep -c pass                          # 90 rows (see table)
```
