# Project Status and Roadmap

_Last reconciled: 2026-09-28._

## Current state

The project is an **incubating public governance playbook/specification with executable conformance pieces**.

It is more mature than a starter template: the repository has a canonical architecture, AI-native SDLC and trust models, normative task/risk/evidence policy, machine-readable task-envelope structure, dual validators, validator tests, repository-integrity checks, contribution/security policy, and an active validation workflow.

It is **not** an agent runtime, authorization service, policy engine, evidence attestation service, or production deployment system. One standalone representative adoption is demonstrated; broad production adoption and end-to-end runtime enforceability have not been demonstrated.

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
| Reproducible CI environment | validated | `flake.nix` + committed `flake.lock`; CI runs flake-owned checks and no longer installs repository Python dependencies with pip |
| Evidence trust/binding model | implemented guidance | `docs/delivery-evidence-standard.md`; coverage is separated from producer/binding/integrity/independence |
| Identity/delegation/capability model | implemented guidance | `docs/identity-delegation-and-capability-grants.md`; runtime enforcement remains outside current implementation |
| Context/memory supply-chain controls | implemented + validated structure | `docs/context-budget-and-provenance.md`; revoked-context schema/validator support; #40 complete |
| Adversarial/bypass-resistance fixtures | validated | 10 machine-readable scenarios + deterministic CI evaluator under `examples/adversarial/`; #41 complete |
| Minimal adoption kernel | implemented guidance | `docs/adoption/minimal-adoption-kernel.md`; optional artifacts are risk-triggered |
| Standalone reference adoption | demonstrated (representative) | baseline PR #71 + governed T2/rejected paths in PR #72; `examples/reference-adoption/case-study.md` |
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

### 2. #43 — define release/version compatibility

Turn the now-demonstrated adoption contract into an explicit pre-1.0 versioning/release policy without implying runtime conformance that the repository cannot enforce.

Exit: normative/schema/template compatibility and release expectations are documented and testable where objective.

### 3. #45 — build the lightweight conformance kit

Package the minimal validated pieces needed to evaluate an adopting repository without copying the whole playbook.

Exit: adopters can run a small, versioned conformance path that reports what is structurally checked and what remains human/policy judgment.
## Follow-on maturity work

The core guidance now has executable self-conformance, adversarial fixtures, and one standalone representative adoption. Remaining work should focus on provider admission (#60), release/compatibility (#43), and a proportionate conformance kit (#45), while preserving the documented limits around runtime enforcement and production evidence.

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
