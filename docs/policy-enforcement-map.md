# AI-Native SDLC Policy and Enforcement Map

This document maps the playbook's AI-native software-delivery controls to their normative source, human judgment boundary, deterministic checks, and enforcement mode.

It is intentionally an **integration map**, not a second lifecycle model or a dependency on a particular agent runtime, CI provider, or governance product.

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

| AI-Native SDLC concept | Vendor-neutral playbook realization | Typical enforcement surface |
| --- | --- | --- |
| Plan-first execution | Bounded intent and task envelope | task schema + accountable review |
| Structured context | Provenance-aware bounded context treated as an untrusted supply-chain input | context records + retrieval/tool policy |
| Engineering memory | Candidate learning plus explicit promotion into trusted durable context | memory/policy owner + promotion control |
| AI quality gates | Independently attributable exact-subject verification evidence | verifier + CI/runtime evidence |
| Human-in-the-loop | Accountable approval selected by risk/policy | repository/release/change-approval boundary |
| Tool and agent constraints | Bound identity, delegation, capabilities, scope, and expiry | runtime/tool/sandbox/credential boundary |
| Governance | Policy, evidence, approval, and effect remain distinct | policy/control plane |
| Lifecycle evidence | Replayable task/change/evidence relationships | evidence store + audit trail |
| Freshness | Effect-time validation of policy-relevant dependencies | authorization/effect boundary |
| Continuous learning | Plan -> Work -> Review -> Compound -> Repeat | engineering workflow + controlled promotion |

## Control map

| Control | Source of truth | Human responsibility | Local / CI / runtime check | Mode |
| --- | --- | --- | --- | --- |
| Bounded task intent | Task envelope + issue/spec | Confirm semantic goal, non-goals, and acceptable blast radius | Schema/required-field validation | Mixed |
| Risk classification | `docs/task-risk-matrix.md` | Classify semantic risk and reject downgrades | Validate tier identifiers and required declared fields | Mixed |
| Context provenance | Context records / cited sources | Judge relevance, authority, and contradictions | Validate declared provenance/freshness metadata where available | Mixed |
| Context expansion | Task scope / runtime policy | Approve material expansion for sensitive work | Detect undeclared sources/tools where observable | Mixed |
| Agent/runtime identity | Trust model + invocation record | Decide acceptable accountable principal/runtime | Bind verifiable runtime/invocation identity | Mixed |
| Delegated authority | Exact task/capability grant | Define allowed effects and issuer accountability | Scope, expiry, revision, target, and action checks | Hard fail for objective mismatch |
| Tool/capability constraints | Capability catalog + runtime configuration | Decide which capabilities are appropriate | Tool registry, sandbox, credential, network, path restrictions | Mixed |
| Sensitive paths | Repository policy | Review false positives and any requested exception | Deterministic path matching | Escalate / hard fail when exact |
| Evidence completeness | Delivery evidence standard | Judge whether evidence is sufficient and meaningful | Validate required evidence fields/references | Mixed |
| Evidence subject binding | Exact candidate/revision identity | Judge semantic relevance of verifier | Verify evidence binds exact subject/revision | Hard fail for mismatch |
| Verification independence | Verification policy | Decide required independence for the risk | Verify producer/verifier identity separation where configured | Mixed |
| Separation of duties | Trust model | Approve exceptions only through explicit policy | Prevent same authority from generating + approving/releasing where identities are verifiable | Mixed |
| Approval | Risk/repository/release policy | Accept residual risk where policy requires | Bind approval to exact request, state, scope, and expiry | Mixed |
| Authority freshness | Current policy-relevant state | Resolve semantic conflicts/exception policy | Re-evaluate bound state dependencies at effect time | Hard fail for stale/mismatch |
| Governed effect | Repository/runtime/release boundary | Define consequential effects and protected boundary | Complete mediation / allow-deny-indeterminate execution control | Hard fail |
| Candidate learning | Engineering workflow | Decide whether a lesson is reusable | Emit non-authoritative candidate with provenance | Advisory |
| Learning promotion | Trusted-context/policy owner | Approve attributable promotion into durable trusted context | Validate exact target/revision and required evidence | Mixed |
| Rollback / rejection | Task/release policy | Decide when rollback is acceptable/sufficient | Validate declared rollback hooks/checks where objective | Mixed |
| CI/governance self-modification | Protected workflow/policy sources | Review semantic impact and authority changes | Sensitive-path detection, branch protection, policy guards | Escalate / hard fail |

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

1. first locate the existing authoritative owner in the adopting environment;
2. extend that owner rather than creating a parallel SDLC abstraction;
3. create new implementation work only for a concrete missing enforcement/evidence/authority relationship;
4. preserve the distinction between methodology, runtime execution, verification, governance, and durable memory.

Terminology differences alone are not implementation gaps.

## Non-normative Micrantha realization

Micrantha is one concrete downstream realization of this vendor-neutral map. These references are examples, not dependencies of the playbook:

| Concern | Existing Micrantha owner |
| --- | --- |
| Organization governed-actuation coordination | `hackelia-micrantha/.github#11` |
| Context/memory as untrusted input | this playbook #40 plus repository/runtime policy |
| Identity/delegation/capabilities | this playbook #39 plus Anthesis authority contracts |
| Execution/evidence lineage | `hackelia-micrantha/anthesis#139` |
| Independent semantic verification | `hackelia-micrantha/anthesis#199`; `ryjen/dubnium#891/#896` |
| Effect-time authority freshness | `hackelia-micrantha/anthesis#203` |
| Governed learning promotion | `hackelia-micrantha/anthesis#208`; `ryjen/dubnium#617/#921` |
| Internal end-to-end rehearsal | `hackelia-micrantha/anthesis#188` |

## Related playbook material

- `docs/ai-native-sdlc.md`
- `docs/trust-model.md`
- `docs/task-risk-matrix.md`
- `docs/delivery-evidence-standard.md`
- #37 — minimal adoption kernel
- #39 — identity/delegation/capability model
- #40 — context and memory as untrusted supply-chain inputs
- #58 — this enforcement-map work
