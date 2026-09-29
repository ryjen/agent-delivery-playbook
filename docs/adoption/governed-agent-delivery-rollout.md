# Governed Agent Delivery Rollout

This guide describes a practical adoption path for teams introducing AI-assisted or agent-assisted delivery.

The goal is to avoid two bad outcomes:

1. agents operate informally with no reviewable boundary;
2. governance becomes too heavy and nobody uses it.

## Phase 1: Make Work Visible

Introduce lightweight artifacts without blocking normal delivery.

Adopt:

- a visible task objective and scope for all write-capable agent work;
- inline task/risk/evidence fields for small T1 work;
- structured task envelopes as the normal T2+ path or when authority/context complexity triggers one;
- evidence in PRs;
- reviewer guidance proportionate to risk.

Do not enforce everything immediately.

### Success Criteria

- AI-assisted PRs say what the agent was asked to do.
- Evidence is specific enough to review.
- Reviewers can identify scope expansion.

## Phase 2: Classify Risk

Add risk tiering and sensitive path review.

Adopt:

- T1-T4 risk tiers
- sensitive path policy
- minimum controls policy

### Success Criteria

- high-risk T3 and restricted T4 surfaces are visible before merge.
- CI, auth, secrets, infra, and dependency changes are no longer treated as routine cleanup.
- Reviewers challenge incorrect tiering.

## Phase 3: Govern Tool Authority

Start recording material tool decisions.

Adopt:

- tool-call decision records when a material external effect or authority decision exists;
- explicit approval gates for sensitive T3 effects where policy requires them;
- human-led handling for restricted T4 effects rather than delegating those effects to the agent;
- explicit denial/escalation records.

### Success Criteria

- shell, network, dependency, and CI changes have clear rationale.
- denied or escalated tool requests are documented.
- tool authority is not hidden in chat history.

## Phase 4: Enforce the Baseline

Move from convention to policy.

Adopt:

- PR template checks
- CODEOWNERS or branch protection for sensitive paths
- schema validation for task envelopes
- CI checks for required evidence fields

### Success Criteria

- obvious missing controls block merge.
- sensitive paths trigger required review.
- evidence gaps are caught before human review.

## Phase 5: Improve Auditability

Add stronger provenance and replayability for higher-autonomy workflows.

Adopt:

- signed artifacts where useful
- retained command logs
- model/tool provenance
- independent verification for high-risk paths

### Success Criteria

- incident review can reconstruct the work.
- approvals are traceable.
- evidence can be independently checked.

## Minimal Team Policy

A team can start with three rules:

1. Any write-capable agent-assisted PR needs bounded intent and evidence; T1 may represent this inline.
2. Sensitive paths trigger the repository's minimum risk floor—typically T3, with T4 reserved for restricted human-led authority.
3. CI, auth, secrets, infra, or production-data changes require the applicable accountable human/platform/security review; restricted effects are not delegated merely because approval exists.

## Anti-Patterns

Avoid:

- treating chat history as the audit log
- accepting "the model said tests pass" as evidence
- letting agents modify workflows to make checks pass
- hiding dependency changes inside feature work
- downgrading risk because the diff is small
- requiring heavyweight process for harmless docs changes

## Practical Default

Start at Level 3 of the maturity model for high-risk work and Level 1-2 for low-risk work.

That gives teams a usable path without pretending all agent work needs the same amount of ceremony.


## Reference adoption finding

The standalone reference adoption in `examples/reference-adoption/case-study.md` confirmed that applying every artifact universally creates unnecessary ceremony. The useful boundary was concern-based:

- T2 needed explicit intent/scope, a bounded grant representation, E2 evidence, and an accountable outcome;
- capability catalogs, attestations, and separate tool-decision records were unnecessary for the successful localized task;
- the authority-expansion request was easier to reason about as a separate denied task/grant request;
- exact candidate CI identity is best retained by the PR/run system rather than self-referenced inside the same changing commit.

Use the minimal adoption kernel as the authority for the smallest sufficient artifact set.
