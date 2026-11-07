# ArtCraft Studio — evidence ledger (tag `artcraft-v0.41.1`)

Audit basis: this checkout is tag **`artcraft-v0.41.1`**, commit **`07ebde1454d4bc99f0d9add90618fb4d871f6b1d`** ("fix(ci): exclude desktop GUI crates and pin architecture for FreeBSD CI", 2026-11-06; inspection 2026-11-07). First audit: there is no previous skill for this app, so no delta is reported and nothing was carried forward. The installed bundle matches (Info.plist 0.41.1, `ai.artcraft.app`) and was **never executed** — only read via `plutil -p`, `codesign -dv`, `spctl -a -vv` and a directory listing. No build, test, commit or network request was made for this audit; the only executable run was read-only `sqlite3` and `grep`/`awk` over the clone.

Tier legend: **implemented** = code path exists and is wired into the app; **partial** = code exists with a named gap;
**claimed-only** = stated in docs/README but absent or contradicted by code; **unverified** = plausible from code/tests but not exercised here.

## 1. Capability claims → evidence → tier

| # | Claim | Evidence (repo-relative) | Tier |
|---|---|---|---|
| 1 | App is Tauri 2, version + bundle id fixed in config | `crates/desktop/artcraft/tauri.conf.json` (`"version": "0.41.1"`, `"identifier": "ai.artcraft.app"`); `src/version.rs` `ARTCRAFT_VERSION = "0.41.1"` | implemented |
| 2 | 62 Tauri commands registered; all are webview IPC | `crates/desktop/artcraft/src/lib.rs` `generate_handler![…]` — 62 identifier lines between the macro brackets | implemented |
| 3 | No CLI, no control channel, no MCP server, no AppleScript | zero `clap` in any `Cargo.toml`; zero `env::args` in `crates/desktop/artcraft` + `artcraft-native`; only `TcpListener` hits are in tests (`core/utils/auto_download.rs`, `services/storyteller/commands/storyteller_login_bridge_tests.rs`); bundle `Contents/MacOS` holds only `artcraft`; Info.plist has no `NSAppleScriptEnabled` | implemented (absence) |
| 4 | Five generation modalities via one JSON dispatch to `/v1/omni_gen/generate/{modality}` and cost via `/v1/omni_gen/cost/{modality}` | `core/commands/generate/omni/{dispatch.rs,request.rs}` (`Modality::{Image,Video,Mesh,Splat,Audio}`, `route = format!("/v1/omni_gen/generate/{}", …)`, `"/v1/omni_gen/cost/{}"`) | implemented |
| 5 | Audio and mesh are ArtCraft-only | `generate_audio_command.rs`, `generate_mesh_command.rs`: `if !request.uses_artcraft() { Err("No direct provider adapter is configured for this modality.") }` | implemented |
| 6 | Image routes ArtCraft/Grok models through Omni, others through legacy handlers | `generate_image/generate_image_command.rs`: `uses_artcraft() && !uses_legacy_image_endpoint()` → `omni::generate`; else ArtCraft / Midjourney / router | implemented |
| 7 | Video routes ArtCraft through Omni; native path has Grok and Sora 2 | `crates/desktop/artcraft/src/core/commands/generate/generate_video/generate_video_command.rs` + `crates/desktop/artcraft/src/core/commands/generate/generate_video/mod.rs` (`mod artcraft; mod grok; pub mod sora2;`) | implemented |
| 8 | fal is the only provider with a mapped credential key in the router | `generate_image/providers/artcraft_router/handle_router.rs` `map_provider_to_credential_key` → `Fal => FalApiKey`, everything else `NotYetImplemented` | implemented (limits providers) |
| 9 | Provider credential files live in `~/Artcraft/credentials` | `core/providers/credentials/provider_credential_key.rs` (`fal.api_key.txt`, `replicate.api_key.txt`, `grok.web_login.toml`, `higgsfield.web_login.toml`, `midjourney.web_login.toml`, `runway.web_login.toml`); `provider_credential_loading_cache.rs` joins `credentials_dir()` | implemented |
| 10 | 14 provider values declared; desktop wires six | `crates/schema/public/enums/src/common/generation_provider.rs` (14 variants, `all_variants().len() == 14` in its own test; eight have no desktop wiring); desktop deps `crates/desktop/artcraft/Cargo.toml` (artcraft_client/router, fal_client, grok_consumer_client, midjourney_client, openai_sora_client, worldlabs_consumer_client) | implemented |
| 11 | Model id space: 24 image / 46 video (3 deprecated) / 5 audio / 11 mesh / 7 splat = 93 | count method in §2 | implemented |
| 12 | Model catalog is server-driven and cached 60 s, called without credentials | `core/commands/generate/models/image/list_image_models_command.rs` (`CACHE_TTL = 60s`, `maybe_creds: None`), `…/video/list_video_models_command.rs` (same); capability fields in `crates/api_clients/artcraft/artcraft_client/src/endpoints/omni_gen/models/image/omni_gen_list_image_models.rs` | implemented; anonymous access **unverified** (see `live_tests`, `#[ignore]`) |
| 13 | Router has 82 ArtCraft model rows (22 image, 39 video, 5 audio, 11 mesh, 5 splat) | `ls -d crates/api_clients/artcraft/artcraft_router/src/generate/generate_<kind>/providers/artcraft/*/` per kind | implemented |
| 14 | 17 tab branches; declared `EDIT` tab has no branch | `frontend/apps/artcraft/app/src/pages/MainApp.tsx` (17 `case "` lines); `pages/Stores/TabState.ts` `TabId` includes `"EDIT"` | implemented |
| 14b | Both watermark-remover pages are non-functional stubs (2 s `setTimeout` then a success toast; no upload, no backend call) | `frontend/apps/artcraft/app/src/pages/PageImageWatermarkRemover/ImageWatermarkRemover.tsx` (`handleRemoveWatermark`), `…/PageVideoWatermarkRemover/VideoWatermarkRemover.tsx`; a repo-wide grep for the 2 s stub pattern hits only these two files | implemented (stub) |
| 15 | No local project/document format; video-editor projects in IndexedDB; 3D scene uploaded as a server media file | `frontend/libs/components/video-editor/src/lib/adapters/default/indexeddb-project-storage.ts` (`DB_NAME "video-editor"`, `DB_VERSION 1`, store `projects`); `frontend/apps/artcraft/app/src/pages/PageScene/useTauriPageSceneAdapter.tsx` (`/v1/media_files/upload/new_scene`, `?engine_category=scene`, `/v1/media_files/file/{token}`) | implemented (gap) |
| 16 | Server-side project endpoints exist as types only; no frontend caller | `crates/api_clients/artcraft/artcraft_api_defs/src/media_file/project/upload_new_{editor_2d,mood_board,scene_3d,video_timeline}_project.rs`; grep for those paths under `frontend/` returns nothing | claimed-only (for desktop) |
| 17 | Local data root `~/Artcraft` with six subdirs and `artcraft_debug.log` | `core/state/data_dir/app_data_root.rs` (`DEFAULT_DATA_DIR "Artcraft"`, `LOG_FILE_NAME "artcraft_debug"`), `app_{assets,credentials,downloads,settings,state}`, `temporary_dir` | implemented |
| 18 | Task DB `state/tasks_v7.sqlite`, WAL mode, `_sqlx_migrations` + `tasks` | `core/state/task_database_version.rs` (`TASK_DATABASE_VERSION: u32 = 7`), `app_state_dir.rs`; live check: `sqlite3 "file:tasks_v7.sqlite?mode=ro" ".tables"` → `_sqlx_migrations tasks`, `pragma journal_mode` → `wal`, 0 rows | implemented |
| 19 | DB schema: 9 task statuses, 7 task types, rich completion/failure columns | `_database/sql/artcraft_migrations/20250708000000_create_tasks_table.sql`; `crates/schema/public/enums/src/tauri/tasks/task_status.rs` (9), `crates/schema/public/enums/src/tauri/tasks/task_type.rs` (7) | implemented |
| 20 | Download naming `{model_slug}_{YYYY-MM-DD-HH-MM-SS}[_n].{ext}`, OS Downloads by default | `core/state/app_preferences/preferred_download_filename.rs` (unit tests pin exact strings), `preferred_download_directory.rs` (`dirs::download_dir()`; `~/Artcraft/downloads` fallback) | implemented |
| 21 | Auto-download is opt-in and checkpoints to `state/auto_download_<task_id>.json` | `core/state/app_preferences/app_preferences.rs` (`auto_download: false` default), `core/utils/auto_download.rs` `checkpoint_path` | implemented |
| 22 | Job polling: 5 s `/v1/jobs/session`, 60 s on 429, 30 s on error | `services/storyteller/threads/storyteller_task_polling_thread/storyteller_task_polling_thread.rs` (`from_millis(5_000)`, `60_000`, `30_000`) | implemented |
| 23 | Third-party polling cadence 10 s / 2 s / 1 s / 30 s | `core/threads/third_party_task_polling_thread/third_party_task_polling_thread.rs` (`SLEEP_NO_THIRD_PARTY_JOBS_SEEN`, `SLEEP_THIRD_PARTY_JOBS_SEEN`, `SLEEP_BETWEEN_FAL_POLLS`, `SLEEP_ON_ERROR`) | implemented |
| 24 | Credits = free + monthly + banked; 402 typed | `crates/api_clients/artcraft/artcraft_api_defs/src/credits/get_session_credits.rs`; `crates/api_clients/artcraft/artcraft_client/src/utils/filter_bad_response.rs` (401/402/403/404/429/500 arms); `crates/api_clients/artcraft/artcraft_router/src/errors/artcraft_router_error.rs` `ProviderBillingError` | implemented |
| 25 | API access gated per account by a feature flag | `crates/schema/public/enums/src/by_table/users/user_feature_flag.rs` (`ApiKey`, 11 variants total); `crates/api_clients/artcraft/artcraft_api_defs/src/users/session_info.rs` `maybe_feature_flags`, `can_access_studio` | implemented |
| 26 | Omni API (API-key) paths, auth forms, polling | `_docs/artcraft_omni_api.md`; types at `crates/api_clients/artcraft/artcraft_api_defs/src/omni_api/{generate_requests,job_status,omni_upload_*}`; terminal/non-terminal states match `crates/schema/public/enums/src/common/job_status_plus.rs` (8 variants) | documented + typed; **server behaviour unverified** |
| 27 | Omni API has undocumented fields/endpoints | `OmniApiVideoGenerateRequest` adds `bitrate`, `quality`, `video_batch_count`, `reference_character_tokens`; `OmniApiImageGenerateRequest` adds `image_urls`, `image_batch_count`, `quality`, `adjust_*`; upload types document `POST /v1/omni_api/upload/{image,video,audio}` | implemented (types) |
| 28 | MCP is server-side session management only | `crates/schema/public/tokens/src/tokens/{mcp_sessions,mcp_session_private,mcp_session_refresh}.rs`; `crates/api_clients/artcraft/artcraft_api_defs/src/mcp_sessions/{create,refresh,revoke,delete}_mcp_session.rs`, `…/list_mcp_sessions.rs` (`POST /v1/mcp/session/create`); `crates/schema/public/enums/src/common/platform_type.rs` `PlatformType::Mcp` | implemented (server) |
| 29 | `artcraft-native` is a separate egui client that does not ship | `artcraft-native/README.md`; `Cargo.toml` members include `artcraft-native`; `.github/workflows/*` never build it — only `freebsd.yml` names it (`--exclude artcraft_native`) | implemented (source-only) |
| 30 | macOS universal + notarized; Linux matrix; FreeBSD excluded | `codesign -dv` (x86_64+arm64, hardened runtime), `spctl -a -vv` ("accepted, source=Notarized Developer ID"); `packaging/linux/README.md`, `packaging/linux/tauri.conf.json`, `.github/workflows/artcraft-{macos,windows,linux}-publish.yml`, `freebsd.yml` | implemented (mac verified locally) |
| 31 | UI is not scriptable from outside; session cookie kept out of JS/web storage | `docs/website-login.md` ("The signed session cookie never crosses IPC or gets written to JavaScript local storage"); `crates/vendor/tauri-plugin-http/src/lib.rs` (`COOKIES_FILENAME ".cookies"` under `app_cache_dir()`) | implemented |
| 32 | Dead code: `assets/`, `weights/`, image `grok`/`sora` provider dirs, bg-removal TODOs | `crates/desktop/artcraft/src/core/state/data_dir/app_assets_dir.rs` `make_or_get_current_date_dir` has no callers; `AppWeightsDir` is declared in `crates/desktop/artcraft/src/core/state/data_dir/mod.rs` but never instantiated by `AppDataRoot` and `~/Artcraft/weights` does not exist; `crates/desktop/artcraft/src/core/commands/generate/generate_image/providers/mod.rs` lists only artcraft/artcraft_router/midjourney; `crates/desktop/artcraft/src/core/commands/enqueue/image_bg_removal/enqueue_image_bg_removal_command.rs` `TODO`/`FIXME` comments | implemented (dead) |

