# PdfCraft automation tool table (names, titles, hints)

Generated from `crates/automation/src/tools.rs` (`tools()`) at tag `v0.19.0`,
commit `8c572792d6760bdc903d6f9a032e3e38e8f71cb8`, date 2026-11-07. **195 tools** (v0.18.1 had
184; v0.19.0 adds `bookmark_copy`, `bookmark_export`, `bookmark_import`, `comments_copy`,
`comments_paste`, `model_add`, `model_render`, `ocr_dictionary`, `ocr_review_apply`, `ocr_words`
and `page_enhance_scan`, and removes none). The order below is the order `tools()` returns; hints
and command mappings are parsed from the same source file.

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
- 99 tools carry a registry command id (`ToolDef::command`, `.cmd(…)`), covering 73 distinct
  command ids of the 214 in the registry; `command_list` reports the mapping and
  `command_run id=… params=…` runs a command through it. `view.page_gaps` is the notable command
  with **no** tool: `command_run` fails with "has no headless tool"
  (`crates/automation/src/conventions.rs:15`).
- 53 tools are read-only (`.ro()`), 30 are destructive (`.destructive()`): destructive ones may
  remove content or overwrite a file on disk.
- This table is **not** the All tools catalogue. The catalogue (`crates/engine/src/catalog.rs:75`)
  is a UI list of 150 entries in 24 groups (30 sections); its availability variants are `Ready`,
  `Planned` and `Provider`. 24 entries and 5 whole groups carry a planned-milestone badge that
  does not by itself mean the command is absent (for example the "Protect a PDF" group is badged
  M8 while "Protect with password" in it is ready); one group is badged `Optional`.

## Tools

