# EffectCraft extensions: plug-ins, helpers, the Plug-in Library, scripts (v0.22.0)

Reference for the surfaces in "Extensions" in `SKILL.md`. Grounded in `crates/effects/src/plugin.rs`,
`crates/plugin/src/{lib,wasm}.rs`, `crates/helper-host/src/`, `crates/engine/src/system/library.rs`,
`crates/engine/src/cmd/effect.rs`, `docs/plugins.md`, `docs/external-helpers.md`,
`docs/publishing-plugins.md` and `docs/adr/0001-external-effect-helpers.md`.

**Everything here executes third-party code.** Load a plug-in or a helper only when the user asked
for that plug-in or helper by name, prefer the catalog path over an arbitrary file path, and never
install into an app another process is using.

## Three kinds of plug-in, three ABIs

| Kind | ABI | Runs | Commands |
|---|---|---|---|
| WebAssembly effect plug-in | `.wasm` / `.wat`, **plug-in API v1** | in-process, `wasmi` interpreter | `effect.plugins.load`, `effect.plugins.install`, `effect.plugins.list` |
| Native plug-in (API v2) | Rust / native, `PLUGIN_API_VERSION = 2` | in-process (built in) | manifest `api` may be 1 or 2 (`crates/effects/src/plugin.rs`) |
| External effect helper | its own manifest, API 1–2, **helper protocol v1** | a separate child process | `effect.helpers.scan`, `effect.helpers.load`, `effect.helpers.list` |

`WASM_API_VERSION = 1` is unchanged in v0.22.0. A `.wasm` module declares `ec_api_version`, which
must return `1`. API 2 additions (layer parameters, host services) are what native code and helpers
get; they are not part of the WebAssembly ABI.

## WebAssembly plug-ins

- A module must have **no imports** and export `memory`, `ec_api_version`, `ec_manifest_ptr`,
  `ec_manifest_len`, `ec_alloc` and `ec_render(pixels, width, height, params, nparams, time, scale)`.
  Pixels are premultiplied RGBA `f32` in linear memory; `ec_render` processes them in place.
- Sandbox: the `wasmi` interpreter with deterministic floats, no files, network or clock, a fuel
  limit per frame, one instance, at most **1 GiB** of linear memory, and a manifest cap of 1 MiB
  (`crates/plugin/src/wasm.rs`). The crate's own docs state that a plug-in cannot escape its
  sandbox, hang the app or render differently on another machine — but it can still be *wrong*,
  so check its output.
- The `wasm` feature is enabled on native builds by the host crate (`crates/host/Cargo.toml`,
  `[target.'cfg(not(target_arch = "wasm32"))'.dependencies]`); without it, loading reports that
  WebAssembly plug-ins are unavailable.
- `effect.plugins.load {path | folder}` — loads for this session (`API v1`).
- `effect.plugins.install {path | folder | bundle?}` — copies a `.wasm` into the Plug-ins folder so
  it loads on every start; a **bundle** folder means every `.wasm` goes into the Plug-ins folder and
  every `.jsx` becomes a ScriptUI panel.
- `effect.plugins.list` → `{api, wasm, helpers, plugins: [{id, name, category, version, author,
  source, params, error}]}`; `source` says whether an effect came from a file or a helper
  (`helper: …`).

## External effect helpers

A helper is a separate program that offers effects; each effect renders through it as an ordinary
plug-in effect (properties, keyframes, expressions, Effect Controls). It exists to run **native**
code — an OpenFX host, for example — outside EffectCraft's process, so a crash is an error on the
effect rather than a crash.

- **Install:** put `effectcraft-helper-<name>` (`.exe` on Windows) in `helpers/` next to the app, in
  `helpers/` in the settings folder, or in a folder named by `EFFECTCRAFT_HELPER_PATH` (a path list;
  entries may be programs or folders, one level of subfolder is searched).
- **Start:** nothing starts a helper unless asked. `effect.helpers.scan` starts them; setting
  `EFFECTCRAFT_HELPERS=1` starts them at launch (an environment variable, not a setting, so writing
  the settings folder cannot turn it on). `effect.helpers.load {path}` hands a file or folder (for
  example a folder of `.ofx` plug-ins) to the helpers that accept it.
