# PdfCraft automation tool table (names, titles, hints)

Generated from `crates/automation/src/tools.rs` (`tools()`) at tag `v0.17.0`,
commit `7d78f3e14474b978be014715e0cc64895d77025a`, date 2026-11-02. **183 tools** (v0.16.1 had 182; +`text_script`; v0.16.0 added `doc_backdrops`, `bookmark_from_text_styles`, `text_styles`). The order below is
the order `tools()` returns; hints and command mappings are parsed from the same source file.

The repo's own docs are stale on this number: `docs/architecture.md` (§4), `docs/ui-parity.md` and
`docs/target-app-parity.md` still say "141 automation tools" and "184 registered commands";
`docs/roadmap.md` (M13) says 123. Trust the table below, `pdfcraft-cli tools` or MCP `tools/list`
for the version in front of you.

## How the table is used

- `pdfcraft-cli tools` prints every tool with its full JSON Schema (names only here).
- `pdfcraft-cli run <tool> key=value …` calls one; `--script steps.json` chains several in one
  session; `--root DIR` confines every path.
- MCP: `tools/list` / `tools/call` over stdio (`pdfcraft-cli mcp`). `--compact` returns only the
  15 core tools (`COMPACT_CORE_TOOLS`, `crates/automation/src/mcp.rs:45`) plus `tool_search` and
  `tool_call`; every tool still works by name.
- 71 tools carry a registry command id (`ToolDef::command`, `.cmd(…)`); `command_list` reports the
  mapping and `command_run id=… params=…` runs a command through it. `view.page_gaps` is the
  notable command with **no** tool: `command_run` fails with "has no headless tool"
  (`crates/automation/src/conventions.rs:15`).
- 48 tools are read-only (`.ro()`), 25 are destructive (`.destructive()`): destructive ones may
  remove content or overwrite a file on disk.
