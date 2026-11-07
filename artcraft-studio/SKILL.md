---
name: artcraft-studio
description: ArtCraft Studio is the ArtCraft desktop app for generating AI images, video, music, sound, 3D meshes and Gaussian-splat worlds — a Tauri 2 workspace (React UI over Rust API clients) that drives cloud models through ArtCraft's own Omni API, with your own fal key or Midjourney/Sora/Grok/World Labs logins as alternative providers. Trigger this skill whenever the user mentions ArtCraft Studio, "the ArtCraft app", the Storyteller API, the Omni API, `artcraft_api_` keys, `~/Artcraft` data, a `tasks_v7.sqlite` task queue, or asks what the app can or cannot do, how to draft prompts and reference images for it, how to call its generation API from code, how to poll or cancel a generation job, how to find, download or verify media it produced, which models and providers exist, why a generation failed or cost credits, or whether it can be scripted or automated — including when they never name the app and just describe the job ("generate a 6-second video from this still", "make a product image with Nano Banana", "turn this photo into a 3D model", "why did my generation fail", "read the app's job history"). It is a cloud-billed creative workspace, not an editor — there is no local inference, no local project file, no CLI, no control channel and no MCP server, so never promise offline generation, GUI automation or a project format — and never touch its stored cookies or keys.
---

# ArtCraft Studio

**Audit basis.** First audit against tag **`artcraft-v0.41.1`**, commit **`07ebde1454d4bc99f0d9add90618fb4d871f6b1d`** (`git rev-parse HEAD` in the pinned checkout confirms; commit title "fix(ci): exclude desktop GUI crates and pin architecture for FreeBSD CI", 2026-11-06). The code agrees with the installed bundle: `crates/desktop/artcraft/src/version.rs` declares `ARTCRAFT_VERSION = "0.41.1"` and `crates/desktop/artcraft/tauri.conf.json` pins `"version": "0.41.1"`, `"identifier": "ai.artcraft.app"`. **The app has no `--version` CLI** — it is a Tauri binary, so the installed bundle was read as a file, never executed: it reports `CFBundleShortVersionString` 0.41.1, `CFBundleIdentifier` `ai.artcraft.app`, `CFBundleExecutable` `artcraft`, a universal x86_64+arm64 Mach-O, signed and notarized. Inspection date **2026-11-07**.

**First audit — no predecessor skill.** There is no vOLD → v0.41.1 delta to report; this file is the baseline. Everything quoted below was derived from the tag named above, and the per-claim evidence lives in `evidence.md`. Nothing here was carried forward from an earlier release.

## Overview

ArtCraft Studio is the public desktop client of ArtCraft ("The IDE for artists", `README.md`): a Tauri 2 app — Rust backend in `crates/desktop/artcraft`, React/TypeScript frontend in `frontend/apps/artcraft` — that composes prompts, reference images and 3D scenes locally and sends the actual generation to ArtCraft's cloud. Repo `storytold/artcraft`, MIT or Apache-2.0 at your option; the backend services, the web app and the model catalog live in a separate private repo (`AGENTS.md`), which is why several endpoints here exist only as shared wire types. Maturity is pre-1.0 (0.41.1): every generation path is a network round trip to an authenticated, credit-billed account. The repo also contains a second, pure-Rust egui client (`artcraft-native/`) that is **not** the shipped app — see Known limitations.

## Capabilities (verified)

### Generation — five modalities, all cloud-side

