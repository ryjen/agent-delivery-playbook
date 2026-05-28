# Release Expectations

Use this file to define how agent-assisted changes move toward release.

## Baseline rule

Agent-assisted changes must follow the same release controls as human-authored changes. Agents may help prepare release notes, verification steps, and rollback plans, but they should not bypass human approval or protected release systems.

## Release risk classification

| Change type | Release risk | Notes |
| --- | --- | --- |
| Documentation only | Low | No runtime impact |
| Test-only change | Low | Confirm no production files changed |
| Internal refactor | Medium | Confirm behavior did not change |
| User-facing feature | Medium | Require product/owner approval where applicable |
| Dependency update | Medium/High | Depends on runtime, native, and transitive impact |
| Auth/security/privacy change | High | Requires security review |
| CI/CD or deployment change | High | Requires platform/release review |
| Mobile signing, entitlements, permissions, or store config | High | Requires mobile release owner review |
| Production credential or destructive data operation | Restricted | Human-led only |

## Pre-release checklist

- [ ] Scope matches the approved task
- [ ] Required tests passed
- [ ] Security invariants preserved
- [ ] Dependency changes reviewed
- [ ] CI/CD changes reviewed by platform owner
- [ ] Mobile config/signing/privacy changes reviewed by mobile owner
- [ ] Rollback path documented for medium/high-risk changes
- [ ] Monitoring or validation plan exists for risky changes
- [ ] Release notes mention relevant user-facing or operational impact

## Evidence required

For each release candidate, capture:

- Commit or PR reference
- Tests and builds run
- CI results
- Manual verification notes
- Security review notes where applicable
- Dependency scan results where applicable
- Known risks
- Rollback procedure

## Rollback patterns

Prefer rollback mechanisms that are boring and rehearsed:

- Revert commit
- Disable feature flag
- Roll back deployment artifact
- Re-pin dependency
- Disable config remotely
- Halt phased mobile rollout
- Ship hotfix build only when necessary

## Mobile release considerations

React Native:

- Confirm whether the change ships over app release, OTA update, or both
- Review native dependency changes separately from JS changes
- Avoid OTA delivery for changes that assume native code not present in installed builds

IOS:

- Review provisioning, entitlements, privacy manifests, and App Store disclosure impact
- Confirm release build signs with approved credentials
- Consider phased release and halt strategy

Android:

- Review manifest permissions, exported components, Play Integrity, signing config, and Play Store disclosure impact
- Confirm release build uses approved signing flow
- Consider staged rollout and halt strategy

Kotlin Multiplatform:

- Verify platform-specific artifacts where shared code changes behavior
- Confirm persistence/serialization compatibility before release

## Agent boundaries

Agents may:

- Draft release notes
- Draft rollback plans
- Summarize verification evidence
- Identify changed release-sensitive files
- Prepare checklists for human execution

Agents should not:

- Submit production releases without explicit human approval
- Access signing keys or store credentials by default
- Rotate production secrets
- Modify protected release workflows as part of unrelated tasks
- Self-certify release readiness
