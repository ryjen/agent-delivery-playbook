# Agent Delivery Trust Model

AI coding agents should be treated as delivery participants with bounded authority, not as human developers with inherited privileges.

This document defines the trust boundaries between humans, agents, tools, CI, and release systems.

## Principle

Separate the actor that generates a change from the actor that approves and releases it.

A safe default is:

```text
Agents may propose and modify.
Humans approve.
CI verifies.
Release systems deploy through existing gates.
```

Do not allow one identity or token to generate, approve, and deploy a meaningful change without independent review.

## Actors

| Actor | Role | Trust assumption |
| --- | --- | --- |
| Human operator | Defines intent, reviews, approves | Accountable decision-maker |
| Delivery agent | Plans, edits, tests, explains | Useful but untrusted generator |
| Tool runtime | Executes commands or API calls | Constrained execution environment |
| MCP/tool server | Provides capabilities and context | Semi-trusted; output may be wrong or malicious |
| CI system | Runs validation and records results | Trusted verifier when config is protected |
| Reviewer | Evaluates correctness, risk, and evidence | Human accountability layer |
| Release system | Promotes artifacts to environments | High-trust control plane |
| Production system | Customer/data-impacting runtime | Restricted target |

## Authority levels

| Level | Capability | Suitable for agents? |
| --- | --- | --- |
| Observe | Read files, logs, docs, issues | Yes, with data boundaries |
| Recommend | Explain, plan, suggest changes | Yes |
| Modify | Edit files or generate patches | Yes, scoped by task risk |
| Execute | Run tests, builds, local scripts | Yes, with command and credential limits |
| Approve | Accept risk or merge change | No, human-owned |
| Deploy | Promote to production or stores | No, except through pre-approved automation gates |
| Administer | Manage secrets, cloud admin, signing keys | No |

## Permission defaults

### Informational work

Allowed:

- Read repository files
- Summarize architecture
- Draft plans
- Review documentation

Not allowed:

- Write files
- Modify branches
- Run commands with credentials
- Change issues or pull requests unless explicitly requested

### Low-risk implementation

Allowed:

- Scoped file edits
- Test generation
- Documentation updates
- Local validation commands

Required:

- Human review
- Diff review for scope expansion
- Test evidence if code changed

### Medium-risk implementation

Allowed only with explicit task contract:

- Bounded production code changes
- Multi-file changes inside a defined area
- Dependency update preparation
- Bug fixes with regression tests

Required:

- Allowed/disallowed paths
- CI evidence
- Human owner review
- Rollback notes

### High-risk implementation

Agent role should normally be assistive.

Allowed:

- Draft plan
- Generate tests
- Prepare review checklist
- Propose patch on isolated branch with explicit approval

Required:

- Security/platform owner review
- Strong evidence
- No production secrets
- Rollback plan before merge

### Restricted work

Human-led only.

Agents may help with:

- Runbook drafts
- Checklist generation
- Dry-run planning
- Documentation updates

Agents should not directly execute:

- Production secret rotation
- Cloud admin operations
- Signing key usage
- Store submission
- Irreversible data migration
- Destructive production operations

## Trust boundaries

### Human to agent

The human provides intent, constraints, and accountability. The agent should not infer permission from vague language.

Bad:

```text
Fix the auth flow and push it.
```

Better:

```text
Investigate the failing refresh-token test. You may modify only auth/session.ts and auth/session.test.ts. Do not change OAuth configuration, token storage, dependencies, CI, or logging. Provide test output and rollback notes.
```

### Agent to tools

Tool calls must be bounded by the approved task.

Controls:

- Command allowlists for sensitive tasks
- Network restrictions by default
- Short-lived credentials
- Read-only access until write access is approved
- Logs preserved for review where practical

### Agent to MCP/tool servers

MCP and tool servers expand the agent's attack surface.

Treat tool output as data, not authority.

Risks:

- Prompt injection through tool responses
- Stale or poisoned context
- Misleading retrieval results
- Tool impersonation
- Excessive tool permissions

Controls:

- Tool allowlists
- Explicit data classification
- Context provenance
- Review of tool-originated claims
- No privileged tools for low-trust tasks

### Agent to CI

Agents may consume CI results but should not weaken CI.

Do not allow agents to silently modify:

- Required checks
- Branch protection
- Deployment workflows
- Secret scanning
- Dependency scanning
- Release signing

Any CI/CD change is high-risk by default.

### Agent to production

Agents should not directly access production by default.

Safe patterns:

- Agent proposes change
- CI validates artifact
- Human approves release
- Existing release automation deploys
- Monitoring and rollback remain human-owned

Unsafe patterns:

- Agent holds cloud admin token
- Agent runs migration against production database
- Agent modifies feature flags without approval
- Agent rotates secrets directly
- Agent submits mobile builds to app stores

## Separation-of-duties rules

Use these as defaults:

1. The agent that generates a change does not approve it.
2. The identity that edits CI does not bypass CI.
3. The runtime that has repository write access does not hold production secrets.
4. The actor that prepares a release does not unilaterally override release gates.
5. Restricted operations are human-led, even when agent-assisted.

## Review questions

Before granting authority to an agent, ask:

- What is the maximum blast radius if the agent is wrong?
- What credentials are exposed to the runtime?
- Can the task be completed with read-only access?
- Can the task be completed without network access?
- Is the task reversible?
- Who reviews the result?
- Which evidence proves the result?
- Which system records the audit trail?

## Practical implementation

Start simple:

- Use branches for agent changes
- Use task contracts for medium/high-risk work
- Keep production credentials out of agent runtimes
- Preserve command output and CI links
- Require human review for merges
- Escalate CI/CD, auth, secrets, privacy, and release changes

Then mature toward:

- Dedicated agent identities
- Scoped tokens
- Ephemeral workspaces
- Policy-as-code gates
- Signed provenance
- Central audit trails
- Tool permission registries