- **One dispatch path.** The desktop does not hardcode model capabilities: it posts a JSON field map to `/v1/omni_gen/generate/{image,video,audio,mesh,splat}` and a cost probe to `/v1/omni_gen/cost/{modality}`, renaming per-modality fields on the way (`crates/desktop/artcraft/src/core/commands/generate/omni/dispatch.rs`, `crates/desktop/artcraft/src/core/commands/generate/omni/request.rs` `Modality`). Unknown or newer model ids and option strings pass through untouched, so the server can add models without an app update.
- **Images** (`generate_image_command`): text-to-image, image edit/remix with reference images, inpainting/masks, angle manipulation (`adjust_horizontal_angle`/`adjust_vertical_angle`/`adjust_zoom`), batch counts, and background removal as a queued job that reports `image_cdn_url` back to the page. Long-standing legacy request shapes still exist for `recraft_3`, `flux_pro_kontext_max`, `flux_dev_juggernaut`, `flux_pro_1` (`crates/desktop/artcraft/src/core/commands/generate/omni/request.rs` `uses_legacy_image_endpoint`).
- **Video** (`generate_video_command`): text-to-video and image-to-video with start/end keyframes, reference images/videos/audio, duration, aspect ratio, resolution, bitrate, `generate_audio`, batch count (`crates/api_clients/artcraft/artcraft_api_defs/src/omni_gen/cost_and_generate_requests/omni_gen_video_cost_and_generate_request.rs`).
- **Audio, mesh and splat**: music/sound (Suno family, Seed Audio), image→3D object (Hunyuan 3D, Tripo3D, Meshy, Rodin) and image→Gaussian world (Marble, TripoSplat). Audio and mesh are **ArtCraft-only** — asking for another provider returns "No direct provider adapter is configured for this modality" (`generate_audio_command.rs`, `generate_mesh_command.rs`).
- **Task types the queue understands**: `image_generation`, `image_inpaint_edit`, `video_generation`, `audio_generation`, `object_generation`, `gaussian_generation`, `background_removal` — 7 (`crates/schema/public/enums/src/tauri/tasks/task_type.rs`).

### Model space

- **93 model ids in code**: 24 image, 46 video (3 `#[deprecated]`), 5 audio, 11 mesh, 7 splat (`crates/schema/public/enums/src/common/generation/common_*_model.rs`). Full id tables and the shared option enums are in `references/model-ids.md`.
- **The live menu is remote.** `GET /v1/omni_gen/models/image` and `…/video` return per-model capabilities — `text_prompt_max_length`, `negative_text_prompt_supported`, `image_refs_max`, `aspect_ratio_options`, `resolution_options`, `quality_options`, `batch_size_*`, `is_disabled` — decoded permissively with `Unknown(String)` catch-alls so a newer server cannot break an older build (`crates/api_clients/artcraft/artcraft_client/src/endpoints/omni_gen/models/image/omni_gen_list_image_models.rs`). The desktop calls it **without credentials** and caches for 60 s, so the catalog is presumably anonymously readable; the repo's own live test hits production with `maybe_creds: None` and asserts success (that test is `#[ignore]`d and was not re-run for this audit — treat anonymous access as **claimed by code/test, unverified live**).
- **`artcraft_router`** can route a model to a second provider (fal, World Labs, Grok API, gmicloud, kinovi) for the same id — e.g. 39 ArtCraft video rows against 22 fal rows. That routing table is a superset of what the desktop exposes; the app's own menu is the server list.

### Providers

- **ArtCraft** (default, credit-billed, cookie/session auth) — the only path for audio and mesh.
- **fal** — bring your own API key; the only provider the desktop's router maps to a credential key (`generate_image/providers/artcraft_router/handle_router.rs` `map_provider_to_credential_key`). Stored as `credentials/fal.api_key.txt`.
- **Midjourney, Sora 2, Grok, World Labs** — web-login sessions captured into the app's own cookie stores; used for images (Midjourney), video (Sora 2, Grok) and worlds (World Labs legacy splat path). Each has a provider login window and a credential file under `credentials/`.
- **Provider priority is deprecated**: the remaining enum is `artcraft | sora | fal`, default order ArtCraft → Sora → Fal (`crates/desktop/artcraft/src/core/state/provider_priority.rs`); the commands that set it are under `core/commands/providers/deprecated/`.
- **14 provider values exist in the shared enum but only six are wired by 0.41.1**: `higgsfield`, `krea`, `leonardo`, `magnific`, `openart`, `picsart`, `pixverse` and `runway` are declared ahead of integration (`crates/schema/public/enums/src/common/generation_provider.rs`).

