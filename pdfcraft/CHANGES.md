# PdfCraft — round 2026-11-07 changes

Re-pinned: v0.18.1 (`8bb0528`) -> v0.19.0 (`8c572792d6760bdc903d6f9a032e3e38e8f71cb8`, installed `pdfcraft 0.19.0`).

## Corrected / re-measured

- Tools **184 → 195** (+11, 0 removed): `bookmark_copy`, `bookmark_export`, `bookmark_import`, `comments_copy`, `comments_paste`, `model_add`, `model_render`, `ocr_dictionary`, `ocr_review_apply`, `ocr_words`, `page_enhance_scan`.
- Registry commands **210 → 214** (+4, 0 removed): `comment.copy`, `comment.paste`, `ocr.correct`, `ocr.enhance`.
- Convertible input extensions **12 → 13** (`pcx` joins png/jpg/jpeg/tif/tiff/gif/bmp/jp2/j2k/jpx/txt/text; `crates/create/src/lib.rs`).
- Redaction patterns **5 → 6**: `Iban` joins Phone/Email/CreditCard/Ssn/Date (`crates/redact/src/patterns.rs`).
- Command ids reachable from a tool **71 → 73** (99 tools declare `.cmd(…)`; `edit.undo`/`edit.redo` are named by tools but are not `COMMANDS` entries).
- Fixed the shipped skill's own stale counts: its "at a glance" table still said 183 tools, 205 commands and 35 languages while its audit-basis sentence and `evidence.md` said 184/210. The table and the prose now both say 195/214.
- Corrected the "71 tools mapped to a command" sentence: 71 was the distinct *command-id* count at v0.18.1, not a tool count. It is 99 tools / 73 ids at v0.19.0.
- Corrected "134 of 210 commands have no tool": the same extraction gives **141** of 210 at v0.18.1 and **143** of 214 at v0.19.0.
- Corrected "Office export 4 kinds / 5 extensions" to **5 kinds / 7 extensions** (`docx`, `pptx`, `html`/`htm`, `rtf`, `md`/`markdown`): Markdown was already in `OfficeFormat::from_extension` at v0.18.1, so this is a correction, not a delta.
- Corrected the catalogue's "5 categories" to **24 groups / 30 sections**; the availability variants are `Ready`, `Planned`, `Provider`.
- Corrected the version strings the old text quoted: the bundle and its binary both print **0.19.0** (the baseline still quoted `0.15.0`/`0.17.0` in two places), and MCP `tools/call` accepts **195** names, not 179.
- Dropped the "35 interface languages" claim (and the platform bullet that repeated it): `crates/ui-egui/src/i18n/` holds only `tests.rs`; catalogs come from the pinned `craft-i18n` crate (`craft-i18n.rev` = `575cfdef63227b14daf173b8cc87928bfdfa325e`), so no language count is measurable in-tree.

## Method

- `git rev-parse HEAD` in the pinned clone gave `8c572792d6760bdc903d6f9a032e3e38e8f71cb8`; `git describe --tags` gave `v0.19.0`; the working tree was clean. The shallow clone carries both `v0.18.1` and `v0.19.0` tags, so every set was diffed between tags rather than against notes.
- `git diff --stat v0.18.1..HEAD` = **375 files changed, 58 349 insertions, 3 517 deletions**. The round context's compare-API note says 300 files; the clone wins.
- Tool ids: `t\(\s*"name"` over `crates/automation/src/tools.rs` (handles single-line and wrapped declarations), unique set per tag, then set diff. 195 at HEAD, 184 at v0.18.1.
- Command ids: `c\(\s*"id"` over `crates/engine/src/commands.rs`, unique per tag, then set diff. 214 / 210.
- Tools mapped to a command: each top-level `t(` declaration split into a chunk, chunk counted when it contains `.cmd("…")`; distinct `.cmd()` ids intersected with the registry.
- Control methods: unique `"x.y"` strings in `crates/ui-egui/src/control/requests.rs` (17 at both tags). CLI subcommands: match arms in `apps/pdfcraft-cli/src/main.rs` (zero diff between tags).
- Convertible / Office / form-data / page-image / redaction-pattern / catalogue counts read from the defining arrays and `match` arms in the files cited above.
- Installed bundle inspected read-only: `Contents/Info.plist` → `CFBundleShortVersionString` 0.19.0, `CFBundleIdentifier` `ai.storyteller.pdfcraft`; the binary's `--version` → `pdfcraft 0.19.0`. The GUI was never launched.
- Every repo-relative path cited by the skill was re-resolved with `git cat-file -e HEAD:<path>`; all resolve (brace shorthands expanded).

## Unchanged

- UI control methods **17** (identical set at both tags); CLI **14 documented subcommands + internal `check-one`** (`apps/pdfcraft-cli/src/main.rs` has zero diff); MCP compact **17 entries** (15 core + `tool_search` + `tool_call`), **4 resource templates + 2 list resources**, 16 MiB request-line cap; page-image export **3** formats (png/jpeg/tiff); form data **8 extensions → 6 formats**; All-tools catalogue **150 entries / 24 groups**; 195 tools minus the 11 additions is exactly the 184-name v0.18.1 set, so nothing was renamed.
- Capability sentences whose code path did not move were kept as written and are dated "unchanged at v0.19.0" only where a set was re-measured.

## Known gap in this round

- Pin-and-verify, not a new from-scratch audit: sections outside the changed areas keep the baseline prose with only path re-resolution and the corrections listed above.
- `pdfcraft-cli` is not inside the macOS bundle, so no live `pdfcraft-cli tools`/`--help` run was possible; counts come from the source at the tag.
- The new Tesseract OCR engine was not exercised (no `tesseract` binary was assumed or run), and the OCR tool's `language` enum is still `["en"]` (built from `crates/ocr/src/ocrs.rs::LANGUAGES`), so the 12 allow-listed Tesseract codes in `crates/ocr/src/tesseract.rs` are not reachable through the headless schema at this tag.
- U3D model rendering was not tested: `model_render` documents that only PRC streams draw and U3D gives an error.
- Older delta history (v0.16.1 → v0.18.1 feature highlights) was folded out of `SKILL.md`, which now carries the new v0.18.1 → v0.19.0 paragraph plus the single most recent historical one (v0.17.0 → v0.18.1); those older highlights remain described in the body sections where the code still supports them.
