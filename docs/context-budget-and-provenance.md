# Context Budget and Provenance

Context selection is a governance boundary and a software-supply-chain boundary. Repository files, issues, PR comments, logs, web content, tool/MCP responses, retrieved documents, generated summaries, and persistent memory can all influence delivery decisions.

Treat those inputs as **observations**, not authority.

```text
source content != instruction authority
retrieval success != source trust
summary != source evidence
memory != current policy
prior approval != current authorization
```

A context budget is therefore not only a token/cost limit. It is the approved boundary for what may be inspected, retained, summarized, excluded, revoked, or escalated.

## Trust dimensions

Do not compress context trust into one label. Evaluate dimensions independently:

| Dimension | Question |
| --- | --- |
| Origin/provenance | Where did this input come from, and can that origin be established? |
| Authority | Is this source actually authoritative for the decision, or merely informative? |
| Freshness | Is it current, stale, unknown, superseded, or revoked? |
| Integrity | Is the exact content/revision/digest known where that matters? |
| Interpretation | Is this raw source content, a generated summary, or model inference? |
| Confidence | How confident is the interpretation or extraction? Confidence never grants authority. |
| Sensitivity | Does it contain secrets, personal/customer data, private IP, or security-sensitive topology? |
| Isolation | Which repository/project/tenant/task is allowed to receive it? |
| Retention | How long should it remain available, and how is invalidation/deletion handled? |

A source can be authentic but stale, current but non-authoritative, or authoritative but too sensitive to place in model context.

## Source content versus generated interpretation

Keep these distinct:

| Kind | Example | Default posture |
| --- | --- | --- |
| Source evidence | exact file/commit, issue comment, log entry, tool result, policy document | untrusted observation unless independently established as authoritative for the decision |
| Generated summary | condensed incident, retrieved-doc summary, memory synthesis | derived interpretation; preserve links/digests to sources and omission caveats |
| Inference | model conclusion about architecture, intent, risk, or likely state | claim requiring verification; never source evidence |
| Authority input | protected policy/config/approval identity used by enforcement | supplied through trusted control context, not inferred from natural-language content |

Generated summaries must not silently replace sources when the omitted detail could change a security, risk, or authorization decision.

## Threats

### Indirect prompt/context injection

Attacker-controlled repository text, issue/PR content, logs, web pages, tool responses, package metadata, or memory may contain instructions intended to redirect the model.

Controls:

