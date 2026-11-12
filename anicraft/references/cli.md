# AniCraft CLI and MCP — operator reference

Companion to `SKILL.md`. Everything here was read at tag **v0.2.1**
(`d0beaf253274948b55ee9e1107749f9491bff880`) from `crates/cli/src/lib.rs`,
`crates/cli/src/main.rs`, `crates/cli/src/mcp.rs`, `docs/mcp.md` and `docs/plugins.md`, and
cross-checked against the installed 0.2.1 CLI.

## Where the binary is

`anicraft-cli` ships as a separate macOS ZIP and inside the app bundle next to the GUI binary
(the installed app is a universal Mach-O signed with a Developer ID and a stapled notarization
ticket, checked read-only with `codesign`). `anicraft` is the desktop app; `anicraft-cli` is the
headless front end. The CLI has no daemon and opens no listening port: its transports are argv,
stdin/stdout and files.

## Subcommands

| Subcommand | Arguments / flags | What it does |
|---|---|---|
| `info` | `<file\|--sample>` | Prints document JSON: `stage`, `scenes`, `frames`, `movie_frames`, `layers` (with keyframes), `library`, `sounds`, `selection`, `revision`, `dirty`, `history`. |
| `render` | `<file\|--sample> --out <png> [--frame N] [--scale S]` | Renders one frame of the **current scene**. Returns `{written, bytes, frame}`. |
| `render-seq` | `<file\|--sample> --out-dir <dir> [--from A] [--to B] [--scale S]` | Renders the whole movie (every scene in order) to numbered PNGs. |
| `gif` | `<file\|--sample> --out <gif> [--from A] [--to B] [--scale S] [--overwrite yes]` | Animated GIF; `--overwrite yes` sets `"confirm": true`. |
| `commands` | none | The full command registry as a JSON array (id, label, menu, shortcut, params, mutates). |
| `run` | `<file\|--sample> <script.json> [--save <out.anicraft>]` | Runs a JSON **array** of `{"cmd","params"}` steps in order; stops at the first error and names the step. Accepts a UTF-8 BOM. |
| `exec` | `<file\|--sample> <id> ['<json>'] [--save <out.anicraft>]` | Runs one command with a JSON object (default `{}`). |
| `new` | `--out <file.anicraft> [--width W] [--height H] [--fps F]` | New empty document; defaults 1280×720 at 24 fps. |
| `bench` | `[--layers N] [--shapes N] [--frames N]` / `--check yes` | Stress-document timing probe; `--check` compares the default scenario with `TIME_BUDGETS` in `crates/cli/src/lib.rs` and needs a release build. |
| `serve` | `[file\|--sample]` | JSON-lines control channel. |
| `mcp` | `[file\|--sample]` | MCP server (stdio JSON-RPC). |
| `version` / `--version` / `-V` | none | `anicraft-cli 0.2.1`. |
| `help` / `--help` / `-h` | none | The usage block. |

`--plugins <folder>` works on any subcommand (or set `ANICRAFT_PLUGINS`). It first runs
`plugin.reload` with that folder. Headless runs otherwise load **no** plug-ins, so they are
repeatable. Plugin load failures go to stderr and do not stop the run.

`--screenshot <png>` is **not** a CLI feature: `crates/cli/src/main.rs` sees the flag and hands
the whole argv to the desktop `anicraft` binary next to it. It therefore launches the GUI (or
fails if that binary is absent); do not use it in a headless agent loop.

## Frames, params and confirmations

* **CLI flags are 1-based** (`--frame`, `--from`, `--to`); `--frame 0` is rejected with
  "the first frame is 1".
* **Command params and MCP frames are 0-based.** `file.export_png {"frame": 0}` and MCP
  `anicraft_render {"frame": 0}` both mean the first frame.
* Params are JSON objects. Unknown or wrong-typed params are errors; commands document accepted
  keys in their `params` string.
* Irreversible commands are refused unless the params contain `"confirm": true`
  (`crates/engine/src/confirm.rs`, ADR 0004). This includes discarding recovery, deleting
  library items that are in use, replacing files, and overwriting publish outputs.
* Exit status is `0` on success and `1` on error; errors are printed as `error: …` on stderr.
  The CLI prints command results as JSON.

## `serve` — JSON-lines channel

Startup prints one line:

```json
{"ready":true,"app":"AniCraft","version":"0.2.1"}
```

Then one request per line:

```json
{"id":1,"cmd":"draw.rect","params":{"x":10,"y":10,"w":50,"h":50}}
```

One response per line:

```json
{"id":1,"ok":true,"result":{...},"revision":7,"frame":0}
```

Failures keep the same envelope with `"ok":false` and an `"error"` string. A `"commands"` request
returns the registry array. `{"cmd":"quit"}` answers `{"ok":true,"bye":true}` and ends the loop;
EOF also ends it. Blank lines are ignored, and a leading UTF-8 BOM is stripped.

## MCP server

```json
{
  "mcpServers": {
    "anicraft": {
      "command": "anicraft-cli",
      "args": ["mcp", "scene.anicraft"]
    }
  }
}
```

Use `["mcp", "--sample"]` for the sample animation, or `["mcp"]` for an empty document. The
server speaks MCP's stdio transport: JSON-RPC 2.0, one message per line. Protocol revisions:
**2025-06-18** (preferred), 2025-03-26, 2024-11-05. serverInfo: `{"name":"anicraft",
"title":"AniCraft","version":"0.2.1"}`.

### Tools

