# Testing Expectations

This file defines how agents and humans should prove that a change works.

## Baseline rule

A change is not correct because the agent says it is correct. Correctness needs evidence from tests, builds, static analysis, manual verification, or reviewable reasoning.

## Required evidence by change type

| Change type | Minimum evidence |
| --- | --- |
| Documentation only | Links or paths checked, no code execution required |
| Test-only change | Test command output or explanation if not run |
| Bug fix | Failing case or reproduction, regression test, passing test output |
| Feature work | Unit/integration tests, relevant manual verification |
| Refactor | Existing tests pass, no intentional behavior change noted |
| Dependency update | Build/test output, lockfile review, vulnerability/license scan if available |
| Security-sensitive change | Negative tests, security review notes, invariant mapping |
| Mobile native/config change | Affected platform build evidence and config diff review |

## Commands

Document project-specific commands here.

```sh
# Format

# Lint

# Unit tests

# Integration tests

# Type checks

# Build

# Security scan
```

## Test quality rules

- Prefer behavior tests over implementation-detail assertions
- Add regression tests for bug fixes
- Do not delete or weaken tests to make a change pass
- Avoid excessive mocking at trust boundaries
- Include negative tests for validation, authorization, and error handling
- Keep tests deterministic
- Avoid sleeps/timeouts unless unavoidable
- Explain any skipped tests

## Agent-specific rules

Agents must report:

- Commands run
- Command results
- Tests not run and why
- Any failures observed
- Whether failures appear related to the change
- Manual checks performed

Agent claims without command output, CI links, or reproducible instructions should be treated as unverified.

## Mobile testing

React Native:

- Run JavaScript/TypeScript tests where relevant
- Verify native builds when dependencies or native modules change
- Check both iOS and Android for shared behavior changes where practical

IOS:

- Build affected schemes
- Run unit/UI tests where available
- Review simulator versus device assumptions
- Check entitlements, privacy manifests, and `Info.plist` diffs

Android:

- Run Gradle build/test tasks
- Review manifest, permissions, exported components, and network config
- Check R8/ProGuard changes when release behavior is affected

Kotlin Multiplatform:

- Run common tests
- Run platform-specific tests for affected source sets
- Verify serialization, persistence, and coroutine behavior across platforms where relevant

## When tests are unavailable

If a project lacks tests, the agent should not pretend otherwise.

Use fallback evidence:

- Reproduction steps
- Manual verification notes
- Static analysis
- Build output
- Small reviewable diff
- Explicit recommendation for missing tests

For production-sensitive changes, missing tests should increase risk tier and review requirements.