### Account, credits and gating

- **Credits model**: `free_credits`, `monthly_credits`, `banked_credits`, `sum_total_credits` (`crates/api_clients/artcraft/artcraft_api_defs/src/credits/get_session_credits.rs`); the app refetches after every enqueue (`CreditsBalanceChangedEvent`).
- **Spending failures are typed**: HTTP 402 becomes `ApiError::PaymentRequired`, and the router lifts it to `ProviderBillingError` alongside Midjourney "subscription required", fal billing and kinovi billing (`crates/api_clients/artcraft/artcraft_client/src/utils/filter_bad_response.rs`, `crates/api_clients/artcraft/artcraft_router/src/errors/artcraft_router_error.rs`).
- **Per-account gates**: `SessionUserInfo.maybe_feature_flags` carries 11 flags including `api_key`, `seedance_whitelist`, `minimax_priority` and `explore_media` (`crates/schema/public/enums/src/by_table/users/user_feature_flag.rs`); `can_access_studio` gates studio access. Model availability can therefore differ per account.

### Library, downloads, media

- **Generated media lives on the server** as media files with tokens, batch tokens, `cdn_url`s and thumbnail templates; the app records the primary result on the task row (`on_complete_primary_media_file_cdn_url` etc.) and lists batches via `list_batch_generated_redux_media_files`.
- **Downloads** go to the preferred directory — default is the **OS Downloads folder**, with `~/Artcraft/downloads` only as a fallback (`core/state/app_preferences/preferred_download_directory.rs`). Names default to `{model_slug}_{YYYY-MM-DD-HH-MM-SS}[_{batch_index}].{ext}` with `seedance_2p0` rendered `seedance_2.0`; a `custom_format` template supports `{model}`, `{date}`, `{YYYY}{YY}{MM}{DD}{HH}{mm}{SS}`, `{batch_index}` and is sanitised against path separators, `..`, control characters and Windows device names (`preferred_download_filename.rs`).
- **Auto-download is off by default**; when enabled it downloads before the task is marked complete and checkpoints each URL in `state/auto_download_<task_id>.json` so a retry does not duplicate files (`core/utils/auto_download.rs`).

### Workspaces (the UI)

17 tab branches are routed in `frontend/apps/artcraft/app/src/pages/MainApp.tsx` (`grep -c '^    case "'` = 17): Apps index, 2D canvas compositing, 3D scene, Text to Image, Image to Video, Create Audio, Video Editor, Moodboard, Storyboard, Angles, Background Change, Remove Background, Image→3D Object, Image→3D World, Video Frame Extractor, Video Watermark Remover, Image Watermark Remover. A `TabId` named `EDIT` is declared in `pages/Stores/TabState.ts` but has no branch — it renders nothing.

### Platform

- **macOS**: universal, signed, notarized (Gatekeeper accepts it; Developer ID "Learning Machines LLC"). **Windows**: Tauri publish workflow present. **Linux**: x86_64 and aarch64 AppImage/DEB/RPM/tar.zst/Arch/Flatpak/OCI, plus riscv64 DEB/RPM/tar only, with Flatpak `ai.artcraft.app` on GNOME 51 (`packaging/linux/README.md`, `packaging/linux/flatpak.yml`, `.github/workflows/artcraft-*-publish.yml`). **FreeBSD is not shipped**: the FreeBSD CI job builds and tests the shared crates only, with `--exclude artcraft --exclude artcraft_native --exclude tauri-plugin-http` (`.github/workflows/freebsd.yml`).

## Known limitations and not-implemented

Read this before assigning work — most of these are hard stops, not bugs.

