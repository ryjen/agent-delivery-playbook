# Agent Capability Catalog

Use this catalog to document durable agent/tool authority in this repository.

## Catalog metadata

| Field | Value |
| --- | --- |
| Repository/workspace |  |
| Catalog owner |  |
| Last reviewed |  |
| Next review due |  |
| Review cadence |  |

## Agent or tool entry

| Field | Value |
| --- | --- |
| Name |  |
| Type | coding agent / CI bot / MCP server / shell executor / hosted service / other |
| Owner |  |
| Intended use cases |  |
| Prohibited use cases |  |
| Allowed repositories/workspaces |  |
| Allowed paths |  |
| Sensitive paths | none / listed below |
| Human escalation contact |  |
| Runtime/workload identity or class |  |
| Runtime identity evidence | authenticated / provider-attested / declared / unknown |
| Invocation/workflow identity source |  |
| Nested delegation allowed | no / yes, bounded below |
| Maximum grant lifetime |  |
| Revocation mechanism |  |

### Authority profile

| Authority dimension | Granted? | Scope | Notes |
| --- | --- | --- | --- |
| Read repository content | yes / no |  |  |
| Read issues/PRs | yes / no |  |  |
| Write files | yes / no |  |  |
| Create branches | yes / no |  |  |
| Create or update PRs | yes / no |  |  |
| Modify issues/labels | yes / no |  |  |
| Run local shell commands | yes / no |  |  |
| Run package managers | yes / no |  |  |
| Trigger CI workflows | yes / no |  |  |
| Access network | yes / no |  |  |
| Access credentials/secrets | yes / no |  |  |
| Approve/merge/release | yes / no |  |  |

### Credential class

- [ ] No credentials
- [ ] Read-only token
- [ ] Repository-scoped write token
- [ ] CI-scoped token
- [ ] Runtime-local credential file
- [ ] Privileged credential requiring explicit approval

Credential storage and rotation notes:

```text

```

### Delegation limits

- Maximum child capabilities:
- Maximum child resource/path scope:
- Maximum child lifetime:
- Maximum delegation depth:
- Authorities that may never be delegated:

### Approval requirements

| Action | Approval required | Approver |
| --- | --- | --- |
| Read approved context |  |  |
| Modify non-sensitive files |  |  |
| Modify sensitive paths |  |  |
| Run shell/build/test commands |  |  |
| Trigger CI or deployment workflows |  |  |
| Access secrets or production-adjacent data |  |  |

### Evidence expectations

- Task envelope reference:
- Required evidence levels:
- Replayable evidence required: yes / no
- CI artifacts required:
- Manual verification required:
- Rollback evidence required:

### Decommission and stale-authority controls

- Last permission review:
- Next permission review:
- Disable condition:
- Token revocation path:
- Owner handoff path:

## Review rule

Model identity is not authority identity. Record runtime identity evidence, tool surface, token class, delegation limits, lifetime, revocation path, and approval boundary. Cataloged authority is a ceiling, not a task grant.