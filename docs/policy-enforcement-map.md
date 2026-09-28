# AI-Native SDLC Policy and Enforcement Map

This document maps the playbook's AI-native software-delivery controls to their normative source, human judgment boundary, deterministic checks, enforcement mode, and implementation owner.

It is intentionally an **integration map**, not a second lifecycle model.

External vocabulary reference:

- [AI Native Project — AI Software Development Lifecycle](https://theainativeproject.org/ai-software-development-lifecycle/)
- [AI Native Project — AI-Native SDLC Handbook](https://theainativeproject.org/ai-native-sdlc-handbook/)

The external framework is informative. The playbook and repository-local contracts remain authoritative for governed delivery.

## Enforcement modes

| Mode | Meaning |
| --- | --- |
| Human | Requires accountable semantic judgment; automation may provide evidence but cannot decide the meaning |
| Advisory | Produces guidance or findings without blocking |
| Deterministic warning | Objective condition is detected and surfaced for review |
| Hard fail | Objective invariant is precise enough to reject automatically |
| Mixed | Deterministic checks enforce part of the control while semantic judgment remains human/policy-owned |

## Core lifecycle crosswalk

| AI-Native SDLC concept | Playbook / Micrantha realization | Normative source / owner | Enforcement posture |
| --- | --- | --- | --- |
| Plan-first execution | Bounded intent and task envelope | task-envelope schema, risk matrix | Mixed |
| Structured context | Provenance-aware bounded context; context treated as untrusted supply-chain input | `docs/ai-native-sdlc.md`, #40 | Mixed |
| Engineering memory | Candidate learning plus explicit governed promotion | Micrantha Compound workflow; Anthesis #208; Dubnium #617/#921 | Mixed |
| AI quality gates | Independently attributable exact-subject verification evidence | evidence standard; Anthesis #199; Dubnium #891/#896 | Mixed |
| Human-in-the-loop | Accountable approval selected by risk/policy | risk matrix, trust model, repository/release policy | Human / Mixed |
| Tool and agent constraints | Bound identity, delegation, capabilities, scope, and expiry | trust model, #39; Anthesis authority contracts | Mixed |
| Governance | Policy/evidence/approval separation | playbook methodology; Anthesis enforcement | Mixed |
| Lifecycle evidence | Replayable task/change/evidence relationships | delivery evidence standard; Anthesis #139 | Mixed |
| Freshness | Effect-time validation of policy-relevant dependencies | Anthesis #203 | Hard fail where implemented |
| Continuous learning | Plan -> Work -> Review -> Compound -> Repeat | Micrantha shared engineering workflow | Human / Mixed |

## Control map

| Control | Source of truth | Human responsibility | Local / CI / runtime check | Mode | Current owner / extension |
| --- | --- | --- | --- | --- | --- |
| Bounded task intent | Task envelope + issue/spec | Confirm semantic goal, non-goals, and acceptable blast radius | Schema/required-field validation | Mixed | playbook |
| Risk classification | `docs/task-risk-matrix.md` | Classify semantic risk and reject downgrades | Validate tier identifiers and required declared fields | Mixed | playbook |
| Context provenance | Context records / cited sources | Judge relevance, authority, and contradictions | Validate declared provenance/freshness metadata where available | Mixed | #40 |
| Context expansion | Task scope / runtime policy | Approve material expansion for sensitive work | Detect undeclared sources/tools where observable | Mixed | #40 / runtime |
| Agent/runtime identity | Trust model + invocation record | Decide acceptable accountable principal/runtime | Bind verifiable runtime/invocation identity | Mixed | #39 / runtime |
| Delegated authority | Exact task/capability grant | Define allowed effects and issuer accountability | Scope, expiry, revision, target, and action checks | Hard fail for objective mismatch | #39 / Anthesis |
| Tool/capability constraints | Capability catalog + runtime configuration | Decide which capabilities are appropriate | Tool registry, sandbox, credential, network, path restrictions | Mixed | playbook / runtime / Anthesis |
| Sensitive paths | Repository policy | Review false positives and any requested exception | Deterministic path matching | Escalate / hard fail when exact | playbook / repository |
| Evidence completeness | Delivery evidence standard | Judge whether evidence is sufficient and meaningful | Validate required evidence fields/references | Mixed | playbook |
| Evidence subject binding | Exact candidate/revision identity | Judge semantic relevance of verifier | Verify evidence binds exact subject/revision | Hard fail for mismatch | Anthesis #199 |
| Verification independence | Verification policy | Decide required independence for the risk | Verify producer/verifier identity separation where configured | Mixed | Anthesis #199 / Dubnium #891/#896 |
| Separation of duties | Trust model | Approve exceptions only through explicit policy | Prevent same authority from generating + approving/releasing where identities are verifiable | Mixed | #39 / platform policy |
| Approval | Risk/repository/release policy | Accept residual risk where policy requires | Bind approval to exact request, state, scope, and expiry | Mixed | Anthesis |
| Authority freshness | Current policy-relevant state | Resolve semantic conflicts/exception policy | Re-evaluate bound state dependencies at effect time | Hard fail for stale/mismatch | Anthesis #203 |
| Governed effect | Repository/runtime/release boundary | Define consequential effects and protected boundary | Complete mediation / allow-deny-indeterminate execution control | Hard fail | Anthesis + runtime |
| Candidate learning | Compound workflow | Decide whether a lesson is reusable | Emit non-authoritative candidate with provenance | Advisory | Micrantha .github / Dubnium #921 |
| Learning promotion | Trusted-context/policy owner | Approve attributable promotion into durable trusted context | Validate exact target/revision and required evidence | Mixed | Anthesis #208 |
| Rollback / rejection | Task/release policy | Decide when rollback is acceptable/sufficient | Validate declared rollback hooks/checks where objective | Mixed | repository / release system |
| CI/governance self-modification | Protected workflow/policy sources | Review semantic impact and authority changes | Sensitive-path detection, branch protection, policy guards | Escalate / hard fail | repository / organization policy |

## Authority model

The lifecycle must not collapse evaluation, evidence, policy, and approval into one actor:

```text
AI / agent evaluates or proposes
            |
            v
independent checks produce evidence
            |
            v
policy evaluates current authoritative state
            |
            +----> allowed effect
            |
            +----> approval required ----> accountable approval
            |
            `----> deny / indeterminate
```

A successful model judgment, test, verifier, previous approval, or remembered lesson cannot mint or widen authority by itself.

## Minimal adoption kernel

The minimum useful governed-delivery profile remains:

1. bounded task intent;
2. risk classification;
3. authority and tool constraints;
4. evidence requirements;
5. accountable review/outcome.

Additional controls are triggered by risk. Do not require every artifact for every task.

Examples of risk-triggered additions:

- context provenance ledger;
- explicit capability catalog;
- replayable evidence bundle;
- independent verifier;
- signed/trusted-runner evidence;
- effect-time freshness binding;
- enhanced approval;
- rollback rehearsal;
- governed learning promotion.

## Implementation rule

When this map identifies a missing control:

1. first locate the existing authoritative owner;
2. extend that owner rather than creating a parallel SDLC abstraction;
3. create a new issue only for a concrete missing enforcement/evidence/authority relationship;
4. preserve the distinction between methodology, runtime execution, verification, governance, and durable memory.

Terminology differences alone are not implementation gaps.

## Related

- `docs/ai-native-sdlc.md`
- `docs/trust-model.md`
- `docs/task-risk-matrix.md`
- `docs/delivery-evidence-standard.md`
- #37 — minimal adoption kernel
- #39 — identity/delegation/capability model
- #40 — context and memory as untrusted supply-chain inputs
- #58 — this enforcement-map work
- `hackelia-micrantha/.github#11` — governed actuation coordination
- `hackelia-micrantha/anthesis#139` — lineage and evidence provenance
- `hackelia-micrantha/anthesis#199` — independent semantic verification
- `hackelia-micrantha/anthesis#203` — effect-time authority freshness
- `hackelia-micrantha/anthesis#208` — governed persistent-learning promotion
- `ryjen/dubnium#617`, `#891`, `#896`, `#921` — runtime state, verification, and candidate-learning integration
