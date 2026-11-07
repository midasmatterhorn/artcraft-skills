# WordCraft — round 2026-11-07 changes

Re-pinned: v0.15.1 (`08afab5`) -> v0.16.0 (`02a802c`, installed `wordcraft 0.16.0 (02a802cb)`).

## Corrected / re-measured

- `CommandSpec::new` command set 652 -> **656** live ids; the four additions are `font.missing`, `format.emphasisMark`, `select.member` and `smartArt.itemColor`. A raw site count now prints 658 because two `CommandSpec::new` test fixtures were added in `crates/engine/src/tests.rs`.
- Catalog coverage 505/520 -> **506/521 (97.1%)**: one row added (`Home › Font › Emphasis Mark`). The generated `docs/parity-checklist.md` was not regenerated and still prints 505/520 — recorded as drift.
- Control-channel methods 21 -> **22**: `file.closeDocument` is a dispatched method now (`id`/`force`, unsaved-work refusal). It was already an engine command.
- Open / save extensions 21 / 14 -> **23 / 16**: `.ott` and `.fodt` added to both. The ODT reader/writer lands the gap-19 ODT work this release (nearly whole documents opened, edited and saved), and a password-protected `.odt`/`.ott` now saves with its password.
- Interface languages: the published skill said 27, code says **28** at both tags (`LANGUAGES: [LangInfo; 28]`). Corrected and marked unchanged at v0.16.0. `craft-i18n.rev` moved to `1e515422…`, so catalogs were rebuilt, but the language set did not change.
- Built-in proofing variants: the published skill said 15; **16** at both tags (the list was missing English (Australia)). Corrected and marked unchanged.
- Default shortcuts: the published skill said 167; **166** `.key()` specs at both v0.15.1 and v0.16.0. Corrected.
- Open extensions: the published skill said 19; **21** at v0.15.1, **23** now. Corrected.
- Dialog names: the published skill said 89 at v0.11.0 and "~90"; **91** distinct `Dialog::name` values at both tags. Re-measured.
- Removed the "no MHT" limitation: `.mht`/`.mhtml` were already in `OPEN_EXTS` at v0.15.1 and are read by `crates/formats/src/mht.rs`. Saving MHT is still missing (gap 26). The import list now names `.mht`/`.mhtml`, `.ott` and `.fodt`.
- Fixed one dead citation: `crates/proof/src/lang.rs` no longer exists (proofing moved to craft-libs `craft-proof`); re-cited `crates/ui-egui/src/ribbon/language.rs` and `crates/ui-egui/src/language_packs.rs`.
- Installed-bundle line fixed: the previous round contradicted itself (its audit basis said `wordcraft 0.15.1 (08afab50)`, its Sources section 0.12.0 `(3de6ff95)`, its evidence ledger 0.14.0 `(08afab58)`). This round the bundle is 0.16.0 and its binary prints `wordcraft 0.16.0 (02a802cb)`.

## Method

- Diff `v0.15.1..v0.16.0` read directly in the clone: **475 files, +50,297 / −4,226**. The clone's history is squashed (one commit per tag), so the compare-API commit count is not quoted as a measurement.
- Command, control-method, MCP-tool, CLI, language, proofing, shortcut, format and dialog counts were extracted from code with the commands listed in `evidence.md` at both tags; changed sets are named, unchanged sets are labelled "unchanged at v0.16.0" in `SKILL.md`.
- The installed bundle's `--version` and `-h` were run read-only (they return before the window opens); the GUI was never launched. No build, no commit, no clone change.
- Every repo-relative path cited in `SKILL.md` was re-resolved in the clone; the one dead path was re-cited.

## Unchanged

- MCP tools **17**, CLI subcommands **10**, CLI flags **21** (+ `-h/--help`, `--version`), interface languages **28**, built-in proofing **16**, shortcuts **166**, dialog names **91** — each verified at both tags.
- The CLI/control/MCP shapes this skill documents (tool names, method names, script caps, control-key scheme, personal-template rules, recovery and Zotero notes) did not move; the control set gained one method only.
- Older history (v0.12.0–v0.14.0) is folded into one compact "Carried from" subsection; the two most recent delta paragraphs below the new one are kept.

## Known gap in this round

- `wordcraft-cli` is not in the app bundle and no CLI artifact was available on the authoring machine, so the strongest live check (`commands --json`, `parity`, a real conversion) could not be run; counts are code-derived and the installed binary contributed only its version/help text.
- GUI-only changes from the release wave (modal dialogs, Read Mode page colour, mirrored Arabic dialogs, AccessKit focus guard) were not observed; they are noted as landed with their files, not verified by use.
- PDF/printing field freshness (SEQ/STYLEREF/REF) appears in the release notes but was not re-derived from code, so `SKILL.md` does not claim it.
