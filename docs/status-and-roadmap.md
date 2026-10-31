# Project Status and Roadmap

_Last reconciled: 2026-10-30 against Git `main` at `8a6b4ab341aa1e25fff8aeafc97a09f0dba1d50f`, the immutable `v0.1.0` tag and the recorded GitHub provider/adopter evidence. This is an evidence snapshot, not authority to merge or release._

## Current state

The project is an **incubating public governance playbook with executable structural validation, a qualified tag-only `v0.1.0` distribution, and a read-only pilot against one independently maintained adopter**. It is not an agent runtime, authorization service, protected attestation service, CI provider, or production deployment system.

**Distribution:** [issue #89](https://github.com/ryjen/agent-delivery-playbook/issues/89) completed the explicitly approved **annotated Git tag only** milestone. `v0.1.0` tag object `023e8f543a341a2df5e0bc714eb44277074e0aba` resolves to commit `033ae363d1ce3c838b8e910c2f0ab75b08f7240e`. The tag is **unsigned**; no separate GitHub Release object, release binaries, security certification, or production enforcement was published. Do not move the tag.

**Adoption:** [issue #90](https://github.com/ryjen/agent-delivery-playbook/issues/90#issuecomment-6244296926) completed a source-pinned, read-only evaluation of [config-drift-guard](https://github.com/ryjen/config-drift-guard) at `36286b4e489b3ac424fb3d2ab85f1925e8f47206`. The kit detected an actual gap only after separate authenticated provider verification. The adopter-owned [issue #43](https://github.com/ryjen/config-drift-guard/issues/43#issuecomment-6244815987) subsequently closed with strict PR/check rules activated and a failed required-check PR blocked by GitHub. A second adopter, broad portability, and runtime authority mediation are **not** qualified by these results.

## Capability and evidence status

| Capability | Qualified state | Evidence and boundary |
| --- | --- | --- |
| Governance architecture, risk and evidence tiers, identity/delegation, context provenance | documented, with structural checks where applicable | [Architecture](architecture.md), [risk matrix](task-risk-matrix.md), [trust model](trust-model.md); intent and schema validity are not authority |
| Task-envelope schema, validators, glossary and policy integrity checks | implemented and tested | `schemas/task-envelope.schema.json`, `scripts/`, `flake.nix`; validation does not determine semantic correctness |
| Adversarial and agent-configuration fixtures | synthetic regression checks | `examples/adversarial/`, `examples/agent-regression/`; not a production containment benchmark |
| Reproducible repository validation | flake-first and CI-checked | [tagged-commit CI run 39080109844](https://github.com/ryjen/agent-delivery-playbook/actions/runs/39080109844) passed both checks and 96 unit tests; this run does not cover later `main` commits |
| Default-branch PR/status admission | provider-enforced for tested path | Playbook [issue #60](https://github.com/ryjen/agent-delivery-playbook/issues/60) and [negative PR #87](https://github.com/ryjen/agent-delivery-playbook/pull/87) establish failing-check rejection. Missing-check and direct-push rejections were not separately tested; admins retain ruleset control-plane powers |
| Read-only conformance kit | implemented, pilot exercised | [Conformance contract](conformance-kit.md) and [adopter pilot #90](https://github.com/ryjen/agent-delivery-playbook/issues/90); `effect_authorized=false` regardless of report or exit status; evidence/approval is not independently attested |
| Minimal adoption kernel and standalone reference example | documented and demonstrated | [Minimal kernel](adoption/minimal-adoption-kernel.md), [reference case](../examples/reference-adoption/case-study.md); risk-triggered controls avoid unnecessary files |
| `v0.1.0` distribution | annotated tag qualified, no GitHub Release | [Tag/CI/clean checkout evidence #89](https://github.com/ryjen/agent-delivery-playbook/issues/89); unsigned immutable-by-convention tag, x86_64-linux evidence only |
| Independent consumer portability | one external repository evaluated read-only | [config-drift-guard pilot #90](https://github.com/ryjen/agent-delivery-playbook/issues/90#issuecomment-6244296926); source pinned, separate Python venv, not the Nix closure; parser-subset limitation observed |
| Runtime grants, effect-time authorization, approval verification, protected attestations | outside playbook implementation | Requires separately governed implementation and exact-subject independent evidence; not inferred from conformance |

## Immediate queue — after tag and first adoption

1. **Reconcile publication facts.** Keep README, status, index, and the historical [pre-tag qualification dossier](releases/v0.1.0-readiness.md) consistent with issue #89 and #90. No schema, normative control or release action is required for documentation repair.
2. **Evaluate a second distinct adopter, read-only.** Pin `v0.1.0` source and a separate target commit; inventory existing controls, run reproducible structural checks where tooling permits, exercise a bounded and an unauthorized synthetic case, and report real friction, skips, limitations, and independently verified provider facts. Make no adopter changes as part of the assessment.
3. **Integrate only supported findings.** Record follow-up work in the actual owning repository for material gaps. Anthesis owns evidence/provenance and effect-time authority semantics; Dubnium owns executor, runner and verification mechanics; GitHub/provider controls remain local to each adopter. No new playbook runtime or policy engine is implied.
4. **Decide on later versioned changes only after evidence.** Do not overwrite `v0.1.0`, publish an unapproved GitHub Release, or make portability/security claims beyond the observations.

## Completed milestones, retained as evidence

- [#89](https://github.com/ryjen/agent-delivery-playbook/issues/89) — tag-only `v0.1.0` distribution, post-merge CI and clean tagged checkout.
- [#90](https://github.com/ryjen/agent-delivery-playbook/issues/90) — independent read-only Config Drift Guard pilot; adopter gap tracked and resolved separately.
- [#60](https://github.com/ryjen/agent-delivery-playbook/issues/60) — playbook provider-enforced required PR/check admission for tested failing-check case.
- [#45](https://github.com/ryjen/agent-delivery-playbook/issues/45), [#35](https://github.com/ryjen/agent-delivery-playbook/issues/35), [#36](https://github.com/ryjen/agent-delivery-playbook/issues/36), [#43](https://github.com/ryjen/agent-delivery-playbook/issues/43) — conformance, glossary, ADR and versioning foundations.

## Scope and qualification rules

This playbook owns portable governed-delivery guidance, normative policy, schemas, templates, synthetic tests and advisory conformance. It does **not** own runtime effects, CI administration, attestations, production adoption, personal automation, or domain-specific reporting. Consumers retain their own policy and provider admission authority.

- **Documented** means described, not implemented.
- **Validated** means a repeatable check supports a specific claim and subject.
- **Demonstrated** means an attributable bounded use case was exercised.
- **Provider-enforced** means live provider configuration and a material negative admission path were observed.
- **Distributed** means the approved tagged source tree was independently read back and smoke tested. This repo's `v0.1.0` is distributed as a tag; **no GitHub Release object** exists.
- **Authorized** means a current, independent, appropriate authority decided a particular effect; neither an envelope nor a conformance report supplies this.

The [release-readiness dossier](releases/v0.1.0-readiness.md) is a **historical October 17 pre-tag assessment**, not the live release checklist. Preserve its original evidence and limitations; use #89 for the actual tag disposition.
