# Policy-to-CI Enforcement Strategy

This strategy defines how the playbook can move from documented governance to automated checks without overbuilding or replacing reviewer judgment.

## Principle

CI should enforce objective rules, warn on likely risk signals, and leave semantic risk decisions to humans.

## Enforcement Categories

| Category | Meaning | Examples |
| --- | --- | --- |
| Hard failure | Objective, deterministic rule failed | invalid task envelope example, malformed policy file, missing required PR section after policy is adopted |
| Warning / review prompt | Risk signal needs human confirmation | sensitive path match, broad glob match, missing rollback detail on a non-trivial change |
| Human judgment only | CI cannot safely decide | whether evidence is convincing, whether risk tier is appropriate, whether architecture drift is acceptable |

## Candidate Checks

| Check | Category | Notes |
| --- | --- | --- |
| Task envelope examples validate against schema | hard failure | Safe once validation is stable and dependency-light |
| Required PR sections exist | warning first, hard failure later | Useful only after template adoption is stable |
| Sensitive paths trigger review prompt | warning / review prompt | Broad matches should not automatically block |
| T3/T4 changes are not auto-merge eligible | warning / branch protection input | CI can signal; repository settings enforce |
| Broad path matches require manual confirmation | review prompt | Prevents false confidence from naive glob matching |

## Incremental Roadmap

### Phase 0: Manual Templates and Docs

- governed PR template
- task envelope examples
- reviewer checklist
- evidence standard
- sensitive path policy

Outcome: humans have consistent prompts and vocabulary.

### Phase 1: Local Validation

- validate task envelope examples locally
- keep scripts dependency-light
- document expected failures

Outcome: contributors can check examples before opening a PR.

### Phase 2: Advisory CI

- run validators in CI without blocking initially, or post review prompts
- surface sensitive path matches as review notes
- report missing PR sections as warnings

Outcome: CI assists reviewers without pretending to decide risk.

### Phase 3: Blocking CI for Objective Rules

Only promote checks to hard failures when they are deterministic and low-noise:

- malformed schema or policy files
- invalid example envelopes
- missing required files in examples
- invalid enum values

Outcome: mechanical drift is blocked.

### Phase 4: Branch Protection and CODEOWNERS Integration

- map sensitive paths to CODEOWNERS or owner review requirements
- use branch protection for required review and status checks
- keep broad matches advisory unless allowlists and downgrade rules exist

Outcome: enforcement moves into existing repository controls instead of a custom platform.

## PR Body Checks

PR body checks are useful as a reminder, but fragile as hard gates.

Recommended posture:

1. warn when sections are missing;
2. do not parse free text for risk truth;
3. require humans to confirm risk tier, evidence, rollback, and sensitive path review;
4. only block once the template has stabilized and false positives are low.

## Sensitive Path Policy Interaction

Sensitive path checks should:

- identify matched paths;
- show the minimum expected tier and review owner;
- distinguish exact control paths from broad name-based globs;
- require manual confirmation for downgrades;
- integrate with CODEOWNERS where possible.

They should not:

- automatically classify all broad matches as hard failures;
- replace owner review;
- imply CI understands semantic intent.

## Non-goals

- automated semantic risk classification;
- CI replacing reviewer judgment;
- heavyweight policy engine inside this repository;
- autonomous merge or release decisions;
- custom approval platform.

## Good First CI Candidate

The safest first blocking check is validating repository-owned examples and policy data, because failures are objective and local to this playbook.

## Deferred Work

- exact validator implementation details;
- PR comment bot behavior;
- CODEOWNERS examples;
- branch protection recipes;
- repository-specific allowlists.
