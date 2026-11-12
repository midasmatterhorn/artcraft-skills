# EffectCraft — evidence ledger (tag v0.24.1)

Audit basis: this checkout is tag **`v0.24.1`**, commit
**`582344dd4ef462362c02e56e3094de7af01847ab`** (`git rev-parse HEAD` and `git describe --tags`
agree; inspection **2026-11-12**). The installed bundle is **0.24.1**, bundle id
`ai.storyteller.effectcraft`, and the recorded `--version` string is `effectcraft 0.24.1`. The GUI
was not launched and the app binary was not executed; only `Info.plist` and the repo were read. No
`effectcraft-cli` binary is installed on this machine (the `.app` ships none), so no `--version`,
`info` or `commands` run was possible — every count below is static, from the code. The previous
release this skill described was v0.22.0 (`42e3c6a6c119d973aa59ab0437487ea6cae6a15d`); a read-only
`git archive` extraction of that tree was used for every set and count diff.

Delta headline, v0.22.0 -> v0.24.1: **476 files changed, +35,892/−4,162** (local diff; the
two-commit shallow clone has no commit count, and the upstream compare API caps its file list at
300). Engine command ids **700 -> 703 (+3, none removed)**: `layer.unprecompose`, `journal.export`,
`help.exportRepro`. Everything else the skill counts is unchanged at v0.24.1 and marked so below.

