# After Effects projects in EffectCraft (v0.24.1)

Reference for the `file.importAep` / `file.exportAep` surface, and for `file.import` when it is
handed an After Effects project. Everything here is grounded in `crates/aep/` (container, import,
export), `crates/engine/src/cmd/aep.rs`, `crates/engine/src/cmd/file.rs` and the three format
notes (`docs/aep-format.md`, `docs/aep-import.md`, `docs/aep-export.md`). The import note was last
updated 2026-11-11, the export note 2026-11-05; where a note and the code disagree, the code wins.

## Commands

```
file.importAep {path (.aep or .aepx), allowLosses?: bool, dryRun?: bool, applySettings?: bool}
  -> {folder, comps, items, report}
file.exportAep {path (.aep), allowLosses?: bool, dryRun?: bool}
  -> {path, bytes, report}
```

- Import adds the file's items to the **open project** in a folder named after the file, inside one
  undoable edit; the first composition opens. It never replaces the project.
- `applySettings` is true by default only when the project has no compositions yet: the import does
  not silently rewrite settings of a project that is already in use.
- **Routes.** File ▸ Import ▸ **Adobe After Effects Project…** and File ▸ Export ▸ Adobe After
  Effects Project… are the menu entries. `file.import` / `file.importMultiple` also accept
  `.aep`/`.aepx` (and `.ecproj`/`.ecprojx`), import each as a project and return them under
  `projects`; a file that would lose parts comes back as an `errors` entry that points at
  `file.importAep`, because `file.import` has no `allowLosses`. A dropped or picked project goes
  through the same path, one losses prompt at a time.
- **Loss policy.** Without `allowLosses`, an import or export that would lose anything is refused
  with an error naming the categories (`importing would lose effects: 3, markers: 1; allow losses
  to import anyway`) and changes nothing. With `allowLosses: true` it proceeds and returns the same
  report. `dryRun: true` returns only the report — use it before committing.
- **Report shape.** Each category carries an exact `count`, up to 20 example `details` lines and an
  `unlisted` count for the rest (`crates/aep/src/import/report.rs`, `MAX_DETAILS = 20`); unmapped
  effects are listed most used first.
- `missingFonts` is reported but is **not** a loss: the text keeps the font name and is drawn with
  the fallback font.

## The container

- An `.aep` is a `RIFX` container (big-endian RIFF) with form type `Egg!`: chunks of a 4-byte id, a
  big-endian `u32` size and a body padded to an even length; `LIST` chunks start with a 4-byte list
  type. `parse` builds the tree and `write` serialises it, and for every input that parses
  `write(parse(x)) == x` byte for byte — pad bytes, odd bodies and the XMP packet after the
  container are preserved.
- `.aepx` (the XML form) is read into the same tree by `read_aepx`, a small bounded XML tokenizer
  with no dependency; `parse_any` picks the reader by content. **`.aepx` is a read path only.**
- Input is untrusted: sizes are checked against the remaining input, nesting and chunk count are
  bounded (`Limits`), nothing is allocated from a declared size, and truncated or damaged files
  return `Err`. Bodies that look like lists but are not chunk sequences stay opaque instead of
  failing the parse.
- The crate does no file access — callers pass bytes — so it builds for wasm32 and is shared by
  every frontend.

## What the importer covers

Areas the reader decodes and maps into the project model (`docs/aep-import.md`, per area with the
corpus case numbers that back it):

