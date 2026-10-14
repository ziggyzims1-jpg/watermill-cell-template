# Four crew roles with separated powers

Status: accepted (owner decision, 2026-10-14, epic water-mill-fwm)

Work in a cell moves through four agents defined in `.claude/agents/`: **millstone** implements one bead into one PR; **bolter** reviews the diff against `CODING_STANDARDS.md`, `docs/adr/` and `CONTEXT.md` and is report-only; **sluice** reviews the PR against the bead and verifies independently, and is the only reviewer that pushes (it also acts on bolter's blocking findings); **tailrace** verifies in CI, squash-merges and closes the bead, one merge at a time. Separating them means the agent that wrote the change never approves it, and the one that merges is not the one that fixes. The agent files are managed by `watermill sync` from `water-mill/canon/`; edit them there, never in the cell.

## Consequences

- Millstone writes tests at seams, lists the seams in the PR body and handoff, and shows the new tests failing on the base (docs-only PRs say so instead). Sluice bounces a code PR without that evidence.
- Every agent writes a handoff before signing off, even when blocked, and says what failed. Per-bead notes go in `brain/handoffs/mill/<slug>.md` in the main checkout and are never part of the PR; the orchestrator commits them at the end of the session (`.claude/agents/millstone.md`; `brain/` is not on this template's fence, the agent files keep the note out of the PR).
- A denied tool call is a stop, not a puzzle: the agent reports BLOCKED and quotes the denial rather than retrying or re-wording.
- Sluice may file at most two `auto-mill` follow-up beads per parent (P3, clearly defined, never touching the fence, security code, schema or CI).

Sources: `.claude/agents/{millstone,bolter,sluice,tailrace}.md`; workshop `CLAUDE.md` "Every agent writes a handoff"; `water-mill/canon/workshop/CLAUDE.md` "Auto-mill: smells filed by the reviewer run through the crew next" and `.claude/agents/sluice.md` step 5d; water-mill `canon/` and epic water-mill-fwm; owner memory notes `mill-crew-in-repos.md`, `agent-handoff-rule.md`, `mill-permission-denial-escalation.md`.
