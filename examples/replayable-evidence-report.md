# Replayable Evidence

## Task Reference

- Envelope: `examples/task-envelope/t1-doc-change.yaml`
- Risk tier: T1
- Required evidence levels: E1

## Change Reference

- PR: example documentation PR
- Repository: `example/app`
- Ref: `feature/readme-setup-docs`
- Exact commit: not recorded in this static example
- Artifact/result digest: not applicable
- Changed paths:
  - `README.md`

## Execution Identity and Authority

- Agent/tool: coding assistant operating through branch-only repository write access
- Human operator: repository maintainer
- Credential class: repository-scoped write token; no secrets or production credentials
- Approval boundary: human PR review before merge
- Prohibited actions avoided:
  - no package script edits
  - no CI edits
  - no dependency changes

## Context and Provenance

- Included context:
  - `README.md`
  - `package.json` scripts section
- Summarized context:
  - none
- Excluded context and reason:
  - `.github/workflows/**` excluded because CI changes were outside the T1 task
- Deferred context:
  - deployment docs not needed for setup command correction
- Escalated context and approval:
  - none
- Stale-context caveats:
  - README was treated as possibly stale; package scripts were treated as source of truth for commands

## Checks and Artifacts

| Check | Command/artifact | Evidence source / producer | Subject binding | Environment / run | Trust/binding properties | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Agent summary | "README commands match package scripts" | coding assistant | mutable branch only | agent session | unverified claim | Useful review hint; does not satisfy E1 by itself |
| Static review | manual diff comparison | human reviewer | changed paths on example PR; exact commit omitted in this static fixture | reviewer workstation | captured/manual observation; not independently reproducible from this fixture alone | Commands match `package.json` script names |
| Tests | not run | n/a | n/a | documentation-only | n/a | Not applicable; no runtime changes |
| CI | not available in example | n/a | n/a | n/a | missing evidence | Unverified |

## Manual Verification

Reviewer should compare the README commands against `package.json` before merge.

## Known Limits and Nondeterminism

- Full setup was not executed locally.
- CI status is not represented in this static example.
- The example intentionally omits an exact commit SHA, so its static-review evidence is **not exact-subject-bound**. A real merge decision that requires commit-bound evidence should record the reviewed commit or CI run.

## Unverified Claims

- End-to-end setup success is unverified.
- Package installation behavior is unverified.

## Rollback

Revert the README change.

## Evidence Trust Note

This example distinguishes an agent claim from a human observation. Neither is magically upgraded by appearing in an evidence report.

For a stronger example, protected CI that checks the exact PR commit would be **subject-bound trusted-runner evidence**. If a distinct reviewer independently repeated the check against that exact commit, that would additionally provide **independent verification**. Signing the CI result would add provenance/integrity properties but would not prove the README is semantically correct beyond the checks performed.

## Reviewer Notes

Confirm the change stayed documentation-only and did not modify scripts, dependencies, workflows, or release behavior.