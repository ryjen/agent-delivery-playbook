# Architecture Decision Records (ADRs)

ADRs preserve consequential **decisions already made or under review** without duplicating the normative policies, schemas, or provider settings that implement them. See [canonical architecture](../architecture.md), [governance lifecycle](../governance-lifecycle.md), and [glossary](../glossary.md).

## Status and maintenance

- **proposed** — candidate rationale; no adopted change is implied.
- **accepted** — adopted repository design decision; normative requirements still live in their referenced source documents.
- **superseded** — replaced by a later ADR; retain this record and link both directions.
- **deprecated** — no longer recommended, pending replacement or explicit migration; do not silently delete historical rationale.

These ADR statuses describe *decisions*, not provider rule activation or the maturity of a release. "Accepted" does not prove CI enforcement, operational adoption, or external effect authorization.

Use sequential `NNNN-short-title.md` filenames. New ADRs should state problem, decision, alternatives, consequences, **source-of-truth links**, and status. Keep them short: link to normative details rather than copying their entire control matrices. Record "Supersedes" / "Superseded by" links in both old and new ADRs when replacing a decision. When policy/schema meaning changes, update the actual normative source and compatibility/migration notes in the **same** PR; an ADR alone does not change enforcement.

See [ADR template](TEMPLATE.md). Contributors should add/update an ADR for a security or compatibility decision with meaningful trade-offs, reversibility concerns, or likely future disputes. Routine implementation, typos, and narrow fixes do not automatically need one.

## Decision index

| ID | Topic | Status | Governing source |
| --- | --- | --- | --- |
| [0001](0001-task-risk-tiers.md) | T1–T4 task risk tiers | accepted | Risk matrix, minimum controls |
| [0002](0002-evidence-coverage-and-trust.md) | E1–E4 coverage versus evidence trust/binding | accepted | Delivery evidence standard |
| [0003](0003-envelope-intent-not-authority.md) | Task envelope as intent, not runtime authority | accepted | Envelope schema, identity/grants |
| [0004](0004-manual-first-deterministic-validation.md) | Manual-first controls and pinned deterministic validation | accepted | Validator contracts, Nix flake |
| [0005](0005-policy-authority-and-projections.md) | Normative sources versus guidance and projections | accepted | Canonical architecture, lifecycle |
| [0006](0006-schema-compatibility-and-unknown-fields.md) | Fail-closed schema fields and version migration | accepted | JSON Schema, compatibility policy |
| [0007](0007-separate-delivery-authorities.md) | Generation, verification, approval, merge, release | accepted | Trust model, delivery evidence |

**Observed enforcement boundary:** [Issue #60](https://github.com/ryjen/agent-delivery-playbook/issues/60) is complete for active GitHub PR/required-check rules and a blocked failing-check test in this repository; see the [provider runbook](../operations/main-admission.md). An ADR is never provider evidence itself. Missing-check/direct-push rejection and runtime permission enforcement are not claimed.
