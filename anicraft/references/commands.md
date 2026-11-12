# AniCraft command registry, shortcuts and recipes

Companion to `SKILL.md`. Counts and ids were read from `anicraft-cli commands` at **v0.2.1**
(commit `d0beaf253274948b55ee9e1107749f9491bff880`) and checked against
`crates/engine/src/lib.rs` `commands()`.

## How the registry is shaped

Every command has `id`, `label`, `menu`, `shortcut` (nullable), `params` (a human-readable
description of the JSON keys) and `mutates`. `anicraft-cli commands` prints the same list the
GUI builds its menus from; ids are stable English, param names are stable English, and both stay
untranslated even when the interface language changes.

Use ids exactly as printed. The examples below show only the keys a command needs; the `params`
string in the registry is the authoritative list, including optional keys.

## Namespaces (33, 240 commands)

| Namespace | Count | Representative ids |
|---|---:|---|
| `file` | 24 | `file.new`, `file.open`, `file.save`, `file.export_png`, `file.import`, `file.publish` |
| `edit` | 10 | `edit.undo`, `edit.redo`, `edit.select_all`, `edit.cut`, `edit.copy`, `edit.paste` |
| `doc` | 2 | `doc.set_stage`, `doc.info` |
| `publish` | 2 | `publish.settings_get`, `publish.settings_set` |
| `prefs` | 3 | `prefs.recent_pin`, `prefs.recent_remove`, `prefs.recent_clear` |
| `timeline` | 21 | `timeline.insert_frame`, `timeline.insert_keyframe`, `timeline.create_tween`, `timeline.create_shape_tween` |
| `layer` | 16 | `layer.new`, `layer.new_folder`, `layer.set_type`, `layer.toggle_mask`, `layer.set_volume` |
| `camera` | 4 | `camera.add`, `camera.remove`, `camera.set`, `camera.info` |
| `bone` | 7 | `bone.add`, `bone.remove`, `bone.set_limits`, `bone.pin` |
| `motion` | 13 | `motion.set_key`, `motion.remove_key`, `motion.set_ease`, `motion.info` |
| `tween` | 5 | `tween.add_hint`, `tween.move_hint`, `tween.remove_hint`, `tween.clear_hints` |
| `scene` | 9 | `scene.new`, `scene.duplicate`, `scene.rename`, `scene.delete` |
| `frames` | 9 | `frames.artwork`, `frames.edit_multiple`, `frames.transform`, `frames.align` |
| `draw` | 14 | `draw.rect`, `draw.ellipse`, `draw.star`, `draw.path`, `draw.brush`, `draw.erase` |
| `element` | 15 | `element.select`, `element.pick`, `element.translate`, `element.set_transform`, `element.set_color_effect` |
| `symbol` | 4 | `symbol.set_kind`, `symbol.set_scale_grid`, `symbol.edit`, `symbol.exit` |
| `arrange` | 4 | `arrange.bring_to_front`, `arrange.bring_forward`, `arrange.send_backward`, `arrange.send_to_back` |
| `modify` | 8 | `modify.convert_to_symbol`, `modify.break_apart`, `modify.rotate_cw`, `modify.rotate_ccw` |
| `library` | 10 | `library.place`, `library.items`, `library.new_folder`, `library.rename` |
| `align` | 8 | `align.left`, `align.hcenter`, `align.right`, `align.top` |
| `path` | 5 | `path.move_points`, `path.add_point`, `path.delete_points`, `path.convert_point` |
| `raw` | 11 | `raw.move_point`, `raw.select_rect`, `raw.merge`, `raw.hit` |
| `find` | 3 | `find.search`, `find.replace`, `find.goto` |
| `explorer` | 1 | `explorer.tree` |
| `paint` | 4 | `paint.bucket`, `paint.ink`, `paint.pick`, `paint.apply_style` |
| `text` | 3 | `text.create`, `text.edit`, `text.fonts` |
| `stroke` | 5 | `stroke.set_profile`, `stroke.set_width_point`, `stroke.delete_width_point`, `stroke.width_at` |
| `plugin` | 5 | `plugin.install`, `plugin.list`, `plugin.run`, `plugin.remove`, `plugin.reload` |
| `sound` | 5 | `sound.place`, `sound.set`, `sound.remove`, `sound.delete` |
| `control` | 1 | `control.test_movie` |
| `actions` | 3 | `actions.set`, `actions.clear`, `actions.list` |
| `instance` | 1 | `instance.set_name` |
| `script` | 5 | `script.set`, `script.clear`, `script.list`, `script.check`, `script.set_class` |

