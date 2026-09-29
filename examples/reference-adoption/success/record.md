# Successful Path Record — REF-T2-001

## Baseline

- Repository: `ryjen/agent-delivery-playbook`
- Base commit: `54b9cb7b5c0d29e5129415f5bfe24f1ca0f240d4`
- Reference project: `examples/reference-adoption/project/tag_normalizer.py`
- Characterized behavior before the task: trimming, lowercasing, and ordinary-space replacement.
- Defect: repeated spaces produce repeated hyphens and tab/mixed whitespace is not normalized consistently.

## Execution identity and authority

The candidate was prepared in an AI coding-assistant session using the connected GitHub repository surface.

The repository can observe branch commits attributed through GitHub, but it cannot independently authenticate the model/runtime identity from Git history. The capability grant therefore labels the runtime identity as **declared**, not verified.

The reference task grant is branch/path scoped and explicitly denies CI workflow, policy, dependency, merge, release, secret, and admin authority.

A limitation of this demonstration is that the surrounding chat/tool integration has broader orchestration abilities than the synthetic task grant can cryptographically enforce. The case study demonstrates the intended logical grant boundary; it does not claim credential-level mediation.

## Execution record

1. Read the merged baseline source and characterization tests.
2. Classified the change as T2: localized executable behavior change with regression-test evidence required.
3. Selected only the source file, existing test file, minimal adoption kernel, and evidence standard as material context.
4. Excluded CI workflow and policy files from the task.
5. Changed normalization from literal-space replacement to split/join whitespace normalization.
6. Added regression coverage for repeated and mixed whitespace.
7. Added the task, grant, and reference-adoption records.
8. Did **not** claim local test execution; independent repository CI is the required E2 evidence source.

## Candidate change

Expected behavior:

- `"  release   candidate  "` -> `"release-candidate"`
- `"release\tcandidate notes"` -> `"release-candidate-notes"`
- existing simple/already-normalized behavior remains unchanged.

No dependency, public API, CI, policy, release, or credential changes are part of this task.

## Evidence plan

Required coverage: E2.

Reproducible command:

```bash
python3 -m unittest tests.test_reference_project -v
```

Repository-wide independent validation:

```bash
nix flake check --print-build-logs
```

The final exact-head GitHub Actions run and merge commit cannot be embedded into the same commit without creating a self-reference loop. They are recorded externally on issue #42 after final exact-head validation/merge. The checked-in record remains bound to the exact base commit, task-envelope digest, named fixture paths, and candidate PR history.

## Review decision

The accountable maintainer explicitly instructed the assistant to proceed autonomously through review/fix/verify loops and merge green work.

Exact-head evidence for PR #72:

- candidate: `bbd274915ee25b873225707d386c7ca4909b3ff3`;
- CI run: `36524643542`;
- `Repository integrity`: passed;
- `Task envelopes`: passed;
- reference-project tests recorded by CI:
  - `test_collapses_repeated_whitespace ... ok`;
  - `test_normalizes_mixed_whitespace ... ok`;
  - `test_normalizes_simple_tag ... ok`;
  - `test_preserves_already_normalized_tag ... ok`.

The maintainer's instruction is accountable human delegation for this autonomous workflow, but repository evidence does **not** show a distinct human line-by-line diff reviewer. It is therefore not represented as independent E4 verification.

## Outcome

PR #72 was admitted after the exact-head checks passed and squash-merged as:

`24167d8883f27c8e17f77d2a331fc6cf9dd73924`

The public function signature and dependency set remained unchanged. The separately requested CI/merge authority expansion remained denied and produced no effect.