## 2. Re-measured counts and the exact method

| Count | Value | Method (run at the tag above) |
|---|---:|---|
| Image model ids | **24** | `awk '/^pub enum CommonImageModel/,/^}/' crates/schema/public/enums/src/common/generation/common_image_model.rs \| grep -c 'rename = "'` |
| Video model ids | **46** (3 deprecated) | same pattern on `common_video_model.rs`; `grep -c '#\[deprecated'` = 3 (`grok_video`, `seedance_2p0_u`, `seedance_2p0_u_fast`) |
| Audio / mesh / splat ids | **5 / 11 / 7** | same pattern on `common_audio_model.rs`, `common_mesh_model.rs`, `common_splat_model.rs` |
| Persisted `model_type` space | **110** | `awk '/^pub enum CommonModelType/,/^}/' …/common_model_type.rs \| grep -cE '^  [A-Z]'` — a superset with legacy ids |
| Generation providers declared | **14** | `crates/schema/public/enums/src/common/generation_provider.rs` variants + its own `all_variants().len() == 14` test |
| Provider rows routed per kind (ArtCraft) | **22 / 39 / 5 / 11 / 5** | `ls -d …/artcraft_router/src/generate/generate_<kind>/providers/artcraft/*/ \| wc -l` |
| Task statuses / task types | **9 / 7** | enum variant counts in `crates/schema/public/enums/src/tauri/tasks/task_status.rs`, `crates/schema/public/enums/src/tauri/tasks/task_type.rs` |
| User feature flags | **11** | `awk '/^pub enum UserFeatureFlag/,/^}/' …/user_feature_flag.rs \| grep -cE '^  [A-Z]'` |
| Tauri commands | **62** | identifier lines inside `generate_handler![ … ]` in `crates/desktop/artcraft/src/lib.rs` |
| UI tabs routed | **17** | `grep -c '^    case "' frontend/apps/artcraft/app/src/pages/MainApp.tsx` |
| Task DB version | **7** | `TASK_DATABASE_VERSION: u32 = 7`; live file `tasks_v7.sqlite` |
| Shared resolution / quality / aspect / bitrate values | **8 / 6 / 18 / 2** | enum variant counts in `crates/schema/public/enums/src/common/generation/common_{resolution,quality,aspect_ratio,bitrate}.rs` |
| Video job-status states (Omni API) | **8** (3 non-terminal) | `common/job_status_plus.rs` variants |

