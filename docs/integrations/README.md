# Integrations: gated by default, ungated by proof

The full policy lives in `water-mill/docs/INTEGRATIONS.md`. The short version
every cell carries:

**Gated (the default).** Every external integration is out of the mill's
reach until proven:

1. `services/integrations/` is on the fence in `watermill.yaml`, so no mill
   agent can touch a provider module in an unsupervised run.
2. Beads that require a live provider are created **deferred** (`bd create
   --defer`), so they never appear in `bd ready` and the mill cannot claim
   them. Skeleton/stub beads (mock data only, no credentials, no network) may
   stay open — they build the seam, not the connection.

**Ungating a provider** requires all three, by a human, in one PR:

1. **Wire it**: accounts, credentials, OAuth apps, ToS — the parts an agent
   cannot do and must not hold.
2. **Prove it live**: a real round-trip against the provider from the machine
   that will run it, recorded (the request made, the response received, the
   date). "It should work" is not proof; the Actual Budget and Libby lessons
   both came from builds that skipped this step.
3. **File the wiring record**: copy `TEMPLATE.md` to
   `docs/integrations/<provider>.md` and fill in every section. The record is
   what makes the ungating safe — it is how a mill agent, later, knows how
   the integration actually works rather than how it plausibly might.

The same PR narrows the fence and un-defers the provider's beads
(`bd update <id> --status open`). The fence format has no negation patterns,
so narrowing means **replacing** the `services/integrations/` entry in
`watermill.yaml` with one entry per still-gated module (e.g.
`services/integrations/quickbooks*`). From that point the gated list is
enumerated, which adds one duty: a **new** provider's module must be added
to the fence in the same change that creates it, or it is born ungated.
Providers not named in a wiring record stay fenced.

**Re-gating.** If the provider changes under the integration — a schema
error, a moved endpoint, an auth flow that stops working — the provider goes
back on the fence and its beads back to deferred until a human re-proves it
and updates the record. A wiring record describes the provider as it was on
its `verified` date, not forever.
