# Task Risk Matrix

Use this matrix before assigning work to an AI coding agent. The goal is not to block agent use. The goal is to match the task to the right constraints, evidence, and review path.

## Risk tiers

| Tier | Description | Agent suitability | Required controls |
| --- | --- | --- | --- |
| 0: Informational | Read-only explanation, summarization, navigation, docs review | Good fit | No write access, cite files or paths used |
| 1: Low | Docs, comments, tests, local refactors with narrow scope | Good fit | Normal review, tests if code touched |
| 2: Medium | Bug fixes, feature work, dependency prep, multi-file changes | Fit with controls | Task contract, scoped write access, CI evidence, human review |
| 3: High | Auth, privacy, security, CI/CD, release, mobile signing, migrations | Assistive only unless tightly controlled | Security/platform owner review, explicit rollback, stronger evidence |
| 4: Restricted | Production secrets, signing keys, cloud admin, irreversible data changes | Human-led | Agent may help draft plan/docs only |

## Classification questions

Classify as the highest tier triggered by any question.

| Question | If yes |
| --- | --- |
| Does the task only ask for explanation or documentation review? | Tier 0 |
| Does the task change only docs, comments, or tests? | Tier 1 |
| Does the task change production code in one bounded area? | Tier 2 |
| Does the task require dependency changes? | Tier 2 minimum |
| Does the task touch auth, crypto, secrets, privacy, or policy enforcement? | Tier 3 minimum |
| Does the task touch CI/CD, release, signing, package publishing, or deployment? | Tier 3 minimum |
| Does the task require production credentials or privileged cloud access? | Tier 4 |
| Does the task include irreversible data migration or deletion? | Tier 4 unless human-led with controlled tooling |
| Does the task affect mobile permissions, entitlements, privacy manifests, or signing? | Tier 3 minimum |

## Required controls by tier

### Tier 0: Informational

Allowed:

- Read repository files
- Explain architecture
- Summarize risks
- Draft plans

Not allowed:

- Write files
- Run commands with credentials
- Modify issues, PRs, releases, or branches unless explicitly requested

Evidence:

- Files inspected
- Assumptions and uncertainty

### Tier 1: Low

Allowed:

- Documentation changes
- Test scaffolding
- Small local refactors
- Comments and examples

Controls:

- Human review
- Diff check for scope expansion
- Tests if executable code changed

Evidence:

- Summary of changes
- Commands run if applicable
- Known limitations

### Tier 2: Medium

Allowed:

- Bounded production bug fixes
- Small features
- Multi-file refactors with explicit boundary
- Dependency update preparation

Controls:

- Task contract
- Allowed/disallowed file paths
- Scoped write access
- CI evidence
- Human review from owning team
- Dependency/license scan if dependencies changed

Evidence:

- Test output or CI link
- Before/after behavior
- Risk notes
- Rollback path

### Tier 3: High

Allowed:

- Agent-assisted implementation only with tight constraints
- Safer default: agent drafts plan, tests, or review checklist; human performs sensitive changes

Controls:

- Security or platform owner review
- Explicit approval before execution
- No production secrets in agent runtime
- Strong CI evidence
- Negative/security tests where relevant
- Rollback plan before merge
- CODEOWNERS or equivalent review gate

Evidence:

- Threat considerations
- Security invariant mapping
- Test matrix
- Rollback or disablement procedure
- Manual review notes

### Tier 4: Restricted

Allowed:

- Documentation assistance
- Dry-run planning
- Checklist generation
- Human-reviewed scripts that are never executed by the agent with privileged credentials

Not allowed:

- Direct production access
- Direct use of signing keys
- Direct execution of destructive migrations
- Cloud admin operations
- Store release submission
- Secret rotation execution

Controls:

- Human-led execution
- Change management approval
- Break-glass procedures where applicable
- Full audit trail

## Examples

| Task | Tier | Notes |
| --- | --- | --- |
| Add README usage examples | 1 | Keep public-facing and verify commands |
| Generate unit tests for a parser | 1 | Ensure tests assert behavior, not implementation quirks |
| Fix a null handling bug in one module | 2 | Require reproduction and regression test |
| Upgrade a minor dependency | 2 | Review lockfile and changelog |
| Add OAuth refresh handling | 3 | Auth-sensitive; require owner/security review |
| Change GitHub Actions deployment workflow | 3 | Release path risk |
| Rotate production database password | 4 | Human-led; agent may draft runbook only |
| Update iOS entitlements | 3 | Privacy/signing/store risk |
| Modify Android permissions | 3 | Runtime and store disclosure risk |
| Refactor KMP persistence layer | 2 or 3 | Tier depends on data sensitivity and migration risk |

## Mobile-specific escalation

Escalate mobile tasks when they touch:

- `Info.plist`
- iOS entitlements
- Privacy manifests
- Android `AndroidManifest.xml`
- Android permissions
- Network security config
- Keystores or signing configs
- Provisioning profiles or certificates
- CocoaPods, Gradle, or native dependency configuration
- React Native native modules
- KMP `expect`/`actual` boundaries
- Analytics, crash reporting, attribution, or telemetry SDKs

## Good enough versus production-grade

Good enough for low-risk experimentation:

- Human prompts agent with a small task
- Agent opens a diff
- Human reviews and runs local tests

Production-grade for real repositories:

- Task risk classification
- Written task contract for meaningful risk
- Sandboxed execution
- Scoped credentials
- Automated evidence from CI
- Security invariants documented
- Review checklist applied
- Rollback path known before merge
