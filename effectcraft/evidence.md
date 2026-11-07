# EffectCraft — evidence ledger (tag v0.22.0)

Audit basis: this checkout is tag **`v0.22.0`**, commit **`42e3c6a6c119d973aa59ab0437487ea6cae6a15d`** (`git rev-parse HEAD` and `git describe --tags` agree; inspection **2026-11-07**). The installed bundle is **0.22.0**, bundle id `ai.storyteller.effectcraft`, recorded `--version` string `effectcraft 0.22.0`. The GUI was not launched and the app binary was not executed; only `Info.plist` and the repo were read. The previous published skill described v0.21.0 (`7870b5916ae0749d497d880989683bf2946d6c8b`); a read-only extraction of that tree was used for every set and count diff below.

Delta headline, v0.21.0 → v0.22.0: **203 commits, 512 files, +85,465/−2,251**. Engine command ids **681 → 697 (+16, none removed)**: `file.importAep`, `file.exportAep`, `layer.quickSetAnchor`, `mask.setRoundness`, `library.{install,list,loadInstalled,missing,preview,refresh,uninstall,update}`, `effect.helpers.{list,load,scan}`. Effect parameters **2987 → 2988** (Cryptomatte's fifth parameter). Everything else the skill counts is unchanged at v0.22.0 and marked so below.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | `.aep` / `.aepx` import; `.aep` export | `crates/aep/src/{container,import,export}`, `crates/engine/src/cmd/aep.rs` (`file.importAep`, `file.exportAep`), `docs/aep-import.md`, `docs/aep-export.md` | implemented |
| 2 | Import/export refuse losses unless `allowLosses`; `dryRun` returns only the report | `crates/engine/src/cmd/aep.rs`; `docs/aep-import.md` §The command | implemented |
| 3 | Packaged library commands: 8 `library.*` over a SHA-256-checked catalog | `crates/engine/src/system/library.rs` (`CATALOG_URL`, `CATALOG_SCHEMA = 1`, `HOSTS`, `MAX_CATALOG`, `MAX_MODULE`) | implemented |
| 4 | External helpers, protocol v1, opt-in start, blocklist after 3 stops | `crates/helper-host/src/{protocol,serve,client,blocklist}.rs`, `docs/external-helpers.md`, `docs/adr/0001-external-effect-helpers.md` | implemented |
| 5 | WebAssembly plug-in API v1, no imports, `wasmi`, fuel per frame, 1 GiB memory cap | `crates/plugin/src/lib.rs` (ABI table), `crates/plugin/src/wasm.rs` (`MAX_MEMORY`, `FUEL_BASE`, `FUEL_PER_PIXEL`), `crates/effects/src/plugin.rs` (`WASM_API_VERSION = 1`) | implemented |
| 6 | Native plug-in API 2 | `crates/effects/src/plugin.rs` (`PLUGIN_API_VERSION: u32 = 2`; manifest accepts `1..=PLUGIN_API_VERSION`) | implemented |
| 7 | 308 effects / 2988 params / 280 GPU / 21 categories / 0 partial | `docs/effects.md` lines 6–10 (generated from the registry; `effects_doc_is_current` in `crates/effects/src/catalog.rs` fails if the doc is stale); `PARTIAL` is an empty slice | implemented |
| 8 | 76 built-in presets (8 text animators / 23 backgrounds / 23 transitions / 22 behaviors) | `crates/engine/presets/*.json` (`presets` arrays), `crates/engine/src/cmd/anim_presets.rs` | implemented |
| 9 | 697 engine command ids, 82 `specs()` modules | `crates/engine/src/cmd.rs` `command_specs()`; extractor below | implemented |
| 10 | 111 UI-only ids | `crates/ui-egui/src/menus/commands.rs` `UI_COMMANDS` (111 `uic!` entries, all unique) | implemented |
| 11 | 36 MCP tools (27 + 9 bridge-only), 2 resources | `crates/automation/src/tools.rs` (`ToolDef {` ×36, `bridge_only: true` ×9); `crates/automation/src/server.rs` (`effectcraft://document`, `effectcraft://commands`) | implemented |
| 12 | 24 control methods across 21 dispatch arms | `crates/ui-egui/src/control.rs` (`engine.execute \| ui.menu.invoke` share one arm) | implemented |
| 13 | 12 CLI subcommands + `--exr-compression` / `--exr-depth` | `apps/effectcraft-cli/src/main.rs` (`USAGE`, `VALUED`) | implemented |
| 14 | 14 Render Queue formats; EXR compression ×10 and bit depth half/float; scan-line EXR | `crates/project/src/render_queue.rs` (`OutputFormat::ALL`, `ExrCompression::ALL`, `ExrBitDepth::ALL`), `crates/export/src/exr_out.rs` | implemented |
| 15 | Concurrent `--save` CLI runs serialise on an OS lock | `apps/effectcraft-cli/src/project_lock.rs` (lock file `.<name>.lock` beside the project, released by process exit) | implemented |
| 16 | 38 blend modes; 9 layer styles; 7 mask modes | `crates/color/src/blend.rs` (`ALL: [BlendMode; 38]`), `crates/project/src/styles.rs` (`STYLES`, 9), `crates/project/src/props.rs` (`MaskMode::ALL`, 7) | implemented |
| 17 | 13 menu catalogs / 11 panel catalogs | `crates/ui-egui/src/i18n.rs` (`CATALOG_CODES: [&str; 13]`), `crates/ui-egui/src/i18n/ui.rs` (`catalog()` match: ja, zh-hans, zh-hant, uk, pt-br, cs, es, pl, fr, ka, sv = 11) | implemented |
| 18 | 34 panel kinds in `PanelKind::ALL` (+`Viewer(u32)`, `ScriptPanel(u32)`), 13 named workspaces | `crates/ui-egui/src/dock.rs` (`ALL: [PanelKind; 34]`, `workspace_root` match) | implemented |
| 19 | Import formats incl. AVI (partial import, no output) | `crates/project/src/footage.rs` (`VIDEO_EXTENSIONS` incl. `avi`), `crates/media/src/lib.rs` (`STILL_EXTENSIONS` 17, `MODEL_EXTENSIONS` 5, `is_importable`), `crates/media/src/dpx.rs` (`dpx`, `cin`), `crates/engine/src/cmd/file.rs` (`DATA_EXTENSIONS`), `docs/file-format-parity.md` (AVI row) | implemented (AVI partial) |
| 20 | No `.ffx`, `.mogrt`, `.aex`, `.prproj`; `.aepx` not written | `docs/file-format-parity.md`, `crates/engine/src/cmd/timeline.rs` (`.prproj` rejection), `crates/engine/src/cmd/aep.rs` (export is `.aep` only) | not implemented (verified absent) |
| 21 | No hardware video decode/encode; no `.jsxbin`; no Legacy ExtendScript mode; no BridgeTalk messaging | `docs/hardware-parity.md`, `docs/scripting-parity.md` | not implemented (verified absent) |
| 22 | Control channel: no auth, 16 connections, 60 s, 4 MiB lines | `apps/effectcraft/src/control_server.rs` (`MAX_CONNECTIONS = 16`, `MAX_LINE = 4 * 1024 * 1024`, `recv_timeout(60 s)`) | implemented |

## 2. Counts: v0.21.0 → v0.22.0

| Surface | v0.21.0 | v0.22.0 (measured) | Change |
|---|---:|---:|---|
| Engine command ids | 681 | **697** | +16, removed 0 |
| `specs()` modules wired in `command_specs()` | 80 | **82** | +`aep`, +`crate::library` |
| UI-only ids | 111 | **111** | unchanged |
| MCP tools | 36 (27+9) | **36 (27+9)** | unchanged |
| Control methods / arms | 24 / 21 | **24 / 21** | unchanged |
| CLI subcommands | 12 | **12** | unchanged (2 new flags) |
| Render Queue formats | 14 | **14** | unchanged |
| Effects / parameters | 308 / 2987 | **308 / 2988** | parameters +1 |
| GPU / categories / partial | 280 / 21 / 0 | **280 / 21 / 0** | unchanged |
| Blend modes | 38 | **38** | unchanged |
| Layer styles | 9 | **9** | unchanged |
| Menu / panel catalogs | 13 / 11 | **13 / 11** | unchanged |
| Panel kinds / workspaces | 34 (+2) / 13 | **34 (+2) / 13** | unchanged |
| Built-in presets | 76 | **76** | unchanged |

## 3. Count method (repeatable)

Engine ids — the unique first string argument of every `cmd!` / `query!` registry invocation under
`crates/` and `apps/`, test trees excluded, multi-segment ids matched whole:

```sh
# 702 macro sites at v0.22.0 (686 at v0.21.0)
rg -U -o --no-filename '\b(cmd|query)!\s*\(' crates/ apps/ --glob '!**/tests/**' | wc -l
# 697 unique command ids (681 at v0.21.0)
rg -U -o --no-filename -r '$2' '\b(cmd|query)!\s*\(\s*"([a-z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)+)"' \
   crates/ apps/ --glob '!**/tests/**' | sort -u | wc -l
```

Five macro sites carry no literal id (the `cmd!`/`query!` definitions in `crates/engine/src/cmd.rs`
and `crates/engine/src/cmd/frontend.rs`, plus three in `crates/engine/src/cmd/viewer_cmds.rs`/`crates/engine/src/cmd/view.rs` that pass a
pre-built id), which is why 702 − 697.

The published skill's earlier "584/608/680/681" figures mixed a narrower pattern that could not match
multi-segment ids (`layer.mask.shape`, `mask.featherPoint.add`) with a different call-site count.
The extractor above is the one this round used for both tags, so the +16/−0 delta is like-for-like.

Other surfaces are the literal declarations named in the evidence column above; nothing is taken
from README, release notes or `docs/*.md` except the generated, test-enforced `docs/effects.md`.

## 4. Uncertain / not verified

- The 12-entry **audio** extension list is not in this repository: `crates/media/src/lib.rs`
  re-exports `filmcraft_media::AUDIO_EXTENSIONS`, pinned to a FilmCraft revision in `Cargo.toml`
  that no local checkout matches. The list quoted in `SKILL.md` matches a nearby FilmCraft tree and
  the previous skill; treat it as carried, and confirm on a real install with `file.import`.
- `.aep` coverage is quoted from the code paths plus `docs/aep-import.md` / `docs/aep-export.md`
  (last reviewed 2026-11-05). The corpus tests that back those tables are **opt-in** and skip
  themselves when `EFFECTCRAFT_AEP_FIXTURES` is unset (`crates/aep/tests/it/common/mod.rs`), so no
  test evidence was produced in this audit — only code and docs were read.
- No render, build or GUI run happened here. Every "renders within N/255" or fidelity figure is
  carried from `docs/fidelity/README.md` and is **not** re-verified.

## 5. Doc-vs-code drift found at this tag (code wins)

| Doc statement | Code reality |
|---|---|
| "306 effects" in `docs/architecture.md`, `docs/roadmap.md`, `docs/gaps.md`, `docs/hardware-parity.md`, `docs/target-app-parity.md` | 308 (`docs/effects.md`, test-enforced) |
| `docs/target-app-parity.md`: "411 registered engine commands" | 697 ids in the registry |
| `README.md`: "Proprietary project formats … are not supported" | `.aep`/`.aepx` import and `.aep` export landed in this release |
| `docs/gaps.md` gap 4 "no PR CI gate" (older audit called it stale) | closed: `.github/workflows/ci.yml` runs `cargo xtask ci` on pull requests |

## 6. Verification commands (read-only)

```sh
git rev-parse HEAD                                   # 42e3c6a6c119d973aa59ab0437487ea6cae6a15d
git describe --tags                                  # v0.22.0
git diff --shortstat v0.21.0..HEAD                   # 512 files changed, 85465 insertions(+), 2251 deletions(-)
sed -n '6,10p' docs/effects.md                       # 308 / 2988 / 280 / 32 / 0 partial
awk '/static TOOLS/,/^];/' crates/automation/src/tools.rs | grep -cE 'ToolDef \{'   # 36
grep -c 'bridge_only: true' crates/automation/src/tools.rs                          # 9
grep -n 'pub const ALL: \[OutputFormat' crates/project/src/render_queue.rs          # [OutputFormat; 14]
grep -n 'CATALOG_CODES' crates/ui-egui/src/i18n.rs                                  # [&str; 13]
grep -n 'MAX_CONNECTIONS\|MAX_LINE' apps/effectcraft/src/control_server.rs          # 16 / 4 MiB
```

## Round 2026-11-07 (refresh)

- Pinned to `v0.22.0` = `42e3c6a6c119d973aa59ab0437487ea6cae6a15d`; installed bundle 0.22.0
  (`effectcraft 0.22.0`). Previous pin: v0.21.0 = `7870b59…`.
- Re-measured from code at both tags with one extractor: command ids 681 → 697, `specs()` modules
  80 → 82; UI 111, MCP 36 (9 bridge-only), control 24/21, CLI 12, formats 14 all unchanged.
- Generated effect table moved once: parameters 2987 → 2988 (Cryptomatte).
- Corrected this round: `.aep`/`.aepx` are no longer "will not open"; AVI import exists (partial, no
  output); Targa is a Render Queue format (the previous table listed 13 in one place and 14 in
  another); built-in presets are 76, not 54 (the behavior library was missing from the count);
  workspaces are 13, not 15; menu/panel catalogs are 13/11, not 11/8 (the inherited
  "18 languages at v0.21.0" figure is contradicted by `CATALOG_CODES` at both tags); panel kinds
  are 34 in `PanelKind::ALL` plus two parameterised variants; Startup/Shutdown script folders and
  script shortcuts exist, so those scripting gaps were removed.
- Not re-derived from scratch: per-feature render fidelity, GUI behaviour, the audio extension list
  (see §4).
