# PdfCraft — round 2026-11-12 changes

Re-pinned: v0.19.0 (`8c57279`) -> v0.21.1 (`b503b2e62dfeec5598f344e4e287d9c9cbdb34fa`, installed `pdfcraft 0.21.1`).

## Corrected / re-measured

- Automation tools **195 → 208** (+13, 0 removed): `accessibility_layout_table_to_blocks`, `attachment_edit`, `comment_popup`, `doc_convert_colours`, `doc_fix_hairlines`, `doc_printer_marks`, `form_focus`, `js_event`, `object_copy`, `object_paste`, `printer_papers`, `text_prepare`, `text_replace`.
- Registry commands **214 → 221** (+7, 0 removed): `edit.replace`, `prepress.convert_colors`, `prepress.hairlines`, `prepress.marks`, `prepress.marks.remove`, `view.split`, `view.toggle_interface`.
- Tools carrying a command id **99 / 73 distinct ids (71 registry) → 104 / 77 (75 registry)**; `edit.undo` and `edit.redo` are tool-only names. Registry commands with no tool: **146 of 221** (was 143 of 214).
- Read-only tools **53 → 54**; destructive tools **30 → 30** (unchanged). No tool is both.
- All-tools catalogue: totals are **152 entries (149 `item(` + 3 `menu_item(`) / 23 groups / 29 sections** at both tags, but the previous edition's 150/24/30 was off by one on each. Planned state changed: **24 planned entries → 21** because Convert colors, Add printer marks and Fix hairlines became ready; **5 of the 23 groups** are still planned, and one group is provider-only.
- CLI `--flag` names: the previous edition said 25. `apps/pdfcraft-cli/src` holds **34** unique `--flag` names at both tags; subcommands are unchanged at **14 documented + internal `check-one`** (`apps/pdfcraft-cli/src/main.rs` has zero diff).
- Launch view/preference keys: the previous edition said 46. `PdfCraftApp::set_option` matches **58** top-level keys (`crates/ui-egui/src/app/control.rs`).
- UI control-method set corrected: there is no `ui.dock`. The 17 methods are `ui.state`, `ui.commands`, `ui.command`, `ui.set`, `ui.open`, `ui.inspect`, `ui.click`, `ui.focus`, `ui.resize`, `ui.quit`, `ui.drag`, `ui.move`, `ui.type`, `ui.key`, `ui.screenshot`, `ui.panel`, `ui.dock.reset` (unchanged at v0.21.1; `ui.panel` drives side panels and `ui.dock.reset` resets them).
- Comment types: `comment_add`'s `type` enum has **20** values at both tags (the old prose said 19).
- Print paper presets: `PAPERS` went **21 → 23** (`crates/print/src/settings.rs`); the print tool also accepts a driver paper name from `printer_papers`.
- Office import is no longer absent: `crates/create/src/office.rs` converts **28** Office/OpenDocument/RTF extensions through an installed LibreOffice. It is wired into File ▸ Open (background worker), `doc_combine` and `doc_create_multiple`. It is **not** wired into `doc_open` (PDF only) and the GUI's Combine, Insert Pages and Create Multiple refuse an Office file on the frame thread (`crates/ui-egui/src/workflows/combine_ui/parts.rs`, `crates/ui-egui/src/workflows/create_multiple_ui.rs`), so say which path works.
- `doc_create` text is no longer WinAnsi-only: it falls back to the bundled Inter face for Latin, Greek and Cyrillic letters outside WinAnsi; CJK, Arabic, Hebrew and Indic text is still refused (`crates/automation/src/tools.rs` `doc_create`, `crates/create/src/text_font.rs`).
- `model_render` can now orbit, turn, zoom, pan and pick front/right/top/back/iso views (`crates/prc-render/src/nav/`); the old "no tool rotates a model" sentence was wrong. U3D still cannot be drawn.
- Portfolio view now exists: the tab shows the portfolio's file list and opens the `/D` document first; `doc_info` reports `portfolio.initial` and `portfolio.view` (`crates/ui-egui/src/app/files.rs`, `crates/automation/src/json.rs`). The old "no portfolio view" limitation is gone; there is still no tool that extracts an attachment.
- Split view now exists (`view.split`, ⌘\\; `crates/ui-egui/src/panes.rs`), and a document's own `/HideToolbar`, `/HideMenubar` and `/HideWindowUI` are honoured with `view.toggle_interface` (F8) to bring the chrome back (`crates/ui-egui/src/viewer_prefs.rs`). The old "split view is missing" limitation is gone.
- `content_copy` is still the added-content paste path; the new `object_copy` / `object_paste` pair copies page objects (content operators plus their resources) within or between documents (`crates/engine/src/rich_copy.rs`, `crates/automation/src/tools.rs`). The old "content_copy is the only paste path" sentence was too broad.
- Document actions: `/OpenAction` JavaScript plus `/AA` `WillSave` and `WillPrint` run in the host (unasked requests restricted to highlight, zoom, focus and page); the old "document actions missing" limitation is narrowed to the other triggers (`crates/engine/src/js.rs`, `crates/ui-egui/src/workflows/js_ui.rs`).
- Print production is now **partial**, not absent: fix hairlines, convert colours (device formulas, no ICC/output intent) and add/remove printer marks are tools (`crates/edit/src/{hairlines,convert_colours,printer_marks}.rs`). Output preview, separations, overprint, ink manager, flattener preview and colour-management settings are still missing.
- Web build: it now exposes an in-page `window.pdfcraft` API over the UI control channel when the page is opened with `?control`, and OCR runs in Web Workers (`apps/pdfcraft-web/src/api.rs`, `apps/pdfcraft-ocr-worker/src/main.rs`). The old "no control-channel transport" sentence was wrong; there is still no network transport.
- MCP compact mode is **15 core tools + `tool_search` + `tool_call` = 17** entries; the README's "about ten core tools" is stale.

