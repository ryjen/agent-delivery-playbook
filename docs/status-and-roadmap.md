# Project Status and Roadmap

_Last reconciled: 2026-10-17 against \`main\` commit \`56ab8b343200914ad286e04893ea9ce3f2a31d25\` and GitHub's live ruleset. This is an evidence snapshot, not a release authorization._

## Current state

The project is an **incubating public governed-delivery playbook with validated structural conformance tooling and one representative standalone adoption**. It is more than a starter template, but it is not an agent runtime, policy authorization service, independent attestation service, or production deployment system.

The next milestone is a carefully qualified first **\`v0.1.0\` release**, not a new governance engine. No release or tag has been published. See [the first-release readiness dossier](releases/v0.1.0-readiness.md) and [draft release notes](releases/v0.1.0-notes.md).

## Capability and evidence status

| Capability | Qualified state | Evidence and boundary |
| --- | --- | --- |
| Canonical architecture, governance lifecycle and trust model | documented | [Architecture](architecture.md), [trust model](trust-model.md), [governance lifecycle](governance-lifecycle.md); implementation-independent |
| Normative task risk, evidence and minimum controls | documented | [Task risk matrix](task-risk-matrix.md), [evidence standard](delivery-evidence-standard.md), [minimum controls](policy/minimum-controls.md) |
| Task-envelope JSON Schema and lightweight/standards-based validation | validated structural checks | \`schemas/task-envelope.schema.json\`, \`scripts/validate-task-envelopes.py\` and \`scripts/validate-task-envelopes-standard.py\`; schema success does not validate intent or grant authority |
| Context/memory provenance, identity and delegation | documented with structure checks | \`docs/context-budget-and-provenance.md\`, \`docs/identity-delegation-and-capability-grants.md\`; **not** runtime authorization |
| Glossary and ADR history | implemented and checked where structural | [Glossary](glossary.md), [ADR index](adr/README.md); issues [#35](https://github.com/ryjen/agent-delivery-playbook/issues/35) and [#36](https://github.com/ryjen/agent-delivery-playbook/issues/36) closed |
| Adversarial fixtures and agent-configuration regression profile | validated synthetic contracts | \`examples/adversarial/\`, \`examples/agent-regression/\`; deterministic fixture results are not empirical benchmarks or production security proof |
| Reproducible repository validation | validated on \`main\` | \`flake.nix\` + \`flake.lock\`; [Validate run 39075352393](https://github.com/ryjen/agent-delivery-playbook/actions/runs/39075352393) at \`56ab8b3\` passed \`Repository integrity\` and \`Task envelopes\` |
| Default-branch PR/status admission | provider-enforced, failing-check path demonstrated | GitHub ruleset \`17832277\` active: PR and strict two-check requirement, no ruleset bypass actors; [disposable failed-check PR #87](https://github.com/ryjen/agent-delivery-playbook/pull/87) reported \`mergeable_state: blocked\`; issue [#60](https://github.com/ryjen/agent-delivery-playbook/issues/60) closed. Missing-check and direct-push cases not independently exercised; administrators can still edit provider settings |
| Lightweight read-only conformance kit | implemented and self-validated pilot | \`scripts/conformance-kit.py\`, [kit contract](conformance-kit.md) and negative tests; issue [#45](https://github.com/ryjen/agent-delivery-playbook/issues/45) closed. **Adopter portability and independent provenance/approval validation are not demonstrated** |
| Minimal adoption kernel and standalone case study | documented and one example demonstrated | [Minimal kernel](adoption/minimal-adoption-kernel.md), [reference adoption](../examples/reference-adoption/case-study.md), candidate PRs [#71](https://github.com/ryjen/agent-delivery-playbook/pull/71) and [#72](https://github.com/ryjen/agent-delivery-playbook/pull/72); synthetic/tiny project, not production adoption |
| Version/compatibility and draft first-release process | documented, release not qualified | [Compatibility policy](versioning-and-compatibility.md), \`CHANGELOG.md\`, [release dossier](releases/v0.1.0-readiness.md); no tag/release or accountable exact-commit release approval |
| Runtime capability enforcement, protected attestations, production adoption | not demonstrated or out of playbook scope | Requires implementing systems, authenticated independent evidence, and a separate risk-qualified decision |

**Evidence rule:** “implemented,” “validated,” “demonstrated,” and “provider-enforced” are distinct. A structural validator returning green neither authorizes a tool effect nor verifies a signed approval or evidence producer.

## Immediate queue — first release qualification

1. **Reconcile the candidate package.** Confirm the policy/schema/validator/example compatibility contract and publishable, version-neutral guidance remain coherent. This is a documentation and evidence check; do not change the normative schema merely to improve release wording.
2. **Qualify an exact candidate.** Run \`nix flake check --print-build-logs\` and the required GitHub PR jobs against the reviewed release-preparation head. Recheck final \`main\` after merge: the preparatory baseline commit above is **not** the later release commit.
3. **Review operational and distribution boundaries.** Inspect the reference adoption and adversarial fixture results, document untested portability, pinning, provenance and negative-admission limits, and prepare release notes. Avoid claims of broad production rollout.
4. **Require accountable release authorization.** Only after explicit approval of the **exact final commit** may an authorized operator create and verify the annotated \`v0.1.0\` tag and corresponding GitHub release. A documentation PR is not such approval.
5. **Demonstrate pinned adoption** in a separate consumer checkout after tagging. Preserve exact tag-to-commit and flake-lock binding; do not implicitly fetch moving \`main\`.

The [release dossier](releases/v0.1.0-readiness.md) contains the proof matrix and remaining tag checks. A release must not be marked done merely because this readiness PR merges.

## Completed issues, retained as history

- [#45](https://github.com/ryjen/agent-delivery-playbook/issues/45) — read-only conformance kit merged in PR #82; portability beyond the self-test remains unverified.
- [#60](https://github.com/ryjen/agent-delivery-playbook/issues/60) — activated GitHub rules and blocked negative PR demonstrated; administrative-control-plane and untested negative-path limits retained.
- [#35](https://github.com/ryjen/agent-delivery-playbook/issues/35) — canonical glossary with identifier check in PR #83.
- [#36](https://github.com/ryjen/agent-delivery-playbook/issues/36) — ADR template, history and contribution conventions in PR #84.
- [#74](https://github.com/ryjen/agent-delivery-playbook/issues/74) — optional, non-authoritative decision/prediction guidance in PR #85.
- [#43](https://github.com/ryjen/agent-delivery-playbook/issues/43) — versioning and compatibility policy; publishing the first tag is **separate** from closing the policy issue.

## Deferred maturity work

Actual cross-repository consumer portability tests, richer evidence provenance/independence, published compatibility migrations, and production adoption may warrant later scoped issues **after** the first candidate review. Do not re-open closed implementation issues merely because a future maturity goal is unproven. No new policy engine, learned-model runtime, generic attestation platform, or new CI provider is required for \`v0.1.0\`.

## Scope boundary

The playbook owns portable governed-delivery methodology, contracts, templates, examples and deterministic conformance guidance. It does **not** own personal automation, CareerOps, scheduled reporting infrastructure, or domain-specific n8n workflows. Domain-specific work remains with its respective repositories (Anthesis, Dubnium, ops-cadence, career-workflows).

## Completion standard

- **Documented:** a rule or architecture is described.
- **Implemented:** code or an artifact exists.
- **Validated:** repeatable, appropriately bound evidence supports the implemented behavior.
- **Demonstrated:** a bounded real or representative use case was exercised with attributable results.
- **Provider-enforced:** the external service's active configuration and material admission behavior were observed.
- **Released:** an explicitly approved immutable tag and published notes are verified against the accepted commit; **not yet achieved**.

Update this page when evidence changes, not on a ceremonial schedule.
