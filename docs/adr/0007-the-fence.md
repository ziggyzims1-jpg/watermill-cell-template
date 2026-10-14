# The fence: paths an unsupervised run may not modify, checked against the diff

Status: accepted (Water Mill safety model, carried into every cell's contract)

`fence.paths` in `watermill.yaml` lists the paths a mill task may never modify. Water Mill names them in the agent's prompt **and** checks them against the diff after the agent exits (staged, unstaged and untracked changes and the commit); a task that touches a fenced path has its work discarded whatever else it did. We chose a checked list over an instruction because "stating a fence in a prompt is a request; checking it against the diff is evidence", and because an agent that can edit the gate, or what decides what the gate means, can make itself pass. This template fences the gate and its configuration (`Makefile`, `ruff.toml`, `.github/workflows/`, `frontend/vite.config.js`, `frontend/eslint.config.js`), the schema (`db.py`), the work graph and doctrine (`.beads/`, `CLAUDE.md`), client branding (`assets/branding/`) and the gated integrations (`services/integrations/`, ADR-0001).

## Consequences

- Patterns are `fnmatch` globs against repository-relative paths; an entry ending in `/` covers everything beneath it. The format has no negation, which is why ungating a provider replaces the directory entry with per-module entries (ADR-0001).
- A bead may direct an edit to a fenced path; without that direction, the reviewer treats any fenced-path hunk as a violation. A change to what the gate means is a human change.
- A rule that can be expressed as a fence entry belongs in the fence, not in the contract's `notes`, which are advice and never checked.

Sources: `watermill.yaml` fence comments; `water-mill/docs/SAFETY.md` "2. The fence"; `water-mill/docs/CONTRACT.md` "`fence.paths`" and "`notes`"; `.claude/agents/sluice.md` step 2.