- treat content as data by default;
- resolve allowed tools/resources/credentials outside observed natural language;
- preserve source identity around retrieved content;
- separate diagnostics/content from control fields;
- use deterministic policy/admission for consequential effects;
- add adversarial fixtures for important paths (#41).

### Staleness and supersession

Architecture docs, runbooks, tickets, prior reviews, cached retrieval results, or memories may contradict current code/policy.

Controls:

- bind important context to revision/digest where practical;
- record retrieval time or freshness caveats;
- prefer current protected policy/code over stale summaries;
- fail closed when freshness is required but cannot be established;
- explicitly revoke/supersede previously approved context.

### Omission and summary distortion

A generated summary can omit constraints, negative results, dissent, or qualifiers.

Controls:

- preserve source references;
- record what was summarized versus supplied raw;
- record material exclusions/deferred sources;
- require source inspection for high-risk decisions when summary loss is consequential;
- treat summary confidence as interpretation metadata, not authority.

### Cross-project or cross-tenant contamination

Persistent memory, retrieval indexes, shared workspaces, or copied context may introduce information from another project, tenant, customer, or task.

Controls:

- default-deny cross-project/tenant retrieval;
- bind memory/retrieval scope to repository/project/tenant/task identifiers;
- never use one tenant/project's sensitive context to influence another;
- require explicit approved expansion for cross-repository use;
- support invalidation when ownership/classification changes.

### Over-collection and retention

More context increases leakage, privacy, and governance risk.

Controls:

- minimize to task-relevant fields/sections;
- redact secrets, credentials, personal/customer data, and unnecessary logs;
- prefer references/hashes to copying sensitive payloads;
- record retention/deletion expectations for durable context/memory;
- do not retain source material merely because it was useful once.

### Hidden or malicious tool output

Tool stdout/stderr, provider diagnostics, MCP results, search snippets, and structured fields can influence reasoning even when not visible in the final change.

Controls:

- preserve tool/source provenance in observations;
- do not parse free-form diagnostics into authority-bearing fields;
- expose material hidden inputs in replayable evidence where they affected the result;
- fail closed on malformed security-relevant structure rather than repairing it permissively.

## Context decision types

| Type | Meaning | Example |
| --- | --- | --- |
| Approved source | Source allowed for the task; approval does not make its content authoritative | `src/auth/session.ts` |
| Included context | Source supplied/inspected | current failing test |
| Summarized context | Source condensed before use | incident summary without raw customer data |
| Excluded context | Intentionally not supplied | production logs with PII |
| Deferred context | Held back unless needed | unrelated architecture RFC |
| Escalated context | Additional context requested after execution begins | CI workflow requires owner approval |
| Revoked context | Previously approved/known source that must no longer influence the task | superseded runbook or invalidated memory |
| Stale/unknown context | Source with unresolved freshness risk | old design doc whose implementation status is uncertain |

## Task-envelope ledger shape

The task envelope records material context decisions, not every retrieval implementation detail.

```yaml
context:
  repositories:
    - example-app
  references:
    - README.md
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
      - path: production-logs/
        reason: Customer data is unnecessary for this task.
    deferred:
      - docs/deployment.md
    escalations:
      - source: .github/workflows/ci.yml
        reason: Would cross into CI authority.
        status: denied
    revoked:
      - source: docs/legacy-setup.md
        reason: Superseded by current package scripts.
        replacement: package.json
    stale_context_caveats:
      - README may lag implementation; package.json is authoritative for script names.
```

## Detailed source records

Where risk justifies it, an adopting system may preserve richer per-source metadata outside the task envelope:

- stable source/origin identifier;
- repository/ref/commit or object digest;
- retrieval/observation time;
- authority classification;
- freshness state: current / unknown / stale / revoked;
- raw / summary / inference classification;
- interpretation confidence and known omissions;
- sensitivity/data classification;
- project/tenant/task scope;
- retention/deletion rule;
- superseding/replacement source.

This playbook does not mandate a retrieval, memory, MCP, or vector-store schema.

## Expansion and revocation rules

Stop and reclassify or request approval when context expansion would:

- read unapproved sensitive paths;
- cross repository/project/tenant boundaries;
- introduce production/customer/secret/signing data;
- require stronger tools or credentials;
- change the task's semantic risk;
- rely on summaries rather than sources for a consequential decision.

Revoked context must stop influencing new decisions once revocation is known. If prior output materially depended on revoked context, mark that output/evidence stale and re-evaluate before merge/effect.

## Memory

Persistent memory is candidate context, not durable authority.

- Memory entries retain provenance and project/tenant scope where practical.
- Prior conclusions, approvals, or credentials do not become current authority through memory.
- Cross-project promotion requires an explicit owner/policy decision.
- Revoked or superseded memory must be invalidated or marked so consumers can fail closed where required.
- Generated memory summaries remain interpretations linked back to their sources.

## Privacy and retention

For context and memory:

- minimize sensitive content before model/tool ingress;
- redact credentials and secret-bearing diagnostics;
- avoid copying personal/customer data when identifiers or aggregates suffice;
- define retention appropriate to the task, audit need, and data policy;
- keep tenant/project boundaries intact;
- ensure deletion/invalidation propagates to derived summaries where required.

## Enforcement mapping

| Control | Human / policy judgment | Deterministic/advisory opportunity |
| --- | --- | --- |
| Source relevance/authority | Human/policy determines semantic authority | require source IDs/references; warn on unknown provenance |
| Injection/data-control separation | Policy defines allowed effects | hard-fail attempts to derive capabilities/credentials/targets from untrusted content where structured control exists |
| Freshness | Human judges semantic staleness | compare revisions/timestamps; hard-fail known revoked/mismatched required sources |
| Context expansion | Owner approves material expansion | detect undeclared repos/paths/tools where observable |
| Cross-project/tenant isolation | Owner defines allowed boundary | hard resource/tenant allowlists |
| Minimization/retention | Data owner defines necessity/retention | secret/PII filters, size limits, retention jobs |
| Summary/inference use | Reviewer judges omitted semantics | require source links and interpretation labels |

## Reviewer questions

- Which exact sources materially shaped the change?
- Which were raw sources versus summaries/inference?
- Could any source contain attacker-controlled instructions?
- Which source was authoritative for conflicting facts, and why?
- Are stale/unknown/revoked inputs visible?
- Was any context expansion approved by the correct authority?
- Did retrieval cross project/tenant/sensitivity boundaries?
- Were secrets/customer data minimized?
- Could hidden tool output have influenced the decision?
- Does replayable evidence preserve enough provenance to reconstruct material inputs?

## Good-enough versus stronger adoption

For low-risk work, a short provenance note and explicit exclusions may be enough.

For T3/T4 or sensitive-context work, use a fuller ledger, explicit expansion approval, exact source/revision binding where practical, project/tenant isolation, and revalidation when important sources become stale or revoked.