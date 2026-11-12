# PdfCraft automation tool table (names, titles, hints)

Generated from `crates/automation/src/tools.rs` (`tools()`) at tag `v0.21.1`,
commit `b503b2e62dfeec5598f344e4e287d9c9cbdb34fa`, date 2026-11-12. **208 tools** (v0.19.0 had
195; v0.21.1 adds `accessibility_layout_table_to_blocks`, `attachment_edit`, `comment_popup`,
`doc_convert_colours`, `doc_fix_hairlines`, `doc_printer_marks`, `form_focus`, `js_event`,
`object_copy`, `object_paste`, `printer_papers`, `text_prepare` and `text_replace`, and removes
none). The order below is the order `tools()` returns; hints and command mappings are parsed from
the same source file.

The repo's own docs are stale on this number: `docs/ui-parity.md` and `docs/target-app-parity.md`
still say "141 automation tools" and "184 registered commands"; `docs/roadmap.md` (M13) says 123.
Trust the table below, `pdfcraft-cli tools` or MCP `tools/list` for the version in front of you.

## How the table is used

- `pdfcraft-cli tools` prints every tool with its full JSON Schema (names only here).
- `pdfcraft-cli run <tool> key=value …` calls one; `--script steps.json` chains several in one
  session; `--root DIR` confines every path.
- MCP: `tools/list` / `tools/call` over stdio (`pdfcraft-cli mcp`). `--compact` returns only the
  15 core tools (`COMPACT_CORE_TOOLS`, `crates/automation/src/mcp.rs:45`) plus `tool_search` and
  `tool_call`; every tool still works by name.
- 104 tools carry a registry command id (`ToolDef::command`, `.cmd(…)`), covering 77 distinct
  command ids of the 221 in the registry (75 of the ids are registry entries; `edit.undo` and
  `edit.redo` are tool-only names). `command_list` reports the mapping and `command_run id=… params=…`
  runs a command through it. 146 of the 221 registry commands have no headless tool; `view.page_gaps`
  is one of them (`command_run` fails with "has no headless tool",
  `crates/automation/src/conventions.rs`).
- 54 tools are read-only (`.ro()`), 30 are destructive (`.destructive()`): destructive ones may
  remove content or overwrite a file on disk.
- This table is **not** the All tools catalogue. The catalogue (`crates/engine/src/catalog.rs:75`)
  is a UI list of 152 entries in 23 groups (29 sections); its availability variants are `Ready`,
  `Planned` and `Provider`. 21 entries and 5 whole groups carry a planned-milestone badge that
  does not by itself mean the command is absent (for example the "Protect a PDF" group is badged
  M8 while "Protect with password" in it is ready); one group is provider-only. Three prepress
  entries (Convert colors, Add printer marks, Fix hairlines) moved from Planned to Ready this
  release, so the planned count fell from 24 to 21.