Counts are the registry at this tag; a later release may add ids. Re-run
`anicraft-cli commands` rather than assuming one.

## Default shortcuts (52 registry commands)

macOS displays these with ⌘ and the Apple modifier order; the registry spelling is `Ctrl+…`
(`src/platform.rs`). Every one is rebindable in the in-app shortcut editor (`F1`).

| Keys | Command | Keys | Command |
|---|---|---|---|
| `Ctrl+N` | `file.new` | `Ctrl+O` | `file.open` |
| `Ctrl+S` | `file.save` | `Ctrl+Shift+S` | `file.save_as` |
| `Ctrl+R` | `file.import` | `Ctrl+Z` | `edit.undo` |
| `Ctrl+Y` | `edit.redo` | `Ctrl+Shift+F12` | `publish.settings_get` |
| `Shift+F12` | `file.publish` | `F5` | `timeline.insert_frame` |
| `Shift+F5` | `timeline.remove_frame` | `F6` | `timeline.insert_keyframe` |
| `F7` | `timeline.insert_blank_keyframe` | `Shift+F6` | `timeline.clear_keyframe` |
| `.` | `timeline.next_frame` | `,` | `timeline.prev_frame` |
| `Home` | `timeline.first_frame` | `End` | `timeline.last_frame` |
| `Ctrl+Shift+H` | `tween.add_hint` | `Shift+PageUp` | `scene.prev` |
| `Shift+PageDown` | `scene.next` | `Ctrl+Alt+X` | `timeline.cut_frames` |
| `Ctrl+Alt+C` | `timeline.copy_frames` | `Ctrl+Alt+V` | `timeline.paste_frames` |
| `J` | `draw.object_drawing` | `Ctrl+Shift+/` | `draw.snap_to_objects` |
| `Ctrl+A` | `edit.select_all` | `Ctrl+Shift+A` | `edit.deselect` |
| `Delete` | `edit.delete` | `Ctrl+D` | `edit.duplicate` |
| `Ctrl+Shift+Up` | `arrange.bring_to_front` | `Ctrl+Up` | `arrange.bring_forward` |
| `Ctrl+Down` | `arrange.send_backward` | `Ctrl+Shift+Down` | `arrange.send_to_back` |
| `F8` | `modify.convert_to_symbol` | `Ctrl+B` | `modify.break_apart` |
| `Ctrl+X` | `edit.cut` | `Ctrl+C` | `edit.copy` |
| `Ctrl+V` | `edit.paste` | `Ctrl+Shift+V` | `edit.paste_in_place` |
| `Ctrl+Shift+9` | `modify.rotate_cw` | `Ctrl+Shift+7` | `modify.rotate_ccw` |
| `Ctrl+Shift+Z` | `modify.remove_transform` | `Ctrl+Alt+1` | `align.left` |
| `Ctrl+Alt+2` | `align.hcenter` | `Ctrl+Alt+3` | `align.right` |
| `Ctrl+Alt+4` | `align.top` | `Ctrl+Alt+5` | `align.vcenter` |
| `Ctrl+Alt+6` | `align.bottom` | `Ctrl+E` | `symbol.edit` |
| `Ctrl+F` | `find.search` | `Ctrl+Enter` | `control.test_movie` |

Tool keys (also rebindable; `src/app.rs` `Tool::shortcut`): `V` selection, `A` subselection,
`Q` free transform, `U` width, `M` bone, `P` pen, `T` text, `Shift+Y` pencil, `B` brush,
`E` eraser, `R` rectangle, `O` oval, `N` line, `K` paint bucket, `S` ink bottle, `I` eyedropper,
`C` camera, `H` hand, `Z` zoom; PolyStar has no default key.

