# ADR-0004: Start with manual review, then promote objective checks to pinned CI

- **Status:** accepted
- **Date:** 2026-10-17 (records established approach)
- **Deciders:** playbook maintainers
- **Supersedes:** none
- **Superseded by:** none

## Context

Purely model-judged gates are nondeterministic and vulnerable to self-report; mandatory heavyweight runtime policy engines would prevent small repositories adopting the playbook. We also need a reproducible toolchain.

## Decision

Begin with bounded human review and minimal task/evidence artifacts. Encode repeatable **objective** predicates in local validators and [flake-owned CI](../../flake.nix) as they stabilize. Keep semantic risk/approval interpretation accountable to policy owners. The original lightweight envelope parser favors Python standard-library checks for portable fast feedback; the standards/schema parity checker also uses pinned **PyYAML and JSON Schema dependencies from the Nix flake**. Do **not** claim the whole validation suite is dependency-free.

## Alternatives considered

- Full policy engine at initial adoption: broadens trust and operational complexity without proven need.
- AI-only assurance reports: cannot establish reproducible test execution or protected admission.

## Consequences and verification

Local and CI tests can provide objective evidence, not automatic runtime authorization or provider admission. The live GitHub branch ruleset remains [unqualified (#60)](https://github.com/ryjen/agent-delivery-playbook/issues/60) until an administrator enables required checks and negative-admission testing proves enforcement. No CI change should silently weaken existing checks.
