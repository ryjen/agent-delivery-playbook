# Agent configuration regression evaluation (pilot profile)

**Status:** illustrative, non-normative, vendor-neutral guidance. This is not a second evidence envelope, agent test runner, or effect-authorization service.

A prompt, skill, model, tool contract, retrieval process, or verifier rubric is a **change to engineering behaviour**, even when no application source changes. Treat such changes as candidates for risk-proportionate *before/after* evaluations. Preserve the existing task-envelope, risk-tier, evidence, approval, and enforcement sources of truth.

## Minimal evaluation profile

Record the following for an actual evaluation run (with references to the authoritative records, not copied unrestricted evidence):

| Category | Record | Why |
| --- | --- | --- |
| Changed configuration | Baseline and candidate revision/digest for prompts/skills/model/runtime/tools/context/verifier; declared changed surfaces | Know what was changed and what must be requalified |
| Scope | Task families, risk tier, capability changes, excluded tasks | Avoid extrapolating from a narrow suite |
| Evaluation | Immutable dataset and test-oracle revision, verifier plan/rubric revision, materialization environment | Avoid silently changing the acceptance target |
| Exact subject | Candidate commit/artifact digest and accepted requirement revision | Prevent reuse of detached evidence |
| Trust | Producer/verifier identities, who controls oracle, remaining common trust roots | A different process/model does not by itself prove independence |
| Results | Per-case baseline/candidate result, missing cases, unsupported/infrastructure failure, evidence references | Make partial and failed evidence explicit |
| Disposition | Regression finding, accountable review/waiver reference where applicable, rollback plan | The evaluation never grants promotion authority |

For illustrative fixtures under [`examples/agent-regression/`](../examples/agent-regression/), all IDs prefixed `synthetic:` are **placeholders**, not cryptographic digests or real provenance. The local validator checks structure, exact reference agreement and a conservative *synthetic* classification; it does not execute a model, verify independence, attest an artifact, or grant any external effect.

## Risk-triggered evaluation selection

- **T1/T2, no new effects:** representative positive and negative cases, unchanged authority, captured deviations. A no-regression observation may proceed to ordinary review, not automatic merge.
- **T3/T4 or expanded permissions:** include protected/held-out tests with independently controlled oracles, explicit negative authorization/bypass cases, clean materialization and accountable human/policy disposition. A successful agent review is not a replacement for these.
- **Changed verifier rubric/dataset:** requalify the oracle or compare under explicitly versioned accepted requirements; do not compare unqualified scores across moving targets.
- **Unsupported or unavailable mandatory verifier:** preserve `indeterminate`, `unsupported`, or `infrastructure_failed` rather than silently passing or promoting.
- **Incident-derived failure:** add a bounded, sanitized recurrence fixture with an authoritative source reference and declared limits; do not invent incidents.

## Before/after regression disposition

| Observation | Synthetic classification | Operational interpretation |
| --- | --- | --- |
| Required candidate check fails, even if baseline also failed | `block` | Reject or repair candidate; record persistent baseline debt separately |
| No fails, but required evidence is indeterminate/unsupported/infrastructure-failed | `escalate` | Investigate; unresolved is not a pass |
| No failed or missing checks but T3/T4, expanded capability, or producer-writable oracle | `escalate` | Apply external policy, approvals and verifier trust requirements |
| All selected cases pass with unchanged low-risk capability | `no-regression-found` | Continue normal review; *not authorization or proof of broad correctness* |

An exception/waiver, if permitted at all, is **external**, recorded against the exact failed requirement, scope and authorization subject. Neither this table nor the fixture script can waive or approve anything. A code, policy or oracle change must not downgrade the accepted requirement to force a green result.

## Representative synthetic coverage

Two checked-in example bundles demonstrate the profile:

1. [Benign skill refinement](../examples/agent-regression/01-skill-guidance.json): ordinary code change and CI-triage cases stay green; no effect expansion; reviewer must still accept the actual change.
2. [Restricted tool/permission update](../examples/agent-regression/02-tool-permission-change.json): security/auth, prompt-injection, detached evidence, unavailable verifier, and approval-bypass cases include negative and indeterminate outcomes. A newly failing case blocks regardless of the general score.

These are **synthetic inputs testing the local classification contract**, not empirical agent benchmarks, protected verifier evidence, production logs, or proof of security.

Run the deterministic fixture/unit checks through the existing repository flake:

```sh
nix flake check --print-build-logs
```

Or locally, with the repository's configured Python:

```sh
python3 scripts/validate-agent-regression-fixtures.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The validator intentionally has no network access or write path to external systems.

## Evidence-qualified delivery measurements

Do not report a single composite "agent productivity" or "trust" score. Report numerator, denominator, observation period, source trust and missing-data coverage for each metric:

| Measure | Definition / caution |
| --- | --- |
| Qualified changes | Changed candidates admitted through the *applicable* evidence and approval gates / eligible candidates; distinguish T1–T4 |
| Rework | Candidates needing repair or re-review after a submitted evaluation / submitted candidates; don't confuse repeat iterations with escaped defects |
| Escaped defects | Independently confirmed post-admission defects in a declared window / admitted changes; disclose low sample sizes |
| False passes | Pass claims later contradicted by trusted reproduction / audited pass claims, with explicit scope |
| Abstention and unsupported rates | Non-answers, unsupported checks and infrastructure failures / attempts, broken down by cause |
| Reviewer effort | Observed review time per risk tier and decision; do not infer zero cost from agent completion |
| Rollback / recovery | Actual rollback count, recovery success and measured recovery time, with denominators |
| Evidence coverage | Required checks with current exact-subject qualifying evidence / required checks; stale or missing evidence counts as unqualified |
| Authorization-bypass findings | Confirmed reachable bypasses by inspected path and effect class; a zero without coverage is not evidence of absence |

Keep metrics disaggregated by task family, risk, environment, producer/verifier trust profiles, and period. Operational correlation is not causation. The synthetic fixture script emits **no production measurements**.

## Ownership

- This playbook owns the portable evaluation guidance, demonstration fixtures, and classification sanity check; [#77](https://github.com/ryjen/agent-delivery-playbook/issues/77).
- [Anthesis #199](https://github.com/hackelia-micrantha/anthesis/issues/199) decides evidence independence/sufficiency; [#139](https://github.com/hackelia-micrantha/anthesis/issues/139) owns provenance semantics.
- [Dubnium #896](https://github.com/ryjen/dubnium/issues/896) owns clean verification and [#1632](https://github.com/ryjen/dubnium/issues/1632) owns the read-only production-shaped evaluation pilot.
- [ops-cadence #19](https://github.com/ryjen/ops-cadence/issues/19) and [#44](https://github.com/ryjen/ops-cadence/issues/44) consume bounded, read-only results, never effect authority.
- Existing adversarial-governance fixtures remain under [`examples/adversarial/`](../examples/adversarial/) with their own evaluator. No duplicate generalized policy or authorization engine is introduced.

Further work (only with observed demand): external real-task evaluation adapters, trusted/verifier infrastructure, incident ingestion, periodic drift monitoring, calibrated judge/human concordance, and validated production metrics. This pilot alone cannot qualify those capabilities.
