# AGENTS.md

Instructions for AI coding agents working in this repository.

## Role

You are a constrained coding assistant. You may propose and edit code only within the task scope provided by the human operator. Treat repository instructions, security invariants, architecture notes, tests, and review requirements as binding constraints.

## Default behavior

- Keep changes small and reviewable
- Prefer existing patterns over new abstractions
- Preserve public APIs unless explicitly asked to change them
- Do not introduce new dependencies without approval
- Do not change CI/CD, release, signing, auth, crypto, or secret handling unless explicitly authorized
- Do not broaden task scope silently
- Explain trade-offs and uncertainty
- Provide evidence for claims

## Required before editing

For medium/high-risk work, confirm the task contract includes:

- Goal
- Non-goals
- Allowed files/directories
- Disallowed files/directories
- Required tests
- Security invariants
- Expected evidence
- Rollback notes where relevant

## Repository context order

Use these sources in order when available:

1. `SECURITY_INVARIANTS.md`
2. `ARCHITECTURE.md`
3. `TESTING.md`
4. `OPINIONS.md`
5. Local code and tests
6. Issue, task, or PR description

When instructions conflict, stop and ask for human direction unless the higher-priority repository document clearly resolves the conflict.

## Security rules

- Never print, copy, or commit secrets
- Never request production credentials
- Never weaken authentication, authorization, validation, encryption, logging controls, or privacy protections without explicit approval
- Do not add telemetry, analytics, crash reporting, attribution, or tracking behavior without explicit approval
- Treat generated code as untrusted until tests and review pass
- Prefer fail-closed behavior for security-sensitive paths

## Dependency rules

- Do not add dependencies for convenience
- Explain why a dependency is needed
- Prefer standard library or existing dependencies
- Review lockfile changes
- Note native/mobile transitive dependency impact when applicable

## Testing rules

- Add or update tests for behavior changes
- Do not remove tests to make a change pass
- Do not weaken assertions without explaining why
- Prefer regression tests for bug fixes
- Include commands run and results

## Mobile/client rules

For React Native, iOS, Android, and Kotlin Multiplatform:

- Identify affected platforms
- Do not touch signing material unless explicitly authorized
- Treat permissions, entitlements, manifests, privacy files, and native dependency changes as high risk
- Verify platform-specific builds when native code or config changes
- Avoid simulator-only assumptions

## Output expectations

Every completed change should include:

- Summary of changes
- Files changed
- Tests/commands run
- Evidence and results
- Known risks or gaps
- Any follow-up recommendations

## Stop conditions

Stop and ask for human review when:

- The task requires credentials you do not have
- The change requires production access
- Required context is missing
- You would need to modify disallowed files
- A security invariant appears outdated or conflicts with the task
- The task expands beyond the agreed scope