| Tool | Input | Output | Annotations |
|---|---|---|---|
| `anicraft_commands` | `{filter?: string}` — words matched against id and label | JSON array of command entries (id, label, menu, shortcut, params, mutates) | read-only |
| `anicraft_run` | `{command: string, params?: object}` | `{result, revision, frame, scene}`; command failures come back as a tool result with `isError` | destructive, not idempotent |
| `anicraft_run_script` | `{steps: [{command, params?}, …]}` up to **10,000** steps | `{results, revision, frame}`; on failure `{failed_step, error, done}` with `isError` | destructive, not idempotent |
| `anicraft_document` | `{}` | The same document JSON as `info` | read-only |
| `anicraft_render` | `{frame?: integer ≥ 0, scale?: number > 0 and ≤ 4}` | `image/png` content block (base64) plus a text note; default scale 0.5; longest edge capped at 2048 px | read-only |

Notes:

* Frames in all tool params are **0-based**; `anicraft_render` defaults to the session's current
  frame and rejects a frame past the end with a readable message.
* `anicraft_run_script` stops at the first error; earlier steps stay applied and can be undone
  with `edit.undo`.
* Tool failures are results marked `isError`, so the assistant can read and correct them; only
  malformed calls are JSON-RPC protocol errors.
* Commands act on the session's current scene, layer, frame and selection. Read
  `anicraft_document` first when the target is ambiguous.
* Every call goes through `Session::execute`: params are validated, edits are undoable, and
  confirmation tiers apply exactly as in the app.

## Plug-ins from the CLI

```sh
anicraft-cli exec --sample plugin.run '{"id":"org.anicraft.star-field","params":{"count":200}}' \
  --plugins <folder> --save stars.anicraft
```

* `plugin.list {}` reports installed plug-ins, their folder and the ABI version.
* `plugin.install {path}` validates the `.wasm`; replacing an installed file needs `"confirm": true`.
* `plugin.run {id, params?}` is atomic: on any failure the document is restored, and a successful
  run is one undo step named after the plug-in.
* Plug-ins may call document namespaces only. They cannot call `file.*`, `plugin.*`,
  `publish.*` (except `publish.settings_get`), `prefs.*`, `control.*`, or cut/copy/paste/undo/redo
  (`crates/engine/src/cmds_plugin.rs` `plugin_may_call`).
* Limits: 16 MiB module, 256 MiB linear memory, 1,000,000,000 instructions per run, 5 s wall
  clock (native), 100,000 requests, 1 MiB request / 8 MiB response, 64 MiB of requests per run,
  200 log lines (`docs/plugins.md`; `crates/plugins/src/runtime.rs`).

## Publish from the CLI

```sh
anicraft-cli exec scene.anicraft publish.settings_set '{"format":"html","enabled":true,"output":"web/{name}.html"}'
anicraft-cli exec scene.anicraft file.publish '{}' --save scene.anicraft
```

`publish.settings_get {}` returns the profile and the resolved output for each format.
`file.publish {formats?, confirm?}` writes enabled formats, returns the report, and needs
`"confirm": true` to replace files that already exist. Formats: `html`, `gif`, `video`,
`lottie`, `sprite_sheet`, `png_sequence`, `png`, `svg`, `audio`. Output names are relative to the
document's folder; `{name}` is the document name; names cannot escape the folder and two formats
cannot write the same file (`crates/engine/src/publish.rs`; ADR 0060).

## Video and audio specifics

* `file.export_video` accepts `.mp4`, `.m4v`, `.mov` and `.webm` in code (the documented choices
  are `.mp4` and `.webm`). It streams raw frames to ffmpeg: `libx264`/AAC for MP4,
  `libvpx-vp9`/Opus for WebM. ffmpeg comes from the `ffmpeg` param, else `ANICRAFT_FFMPEG`, else
  `PATH`. It refuses in the browser build (`crates/engine/src/cmds_file.rs`).
* `file.export_audio` writes WAV with `rate` (Hz) and `bits` (16, 24, 32 = float).
* `file.export_sprite_sheet` writes the PNG plus a JSON hash frame map beside it.
* `file.export_lottie` and `file.export_html` take movie frames (`from`/`to`, every scene in
  order), not scene-local frames.

## Environment variables

| Variable | Effect |
|---|---|
| `ANICRAFT_PLUGINS` | Folder of `.wasm` plug-ins for headless runs (same as `--plugins`). |
| `ANICRAFT_FFMPEG` | ffmpeg executable used by video export when the `ffmpeg` param is absent. |
| `ANICRAFT_STAGE_RENDERER` | GUI stage renderer, `gpu` (default) or `cpu` (`src/main.rs`). |
| `ANICRAFT_RENDERER` | GUI graphics backend, `wgpu` or `gl` (`src/main.rs`). |

## Failure modes worth recognizing

| Symptom | Meaning |
|---|---|
| `error: …: file version N is newer than this AniCraft (supports 3)` | The `.anicraft` was written by a newer app; do not try to downgrade by editing the version. |
| `error: …: no file name yet: pass {"path": …}` | `file.save` on an untitled session; pass a path. |
| `error: --frame is 1-based; the first frame is 1` | You passed 0 to a CLI frame flag. |
| `error: … (pass "confirm": true to proceed)` | The command would lose data or replace a file; ask the user first. |
| `error: … is not a movie clip: only the main timeline and movie clips run frame actions` | Frame actions were aimed at a graphic symbol or guide layer. |
| Video export says ffmpeg is missing | Install ffmpeg or pass `ffmpeg` / `ANICRAFT_FFMPEG`; no encoder is bundled. |
