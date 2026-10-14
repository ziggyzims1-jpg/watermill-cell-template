# What a Claude Code cloud session can and cannot do for the mill

Status: accepted (learned 2026-10-13 from the cloud-environments docs and two real runs; water-mill-mb6)

The crew can run in a Claude Code cloud session as well as on the owner's laptop, and the cloud environment constrains it in ways nothing in the code shows. Each crew file therefore carries a "Cloud mode" section that applies only when `CLAUDE_CODE_REMOTE` is exactly `true` and overrides its laptop steps: GitHub is reached through the REST API only (`gh pr ...` uses GraphQL, which returns 403); the git proxy accepts pushes of a branch and nothing else, so the session pushes only its own `claude/...` branch, which is the PR head for every bead; and the container is thrown away, so handoffs and run records are committed on that branch instead of left untracked.

## Consequences

- Beads never travel through Dolt from a cloud session: every `bd` command runs with `BD_DOLT_AUTO_PUSH=false`, `bd dolt push` and any `refs/dolt/*` push are forbidden, and bead changes are `.beads/issues.jsonl` commits on the session branch, never part of a feature PR (ADR-0002).
- The crew files expect "the repo's beads-sync workflow" to carry those commits to main. This template ships no such workflow (`.github/workflows/` holds only `verify.yml`), and the workflow directory is fenced, so a cell worked from the cloud needs one added by a human.
- The Agent tool's `isolation: "remote"` falls back to a local worktree on the laptop, so a real cloud run is started by the owner from claude.ai/code, and an agent checks `CLAUDE_CODE_REMOTE` before acting in cloud mode.

Sources: `.claude/agents/{millstone,bolter,sluice,tailrace}.md` "Cloud mode"; owner memory note `claude-cloud-sessions-constraints.md`; cheme-solver `brain/runbooks/cloud-mill.md` (the spec the crew files cite).