View keys (`src/app.rs` `VIEW_SHORTCUTS`): `Ctrl+2` fit, `Alt+Shift+O` onion skin,
`Ctrl+Alt+A` select all frames, `Ctrl+Alt+8` align to stage, `Ctrl+F6` next panel,
`Ctrl+Shift+F6` previous panel, `F9` Actions, `F3`/`Shift+F3` find next/previous,
`Alt+F3` Movie Explorer, `[`/`]` brush size. `Ctrl+K` opens the command palette and `F1` the
shortcut editor (`src/keymap.rs`, `src/dialogs.rs`).

## Recipes

### Create, draw, save, inspect (no selection assumptions)

```json
[
  {"cmd": "file.new",  "params": {"width": 1280, "height": 720, "fps": 24}},
  {"cmd": "layer.new", "params": {"name": "Artwork"}},
  {"cmd": "draw.rect", "params": {"x": 80, "y": 80, "w": 240, "h": 140, "fill": "#3366cc"}},
  {"cmd": "file.save", "params": {"path": "work.anicraft"}}
]
```

Run it with `anicraft-cli run --sample script.json --save work.anicraft`, then
`anicraft-cli info work.anicraft` and `anicraft-cli render work.anicraft --frame 1 --out check.png`.

### Animation

Commands act on the **current scene, layer, frame and selection**, which
`anicraft_document`/`info` reports. A typical sequence:

* frames: `timeline.insert_frame`, `timeline.remove_frame`, `timeline.insert_keyframe`,
  `timeline.insert_blank_keyframe`, `timeline.clear_keyframe`, `timeline.goto`;
* tweens: `timeline.create_tween {easing?}`, `timeline.create_shape_tween`,
  `timeline.create_motion_tween`, `timeline.remove_tween`, `timeline.set_easing`,
  `timeline.set_orient`;
* shape hints: `tween.add_hint`, `tween.move_hint`, `tween.remove_hint`;
* motion editor: `motion.set_key`, `motion.remove_key`, `motion.set_ease`, `motion.info`,
  `motion.set_path`, `motion.pin_point`;
* multi-frame editing: `frames.edit_multiple`, `frames.artwork` (what the range shows),
  `frames.transform`, `frames.align`, `frames.delete` / `copy` / `cut` / `paste` / `merge`,
  `timeline.cut_frames` / `copy_frames` / `paste_frames`.

Onion skin is view state in the shell (its on/off and range live in the app, not the document),
so there is no `onion.*` command; `frames.artwork` reports the elements Edit Multiple Frames
shows.

Move playheads with `timeline.goto {frame}` (0-based) before editing frame-specific content.
Move selected artwork with `element.translate {dx,dy}` or `element.set_transform
{x?,y?,sx?,sy?,rotation?}`.

### Symbols and library

* `modify.convert_to_symbol {kind?, name?, folder?}` creates a symbol from the selection.
* `symbol.edit` / `symbol.exit` open and leave a symbol in place.
* `symbol.set_kind {kind: graphic|movie_clip|button}`.
* `symbol.set_scale_grid {on?, left?, right?, top?, bottom?}` sets 9-slice guides.
* `library.place {symbol|bitmap|sound | items:[…], x?, y?}` places items at the playhead.
* `library.items`, `library.new_folder`, `library.rename`, `library.move`, `library.duplicate`,
  `library.delete`, `library.unused`, `library.delete_unused`, `library.set_smoothing`.

### Colour, filters and blending

* `element.set_fill {color}`, `element.set_stroke {color?, width?, cap?, join?, style?, dash?}`.
* `element.set_alpha {alpha}`, `element.set_color_effect {style, …}` (styles: none, brightness,
  tint, advanced, alpha).
* `element.set_blend {mode}` — normal, layer, darken, multiply, lighten, screen, overlay,
  hardlight, add, subtract, difference, invert, alpha, erase.
