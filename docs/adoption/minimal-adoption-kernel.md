# Minimal Adoption Kernel

Use this profile when adopting the playbook into an existing repository. The objective is the smallest control set that makes agent-assisted work bounded, reviewable, and attributable without applying every artifact to every task.

## Five kernel concerns

Every meaningful write-capable task must resolve:

1. **Bounded intent** — requested outcome, non-goals, scope, and accountable owner.
2. **Risk classification** — highest applicable tier and why.
3. **Authority and tool constraints** — allowed reads/writes/tools/effects plus explicit prohibitions.
4. **Evidence requirements** — observable evidence required for the tier and any unverified claims.
5. **Accountable review and outcome** — who or what may accept, reject, escalate, or merge under repository policy.

These are logical concerns, not five mandatory documents. Existing issues, PR templates, repository permissions, CI, and review controls may represent them when they are equivalent or stronger.

## Smallest sufficient profile

| Tier | Smallest sufficient representation | Evidence | Review / execution posture |
| --- | --- | --- | --- |
| T1 | Short inline scope + risk + prohibitions in issue/PR; no standalone envelope required by default | E1; tests only if executable behavior changes | Lightweight accountable review under repo policy; no privileged effects |
| T2 | Structured task envelope; explicit allowed/disallowed paths/tools | E2 + stated gaps + rollback | Owning-team review; scoped write/tool authority |
| T3 | Task envelope; explicit approval before sensitive execution; bounded capabilities; operational/rollback plan | E2 + E3 | Agent assistive/tightly constrained; owner/platform/security review as applicable |
| T4 | Task envelope as governance record; privileged/destructive execution remains human-led | E2 + E3 + E4 for the resulting human-led change | Agent may inspect, plan, draft tests/checklists, and summarize; it does not directly exercise restricted authority |

Informational/read-only work corresponds to Tier 0 in the risk matrix and does not require a write-task envelope. The current machine-readable envelope schema represents T1-T4 write-capable work.

## Risk-triggered extensions

| Extension | Add it when |
| --- | --- |
| Context provenance ledger | external/retrieved/tool-provided context materially influences the change or may be stale, untrusted, private, or contradictory |
| Capability catalog | recurring or multi-tool authority needs durable review; shell/network/write/dependency/CI/external-system effects are material |
| Tool-call decision record | a material external effect, authority expansion, sensitive boundary, or explicit approval decision exists |
| Replayable evidence bundle | T2+ work, incident reconstruction, nondeterministic execution, or evidence cannot be understood from the diff alone |
| Specialist security/platform review | auth, authorization, secrets, privacy, crypto, CI/CD, release, signing, deployment, privileged infrastructure, or production data |
| Trusted/signed/independent evidence | producer self-certification is insufficient or T3/T4 policy requires a stronger producer/verifier boundary |
| Rollback rehearsal | rollback is stateful, destructive, migration-sensitive, operationally complex, or uncertain |
| Enhanced approval | T3/T4 effects, authority expansion, governance self-modification, exceptions, or break-glass paths |
| Sensitive-path gate | a small diff can materially change a protected boundary |

An extension may be satisfied by an existing repository mechanism. Do not copy this repository's template merely to prove that an artifact exists.

## Complexity budget

- **T1:** one issue/PR should normally be enough. Do not require capability catalogs, provenance ledgers, replay bundles, or attestations without a real trigger.
- **T2:** normally one structured envelope plus one evidence section. Specialist review and operational exercises are trigger-driven.
- **T3:** spend additional process on affected trust boundaries: authority, provenance, operational evidence, rollback, and independent review.
- **T4:** spend process controlling the human-led privileged change; paperwork does not make restricted agent execution safe.

Policy-theatre warning signs:

- every task copies every template regardless of risk;
- a docs edit carries the same evidence burden as an auth/CI change;
- reviewers check boxes that do not correspond to observable properties;
- model-generated summaries count as independent evidence;
- nobody can explain which risk triggered an artifact;
- process grows while effective runtime authority remains broad.

Prefer deleting an unnecessary artifact over institutionalizing it.

## Intentional omission

An optional artifact may be omitted when:

1. no documented trigger applies;
2. the concern is already represented by an existing repository control or is genuinely not applicable;
3. omission does not hide missing required evidence or authority;
4. a reviewer can reconstruct why the lighter path was sufficient.

Do not use `not applicable` after scope expansion to suppress a control that has become required.

## Examples

- **T1 documentation:** `../../examples/task-envelope/t1-doc-change.yaml` — standalone envelope optional for a one-off docs PR.
- **T2 localized bug fix:** `../../examples/task-envelope/t2-bugfix.yaml` — envelope + scoped tools + E2 regression evidence + owner review.
- **T3 CI change:** `../../examples/task-envelope/t3-ci-change.yaml` — approval before sensitive execution + E2/E3 + platform review + rollback notes.
- **T4 restricted authority:** `../../examples/task-envelope/t4-auth-change.yaml` — agent analysis/preparation only; privileged implementation stays human-led.

## Future starter bundle

A copyable starter bundle should stay intentionally small:

- `AGENTS.md`;
- active PR template;
- reviewer checklist;
- task-envelope schema plus minimal T1-T4 examples;
- minimal validation/conformance entry point;
- links to security/contribution guidance rather than duplicated organization policy where inheritance applies.

Repository-specific security invariants, CODEOWNERS, release policy, language tooling, CI details, and public/private topology remain explicit adoption decisions. Versioning/distribution of the starter bundle belongs to #43.

## Adoption rule

Start with this kernel manually. Promote repeated objective checks into CI/repository controls only after the team understands what each control proves.

The target is not maximum paperwork. It is the **smallest reviewable/enforceable control set that matches the actual risk**.