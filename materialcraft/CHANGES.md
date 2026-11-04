# MaterialCraft — round 2026-11-04 (first audit)

New app, first public release: tag `v0.1.0`, commit `cedabf02030a3c662fda99b197ceb3ed12790ee7`,
installed `MaterialCraft 0.1.0 (cedabf0 2026-11-02)`.

## What this skill covers

- The `.mcraft` package (zip + `package.json`) and the `.mcmat` portable-material contract with
  TextureCraft (maps, exposed parameters, `source.mcraft`, format `craft-material` v1).
- The four surfaces over one registry: 68 command ids, 11 CLI subcommands, 21 MCP tools,
  11 JSON-lines methods, plus the token-authenticated control channel.
- The node/graph model: exposed inputs, dynamic parameters and function graphs, sub-graph
  instancing, presets, frames/comments/pins.
- An explicit not-implemented list taken from the repo's own `docs/gaps.md`, so no agent
  assigns this v0.1.0 app work it cannot do.

## What was not verified

- Runtime behaviour: no GUI was launched, nothing was built.
- The bundled asset library (materials/presets) was not enumerated.
- The `227 nodes` headline is the repo's own generated claim, labeled `claimed` in `evidence.md`.

## Drift found

- `docs/control-protocol.md` names `file.new` for a new package; the registry also has
  `file.newPackage`. Both exist — the doc is imprecise, not wrong.