- **No local inference, no offline mode.** Every generation, cost estimate, model list and media lookup is an HTTPS call to `api.storyteller.ai` (or the `localhost:12345` dev host). The app cannot generate without a live account, credits and network.
- **No CLI, no MCP server, no control channel, no AppleScript.** There is no `clap` dependency anywhere in the workspace, no `env::args` use and no listener in `crates/desktop/artcraft` or `artcraft-native`; the **62** registered `#[tauri::command]`s (`crates/desktop/artcraft/src/lib.rs` `generate_handler!`) are webview IPC only. The macOS bundle ships exactly one file in `Contents/MacOS` (`artcraft`) — no CLI beside it, and no `NSAppleScriptEnabled`/`.sdef`. Unlike PhotoCraft/WordCraft and the other Craft apps, there is **no `--control` port to connect to**.
- **MCP here is server-side session management, not a local tool server.** `crates/schema/public/tokens/src/tokens/mcp_session*.rs` and `crates/api_clients/artcraft/artcraft_api_defs/src/mcp_sessions/` define `POST /v1/mcp/session/create|refresh|revoke` and a `private_session_token` for a **hosted** MCP endpoint; `PlatformType::Mcp` is a request-classification value. Nothing in this repo runs an MCP server on your machine.
- **The two watermark removers are stubs.** `pages/PageImageWatermarkRemover/ImageWatermarkRemover.tsx` and `pages/PageVideoWatermarkRemover/VideoWatermarkRemover.tsx` wait 2 s (`setTimeout`) and then toast "Watermark removal completed!" without uploading anything or calling the backend — nothing is processed and no file is produced. If a user reports that watermark removal "says done but changes nothing", this is why; do not retry it as if it were a failing job.
- **No local document or project file.** The 2D canvas, scene and moodboard keep state in memory and lose it on restart; 3D scenes are saved by uploading a JSON file to `/v1/media_files/upload/new_scene` (engine category `scene`) and re-loaded from `/v1/media_files/file/{token}` (`frontend/apps/artcraft/app/src/pages/PageScene/useTauriPageSceneAdapter.tsx`). The video editor is the only page with openable projects, and it stores them in the **WebView's IndexedDB** — database `video-editor`, object store `projects`, version 1, "no migration logic — phase 1 schema only" (`frontend/libs/components/video-editor/src/lib/adapters/default/indexeddb-project-storage.ts`). Server-side project endpoints exist as wire types only (`crates/api_clients/artcraft/artcraft_api_defs/src/media_file/project/upload_new_editor_2d_project.rs`, `…_mood_board_…`, `…_scene_3d_…`, `…_video_timeline_…`) and no frontend code calls them.
- **The Omni API's HTTP surface is documented, not implemented here.** `_docs/artcraft_omni_api.md` documents `POST /v1/omni_api/generate/video|image`, `GET /v1/omni_api/job_status/job/{token}` and `…/batch`, and the repo carries the request/response types plus the (undocumented) upload endpoints `POST /v1/omni_api/upload/{image,video,audio}`; the client code lives in the server repo. Do not assume endpoints beyond these.
- **API keys are gated per account** by the `api_key` user feature flag; the guide states access is enabled by staff and that the secret is shown once. Never promise a key.
- **`artcraft-native` does not ship.** It is a real egui app over the same crates (`~/Artcraft/credentials/native_session.json`, `state/native_provider_jobs.json`, `/v1/omni_gen/*`, `/v1/jobs/session`), but no release workflow builds or uploads it — it appears in CI only to be excluded. Document it as source-only, never as "the ArtCraft app".
- **Dead code at this tag** (do not cite as features): `app_assets_dir.rs` (`assets/`) and `app_weights_dir.rs` (`weights/`) — the latter is never instantiated, so `~/Artcraft/weights` does not exist; `core/commands/generate/generate_image/providers/grok/` and `…/sora/` are not in the module tree; the background-removal command carries `TODO`/`FIXME` about provider routing (`enqueue_image_bg_removal_command.rs`).
- **Docs disagree with code.** `README.md` advertises a "full 62-model catalog"; the 0.41.1 code space is 93 ids and the ArtCraft router alone has 82 model rows (22 image, 39 video, 5 audio, 11 mesh, 5 splat) — the server list, not the README, is authoritative. `MainApp.tsx`'s comment says "13 tab branches" beside 17.
- **Not verified by this audit**: Windows and Linux behaviour, the riscv64/Flatpak packages, and live server responses (no generation was run — that costs credits on a real account).