- This table is **not** the All tools catalogue. The catalogue
  (`crates/engine/src/catalog.rs:562`) is a UI list of 150 entries in 24 groups and 5 categories;
  26 entries and 5 whole groups carry a planned-milestone badge that does not by itself mean the
  command is absent (for example the "Protect a PDF" group is badged M8 while "Protect with
  password" in it is ready).

## Tools

| # | Tool | Title | Hints | Command |
|---|---|---|---|---|
| 1 | `doc_batch` | Process files and folders | — | — |
| 2 | `attachment_add` | Attach a file | — |  |
| 3 | `attachment_delete` | Delete an attachment | destructive | — |
| 4 | `doc_open` | Open a PDF | — |  |
| 5 | `doc_list` | List open documents | read-only | — |
| 6 | `doc_info` | Inspect a document | read-only |  |
| 7 | `doc_close` | Close a document | — |  |
| 8 | `doc_save` | Save a document | destructive |  |
| 9 | `doc_set_info` | Set document metadata | — | — |
| 10 | `page_render` | Render a page | read-only | — |
| 11 | `object_list` | List editable objects | read-only | — |
| 12 | `object_move` | Move objects together | — | — |
| 13 | `text_word_count` | Word count | read-only |  |
| 14 | `text_extract` | Extract text | read-only |  |
| 15 | `text_find` | Find text | read-only |  |
| 16 | `page_rotate` | Rotate pages | — |  |
| 17 | `page_enhance_camera` | Enhance camera image | — |  |
| 18 | `page_delete` | Delete pages | destructive |  |
| 19 | `page_move` | Move pages | — | — |
| 20 | `page_reverse` | Reverse pages | — |  |
| 21 | `page_insert_blank` | Insert a blank page | — |  |
| 22 | `page_insert_file` | Insert pages from a file | — |  |
| 23 | `page_extract` | Extract pages | — |  |
| 24 | `doc_combine` | Combine files | — |  |
| 25 | `doc_create_multiple` | Create PDF from multiple files | — |  |
| 26 | `doc_split` | Split a document | — |  |
| 27 | `bookmark_list` | List bookmarks | read-only | — |
| 28 | `bookmark_add` | Add a bookmark | — | — |
| 29 | `bookmark_rename` | Rename a bookmark | — | — |
| 30 | `bookmark_delete` | Delete a bookmark | destructive | — |
| 31 | `bookmark_move` | Move a bookmark | — | — |
| 32 | `bookmark_set_page` | Set a bookmark's page | — | — |
| 33 | `bookmark_set_style` | Set a bookmark's style and colour | — | — |
| 34 | `bookmark_from_structure` | New bookmarks from structure | — | — |
| 35 | `text_styles` | List text styles | read-only | — |
| 36 | `bookmark_from_text_styles` | New bookmarks from text styles | — | — |
| 37 | `page_number` | Number pages | — | — |
| 38 | `form_fields` | List form fields | read-only | — |
| 39 | `form_fill` | Fill in form fields | — | — |
| 40 | `form_reset` | Clear form | destructive | — |
| 41 | `form_add_field` | Prepare form: add a field | — | — |
| 42 | `form_add_field_table` | Prepare form: add a table of text fields | — |  |
| 43 | `stamp_custom` | Add a custom stamp | — |  |
| 44 | `form_set_image` | Set an image field's picture | — | — |
| 45 | `form_set_props` | Field properties | — | — |
| 46 | `form_tab_order` | Set the tab order | — | — |
| 47 | `form_calculation_order` | Read or set the calculation order | — |  |
| 48 | `doc_export_data` | Export comments or form data | destructive | — |
| 49 | `doc_import_data` | Import comments or form data | — | — |
| 50 | `form_delete_field` | Delete a field | destructive | — |
| 51 | `redact_mark` | Mark for redaction | — | — |
| 52 | `redact_apply` | Apply redactions | destructive | — |
| 53 | `redact_clear` | Remove redaction marks | destructive | — |
| 54 | `doc_hidden_info` | Find hidden information | read-only | — |
| 55 | `doc_remove_hidden` | Remove hidden information / Sanitize | destructive | — |
| 56 | `doc_audit_redactions` | Audit faux redactions | read-only | — |
| 57 | `printers` | List printers | read-only | — |
| 58 | `printer_options` | List printer options | read-only | — |
| 59 | `doc_print` | Print | — | — |
| 60 | `content_list` | List added content | read-only | — |
| 61 | `page_add_text` | Add text to a page | — |  |
| 62 | `page_add_image` | Add an image to a page | — |  |
| 63 | `content_update` | Edit added content | — | — |
| 64 | `content_copy` | Copy and paste added content | — | — |
| 65 | `content_delete` | Delete added content | destructive | — |
| 66 | `link_list` | List links | read-only | — |
| 67 | `link_open` | Open a linked PDF | — | — |
| 68 | `link_add` | Add a link | — |  |
| 69 | `link_edit` | Edit a link | — | — |
| 70 | `link_delete` | Delete a link | destructive | — |
| 71 | `links_from_urls` | Create links from URLs | — |  |
| 72 | `links_remove` | Remove all links | destructive |  |
| 73 | `measure_distance` | Measure distance | — |  |
| 74 | `measure_perimeter` | Measure perimeter | — |  |
| 75 | `measure_area` | Measure area | — |  |
| 76 | `measure_info` | Read a measurement | read-only |  |
| 77 | `measure_list` | List measurements | read-only | — |
| 78 | `measure_scale` | Set or read a measurement scale | — |  |
| 79 | `measure_snap` | Snap a measurement vertex | read-only |  |
| 80 | `measure_export` | Export measurements as CSV | — |  |
| 81 | `comment_list` | List comments | read-only | — |
| 82 | `comment_add` | Add a comment | — | — |
| 83 | `comment_reply` | Reply to a comment | — | — |
| 84 | `comment_set_status` | Set a comment's status | — | — |
| 85 | `sign_list` | List and validate signatures | read-only | — |
| 86 | `sign_id_create` | Create a digital ID | — | — |
| 87 | `sign_windows_ids` | List Windows store digital IDs | read-only |  |
| 88 | `sign_keychain_ids` | List Keychain digital IDs | read-only |  |
| 89 | `sign_document` | Sign a document | — |  |
| 90 | `sign_trust` | Trust certificates | — | — |
| 91 | `comment_mark` | Mark a comment with a checkmark | — | — |
| 92 | `comment_lock` | Lock a comment | — | — |
| 93 | `layer_set` | Show or hide a layer | — | — |
| 94 | `comments_hide` | Hide all comments | — |  |
| 95 | `view_reading_colors` | Set reading colours | — | — |
| 96 | `comments_summarize` | Summarize comments | — |  |
| 97 | `comment_edit` | Edit a comment | — | — |
| 98 | `comment_image_preview` | Preview image signature layers | read-only | — |
| 99 | `comment_delete` | Delete a comment | destructive | — |
| 100 | `doc_protect` | Protect with passwords | — |  |
| 101 | `doc_unprotect` | Remove security | destructive |  |
| 102 | `page_replace` | Replace pages | — |  |
| 103 | `page_duplicate` | Duplicate pages | — |  |
| 104 | `page_transition_set` | Set page transitions | — | — |
| 105 | `page_set_box` | Set page boxes / crop | — |  |
| 106 | `doc_header_footer` | Add header and footer | — |  |
| 107 | `doc_watermark` | Add watermark | — |  |
| 108 | `doc_background` | Add background | — |  |
| 109 | `doc_backdrops` | List page backdrops | read-only |  |
| 110 | `doc_remove_marks` | Remove header & footer, watermark or background | destructive | — |
| 111 | `doc_export_images` | Export pages as images | — |  |
| 112 | `accessibility_autotag_preview` | Preview automatic tags | read-only | — |
| 113 | `accessibility_autotag_apply` | Automatically tag text-only PDF | — | — |
| 114 | `accessibility_autotag_form_fields` | Tag form fields | — | — |
| 115 | `accessibility_check` | Check for accessibility | read-only | — |
| 116 | `accessibility_find_untagged` | Find untagged content | read-only | — |
| 117 | `accessibility_report` | Accessibility report | destructive | — |
| 118 | `accessibility_review_record` | Accessibility review record | destructive | — |
| 119 | `accessibility_review_save` | Save accessibility review decisions | destructive | — |
| 120 | `accessibility_review_load` | Open accessibility review decisions | read-only | — |
| 121 | `accessibility_review_html` | Accessibility review summary | destructive | — |
| 122 | `accessibility_fix` | Fix an accessibility problem | — | — |
| 123 | `accessibility_figures` | List figures | read-only | — |
| 124 | `accessibility_set_alt` | Set alternate text | — | — |
| 125 | `accessibility_tags` | List structure tags | read-only | — |
| 126 | `accessibility_tag_content` | List tag content | read-only | — |
| 127 | `accessibility_set_tag_property` | Edit tag property | — | — |
| 128 | `accessibility_mark_tag_artifact` | Mark tag content as artifact | — | — |
| 129 | `accessibility_move_tag` | Move structure tag | — | — |
| 130 | `form_merge_data` | Merge data files into spreadsheet | — |  |
| 131 | `js_run` | Run JavaScript | — |  |
| 132 | `js_document_scripts` | Document JavaScripts | read-only |  |
| 133 | `js_set_document_script` | Edit a document JavaScript | — |  |
| 134 | `form_set_script` | Set a field's JavaScript | — |  |
| 135 | `doc_export_office` | Export to Word, PowerPoint, HTML, RTF or Markdown | — |  |
| 136 | `pdfa_verify` | Verify PDF/A | read-only |  |
| 137 | `print_readiness` | Print readiness | read-only | — |
| 138 | `pdfa_convert` | Save as PDF/A | — |  |
| 139 | `standards_remove_id` | Remove PDF/A or PDF/X identification | — | — |
| 140 | `action_list` | List actions | read-only |  |
| 141 | `action_run` | Run an action | — |  |
| 142 | `doc_compare` | Compare files | read-only |  |
| 143 | `doc_compare_report` | Compare report | — |  |
| 144 | `doc_compare_mark` | Mark differences as comments | — |  |
| 145 | `form_detect_fields` | Detect form fields | — |  |
| 146 | `form_actions` | Field actions | read-only |  |
| 147 | `form_set_actions` | Set field actions | — |  |
| 148 | `js_enabled` | JavaScript on or off | — | — |
| 149 | `ocr_recognize` | Recognize text (OCR) | — |  |
| 150 | `ocr_recognize_files` | Recognize text in multiple files | — |  |
| 151 | `ocr_status` | OCR status | read-only |  |
| 152 | `doc_export_all_images` | Export all images | — |  |
| 153 | `doc_export_text` | Export text | — |  |
| 154 | `fill_sign_add` | Fill & Sign: type text or place a mark | — |  |
| 155 | `fill_sign_date_format` | Date format for Fill & Sign | — | — |
| 156 | `doc_create` | Create a PDF | — | — |
| 157 | `doc_reduce` | Reduce file size | — |  |
| 158 | `doc_initial_view` | Initial view | — | — |
| 159 | `doc_audit_space` | Audit space usage | read-only |  |
| 160 | `text_lines` | List text lines | read-only |  |
| 161 | `image_hit` | Hit test page artwork | read-only |  |
| 162 | `page_images` | List page images | read-only |  |
| 163 | `image_edit` | Edit an image | — |  |
| 164 | `image_save` | Save image as | destructive |  |
| 165 | `text_font_files` | List installed document fonts | read-only |  |
| 166 | `text_font_import` | Load document font | — |  |
| 167 | `text_fonts` | List document fonts | read-only |  |
| 168 | `text_paragraphs` | List paragraphs | read-only |  |
| 169 | `text_edit_layout` | Measure text draft | read-only |  |
| 170 | `text_edit` | Edit text | — |  |
| 171 | `text_script` | Superscript or subscript | — |  |
| 172 | `doc_revisions` | List revisions | — | — |
| 173 | `doc_open_revision` | Open a revision | — | — |
| 174 | `doc_optimize` | Optimize PDF | — |  |
| 175 | `doc_flatten` | Flatten | destructive | — |
| 176 | `xfa_to_static` | Convert an XFA form to a static form | destructive | — |
| 177 | `edit_undo` | Undo | — |  |
| 178 | `edit_redo` | Redo | — |  |
| 179 | `command_list` | List commands | read-only | — |
| 180 | `command_run` | Run a command | destructive | — |
| 181 | `command_batch` | Run several commands | destructive | — |
| 182 | `doc_inspect` | Inspect open documents | read-only | — |
| 183 | `render_preview` | Render a preview | read-only | — |
## Notes on tools added at this tag

- `attachment_add` / `attachment_delete` (`crates/automation/src/lib.rs:841`) add or remove a
  **document-level** attachment (the Attachments panel entry, not a paper-clip page comment). The
  added one keeps a unique key, defaults its name to the file name and is undoable. `doc_info`
  lists attachments. There is still **no tool that extracts/saves an attachment**: the panel can
  open or save one, the automation table cannot.
- `bookmark_set_style` (`crates/organize/src/outline.rs:636` for `/C`, `:647` for `/F`) sets a
  bookmark's colour and bold/italic flag; `bookmark_list` now reports both. It does not change nesting or targets.
- `content_copy` (`crates/automation/src/content.rs:217`, engine `Edit::PasteContent`,
  `crates/engine/src/lib.rs:1847`) pastes an **added** text box or image (from `content_list`)
  into the same or another open document, keeping type, font, size, colour, alignment, box,
  rotation, flips and crop. 18 pt cascade per existing copy, at an explicit `at`, refused when the
  source document withholds copying. It is the headless half of Edit ▸ Copy/Paste: the desktop
  keys and menus were not wired at this tag (`ROADMAP.md`). It copies added content only — not
  page objects, text runs or annotations.
