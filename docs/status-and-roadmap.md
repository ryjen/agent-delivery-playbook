# Project Status and Roadmap

_Last reconciled: 2026-09-28._

## Current state

The project is an **incubating public governance playbook/specification with executable conformance pieces**.

It is more mature than a starter template: the repository has a canonical architecture, AI-native SDLC and trust models, normative task/risk/evidence policy, machine-readable task-envelope structure, dual validators, validator tests, repository-integrity checks, contribution/security policy, and an active validation workflow.

It is **not** an agent runtime, authorization service, policy engine, evidence attestation service, or production deployment system. Broad real-world adoption and end-to-end enforceability have not yet been demonstrated.

## Capability status

| Capability | State | Evidence / limitation |
| --- | --- | --- |
| Canonical governed-delivery architecture | implemented guidance | `docs/architecture.md`; lifecycle, boundaries, sources of truth, failure paths |
| AI-native SDLC governance model | implemented guidance | `docs/ai-native-sdlc.md` |
| Policy/enforcement crosswalk | implemented guidance | `docs/policy-enforcement-map.md`; vendor/runtime neutral |
| Trust and separation-of-duties model | implemented guidance | `docs/trust-model.md` |
| Task-envelope schema | implemented | JSON Schema plus checked-in examples |
| Lightweight task-envelope validator | validated | unit-tested repository tooling |
| Standards-based YAML/JSON-Schema validation | validated | independent standards-based path |
| Repository integrity validation | validated | local-link, JSON, and Mermaid/document checks |
| GitHub Actions validation | validated but not admission-enforced | current workflow passes; #60 tracks required admission |
| Reproducible CI environment | incomplete | current CI still uses ambient runner/Python + imperative dependency installation; #55 |
| Evidence trust/binding model | planned | #38 |
| Identity/delegation/capability binding | planned | #39 |
| Context/memory supply-chain controls | planned | #40 |
| Adversarial/bypass-resistance fixtures | planned | #41 |
| Minimal adoption kernel | planned | #37 |
| Standalone reference adoption | not demonstrated | #42 |
| Release/version compatibility contract | planned | #43 |
| Lightweight conformance kit | planned | #45 |
| Runtime authorization / tool-effect gating | not implemented | deliberately outside this repository's runtime scope |
| Protected evidence storage / attestation | not implemented | downstream enforcement concern |
| Production adoption evidence | not demonstrated | requires reference/real adoption work |

## Immediate execution queue

Keep the near-term queue intentionally small.

### 1. #60 — enforce repository admission

Make this repository obey the governance model it describes:

- require normal PR admission for non-trivial changes;
- require stable validation checks;
- define explicit accountable break-glass behavior;
- bind admission evidence to the applicable candidate.

Exit: a failing or missing required check cannot silently admit a normal change to `main`.

### 2. #55 — make CI flake-first and reproducible

Move executable CI tooling into a repository-owned Nix flake while retaining `mise` as the task UX.

Exit: CI and local validation use the same locked, repository-owned environment and no longer rely on ambient Python plus dynamic transitive pip resolution.

### 3. #37 — define the minimal adoption kernel

Make first adoption proportionate rather than ceremonial.

Exit: an adopter can identify the smallest sufficient control set in under five minutes, with additional artifacts triggered explicitly by risk/authority.

### 4. #38 — define evidence trust and binding

Clarify the difference between a claim, captured output, commit-bound CI evidence, trusted-runner evidence, attestation, and independent reproduction.

Exit: evidence requirements state what each evidence class proves and what it does not prove.

## Follow-on security and demonstration work

After the immediate queue:

1. #39 — identity, delegation, and capability model;
2. #40 — context and memory as untrusted supply-chain inputs;
3. #41 — adversarial governance and bypass-resistance examples;
4. #42 — standalone reference adoption and case study.

These should feed back into the playbook rather than being treated as independent documentation exercises.

## Distribution and maturity work

After the core model is demonstrated:

- #43 — versioning, releases, and compatibility policy;
- #45 — lightweight governed-delivery conformance kit.

A pre-1.0 release should represent a coherent, demonstrated adoption contract rather than simply a documentation milestone.

## Deferred governance refinements

Useful governance work should not displace executable self-conformance:

- #35 — glossary and terminology governance;
- #36 — ADR process for stable governance choices.

Promote either only when current work is blocked by terminology or decision-history ambiguity.

## Scope boundary

The playbook owns **portable governed-delivery methodology, contracts, templates, examples, and deterministic conformance guidance**.

It does not own personal automation, CareerOps, scheduled reporting infrastructure, or domain-specific n8n workflows. The 2026-09-28 review routed previous scope drift to domain owners:

- Anthesis research intake → `hackelia-micrantha/anthesis#265`;
- personal writing/blog intake → `ryjen/blog#109`;
- scheduled project/CI/repository-health reporting → `ryjen/ops-cadence#44`;
- resume/job-pipeline reporting → `ryjen/career-workflows#280`.

Reusable lessons from those systems may return here only when they generalize into vendor-neutral governed-delivery controls.

## Completion standard

A capability is not considered demonstrated merely because documentation exists or CI is green.

Claims should distinguish:

- **documented** — behavior or policy is described;
- **implemented** — supporting artifact/tooling exists;
- **validated** — implementation has relevant repeatable evidence;
- **demonstrated** — an end-to-end supported use case has been exercised;
- **deferred** — intentionally outside the current milestone.

The roadmap should be updated when implementation evidence changes, not on a fixed ceremonial cadence.