## 1. Capability claims -> evidence -> tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | Native `.ecproj` (schema 2 JSON) + `.ecprojx` XML round-trip; `repaired` list on open | `crates/project/src/lib.rs`, `crates/project/src/settings.rs`, `crates/project/src/limits.rs`, `crates/engine/src/cmd/file.rs` | implemented |
| 2 | `.aep`/`.aepx` import, `.aep` export, loss policy (`allowLosses`, `dryRun`, per-category report with `unlisted`) | `crates/aep/src/{container,import,export}`, `crates/engine/src/cmd/aep.rs`, `crates/aep/src/import/report.rs`, `docs/aep-import.md`, `docs/aep-export.md` | implemented |
| 3 | AEP import covers project tree/settings/comps/layers/transform/expressions/cameras/lights/text/masks/shapes/markers/time remap/styles/sequences and an effect table | `crates/aep/src/import/*.rs`, `crates/aep/src/container/effect_map.rs` | implemented (subset, reported) |
| 4 | AEP import: Lumetri Color with master RGB curve, Hue vs Sat and colour wheels | `crates/aep/src/import/lumetri.rs`, `docs/aep-import.md` §Effects (Lumetri Color) | implemented |
| 5 | AEP import: Puppet arrives with name/switch but without meshes/pins, reported per mesh | `crates/aep/src/import/puppet.rs`, `docs/aep-import.md` | partial (meshes/pins not decoded) |
| 6 | `file.import` takes `.aep`/`.aepx`/`.ecproj`/`.ecprojx` and returns `projects` | `crates/engine/src/cmd/file.rs` (`projects`), `crates/ui-egui/src/menus/frontend.rs` | implemented |
| 7 | Un-precompose with warnings/`force`/`dryRun`, one undo step | `crates/engine/src/cmd/layer.rs` (`layer.unprecompose`), `crates/engine/src/cmd/layer/timing.rs` (`unprecompose`), `crates/ui-egui/src/panels/unprecompose.rs` | implemented |
| 8 | Source: every interactive action is an engine command; 703 registered ids | `crates/engine/src/cmd.rs` `command_specs()` (83 `specs()` modules); count method §3 | implemented |
| 9 | UI-only ids dispatch in the app only: 111 | `crates/ui-egui/src/menus/commands.rs` (`uic!` sites) | implemented |
| 10 | MCP server: 36 tools (27 headless + 9 bridge-only), resources `effectcraft://document`, `effectcraft://commands` | `crates/automation/src/tools.rs` (`ToolDef {` x36, `bridge_only: true` x9), `crates/automation/src/server.rs` | implemented |
| 11 | Control channel: 24 methods over 21 arms; no auth; 16 connections; 4 MiB lines; 60 s timeout | `crates/ui-egui/src/control.rs` (dispatch match), `apps/effectcraft/src/control_server.rs` (`MAX_CONNECTIONS`, `MAX_LINE`) | implemented |
| 12 | A wait for `renderQueue.render` keeps the window responsive; a whitelist of methods answers, the rest error; Stop Render id `scriptRender.stop` | `docs/control-protocol.md` §Waiting for a render, `crates/ui-egui/src/app/frame.rs`, `crates/ui-egui/tests/it/ui_script_render.rs` | implemented |
| 13 | CLI: 13 subcommands, `replay SCRIPT.jsonl [--keep-going]`, `--exr-compression`/`--exr-depth`, `--template`/`--values` | `apps/effectcraft-cli/src/main.rs` (`USAGE`, `FLAGS`, dispatch match) | implemented |
| 14 | Repro scripts: JSON-lines format, `journal.export`, `help.exportRepro`, crash repros in `Repros/`, 64 MiB cap | `crates/engine/src/replay.rs` (`MAX_SCRIPT_BYTES`), `crates/engine/src/cmd/journal.rs`, `docs/agents.md` §Repro scripts, `crates/host/tests/it/repros.rs`, `tests/repros/*.jsonl` | implemented |
| 15 | 308 effects / 2988 parameters / 280 GPU / 21 categories / 0 partial | `docs/effects.md` lines 5–10 (generated; `effects_doc_is_current` in `crates/effects/src/catalog.rs` fails when stale) | implemented |
| 16 | 72 effect display names renamed; ids/params stable; old names still resolve | `crates/effects/src/display_names.rs` (`RENAMED`, 72 rows), `crates/effects/src/lib.rs` (`lookup`, `name_matches`), `docs/feature-naming.md` | implemented |
| 17 | WebAssembly plug-in ABI 2 (`ec_render2` with neighbour frames), ABI 1 still loads; native plug-in API 2 | `crates/effects/src/plugin.rs` (`WASM_API_VERSION = 2`, `MIN_WASM_API_VERSION = 1`, `PLUGIN_API_VERSION = 2`), `crates/plugin/src/lib.rs`, `crates/plugin/src/wasm.rs` (`MAX_MEMORY`, `FUEL_*`) | implemented |
| 18 | Plug-in Library: 8 `library.*` commands, both ABIs, catalog <= 4 MiB, module <= 64 MiB, GitHub hosts only, SHA-256 | `crates/engine/src/system/library.rs` (`CATALOG_SCHEMA`, `HOSTS`, `MAX_CATALOG`, `MAX_MODULE`, `runs_here`) | implemented |
| 19 | External helpers: protocol v1, opt-in start, blocklist after 3 stops, 120 s render / 600 s load timeouts | `crates/helper-host/src/{protocol,client,serve,blocklist}.rs`, `docs/external-helpers.md` | implemented |
| 20 | 14 Render Queue formats; EXR compression x10 and bit depth half/float; output side cap 30 000 px; frame-rate override clamped | `crates/project/src/render_queue.rs` (`OutputFormat::ALL`, `ExrCompression::ALL`, `ExrBitDepth::ALL`, `MAX_OUTPUT_SIDE`) | implemented |
| 21 | 38 blend modes; 9 layer styles; 7 mask modes; 76 presets (8/23/23/22) | `crates/color/src/blend.rs` (`ALL: [BlendMode; 38]`), `crates/project/src/styles.rs` (`STYLES`), `crates/project/src/props.rs` (`MaskMode::ALL`), `crates/engine/presets/*.json` | implemented |
| 22 | 34 panel kinds (+`Viewer(u32)`, `ScriptPanel(u32)`), 15 named workspaces, 13 menu / 11 panel catalogs | `crates/ui-egui/src/dock.rs` (`ALL: [PanelKind; 34]`, `WORKSPACES`), `crates/ui-egui/src/i18n.rs` (`CATALOG_CODES`), `crates/ui-egui/src/i18n/ui.rs` (`catalog()`) | implemented |
| 23 | Confined automation: batch steps cannot use `$N` for params; renders refuse outward links and bound numbered folders | `crates/automation/src/confine.rs`, `crates/automation/src/tests.rs` | implemented |
| 24 | Import formats unchanged (stills 17, video 7, models 5, data 3, interchange 6, DPX/Cineon) | `crates/media/src/lib.rs` (`STILL_EXTENSIONS`, `MODEL_EXTENSIONS`), `crates/project/src/footage.rs` (`VIDEO_EXTENSIONS`), `crates/engine/src/cmd/file.rs` (`DATA_EXTENSIONS`), `crates/interchange/src/lib.rs` | implemented |
| 25 | No `.ffx`, `.mogrt`, `.aex`, `.prproj`; `.aepx` never written; no hardware video decode/encode; no `.jsxbin`/Legacy engine/BridgeTalk | `docs/file-format-parity.md`, `docs/hardware-parity.md`, `docs/scripting-parity.md`, `crates/engine/src/cmd/aep.rs` | not implemented (verified absent) |
| 26 | Render fidelity mostly unmeasured; 1–3/255 on the named effects, Brightness & Contrast up to 6.2/255 | `docs/fidelity/README.md` | carried, not re-verified |

