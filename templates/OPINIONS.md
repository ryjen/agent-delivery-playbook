# Engineering Opinions

This file captures repository-specific preferences that agents and humans should follow unless a task explicitly overrides them.

## Purpose

Opinions reduce ambiguity. They prevent agents from inventing local conventions, introducing unnecessary frameworks, or optimizing for generic tutorial patterns instead of this codebase.

## Default engineering stance

- Prefer simple, explicit code over clever abstractions
- Prefer boring dependencies over novel ones
- Prefer small diffs over broad rewrites
- Prefer tests that describe behavior over implementation detail
- Prefer compatibility and rollback over perfect cleanup
- Prefer existing architecture unless an intentional design change is approved

## Code style

Document project-specific choices here:

- Language versions
- Formatting tools
- Naming conventions
- Error handling style
- Logging style
- API design conventions
- Module boundaries
- Dependency injection approach
- Concurrency model

## Architecture preferences

Examples:

- Keep domain logic out of UI controllers
- Keep network models separate from persistence models
- Avoid business logic in build scripts
- Keep generated code isolated
- Prefer explicit adapters at trust boundaries
- Use feature flags for risky behavior changes

## Security preferences

Examples:

- Fail closed on authorization uncertainty
- Validate input at trust boundaries
- Avoid logging raw request/response bodies containing user data
- Do not persist tokens outside approved secure storage
- Do not weaken TLS, certificate, or network security behavior for convenience
- Keep secrets out of source, tests, prompts, and logs

## Mobile/client preferences

React Native:

- Keep native changes explicit and reviewed separately
- Avoid adding native modules unless justified
- Verify both iOS and Android when shared JS changes can affect platform behavior

IOS:

- Treat entitlement and privacy manifest changes as high risk
- Avoid broad App Transport Security exceptions
- Keep keychain behavior explicit

Android:

- Treat manifest permissions and exported components as high risk
- Avoid broad cleartext traffic exceptions
- Review R8/ProGuard keep rules carefully

Kotlin Multiplatform:

- Keep platform-specific behavior visible at `expect`/`actual` boundaries
- Avoid assuming JVM semantics in common code
- Test serialization and persistence migrations per platform

## Dependency preferences

- Use existing dependencies before adding new ones
- Require approval for new runtime dependencies
- Explain transitive dependency impact
- Avoid abandoned packages
- Prefer packages with clear maintenance, licensing, and security posture

## Testing preferences

- Add regression tests for bug fixes
- Keep integration tests close to real boundaries
- Do not over-mock security-sensitive behavior
- Prefer deterministic tests over sleeps/timeouts
- Include platform-specific tests for mobile config/native changes

## Change management preferences

- Use small, reviewable commits
- Separate mechanical refactors from behavior changes
- Separate dependency updates from feature work when practical
- Document rollback for medium/high-risk changes
- Add ADRs for intentional architecture changes
