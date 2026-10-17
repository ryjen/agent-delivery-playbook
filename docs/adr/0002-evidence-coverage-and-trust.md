# ADR-0002: Keep evidence coverage separate from trust and authority

- **Status:** accepted
- **Date:** 2026-10-17 (records established policy)
- **Deciders:** playbook maintainers
- **Supersedes:** none
- **Superseded by:** none

## Context

A green test, captured log, signed attestation, or independent review can establish different facts. Calling all of them "verified" collapses source trust, exact subject binding, independence and decision authority.

## Decision

Use **E1–E4** for *coverage*: static, test, operational, and independent verification. Apply risk-specific composite requirements from the [Delivery Evidence Standard](../delivery-evidence-standard.md). Track provenance/producer, immutable subject, execution environment, integrity and independence **separately**. `E0` describes absence of evidence, not a schema-allowed required level. An approval record evidences approval but does not independently establish code correctness.

## Alternatives considered

- One score for evidence "strength": falsely orders attestation versus independent reproduction.
- Accept model-reported test success as sufficient proof: confuses a claim with attributable evidence.

## Consequences and verification

Reviewers must assess both the property covered and the source/binding. Required independence cannot be fulfilled by self-report from the producer. The [envelope schema](../../schemas/task-envelope.schema.json) restricts required evidence levels; conformance checking is structural and cannot mint verification authority.
