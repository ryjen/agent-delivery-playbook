# ADR-0005: Keep normative sources authoritative over templates and examples

- **Status:** accepted
- **Date:** 2026-10-17 (records established architecture)
- **Deciders:** playbook maintainers
- **Supersedes:** none
- **Superseded by:** none

## Context

A copied template, quickstart, validator, or generated explanation can disagree with the intended controls. Without concern-specific sources of truth, changes to examples could silently redefine governance.

## Decision

Use the concern-specific authority map in [Canonical Architecture](../architecture.md): normative task-envelope meaning, risk, evidence and trust policies; machine-checkable schema for envelope *structure*; templates and examples as derived projections; guidance as explanation. The [governance lifecycle](../governance-lifecycle.md) governs changes and migration. The [glossary](../glossary.md) links terms but does not override normative definitions.

## Alternatives considered

- Make README or examples universally authoritative: convenient but weakens drift control.
- Treat a successful validator run as policy or admission approval: collapses semantic judgment and enforcement.

## Consequences and verification

Disagreement should fail closed for consequential work until reconciled. Updating normative semantics means updating relevant projections, examples, checks and migration notes together. A recorded ADR cannot itself enable runtime/CI/provider controls.
