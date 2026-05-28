# Agent Task Contract

Use this contract before assigning medium or high-risk work to an AI coding agent.

## Task

**Title:**

**Requester:**

**Reviewer:**

**Risk tier:** 0 / 1 / 2 / 3 / 4

## Goal

Describe the specific outcome expected from the agent.

## Non-goals

List what the agent must not attempt, even if it appears adjacent.

## Allowed scope

Files, directories, modules, or systems the agent may inspect or modify:

- 

## Disallowed scope

Files, directories, modules, or systems the agent must not modify:

- CI/CD or release workflows unless explicitly included
- Secrets, credentials, signing material, or production configuration
- Auth/security/privacy-sensitive code unless explicitly included
- Unrelated refactors

## Context to use

- Relevant files:
- Relevant tests:
- Relevant docs:
- Relevant logs/errors:
- Security invariants:
- Architecture notes:

## Constraints

- No new dependencies without approval
- No production secrets
- No unrelated formatting sweeps
- Preserve existing public APIs unless explicitly changing them
- Keep the diff reviewable

## Required tests and checks

```sh
# Add expected commands here
```

## Required evidence

The agent must report:

- Summary of changes
- Files changed
- Commands run
- Test results
- Tests not run and why
- Risks or uncertainty
- Follow-up recommendations

## Security review notes

Map the task to any relevant invariants:

- Authentication/authorization:
- Data protection:
- Secrets:
- Dependencies:
- Logging/telemetry:
- Mobile/client permissions or signing:

## Rollback plan

Describe how the change can be reverted or disabled:

- Revert commit:
- Feature flag:
- Config rollback:
- Dependency pin rollback:
- Mobile phased rollout halt:

## Acceptance criteria

- [ ] Task stayed within scope
- [ ] Required tests/checks passed or failures are explained
- [ ] Evidence is attached or summarized
- [ ] Security invariants preserved
- [ ] Reviewer can understand the change without trusting the agent
- [ ] Rollback path is documented for meaningful risk
