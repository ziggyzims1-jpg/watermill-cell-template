# Beads live in git and are pushed before a session ends

Status: accepted (owner's rule, 2026-09-03)

The queue is `bd`, whose live store is a local database; `.beads/issues.jsonl` is the copy that travels. Any session or agent that creates, updates, closes or defers a bead commits and pushes `.beads/issues.jsonl` (a `chore(beads): ...` commit is fine) before signing off. On 2026-09-03 three days of bead activity sat uncommitted on one machine and the owner could not see it elsewhere; bd's git hooks re-export on commit, but a write with no later commit never leaves the machine.

## Consequences

- In a Claude Code cloud session the git proxy rejects pushes of anything but a branch, so `bd dolt push` and any `refs/dolt/*` push fail. Beads travel as `.beads/issues.jsonl` commits on the session branch, and are never part of a feature PR (an `issues.jsonl` in a PR conflicts on line order alone).
- After pulling, compare the JSONL against the database and `bd import` if they differ; the post-merge hook has not always imported.
- `.beads/` is on the fence: an unsupervised agent does not edit the work graph.

Sources: workshop `CLAUDE.md` "Beads live in git"; owner memory notes `beads-push-to-git.md`, `beads-import-after-pull.md`, `claude-cloud-sessions-constraints.md`; this template's `CLAUDE.md` "Beads Issue Tracker" and `watermill.yaml` fence.
