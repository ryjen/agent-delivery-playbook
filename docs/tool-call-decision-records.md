# Tool Call Decision Records

A Tool Call Decision Record captures why an agent used, requested, or was denied a tool.

The goal is not to log every implementation detail. The goal is to preserve meaningful authority changes: shell access, filesystem writes, network calls, CI execution, secrets-adjacent reads, production access, and workflow changes.

## Why This Exists

Agent risk often comes from tool use, not text generation.

A safe-looking prompt can become dangerous when the agent gains access to:

- shell execution
- repository writes
- package installation
- browser or network access
- CI/CD modification
- credentials or secret-adjacent files
- production systems

Tool Call Decision Records make those boundaries reviewable.

## Record Format

```yaml
tool_call_decision:
  id: TCDR-0001
  task_id: T-0002
  grant_id: GRANT-WRITE-017
  invocation_id: workflow-run:<run-id>
  requested_tool: shell_tests
  requested_action: run targeted unit tests
  decision: approved
  reason: Required to satisfy E2 evidence for localized bug fix.
  constraints:
    - run test command only
    - do not install packages
    - do not access secrets
  evidence:
    - command output attached to PR evidence
  decided_by: task_owner
```

## Decision Types

| Decision | Meaning |
| --- | --- |
| approved | Tool use is allowed within explicit constraints. |
| denied | Tool use is not allowed for this task. |
| escalated | Tool use requires higher risk tier, approval, or review. |
| deferred | Tool use is not needed yet or lacks enough context. |

## Tools That Usually Need a Record

| Tool Surface | Record Required? | Reason |
| --- | --- | --- |
| Read-only repository inspection | Usually no | Low authority if bounded. |
| Repository writes | Yes | Changes project state. |
| Shell commands | Yes | Can execute unexpected behavior. |
| Package installation | Yes | Supply-chain surface. |
| CI workflow edits | Yes, normally T3; T4 if restricted authority is required | Changes delivery authority and may trigger stronger review. |
| Network access | Yes | Exfiltration and untrusted input surface. |
| Secret or credential paths | Yes; T4 when restricted credentials are requested | High-impact exposure risk. |
| Production access | Yes; typically T4 for privileged/destructive effects | Operational impact and restricted authority. |

## Denial Example

```yaml
tool_call_decision:
  id: TCDR-0007
  task_id: T-0004
  requested_tool: filesystem_read
  requested_action: inspect .env.production
  decision: denied
  reason: Production secret access is prohibited by the task envelope.
  constraints: []
  evidence:
    - denial noted in PR evidence
  decided_by: policy
```

## Escalation Example

```yaml
tool_call_decision:
  id: TCDR-0011
  task_id: T-0009
  requested_tool: github_workflow_write
  requested_action: change pull_request workflow permissions
  decision: escalated
  reason: CI permission changes require high-risk reclassification and platform/security review; restricted authority, if requested, remains T4 and human-led.
  constraints:
    - stop execution until reclassified
  evidence:
    - changed path matched sensitive path policy
  decided_by: policy
```

## Reviewer Checklist

- Did the agent use tools outside the task envelope?
- Did shell or network access have a bounded reason?
- Did dependency changes include provenance evidence?
- Did sensitive path edits trigger escalation?
- Were denied or escalated tool requests documented?

## Design Rule

Do not bury tool authority inside chat transcript. Put the decision where reviewers can see it.

## Grant relationship

When grant and invocation identifiers exist, material tool-call decisions should reference them.

A decision can approve use already inside the active grant, deny, defer, or escalate a request for a new/superseding grant. It cannot widen the current grant by itself, and the requesting runtime cannot approve its own expansion.

Retries use a new invocation ID. The same grant may be reused only while its task/resource/code/capability/time bindings remain valid.