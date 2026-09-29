# Identity, Delegation, and Capability Grants

This document defines the vendor-neutral identity and delegation model used by the playbook.

The task envelope describes **intended work**. A capability grant describes **effective delegated authority** for one bounded execution window. Neither a prompt nor a self-declared identity authenticates the runtime.

## Core invariants

```text
task intent != runtime authority
model identity != runtime identity
runtime identity != accountable principal
declared identity != verified identity
possession of a tool != permission to use it
retry != new authority
delegation cannot widen its parent grant
verification != approval
```

## Identity layers

| Identity | Meaning | Typical evidence source |
| --- | --- | --- |
| Accountable principal | Human or service principal responsible for the task/decision | IdP/session, repository identity, signed approval, organization record |
| Runtime identity | Concrete agent/executor process or service instance exercising capabilities | workload identity, runner identity, service account, local runtime/session identity |
| Invocation/workflow identity | One execution attempt, workflow run, job, session, or resumed attempt | workflow/run ID, session ID, invocation UUID |
| Model/runtime metadata | Model/provider/runtime version useful for reproducibility or incident analysis | runtime/provider metadata; informational unless independently protected |
| Reviewer/approver identity | Principal authorized by policy to accept risk or approve a transition | protected review/approval system |
| Verifier identity | CI, test runner, security scanner, or reviewer producing independent evidence | protected workflow/runner/review record |
| Release/admin identity | Principal/system allowed to promote, administer, or perform restricted effects | release system or privileged control plane |

Logical roles remain distinct even when an implementation reuses infrastructure.

## Capability-grant tuple

A grant should answer **who may do what, to which subject, for which task, until when, under whose authority**.

```text
grant = {
  grant_id, accountable_principal, runtime_identity, invocation_identity,
  task_envelope_id, task_envelope_digest,
  repository_or_workspace, ref_scope, code_subject,
  allowed_capabilities, prohibited_capabilities,
  credential_scope, network_scope,
  issuer, approval_record, issued_at, expires_at,
  revocation_state, parent_grant_id
}
```

### Binding rules

- Bind the grant to the task-envelope identifier and, where practical, an immutable envelope digest.
- Bind repository/workspace plus readable/writable ref/path scope; protected refs remain explicit denials.
- Bind authority to a base/head commit, patch digest, artifact digest, or equivalent code subject when code state matters.
- Enumerate effects, not vague tool names alone. `GitHub access` is weaker than `create/update PR on branch X; no merge/ruleset/secret/admin effects`.
- Use short-lived grants so task completion or abandonment does not leave ambient authority.
- Identify issuer/approver independently from the runtime receiving the grant.
- Bind approvals to the exact grant/effect/resource where policy requires approval.

A model name, prompt, issue body, README, tool response, or agent-produced field is not authenticated identity evidence by itself.

## Expiration and revocation

Authority ends when the task completes, expiry is reached, the owner/policy revokes it, runtime identity changes materially, task scope/risk changes, code/ref moves outside the approved binding, or a security event invalidates the grant.

Revocation should disable future effects and, where practical, invalidate the credential/capability that enabled them. A model-visible `revoked` field alone is not enforcement.

## Retries and resumed sessions

A retry is a new **invocation identity**, not a new permission set. A retry may reuse a still-valid grant only if task, repository/ref/code subject, capability scope, runtime class, and expiry remain valid and policy permits reuse.

A resumed chat/session must re-establish current grant state. Transcript history is not live authorization.

## Nested delegation and specialists

For parent grant `G` and child grant `C`:

```text
capabilities(C) subset-of capabilities(G)
resources(C)    subset-of resources(G)
time(C)         subset-of time(G)
credential(C)   no-stronger-than credential(G)
approval(C)     cannot exceed approval(G)
```

Additional rules:

- child runtime and invocation identity are distinct;
- parent grant ID is recorded;
- child scope is equal or narrower;
- a runtime cannot mint approval, merge, release, admin, secret, or production authority it did not receive;
- delegation depth may be bounded;
- child results return as evidence/observations, not authority;
- a specialist cannot authorize a supervisor to exceed the original grant.

If broader access is required, stop and escalate to the accountable issuer/owner.

## No self-expansion

A runtime may **request** broader capability. It may not approve its own request.

Expansion requires a new or superseding grant issued by an authority independent of the requesting runtime. Editing the task envelope, catalog, prompt, or tool-call record does not enlarge effective permission.

## Authority-role separation

| Authority | Agent runtime posture |
| --- | --- |
| Generate/recommend | Allowed |
| Repository read | Allowed when bounded |
| Repository write | Allowed when branch/path scoped |
| Execute tests/builds | Allowed with command/credential/network limits |
| Verification | Independent requirements need a distinct verifier |
| Approval/risk acceptance | Human/service policy role; separate by default |
| Merge | Separate policy decision; not inherited from PR/write authority |
| Release/deploy | Existing pre-approved gates only |
| Secrets/admin/restricted production effects | Human-led for T4 |

Generation, verification, approval, release, and administration authorities must not be silently collapsed into one token/runtime.

## Declarations versus verified facts

Catalogs/grants may contain declarations such as runtime name, requested tools, task ID, or model version. Depending on platform, independently verifiable facts may include authenticated human/workload identity, token scope, protected workflow run ID, exact commit/artifact digest, credential expiry, branch protection, and approval records.

When a fact cannot be independently verified, label it as declared/observed rather than trusted identity evidence.

## Relationship to the task envelope

The task envelope remains the canonical **intent and governance record**. Runtime authentication, invocation identity, credential scope, expiry, revocation, retries, and nested delegation stay outside the current task-envelope schema.

This is deliberate: an envelope cannot authenticate a runtime merely by naming it, and grant facts vary per invocation while task intent may remain stable. A grant should reference `task_envelope_id` plus an immutable digest where practical.

A future envelope schema may add a non-authoritative grant reference only if real adoption shows that it improves traceability without confusing intent with authority.

## Relationship to the capability catalog

The capability catalog describes durable configuration and maximum expected authority.

```text
effective task grant subset-of durable catalog profile
```

The catalog is a ceiling, not task authorization.

## Relationship to tool-call decisions

Material tool-call decisions should reference grant and invocation IDs when available. A Tool Call Decision Record may approve use already inside a grant, deny, defer, or escalate; it cannot widen the grant by itself.

## Examples

- `../examples/capability-grants/read-only.yaml`
- `../examples/capability-grants/write-limited.yaml`
- `../examples/capability-grants/denied.yaml`

These are illustrative governance records, not authorization tokens.

## Implementation neutrality

Adopting systems may use workload identity, OAuth, GitHub Apps, short-lived tokens, sandbox policy, capability tokens, local mediation, or human-controlled tool exposure. The playbook specifies required security properties, not a provider.