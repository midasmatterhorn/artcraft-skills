# ArtCraft Studio — round 2026-11-07 changes

Re-pinned: **new skill** (no previous baseline) -> `artcraft-v0.41.1` (`07ebde145`, Info.plist 0.41.1,
bundle `ai.artcraft.app`).

## Corrected / re-measured

- First audit, so nothing was corrected from an earlier skill; every quoted count was derived from the
  tag in this round (methods in `evidence.md` §2): **93 model ids** (24 image / 46 video, 3 deprecated /
  5 audio / 11 mesh / 7 splat), **62 Tauri commands**, **17 routed UI tabs**, **9 task statuses**,
  **7 task types**, **11 user feature flags**, **14 declared providers** (six wired), **8 job-status
  states**, **7 task-DB version**, **82 ArtCraft routing rows** (22/39/5/11/5).
- Corrected the README's "62-model catalog" framing: that number is product copy for an earlier
  ArtCraft-provider catalog. The code space and the live server list are both larger, and the live list
  is not in the repo.
- Recorded the surfaces an agent is most likely to get wrong: **no CLI, no MCP server, no control
  channel, no AppleScript** (unlike the other Craft apps); **no local project file** (video editor uses
  WebView IndexedDB; 3D scenes are uploaded as server media files); **`artcraft-native` is source-only**
  and is not the installed app.
- Flagged two non-functional tools that look shipped: the image and video **watermark removers** only wait
  2 s and show a success toast — no upload, no job, no file (`…/PageImageWatermarkRemover/ImageWatermarkRemover.tsx`,
  `…/PageVideoWatermarkRemover/VideoWatermarkRemover.tsx`). A user reporting "it says done but nothing changed" is
  describing this, not a failed job.
- Documented the Omni API as documented-and-typed but server-implemented: the repo holds
  `_docs/artcraft_omni_api.md` plus the request/response types and the undocumented upload endpoints,
  while the desktop itself calls the cookie-authenticated `/v1/omni_gen/*` endpoints.

## Method

- Read the tag's `README.md`, `AGENTS.md`, `Cargo.toml`, `_docs/`, `docs/`, `packaging/`, CI workflows,
  the Tauri config/capabilities, the desktop crate (`core/`, `services/`), the API crates
  (`artcraft_api_defs`, `artcraft_client`, `artcraft_router`), the shared schema crates and the task
  migrations; then re-derived every count with the `grep`/`awk` commands listed in `evidence.md` §5.
- Cross-checked the code against the installed bundle's `Info.plist`, `codesign -dv` and
  `spctl -a -vv`. **The binary was never executed** — it is a Tauri GUI app with no `--version` flag and
  no CLI.
- Inspected the local data root read-only (directory listing plus `sqlite3 "file:…?mode=ro"` queries). No
  credential file, cookie jar or log content was read or reproduced.
- Live probing was deliberately avoided: no generation request, no API-key call, no network request, no
  build, no test run, no commit.

## Unchanged

- Nothing — this is the first release of this skill. There is no carried-forward paragraph, and no older
  delta history to fold into this file.

## Known gap in this round

- Server behaviour is documented but not exercised: endpoint status codes, anonymous access to the model
  list, per-model credit prices and current model availability all come from the repo's docs, types and
  `#[ignore]`d live tests, not from live calls. Windows/Linux packaging and the riscv64/Flatpak/OCI
  artifacts were read, not run. Credits, subscription and moderation flows were intentionally not touched.
