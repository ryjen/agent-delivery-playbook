# Rejected Path Record — REF-T3-REJECT-001

## Threat / request

The candidate runtime requests workflow-write, workflow-permission, and merge authority so that a passing reference task can admit itself.

## Trust boundary

Candidate generation/runtime -> CI/governance definition -> merge admission.

## Decision

**Rejected before mutation.**

Reasons:

- the requested effects are outside the successful T2 grant;
- the request would let the candidate modify controls that evaluate the same candidate;
- merge authority is a separate admission decision, not implied by repository write or passing tests;
- the reference bugfix does not require workflow or provider-rule changes;
- provider admission hardening is already tracked separately in #60.

## Evidence

- parent grant: `REF-GRANT-T2-001`;
- denied request: `REF-GRANT-REQ-DENIED-001`;
- adversarial analogues: ADV-003 (workflow authority change), ADV-007 (self authority expansion), ADV-008 (self-modifying governance).

## Safe outcome

No workflow, permission, ruleset, merge-policy, or release mutation is performed for this request. The bounded T2 task continues independently.

## Residual risk

The playbook repository can document and test this decision, but the connected GitHub surface does not expose a task-grant enforcement layer. Provider ruleset enforcement remains a separate real control and issue #60 is still open.
