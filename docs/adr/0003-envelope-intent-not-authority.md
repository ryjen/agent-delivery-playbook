# ADR-0003: Separate task-envelope intent from runtime authorization

- **Status:** accepted
- **Date:** 2026-10-17 (records established policy)
- **Deciders:** playbook maintainers
- **Supersedes:** none
- **Superseded by:** none

## Context

An untrusted producer may write task metadata, prompts, and PR descriptions. If claiming `owner` or `allowed tools` in an envelope were sufficient to gain permissions, editing the envelope would become privilege escalation.

## Decision

The [task envelope](../agent-task-envelope.md) is a stable statement of **task intent and governance constraints**; it is *not* a credential or authenticated identity. Effective authority requires a separately issued, bounded [capability grant](../identity-delegation-and-capability-grants.md), constrained by runtime, task, resource/ref, effect, issuer, expiry and revocation. Retry, resume, and nested delegation do not expand authority.

## Alternatives considered

- Put runtime credentials/identity assertions into the envelope: confuses self-authored declarations with verified identity.
- Treat tool visibility as authorization: breaks least privilege and protected merge/release boundaries.

## Consequences and verification

Envelope validation establishes shape, not live enforcement. Adopters must verify permissions at the actual execution boundary. A future grant-reference field would require reviewed schema/compatibility changes and must remain non-authoritative on its own. See the [trust model](../trust-model.md).
