# Reviewer Checklist

Use this checklist when reviewing AI-assisted delivery work.

The goal is not to make every PR heavy. The goal is to make risk, scope, evidence, and tool authority visible.

## 1. Task Fit

- [ ] The PR maps to a task envelope.
- [ ] The objective is clear.
- [ ] The diff stays inside the stated scope.
- [ ] Any scope expansion is documented and reclassified.

## 2. Risk Classification

- [ ] The risk tier is plausible.
- [ ] Sensitive paths were checked.
- [ ] T4 surfaces were not downgraded silently.
- [ ] The evidence level matches the risk tier.

## 3. Tool Authority

- [ ] Tool use was appropriate for the task.
- [ ] Shell, network, dependency, CI, or write access is documented when material.
- [ ] Denied or escalated tool requests are visible.
- [ ] No tool use violates prohibited actions.

## 4. Context and Provenance

- [ ] Material sources that shaped the change are identifiable.
- [ ] Source content is distinguishable from generated summaries/inference.
- [ ] Untrusted repository/tool/web/memory content did not become authority merely by being observed.
- [ ] Stale, unknown, superseded, or revoked inputs are visible.
- [ ] Material context expansion was approved where required.
- [ ] Cross-project/tenant and sensitive-data boundaries were preserved.
- [ ] Secrets/customer/private data were minimized and retention is appropriate.

## 5. Evidence

- [ ] The PR includes specific evidence, not model claims.
- [ ] Test commands and results are named.
- [ ] Missing tests are explained.
- [ ] Operational validation exists for T3/T4 changes.
- [ ] Independent review exists for T4 changes.

## 6. Security Review

Challenge the PR if it touches:

- authentication
- authorization
- secrets
- CI/CD authority
- production data
- deployment paths
- infrastructure state
- dependency provenance
- audit logging

## 7. Attack Catalog Review

Look for signs of:

- prompt injection
- context poisoning
- dependency confusion
- secret exposure
- CI privilege escalation
- approval bypass
- evidence manipulation

## 8. Rollback

- [ ] The rollback path is specific.
- [ ] Reverting is sufficient, or a disable path exists.
- [ ] T3/T4 changes include operational recovery notes.

## 9. Merge Decision

Approve only when:

- the task envelope matches the work;
- the risk tier is credible;
- the evidence is sufficient;
- the rollback path is clear;
- any sensitive authority changes have explicit approval.

## Minimal Review Comment

```markdown
Reviewed against:

- Task envelope:
- Risk tier:
- Evidence level:
- Sensitive paths:
- Tool authority:

Decision:
```
