# Standalone Reference Adoption

This directory is a publicly inspectable, self-contained adoption of the playbook against a tiny dependency-free Python project.

It is intentionally representative rather than production-facing. The project can be built/tested locally with Python/Nix; GitHub Actions is used by this repository to produce independent CI evidence but is not required to reproduce the software tests.

## Baseline

The reference project baseline was established and merged in PR #71 at:

`54b9cb7b5c0d29e5129415f5bfe24f1ca0f240d4`

The baseline contains a small tag normalizer and basic characterization tests.

## Successful bounded task

Task: `success/task-envelope.yaml` (`REF-T2-001`).

Goal: fix repeated/mixed-whitespace normalization without changing the public function signature or dependencies.

Artifacts:

- task envelope;
- scoped capability grant;
- execution/evidence/review/outcome record;
- candidate source diff;
- regression tests;
- independently attributable repository CI, recorded externally on #42 after exact-head validation.

The success path deliberately does not require capability catalogs, attestations, tool-decision records, or a separate provenance service. The task envelope plus grant/evidence record are sufficient for this small T2 demonstration.

## Rejected authority-expansion task

Task: `rejected/task-envelope.yaml` (`REF-T3-REJECT-001`).

The candidate requests workflow-write/permission and merge authority so it can admit itself. The request is rejected before mutation and linked to the existing adversarial controls.

## Practical measures

| Signal | Observed result |
| --- | --- |
| Baseline/setup | Separate merged baseline PR #71; exact base commit recorded |
| Successful-task governance artifacts | task envelope + task grant + consolidated record |
| Rejected-task governance artifacts | task envelope + denied grant request + consolidated rejection record |
| Reviewer time | Not reliably measured by the repository/tooling; intentionally not estimated |
| Agent local test time | Not applicable; the agent record does not claim local shell execution |
| Validation failures caught | 0 candidate CI failures; 2 new regression cases cover repeated/mixed whitespace that the baseline test set did not cover. The baseline was not retroactively rerun with the new tests. |
| False-positive/unnecessary-control rate | No false-positive is claimed from a sample of two paths; sample is too small to generalize |
| Missing-context escalations | 0 on the bounded T2 path |
| Authority escalations/rejections | 1 rejected self-modifying/merge-authority request |
| Independent reproducibility | Python unittest + Nix flake commands are local/reproducible without proprietary agent services |
| Independent CI evidence | PR #72 head `bbd274915ee25b873225707d386c7ca4909b3ff3`, run `36524643542`: `Repository integrity` and `Task envelopes` both passed; the log records all four reference-project tests as `ok` |
| Production adoption evidence | None; this is a standalone representative adoption, not production usage |

## Friction and findings

### Exact-head evidence is externally anchored

A commit cannot contain its own eventual commit SHA. Storing exact final PR-head/run identity inside the same changing commit creates a self-reference loop.

The practical pattern is:

1. checked-in evidence binds task ID/digest, exact base commit, paths/artifacts, commands, and declared producer;
2. protected CI binds results to the actual candidate SHA;
3. the PR/issue/merge record preserves that external exact-head binding.

This is consistent with the evidence standard's artifact/result-digest option and should remain explicit in adoption guidance.

### Inspectable case studies create more files than ordinary T2 work

This reference intentionally separates task and grant records so readers can inspect boundaries. A normal small T2 repository may represent the same concerns in issue/PR fields plus branch permissions.

The case study should not be copied as a minimum mandatory file set.

### Identity separation is only partially demonstrated

Repository history can attribute mutations to GitHub identities and CI runs, but it cannot independently prove the model identity behind this chat/tool execution. The case study therefore treats model/runtime identity as declared.

Similarly, the surrounding integration may expose broader orchestration authority than the synthetic task grant. This case study demonstrates the **playbook contract**, not a cryptographic runtime capability system.

### Rollout guidance needed alignment

Applying the current minimal kernel revealed that the older rollout guide still suggested task envelopes for all AI-assisted work and approval gates for T4 tool use. That predates the risk-shaped kernel and human-led T4 boundary.

The finalization change updates the rollout guide: T1 may remain inline/lightweight, structured envelopes are the normal T2+ path, sensitive T3 tool effects use explicit approval where policy requires it, and restricted T4 effects remain human-led.

## Limitations

- One tiny project cannot establish broad usability or false-positive rates.
- No production credentials, data, release, or infrastructure are involved.
- No proprietary agent runtime is required to reproduce the reference project/tests.
- GitHub Actions provides this repository's independent CI record, but local Nix/Python commands reproduce the technical checks.
- Independent human diff-review identity is not demonstrated by repository evidence in this autonomous workflow; the accountable user's instruction to proceed is recorded as delegation, not upgraded into an E4 claim.

## Completion

The successful bounded task was merged via PR #72:

- base commit: `54b9cb7b5c0d29e5129415f5bfe24f1ca0f240d4`;
- candidate head: `bbd274915ee25b873225707d386c7ca4909b3ff3`;
- independent CI run: `36524643542`;
- merged outcome: `24167d8883f27c8e17f77d2a331fc6cf9dd73924`.

The rejected authority-expansion path produced no workflow, permission, ruleset, merge-policy, or release mutation.

This demonstrates one **representative standalone adoption**, not production adoption or runtime capability enforcement.