| # | Tool | Title | Hints | Command |
|---|---|---|---|---|
| 1 | `doc_bates_multi` | Add Bates numbering across files | destructive | — |
| 2 | `doc_batch` | Process files and folders | — | — |
| 3 | `attachment_add` | Attach a file | — | edit.attach |
| 4 | `attachment_delete` | Delete an attachment | destructive | — |
| 5 | `doc_open` | Open a PDF | — | file.open |
| 6 | `doc_list` | List open documents | read-only | — |
| 7 | `doc_info` | Inspect a document | read-only | file.properties |
| 8 | `doc_close` | Close a document | — | file.close |
| 9 | `doc_save` | Save a document | destructive | file.save |
| 10 | `doc_set_info` | Set document metadata | — | — |
| 11 | `page_render` | Render a page | read-only | — |
| 12 | `model_render` | Render a 3D model | read-only | — |
| 13 | `object_list` | List editable objects | read-only | — |
| 14 | `object_move` | Move objects together | — | — |
| 15 | `text_word_count` | Word count | read-only | file.word_count |
| 16 | `text_extract` | Extract text | read-only | edit.column_select |
| 17 | `text_find` | Find text | read-only | edit.find |
| 18 | `page_rotate` | Rotate pages | — | page.rotate |
| 19 | `page_enhance_camera` | Enhance camera image | — | ocr.enhance_camera |
| 20 | `page_enhance_scan` | Enhance scanned file | — | ocr.enhance |
| 21 | `page_delete` | Delete pages | destructive | page.delete |
| 22 | `page_move` | Move pages | — | — |
| 23 | `page_reverse` | Reverse pages | — | page.reverse |
| 24 | `page_insert_blank` | Insert a blank page | — | page.insert_blank |
| 25 | `page_insert_file` | Insert pages from a file | — | page.insert |
| 26 | `page_extract` | Extract pages | — | page.extract |
| 27 | `doc_combine` | Combine files | — | page.combine |
| 28 | `doc_create_multiple` | Create PDF from multiple files | — | create.multiple |
| 29 | `doc_split` | Split a document | — | page.split |
| 30 | `bookmark_list` | List bookmarks | read-only | — |
| 31 | `bookmark_add` | Add a bookmark | — | — |
| 32 | `bookmark_export` | Export bookmarks | destructive | — |
| 33 | `bookmark_import` | Import bookmarks | destructive | — |
| 34 | `bookmark_copy` | Copy bookmarks from another document | destructive | — |
| 35 | `bookmark_rename` | Rename a bookmark | — | — |
| 36 | `bookmark_delete` | Delete a bookmark | destructive | — |
| 37 | `bookmark_move` | Move a bookmark | — | — |
| 38 | `bookmark_set_page` | Set a bookmark's page | — | — |
| 39 | `bookmark_set_style` | Set a bookmark's style and colour | — | — |
| 40 | `bookmark_from_structure` | New bookmarks from structure | — | — |
| 41 | `text_styles` | List text styles | read-only | — |
| 42 | `bookmark_from_text_styles` | New bookmarks from text styles | — | — |
| 43 | `page_number` | Number pages | — | — |
| 44 | `form_fields` | List form fields | read-only | — |
| 45 | `form_fill` | Fill in form fields | — | — |
| 46 | `form_reset` | Clear form | destructive | — |
| 47 | `form_add_field` | Prepare form: add a field | — | — |
| 48 | `form_add_field_table` | Prepare form: add a table of text fields | — | form.add.text_table |
| 49 | `stamp_custom` | Add a custom stamp | — | comment.stamp |
| 50 | `model_add` | Add a 3D model | — | — |
| 51 | `form_set_image` | Set an image field's picture | — | — |
| 52 | `form_set_props` | Field properties | — | — |
| 53 | `form_tab_order` | Set the tab order | — | — |
| 54 | `form_calculation_order` | Read or set the calculation order | — | form.calculation_order |
| 55 | `doc_export_data` | Export comments or form data | destructive | — |
| 56 | `doc_import_data` | Import comments or form data | — | — |
| 57 | `form_delete_field` | Delete a field | destructive | — |
| 58 | `redact_mark` | Mark for redaction | — | — |
| 59 | `redact_apply` | Apply redactions | destructive | — |
| 60 | `redact_clear` | Remove redaction marks | destructive | — |
| 61 | `doc_hidden_info` | Find hidden information | read-only | — |
| 62 | `doc_remove_hidden` | Remove hidden information / Sanitize | destructive | — |
| 63 | `doc_audit_redactions` | Audit faux redactions | read-only | — |
| 64 | `printers` | List printers | read-only | — |
| 65 | `printer_options` | List printer options | read-only | — |
| 66 | `doc_print` | Print | — | — |
| 67 | `content_list` | List added content | read-only | — |
| 68 | `page_add_text` | Add text to a page | — | edit.text |
| 69 | `page_add_image` | Add an image to a page | — | edit.image |
| 70 | `content_update` | Edit added content | — | — |
| 71 | `content_copy` | Copy and paste added content | — | — |
| 72 | `content_delete` | Delete added content | destructive | — |
| 73 | `link_list` | List links | read-only | — |
| 74 | `link_open` | Open a linked PDF | — | — |
| 75 | `link_add` | Add a link | — | edit.link |
| 76 | `link_edit` | Edit a link | — | — |
| 77 | `link_delete` | Delete a link | destructive | — |
| 78 | `links_from_urls` | Create links from URLs | — | edit.links_from_urls |
| 79 | `links_remove` | Remove all links | destructive | edit.remove_links |
| 80 | `measure_distance` | Measure distance | — | measure.distance |
| 81 | `measure_perimeter` | Measure perimeter | — | measure.perimeter |
| 82 | `measure_area` | Measure area | — | measure.area |
| 83 | `measure_info` | Read a measurement | read-only | measure.info |
| 84 | `measure_list` | List measurements | read-only | — |
| 85 | `measure_scale` | Set or read a measurement scale | — | measure.scale |
| 86 | `measure_snap` | Snap a measurement vertex | read-only | measure.snap |
| 87 | `measure_export` | Export measurements as CSV | — | measure.export |
| 88 | `comment_list` | List comments | read-only | — |
| 89 | `comment_add` | Add a comment | — | — |
| 90 | `comment_reply` | Reply to a comment | — | — |
| 91 | `comment_set_status` | Set a comment's status | — | — |
| 92 | `sign_list` | List and validate signatures | read-only | — |
| 93 | `sign_id_create` | Create a digital ID | — | — |
| 94 | `sign_windows_ids` | List Windows store digital IDs | read-only | sign.digital |
| 95 | `sign_keychain_ids` | List Keychain digital IDs | read-only | sign.digital |
| 96 | `sign_document` | Sign a document | — | sign.digital |
| 97 | `sign_trust` | Trust certificates | — | — |
| 98 | `comment_mark` | Mark a comment with a checkmark | — | — |
| 99 | `comment_lock` | Lock a comment | — | — |
| 100 | `layer_set` | Show or hide a layer | — | — |
| 101 | `comments_hide` | Hide all comments | — | comment.hide_all |
| 102 | `view_reading_colors` | Set reading colours | — | a11y.reading_options |
| 103 | `comments_summarize` | Summarize comments | — | comment.summarize |
| 104 | `comment_edit` | Edit a comment | — | — |
| 105 | `comment_image_preview` | Preview image signature layers | read-only | — |
| 106 | `comment_delete` | Delete a comment | destructive | — |
| 107 | `comments_copy` | Copy comments | read-only | — |
| 108 | `comments_paste` | Paste comments | — | — |
| 109 | `doc_protect` | Protect with passwords | — | protect.password |
| 110 | `doc_unprotect` | Remove security | destructive | protect.remove |
| 111 | `page_replace` | Replace pages | — | page.replace |
| 112 | `page_duplicate` | Duplicate pages | — | page.duplicate |
| 113 | `page_transition_set` | Set page transitions | — | — |
| 114 | `page_set_box` | Set page boxes / crop | — | page.boxes |
| 115 | `doc_header_footer` | Add header and footer | — | edit.header_footer |
| 116 | `doc_watermark` | Add watermark | — | edit.watermark |
| 117 | `doc_background` | Add background | — | edit.background |
| 118 | `doc_backdrops` | List page backdrops | read-only | edit.background |
| 119 | `doc_remove_marks` | Remove header & footer, watermark or background | destructive | — |
| 120 | `doc_export_images` | Export pages as images | — | export.image |
| 121 | `accessibility_autotag_preview` | Preview automatic tags | read-only | — |
| 122 | `accessibility_autotag_apply` | Automatically tag text-only PDF | — | — |
| 123 | `accessibility_autotag_form_fields` | Tag form fields | — | a11y.autotag_fields |
| 124 | `accessibility_check` | Check for accessibility | read-only | a11y.check |
| 125 | `accessibility_find_untagged` | Find untagged content | read-only | a11y.find_untagged |
| 126 | `accessibility_report` | Accessibility report | destructive | a11y.report |
| 127 | `accessibility_review_record` | Accessibility review record | destructive | — |
| 128 | `accessibility_review_save` | Save accessibility review decisions | destructive | — |
| 129 | `accessibility_review_load` | Open accessibility review decisions | read-only | — |
| 130 | `accessibility_review_html` | Accessibility review summary | destructive | — |
| 131 | `accessibility_fix` | Fix an accessibility problem | — | — |
| 132 | `accessibility_figures` | List figures | read-only | a11y.alt_text |
| 133 | `accessibility_set_alt` | Set alternate text | — | a11y.alt_text |
| 134 | `accessibility_tags` | List structure tags | read-only | a11y.tags |
| 135 | `accessibility_tag_content` | List tag content | read-only | a11y.tags |
| 136 | `accessibility_set_tag_property` | Edit tag property | — | — |
| 137 | `accessibility_mark_tag_artifact` | Mark tag content as artifact | — | — |
| 138 | `accessibility_move_tag` | Move structure tag | — | — |
| 139 | `form_merge_data` | Merge data files into spreadsheet | — | form.merge_data |
| 140 | `js_run` | Run JavaScript | — | tools.js_console |
| 141 | `js_document_scripts` | Document JavaScripts | read-only | tools.document_js |
| 142 | `js_set_document_script` | Edit a document JavaScript | — | tools.document_js |
| 143 | `form_set_script` | Set a field's JavaScript | — | form.prepare |
| 144 | `doc_export_office` | Export to Word, PowerPoint, HTML, RTF or Markdown | — | export.docx |
| 145 | `pdfa_verify` | Verify PDF/A | read-only | standards.pdfa |
| 146 | `print_readiness` | Print readiness | read-only | — |
| 147 | `pdfa_convert` | Save as PDF/A | — | standards.pdfa |
| 148 | `standards_remove_id` | Remove PDF/A or PDF/X identification | — | — |
| 149 | `action_list` | List actions | read-only | actions.wizard |
| 150 | `action_run` | Run an action | — | actions.wizard |
| 151 | `doc_compare` | Compare files | read-only | doc.compare |
| 152 | `doc_compare_report` | Compare report | — | doc.compare |
| 153 | `doc_compare_mark` | Mark differences as comments | — | doc.compare |
| 154 | `form_detect_fields` | Detect form fields | — | form.detect |
| 155 | `form_actions` | Field actions | read-only | form.prepare |
| 156 | `form_set_actions` | Set field actions | — | form.prepare |
| 157 | `js_enabled` | JavaScript on or off | — | — |
| 158 | `ocr_recognize` | Recognize text (OCR) | — | ocr.recognize |
| 159 | `ocr_words` | Words of a recognition (for review) | read-only | — |
| 160 | `ocr_review_apply` | Apply or discard reviewed OCR words | — | ocr.correct |
| 161 | `ocr_dictionary` | Read or update an OCR review dictionary | destructive | ocr.correct |
| 162 | `ocr_recognize_files` | Recognize text in multiple files | — | ocr.recognize_batch |
| 163 | `ocr_status` | OCR status | read-only | ocr.recognize |
| 164 | `doc_export_all_images` | Export all images | — | export.all_images |
| 165 | `doc_export_text` | Export text | — | export.text |
| 166 | `fill_sign_add` | Fill & Sign: type text or place a mark | — | sign.fill.text |
| 167 | `fill_sign_date_format` | Date format for Fill & Sign | — | — |
| 168 | `doc_create` | Create a PDF | — | — |
| 169 | `doc_reduce` | Reduce file size | — | optimize.reduce |
| 170 | `doc_initial_view` | Initial view | — | — |
| 171 | `doc_audit_space` | Audit space usage | read-only | optimize.advanced |
| 172 | `text_lines` | List text lines | read-only | edit.edit_text |
| 173 | `image_hit` | Hit test page artwork | read-only | edit.edit_text |
| 174 | `page_images` | List page images | read-only | edit.edit_text |
| 175 | `image_edit` | Edit an image | — | edit.edit_text |
| 176 | `image_save` | Save image as | destructive | edit.edit_text |
| 177 | `text_font_files` | List installed document fonts | read-only | edit.edit_text |
| 178 | `text_font_import` | Load document font | — | edit.edit_text |
| 179 | `text_fonts` | List document fonts | read-only | edit.edit_text |
| 180 | `text_paragraphs` | List paragraphs | read-only | edit.edit_text |
| 181 | `text_edit_layout` | Measure text draft | read-only | edit.edit_text |
| 182 | `text_edit` | Edit text | — | edit.edit_text |
| 183 | `text_script` | Superscript or subscript | — | edit.edit_text |
| 184 | `doc_revisions` | List revisions | — | — |
| 185 | `doc_open_revision` | Open a revision | — | — |
| 186 | `doc_optimize` | Optimize PDF | — | optimize.advanced |
| 187 | `doc_flatten` | Flatten | destructive | — |
| 188 | `xfa_to_static` | Convert an XFA form to a static form | destructive | — |
| 189 | `edit_undo` | Undo | — | edit.undo |
| 190 | `edit_redo` | Redo | — | edit.redo |
| 191 | `command_list` | List commands | read-only | — |
| 192 | `command_run` | Run a command | destructive | — |
| 193 | `command_batch` | Run several commands | destructive | — |
| 194 | `doc_inspect` | Inspect open documents | read-only | — |
| 195 | `render_preview` | Render a preview | read-only | — |

