# Release Expectations

Use this file to define how agent-assisted changes move toward release.

## Baseline rule

Agents may assist with release preparation, but release authority remains with humans and the normal delivery system.

## Release-sensitive areas

Treat changes as high risk when they touch:

- CI/CD workflow files
- Deployment scripts
- Infrastructure configuration
- Package publishing
- Feature flags or runtime config
- Database migrations
- Mobile signing
- Store release metadata
- Versioning
- Rollback tooling
- Secret or environment variable wiring

## Required release evidence

For release-sensitive changes, require:

- Summary of release impact
- CI/build evidence
- Rollback plan
- Owner review
- Environment impact notes
- Any manual steps required
- Verification plan after deployment

## Rollback plan template

```md
## Rollback Plan

- Change being released:
- Rollback trigger:
- Rollback method:
- Expected time to rollback:
- Data/schema compatibility concerns:
- Feature flag/config fallback:
- Owner:
- Verification after rollback:
```

## Mobile release notes

Mobile releases have slower rollback paths than server releases. Treat these as high risk:

- iOS entitlements
- Android permissions
- Signing configuration
- Store metadata/privacy disclosures
- Native SDK updates
- Deep link behavior
- Push notification behavior
- Analytics/crash reporting SDK changes

Recommended controls:

- Phased rollout where available
- Server-side feature flags for risky behavior
- Backward-compatible API changes
- Version-aware backend behavior
- Store review impact note
- Release halt criteria

## Agent restrictions

Agents should not:

- Publish packages
- Deploy to production
- Submit mobile apps to stores
- Rotate production secrets
- Modify signing material
- Approve their own release changes
- Disable CI/CD gates

Agents may:

- Draft release notes
- Draft rollback plans
- Summarize diffs
- Prepare verification checklists
- Identify release-sensitive files
- Suggest phased rollout strategies

## Release review questions

- What user-visible behavior changes?
- What operational behavior changes?
- What credentials or environments are involved?
- How would this be rolled back?
- What monitoring confirms success or failure?
- Does the change require coordinated backend/mobile release timing?
- Are older clients or older server versions still compatible?