README's "full 62-model catalog" (16 image + 25 video + 5 audio + 11 mesh + 5 splat) is a **product-copy number for the ArtCraft provider at some earlier date**: the 0.41.1 code space is 93 ids and the ArtCraft router alone has 82 model rows. The live server list is the only authoritative number and it is not in this repo.

## 3. Doc-vs-code drift found at this tag (code wins)

| Doc / comment | Code reality |
|---|---|
| `README.md` "ArtCraft: the full 62-model catalog" | 93 model ids in code; 82 ArtCraft-routed rows; catalog fetched live from the server |
| `MainApp.tsx` comment "one of the 13 tab branches" | 17 `case` branches |
| `_docs/artcraft_omni_api.md` request tables | code types add `bitrate`, `quality`, `video_batch_count`, `reference_character_tokens`, `image_urls`, `image_batch_count`, `adjust_*`; upload endpoints exist but are undocumented |
| `_docs/artcraft_omni_api.md` "companion image endpoint" | both image and video generate request types exist (`OmniApiImageGenerateRequest`) |
| `README.md` provider table (ArtCraft, Grok, Midjourney, Sora, World Labs) | fal is also reachable with a user key; audio/mesh are ArtCraft-only; eight further provider ids are declared but unwired |
| `artcraft-native/README.md` describes a working second client | no release workflow builds it; it is excluded from CI builds |
| Two watermark-remover tools look shipped in the UI | they only wait 2 s and toast success; no job, no file (`ImageWatermarkRemover.tsx`, `VideoWatermarkRemover.tsx`) |
| `ROADMAP.md` "Remove dependence on ArtCraft hosted services" | 0.41.1 has no local inference path at all |