## 2. Counts: v0.22.0 -> v0.24.1

| Surface | v0.22.0 | v0.24.1 (measured) | Change |
|---|---:|---:|---|
| Registered engine command ids | 700 | **703** | +3, removed 0 |
| — of which visible to the `cmd!`/`query!` extractor | 697 | **698** | +1 |
| `specs()` modules wired in `command_specs()` | 82 | **83** | +`journal` |
| UI-only ids | 111 | **111** | unchanged |
| MCP tools | 36 (27+9) | **36 (27+9)** | unchanged |
| Control methods / arms | 24 / 21 | **24 / 21** | unchanged |
| CLI subcommands | 12 | **13** | +`replay` |
| Render Queue formats | 14 | **14** | unchanged |
| Effects / parameters | 308 / 2988 | **308 / 2988** | unchanged |
| GPU / categories / partial | 280 / 21 / 0 | **280 / 21 / 0** | unchanged |
| Blend modes | 38 | **38** | unchanged |
| Layer styles | 9 | **9** | unchanged |
| Mask modes | 7 | **7** | unchanged |
| Menu / panel catalogs | 13 / 11 | **13 / 11** | unchanged |
| Panel kinds | 34 (+2) | **34 (+2)** | unchanged |
| Named workspaces | 15 | **15** | unchanged (last round said 13 — wrong) |
| Built-in presets | 76 | **76** | unchanged |
| WebAssembly plug-in ABI | 1 | **1 and 2** | ABI 2 added, 1 still loads |
| Renamed effect display names | 0 | **72** | naming pass |

## 3. Count method (repeatable)

Engine ids, part 1 — the unique first string argument of every `cmd!` / `query!` registry invocation
under `crates/` and `apps/`, test trees excluded, multi-segment ids matched whole:

```sh
# 703 macro sites at v0.24.1 (702 at v0.22.0)
rg -U -o --no-filename '\b(cmd|query)!\s*\(' crates/ apps/ --glob '!**/tests/**' | wc -l
# 698 unique command ids (697 at v0.22.0)
rg -U -o --no-filename -r '$2' '\b(cmd|query)!\s*\(\s*"([a-z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)+)"' \
   crates/ apps/ --glob '!**/tests/**' | sort -u | wc -l
```

Part 2 — commands the macros cannot see, i.e. ids built as literal `CommandSpec { … }` values or
through the `spec()` helper in `crates/engine/src/cmd/journal.rs`:

```sh
# Excluding the macro definitions in cmd.rs and stubs.rs: batch.rs (engine.batch) and
# content_fill.rs (contentFill.generate, layer.newContentAwareFill); journal.rs builds its two
# ids through spec(), below.
rg -n 'CommandSpec \{' crates/engine/src --glob '!**/tests/**'
# journal.export, help.exportRepro — and test.panic, which is #[cfg(test)] and not registered
rg -U -o -r '$1' 'spec\(\s*"([a-z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)+)"' crates/engine apps/ \
   --glob '!**/tests/**' | sort -u
```

Three ids at v0.22.0 (`engine.batch`, `contentFill.generate`, `layer.newContentAwareFill`) and five
at v0.24.1 (those three plus `journal.export`, `help.exportRepro`) are outside the macro count:
700 -> 703. `journal.rs` also defines `test.panic` under `#[cfg(test)]`, which is not registered.

**Why this changed.** The previous round quoted 697 as "the command registry". That was the macro
count; the registry was 700, because the three literal ids above were never in it. The same
extractor is used at both tags, so the +3 delta is like-for-like; only the total is restated. To
confirm the total on a real install, `effectcraft-cli info --json` prints
`command_specs().len()` under `"commands"`, and `app.capabilities` reports the same number.

Other surfaces are the literal declarations named in the evidence column; nothing is taken from
README, release notes or `docs/*.md` except the generated, test-enforced `docs/effects.md`.

## 4. Uncertain / not verified

- **No live CLI.** No `effectcraft-cli` binary is installed here and the `.app` contains only the
  app binary, so `info`, `commands`, `app.capabilities`, `render` and `replay` were not executed.
  The 703 figure, the 36 MCP tools and the 24 control methods are static counts.
- The `.aep` coverage tables are quoted from the code paths plus `docs/aep-{import,export,format}.md`
  (import note last updated 2026-11-11). The corpus tests behind them are **opt-in** and skip
  themselves when `EFFECTCRAFT_AEP_FIXTURES` is unset (`crates/aep/tests/it/common/mod.rs`); only
  `crates/aep/tests/fixtures/synthetic.aep` ships in the repo, so no import/export round trip was
  produced in this audit.
