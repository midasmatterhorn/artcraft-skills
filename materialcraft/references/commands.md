# MaterialCraft — engine command index (v0.4.1)

Measured at tag `v0.4.1` (`65f7bfd3e5f40d695d03162285879f0f8079ff6c`) from the `cmd!` literals in the
37 modules aggregated by `crates/engine/src/commands.rs::command_specs()`: **119 unique ids**.
Labels are the registry's own. Params docs, menu paths and live `enabled` state come from
`materialcraft-cli commands` (or MCP `command_list`); run them there before scripting an id.

Menu-less ids are still runnable through `command.run`, the CLI `run` subcommand and MCP.

## `edit.*` (13)

| id | label |
|---|---|
| `edit.copy` | Copy selection |
| `edit.cut` | Cut selection |
| `edit.delete` | Delete selection |
| `edit.deleteRelink` | Delete and relink |
| `edit.duplicate` | Duplicate selection |
| `edit.duplicateWithoutLinks` | Duplicate selection without link |
| `edit.finish` | Finish edit gesture |
| `edit.paste` | Paste |
| `edit.pasteWithoutLinks` | Paste without link |
| `edit.redo` | Redo |
| `edit.selectAll` | Select all |
| `edit.selectNone` | Deselect |
| `edit.undo` | Undo |

## `explorer.*` (3)

| id | label |
|---|---|
| `explorer.copy` | Copy Explorer item |
| `explorer.move` | Move Explorer item |
| `explorer.paste` | Paste Explorer item |

## `file.*` (13)

| id | label |
|---|---|
| `file.export` | Export outputs... |
| `file.exportMaterial` | Export material... |
| `file.importBitmap` | Import bitmap... |
| `file.importVector` | Import vector graphics... |
| `file.new` | Graph... |
| `file.newAtomicSample` | Atomic sample |
| `file.newPackage` | Empty package |
| `file.open` | Open... |
| `file.reload` | Reload package |
| `file.save` | Save |
| `file.saveAs` | Save as... |
| `file.saveCopyAs` | Save a copy as... |
| `file.sendToTextureCraft` | Send to TextureCraft |

## `folder.*` (5)

| id | label |
|---|---|
| `folder.attributes` | Folder attributes |
| `folder.create` | New folder |
| `folder.properties` | Inspect folder properties |
| `folder.remove` | Remove folder |
| `folder.rename` | Rename folder |

## `graph.*` (65)

| id | label |
|---|---|
| `graph.align` | Align nodes |
| `graph.annotation.select` | Select annotation |
| `graph.attributes` | Graph attributes |
| `graph.comment.add` | Add Comment |
| `graph.comment.delete` | Delete comment |
| `graph.comment.edit` | Edit comment |
| `graph.connect` | Connect |
| `graph.context` | Graph evaluation context |
| `graph.cook` | Compute graph |
| `graph.createFromSelection` | Create graph from selection |
| `graph.delete` | Delete graph |
| `graph.disconnect` | Disconnect |
| `graph.duplicate` | Duplicate graph |
| `graph.exposed.add` | Expose parameter |
| `graph.exposed.delete` | Delete input |
| `graph.exposed.prepare` | Prepare graph input |
| `graph.exposed.set` | Set input value |
| `graph.format` | Output format |
| `graph.frame.add` | Add Frame |
| `graph.frame.delete` | Delete frame |
| `graph.frame.edit` | Edit frame |
| `graph.frame.move` | Move frame and contents |
| `graph.function.edit` | Edit function node |
| `graph.function.node.info` | Copy function node info |
| `graph.function.set` | Edit Function Graph |
| `graph.function.variables` | List function variables |
| `graph.input.bind` | Set input preview image |
| `graph.input.unbind` | Clear input preview image |
| `graph.instance.add` | Add graph instance |
| `graph.instance.reference` | Open graph reference |
| `graph.node.add` | Add node |
| `graph.node.base` | Set base parameters |
| `graph.node.bind` | Bind parameter to input |
| `graph.node.disable` | Disable selection |
| `graph.node.edit` | Edit node graph |
| `graph.node.function` | Set parameter function |
| `graph.node.function.edit` | Edit parameter function |
| `graph.node.info` | Copy node info |
| `graph.node.move` | Move nodes |
| `graph.node.param` | Set parameter |
| `graph.node.parameterInfo` | Inspect parameter |
| `graph.node.rename` | Rename node |
| `graph.node.reset` | Reset parameters |
| `graph.node.value_input` | Edit value input |
| `graph.open` | Open graph |
| `graph.pattern.edit` | Edit FX-Map node |
| `graph.pattern.set` | Edit FX-Map graph |
| `graph.pin.add` | Add Navigation pin |
| `graph.pin.delete` | Delete pin |
| `graph.pin.edit` | Edit Navigation pin |
| `graph.preset.apply` | Apply preset |
| `graph.preset.delete` | Delete preset |
| `graph.preset.save` | Save preset |
| `graph.properties` | Inspect graph properties |
| `graph.rename` | Rename graph |
| `graph.resource.add` | Add resource to graph |
| `graph.seed` | Random seed |
| `graph.select` | Select nodes |
| `graph.selectDownstream` | Select downstream nodes |
| `graph.selectUpstream` | Select upstream nodes |
| `graph.size` | Graph size |
| `graph.templates` | Graph templates |
| `graph.wire.delete` | Delete links |
| `graph.wire.insertDot` | Insert reroute dot |
| `graph.wire.swap` | Swap links |

## `library.*` (6)

| id | label |
|---|---|
| `library.add` | Add library entry |
| `library.function.add` | Add library function |
| `library.functions` | List library functions |
| `library.list` | Library |
| `library.reload` | Reload library |
| `library.tree` | Library categories |

## `package.*` (3)

| id | label |
|---|---|
| `package.activate` | Open package |
| `package.close` | Close package |
| `package.closeAll` | Close all packages |

## `session.*` (3)

| id | label |
|---|---|
| `session.environment` | Evaluation environment |
| `session.history` | History preferences |
| `session.inspect` | Inspect |

## `view.*` (8)

| id | label |
|---|---|
| `view.2d` | View output in 2D view |
| `view.3d` | 3D view settings |
| `view.3d.assign` | View output in 3D view |
| `view.3d.clear` | Clear material assignments |
| `view.3d.loadMesh` | Load mesh... |
| `view.3d.outputs` | View outputs in 3D view |
| `view.3d.reset` | Reset scene |
| `view.previewSize` | Preview size |