- `doc_open` opens PDFs only. Word, Excel, PowerPoint, OpenDocument and RTF files convert through
  an installed LibreOffice in `doc_combine` and `doc_create_multiple` (and in the GUI's File ▸ Open),
  not through `doc_open`.

## Tools

| # | Tool | Title | Hints | Command |
|---|---|---|---|---|
| 1 | `doc_bates_multi` | Add Bates numbering across files | destructive | — |
| 2 | `doc_batch` | Process files and folders | — | — |
| 3 | `doc_fix_hairlines` | Fix hairlines | — | prepress.hairlines |
| 4 | `attachment_add` | Attach a file | — | edit.attach |
| 5 | `attachment_delete` | Delete an attachment | destructive | — |
| 6 | `doc_convert_colours` | Convert colours | — | prepress.convert_colors |
| 7 | `attachment_edit` | Edit an attachment description | — | — |
| 8 | `doc_open` | Open a PDF | — | file.open |
| 9 | `doc_list` | List open documents | read-only | — |
| 10 | `doc_info` | Inspect a document | read-only | file.properties |
| 11 | `doc_close` | Close a document | — | file.close |
| 12 | `doc_save` | Save a document | destructive | file.save |
| 13 | `doc_set_info` | Set document metadata | — | — |
| 14 | `page_render` | Render a page | read-only | — |
| 15 | `model_render` | Render a 3D model | read-only | — |
| 16 | `object_list` | List editable objects | read-only | — |
| 17 | `object_move` | Move objects together | — | — |
| 18 | `object_copy` | Copy or cut objects together | — | — |
| 19 | `object_paste` | Paste copied objects | — | — |
| 20 | `text_word_count` | Word count | read-only | file.word_count |
| 21 | `text_extract` | Extract text | read-only | edit.column_select |
| 22 | `text_find` | Find text | read-only | edit.find |
| 23 | `text_replace` | Replace text | — | edit.replace |
| 24 | `page_rotate` | Rotate pages | — | page.rotate |
| 25 | `page_enhance_camera` | Enhance camera image | — | ocr.enhance_camera |
| 26 | `page_enhance_scan` | Enhance scanned file | — | ocr.enhance |
| 27 | `page_delete` | Delete pages | destructive | page.delete |
| 28 | `page_move` | Move pages | — | — |
| 29 | `page_reverse` | Reverse pages | — | page.reverse |
| 30 | `page_insert_blank` | Insert a blank page | — | page.insert_blank |
| 31 | `page_insert_file` | Insert pages from a file | — | page.insert |
| 32 | `page_extract` | Extract pages | — | page.extract |
| 33 | `doc_combine` | Combine files | — | page.combine |
| 34 | `doc_create_multiple` | Create PDF from multiple files | — | create.multiple |
| 35 | `doc_split` | Split a document | — | page.split |
| 36 | `bookmark_list` | List bookmarks | read-only | — |
| 37 | `bookmark_add` | Add a bookmark | — | — |
| 38 | `bookmark_export` | Export bookmarks | destructive | — |
| 39 | `bookmark_import` | Import bookmarks | destructive | — |
| 40 | `bookmark_copy` | Copy bookmarks from another document | destructive | — |
| 41 | `bookmark_rename` | Rename a bookmark | — | — |
| 42 | `bookmark_delete` | Delete a bookmark | destructive | — |
| 43 | `bookmark_move` | Move a bookmark | — | — |
| 44 | `bookmark_set_page` | Set a bookmark's page | — | — |
| 45 | `bookmark_set_style` | Set a bookmark's style and colour | — | — |
| 46 | `bookmark_from_structure` | New bookmarks from structure | — | — |
| 47 | `text_styles` | List text styles | read-only | — |
| 48 | `bookmark_from_text_styles` | New bookmarks from text styles | — | — |
| 49 | `page_number` | Number pages | — | — |
| 50 | `form_fields` | List form fields | read-only | — |
| 51 | `form_fill` | Fill in form fields | — | — |
| 52 | `form_focus` | Move the focus into or out of a field | — | — |
| 53 | `form_reset` | Clear form | destructive | — |
| 54 | `form_add_field` | Prepare form: add a field | — | — |
| 55 | `form_add_field_table` | Prepare form: add a table of text fields | — | form.add.text_table |
| 56 | `stamp_custom` | Add a custom stamp | — | comment.stamp |
| 57 | `model_add` | Add a 3D model | — | — |
| 58 | `form_set_image` | Set an image field's picture | — | — |
| 59 | `form_set_props` | Field properties | — | — |
| 60 | `form_tab_order` | Set the tab order | — | — |
| 61 | `form_calculation_order` | Read or set the calculation order | — | form.calculation_order |
| 62 | `doc_export_data` | Export comments or form data | destructive | — |
| 63 | `doc_import_data` | Import comments or form data | — | — |
| 64 | `form_delete_field` | Delete a field | destructive | — |
| 65 | `redact_mark` | Mark for redaction | — | — |
| 66 | `redact_apply` | Apply redactions | destructive | — |
| 67 | `redact_clear` | Remove redaction marks | destructive | — |
| 68 | `doc_hidden_info` | Find hidden information | read-only | — |
| 69 | `doc_remove_hidden` | Remove hidden information / Sanitize | destructive | — |
| 70 | `doc_audit_redactions` | Audit faux redactions | read-only | — |
| 71 | `printers` | List printers | read-only | — |
| 72 | `printer_options` | List printer options | read-only | — |
| 73 | `printer_papers` | List printer paper sizes | read-only | — |
| 74 | `doc_print` | Print | — | — |
| 75 | `content_list` | List added content | read-only | — |
| 76 | `page_add_text` | Add text to a page | — | edit.text |
| 77 | `page_add_image` | Add an image to a page | — | edit.image |
| 78 | `content_update` | Edit added content | — | — |
| 79 | `content_copy` | Copy and paste added content | — | — |
| 80 | `content_delete` | Delete added content | destructive | — |
| 81 | `link_list` | List links | read-only | — |
| 82 | `link_open` | Open a linked PDF | — | — |
| 83 | `link_add` | Add a link | — | edit.link |
| 84 | `link_edit` | Edit a link | — | — |
| 85 | `link_delete` | Delete a link | destructive | — |
| 86 | `links_from_urls` | Create links from URLs | — | edit.links_from_urls |
| 87 | `links_remove` | Remove all links | destructive | edit.remove_links |
| 88 | `measure_distance` | Measure distance | — | measure.distance |
| 89 | `measure_perimeter` | Measure perimeter | — | measure.perimeter |
| 90 | `measure_area` | Measure area | — | measure.area |
| 91 | `measure_info` | Read a measurement | read-only | measure.info |
| 92 | `measure_list` | List measurements | read-only | — |
| 93 | `measure_scale` | Set or read a measurement scale | — | measure.scale |
| 94 | `measure_snap` | Snap a measurement vertex | read-only | measure.snap |
| 95 | `measure_export` | Export measurements as CSV | — | measure.export |
| 96 | `comment_list` | List comments | read-only | — |
| 97 | `comment_add` | Add a comment | — | — |
| 98 | `comment_reply` | Reply to a comment | — | — |
| 99 | `comment_set_status` | Set a comment's status | — | — |
| 100 | `sign_list` | List and validate signatures | read-only | — |
| 101 | `sign_id_create` | Create a digital ID | — | — |
| 102 | `sign_windows_ids` | List Windows store digital IDs | read-only | sign.digital |
| 103 | `sign_keychain_ids` | List Keychain digital IDs | read-only | sign.digital |
| 104 | `sign_document` | Sign a document | — | sign.digital |
| 105 | `sign_trust` | Trust certificates | — | — |
| 106 | `comment_mark` | Mark a comment with a checkmark | — | — |
| 107 | `comment_lock` | Lock a comment | — | — |
| 108 | `layer_set` | Show or hide a layer | — | — |
| 109 | `comments_hide` | Hide all comments | — | comment.hide_all |
| 110 | `view_reading_colors` | Set reading colours | — | a11y.reading_options |
| 111 | `comments_summarize` | Summarize comments | — | comment.summarize |
| 112 | `comment_edit` | Edit a comment | — | — |
| 113 | `comment_image_preview` | Preview image signature layers | read-only | — |
| 114 | `comment_delete` | Delete a comment | destructive | — |
| 115 | `comment_popup` | Open, close or move a comment's pop-up | — | — |
| 116 | `comments_copy` | Copy comments | read-only | — |
| 117 | `comments_paste` | Paste comments | — | — |
| 118 | `doc_protect` | Protect with passwords | — | protect.password |
| 119 | `doc_unprotect` | Remove security | destructive | protect.remove |
| 120 | `page_replace` | Replace pages | — | page.replace |
| 121 | `page_duplicate` | Duplicate pages | — | page.duplicate |
| 122 | `page_transition_set` | Set page transitions | — | — |
| 123 | `page_set_box` | Set page boxes / crop | — | page.boxes |
| 124 | `doc_header_footer` | Add header and footer | — | edit.header_footer |
| 125 | `doc_watermark` | Add watermark | — | edit.watermark |
| 126 | `doc_background` | Add background | — | edit.background |
| 127 | `doc_printer_marks` | Add printer marks | — | prepress.marks |
| 128 | `doc_backdrops` | List page backdrops | read-only | edit.background |
| 129 | `doc_remove_marks` | Remove header & footer, watermark, background or printer marks | destructive | — |
| 130 | `doc_export_images` | Export pages as images | — | export.image |
| 131 | `accessibility_autotag_preview` | Preview automatic tags | read-only | — |
| 132 | `accessibility_autotag_apply` | Automatically tag text-only PDF | — | — |
| 133 | `accessibility_autotag_form_fields` | Tag form fields | — | a11y.autotag_fields |
| 134 | `accessibility_check` | Check for accessibility | read-only | a11y.check |
| 135 | `accessibility_find_untagged` | Find untagged content | read-only | a11y.find_untagged |
| 136 | `accessibility_report` | Accessibility report | destructive | a11y.report |
| 137 | `accessibility_review_record` | Accessibility review record | destructive | — |
| 138 | `accessibility_review_save` | Save accessibility review decisions | destructive | — |
| 139 | `accessibility_review_load` | Open accessibility review decisions | read-only | — |
| 140 | `accessibility_review_html` | Accessibility review summary | destructive | — |
| 141 | `accessibility_fix` | Fix an accessibility problem | — | — |
| 142 | `accessibility_figures` | List figures | read-only | a11y.alt_text |
| 143 | `accessibility_set_alt` | Set alternate text | — | a11y.alt_text |
| 144 | `accessibility_tags` | List structure tags | read-only | a11y.tags |
| 145 | `accessibility_tag_content` | List tag content | read-only | a11y.tags |
| 146 | `accessibility_set_tag_property` | Edit tag property | — | — |
| 147 | `accessibility_mark_tag_artifact` | Mark tag content as artifact | — | — |
| 148 | `accessibility_layout_table_to_blocks` | Change layout table to blocks | — | — |
| 149 | `accessibility_move_tag` | Move structure tag | — | — |
| 150 | `form_merge_data` | Merge data files into spreadsheet | — | form.merge_data |
| 151 | `js_run` | Run JavaScript | — | tools.js_console |
| 152 | `js_event` | Run a field's pointer or focus script | — | — |
| 153 | `js_document_scripts` | Document JavaScripts | read-only | tools.document_js |
| 154 | `js_set_document_script` | Edit a document JavaScript | — | tools.document_js |
| 155 | `form_set_script` | Set a field's JavaScript | — | form.prepare |
| 156 | `doc_export_office` | Export to Word, PowerPoint, HTML, RTF or Markdown | — | export.docx |
| 157 | `pdfa_verify` | Verify PDF/A | read-only | standards.pdfa |
| 158 | `print_readiness` | Print readiness | read-only | — |
| 159 | `pdfa_convert` | Save as PDF/A | — | standards.pdfa |
| 160 | `standards_remove_id` | Remove PDF/A or PDF/X identification | — | — |
| 161 | `action_list` | List actions | read-only | actions.wizard |
| 162 | `action_run` | Run an action | — | actions.wizard |
| 163 | `doc_compare` | Compare files | read-only | doc.compare |
| 164 | `doc_compare_report` | Compare report | — | doc.compare |
| 165 | `doc_compare_mark` | Mark differences as comments | — | doc.compare |
| 166 | `form_detect_fields` | Detect form fields | — | form.detect |
| 167 | `form_actions` | Field actions | read-only | form.prepare |
| 168 | `form_set_actions` | Set field actions | — | form.prepare |
| 169 | `js_enabled` | JavaScript on or off | — | — |
| 170 | `ocr_recognize` | Recognize text (OCR) | — | ocr.recognize |
| 171 | `ocr_words` | Words of a recognition (for review) | read-only | — |
| 172 | `ocr_review_apply` | Apply or discard reviewed OCR words | — | ocr.correct |
| 173 | `ocr_dictionary` | Read or update an OCR review dictionary | destructive | ocr.correct |
| 174 | `ocr_recognize_files` | Recognize text in multiple files | — | ocr.recognize_batch |
| 175 | `ocr_status` | OCR status | read-only | ocr.recognize |
| 176 | `doc_export_all_images` | Export all images | — | export.all_images |
| 177 | `doc_export_text` | Export text | — | export.text |
| 178 | `fill_sign_add` | Fill & Sign: type text or place a mark | — | sign.fill.text |
| 179 | `fill_sign_date_format` | Date format for Fill & Sign | — | — |
| 180 | `doc_create` | Create a PDF | — | — |
| 181 | `doc_reduce` | Reduce file size | — | optimize.reduce |
| 182 | `doc_initial_view` | Initial view | — | — |
| 183 | `doc_audit_space` | Audit space usage | read-only | optimize.advanced |
| 184 | `text_lines` | List text lines | read-only | edit.edit_text |
| 185 | `image_hit` | Hit test page artwork | read-only | edit.edit_text |
| 186 | `page_images` | List page images | read-only | edit.edit_text |
| 187 | `image_edit` | Edit an image | — | edit.edit_text |
| 188 | `image_save` | Save image as | destructive | edit.edit_text |
| 189 | `text_font_files` | List installed document fonts | read-only | edit.edit_text |
| 190 | `text_font_import` | Load document font | — | edit.edit_text |
| 191 | `text_fonts` | List document fonts | read-only | edit.edit_text |
| 192 | `text_prepare` | Prepare grouped text | — | edit.edit_text |
| 193 | `text_paragraphs` | List paragraphs | read-only | edit.edit_text |
| 194 | `text_edit_layout` | Measure text draft | read-only | edit.edit_text |
| 195 | `text_edit` | Edit text | — | edit.edit_text |
| 196 | `text_script` | Superscript or subscript | — | edit.edit_text |
| 197 | `doc_revisions` | List revisions | — | — |
| 198 | `doc_open_revision` | Open a revision | — | — |
| 199 | `doc_optimize` | Optimize PDF | — | optimize.advanced |
| 200 | `doc_flatten` | Flatten | destructive | — |
| 201 | `xfa_to_static` | Convert an XFA form to a static form | destructive | — |
| 202 | `edit_undo` | Undo | — | edit.undo |
| 203 | `edit_redo` | Redo | — | edit.redo |
| 204 | `command_list` | List commands | read-only | — |
| 205 | `command_run` | Run a command | destructive | — |
| 206 | `command_batch` | Run several commands | destructive | — |
| 207 | `doc_inspect` | Inspect open documents | read-only | — |
| 208 | `render_preview` | Render a preview | read-only | — |

## Notes on selected tools

- `attachment_add` / `attachment_delete` / `attachment_edit` (`crates/automation/src/dispatch.rs`)
  add, remove or rename a **document-level** attachment (the Attachments panel entry, not a
  paper-clip page comment). The added one keeps a unique key, defaults its name to the file name
  and is undoable. `doc_info` lists attachments and their descriptions. There is still **no tool
  that extracts/saves an attachment**: the panel can open or save one, the automation table cannot.
- `bookmark_set_style` (`crates/organize/src/outline.rs:654` for `/C`, `:666` for `/F`) sets a
  bookmark's colour and bold/italic flag; `bookmark_list` reports both. It does not change nesting
  or targets. `bookmark_export`/`bookmark_import`/`bookmark_copy` move whole trees instead
  (`crates/organize/src/outline_io.rs`).
- `content_copy` (`crates/automation/src/content.rs`) pastes an **added** text box or image (from
  `content_list`) into the same or another open document, keeping type, font, size, colour,
  alignment, box, rotation, flips and crop. 18 pt cascade per existing copy, at an explicit `at`,
  refused when the source document withholds copying. It copies added content only.
  `object_copy` / `object_paste` (new at v0.21.1; `crates/engine/src/{rich_copy,object_clip}.rs`)
  copy 1–1000 mixed `object_list` references with every font, image, ExtGState, colour space,
  pattern and shading they use, within or between documents; pasted content is untagged and in no
  layer. `object_copy` refuses text used as a clipping path, and a shared comment id is refused by
  the `comment_*` tools.
- `text_replace` (`crates/engine/src/find_replace.rs`) rewrites a match inside its own paragraph,
  keeping fonts/sizes/colours and rewrapping; a longer replacement can overlap what follows,
  unreported. It counts matches it leaves alone in `skipped_by` (`spans_paragraphs`,
  `scanned_text`, `missing_glyphs`, `refused`, `not_editable`). `text_prepare` makes grouped text
  inside supported Form XObjects editable on one page and reports `prepared_groups`,
  `repaired_fonts` and `refused_groups`.
- `doc_fix_hairlines`, `doc_convert_colours` and `doc_printer_marks` are **prepress**, not a
  Preflight: `doc_convert_colours` uses device formulas (no ICC profile or output intent), keeps
  spot colours only as approximations and reports `loses_conformance`; `doc_printer_marks` adds
  trim/bleed marks, registration targets, colour bars and a page-information line and may widen
  the page (`make_room`). `doc_remove_marks kind=printer_marks` takes them off. `printer_papers`
  lists a driver's media names and default; the paper can be passed to `doc_print` by that name.
- `model_render` draws a page's **PRC** model and can choose `view` (iso/front/right/top/back),
  `up`, `front`, `turn`, `zoom`, `zoom_at`, `pan` or a raw `direction`; U3D still cannot be drawn.
- `doc_optimize` now also discards an embedded search index (`discard_search_index`), links to
  other documents (`discard_external_refs`) and form submit/import/reset actions
  (`discard_form_actions`), and can retry toward `target_bytes`.
- `comment_popup` opens, closes or moves a comment's pop-up; text boxes, Fill & Sign marks and
  replies have none of their own. `stamp_custom`'s `line` adds a dynamic-style text line under the
  picture. `form_focus` and `js_event` run a field's enter/exit or widget pointer/focus scripts;
  `accessibility_layout_table_to_blocks` turns a layout table into Div/P blocks.
- `doc_open` accepts Adobe open parameters on the path (`manual.pdf#page=12`,
  `#nameddest=Intro`, `#Intro`) and reports the applied destination; other parameters are ignored.
