# Cell context

The shared vocabulary of a Water Mill cell: a client-facing app stamped from `watermill-cell-template` and worked on by the mill crew. The first section is the same in every cell. The second is a placeholder: **on stamping, fill in the terms of this cell's own domain** and keep the first section as is. Format: `water-mill/canon/common/.claude/skills/domain-modeling/CONTEXT-FORMAT.md`.

## Language (every cell)

### The factory

**Cell**:
One client project stamped from `watermill-cell-template`, named `<project>-cell-<cell#>`, with its own repo, contract, gate and fence.
_Avoid_: Project (ambiguous with a Water Mill registered project), instance, tenant

**Water Mill**:
The orchestrator that claims beads from a cell's queue, hands them to the crew, verifies what reached the repository and records what happened.
_Avoid_: Pipeline, CI

**Contract**:
The cell's `watermill.yaml`: the gate, queue commands, review commands, fence, environment checks and caps that the factory reads before a run.
_Avoid_: Config (that is `config.py`), settings

**Gate**:
`make verify`, the one command whose success means a change may merge; CI runs the same command (ADR-0005).
_Avoid_: CI checks, test suite (the suite is only part of it)

**Fence**:
The list of paths in the contract (`fence.paths`) that a mill agent must not modify in an unsupervised run (ADR-0007).
_Avoid_: Protected files, ignore list, blocklist

**Caps**:
The per-night limits in the contract (`caps`) on how much work one night may take on.
_Avoid_: Quotas, budget

**Bead**:
One task in the cell's `bd` queue; the unit of work the mill claims.
_Avoid_: Ticket, issue, story

**Deferred bead**:
A bead created with `bd create --defer` so it never appears in `bd ready`; used for work that needs a live provider and so cannot be claimed by the mill.
_Avoid_: Blocked bead, backlog item

**Crew**:
The four agents that work a bead: `millstone` (implementer), `bolter` (standards reviewer), `sluice` (spec reviewer) and `tailrace` (lander). Their powers: ADR-0003.
_Avoid_: Bots, workers, the team

**Handoff**:
The note an agent writes before signing off, saying where things stand and what failed.
_Avoid_: Summary, report, changelog

### Integrations

**Integration**:
Any module that talks to an external provider (accounting, calendar, payments, e-mail and the like).
_Avoid_: Connector, plugin, adapter

**Gated**:
The default state of every integration: fenced, with every bead that needs it deferred (ADR-0001).
_Avoid_: Disabled, off, stubbed (a stub is the mock seam, not the gate)

**Ungating**:
Taking one provider off the fence after a human has wired it and proved it live (ADR-0001).
_Avoid_: Enabling, unlocking, turning on

**Wiring record**:
The document recording how one provider's integration actually works, as proved by a live round-trip on a stated date.
_Avoid_: Integration docs, setup notes

**Re-gating**:
Returning an ungated provider to the gated state because the provider changed under the integration.
_Avoid_: Disabling, rollback

**Mock data**:
Fixed, credential-free data returned in place of a provider's response, so the seam and the UI can be built without a connection. The integrations policy also calls it "mock fixtures".
_Avoid_: Fake data, seed data (that is database content)

### Data and time

**Schema**:
The DDL that creates a fresh database (`SCHEMA` in `db.py`).
_Avoid_: Models, tables (the schema is the whole DDL, not one table)

**Migration**:
One step that brings an existing database up to the current schema (an entry in `MIGRATIONS`, ADR-0006).
_Avoid_: Schema change, upgrade script

**Today**:
The current local date, as the cell's single definition gives it (`services/clock.py`, `utils.localDate`).
_Avoid_: now, current date

**Job run**:
One recorded execution of a scheduled job and its outcome (a row in `job_runs`).
_Avoid_: Cron log, task log

**Data dir**:
The directory holding the database and the secret key, set by `DATA_DIR`.
_Avoid_: Storage, db folder

**Design token**:
A named color, font or easing value that components use instead of a literal (defined in `frontend/src/index.css`).
_Avoid_: Theme variable, style constant

## Language (this cell)

> Fill in on stamping. Keep only terms specific to this client's domain; general programming concepts do not belong. Pick one word per concept and list the rejected synonyms under `_Avoid_`. Delete this note when the first term is added.

**{Term}**:
{One or two sentences: what it is, not what it does.}
_Avoid_: {synonyms}
