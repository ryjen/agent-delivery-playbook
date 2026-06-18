# Golden Path Examples

Golden paths show how AI-assisted work should move from request to reviewable delivery evidence.

These examples are intentionally small. They are meant to become executable examples later.

## Path 1: Documentation Update

### Task

Update a README section for clarity.

### Risk Assessment

- Tier: T1
- Reason: documentation-only change
- Evidence: E1

### Agent Plan

- inspect README
- make localized edit
- ensure links still resolve syntactically
- summarize changes

### Execution Constraints

- no code changes
- no workflow changes
- no dependency changes

### Evidence

- diff only touches Markdown
- Markdown formatting reviewed

### Review

Lightweight review or auto-merge is acceptable if repository policy allows it.

### Outcome

Mergeable when the diff matches the envelope.

## Path 2: Local Bug Fix

### Task

Fix a localized null handling crash.

### Risk Assessment

- Tier: T2
- Reason: localized runtime behavior change
- Evidence: E2

### Agent Plan

- reproduce or identify failing path
- add regression test
- patch minimal logic
- run targeted tests

### Execution Constraints

- no API contract changes
- no dependency additions
- no broad refactor

### Evidence

- targeted regression test added
- relevant unit test command included
- assumptions documented if full suite is unavailable

### Review

Human review required.

### Outcome

Mergeable when tests and review support the change.

## Path 3: Cross-Cutting Feature

### Task

Add a feature touching API, storage, and UI behavior.

### Risk Assessment

- Tier: T3
- Reason: cross-cutting runtime behavior
- Evidence: E2 + E3

### Agent Plan

- identify affected contracts
- define migration or compatibility approach
- implement incrementally
- add tests at seams
- document rollout and rollback

### Execution Constraints

- no auth semantics changes
- no production data access
- no CI permission changes

### Evidence

- unit or integration tests
- smoke test plan
- migration or compatibility notes
- rollback path

### Review

Human review plus owner review for affected subsystem.

### Outcome

Mergeable when implementation, tests, and operational evidence agree.

## Path 4: Authentication or Authorization Change

### Task

Modify access-control behavior.

### Risk Assessment

- Tier: T4
- Reason: auth-sensitive change
- Evidence: E2 + E3 + E4

### Agent Plan

- stop until explicit approval is recorded
- identify security invariants
- add negative tests
- validate rollback
- request security review

### Execution Constraints

- no weakening validation
- no scope expansion without approval
- no secret access
- no workflow bypass

### Evidence

- approval record
- negative tests
- smoke validation
- rollback plan
- security review notes

### Review

Security review required.

### Outcome

Blocked until approval and evidence are complete.

## Path 5: Rejected Task

### Task

Disable authentication validation to make tests pass.

### Risk Assessment

- Tier: T4
- Reason: explicit security control removal

### Agent Decision

Reject the requested implementation path.

### Safer Alternative

- fix test fixture
- mock identity provider correctly
- document why validation must remain enabled

### Evidence

- original unsafe request
- policy reason for rejection
- proposed safe path

### Outcome

No code execution until a safe task envelope exists.
