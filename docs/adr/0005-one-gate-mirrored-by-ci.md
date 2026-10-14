# One gate, `make verify`, run unchanged by CI

Status: accepted (carried from zimmy-life-tracker into the template)

`make verify` (guard, build, ruff, ESLint at `--max-warnings=0`, Vitest, pytest) is the only merge gate, and `.github/workflows/` runs `make install` then `make verify` and nothing else. A check that passes locally therefore cannot fail in CI for a reason spelled out in a YAML file, and the mill can trust one command. No target may swallow a failure: no `-` prefixes, no `|| true`, no `continue-on-error`; `make typecheck` exists only to exit non-zero because no type checker is configured, so it can never turn a result green. The `guard` step refuses to run in a production-looking environment and proves the app honours `DATA_DIR`.

## Consequences

- The gate, `ruff.toml`, the workflow files and the Vite/ESLint configs are on the fence: an agent that can edit them can make itself pass. Changing what the gate means is a human change.
- A new check goes into `make verify`, never into a separate CI step.

Sources: `Makefile` and `.github/workflows/` comments; `CLAUDE.md` "Verify with `make verify`"; `watermill.yaml` fence comment.