## How to operate

### Launch and first run

```sh
open -a ArtCraft          # GUI only; there is no headless entry point
```

On first launch the app creates its data root `~/Artcraft` with `assets/`, `credentials/`, `downloads/`, `settings/`, `state/`, `temp/` and the log `artcraft_debug.log` (`core/state/data_dir/app_data_root.rs`; `get_default_data_dir` = home directory + `Artcraft`). Sign in with the website-approval (device code) flow, a username/password, or a new account; the session cookie is installed into a native cookie jar and kept out of JavaScript and WebView storage (`docs/website-login.md`).

Point the app at a different API with `settings/env_configs.json`: `{"version":"1","storyteller_host":"localhost","storyteller_port":12345}` or `production` (default). `RUST_LOG=debug|info|warn|error|off` raises or lowers logging (substring match) into `artcraft_debug.log`; default level is `info` (`core/lifecycle/startup/tasks/set_app_log_level.rs`).

### The generation round trip

1. Pick a tab, write the prompt, attach references/keyframes (media tokens or local uploads).
2. Optionally ask the app for a price first — the cost estimate is its own IPC command (`crates/desktop/artcraft/src/core/commands/cost_estimate/estimate_*_cost_command.rs`) posting to `/v1/omni_gen/cost/{modality}`; generating does not call it for you.
3. The generate command posts the request and the server returns an inference job token (plus `all_job_tokens` when a batch creates several jobs); the app writes a row into `state/tasks_v7.sqlite` with `provider='artcraft'` and `provider_job_id=<job token>` (`omni/dispatch.rs` `insert_into_task_database_with_frontend_payload`).
4. A background thread polls `GET /v1/jobs/session` **every 5 s** (60 s back-off on `429`, 30 s on other errors) and matches returned jobs to local tasks by token (`services/storyteller/threads/storyteller_task_polling_thread/`).
5. On success the task row gains the primary media token, media class, `cdn_url` and thumbnail template; the UI shows the item in the library, and auto-download (if enabled) fetches it before completion is recorded.
6. Third-party providers poll on their own cadence: 10 s idle, 2 s while jobs are pending, 1 s between fal polls, 30 s after an error (`core/threads/third_party_task_polling_thread/`).

### Inspecting local state (read-only, app closed)

```sh
sqlite3 "file:$HOME/Artcraft/state/tasks_v7.sqlite?mode=ro" \
  "select task_status, task_type, model_type, provider, provider_job_id, created_at
     from tasks order by created_at desc limit 20;"
```

