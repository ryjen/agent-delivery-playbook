# Delivery Evidence Standard

The Delivery Evidence Standard defines what must be produced before AI-assisted work can be trusted, reviewed, merged, or promoted.

The core rule is simple:

> Trust evidence produced by the delivery process, not claims produced by the model.

## Evidence coverage levels

E1-E4 describe **what class of property is being evidenced**. They do not describe how trustworthy the evidence source is.

```text
coverage != provenance
coverage != binding
coverage != independence
coverage != authority
```

An E2 test result can be a self-authored claim, captured local output, exact-commit CI evidence, or independently reproduced evidence. Those have very different assurance even though they cover the same test property.


| Level | Name | Description |
| --- | --- | --- |
| E0 | No Evidence | Unverified output. Not acceptable for merge. |
| E1 | Static Evidence | Formatting, linting, type checks, schema validation. |
| E2 | Test Evidence | Unit, regression, integration, or contract tests. |
| E3 | Operational Evidence | Deploy checks, smoke tests, logs, metrics, rollback validation. |
| E4 | Independent Verification | Independent review, security review, owner approval record, or independent reproduction. An approval record proves that an approval occurred; it does not by itself prove technical correctness. |

## Risk-to-Evidence Matrix

| Risk Tier | Minimum Evidence | Notes |
| --- | --- | --- |
| T1 | E1 | Documentation and metadata can use lightweight evidence. |
| T2 | E2 | Local code changes need tests or a documented reason tests are unavailable. |
| T3 | E2 + E3 | High-risk bounded runtime/security/CI/operational changes need test plus operational evidence and applicable owner review. |
| T4 | E2 + E3 + E4 | Restricted human-led changes need evidence for the human-executed result plus independent review/verification required by policy. |


## Evidence trust and binding

Evidence trust is not a second numeric ladder. Record the properties that make a piece of evidence more or less reliable for the decision being made.

A useful model is:

```text
evidence =
  observed result
  + producer/provenance
  + exact subject binding
  + environment/run identity
  + integrity properties
  + independence where required
```

Common evidence classes are shorthand for combinations of those properties:

| Class | What it establishes | What it does **not** establish | Typical use |
| --- | --- | --- | --- |
| Unverified claim | Someone or something asserted a result | That the command ran, output is authentic, or subject matches | Planning/debugging only; never satisfies a required check by itself |
| Captured output | Output was captured from a named command/tool invocation | That output was not fabricated/tampered with, or that it applies to the reviewed revision | Low-risk local evidence and diagnostics |
| Subject-bound evidence | Result is attributable to an exact repository/ref/commit, artifact digest, or equivalent subject | That producer/environment is trusted or independent | Normal T2 evidence; exact-candidate CI where producer trust is acceptable |
| Trusted-runner evidence | Subject-bound result came from a protected/identified runner or verifier whose configuration is outside the candidate's unilateral control | Semantic correctness beyond the checks actually run | T2/T3 required CI, especially when local self-report is insufficient |
| Attested provenance | A signature/attestation binds declared producer, inputs, artifact/result identity, and integrity properties | That the task was authorized or the result is semantically correct | Supply-chain/release evidence when provenance integrity matters |
| Independent reproduction / verification | A distinct reviewer/verifier reproduced or evaluated the exact relevant subject | Universal correctness, or authorization unless that verifier is also an authorized approver | T3/T4 boundaries requiring separation of duties |

These classes are **not strictly ordered**. For example, attested evidence may still come from the same producer that created the candidate, while independent reproduction may be unsigned. Policy should require the properties that matter for the risk rather than selecting the largest-sounding label.

### Minimum binding metadata

For evidence used to satisfy a required control, record the applicable fields:

| Metadata | Purpose |
| --- | --- |
| Repository / system | Identifies the authority domain in which the subject exists |
| Ref / exact commit | Prevents evidence from silently moving with a branch name |
| Artifact/result digest | Binds evidence to an immutable built or externally realized subject when commit identity is insufficient |
| Command/check identity | States exactly what produced the observation |
| Scope | Identifies tests, paths, service, environment, or boundary actually exercised |
| Producer identity | Human, agent, workflow, runner, verifier, or service that produced the evidence |
| Environment / runner identity | Makes material execution assumptions inspectable |
| Timestamp / run identifier | Supports freshness, audit, and replay analysis where time matters |
| Result | Pass/fail/indeterminate plus material diagnostics |
| Integrity/attestation reference | Records signature/provenance evidence when required |
| Independence relationship | States whether producer, candidate author/executor, verifier, and approver are distinct where policy depends on that separation |

Use immutable identifiers when the decision depends on exact subject identity. A branch name, "latest" artifact, mutable URL, or copied console snippet is not exact binding.

### Producer claims versus verification

```text
executor report = claim
captured output = observation
verified exact-subject result = evidence
policy evaluation = decision input
approval = authority where policy says so
```

