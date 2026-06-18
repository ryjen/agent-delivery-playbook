# Summary

## Task Envelope

- Task id:
- Risk tier: T1 / T2 / T3 / T4
- Required evidence level: E1 / E2 / E3 / E4
- Task envelope link or path:

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

### Commands / Checks

```text
command:
result:
scope:
```

### Evidence Artifacts

- [ ] Diff reviewed
- [ ] Static checks / lint / formatting
- [ ] Tests
- [ ] Operational validation
- [ ] Independent review / approval

## Assumptions

List assumptions that affected the implementation or review.

## Risks

List known residual risks.

## Rollback

Describe how to revert, disable, or recover from this change.

## Reviewer Focus

Call out the files, behavior, or policy decisions reviewers should inspect first.