- **Use `?mode=ro`, not `?immutable=1`.** The database is WAL-mode; with `immutable=1` the `tasks` table is invisible because it lives in the `-wal` file. Keep `tasks_v7.sqlite`, `-wal` and `-shm` together if you copy them.
- Useful columns: `task_status` (9 values: `pending`, `started`, `complete_success`, `complete_failure`, `attempt_failed`, `dead`, `cancelled_by_user`, `cancelled_by_provider`, `cancelled_by_us`), `task_type`, `model_type`, `provider`, `provider_job_id`, `on_complete_primary_media_file_cdn_url`, `on_failure_type`, `on_failure_message`, `prompt_token`, `queue_status_url`, `queue_response_url`, `created_at`/`updated_at`/`completed_at` (unix seconds). Schema: `_database/sql/artcraft_migrations/20250708000000_create_tasks_table.sql`; table version constant `TASK_DATABASE_VERSION = 7`.
- `settings/app_preferences.json` holds the download directory and filename format, `auto_download` and sound settings; `settings/provider_preferences.json` holds provider ordering; `state/window_size.json` / `window_position.json` are window geometry; `state/auto_download_<task>.json` are download checkpoints.
- **What the DB cannot tell you**: the prompt text (only an opaque `prompt_token`), the model's parameters, the credit price actually charged, or the local path of a download that was moved. Do not infer a failure reason from an empty `on_failure_message` — non-terminal failures can leave it null.

### Secret material — do not read

`credentials/` and the WebView cookie jar are credentials, not state:

- `credentials/artcraft_session.txt`, `artcraft_avt.txt` — the ArtCraft session cookie and visitor id.
- `credentials/fal.api_key.txt`, `replicate.api_key.txt` — provider API keys.
- `credentials/grok.web_login.toml`, `midjourney.web_login.toml`, `higgsfield.web_login.toml`, `runway.web_login.toml`, `midjourney_cookies.toml`, `sora_cookies.txt`, `sora_bearer_token.txt`, `sora_sentinel_token_store.json`, `worldlabs_*.txt|json`, `grok_cookies.txt`, `midjourney_state.json` — third-party session captures (`core/providers/credentials/provider_credential_key.rs`, `core/state/data_dir/app_credentials_dir.rs`).
- The Tauri HTTP plugin also keeps a JSON cookie store `.cookies` under the app **cache** directory (`crates/vendor/tauri-plugin-http/src/lib.rs`, `app_cache_dir()`), which is why `artcraft-native` can import the Tauri session at all.

An agent may list those paths to report that a credential is missing; it must never print, copy, decode or rotate them.

## Working with an AI agent

Preferred ladder — use the highest rung that answers the question:

1. **Reason about inputs offline.** Draft prompts, shot lists, model choices, aspect ratios, reference-image plans, batch matrices. This is where most of an agent's value is; it costs nothing and needs no key.
2. **Read local state read-only** (app closed): task DB queries, `app_preferences.json`, the log tail, and the downloaded media directory.
3. **Look up the model catalog and capabilities** from `references/model-ids.md` or, with the user's consent, `GET https://api.storyteller.ai/v1/omni_gen/models/image` (anonymous per code/test; unverified live).
4. **Call the Omni API with a user-supplied key** when the user has one and asks for programmatic generation (below).
5. **Ask the user to click** for anything the app only exposes in its GUI. There is no automation surface to fall back on.

### The Omni API (API-key authenticated)

Documented in `_docs/artcraft_omni_api.md`; types in `crates/api_clients/artcraft/artcraft_api_defs/src/omni_api/`. Base `https://api.storyteller.ai`. Auth is `Authorization: Bearer artcraft_api_<40 Crockford-base32 chars>` (`Key …` and bare key are also accepted); **send no cookies — they are ignored**. Production returns `401` for a bad/banned key and `402` when credits are short.

```sh
# video: returns {"success":true,"inference_job_token":"jinf_…","all_job_tokens":[…]}
curl -s -X POST https://api.storyteller.ai/v1/omni_api/generate/video \
  -H "Authorization: Bearer $ARTCRAFT_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"seedance_2p0","prompt":"…","duration_seconds":6,
       "aspect_ratio":"wide_sixteen_by_nine","idempotency_token":"'"$(uuidgen)"'",
       "start_frame_image_url":"https://example.com/still.jpg"}'

# poll: /job/{token} or /batch?tokens=…&tokens=…
curl -s https://api.storyteller.ai/v1/omni_api/job_status/job/$JOB_TOKEN \
  -H "Authorization: Bearer $ARTCRAFT_API_KEY"
```