- **Protocol v1:** one JSON object per line on stdin; replies on stdout prefixed with `@ec-helper `;
  every object has an `op`; lines are capped at 256 MB. Pixels never travel through the pipe — the
  host creates a frame-exchange file and passes an image ref. The helper is started with
  `--effectcraft-helper` and may keep state in `EFFECTCRAFT_HELPER_STATE_DIR`.
- **Failure handling:** a failed render leaves the frame as it was and puts a warning after the
  effect's name. An effect that stops its helper three times is turned off and listed in
  `helper_blocklist.txt`; `effect.helpers.scan {"retry": true}` turns it back on. A helper that
  stops five times in a minute stays off until the next scan.
- **Timeouts:** `EFFECTCRAFT_HELPER_TIMEOUT` (seconds per render step, default 120) and
  `EFFECTCRAFT_HELPER_LOAD_TIMEOUT` (start-up, describe, load; default 600); an idle helper is
  pinged after 30 s.
- **Desktop only.** The web build has no helpers. An agent confined with `--automation-read-root` /
  `--automation-write-root` cannot run `effect.helpers.scan` or `effect.helpers.load`, and scripts
  can run them only with Settings ▸ Scripting & Expressions set to allow file writes and network.

## The Plug-in Library

One reviewed catalog (`index.json` in a Git repository) lists community packages with version,
plug-in API, the oldest EffectCraft they need, and the release asset URL plus its **SHA-256**. The
default catalog is the community one (`storytold/effectcraft-plugins`); `library.refresh` accepts a
`https://` or `file://` catalog of your own.

| Command | Does |
|---|---|
| `library.list {query?, tag?, installed?}` | catalog + package status (`latest`, `installed`, `updateAvailable`, `needsNewerApp`, `loaded`, `restartNeeded`, `previewed`, `unlisted`) |
| `library.missing` | effects this project uses that are not installed, and the packages that provide them |
| `library.refresh {catalog?, wait?}` | fetch and cache the catalog (cached as `catalog.json`, so the list works offline) |
| `library.preview {id, version?, wait?}` | download and render the effect on a sample frame **without installing** |
| `library.install {id, version?, wait?}` | download, verify the SHA-256, load |
| `library.update {id?, wait?}` | update one package or every package with an update |
| `library.uninstall {id}` | remove; its effects stay registered until the next start |
| `library.loadInstalled` | load what is installed (the app runs it at start-up) |

- Downloads use the system's `curl` (like trained models), so no networking code is linked in. Only
  `https://` URLs on GitHub's hosts are fetched and a redirect ending elsewhere is refused; a local
  `file://` catalog may name local files. Catalog ≤ 4 MiB, module ≤ 64 MiB.
- Installed packages live under `<Plug-ins>/Library/<id>/<version>/` with an `installed.json` that
  records the SHA-256 they were installed with.
- **Effects cannot be unregistered**, so installing, updating or removing a package that is loaded
  takes effect at the **next start** — the list says so (`restartNeeded`). Plan an app restart into
  any workflow that installs a plug-in.

## Scripts and ScriptUI (for contrast)

- `.jsx` / `.js` run against the After Effects object model; `Scripts/Startup/` and
  `Scripts/Shutdown/` run in alphabetical order at launch and quit, each in its own global scope.
- ScriptUI panels are dockable, reopen at the next launch, and can be given a shortcut in Edit ▸
  Keyboard Shortcuts.
- No `.jsxbin`, no separate Legacy ExtendScript engine mode, no inter-application `BridgeTalk`
  messaging.

## Do not

- Install, load or scan from an agent run the user did not ask for; helpers start **native
  processes**.
- Assume a plug-in effect is registered after `library.uninstall` — it is not until a restart.
- Treat a plug-in's declared parameters as validated input; a broken plug-in fails one frame, not
  the app, but the failure is easy to misread as an EffectCraft bug.
- Assume a helper is sandboxed: it is a child process running native code, isolated by a protocol
  and by error handling, not by a security boundary (`docs/adr/0001-external-effect-helpers.md`).
