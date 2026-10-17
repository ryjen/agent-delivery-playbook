# ADR-0001: Classify governed tasks using T1–T4

- **Status:** accepted
- **Date:** 2026-10-17 (records established policy)
- **Deciders:** playbook maintainers
- **Supersedes:** none
- **Superseded by:** none

## Context

A task's consequences determine safeguards more than line count or agent confidence. A flat "safe/unsafe" label cannot express documentation-only, bounded code, high-risk workflow, and restricted production effects.

## Decision

Use the task-envelope risk identifiers **T1, T2, T3, T4**. Select the highest triggered classification and corresponding minimum controls from the [normative risk matrix](../task-risk-matrix.md) and [minimum controls policy](../policy/minimum-controls.md). The risk matrix's informational "Tier 0" describes read-only work but does **not** introduce an allowed `T0` envelope value. T4 remains human-led for restricted authority/effects.

## Alternatives considered

- Arbitrary numerical risk scores: falsely precise and hard to review across domains.
- Patch-size-only classification: misses one-line credential, CI, or approval-boundary changes.

## Consequences and verification

The task-envelope [schema](../../schemas/task-envelope.schema.json) restricts `classification.risk_tier` to these four identifiers. Structural validation cannot prove the selected tier is semantically justified; owner/risk review remains required. Changes to tier semantics are policy/compatibility changes requiring an explicit migration decision. The [glossary](../glossary.md#risk-tier-identifiers) is an index, not another source of controls.
