# ADR-0007: Separate generation, verification, approval, merge and release

- **Status:** accepted
- **Date:** 2026-10-17 (records established trust model)
- **Deciders:** playbook maintainers
- **Supersedes:** none
- **Superseded by:** none

## Context

A single actor that edits code, reports its own tests, approves risk, and deploys can bypass every purported SDLC gate. Artifact generation and protected evidence are different responsibilities.

## Decision

Separate the principal/runtime that **generates** changes from accountable **verification**, **review/approval**, **merge admission**, and **release administration**. Apply the [trust model](../trust-model.md), [identity/delegation rules](../identity-delegation-and-capability-grants.md), and [evidence standard](../delivery-evidence-standard.md) according to risk. A model reviewer can advise but cannot confer human or provider approval merely by reporting `NO_FINDINGS`.

## Alternatives considered

- Agent self-approval: exposes a direct policy bypass.
- One high-privilege token for code and deployment: increases incident blast radius and destroys separation of duties.

## Consequences and verification

Identity and scope must be enforced by the owning control planes; a green workflow or ADR alone does not activate branch protection, authorizations or release gates. Repository GitHub admission remains pending [issue #60](https://github.com/ryjen/agent-delivery-playbook/issues/60). The solo-maintainer case may require explicitly documented bounded fallback review; never claim independent human review from a local model result.
