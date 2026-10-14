# Never `git stash` in a mill worktree

Status: accepted (owner rule after incidents on 2026-08-30)

Worktrees of one repository share a single `.git`, so the stash stack is global across every concurrent worktree and agent. Twice on 2026-08-30 a `git stash` / `git stash pop` used to prove a test fails without a fix interleaved with another agent's stash: the pop pulled in unrelated changes and silently reverted the fix, with no error. To prove red-before-green, snapshot with a patch file (`git diff > ../<slug>.patch`), `git checkout -- <files>`, run the test, then `git apply` the patch back.

## Consequences

- The git guardrail hook (`.claude/hooks/block-dangerous-git.py`, wired in `.claude/settings.json` and delivered by `watermill sync`) blocks every form of `git stash`, including `git -C <dir> stash`, along with `reset --hard`, `clean -f`, `branch -D`, `checkout .`, `restore .` and force pushes. Plain `git push` stays allowed.
- The same class of hazard applies to a shared `node_modules`: never run `npm ci` or `npm install` in a directory other worktrees symlink to. Use a worktree-local install.

Sources: owner memory notes `watermill-git-stash-hazard.md`, `watermill-shared-node-modules-hazard.md`; `.claude/hooks/block-dangerous-git.py`; epic water-mill-fwm (guardrail hook, child .3).
