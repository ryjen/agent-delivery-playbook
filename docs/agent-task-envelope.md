# Agent Task Envelope

The Agent Task Envelope is the canonical record for AI-assisted engineering work. It defines the objective, risk tier, permitted context, allowed tools, execution constraints, evidence, and review requirements before an agent acts.

The envelope is intentionally boring. It should be easy to diff, review, archive, and replay.

## Why This Exists

AI delivery needs a stable unit of governance. Prompts are too informal, chat history is too implicit, and PR descriptions arrive too late. The task envelope sits before execution and becomes the contract for the work.

Use it as the equivalent of:

- a change request
- a Terraform plan
- a build manifest
- a lightweight audit record

## Required Properties

Every envelope MUST include:

- task id
- objective
- owner
- risk tier
- repositories or bounded workspaces
- allowed tools
- prohibited actions
- evidence expectations
- review requirements

## Risk Tiers

| Tier | Meaning | Typical Review |
| --- | --- | --- |
| T1 | Documentation or non-runtime metadata | Lightweight review or auto-merge |
| T2 | Localized code change with test coverage | Human review |
| T3 | Cross-cutting runtime, data, or workflow change | Human review plus operational evidence |
| T4 | Security, auth, infra, secrets, CI/CD, production data | Explicit approval gate and security review |

## Evidence Levels

Use `evidence.required_levels` as an ordered array. This preserves composite requirements from the Delivery Evidence Standard, such as `E2 + E3` for T3 work and `E2 + E3 + E4` for T4 work.

Legacy examples may refer to singular `required_level`; new envelopes SHOULD use `required_levels`.

## Context and Provenance

The `context` section is part of the authority boundary. It records what the agent may inspect and, when needed, why other context was excluded, summarized, deferred, or escalated.

For small T1/T2 tasks, `repositories` and `references` may be enough. For medium/high-risk work or any sensitive-path-adjacent task, add `context.provenance`.

`context.references` values are strings. Quote values that look like YAML mappings, such as `"issue: APP-1234"`, so examples remain compatible with the JSON Schema.

Recommended provenance fields:

| Field | Purpose |
| --- | --- |
| `approved_sources` | Sources authorized before execution |
| `included` | Sources actually supplied or inspected |
| `summarized` | Sources summarized instead of supplied raw |
| `excluded` | Sources intentionally not supplied, with reason |
| `deferred` | Sources held back unless execution blocks |
| `escalations` | Context expansion requests and approval status |
| `model_context_assumption` | Practical context-size/model assumption, where known |
| `stale_context_caveats` | Known freshness risks in supplied context |

Context expansion requires reclassification or approval when it crosses repositories, sensitive paths, credential boundaries, production data, or the original risk tier.

## Minimal Envelope

```yaml
task:
  id: T-0001
  title: Fix Android login crash
  objective: Resolve crash during token refresh without changing auth semantics.
  owner: rj

classification:
  type: bugfix
  risk_tier: T2

context:
  repositories:
    - mobile-app
  references:
    - "issue: APP-1234"
  provenance:
    approved_sources:
      - src/auth/session-refresh.kt
      - tests/session-refresh-test.kt
    included:
      - failing stack trace
      - affected module
    summarized:
      - none
    excluded:
      - path: signing/
        reason: Signing material is unrelated and sensitive.
    deferred:
      - docs/auth-architecture.md
    escalations:
      - source: CI workflow
        reason: CI edits would require reclassification.
        status: not_requested
    model_context_assumption: Localized bugfix; no large-context retrieval required.
    stale_context_caveats:
      - Issue report may not reflect latest main branch.

constraints:
  allowed:
    - inspect existing login flow
    - modify localized crash handling
    - add regression tests
  prohibited:
    - changing token lifetime
    - changing OAuth scopes
    - editing CI workflows

execution:
  tools:
    - repo_read
    - shell_tests
    - github_pr
  actions:
    - inspect
    - patch
    - test
    - summarize

evidence:
  required_levels:
    - E2
  tests:
    - unit
    - regression
  artifacts:
    - test output
    - PR diff

review:
  required: true
  approvers:
    - code_owner
  notes: Auth-adjacent but not auth-policy-changing.

status: proposed
```

## Governance Rules

Agents MUST NOT expand scope silently. A task requiring a broader workspace, stronger tool, higher risk tier, or weaker evidence must be reclassified before execution continues.

Agents MUST treat the envelope as binding input, not advisory context.

Reviewers SHOULD reject work when the PR does not map back to the envelope objective, constraints, and evidence expectations.

## State Model

```mermaid
flowchart LR
  Proposed --> Approved
  Approved --> Executing
  Executing --> EvidenceCollected
  EvidenceCollected --> Review
  Review --> Merged
  Review --> Rejected
  Executing --> Blocked
```

## Integration Points

The envelope can be used by:

- PR templates
- approval engines
- CI policy checks
- MCP/Hermes tool gates
- audit logs
- incident reviews

## Design Bias

Prefer explicit limits over clever automation. The envelope should make unsafe expansion visible before it becomes an execution problem.
