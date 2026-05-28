# Mobile Agent-Safe Checklist

Mobile/client repositories need extra care because small configuration changes can alter privacy posture, release behavior, platform compatibility, or store review outcomes.

Use this checklist before merging agent-assisted changes in React Native, iOS, Android, or Kotlin Multiplatform repositories.

## Universal mobile checks

- [ ] Task scope identifies affected platforms: iOS, Android, shared, backend contract, or tooling
- [ ] Agent did not receive production signing credentials, provisioning profiles, keystores, or store credentials
- [ ] Build files were reviewed separately from source changes
- [ ] Dependency and lockfile changes are intentional
- [ ] Runtime permissions and privacy disclosures were checked
- [ ] Analytics, crash reporting, attribution, and telemetry changes were reviewed for PII risk
- [ ] Network/security configuration changes were reviewed
- [ ] Offline behavior and retry behavior were considered where relevant
- [ ] Platform-specific tests or builds were run for affected platforms
- [ ] Rollback path is known for released code

## React Native

Check files and areas such as:

- `package.json`
- `yarn.lock`, `package-lock.json`, or `pnpm-lock.yaml`
- Metro config
- Babel config
- Native module bindings
- `ios/` and `android/` subtrees
- Expo config where applicable

Review questions:

- [ ] Did the agent change JavaScript only, or did it also touch native projects?
- [ ] Did a dependency introduce native code?
- [ ] Were bridge boundaries, threading, and lifecycle behavior considered?
- [ ] Are platform-specific code paths tested or guarded?
- [ ] Did the change affect app startup, bundle size, or offline behavior?
- [ ] Did the change add logging of tokens, user identifiers, location, health, payment, or contact data?

Failure modes:

- JS change compiles but native build fails
- Native dependency changes permissions or SDK behavior
- Agent fixes Android and silently breaks iOS
- Generated tests mock away the real bridge behavior
- Metro/Babel changes alter production bundle behavior

## iOS

Check files and areas such as:

- `Info.plist`
- `.entitlements`
- Privacy manifests
- `Podfile` and `Podfile.lock`
- Swift Package Manager configuration
- Keychain usage
- App Transport Security
- URL schemes and universal links
- Background modes
- Push notification configuration
- Build settings and signing configuration

Review questions:

- [ ] Did entitlements change?
- [ ] Did privacy manifests or data usage descriptions change?
- [ ] Did App Transport Security become weaker?
- [ ] Did keychain accessibility or access group behavior change?
- [ ] Did URL scheme handling introduce interception or spoofing risk?
- [ ] Did the change affect background execution, notifications, or location behavior?
- [ ] Were simulator-only assumptions avoided?

Failure modes:

- Debug signing or development team settings leak into repo
- ATS exceptions become broader than intended
- Keychain data becomes accessible in weaker device states
- Privacy strings are added without product/legal review
- Pod update pulls transitive native SDK changes

## Android

Check files and areas such as:

- `AndroidManifest.xml`
- Gradle files
- Version catalogs
- `proguard-rules.pro` / R8 config
- Network Security Config
- Keystore references
- Play Integrity / SafetyNet integration
- Background workers and services
- Exported activities, services, receivers, and providers
- Deep links / app links

Review questions:

- [ ] Did permissions change?
- [ ] Did exported components change?
- [ ] Did network security config become weaker?
- [ ] Did min/target SDK changes alter runtime behavior?
- [ ] Did ProGuard/R8 rules weaken obfuscation or keep too much code?
- [ ] Did background work introduce battery or privacy issues?
- [ ] Did the change affect deep link verification or intent handling?

Failure modes:

- `android:exported="true"` added without validation
- Cleartext traffic enabled broadly
- Dangerous permissions added for convenience
- R8 keep rules expose sensitive implementation
- Background work drains battery or violates platform policy

## Kotlin Multiplatform

Check files and areas such as:

- Shared source sets
- `expect` / `actual` implementations
- Platform-specific persistence
- Platform-specific networking
- Coroutine dispatching
- Serialization
- Native interop
- Gradle KMP configuration

Review questions:

- [ ] Did the agent preserve platform boundaries?
- [ ] Are `actual` implementations equivalent where security matters?
- [ ] Are threading and coroutine dispatchers appropriate per platform?
- [ ] Does shared code assume JVM behavior on Native or iOS?
- [ ] Are serialization changes backward compatible?
- [ ] Are migrations tested on each affected platform?

Failure modes:

- Shared code hides platform-specific security differences
- JVM-only assumptions break iOS/native behavior
- Persistence migration works on Android but corrupts iOS data
- Coroutine context leaks UI work onto the wrong thread

## Mobile evidence expectations

For low-risk changes:

- Relevant unit tests
- Build for affected platform if code changed
- Short manual verification note

For medium-risk changes:

- iOS and/or Android build evidence
- Unit/integration tests
- Dependency/lockfile review
- Platform-specific risk notes

For high-risk changes:

- Full affected-platform build matrix
- Security or mobile owner review
- Permission/entitlement/privacy manifest diff
- Rollback or release halt plan
- Store/release impact note where relevant

## Merge blockers

Block merge when:

- Agent changed signing or release credentials
- Production secrets are present in prompt, diff, logs, or fixtures
- Mobile permissions changed without explicit approval
- Entitlements changed without platform owner review
- Dependency changes are unexplained
- Tests only prove mocks, not platform behavior
- Rollback is unknown for release-sensitive code
