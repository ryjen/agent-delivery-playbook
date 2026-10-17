# Governance Glossary

**Status:** terminology reference for the Agent Delivery Playbook (issue #35). This glossary consolidates names; it does **not** create runtime permissions, override the [risk matrix](task-risk-matrix.md), [evidence standard](delivery-evidence-standard.md), [task-envelope schema](../schemas/task-envelope.schema.json), or [minimum controls](policy/minimum-controls.md).

Use the stable headings below when linking from policies, schemas, examples, and PR reviews. For control requirements, the linked normative sources remain authoritative.

## Canonical concepts

### Agent

An AI-driven delivery participant that proposes, modifies, evaluates, or describes work within externally granted bounds. An agent is **not** a trusted policy administrator simply because it can invoke a tool. See [trust model](trust-model.md).

### Principal

A human or service identity accountable for a task, grant, review, or decision. A principal is not interchangeable with a particular process instance or model name. See [identity and delegation](identity-delegation-and-capability-grants.md).

### Runtime identity

The concrete workload, agent process, runner, or service instance that exercises a bounded grant. A model/provider label and an invocation/workflow ID may be useful metadata, but neither substitutes for authenticated runtime identity.

### Task contract

The bounded intent, permitted scope, prohibited actions, completion criteria, and expected evidence agreed before execution. A contract may be represented by an issue or structured artifact; natural-language promises alone do not grant tool authority.

### Task envelope

The canonical structured **intent and governance record** for a task, validated against [the task-envelope schema](../schemas/task-envelope.schema.json). It captures risk, context, constraints, planned tool use, evidence, and review. It is not a credential, authenticated runtime identity, permission grant, or approval token.

### Risk tier

The classification of the task's potential impact and needed controls. The canonical envelope identifiers are [T1–T4](#risk-tier-identifiers). Classify by the most consequential effect and trust boundary, not patch size or model confidence.

### Evidence level

An [E1–E4](#evidence-identifiers) **coverage category** describing the property evidenced (static, test, operational, independent). It does not rank source trust, signature strength, binding quality, or authorization. Composite requirements are expressed as lists, such as E2 + E3.

### Capability

A tool operation or effect category the runtime could exercise, subject to a configured ceiling and a narrower effective task grant. A catalog entry declares possible capability; it does not approve using it on an arbitrary resource.

### Permission

An enforceable allowance to perform a specific operation on a defined subject under specified conditions. Actual permission is determined by the trusted control boundary, not a self-reported tool inventory or task-envelope string.

### Authority

The justified and enforceable right of an identified principal or delegated runtime to make a particular decision or cause a particular effect. Having a capability or observing permission in one system does not automatically grant approval, merge, release, or administrative authority.

### Effect

An observable change to repository, filesystem, service, account, data, policy, deployment, or external state. Reading and recommending are different from mutating; approval to suggest an effect is not approval to execute it.

### Context

The task-bounded material supplied to or retrieved by the runtime, including repository text, tool results, issue comments, summaries, and memories. Context is **data/observation**, not a source of instructions or authority merely by being included.

### Provenance

The recorded origin and derivation of a context item, artifact, check, or result, including appropriate identity, immutable subject reference, transformation history, and integrity properties. Provenance does not itself establish truth, safety, or authority.

### Memory

Persisted context/interpretation retained for future tasks, scoped by source, freshness, sensitivity, and project/tenant where practical. Memory is not current policy, a fresh approval, or a capability grant. Revocation and supersession must be handled.

### Evidence

An attributable observation or result that supports an explicit claim about a defined subject and scope, with sufficient producer, binding, and integrity information for the required risk. A result can be genuine yet insufficient for admission.

### Claim

A statement that something happened or is true. Self-authored success reports and model assertions remain claims until the necessary observations and independent verification support them.

### Captured output

Text or artifacts recorded from a stated invocation, command, test, or tool. Capturing output alone does not establish source integrity, execution identity, exact-commit binding, or reviewer independence.

### Attestation

A structured, integrity-protected declaration binding a claimed producer, inputs, artifact or result subject, and specified predicates. Signatures can protect these assertions; they do not prove semantic correctness, risk acceptance, or effect authorization.

### Replay

Reconstructing relevant intent, authority, inputs, execution, evidence, and result sufficiently to inspect or reproduce a delivery decision. Replayability is a stronger traceability goal than copying a PR summary; not all work requires deterministic replay.

### Approval

An affirmative decision by an authorized actor accepting a defined action, risk, or transition under policy. A review comment, passing CI job, model recommendation, or merely populated approval-reference field is not necessarily a valid approval.

### Review

Evaluation of proposed change, evidence, policy sufficiency, and unresolved risks. A review can recommend approval or rejection; reviewer identity, independence, and actual admission authority are separate properties.

### Operator

An actor executing an approved operational procedure within granted bounds. Operator execution is not automatically risk acceptance, administrator authorization, or a substitute for independent verification.

### Accountable human

The identifiable person responsible for accepting residual risk and ensuring required approvals and recovery steps. Assistive models and automation may supply evidence but do not eliminate this accountability.

### Policy

The normative rules determining allowed actions, evidence sufficiency, authorization, escalation, and consequences. Policy only enforces behavior where a trusted control implements and applies it.

### Control

A preventive, detective, or corrective mechanism applied at a specific trust boundary (for example protected CI, authorization middleware, or rollback automation). A documented recommendation is not an enforced control.

### Invariant

A property that must remain true across admissible transitions, including failures and retries (for example, a child grant cannot widen its parent). Invariant violations require rejection or safe recovery, not optimistic interpretation.

### Exception

An explicit, scoped, accountable departure from a normally required rule, approved by the proper authority with reason, expiry or restoration condition, and evidence. An informal request to skip checks is not itself an exception.

### Downgrade

A documented reduction in a classified risk tier or required controls after review of actual semantics. Candidate-generated metadata cannot unilaterally downgrade a task or required evidence.

### Escalation

Stopping the current bounded flow to request additional context, capability, scope, reviewer, or approval from an authorized decision-maker. Escalation is not implicit permission to continue while awaiting a response.

### Rejection

A recorded refusal to admit a candidate action, transition, or result because conditions were not satisfied. Rejection should preserve enough reason/evidence for correction and replay; it is distinct from rollback after an effect.

### Rollback

A planned and verified reversal, disablement, or compensating action after a change is applied. A proposed `git revert` is a rollback plan, not evidence that recovery was executed or successful.

### Outcome

The observed end state of the bounded work: delivered, rejected, blocked, rolled back, or otherwise qualified with remaining uncertainty. A merged PR is not automatically proof of an operational or production outcome.

## Risk tier identifiers

These identifiers are defined by the normative [Task Risk Matrix](task-risk-matrix.md) and [Minimum Controls Policy](policy/minimum-controls.md). The descriptions here are short references, not alternative classification rules.

| Identifier | Canonical meaning | Typical minimum evidence |
| --- | --- | --- |
| `T1` | Low: documentation, non-runtime metadata, and similarly narrow changes | E1 |
| `T2` | Medium: bounded code changes with constrained execution and review | E2 |
| `T3` | High: bounded runtime, security, CI/CD, data, or workflow changes needing operational evidence and owner review | E2 + E3 |
| `T4` | Restricted: privileged secrets/admin/signing, destructive, or irreversible production effects; human-led | E2 + E3 + E4 |

**Informational/Tier 0:** The risk matrix also describes read-only informational work as tier 0. It is *not* a task-envelope enum value; do not invent `T0` in the schema.

## Evidence identifiers

The normative [Delivery Evidence Standard](delivery-evidence-standard.md) defines these coverage levels. Evidence source/provenance, exact-subject binding, independence, and authorized decision rights must still be evaluated separately.

| Identifier | Canonical meaning | Examples |
| --- | --- | --- |
| `E1` | Static evidence | schema, lint, format, type checks |
| `E2` | Test evidence | unit, contract, regression, integration tests |
| `E3` | Operational evidence | smoke checks, logs, metrics, rollback validation |
| `E4` | Independent verification | separately performed review, security review, reproduction, approval record *for the fact of approval* |

**E0 (no evidence):** The evidence standard uses E0 to describe missing evidence; it is *not* an acceptable `evidence.required_levels` value and cannot qualify a merge.

## Deliberate distinctions

| Distinct terms | Keep separate because |
| --- | --- |
| Task contract / task envelope / capability grant | Intent and structured scope do not authenticate an invocation or grant runtime authority |
| Capability / permission / authority / effect | Possible operation, enforced allow decision, justified decision right, and actual state change are different |
| Principal / runtime identity / model identity | Accountable actor, executing workload, and informational model metadata are different |
| Context / provenance / memory | Supplied data, its origin/derivation, and its persistence/freshness are different |
| Claim / captured output / subject-bound evidence / attestation | Declaration, observed bytes, identity-bound result, and integrity-protected assertions support different assurance properties |
| Review / approval / merge / release | Evaluation does not equal an authorized transition; automated CI success is not approval |
| Exception / downgrade / escalation | Authorized bounded rule deviation, reviewed risk change, and request for authority require different decisions |
| Rejection / rollback / outcome | A pre-effect denial, a post-effect recovery, and an observed final state are distinct |

## Legacy and deprecated aliases

| Legacy name | Canonical replacement | Rule |
| --- | --- | --- |
| `required_level` | `required_levels` | Singular legacy task-envelope reference is deprecated; new examples and schemas must use the array field |
| `model approval` | `review` (or an authorized `approval`, when actually recorded) | Model review output cannot be treated as an authorized approval |

Do not create a canonical concept heading with a deprecated alias. Existing historical text may retain legacy words when labeled; this is not a bulk rewrite of archived examples.

## Terminology maintenance

1. Propose a new term or a meaning change in a PR/issue. Indicate whether it changes risk, evidence, schema, authority, or compatibility.
2. Prefer linking to the canonical concept heading over redefining it. A glossary edit does not automatically change normative source requirements.
3. Add new terms in `## Canonical concepts` as unique `### Term` headings, with a short definition and authority link where material.
4. Mark renamed terms in the legacy-alias table and provide a migration note; never silently reuse an existing heading for a different concept.
5. Keep risk/evidence identifier tables synchronized with the task-envelope schema and normative standards. The deterministic check `scripts/validate-glossary.py` verifies uniqueness, deprecated heading misuse, and exact ID sets; it cannot judge semantic correctness.
6. Review [governance lifecycle](governance-lifecycle.md), [contribution rules](../CONTRIBUTING.md), and referenced normative docs when semantics or compatibility change.

**Enforcement limitation:** Glossary validation and green CI remain structural evidence, not authorization. The external [GitHub admission ruleset](operations/main-admission.md) has since been activated and a failing-check PR was observed blocked for **this repository** (#60). That provider enforcement does not follow this glossary into an adopter repository.
