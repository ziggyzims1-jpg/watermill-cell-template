# Architecture decision records

Decisions that are hard to reverse, surprising without context, and the result of a real trade-off. Numbered `NNNN-slug.md`; format in `water-mill/canon/common/.claude/skills/domain-modeling/ADR-FORMAT.md`. The bolter reviewer treats an accepted ADR as a documented rule: a diff that breaks one is a blocking finding.

**Every cell inherits ADR-0001 to ADR-0006.** They record decisions made for the whole factory before this cell existed. If this cell must deviate from one, write a new ADR that supersedes it and say why; do not edit the inherited text. Add the cell's own decisions from ADR-0007 on.

| ADR | Decision |
|---|---|
| [0001](0001-integrations-gated-by-default.md) | Integrations are fenced and deferred until a human proves them and files a wiring record |
| [0002](0002-beads-live-in-git.md) | Beads live in git and are pushed before a session ends |
| [0003](0003-the-mill-crew-and-its-roles.md) | Four crew roles with separated powers |
| [0004](0004-never-git-stash.md) | Never `git stash` in a mill worktree |
| [0005](0005-one-gate-mirrored-by-ci.md) | One gate, `make verify`, run unchanged by CI |
| [0006](0006-schema-and-migrations-discipline.md) | SCHEMA plus append-only MIGRATIONS |
