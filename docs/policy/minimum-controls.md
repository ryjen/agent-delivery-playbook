# Minimum Controls Policy

This policy maps risk tiers to the minimum controls expected before merge.

It is intentionally lightweight. The point is to create a common baseline that can later be enforced by templates, CI checks, or approval tooling.

Use [`../adoption/minimal-adoption-kernel.md`](../adoption/minimal-adoption-kernel.md) to choose the smallest sufficient artifact set. A required control does not imply a dedicated file when an existing issue, PR, permission, or protected workflow represents the concern equivalently.

## Representation versus control

The kernel concerns—intent, risk, authority/tool constraints, evidence, and accountable outcome—must be resolved for meaningful write-capable work. Provenance ledgers, capability catalogs, replay bundles, tool decision records, attestations, and rollback rehearsals are risk-triggered extensions rather than universal paperwork.

## Control Matrix

| Tier | Envelope | Evidence | Tool Records | Review | Merge Posture |
| --- | --- | --- | --- | --- | --- |
| T1 | Recommended | E1 | Usually not required | Optional or lightweight | Can be fast path |
| T2 | Required | E2 | Required for shell/write/network/dependency use | Human review | Normal PR |
| T3 | Required | E2 + E3 | Required for material tool use | Owner review | No auto-merge without evidence |
| T4 | Required | E2 + E3 + E4 | Required | Security/infra/owner approval | Blocked until approval complete |

## T1 Controls

Use for documentation-only or non-runtime metadata changes.

Required:

- clear summary
- no sensitive paths
- no runtime behavior changes

Recommended:

- task envelope
- Markdown or link review

## T2 Controls

Use for localized code changes with bounded impact.

Required:

- task envelope
- evidence report
- targeted tests or explicit test gap
- human review

## T3 Controls

Use for cross-cutting runtime, data, workflow, or integration changes.

Required:

- task envelope
- evidence report
- tests
- operational validation
- rollback notes
- owner review

## T4 Controls

Use for restricted authority such as production secrets, signing/admin authority, or destructive/irreversible production effects. High-risk but bounded auth/security/CI/CD work may be T3 when policy permits tightly constrained agent assistance; T4 remains human-led.

Required:

- task envelope
- explicit approval before execution
- evidence report
- tool call decision records
- tests
- operational validation
- rollback or recovery plan
- independent security, infra, or owner review

## Auto-Merge Guidance

Auto-merge is acceptable only when:

- the tier is T1 or explicitly allowed T2;
- required evidence is present;
- no sensitive path policy is triggered;
- no unresolved review concern exists.

Auto-merge should not be used for T3/T4 unless a mature policy engine validates all required controls.

## Escalation Triggers

Escalate the tier when the change introduces:

- new dependency
- new network call
- new file write path
- workflow permission change
- deployment behavior change
- authentication or authorization behavior
- secret access or secret-adjacent path
- production data handling
- broad refactor beyond task scope

## Review Bias

Small diff does not mean low risk. A one-line workflow, permission, dependency, or authorization change can be T4.
