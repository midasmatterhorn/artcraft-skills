# PdfCraft automation tool table (names, titles, hints)

Generated from `crates/automation/src/tools.rs` (`tools()`) at tag `v0.15.0`,
commit `75360d1d7db06fed974f48c914d4c04132757187`, date 2026-10-29. **179 tools** — the same set as
v0.14.0 (153 inline + 26 multi-line `t(` entries; none added, removed or renamed). The order below is
the order `tools()` returns.

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
| 2 | `attachment_add` | Attach a file | — | `edit.attach` |
| 3 | `attachment_delete` | Delete an attachment | destructive | — |
| 4 | `doc_open` | Open a PDF | — | `file.open` |
| 5 | `doc_list` | List open documents | read-only | — |
| 6 | `doc_info` | Inspect a document | read-only | `file.properties` |
| 7 | `doc_close` | Close a document | — | `file.close` |
| 8 | `doc_save` | Save a document | destructive | `file.save` |
| 9 | `doc_set_info` | Set document metadata | — | — |
| 10 | `page_render` | Render a page | read-only | — |
| 11 | `object_list` | List editable objects | read-only | — |
| 12 | `object_move` | Move objects together | — | — |
| 13 | `text_word_count` | Word count | read-only | `file.word_count` |
| 14 | `text_extract` | Extract text | read-only | `edit.column_select` |
| 15 | `text_find` | Find text | read-only | `edit.find` |
| 16 | `page_rotate` | Rotate pages | — | `page.rotate` |
| 17 | `page_enhance_camera` | Enhance camera image | — | `ocr.enhance_camera` |
| 18 | `page_delete` | Delete pages | destructive | `page.delete` |
| 19 | `page_move` | Move pages | — | — |
| 20 | `page_reverse` | Reverse pages | — | `page.reverse` |
| 21 | `page_insert_blank` | Insert a blank page | — | `page.insert_blank` |
| 22 | `page_insert_file` | Insert pages from a file | — | `page.insert` |
| 23 | `page_extract` | Extract pages | — | `page.extract` |
| 24 | `doc_combine` | Combine files | — | `page.combine` |
| 25 | `doc_create_multiple` | Create PDF from multiple files | — | `create.multiple` |
| 26 | `doc_split` | Split a document | — | `page.split` |
| 27 | `bookmark_list` | List bookmarks | read-only | — |
| 28 | `bookmark_add` | Add a bookmark | — | — |
| 29 | `bookmark_rename` | Rename a bookmark | — | — |
| 30 | `bookmark_delete` | Delete a bookmark | destructive | — |
| 31 | `bookmark_move` | Move a bookmark | — | — |
| 32 | `bookmark_set_page` | Set a bookmark's page | — | — |
| 33 | `bookmark_set_style` | Set a bookmark's style and colour | — | — |
| 34 | `bookmark_from_structure` | New bookmarks from structure | — | — |
| 35 | `page_number` | Number pages | — | — |
| 36 | `form_fields` | List form fields | read-only | — |
| 37 | `form_fill` | Fill in form fields | — | — |
| 38 | `form_reset` | Clear form | destructive | — |
| 39 | `form_add_field` | Prepare form: add a field | — | — |
| 40 | `form_add_field_table` | Prepare form: add a table of text fields | — | `form.add.text_table` |
| 41 | `stamp_custom` | Add a custom stamp | — | `comment.stamp` |
| 42 | `form_set_image` | Set an image field's picture | — | — |
| 43 | `form_set_props` | Field properties | — | — |
| 44 | `form_tab_order` | Set the tab order | — | — |
| 45 | `form_calculation_order` | Read or set the calculation order | — | `form.calculation_order` |
| 46 | `doc_export_data` | Export comments or form data | destructive | — |
| 47 | `doc_import_data` | Import comments or form data | — | — |
| 48 | `form_delete_field` | Delete a field | destructive | — |
| 49 | `redact_mark` | Mark for redaction | — | — |
| 50 | `redact_apply` | Apply redactions | destructive | — |
| 51 | `redact_clear` | Remove redaction marks | destructive | — |
| 52 | `doc_hidden_info` | Find hidden information | read-only | — |
| 53 | `doc_remove_hidden` | Remove hidden information / Sanitize | destructive | — |
| 54 | `doc_audit_redactions` | Audit faux redactions | read-only | — |
| 55 | `printers` | List printers | read-only | — |
| 56 | `printer_options` | List printer options | read-only | — |
| 57 | `doc_print` | Print | — | — |
| 58 | `content_list` | List added content | read-only | — |
| 59 | `page_add_text` | Add text to a page | — | `edit.text` |
| 60 | `page_add_image` | Add an image to a page | — | `edit.image` |
| 61 | `content_update` | Edit added content | — | — |
| 62 | `content_copy` | Copy and paste added content | — | — |
| 63 | `content_delete` | Delete added content | destructive | — |
| 64 | `link_list` | List links | read-only | — |
| 65 | `link_open` | Open a linked PDF | — | — |
| 66 | `link_add` | Add a link | — | `edit.link` |
| 67 | `link_edit` | Edit a link | — | — |
| 68 | `link_delete` | Delete a link | destructive | — |
| 69 | `links_from_urls` | Create links from URLs | — | `edit.links_from_urls` |
| 70 | `links_remove` | Remove all links | destructive | `edit.remove_links` |
| 71 | `measure_distance` | Measure distance | — | `measure.distance` |
| 72 | `measure_perimeter` | Measure perimeter | — | `measure.perimeter` |
| 73 | `measure_area` | Measure area | — | `measure.area` |
| 74 | `measure_info` | Read a measurement | read-only | `measure.info` |
| 75 | `measure_list` | List measurements | read-only | — |
| 76 | `measure_scale` | Set or read a measurement scale | — | `measure.scale` |
| 77 | `measure_snap` | Snap a measurement vertex | read-only | `measure.snap` |
| 78 | `measure_export` | Export measurements as CSV | — | `measure.export` |
| 79 | `comment_list` | List comments | read-only | — |
| 80 | `comment_add` | Add a comment | — | — |
| 81 | `comment_reply` | Reply to a comment | — | — |
| 82 | `comment_set_status` | Set a comment's status | — | — |
| 83 | `sign_list` | List and validate signatures | read-only | — |
| 84 | `sign_id_create` | Create a digital ID | — | — |
| 85 | `sign_windows_ids` | List Windows store digital IDs | read-only | `sign.digital` |
| 86 | `sign_keychain_ids` | List Keychain digital IDs | read-only | `sign.digital` |
| 87 | `sign_document` | Sign a document | — | `sign.digital` |
| 88 | `sign_trust` | Trust certificates | — | — |
| 89 | `comment_mark` | Mark a comment with a checkmark | — | — |
| 90 | `comment_lock` | Lock a comment | — | — |
| 91 | `layer_set` | Show or hide a layer | — | — |
| 92 | `comments_hide` | Hide all comments | — | `comment.hide_all` |
| 93 | `view_reading_colors` | Set reading colours | — | `a11y.reading_options` |
| 94 | `comments_summarize` | Summarize comments | — | `comment.summarize` |
| 95 | `comment_edit` | Edit a comment | — | — |
| 96 | `comment_image_preview` | Preview image signature layers | read-only | — |
| 97 | `comment_delete` | Delete a comment | destructive | — |
| 98 | `doc_protect` | Protect with passwords | — | `protect.password` |
| 99 | `doc_unprotect` | Remove security | destructive | `protect.remove` |
| 100 | `page_replace` | Replace pages | — | `page.replace` |
| 101 | `page_duplicate` | Duplicate pages | — | `page.duplicate` |
| 102 | `page_transition_set` | Set page transitions | — | — |
| 103 | `page_set_box` | Set page boxes / crop | — | `page.boxes` |
| 104 | `doc_header_footer` | Add header and footer | — | `edit.header_footer` |
| 105 | `doc_watermark` | Add watermark | — | `edit.watermark` |
| 106 | `doc_background` | Add background | — | `edit.background` |
| 107 | `doc_remove_marks` | Remove header & footer, watermark or background | destructive | — |
| 108 | `doc_export_images` | Export pages as images | — | `export.image` |
| 109 | `accessibility_autotag_preview` | Preview automatic tags | read-only | — |
| 110 | `accessibility_autotag_apply` | Automatically tag text-only PDF | — | — |
| 111 | `accessibility_autotag_form_fields` | Tag form fields | — | `a11y.autotag_fields` |
| 112 | `accessibility_check` | Check for accessibility | read-only | `a11y.check` |
| 113 | `accessibility_find_untagged` | Find untagged content | read-only | `a11y.find_untagged` |
| 114 | `accessibility_report` | Accessibility report | destructive | `a11y.report` |
| 115 | `accessibility_review_record` | Accessibility review record | destructive | — |
| 116 | `accessibility_review_save` | Save accessibility review decisions | destructive | — |
| 117 | `accessibility_review_load` | Open accessibility review decisions | read-only | — |
| 118 | `accessibility_review_html` | Accessibility review summary | destructive | — |
| 119 | `accessibility_fix` | Fix an accessibility problem | — | — |
| 120 | `accessibility_figures` | List figures | read-only | `a11y.alt_text` |
| 121 | `accessibility_set_alt` | Set alternate text | — | `a11y.alt_text` |
| 122 | `accessibility_tags` | List structure tags | read-only | `a11y.tags` |
| 123 | `accessibility_tag_content` | List tag content | read-only | `a11y.tags` |
| 124 | `accessibility_set_tag_property` | Edit tag property | — | — |
| 125 | `accessibility_mark_tag_artifact` | Mark tag content as artifact | — | — |
| 126 | `accessibility_move_tag` | Move structure tag | — | — |
| 127 | `form_merge_data` | Merge data files into spreadsheet | — | `form.merge_data` |
| 128 | `js_run` | Run JavaScript | — | `tools.js_console` |
| 129 | `js_document_scripts` | Document JavaScripts | read-only | `tools.document_js` |
| 130 | `js_set_document_script` | Edit a document JavaScript | — | `tools.document_js` |
| 131 | `form_set_script` | Set a field's JavaScript | — | `form.prepare` |
| 132 | `doc_export_office` | Export to Word, PowerPoint, HTML or RTF | — | `export.docx` |
| 133 | `pdfa_verify` | Verify PDF/A | read-only | `standards.pdfa` |
| 134 | `print_readiness` | Print readiness | read-only | — |
| 135 | `pdfa_convert` | Save as PDF/A | — | `standards.pdfa` |
| 136 | `standards_remove_id` | Remove PDF/A or PDF/X identification | — | — |
| 137 | `action_list` | List actions | read-only | `actions.wizard` |
| 138 | `action_run` | Run an action | — | `actions.wizard` |
| 139 | `doc_compare` | Compare files | read-only | `doc.compare` |
| 140 | `doc_compare_report` | Compare report | — | `doc.compare` |
| 141 | `doc_compare_mark` | Mark differences as comments | — | `doc.compare` |
| 142 | `form_detect_fields` | Detect form fields | — | `form.detect` |
| 143 | `form_actions` | Field actions | read-only | `form.prepare` |
| 144 | `form_set_actions` | Set field actions | — | `form.prepare` |
| 145 | `js_enabled` | JavaScript on or off | — | — |
| 146 | `ocr_recognize` | Recognize text (OCR) | — | `ocr.recognize` |
| 147 | `ocr_recognize_files` | Recognize text in multiple files | — | `ocr.recognize_batch` |
| 148 | `ocr_status` | OCR status | read-only | `ocr.recognize` |
| 149 | `doc_export_all_images` | Export all images | — | `export.all_images` |
| 150 | `doc_export_text` | Export text | — | `export.text` |
| 151 | `fill_sign_add` | Fill & Sign: type text or place a mark | — | `sign.fill.text` |
| 152 | `fill_sign_date_format` | Date format for Fill & Sign | — | — |
| 153 | `doc_create` | Create a PDF | — | — |
| 154 | `doc_reduce` | Reduce file size | — | `optimize.reduce` |
| 155 | `doc_initial_view` | Initial view | — | — |
| 156 | `doc_audit_space` | Audit space usage | read-only | `optimize.advanced` |
| 157 | `text_lines` | List text lines | read-only | `edit.edit_text` |
| 158 | `image_hit` | Hit test page artwork | read-only | `edit.edit_text` |
| 159 | `page_images` | List page images | read-only | `edit.edit_text` |
| 160 | `image_edit` | Edit an image | — | `edit.edit_text` |
| 161 | `image_save` | Save image as | destructive | `edit.edit_text` |
| 162 | `text_font_files` | List installed document fonts | read-only | `edit.edit_text` |
| 163 | `text_font_import` | Load document font | — | `edit.edit_text` |
| 164 | `text_fonts` | List document fonts | read-only | `edit.edit_text` |
| 165 | `text_paragraphs` | List paragraphs | read-only | `edit.edit_text` |
| 166 | `text_edit_layout` | Measure text draft | read-only | `edit.edit_text` |
| 167 | `text_edit` | Edit text | — | `edit.edit_text` |
| 168 | `doc_revisions` | List revisions | — | — |
| 169 | `doc_open_revision` | Open a revision | — | — |
| 170 | `doc_optimize` | Optimize PDF | — | `optimize.advanced` |
| 171 | `doc_flatten` | Flatten | destructive | — |
| 172 | `xfa_to_static` | Convert an XFA form to a static form | destructive | — |
| 173 | `edit_undo` | Undo | — | `edit.undo` |
| 174 | `edit_redo` | Redo | — | `edit.redo` |
| 175 | `command_list` | List commands | read-only | — |
| 176 | `command_run` | Run a command | destructive | — |
| 177 | `command_batch` | Run several commands | destructive | — |
| 178 | `doc_inspect` | Inspect open documents | read-only | — |
| 179 | `render_preview` | Render a preview | read-only | — |

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