## 4. Things that could not be verified (stated as uncertain in SKILL.md)

- **Anonymous model catalog.** Code passes no credentials and an `#[ignore]`d live test asserts production success; no request was made here. Label: claimed by code/test, unverified live.
- **The Omni API as a live service.** Endpoints and shapes come from `_docs/artcraft_omni_api.md` plus the vendored request/response types; the handler code lives in the private `artcraft-services` repo. Status codes and messages are the document's, not re-probed.
- **Windows and Linux behaviour**, the riscv64 build, and the Flatpak/OCI bundles. Only the macOS bundle was inspected.
- **Credit costs per model.** The cost endpoint (`/v1/omni_gen/cost/{modality}`) needs session cookies; no price table is in this repo.
- **Keyboard shortcuts.** Not enumerated in one place in the repo; none are quoted here rather than guessing.

## 5. Verification commands (read-only, reproduce the claims)

```sh
git -C <clone> rev-parse HEAD                                   # 07ebde1454d4bc99f0d9add90618fb4d871f6b1d
plutil -p "$APPDIR/Contents/Info.plist"                        # $APPDIR = the installed bundle; expect 0.41.1 / ai.artcraft.app (never run the binary)
awk '/^pub enum CommonImageModel/,/^}/' crates/schema/public/enums/src/common/generation/common_image_model.rs | grep -c 'rename = "'
awk '/^pub enum CommonVideoModel/,/^}/' crates/schema/public/enums/src/common/generation/common_video_model.rs | grep -c 'rename = "'
sed -n '/generate_handler!\[/,/\]);/p' crates/desktop/artcraft/src/lib.rs | grep -cE '^\s+[a-z_]+,$'
grep -c '^    case "' frontend/apps/artcraft/app/src/pages/MainApp.tsx
grep -rn 'clap' --include=Cargo.toml . | wc -l                  # 0
grep -rn 'env::args' --include=*.rs crates/desktop/artcraft artcraft-native | wc -l   # 0
sqlite3 "file:$HOME/Artcraft/state/tasks_v7.sqlite?mode=ro" ".tables"                 # _sqlx_migrations tasks
sqlite3 "file:$HOME/Artcraft/state/tasks_v7.sqlite?mode=ro" "pragma journal_mode;"    # wal
```

