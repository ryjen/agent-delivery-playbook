# Golden Path Examples

Golden paths show how AI-assisted work should move from request to task envelope to evidence to reviewable outcome.

These examples are intentionally small. The full task bundles live under `examples/golden-path/`.

## Full Task Bundles

| Bundle | Risk | Purpose |
| --- | --- | --- |
| `examples/golden-path/01-doc-update/` | T1 | Lightweight documentation-only flow |
| `examples/golden-path/02-bugfix/` | T2 | Localized bugfix with targeted test evidence |
| `examples/golden-path/03-t4-auth-change/` | T4 | Controlled sensitive change blocked until approval and review |
| `examples/golden-path/04-rejected-task/` | T4 | Unsafe request where refusal/escalation is the correct outcome |

Each bundle includes:

- `task-envelope.yaml`
- `evidence-report.md`
- `reviewer-note.md`
- `outcome.md`

Use these with:

- `docs/task-risk-matrix.md` for risk classification;
- `docs/agent-task-envelope.md` for envelope shape;
- `docs/context-budget-and-provenance.md` for context decisions;
- `docs/delivery-evidence-standard.md` for evidence levels;
- `docs/replayable-evidence-envelope.md` for audit-oriented PR evidence.

## Path 1: Documentation Update

Documentation-only changes should stay lightweight. The task envelope can be brief when the diff is clearly T1 and no sensitive paths are touched.

Constrained behavior:

- inspect approved docs and source-of-truth files only;
- do not modify scripts, dependencies, workflows, or runtime behavior;
- report unverified setup claims instead of implying full execution.

## Path 2: Local Bug Fix

Localized runtime changes need targeted test evidence and human review. The example bundle shows regression coverage without broad refactoring.

Constrained behavior:

- patch only the affected module;
- add targeted tests;
- avoid public API, dependency, and CI changes unless reclassified.

## Path 3: Sensitive Change

Sensitive control-surface changes are not fast paths. The example bundle shows approval, owner review, negative checks, and rollback expectations before completion.

Constrained behavior:

- require explicit approval before sensitive-path edits;
- require independent review;
- document rollback and residual risk.

## Path 4: Rejected Task

Some tasks should not be implemented. The rejected-task bundle shows how to stop, record the policy reason, and propose a safer bounded task instead.

Constrained behavior:

- refuse unsafe authority expansion;
- preserve the rejection rationale;
- propose decomposition or escalation rather than silently complying.