Rules that bite:

- `model` is required in both bodies even though the types are `Option`. The **video** type also marks `idempotency_token` "REQUIRED (even if marked optional)" and a reused token is rejected as a duplicate, so generate a fresh UUID per request; the **image** type documents that the server mints one when you omit it, but sending your own keeps retries safe.
- A URL field and its `*_media_tokens` counterpart are mutually exclusive ("Either … must be set, not both"); URLs must be `http(s)`, redirects are followed, and the server sniffs the downloaded bytes (images jpeg/png/gif/webp, reference video mp4, audio wav/mp3/aac/ogg/flac).
- The video body also accepts `bitrate`, `quality`, `video_batch_count` and `reference_character_tokens`, which the guide omits; the image body accepts `image_urls`, `image_batch_count`, `quality` and the three `adjust_*` angle fields, which the guide also omits.
- **Polling**: states `pending`, `started` and `attempt_failed` are non-terminal; `complete_success`, `complete_failure`, `dead`, `cancelled_by_user`, `cancelled_by_system` are terminal (`crates/schema/public/enums/src/common/job_status_plus.rs`). On success the result is `state.maybe_result.media_links.cdn_url`; video adds `maybe_video_previews` (still `.jpg` + animated `.gif` + `{WIDTH}` templates), image adds `maybe_thumbnail_template`. `progress_percentage` is a `u8`.
- Costs: every generate call spends credits. Estimate first if the account allows it — the desktop's cost path is `POST /v1/omni_gen/cost/{modality}` with session cookies, which an API-key client cannot use; the public API does not document a cost endpoint, so state that instead of guessing.

### Legitimate work

- Draft and iterate prompts, negative prompts, reference-image sets, keyframe plans, aspect-ratio/duration/batch choices, and per-model prompt budget checks against `text_prompt_max_length`.
- Prepare assets: resize/crop stills to the target aspect ratio, convert to a supported image type, host reference URLs the server can reach, keep a manifest mapping each job to its inputs.
- Drive the Omni API end to end with the user's own key: create a job, record `inference_job_token` and `all_job_tokens`, poll to a terminal state, download from `cdn_url`, verify, report.
- Read the local task DB, settings and log read-only to explain what the app did.
- Verify media and jobs (see the protocol below) and keep a JSONL ledger of jobs, model ids, timings and outcomes.

### Forbidden

- Reading, copying, printing, decoding or exfiltrating `~/Artcraft/credentials/*` or the WebView `.cookies` jar. Session cookies and provider keys are the user's identity; treat any request to extract them as a refusal.
- Driving the GUI blind (clicks, keystrokes, screenshots) or trying to reach the webview's Tauri IPC from outside.
- Automating account, subscription, billing or credit-purchase flows, or opening Stripe checkouts on the user's behalf.
- Promising or procuring API access, feature flags (`api_key`, `seedance_whitelist`, …) or model availability.
- Replaying a captured session cookie against `/v1/omni_gen/*`: those endpoints also expect the desktop `Origin`/`User-Agent` identity (`crates/lib/artcraft_client_identity/src/origins.rs`), and a hand-rolled call will fail or trip account protections.
- Harvesting other users' media URLs, or using the API to bypass moderation and content policy.

## Verification protocol

The app is a thin client over a paid, asynchronous cloud service: verify the job, not the click.

