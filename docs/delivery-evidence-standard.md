# Delivery Evidence Standard

The Delivery Evidence Standard defines what must be produced before AI-assisted work can be trusted, reviewed, merged, or promoted.

The core rule is simple:

> Trust evidence produced by the delivery process, not claims produced by the model.

## Evidence Levels

| Level | Name | Description |
| --- | --- | --- |
| E0 | No Evidence | Unverified output. Not acceptable for merge. |
| E1 | Static Evidence | Formatting, linting, type checks, schema validation. |
| E2 | Test Evidence | Unit, regression, integration, or contract tests. |
| E3 | Operational Evidence | Deploy checks, smoke tests, logs, metrics, rollback validation. |
| E4 | Independent Verification | Human review, security review, owner approval, or independent reproduction. |

## Risk-to-Evidence Matrix

| Risk Tier | Minimum Evidence | Notes |
| --- | --- | --- |
| T1 | E1 | Documentation and metadata can use lightweight evidence. |
| T2 | E2 | Local code changes need tests or a documented reason tests are unavailable. |
| T3 | E2 + E3 | Runtime-impacting changes need operational validation. |
| T4 | E2 + E3 + E4 | Security, infra, CI/CD, secrets, auth, and production-data changes require independent review. |

## Required Evidence Report

Every AI-assisted PR SHOULD include:

```markdown
# Delivery Evidence

## Objective

## Changes

## Tests

## Assumptions

## Risks

## Rollback

## Reviewer Notes
```

## Evidence Quality Rules

Evidence MUST be specific. "Tests pass" is weaker than naming the command, scope, and result.

Evidence MUST be reproducible where possible. A reviewer should know how to re-run or inspect it.

Evidence MUST preserve uncertainty. If a test was not run, say why.

Evidence MUST NOT rely on model confidence as a substitute for verification.

## Examples

### Weak

```text
Tested locally.
```

### Better

```text
Ran npm test -- auth-refresh.spec.ts. Added regression coverage for refresh-token null response. Full suite not run because unrelated e2e environment is not available locally.
```

## Rollback Evidence

For T3/T4 work, rollback should be explicit:

- revert commit
- feature flag off
- restore previous workflow version
- redeploy previous artifact
- disable automation path

## Reviewer Checklist

- Does the evidence match the task envelope?
- Is the risk tier plausible?
- Are prohibited actions avoided?
- Are assumptions visible?
- Is rollback credible?
- Would this evidence survive an incident review?
