# Example Agent Capability Catalog

## Catalog metadata

| Field | Value |
| --- | --- |
| Repository/workspace | `example-app` |
| Catalog owner | Platform/AppSec owner |
| Last reviewed | 2026-06-18 |
| Next review due | 2026-07-18 |
| Review cadence | Monthly for write-capable tooling |

## Agent or tool entry

| Field | Value |
| --- | --- |
| Name | Docs PR Assistant |
| Type | hosted coding agent with GitHub PR creation |
| Owner | Developer Experience |
| Intended use cases | Documentation fixes, README updates, examples, non-runtime metadata |
| Prohibited use cases | Auth, secrets, CI workflow edits, release automation, dependency upgrades |
| Allowed repositories/workspaces | `example-app` |
| Allowed paths | `README.md`, `docs/**`, `examples/**` |
| Sensitive paths | `.github/workflows/**`, `infra/**`, `src/auth/**`, `secrets/**` |
| Human escalation contact | Repository maintainer |

### Authority profile

| Authority dimension | Granted? | Scope | Notes |
| --- | --- | --- | --- |
| Read repository content | yes | approved repo paths | Sensitive paths require explicit approval |
| Read issues/PRs | yes | issue and PR metadata | No private customer data |
| Write files | yes | branch only | No direct main writes |
| Create branches | yes | feature branches | Naming convention required |
| Create or update PRs | yes | docs-only PRs | Human review required |
| Modify issues/labels | no | n/a | Maintainer action only |
| Run local shell commands | no | n/a | CI provides validation |
| Run package managers | no | n/a | Avoid dependency drift |
| Trigger CI workflows | no | n/a | CI runs from PR events only |
| Access network | limited | GitHub API only | No arbitrary external calls |
| Access credentials/secrets | no | n/a | No production or CI secrets |
| Approve/merge/release | no | n/a | Humans approve merge and release |

### Credential class

- [ ] No credentials
- [ ] Read-only token
- [x] Repository-scoped write token
- [ ] CI-scoped token
- [ ] Runtime-local credential file
- [ ] Privileged credential requiring explicit approval

Credential storage and rotation notes:

```text
GitHub app token scoped to branch and PR creation. Rotate monthly or on owner change.
```

### Approval requirements

| Action | Approval required | Approver |
| --- | --- | --- |
| Read approved context | no | catalog owner pre-approval |
| Modify non-sensitive files | yes | PR reviewer |
| Modify sensitive paths | yes | code owner plus AppSec/platform owner |
| Run shell/build/test commands | yes | maintainer or CI policy |
| Trigger CI or deployment workflows | yes | maintainer |
| Access secrets or production-adjacent data | yes | security owner; normally prohibited |

### Evidence expectations

- Task envelope reference: required for every PR.
- Required evidence levels: E1 for docs, higher if risk changes.
- Replayable evidence required: yes for medium/high-risk or any sensitive-path discussion.
- CI artifacts required: if CI runs.
- Manual verification required: reviewer confirms scope and sensitive paths.
- Rollback evidence required: revert PR.

### Decommission and stale-authority controls

- Last permission review: 2026-06-18
- Next permission review: 2026-07-18
- Disable condition: stale owner, token leak, scope violation, or unused for 90 days
- Token revocation path: revoke GitHub app installation/token
- Owner handoff path: update catalog before owner change completes

## Review rule

The model used by this assistant is not the authority boundary. The GitHub app token, allowed paths, prohibited actions, and human review gates define authority.