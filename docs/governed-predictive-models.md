# Governed Predictive and Decision Models (optional guidance)

**Status:** exploratory/advisory; issue [#74](https://github.com/ryjen/agent-delivery-playbook/issues/74). This is **not** a required architecture, machine-learning service, authority engine, new task-envelope schema, or proof of a deployed model. A deterministic non-ML solution is a valid final design decision.

Predictive or decision models may assist agent delivery by *estimating* outcomes, anomaly likelihood, cost, resource demand, regression risk, or the next likely state. They must not decide their own permissions, mint capabilities, change required controls, bypass [GitHub admission](operations/main-admission.md), or make a protected effect authoritative.

## Required lifecycle placement

```text
typed observed state and source provenance
  -> deterministic rule/baseline (record expected outcome)
  -> optional learned prediction or recommendation (can abstain)
  -> typed advisory result + uncertainty + provenance + expiry
  -> deterministic policy/evidence sufficiency + accountable review
  -> separately authorized and bounded execution, if allowed
  -> observed effect/outcome + rollback/recovery
  -> independent evaluation, drift monitoring and calibration
```

The existing [task envelope](agent-task-envelope.md), [risk matrix](task-risk-matrix.md), [evidence standard](delivery-evidence-standard.md), [trust model](trust-model.md), and [identity/grant rules](identity-delegation-and-capability-grants.md) stay authoritative. A model is a **candidate source of context and claims**, not a control plane. Applying an action requires an independently established grant and any approval/CI/release gates applicable to its risk.

## Pick the simplest warranted model

| Candidate method | Appropriate question | Important limitation |
| --- | --- | --- |
| Rule or deterministic baseline | Does a known predicate, counter, guardrail, threshold, or run status already decide this? | Requires current inputs, correct policy, and tests; often sufficient |
| Bounded decision model | Given current approved features, estimate a score, label, ranking, or risk on a fixed choice set | Scores are not approvals; spurious correlation and dataset shift remain |
| Transition/predictive state model | Given prior state (and action when appropriate), predict likely subsequent state over a stated horizon | Multi-step rollout can compound error; observational prediction is not necessarily causal effect |
| Representation-space / JEPA-style predictor | Predict a learned target representation from contextual representations, potentially including temporal features | A latent-space match is not a calibrated operational probability or permission to act; requires a validated downstream task and uncertainty evaluation |

JEPA here refers to *joint-embedding predictive architecture*, exemplified by [I-JEPA (Assran et al., CVPR 2023)](https://openaccess.thecvf.com/content/CVPR2023/html/Assran_Self-Supervised_Learning_From_Images_With_a_Joint-Embedding_Predictive_Architecture_CVPR_2023_paper.html). JEPA is **not** the canonical model family for governed delivery. A representation predictor does not automatically establish action-conditioned dynamics, calibrated probability, or improved operational decisions.

## QART-style decision checklist: is ML actually warranted?

Complete this short **question, alternatives, risks, tests** record before selecting a learned component. The decision itself should be stored in an issue, design note or ADR when material; no new universal artifact is required.

- **Question / target:** What exact decision/forecast and operational horizon are valuable? Which stakeholder can use it, and what would acting on a wrong result cost?
- **Alternatives / baseline:** What simple thresholds, existing logs, deterministic tests, queue models, statistics, or manual review solve it? Is there an independently labeled outcome to predict?
- **Readiness / data:** Are there enough representative events and labels? Are definitions stable across versions, repositories, services, tenants, and time? Is use/retention permissible?
- **Threats / authority:** Could training/feature input be poisoned, sensitive, policy-derived, leaked across tenants, or influence a protected tool/effect? Who owns the oracle and approval path?
- **Tests / value:** What predeclared metric, baseline and disaggregated slices would justify ML? How will false negatives, abstentions, calibration, drift, and operational cost be measured?
- **Rollback / no-ML decision:** Can the model be disabled to restore the deterministic baseline without changing permissions? Is *do not use ML* the best result?

**Default disposition:** If ground truth, legal data access, meaningful improvement over baseline, test oracle, or safe fallback cannot be established, **do not train or deploy a learned model**. Record the reason and keep using the baseline.

## Typed boundaries and example advisory record

Define a versioned input and output contract in the *adopting* project; do not add speculative fields to the current task-envelope JSON Schema. A production contract should include source identity, digest/version, captured time, permitted scope, age/freshness policy, null/unknown/abstain handling, and environment/tenant isolation.

Illustrative synthetic result (the fields are *not* an existing playbook schema or a live model output):

```json
{
  "record_type": "synthetic:advisory-prediction.v0",
  "subject": {"repository": "example/repository", "candidate_sha": "synthetic:commit"},
  "observed_state": {"snapshot_ref": "synthetic:snapshot", "captured_at": "synthetic:time"},
  "baseline": {"method": "queue-threshold-v1", "outcome": "inspect"},
  "model": {"artifact_digest": "synthetic:model", "training_data_ref": "synthetic:data"},
  "prediction": {
    "target": "candidate_retry_risk",
    "horizon": "next_attempt",
    "estimate": null,
    "uncertainty": "not_calibrated",
    "abstained": true,
    "reason": "out_of_distribution"
  },
  "evaluation": {"profile_ref": "synthetic:held-out-evaluation"},
  "recommendation": "request_review",
  "authority": "advisory_only",
  "effect_authorized": false
}
```

Never let a candidate provide its own trusted feature allowlist, policy thresholds, model approval, admissible actions, or granted capabilities through this record. An estimator can fail, time out, disagree with a baseline, or abstain; downstream policy must distinguish these from a positive verdict.

## Training, evaluation and leakage controls

1. **Baseline first:** freeze a cheap deterministic or statistical comparator, outcome definition and decision cost before model selection. Compare within the same captured datasets and time horizon.
2. **Temporal splits:** separate training, calibration and held-out evaluation by occurrence time; apply a realistic embargo around correlated events, delayed labels and feature construction when necessary. Do not use future incidents, statuses or post-decision observations as current features.
3. **Group boundaries:** split by appropriate repository, customer/tenant, worker, incident family, machine or workload identity when generalizing across groups; prevent near-duplicate events and siblings from leaking between train/test.
4. **Predeclare success:** report sample counts/denominators and per-group rates (false negative/positive, abstention, OOD, missing evidence, latency, operator cost). For probabilistic scores, evaluate calibration with reliability bins and a proper scoring rule such as Brier/log loss where labels permit. A confidence-looking number is not automatically calibrated.
5. **Stress and negative cases:** include stale/revoked input, changed tool permissions, never-before-seen services, failed upstream CI, poisoned logs/context, missing labels, distribution drift and counterfactual claims unsupported by observations.
6. **Version and bind:** capture dataset snapshot/label definition, time split, features/exclusions, model artifact digest, preprocessing code, calibration data, evaluation oracle and executable environment with immutable references where practical. Distinguish producer-owned from independent evaluation.
7. **Select by effects:** require more stringent protection, independent reproduction, safety checks and explicit operator authorization for T3/T4 or any workflow that may influence release, credentials, policy, data deletion, or protected branch admission.

For changed prompts, skills, models, tool permissions, or verifier rubrics, use the existing [agent-configuration regression profile](agent-regression-evaluation.md). Its synthetic fixtures do not establish a model's predictive validity. Semantic performance, label reliability, calibration and real-world impact need their own versioned observations.

## Out-of-distribution, abstention and disagreement

A model must decline to give a confident answer when inputs violate declared schema, freshness, population, horizon, or training-support assumptions. The adopter should define explicit abstention thresholds **before** inspecting the held-out result, with fallback to ordinary deterministic policy or human review. Important behaviors to test:

- Unknown feature values, training group, environment, tenant, policy revision, or model version.
- Inference service unavailable, slow, stale, expired, unsigned/unqualified artifact, or incomplete provenance.
- Predictions that contradict trusted deterministic state (such as a missing check or permission denial).
- Consecutive rollouts where uncertainty grows and no independently observed feedback corrects the state.

**Failure rule:** a high confidence prediction cannot turn failed, unverified, revoked, or missing required evidence into a pass. When source provenance is absent where required, mark `unverified` and do not promote the learned recommendation. Report abstention coverage and the cost of deferrals as part of the outcome.

## Threat model

| Threat | Failure mode | Control/evidence |
| --- | --- | --- |
| Dataset poisoning / strategic gaming | Agent-controlled labels or logs make poor candidates appear safe | Independent ground truth, data producer identity, integrity checks, attack-family holdouts |
| Leakage and overfit | Future incident labels, near-duplicate tasks, or shared tenants inflate performance | Temporal/group splits, embargo, deduplication, frozen oracle/version |
| Distribution drift / stale model | Deployment or CI policy changes invalidate the training distribution | Drift alerts with denominators, validity window, expiration, baseline fallback, requalification |
| Authority confusion | Prediction score treated as approval, or model recommendation selects its own capability | Typed advisory-only result, deterministic policy and separate grant/approval path |
| False confidence / unknown environment | Uncalibrated scores are presented as certainty | Held-out calibration, selective-risk/abstention curves, OOD tests, uncertainty wording |
| Privacy/retention leakage | Training data or inference logs expose secrets or cross-tenant context | Minimize/redact features, authorized retention, isolation, access controls, deletion/invalidation |
| Feedback and self-confirmation | Model decisions create the labels that later validate themselves | Human-verified outcomes, shadow comparisons, counterfactual limitations, independent incident capture |
| Untrusted retrieval/prompt injection | Observed text instructs a model/tool to change the policy or output format | Structured extraction, separate control plane, deterministic input validation and effect mediation |

Threats apply to both classical decision models and latent transition models. These controls do not guarantee model robustness; requirements must match the specific environment and consequences.

## Controlled progression and rollback

| Stage | Allowed use | Promotion proof |
| --- | --- | --- |
| **No ML / baseline** | Deterministic existing checks and manual interpretation | Baseline reproducibility and bounded failure posture |
| **Offline** | Frozen historical evaluation, no live effects | Predeclared objective, held-out temporal/group results, data/provenance audit, negative fixtures |
| **Shadow** | Score real observed state alongside current workflow; outputs cannot affect decisions | Live slices, calibration, drift, OOD and abstention rates; observed disagreements and false-safe cases |
| **Advisory** | Show bounded recommendations to accountable reviewers with clear source/uncertainty | Demonstrated value over baseline, rollback readiness, human override/effect audit, no policy weakening |
| **Narrowly governed integration** | A separately approved use of recommendations *within* fixed action limits | Explicit risk-specific owner approval and enforced authorization, independent qualification and negative bypass tests; never model-issued grants |

Promotion must be an externally authorized transition, not a self-reported model confidence event. A material model/data/threshold change returns to the appropriate evaluation stage. Expiration, regression, or uncertain inputs trigger abstention/disablement and fallback to the previously qualified baseline. Preserve stale-model and recovery evidence before declaring success.

## Concrete bounded project applications (not claims of deployed ML)

These are **candidate design exercises** showing where the guidance could be evaluated, not assertions that the projects use JEPA or learned models:

- **Dubnium CI/runner observations:** predict queue/backlog or suspected flake-prone validation from historical metadata, but preserve the deterministic runner admission, exact-head CI checks, and resource budgets. Existing [Dubnium verification issue #896](https://github.com/ryjen/dubnium/issues/896) owns real clean-run evidence; any predictor stays advisory.
- **ops-cadence source health:** forecast repeated source unavailability or finding recurrence from past bounded read-only reports; preserve original observed health and [finding lifecycle issue #44](https://github.com/ryjen/ops-cadence/issues/44) as separate truth. A predicted recovery cannot mark a source healthy.
- **Anthesis policy/evidence triage:** prioritize which claims need independent verification, but never assign approvals or create capability grants from inferred risk. [Evidence sufficiency #199](https://github.com/hackelia-micrantha/anthesis/issues/199) is independent of prediction.
- **Playbook agent-configuration regression:** use [synthetic evaluation examples](../examples/agent-regression/) to illustrate abstentions and unsupported verifiers, then independently assess whether a model adds any value. These fixtures are not measured ML performance or production training data.

No downstream project is required to adopt ML to conform to the playbook. The preferable outcome may be a simple threshold, a stronger deterministic check, or no prediction at all.

## Review checklist / acceptance summary

- [ ] Is the target outcome independently observable and sufficiently important?
- [ ] Are deterministic/low-complexity alternatives measured first?
- [ ] Are the observation schema, provenance, staleness and tenant bounds defined?
- [ ] Are temporal/group leakage and label poisoning addressed?
- [ ] Is uncertainty evaluated against actual outcomes and broken down by slice?
- [ ] Do OOD, missing data and backend failures abstain safely?
- [ ] Is the model output *strictly advisory* before any separately approved effect mediation?
- [ ] Are exact model/data/feature/calibration versions bound to the evaluation?
- [ ] Are promotion stages, accountable owners, rollback and model expiry specified?
- [ ] Do existing task risk, evidence, authorization, review and provider admission gates remain intact?
- [ ] Was **do not use ML** considered and recorded as a legitimate option?

**Boundary:** this document cannot satisfy [GitHub provider-admission issue #60](https://github.com/ryjen/agent-delivery-playbook/issues/60) or independently qualify any production ML system.
