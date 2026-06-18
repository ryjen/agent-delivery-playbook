# Context Budget and Provenance

Context selection is a governance boundary. The files, documents, issues, logs, and summaries supplied to an agent shape what the agent can reason about and what authority it may appear to have.

A context budget is not only a token or cost limit. It is the approved boundary for what the agent may inspect, summarize, ignore, or escalate.

## Why this matters

Large-context execution can hide authority expansion. If an agent silently reads more repositories, stale documentation, unrelated tickets, or sensitive files, reviewers may not know which inputs shaped the change.

The task envelope should make context decisions visible enough for review.

## Context decision types

| Type | Meaning | Example |
| --- | --- | --- |
| Approved source | A repository, directory, file, issue, design doc, or log source allowed for the task | `src/auth/session.ts` |
| Included context | Source supplied directly to the agent | Current failing test and target module |
| Summarized context | Source condensed before use | Prior incident summary without raw customer data |
| Excluded context | Source intentionally not supplied | Production logs containing PII |
| Deferred context | Source not needed yet, but may be requested if blocked | Architecture RFC for unrelated subsystem |
| Escalated context | Additional context requested after execution begins | CI secrets workflow requires maintainer approval |

## Minimal ledger shape

```yaml
context:
  repositories:
    - example-app
  references:
    - issue: APP-1234
  provenance:
    approved_sources:
      - README.md
      - package.json
    included:
      - README setup section
      - package.json scripts
    summarized:
      - none
    excluded:
      - path: .github/workflows/
        reason: CI changes are outside this T1 task
    deferred:
      - docs/deployment.md
    escalations:
      - source: .github/workflows/ci.yml
        reason: Would require CI-scope reclassification
        status: not_requested
    model_context_assumption: Small documentation task; no large-context retrieval required.
    stale_context_caveats:
      - README may lag implementation; package.json is treated as source of truth for scripts.
```

## Reclassification triggers

Stop and reclassify when context expansion would require:

- reading sensitive paths that were not approved;
- adding write access where only read access was authorized;
- crossing repositories or workspaces;
- using production logs, customer data, secrets, signing materials, or credentials;
- changing from documentation to runtime behavior;
- weakening evidence because the approved context was insufficient;
- relying on summarized context for a high-risk decision without owner review.

## Reviewer questions

- Does the PR evidence list the context that shaped the change?
- Were excluded or deferred sources reasonable?
- Did the agent need context that would have changed the risk tier?
- Are stale-context caveats visible?
- Does the evidence distinguish actual inspection from model inference?

## Good-enough manual use

For T1/T2 tasks, a short context/provenance note in the task envelope or PR evidence is usually enough.

For T3/T4 tasks, keep a fuller ledger and require explicit approval before context expansion.

## Production-grade direction

Production-grade enforcement may validate envelope fields, require sensitive-path approval, preserve CI artifacts, and store context ledgers with PR evidence. That should come after the manual policy shape is stable.