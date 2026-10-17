# ADR-0006: Preserve strict task-envelope structure and explicit migrations

- **Status:** accepted
- **Date:** 2026-10-17 (records established behavior)
- **Deciders:** playbook maintainers
- **Supersedes:** none
- **Superseded by:** none

## Context

Silent acceptance of unrecognized fields can hide malformed controls or encourage consumers to treat undeclared fields as permissions. But tightening the schema can break downstream envelopes even when the repository only labels it a cleanup.

## Decision

Keep the authoritative [task-envelope JSON Schema](../../schemas/task-envelope.schema.json) explicit, including `additionalProperties: false` on known structures and constrained enums. Treat additions/removals of required fields, stricter validation, or authority-meaning changes as compatibility-sensitive under [pre-1.0 versioning policy](../versioning-and-compatibility.md). Never add an in-envelope version discriminator without a reviewed schema change; pin the whole playbook release externally when needed.

## Alternatives considered

- Silently ignore unknown fields: creates false confidence that undeclared intent and identity hints are enforced.
- Unversioned silent schema changes: makes reproducible adoption and rollback difficult.

## Consequences and verification

Update fixtures, validators, examples and migration notes in the same change. Validation establishes shape, not the truth of claims. The current schema `$id` points to a mutable branch URL; a tagged commit/artifact digest, not that URL alone, identifies a reproducible version. No initial tagged release is claimed.
