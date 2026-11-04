# CADCraft — round 2026-11-04 changes

Re-pinned: v0.16.0 (`4b4ec80`) -> v0.17.0 (`f389d6a`, installed `cadcraft 0.17.0 (f389d6a72e3fc160ea125b4f264d68f64cbe2aba)`).

## Corrected / re-measured

- Registry **449** commands per the regenerated checklist (previous skill: 447 derived); +2 ids (`-wblock`, `oops`); `-ATTDEF` is an alias of `attdef`.
- Command-line parity: `-ATTDEF`, `-WBLOCK`, `LEADER`, plus Thai text.

## Method

- 216 files changed; +2 command ids (`-wblock`, `oops`), none removed, and the regenerated checklist reports **449** registered commands (menu breadth 298/491) — the previous skill's 447 was derived from a stale checklist rather than measured, so it understated the registry.
- Command/tool id sets diffed between `v0.16.0` and `v0.17.0` with the extraction the published skill's `evidence.md` names; the counts above are the new sets.
- Every repo path cited in `SKILL.md` was re-resolved against the new checkout; paths that moved were re-cited.

## Unchanged

- Sections of the skill whose code path and counts did not move. They were path-verified at this tag and carried forward; no claim was silently re-dated.

## Known gap in this round

- The prose was not re-derived from scratch for every capability; this is a pin-and-verify refresh, not a new deep audit of every feature.