## 6. Files read for this audit

`README.md`, `AGENTS.md`, `ROADMAP.md`, `Cargo.toml`, `_docs/artcraft_omni_api.md`, `_docs/dev_setup.md`,
`docs/{website-login,desktop-session-regression}.md`, `crates/desktop/artcraft/{Cargo.toml,src/lib.rs,src/main.rs,src/version.rs,tauri.conf.json,tauri-mac.conf.json,capabilities/default.json}`,
`crates/desktop/artcraft/src/core/state/{data_dir/*,app_preferences/*,app_env_configs/*,task_database_version.rs,provider_priority.rs}`,
`crates/desktop/artcraft/src/core/commands/{generate/omni/*,generate/models/*,generate/generate_{image,video,command}.rs,enqueue/image_bg_removal/*,providers/*}`,
`crates/desktop/artcraft/src/core/{utils/auto_download.rs,threads/third_party_task_polling_thread/*,lifecycle/startup/tasks/set_app_log_level.rs}`,
`crates/desktop/artcraft/src/services/storyteller/{commands/*,threads/storyteller_task_polling_thread/*}`,
`crates/api_clients/artcraft/artcraft_api_defs/src/{omni_api/*,omni_gen/*,mcp_sessions/*,credits/*,jobs/*,media_file/project/*,users/session_info.rs}`,
`crates/api_clients/artcraft/artcraft_client/src/{endpoints/**/*,credentials/*,utils/{api_host,filter_bad_response,constants}.rs}`,
`crates/api_clients/artcraft/artcraft_router/src/{api/*,errors/artcraft_router_error.rs,generate/**/providers/*}`,
`crates/schema/public/enums/src/{common/*,tauri/tasks/*,by_table/users/user_feature_flag.rs}`,
`crates/schema/database/sqlite_tasks/src/queries/*`, `_database/sql/artcraft_migrations/20250708000000_create_tasks_table.sql`,
`crates/schema/public/tokens/src/tokens/mcp_session*.rs`, `crates/lib/artcraft_client_identity/src/origins.rs`,
`crates/vendor/tauri-plugin-http/src/lib.rs`, `artcraft-native/{README.md,Cargo.toml}`,
`packaging/linux/{README.md,tauri.conf.json,flatpak.yml}`, `.github/workflows/*.yml`,
`frontend/apps/artcraft/app/src/{pages/MainApp.tsx,pages/Stores/TabState.ts,pages/PageScene/useTauriPageSceneAdapter.tsx}`,
`frontend/libs/components/video-editor/src/lib/adapters/{project-storage.ts,default/indexeddb-project-storage.ts}`,
`/Applications/ArtCraft.app/Contents/Info.plist` (read only; the binary was never executed), `~/Artcraft` (directory listing and read-only `sqlite3` queries; no credential file opened).

No third-party shared library was consulted: `craft-libs` does not appear in the workspace dependency set — this app shares `crates/*` internally instead.
