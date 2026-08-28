# Wiring record: <Provider>

<!-- Copy this file to docs/integrations/<provider>.md when ungating.
     Every section is required. "N/A" is an answer; blank is not. -->

**Status:** gated | ungated
**Verified live on:** YYYY-MM-DD, by <who>, from <which machine/host>
**Module:** `services/integrations/<provider>.py`

## What it does

One paragraph: what this integration reads or writes, and for which feature.

## Accounts and credentials

- Account: who owns it, where it was created, what plan/tier.
- Credentials: WHERE they live (env var names, config keys) — never values.
  Every secret key must be listed in the app's sensitive-keys set and
  redacted from any config read endpoint.
- OAuth: app name, redirect URI, scopes requested, where the refresh token
  is stored.

## Config keys

| Key | Meaning | Secret? |
|-----|---------|---------|

## Endpoints used

| Method + path | Purpose | Notes |
|---------------|---------|-------|

## The proof

What was actually done to verify it live: the call made, the response
received (shape, not secrets), and what in the app confirmed the round trip.
This is the section that distinguishes "wired" from "written".

## Failure modes and degradation

- What happens when the provider is down (weather) vs. changed (schema)?
  Distinguish them: an outage logs quietly, a shape change is an error.
- The destructive operations, if any, and what guards them. A sync that can
  mark records absent must only reconcile collections the payload actually
  contained.
- Rate limits and polling interval, and why that interval.

## What is still mocked

Anything the module stubs even after ungating, so nobody mistakes a fixture
for the provider.

## Re-verification triggers

The changes that must send this provider back through the proof step (e.g.
provider API version bump, auth flow change, new scope needed).