## Method

- `git rev-parse HEAD` in the pinned checkout gave `b503b2e62dfeec5598f344e4e287d9c9cbdb34fa`; `git describe --tags` gave `v0.21.1`; the working tree was clean. The shallow clone carries both `v0.19.0` and `v0.21.1`, so every set was diffed between tags rather than against notes.
- `git diff --shortstat v0.19.0..HEAD` = **872 files changed, 165 335 insertions, 11 319 deletions**. The round context's compare API reports 1 957 commits and caps its file list at 300; the clone's tag diff is the file count used here.
- Tool ids: every top-level `t(` declaration split into a block, name taken from its first string; 208 unique names at HEAD, 195 at v0.19.0, then a set diff. No duplicate names; no removals.
- Command ids: `c\(\s*"id"` over `crates/engine/src/commands.rs`, unique per tag; 221 / 214, then a set diff.
- Tools mapped to a command: `.cmd("…")` inside each tool block; 104 tools, 77 distinct ids, 75 of them in `COMMANDS`.
- Hints: `.ro()` and `.destructive()` inside each block; 54 / 30, no overlap.
- Catalogue: `ToolGroup {`, `ToolSection {`, `item(` and `menu_item(` occurrences after `pub static TOOL_GROUPS` in `crates/engine/src/catalog.rs`; 23 groups, 29 sections, 152 entries, 21 planned entries at v0.21.1 (24 at v0.19.0), 5 planned groups at both tags.
- CLI: match arms in `apps/pdfcraft-cli/src/main.rs` (14 documented commands + `check-one`); `--flag` strings over `apps/pdfcraft-cli/src/*.rs` (34); file has zero diff between tags.
- Launch keys: top-level string match arms in `PdfCraftApp::set_option` (`crates/ui-egui/src/app/control.rs`); 58.
- Control methods: unique `"ui.…"` strings in `crates/ui-egui/src/control/requests.rs`; 17 at both tags.
- Paper presets: `PAPERS` array length in `crates/print/src/settings.rs`; 21 at v0.19.0, 23 at HEAD.
- Office extensions: `OFFICE_EXTENSIONS` in `crates/create/src/office.rs`; 28. `CONVERTIBLE` in `crates/create/src/lib.rs` remains 13 and excludes Office.
- Installed bundle inspected read-only: `Contents/Info.plist` → `CFBundleShortVersionString` 0.21.1, `CFBundleIdentifier` `ai.storyteller.pdfcraft`, `LSMinimumSystemVersion` 11.0; `Contents/MacOS/PdfCraft --version` → `pdfcraft 0.21.1`, and `--help` printed the current usage including `--combine`. The GUI was never launched.
- Every repo-relative path cited by `SKILL.md` was re-resolved with `git cat-file -e HEAD:<path>`; all exist (brace shorthands expanded).

## Unchanged

- UI control methods **17** (identical set at both tags); CLI **14 documented subcommands + internal `check-one`**; MCP compact **17 entries**; MCP resources **4 URI templates + 2 list resources**; 16 MiB request-line cap.
- Convertible inputs **13** extensions (`png`…`pcx`, `txt`, `text`); Office is a separate 28-extension set through LibreOffice.
- Redaction patterns **6** (phone, email, credit-card, ssn, date, iban); a custom `regex` plus `validate` is the new addition.
- Office export **5 kinds / 7 extensions**; form data **8 extensions → 6 formats**; page-image export **3 formats** (png/jpeg/tiff); accessibility **32 rules in 7 categories**.
- Page budget **256 MiB** decoded per page walk and **50 000** form entries; MCP request lines **16 MiB**; last-view memory **100** files; autosave **60 s**; control channel **8** unauthenticated connections with **10 s** to authenticate.
- Capability sentences whose code path did not move were kept and are dated "unchanged at v0.21.1" only where a set was re-measured.

## Known gap in this round

- Pin-and-verify, not a new from-scratch audit: sections outside the changed areas keep the baseline prose with path re-resolution and the corrections listed above.
- `pdfcraft-cli` is not inside the macOS bundle and is not installed on this machine, so no live `pdfcraft-cli tools` / `--help` / `run` was possible; every tool and command count comes from the source at the tag. The installed GUI binary's `--version` and `--help` were run (no window opened).
- The new tools were read, not exercised: hairline fixing, colour conversion, printer marks, text replace/prepare, object copy/paste, form focus/pointer scripts, portfolio presentation, split view and Office import. The prepress and print claims are code-level only.
- Office import was not run: no LibreOffice installation or conversion was assumed. The 28 extensions and the desktop/worker split are from `crates/create/src/office.rs`, `crates/engine/src/session/files.rs` and the UI call sites.
- U3D model rendering was not tested; `model_render` still documents that only PRC streams draw.
- The Tesseract OCR engine was not exercised; the headless `language` enum is still `["en"]` (from `crates/ocr/src/ocrs.rs::LANGUAGES`).
- Older delta history (v0.17.0 → v0.18.1 feature highlights) was folded out of `SKILL.md`, which now carries the new v0.19.0 → v0.21.1 paragraph plus the single most recent historical one (v0.18.1 → v0.19.0); older highlights remain in the body sections where the code still supports them.
