# Cell context

The shared vocabulary of a Water Mill cell: a client-facing app stamped from `watermill-cell-template` and worked on by the mill crew. The first section is the same in every cell. The second is a placeholder: **on stamping, fill in the terms of this cell's own domain** and keep the first section as is. Format: `water-mill/canon/common/.claude/skills/domain-modeling/CONTEXT-FORMAT.md`.

## Language (every cell)

### The factory

**Cell**:
One client project stamped from `watermill-cell-template`, named `<project>-cell-<cell#>`, with its own repo, contract, gate and fence.
_Avoid_: Project (ambiguous with a Water Mill registered project), instance, tenant

**Water Mill**:
The orchestrator that claims beads from a cell's queue, hands them to the crew, verifies what reached the repository and records what happened.
_Avoid_: The mill (acceptable shorthand in prose, not in code or commit messages), pipeline, CI

**Contract**:
The cell's `watermill.yaml`: the gate, queue commands, review commands, fence, environment checks and caps that the factory reads before a run. An in-repo contract always wins over a vendored one.
_Avoid_: Config (that is `config.py`), settings

**Gate**:
`make verify`: guard, build, ruff, ESLint at `--max-warnings=0`, Vitest and pytest. CI runs exactly this command and nothing else, so the two cannot diverge.
_Avoid_: CI checks, test suite (the suite is only part of it)

**Fence**:
The list of paths in the contract (`fence.paths`) that a mill agent must not modify in an unsupervised run, because editing them could change what "passing" means or what is allowed. Entries are prefixes; the format has no negation.
_Avoid_: Protected files, ignore list, blocklist

**Caps**:
The per-night limits in the contract (`max_tasks`, `max_hours`, `task_timeout_minutes`). Night-one values stay until a night with zero reverts and an accurate report.
_Avoid_: Quotas, budget

**Bead**:
One task in the cell's `bd` queue; the unit of work the mill claims. Bead data lives in git as `.beads/issues.jsonl`.
_Avoid_: Ticket, issue, story

**Deferred bead**:
A bead created with `bd create --defer` so it never appears in `bd ready`; used for work that needs a live provider and so cannot be claimed by the mill.
_Avoid_: Blocked bead, backlog item

**Crew**:
The four agents `millstone` (implements one bead into one PR), `bolter` (standards review, report-only), `sluice` (spec review and independent verification, the only reviewer that pushes) and `tailrace` (verifies in CI, merges, closes the bead).
_Avoid_: Bots, workers, the team

**Handoff**:
The note an agent writes before signing off, saying where things stand and what failed. Per-bead notes live in `brain/handoffs/mill/<slug>.md`.
_Avoid_: Summary, report, changelog

### Integrations

**Integration**:
Any module that talks to an external provider (accounting, calendar, payments, e-mail and the like). Integration modules live in `services/integrations/`.
_Avoid_: Connector, plugin, adapter

**Gated**:
The default state of every integration: its module is on the fence and every bead that needs it is deferred, so no unsupervised run can touch it.
_Avoid_: Disabled, off, stubbed (a stub is the mock seam, not the gate)

**Ungating**:
Removing one provider from the fence, by a human, in a single PR that also files the wiring record and un-defers the provider's beads. See ADR-0001.
_Avoid_: Enabling, unlocking, turning on

**Wiring record**:
`docs/integrations/<provider>.md`, copied from `docs/integrations/TEMPLATE.md`: how the integration actually works, with a `verified` date from a live round-trip. It describes the provider as it was on that date, not forever.
_Avoid_: Integration docs, setup notes

**Re-gating**:
Putting a provider back on the fence and its beads back to deferred when the provider changes under the integration, until a human re-proves it.
_Avoid_: Disabling, rollback

**Mock data**:
Fixed, credential-free data a skeleton or stub bead returns in place of a provider's response, so the seam and the UI can be built without a connection. Mock data never leaves the repo as a stand-in for proof.
_Avoid_: Fixtures (those belong to tests), seed data (that is database content)

### Data and time

**Schema**:
The `SCHEMA` DDL in `db.py`, which may reference only what it itself creates.
_Avoid_: Models, tables (the schema is the whole DDL, not one table)

**Migration**:
One entry in the append-only `MIGRATIONS` list in `db.py`. Entries are added at the end and never edited or reordered.
_Avoid_: Schema change, upgrade script

**Today**:
The cell's single definition of the current date: `services/clock.py` on the backend, `utils.localDate` on the frontend. Local date, never UTC.
_Avoid_: now, current date

**Job run**:
A row in `job_runs` recording one execution and outcome of a scheduled job. A job whose success is invisible needs a heartbeat that alerts when it goes stale.
_Avoid_: Cron log, task log

**Data dir**:
The directory holding the SQLite database, set by `DATA_DIR`. The gate and the tests depend on that override working, so a test never writes beside the live database.
_Avoid_: Storage, db folder

**Design token**:
A named color, spacing or type value defined in `frontend/src/index.css`. Components read tokens and never hard-code colors.
_Avoid_: Theme variable, style constant

## Language (this cell)

> Fill in on stamping. Keep only terms specific to this client's domain; general programming concepts do not belong. Pick one word per concept and list the rejected synonyms under `_Avoid_`. Delete this note when the first term is added.

**{Term}**:
{One or two sentences: what it is, not what it does.}
_Avoid_: {synonyms}
