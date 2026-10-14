# Integrations are fenced and deferred until a human proves them and files a wiring record

Status: accepted (owner's policy, 2026-08-27)

Every external integration in a cell is **gated by default**: `services/integrations/` is a `fence.paths` entry in `watermill.yaml`, and beads that need a live provider are created `--defer` so `bd ready` (what the mill reads) never shows them. A provider is ungated only after a human wires it, proves it live from the machine that will run it, and files `docs/integrations/<provider>.md`; the same PR narrows the fence and un-defers its beads. We chose this because builds that skipped live proof (the Actual Budget and Libby integrations in zimmy-life-tracker) looked complete and did not work, and an unsupervised agent cannot hold credentials or accept a provider's terms.

## Consequences

- The fence format has no negation patterns, so ungating replaces the directory entry with one entry per still-gated module (e.g. `services/integrations/quickbooks*`). From then on a **new** provider module must be added to the fence in the change that creates it, or it is born ungated.
- Skeleton and stub beads (mock data, no credentials, no network) may stay open: they build the seam, not the connection.
- Any schema, endpoint or auth change in the provider re-gates it until a human re-proves it.

Sources: `docs/integrations/README.md` (the procedure) and `docs/integrations/TEMPLATE.md` (the record); `CLAUDE.md` "Integrations are gated by default"; `watermill.yaml` fence comments; owner memory note `integration-ungating-policy.md`; canonical policy `water-mill/docs/policies/INTEGRATIONS.md`.