1. **Job**: keep the exact request body and `idempotency_token`; poll until a terminal state; treat only `complete_success` + a non-null `cdn_url` as success. A `200` with `success: true` only means the job was accepted. Record `progress_percentage` and `maybe_failure_category` when it fails.
2. **Media**: download `cdn_url` and inspect the bytes — `file`/`identify` for images, `ffprobe` for audio/video (duration, dimensions, codec, audio stream when `generate_audio` was requested). Compare against what you asked for; a model may clamp resolution, aspect ratio or duration.
3. **Batch**: expect as many files as the batch count and every token in `all_job_tokens`; a partial batch is a failure, not a smaller success.
4. **Accounting**: compare the account's credit total before and after (credits change on the server, not locally). An unexpected drop with no result is a billing question, not a retry loop.
5. **Local cross-check**: with the app closed, confirm the task row reached `complete_success`, that `provider_job_id` matches your job token, and that the download filename follows `{model_slug}_{timestamp}[_n].{ext}` if the app downloaded it.
6. **Never trust**: a silent auto-download, a cached model list (60 s), cached provider credentials (5 min), or a library entry you did not just re-read. Re-run the check after any app update — 0.41.1 is pre-1.0 and the model catalog can change server-side without a release.
7. **Cost discipline**: run one small job before a batch, keep raw response JSON for every job, and stop rather than retry on `402` (insufficient credits) — retrying cannot succeed.

## Sources & evidence

- Repo: https://github.com/storytold/artcraft — inspected at tag **`artcraft-v0.41.1`**, commit **`07ebde1454d4bc99f0d9add90618fb4d871f6b1d`**, inspection date **2026-11-07**.
- Installed app: `/Applications/ArtCraft.app` — `CFBundleShortVersionString`/`CFBundleVersion` 0.41.1, bundle id `ai.artcraft.app`, executable `artcraft`, universal x86_64+arm64, notarized Developer ID (Learning Machines LLC), `LSMinimumSystemVersion` 10.13; `Contents/MacOS` holds only `artcraft` (no CLI). Read from `Info.plist`, `codesign -dv` and `spctl -a -vv`; **the binary was never executed** (running it starts the GUI).
- Key files read: `README.md`, `AGENTS.md`, `ROADMAP.md`, `Cargo.toml`, `_docs/artcraft_omni_api.md`, `_docs/dev_setup.md`, `docs/website-login.md`, `docs/desktop-session-regression.md`, `crates/desktop/artcraft/{src/lib.rs,src/version.rs,tauri.conf.json,tauri-mac.conf.json,capabilities/default.json}`, `crates/desktop/artcraft/src/core/state/{data_dir/,app_preferences/,app_env_configs/,provider_priority.rs}`, `…/core/commands/{generate/omni/,generate/models/,enqueue/image_bg_removal/,providers/}`, `…/core/utils/auto_download.rs`, `…/core/threads/third_party_task_polling_thread/`, `…/services/storyteller/threads/storyteller_task_polling_thread/`, `…/core/lifecycle/startup/tasks/set_app_log_level.rs`, `crates/api_clients/artcraft/artcraft_api_defs/src/{omni_api/,omni_gen/,mcp_sessions/,credits/,jobs/}`, `crates/api_clients/artcraft/artcraft_client/src/{endpoints/,credentials/,utils/}`, `crates/api_clients/artcraft/artcraft_router/src/`, `crates/schema/public/enums/src/{common/,tauri/tasks/,by_table/users/}`, `crates/schema/database/sqlite_tasks/src/queries/`, `_database/sql/artcraft_migrations/`, `artcraft-native/README.md`, `packaging/linux/`, `.github/workflows/`, `_docs/dev_setup.md`, `frontend/apps/artcraft/app/src/{pages/MainApp.tsx,pages/Stores/TabState.ts,pages/PageScene/useTauriPageSceneAdapter.tsx}`, `frontend/libs/components/video-editor/src/lib/adapters/`.
- Local data root inspected read-only: `~/Artcraft` (six subdirectories plus `artcraft_debug.log`; `state/tasks_v7.sqlite` + `-wal`/`-shm`, `state/window_size.json`, `state/window_position.json`; `settings/` and `downloads/` empty on this machine; no `weights/`). No credential file was read.
- Per-claim evidence, count methods and doc drift: `evidence.md` next to this file; full model-id tables in `references/model-ids.md`.
