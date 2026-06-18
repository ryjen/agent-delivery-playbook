# Summary

Briefly describe what changed and why.

## Task Envelope

- Task id or link/path:
- Risk tier: T1 / T2 / T3 / T4
- Required evidence: E1 / E2 / E3 / E4, or combination such as E2 + E3
- Sensitive paths checked: yes / no / not applicable

For T1 documentation-only work, a short inline envelope is enough when the scope, evidence, and rollback notes below are clear.

## Change Type

- [ ] Documentation only
- [ ] Localized code change
- [ ] Cross-cutting runtime change
- [ ] Infrastructure / CI / deployment change
- [ ] Authentication / authorization / secrets / production data change

## Scope Control

- [ ] The change matches the stated objective.
- [ ] No prohibited actions from the task envelope were performed.
- [ ] No hidden dependency, workflow, secret, or permission changes were introduced.
- [ ] Any scope expansion was explicitly reclassified before proceeding.

## Evidence

```text
command/check:
result:
scope:
```

- [ ] Diff reviewed
- [ ] Static checks / lint / formatting
- [ ] Tests
- [ ] Operational validation
- [ ] Independent review / approval

Explain unchecked items when they are not applicable.

## Assumptions

List assumptions that affected the implementation or review.

## Risks

List known residual risks.

## Rollback

Describe how to revert, disable, or recover from this change.

## Reviewer Focus

Call out the files, behavior, or policy decisions reviewers should inspect first.
