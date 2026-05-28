# Architecture Notes

Use this file to give agents and reviewers enough system context to make safe changes without reading the entire repository.

## System purpose

Describe what the system does, who uses it, and what correctness means.

## Key boundaries

Document important boundaries:

- User interface
- API layer
- Domain logic
- Persistence
- Background jobs
- Third-party integrations
- Authentication and authorization
- Payment, privacy, or compliance-sensitive paths
- Build and release systems

## Trust boundaries

Describe where data or control crosses trust boundaries.

Examples:

- Client to backend
- Public API to internal service
- App to native platform API
- CI to deployment environment
- Build system to package registry
- Agent sandbox to repository

## Data model

Sketch the core data model, ownership, and sensitivity level.

| Entity | Owner | Sensitivity | Notes |
| --- | --- | --- | --- |
| ExampleUser | Auth/domain | PII | Do not log raw identifiers |

## Runtime model

Document:

- Deployment topology
- Process boundaries
- Background workers
- Queues/events
- Caches
- Offline behavior
- Failure/retry behavior

## Security model

Document:

- Authentication mechanism
- Authorization model
- Secret storage
- Token/session lifecycle
- Data protection requirements
- Audit/logging strategy
- Platform-specific security controls

## Mobile/client architecture

For client repositories, document:

- Supported platforms
- Shared versus platform-specific code
- Navigation/state management
- Persistence/offline model
- Networking stack
- Secure storage
- Analytics/crash reporting
- Native modules
- Signing/release flow

React Native notes:

- JS/native boundary
- Native module ownership
- Platform-specific code conventions

IOS notes:

- Keychain usage
- Entitlements
- Privacy manifests
- Background modes

Android notes:

- Manifest permissions
- Exported components
- Network Security Config
- Keystore/signing assumptions

Kotlin Multiplatform notes:

- Source set structure
- `expect`/`actual` boundaries
- Platform-specific persistence/networking

## Extension points

Document where new behavior should be added and where it should not.

Good agent guidance:

- Add new API clients under `src/integrations/`
- Add domain validation in `src/domain/validation/`
- Do not add business logic to controllers
- Do not change release workflows as part of feature work

## Known constraints

Examples:

- Legacy module must remain compatible until migration is complete
- API schema is consumed by mobile clients on older versions
- Database migration must support rollback window
- Mobile release cadence is slower than backend release cadence
- Some tests are flaky and should not be weakened without investigation

## Architecture decision process

Agents should not introduce architecture changes opportunistically.

Require human review or ADR when a change:

- Adds a framework
- Adds a runtime dependency
- Changes public API contracts
- Changes persistence or migration strategy
- Changes authentication, authorization, or privacy behavior
- Changes mobile platform permissions, entitlements, or signing
- Changes CI/CD or release flow
