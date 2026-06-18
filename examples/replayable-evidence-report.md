# Replayable Evidence

## Task Reference

- Envelope: `examples/task-envelope/t1-doc-change.yaml`
- Risk tier: T1
- Required evidence levels: E1

## Change Reference

- PR: example documentation PR
- Branch/commit: `feature/readme-setup-docs`
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

| Check | Command or artifact | Scope | Result |
| --- | --- | --- | --- |
| Static review | manual diff review | README setup section | Commands match `package.json` script names |
| Tests | not run | documentation-only | Not applicable; no runtime changes |
| CI | not available in example | n/a | Unverified |

## Manual Verification

Reviewer should compare the README commands against `package.json` before merge.

## Known Limits and Nondeterminism

- Full setup was not executed locally.
- CI status is not represented in this static example.

## Unverified Claims

- End-to-end setup success is unverified.
- Package installation behavior is unverified.

## Rollback

Revert the README change.

## Reviewer Notes

Confirm the change stayed documentation-only and did not modify scripts, dependencies, workflows, or release behavior.