- The 12-entry **audio** extension list is not in this repository:
  `crates/media/src/lib.rs` re-exports `filmcraft_media::AUDIO_EXTENSIONS` from a FilmCraft revision
  no local checkout matches. It is carried, not re-derived.
- No render, build or GUI run happened here. Every "renders within N/255" figure is carried from
  `docs/fidelity/README.md` and is **not** re-verified.
- The WebAssembly ABI 2 export table is read from `crates/plugin/src/lib.rs` and
  `docs/plugins.md`; no `.wasm` module was loaded.

## 5. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| "306 effects" in `docs/architecture.md`, `docs/roadmap.md`, `docs/gaps.md`, `docs/hardware-parity.md`, `docs/target-app-parity.md` | 308 (`docs/effects.md`, test-enforced) |
| `docs/target-app-parity.md`: "411 registered engine commands" | 703 ids in the registry |
| `crates/engine/src/cmd/query.rs` `PARITY` string (returned by `app.capabilities`): "all After Effects effects present (307 registered)" | 308 |
| `README.md`: "Proprietary project formats and After Effects SDK plug-ins are not supported" | `.aep`/`.aepx` import and `.aep` export have existed since v0.22.0 (subset with a loss report); the SDK plug-in half is still true |
| `docs/gaps.md` row "Opening existing After Effects work ≈ 0% … `.aep` / `.aepx` … can't be read" | stale: the importer/exporter exist and are documented in `docs/aep-*.md` |
| `docs/gaps.md` "Ready for real work ≈ 45% … projects we can't open (`.aep`)" | the parenthetical is stale; the percentage is a self-estimate, not a measurement |
| CLI usage line lists 12 subcommands | 13 exist; `bench` is documented in the usage body, not the one-line synopsis |

## 6. Verification commands (read-only)

```sh
git rev-parse HEAD                                   # 582344dd4ef462362c02e56e3094de7af01847ab
git describe --tags                                  # v0.24.1
git diff --shortstat v0.22.0..HEAD                   # 476 files changed, 35892 insertions(+), 4162 deletions(-)
sed -n '5,10p' docs/effects.md                       # 308 / 2988 / 280 / 32 / 0 partial
awk '/static TOOLS/,/^];/' crates/automation/src/tools.rs | grep -cE 'ToolDef \{'   # 36
grep -c 'bridge_only: true' crates/automation/src/tools.rs                          # 9
grep -n 'pub const ALL: \[OutputFormat' crates/project/src/render_queue.rs          # [OutputFormat; 14]
grep -n 'CATALOG_CODES' crates/ui-egui/src/i18n.rs                                  # [&str; 13]
grep -n 'pub const WORKSPACES' -A 18 crates/ui-egui/src/dock.rs                     # 15 entries
grep -n 'WASM_API_VERSION\|MIN_WASM_API_VERSION' crates/effects/src/plugin.rs        # 2 / 1
grep -n 'MAX_CONNECTIONS\|MAX_LINE' apps/effectcraft/src/control_server.rs          # 16 / 4 MiB
python3 -c "import json,glob;print(sum(len(json.load(open(f))['presets']) for f in glob.glob('crates/engine/presets/*.json')))"  # 76
```

## Round 2026-11-12 (refresh)

- Pinned to `v0.24.1` = `582344dd4ef462362c02e56e3094de7af01847ab`; installed bundle 0.24.1
  (`effectcraft 0.24.1`). Previous pin: v0.22.0 = `42e3c6a…`.
- Re-measured from code at both tags with one extractor: registry ids 700 -> 703 (+3),
  `specs()` modules 82 -> 83; UI 111, MCP 36 (9 bridge-only), control 24/21, formats 14, effects
  308/2988, blend 38, styles 9, masks 7, panels 34, presets 76, catalogs 13/11 all unchanged.
- Corrected this round: command total restated as 703 (the macro-only 697 was three short);
  workspaces 15 not 13; CLI 13 not 12; WebAssembly ABI 2 not 1; menu label "Adobe After Effects
  Project…"; 72 display names renamed with ids and legacy aliases intact.
- New surfaces added to the skill: replay/journal, un-precompose, the AEP import growth (Lumetri,
  Puppet, quick-wins, third-party effects, ArtBox framing, `unlisted` report counts), the
  render/GPU memory settings, the sequence/text/stretch limits, the control-channel render wait and
  the tightened confinement.
- Not re-derived from scratch: per-feature render fidelity, GUI behaviour, the audio extension
  list, `.aep` corpus results (see §4).