| Area | Notes |
|---|---|
| Project tree | folders (nesting and order), compositions, solids, footage items, item labels |
| Project settings | colour depth, working space (None, sRGB, Rec. 709 Gamma 2.4; another is reported), working gamma, Linearize Working Space, Blend Colors Using 1.0 Gamma, time display, frame count start |
| Composition | name, size, exact frame rate, duration, work area, background, pixel aspect, motion blur switch/shutter, display start, Classic/Advanced 3D renderer |
| Layers | solid, null, adjustment, footage, precomposition and text: times and stretch, switches (enabled/audio/solo/shy/locked/effects/motion blur/collapse/3D/guide), label, blend mode, parent, track matte (alpha/luma, inverted or not, matte layer above or below). An unnamed text layer takes the **first 40 characters of its first line**, as EffectCraft names a text layer after its text |
| Transform | Anchor Point, Position, Scale, Rotation, Opacity, X/Y Rotation, Orientation; static or keyed, with per-side interpolation, temporal ease, spatial tangents and roving keys. A keyed or expression-driven **Orientation** imports with its value or keys (#3087); After Effects slerps between keys where EffectCraft interpolates each angle, so in-between values can differ |
| Expressions | on transform/mask properties and on effect, camera and light parameters, with the enable switch |
| Cameras and lights | one- and two-node cameras (POI, position, zoom, DoF, focus distance, aperture); spot, point, parallel and ambient lights. Environment lights are reported |
| Text | Source Text with style runs (font by PostScript name, size, fill/stroke, tracking, leading, faux styles, caps, superscript/subscript, scales, kerning, ligatures, tsume), paragraph settings, point or box text, vertical text; text animators with range selectors |
| Masks | stack order, path with tangents, mode, inverted, feather (x/y), opacity, expansion, path keys; a mask with no stored path arrives as the source rectangle |
| Effects | one shared table for both directions (`effectcraft_aep::effect_map`): Lumetri Color, Curves, Mesh Warp, Tint, Gradient Ramp, Exposure, Invert, the blurs, Drop Shadow, Glow, Fill, Hue/Saturation, Levels, Timewarp, Channel Blur, Black & White, Tritone, Luma Key, the chokers, Transform, HDR Highlight Compression, Echo, Linear Wipe, Offset, Color Stabilizer, CC Color Neutralizer, EXtractoR, IDentifier, and the five expression controls. **Effects outside the table are reported, not imported**; Puppet arrives with its name and fx switch but without meshes and pins |
| Layer styles | the nine styles plus Blending Options; Global Light becomes the composition's |
| Shape layers | groups, rectangle/ellipse/polystar/bezier path, fill/stroke/gradient, trim paths, round corners, merge paths, offset paths, repeater |
| Markers | layer and composition markers with duration, comment, chapter, URL, frame target, label, cue point |
| Time Remapping | an enabled remap becomes the `timeRemap` property with its keys and expression |
| Footage | a link to the stored path, a missing-footage placeholder when it is absent (`missingFootage`), or a whole image sequence (a sequence needs no filename prefix and honours Force alphabetical order); the importer never opens footage. A placed `.ai`/`.pdf` is framed by its ArtBox (clipped to the crop box, `/Rotate` ignored) and drawn to fill the stored footage size |

Unit conversions that matter when comparing renders: Anchor Point arrives as pixels (stored as a
fraction of source size), Scale and Opacity as percent, keyframe times as exact `Tick`s snapped to
the composition frame grid, NTSC rates as 30000/1001 and 24000/1001.

**Lumetri Color** (`crates/aep/src/import/lumetri.rs`) is mapped by match-name suffix, not index:
every slider, checkbox and popup with a counterpart (also from records in the default state), the
master RGB curve's points, Hue vs Sat's points and the three colour wheels. EffectCraft's effect has
no section switches, so a section that is off in After Effects contributes nothing and its set
values are reported in one line instead of imported; LUTs, looks and undecoded curves and wheels
are reported.

**Puppet** (`crates/aep/src/import/puppet.rs`) arrives as EffectCraft's Puppet with its name and
switch; a pin's rest place lives in the mesh data, which is not decoded yet, so the report gives
each mesh's Triangles, Expansion and each pin group's pins, keyed pins and atom match names.

## What neither direction does

- **Not read or written:** `.ffx` animation presets, `.mogrt` templates, AE SDK plug-ins (`.aex` /
  `.plugin`, a different ABI), `.prproj`. Those stay out of scope.
- **Reported rather than carried:** effects outside the table, Puppet meshes and pins, undecoded
  text and style settings, approximated keyframes (a bezier mask-path side becomes linear), mask
  colour/lock/feather falloff/motion blur/RotoBezier, and anything the exporter cannot build.
- **Render parity is not promised.** The importer's render checks compare specific cases against
  After Effects; the rest is self-graded. A clean import report means "nothing was dropped", not
  "it looks the same".

## What the exporter writes

- Every chunk is built in code from the project — no `.aep` template file is read. The project
  skeleton, layer blocks (AV, null, text, camera, light, shape), property records, effects from the
  same shared table, layer styles, masks, markers, text animators, footage items, ICC profiles
  authored by the crate, and the text document.
- Bytes After Effects needs but whose meaning is not decoded are written as the value observed in
  every generated test file, named as a constant; everything else undecoded is zero. The file ends
  with a neutral XMP packet authored by the crate.
- Case-by-case read-back and render checks against After Effects are recorded in
  `docs/aep-export.md`; treat "exported" as "After Effects opens it and the covered features
  agree", not "pixel-identical".

## Test-corpus caveat (read this before claiming verification)

The importer's corpus tests are **opt-in**. Test fixtures are not in this repository: they live in
`storytold/effectcraft-corpus` and `cargo xtask aep-corpus` fetches them at the commit pinned in
`crates/aep/tests/fixtures/corpus.lock`, verifying each SHA-256. Without
`EFFECTCRAFT_AEP_FIXTURES`, a test whose fixture is missing prints `SKIPPED: fixture <name>
missing` **and passes**. Only `crates/aep/tests/fixtures/synthetic.aep` ships in the repo, so a
plain `cargo test` proves much less about `.aep` import than its green output suggests. Set
`EFFECTCRAFT_AEP_FIXTURES` (and `EFFECTCRAFT_AEP_FIXTURES_REQUIRED=1`) when a real answer matters.

## Agent recipe

1. `effectcraft-cli exec file.importAep '{"path":"in.aep","dryRun":true}'` — read `report`, including
   each category's `unlisted` count.
2. Decide: import with `allowLosses: false` (clean) or `true` (accept the listed losses). Never
   silently pass `true` on a user's file.
3. Import into a scratch `.ecproj`, render one frame per imported composition, compare against the
   user's After Effects reference if there is one.
4. `file.exportAep {"dryRun": true}` before writing an `.aep`; the report is the honest scope list.
5. Report the exact command, the report contents, and the render you actually looked at.
