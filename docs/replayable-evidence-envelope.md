# Replayable Evidence Envelope

A replayable evidence envelope is the audit-oriented record for an agent-assisted PR. It is more specific than a PR summary: it should let a reviewer reconstruct what was authorized, what changed, what was checked, what was not checked, and who approved the result.

## Mental model

```mermaid
flowchart LR
  Task[Task envelope] --> Work[Agent-assisted work]
  Work --> Diff[PR diff]
  Work --> Checks[Checks and artifacts]
  Work --> Limits[Known limits]
  Diff --> Replay[Replayable evidence]
  Checks --> Replay
  Limits --> Replay
  Replay --> Review[Human review]
```

The envelope does not make the work deterministic. It makes nondeterminism, missing context, tool limits, and unsupported claims visible.

## Minimum fields

| Field | Purpose |
| --- | --- |
| Task envelope reference | The task contract that authorized the work |
| PR/change reference | The branch, PR, commit, or patch being reviewed |
| Actor/tool identity | Agent, model, tool, workflow, or human identity where known |
| Authority linkage | Tool permissions and approval boundary used for execution |
| Allowed/prohibited scope | Scope actually used compared with the envelope |
| Changed paths | Files or directories changed |
| Commands/checks run | Exact commands, scope, and result |
| Evidence source / producer | Who or what produced each result and whether it is the same actor that produced the candidate |
| Subject binding | Repository, exact commit/ref, artifact digest, external-state revision, or other immutable subject identity |
| Environment / runner | Relevant execution environment or verifier identity |
| Run / timestamp | Run identifier and time when freshness or auditability matters |
| Integrity / independence | Attestation/signature reference and producer/verifier independence where required |
| CI/artifact links | CI runs, logs, screenshots, reports, or generated artifacts |
| Context/provenance summary | Included, excluded, summarized, deferred, or escalated context |
| Manual verification | Human checks performed outside automation |
| Known nondeterminism | Model variability, generated output, flaky tests, unavailable environment |
| Unverified claims | Claims that were not proven, marked explicitly |
| Rollback path | How to revert, disable, or recover |
| Approval/review linkage | Reviewers, owners, or approvals required before merge |

## Markdown template

```markdown
# Replayable Evidence

## Task Reference

- Envelope:
- Risk tier:
- Required evidence levels:

## Change Reference

- PR:
- Repository:
- Ref:
- Exact commit:
- Artifact/result digest, if applicable:
- Changed paths:

## Execution Identity and Authority

- Agent/tool:
- Human operator:
- Credential class:
- Approval boundary:
- Prohibited actions avoided:

## Context and Provenance

- Included context:
- Summarized context:
- Excluded context and reason:
- Deferred context:
- Escalated context and approval:
- Stale-context caveats:

## Checks and Artifacts

| Check | Command/artifact | Evidence source / producer | Subject binding | Environment / run | Trust/binding properties | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Static review |  |  |  |  |  |  |
| Tests |  |  |  |  |  |  |
| CI |  |  |  |  |  |  |

## Manual Verification

## Known Limits and Nondeterminism

## Unverified Claims

Unsupported claims must be marked as unverified. Do not hide them by omission.

## Rollback

## Reviewer Notes
```

## Evidence quality rules

- Record what actually happened, not what the agent intended.
- Prefer exact commands, paths, commit SHAs, artifact digests, run IDs, and CI links over summaries.
- State who/what produced the evidence and which exact subject it evaluates.
- Do not treat a branch name or mutable artifact pointer as exact subject binding.
- Mark missing checks as missing with a reason.
- Mark unsupported claims as `unverified` instead of deleting them.
- For T3 work, prefer protected subject-bound CI/trusted-runner evidence over self-reported local output when the property is independently verifiable.
- For T4 work, self-report cannot satisfy an independent-verification requirement; restricted execution remains human-led.
- Attestation/integrity evidence proves only the bound provenance/integrity predicates, not semantic correctness or authorization.
- Include rollback and required independent verification evidence for T3/T4 work.

## When this is required

| Risk | Expectation |
| --- | --- |
| T1 | PR evidence may be enough when the change is documentation-only and small |
| T2 | Include replay fields for task reference, changed paths, checks, and limits |
| T3 | Include operational evidence, rollback, and context/provenance decisions |
| T4 | Include independent review/approval linkage and explicit authority boundaries |

## Non-goals

This is not an immutable audit log, external evidence store, or runtime trace format. It is a lightweight PR evidence shape that can later be promoted into stronger tooling.