None of these stages automatically grants the next stage's authority.

A producer may legitimately emit useful evidence about its own work, but that evidence cannot satisfy a requirement whose purpose is to establish **independence from that producer**.

### T3/T4 requirements

For T3 work, self-reported local output may support debugging and reviewer understanding, but it is insufficient when a required property can be verified by protected CI, a trusted runner, or another independently attributable system. Required operational evidence should bind to the exact candidate/environment it evaluates.

For T4 work, restricted execution remains human-led under the risk model. Any E4 requirement intended to provide independent verification must be satisfied by a distinct authorized reviewer/verifier or independently attributable system. Agent/executor self-report cannot satisfy that boundary.

### Attestation limits

Signatures, checksums, provenance attestations, and trusted-runner identities prove only the facts they actually bind. They do not establish:

- semantic correctness;
- task authorization;
- policy compliance outside the attested predicates;
- successful external realization unless that state was independently verified;
- approval to perform a later effect.

Do not convert cryptographic integrity into broader authority by implication.

### Retention and privacy

Stronger evidence often contains more metadata. Preserve enough for the declared audit/replay need without turning evidence storage into a secret or personal-data archive.

- prefer hashes, identifiers, and redacted references over sensitive payloads;
- do not capture credentials, authorization headers, private keys, or unnecessary personal data;
- define retention appropriate to incident/release/audit needs;
- protect evidence whose metadata exposes private repositories, runner topology, customer data, or internal security details;
- deletion/retention policy must not silently invalidate a still-required assurance claim.

### Replay and attestation are triggered extensions

Replay, signing, attestation, and protected evidence stores are not universal requirements. Add them when risk, incident reconstruction, supply-chain integrity, or policy requires assurance beyond ordinary subject-bound CI/reviewer evidence.


## Required Evidence Report

Every AI-assisted PR SHOULD include:

```markdown
# Delivery Evidence

## Objective

## Changes

## Tests

## Assumptions

## Risks

## Rollback

## Reviewer Notes
```

## Replayable Evidence

Replayable evidence is not the same as a normal PR summary.

A PR summary explains the final change. Replayable evidence explains the authorized task, execution identity, authority boundary, changed paths, checks, missing checks, context/provenance decisions, residual uncertainty, rollback path, and review linkage.

Use `docs/replayable-evidence-envelope.md` for medium/high-risk work or whenever the reviewer needs to reconstruct how the agent reached the change.

Minimum replay additions for T2+ work:

- task envelope reference;
- changed paths;
- actor/tool identity where known;
- allowed/prohibited scope confirmation;
- command/check names, scope, and results;
- evidence source/producer;
- exact subject binding such as repository + commit or artifact digest;
- relevant environment/runner identity and run/timestamp;
- independence/integrity properties when policy relies on them;
- context/provenance summary;
- known limits and nondeterminism;
- unverified claims;
- rollback path.

Unsupported claims MUST be marked as unverified rather than omitted.

## Evidence Quality Rules

Evidence MUST be specific. "Tests pass" is weaker than naming the command, scope, and result.

Evidence MUST be reproducible where possible. A reviewer should know how to re-run or inspect it.

Evidence MUST preserve uncertainty. If a test was not run, say why.

Evidence MUST NOT rely on model confidence as a substitute for verification.

Evidence MUST distinguish actual inspection or execution from inference.

Evidence MUST state its binding and producer strongly enough for a reviewer to know whether it applies to the exact candidate under review.

Evidence MUST NOT treat a signature, attestation, successful transport, or trusted runner as proof of properties that were not actually verified.

Evidence required for independent verification MUST NOT be satisfied solely by the actor whose result is being verified.

## Examples

### Weak

```text
Tested locally.
```

### Better

```text
Ran npm test -- auth-refresh.spec.ts. Added regression coverage for refresh-token null response. Full suite not run because unrelated e2e environment is not available locally.
```

### Replayable

```text
Task: T-0002, T2 bugfix, required E2.
Changed: src/auth/session.ts, tests/auth/session.test.ts.
Agent/tool: branch-only coding assistant; no CI or secret write authority.
Context: issue APP-1234, failing stack trace, affected module, existing test file. CI workflow excluded as out of scope.
Checks: npm test -- auth/session.test.ts, passed locally.
Unverified: full e2e login path not run because local IdP is unavailable.
Rollback: revert PR.
```

## Rollback Evidence

For T3/T4 work, rollback should be explicit:

- revert commit
- feature flag off
- restore previous workflow version
- redeploy previous artifact
- disable automation path

## Reviewer Checklist

- Does the evidence match the task envelope?
- Is the risk tier plausible?
- Are prohibited actions avoided?
- Are assumptions visible?
- Is rollback credible?
- Are unverified claims marked explicitly?
- Would this evidence survive an incident review?