## Notes on selected tools

- `attachment_add` / `attachment_delete` (`crates/automation/src/dispatch.rs:743`) add or remove a
  **document-level** attachment (the Attachments panel entry, not a paper-clip page comment). The
  added one keeps a unique key, defaults its name to the file name and is undoable. `doc_info`
  lists attachments. There is still **no tool that extracts/saves an attachment**: the panel can
  open or save one, the automation table cannot.
- `bookmark_set_style` (`crates/organize/src/outline.rs`: `set_bookmark_color` at :652 for `/C`,
  `set_bookmark_style` at :664 for `/F`) sets a bookmark's colour and bold/italic flag;
  `bookmark_list` reports both. It does not change nesting or targets. The v0.19.0 tools
  `bookmark_export`/`bookmark_import`/`bookmark_copy` move whole trees instead
  (`crates/organize/src/outline_io.rs`).
- `content_copy` (`crates/automation/src/content.rs:253`, engine `Edit::PasteContent`,
  `crates/engine/src/edit.rs:543`) pastes an **added** text box or image (from `content_list`)
  into the same or another open document, keeping type, font, size, colour, alignment, box,
  rotation, flips and crop. 18 pt cascade per existing copy, at an explicit `at`, refused when the
  source document withholds copying. It is the headless half of Edit ▸ Copy/Paste. It copies added
  content only — not page objects, text runs or annotations.