* `element.set_filters {filters:[{type: blur|drop_shadow|glow|bevel|gradient_glow|gradient_bevel|adjust_color, …}]}`
  (movie clips and buttons).

### Sound

* `file.import_to_library {path, name?}` adds a WAV/Ogg/MP3 or PNG/JPEG.
* `sound.place {sound, layer?, frame?, sync?, repeat?, loop?, effect?, envelope?}`.
* `sound.set {…}` changes sync/repeat/effect/envelope; `sound.remove` takes it off a keyframe;
  `sound.delete` removes it from the library and every keyframe.
* `layer.set_volume`, `layer.toggle_mute`.
* `file.export_audio {path, from?, to?, rate?, bits?}` writes WAV.

### Find, inspect, publish

* `find.search {kind: text|font|color|symbol|sound|bitmap, …}` → located hits, paged.
* `find.replace` (one hit with `at`, or all; one undo step).
* `find.goto {…}` opens the scene/frame/symbol; `explorer.tree {scope?, show?}` pages the tree.
* `publish.settings_get {}`, `publish.settings_set {format?, enabled?, output?, …}`,
  `file.publish {formats?, confirm?}`.

### Interactivity

* `actions.set {actions:[…]}` or `{element, event, actions}`; `actions.clear`, `actions.list`.
* `instance.set_name {element?, name}` names a movie clip or button for ActionScript.
* `script.set {text, language?, symbol?, layer?, frame?}` keeps a frame script;
  `script.check {text}` reports what the subset supports; `script.list` shows kept scripts.
* `control.test_movie {frames?, events?, seed?}` plays the movie headless and returns output,
  sounds started and end state.

## Format matrix

| Direction | Formats | Command / path |
|---|---|---|
| Open | `.anicraft` (v1/v2/v3) | `file.open`; `crates/engine/src/format.rs` |
| Open (import) | `.fla`, `.xfl` folder | `file.open`; `crates/engine/src/cmds_file.rs`, `crates/xfl/` |
| Import to stage | `.svg`, `.png`, `.jpg`, `.jpeg` | `file.import`; `crates/svg/`, `crates/engine/src/cmds_file.rs` |
| Import to stage | `.wav`, `.ogg`, `.mp3` | `file.import`; `crates/engine/src/cmds_sound.rs` |
| Import to library | WAV/Ogg/MP3, PNG/JPEG | `file.import_to_library` |
| Save | `.anicraft` JSON v3 | `file.save`, `file.save_as` |
| Export | `.png` | `file.export_png` |
| Export | PNG sequence into a folder | `file.export_png_sequence` |
| Export | `.svg` (one frame) | `file.export_svg` |
| Export | `.gif` | `file.export_gif` |
| Export | sprite sheet `.png` + `.json` map | `file.export_sprite_sheet` |
| Export | Lottie JSON | `file.export_lottie` |
| Export | self-contained `.html` canvas | `file.export_html` |
| Export | `.mp4`, `.webm` (code also `.m4v`, `.mov`) | `file.export_video` (external ffmpeg) |
| Export | `.wav` | `file.export_audio` |
| Publish | 9 formats from document settings | `file.publish` |

Video export bundles no codec: it pipes frames to ffmpeg chosen by the `ffmpeg` param,
`ANICRAFT_FFMPEG` or `PATH`. In the browser build it refuses; use GIF, PNG sequence or HTML
there.

## Plug-in policy

A plug-in may call the document namespaces: `draw`, `edit` (except clipboard and undo/redo),
`element`, `symbol`, `arrange`, `modify`, `library`, `text`, `scene`, `path`, `paint`,
`timeline`, `layer`, `align`, `doc`, `motion`, `sound`, `stroke`, `tween`, `actions`, `instance`,
`camera`, `bone`, `script`, `raw`, `frames`, `find`, `explorer`. It may read
`publish.settings_get`. It may not call `file.*`, any other `publish.*`, `prefs.*`, `plugin.*`,
`control.*`, or cut/copy/paste and undo/redo (`crates/engine/src/cmds_plugin.rs`
`plugin_may_call`). A run is atomic and one undo step.
