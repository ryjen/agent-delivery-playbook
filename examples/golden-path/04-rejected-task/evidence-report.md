# Delivery Evidence

## Objective

Reject a request that would bypass required checks and provide a safer path.

## Changes

- No implementation performed.
- Policy reason recorded.
- Safer alternative proposed.

## Tests

```text
command/check: not run
result: not applicable
scope: rejected task
```

## Assumptions

The requested shortcut conflicts with the task envelope and minimum controls.

## Risks

The requester may need a new task envelope for the safer path.

## Rollback

No implementation was performed.

## Reviewer Notes

Confirm refusal/escalation was the correct outcome.

## Envelope Mapping

- Task id: GP-0004
- Risk tier: T4
- Required evidence levels: E2, E3, E4
- Prohibited actions checked: yes