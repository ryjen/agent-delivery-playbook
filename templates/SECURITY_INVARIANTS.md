# Security Invariants

Security invariants are rules that must remain true across agent-assisted and human-authored changes.

Agents should treat this file as a hard constraint. If a requested task conflicts with an invariant, stop and request human/security review.

## Authentication and authorization

- Authentication must not be bypassed for convenience
- Authorization checks must remain server-side where applicable
- Admin, support, or debug paths must not create hidden privilege escalation
- Session handling must remain consistent with current security design
- Token validation must not be weakened

## Secrets and credentials

- Secrets must not be committed to source control
- Secrets must not be copied into prompts, logs, test fixtures, screenshots, or generated documentation
- Production secrets must not be exposed to agent runtimes
- Long-lived personal tokens should not be used for automated agent workflows
- Signing keys, keystores, certificates, provisioning profiles, and store credentials require explicit human approval

## Data protection

- Sensitive data must not be logged in raw form
- PII handling must match product, legal, and privacy requirements
- Data retention behavior must not change silently
- Data deletion behavior must be explicit, tested, and reviewed
- Client-side persistence must use approved secure storage for tokens and sensitive user data

## Network security

- TLS validation must not be disabled
- Certificate validation must not be bypassed in production code
- Cleartext traffic must not be enabled broadly
- App Transport Security or Android Network Security Config exceptions require review
- Debug proxy or test-only networking changes must not leak into release builds

## Dependency and supply chain

- New dependencies require justification and review
- Lockfile changes must be visible and intentional
- Package provenance, maintenance, license, and vulnerability status must be considered
- Build scripts must not download or execute unpinned remote code without review
- Generated code must not include opaque or unverifiable blobs unless explicitly approved

## Build, release, and deployment

- CI/CD gates must not be weakened without explicit approval
- Release workflows must not be changed as part of unrelated tasks
- Deployment credentials must remain protected by environment controls
- Package publishing must require human-approved release flow
- Rollback or disablement paths must exist for risky production changes

## Logging, analytics, and telemetry

- Do not add tracking behavior without product/privacy approval
- Do not log tokens, credentials, precise location, payment data, health data, contact data, or private message content
- Debug logging must not ship in production builds
- Crash reporting changes must be reviewed for data capture impact

## Mobile/client invariants

React Native:

- Native module changes require explicit review
- Platform-specific behavior must be tested on affected platforms
- JavaScript changes must not assume identical iOS and Android behavior where native APIs differ

IOS:

- Entitlements must not change without review
- Privacy manifests and usage descriptions must be accurate
- Keychain accessibility must not be weakened
- App Transport Security exceptions require review

Android:

- Dangerous permissions require review
- Exported components require explicit intent and validation
- Network Security Config must not weaken production transport security
- Keystore and signing references must not be exposed

Kotlin Multiplatform:

- Security-sensitive `actual` implementations must preserve equivalent behavior across platforms
- Persistence and serialization changes must preserve compatibility
- Platform-specific secure storage must remain explicit

## Agent-specific invariants

- Agent output is not trusted until reviewed and tested
- Agent claims are not evidence unless backed by logs, commands, CI, or reproducible checks
- Agents must not self-approve changes
- Agents must not silently expand task scope
- Agents must not modify this file to make a task easier without explicit human/security approval
