# Agent-Assisted Review Checklist

Use this checklist when reviewing agent-assisted changes.

## Scope control

- [ ] The diff matches the approved task
- [ ] No unrelated files were changed
- [ ] No opportunistic rewrites were introduced
- [ ] Public APIs or contracts changed only when explicitly intended
- [ ] Generated code, if any, is isolated and understandable

## Security review

- [ ] Authentication and authorization behavior were not weakened
- [ ] Input validation and error handling remain appropriate
- [ ] Secrets were not added to source, tests, logs, prompts, or fixtures
- [ ] Sensitive data is not logged or exposed
- [ ] TLS/network security behavior was not weakened
- [ ] Dependency changes were intentional and reviewed
- [ ] Security invariants still hold

## Evidence review

- [ ] Agent provided commands run and results
- [ ] CI or local test evidence exists
- [ ] Tests prove behavior rather than mocks only
- [ ] Any skipped tests are explained
- [ ] Failures are documented and understood
- [ ] Manual verification is documented where relevant

## Maintainability review

- [ ] Change follows existing architecture
- [ ] Code is readable without trusting the agent explanation
- [ ] Error handling is explicit
- [ ] Logging is useful and safe
- [ ] New abstractions are justified
- [ ] No unnecessary dependencies were added

## Mobile/client review

- [ ] Affected platforms are identified
- [ ] React Native native module changes are explicit
- [ ] iOS entitlements, privacy manifests, and `Info.plist` changes are reviewed
- [ ] Android manifest, permissions, exported components, and network config are reviewed
- [ ] Kotlin Multiplatform `expect`/`actual` behavior remains equivalent where security-sensitive
- [ ] Signing material and release credentials were not exposed
- [ ] Platform builds/tests were run where relevant

## Release review

- [ ] Rollback path is documented for medium/high-risk changes
- [ ] Feature flags or kill switches are used where appropriate
- [ ] CI/CD or deployment changes received platform owner review
- [ ] Release notes or operator notes are updated when needed
- [ ] Monitoring or validation plan exists for risky changes

## Reviewer stance

Review the change as untrusted code from a fast external contributor. Do not accept agent claims as evidence unless they are backed by reproducible commands, CI output, tests, or direct inspection.
