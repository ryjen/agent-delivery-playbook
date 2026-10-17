# AI-Native SDLC Governance

Traditional SDLC assumes humans author changes, tools execute deterministic checks, and reviewers evaluate a bounded diff. AI-native delivery changes that model. Agents can plan work, assemble context, modify files, run tools, open pull requests, and produce review evidence.

This document defines the additional SDLC concern introduced when AI agents become delivery participants.

## External reference and terminology

The [AI Native Project AI Software Development Lifecycle](https://theainativeproject.org/ai-software-development-lifecycle/) and its handbook are useful external reference models for plan-first execution, structured context, lifecycle-wide AI participation, quality gates, governance, and engineering memory.

Kiro's [Frontier Engineering](https://kiro.dev/topics/frontier-engineering/) principles are a useful practitioner signal for agent-oriented codebases, short executable feedback loops, boundary-based trust, and continuous tuning of agent tooling. Treat them as non-normative industry guidance rather than empirical evidence; this playbook does not rely on Kiro's quantitative productivity claims.

This playbook does **not** import either framework as a second normative lifecycle. Their concepts map onto the existing task-envelope, risk, evidence, trust, learning-promotion, and governed-delivery contracts.

In particular:

- model output and agent findings are claims, not authority;
- verifier output is evidence, not authorization;
- persistent context and memory are untrusted inputs until governed where trust matters;
- human review/approval is selected by task risk and policy, not merely because AI participated;
- enforcement belongs at deterministic runtime, CI, repository, release, or governance boundaries rather than in prompting alone.

Use `docs/policy-enforcement-map.md` for the operational crosswalk from lifecycle concerns to current enforcement surfaces and owners.

## Practitioner crosswalk: Anthropic's AI-native SDLC playbook (2026-08-21)

Anthropic's [AI-native SDLC playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook) describes six connected stages (Plan, Design, Build, Test, Deploy, Maintain), versioned handoff artifacts, skills and hooks, layered review, continuous evaluation, and operational feedback. Those are **useful implementation patterns, not an additional normative lifecycle**. This repository remains vendor-neutral and retains its existing task, risk, evidence, trust, and enforcement contracts.

| Practitioner pattern | Adopt through existing playbook control | Limitation to preserve |
| --- | --- | --- |
| `intent.md` / `spec.md` / `plan.md` and committed handoffs | Bounded task contract; recorded acceptance criteria and revisions | A Git commit records a change; it does not prove intent, execution, or independent acceptance |
| Versioned skills, agent instructions, and context | Context provenance, policy ownership, controlled promotion | Instructions guide behavior, but are not a complete enforcement boundary |
| Hooks, managed permissions, and sandbox defaults | Capability catalog, scoped runtime identity, deterministic gates | A hook only mediates the paths it actually intercepts; alternate APIs, credentials, subprocesses and delegates require separate reachability proof |
| Agent reviewers and verifier subagents | Exact-subject E2/E3/E4 evidence and independent-verifier policy | Context or model separation alone does not prove independence when trust roots, oracles or permissions are shared |
| Continuous agent evaluations | Versioned, risk-triggered configuration regression profile (tracked in [#77](https://github.com/ryjen/agent-delivery-playbook/issues/77)) | Agent scores, LLM-as-judge assessments and self-written tests cannot replace independent executable evidence or approvals |
| Incident-to-intent feedback | Bounded read-only observation, claim/evidence separation, approved task intake | A diagnosis or report is a candidate claim, not permission to mutate a repository or production system |

### Qualification rules

1. **Authority is evaluated at the effect boundary.** A tool-call hook is valuable defence in depth, but claiming complete mediation requires enumerating and testing reachable equivalent effect paths. Every consequential path needs an enforceable policy boundary, including retries, alternate routes and delegated actions. See the [policy-enforcement map](policy-enforcement-map.md).
2. **Evidence is about an exact subject.** Retain candidate/base commit or artifact digest, verification plan and version, policy-relevant dependencies, verifier/runner trust identity, results, unsupported/indeterminate states, and approval references separately. A green check, signature, attestation or successful transport proves only the property actually measured; it cannot authorize its own promotion.
3. **Verification independence must be demonstrated.** A different prompt, process, subagent or model may catch errors, but independence requires inspecting common trust roots, who can change tests/oracles, how the candidate is materialized, and whether producer-owned authority can influence the verdict. Prefer deterministic and protected external checks for high-risk decisions.
4. **Configuration is a change surface.** When a prompt, skill, model, tool permission, context-building rule or verifier rubric changes, run proportionate before/after regression evaluations over frozen representative tasks, including adverse and incident-derived cases where available. Report abstentions and infrastructure failures rather than silently treating them as passes.
5. **Optimize for qualified outcomes, not code volume.** Evaluate throughput alongside escaped defects, rework, reviewer effort, false confidence, rollback/recovery, bypass findings, and evidence completeness. Use actual observed measurements; do not invent production quality claims or turn metrics into self-approval.

### Downstream implementation boundaries (informative, not dependencies)

- **Anthesis**: evidence-provenance and semantic-verifier sufficiency — [#139](https://github.com/hackelia-micrantha/anthesis/issues/139), [#199](https://github.com/hackelia-micrantha/anthesis/issues/199).
- **Dubnium**: bounded clean verifier execution, exact candidate identity, failure states and complete-mediation validation — [#896](https://github.com/ryjen/dubnium/issues/896), [#867](https://github.com/ryjen/dubnium/issues/867) (structural fixture; does not establish live proof), [#1632](https://github.com/ryjen/dubnium/issues/1632) (read-only pilot evaluation).
- **ops-cadence**: evidence-aware, source-health-safe, read-only portfolio observation — [#19](https://github.com/ryjen/ops-cadence/issues/19), [#44](https://github.com/ryjen/ops-cadence/issues/44).

The operational evaluation-profile template and measurement guidance belong in [#77](https://github.com/ryjen/agent-delivery-playbook/issues/77); this document establishes interpretation and ownership only.

## Core concern

AI-native SDLC governance answers:

> How do we preserve accountability, reviewability, provenance, and delivery safety when non-human actors participate in software delivery?

This is not only an AI tooling concern. It is a software supply-chain concern.

Agent-assisted delivery creates new artifacts that need governance:

- Prompts
- Task contracts
- Planning notes
- Context bundles
- Tool invocations
- Generated code
- Generated tests
- Review evidence
- Model and agent metadata
- Human approval records

If those artifacts are not controlled, the organization creates a shadow SDLC beside the existing one.

## Traditional delivery model

```mermaid
flowchart LR
    Human[Human developer] --> Code[Code change]
    Code --> Review[Human review]
    Review --> CI[CI and policy checks]
    CI --> Release[Release]
```

The dominant control assumptions are:

- The human author understands the intent.
- The diff is the primary artifact.
- Reviewers evaluate implementation and risk.
- CI validates known technical controls.
- Deployment authority is separated by branch protection, release gates, or change approval.

## Agentic delivery model

```mermaid
flowchart LR
    Human[Human operator] --> Intent[Intent and task boundary]
    Intent --> Agent[Delivery agent]
    Agent --> Context[Curated context]
    Agent --> Tools[Repository and build tools]
    Context --> Output[Generated changes and evidence]
    Tools --> Output
    Output --> Review[Human and automated review]
    Review --> Gates[SDLC gates]
    Gates --> Release[Release or rollback]
```

The new control problem is that the diff no longer tells the full story. Reviewers also need to understand:

- Why the agent made the change
- What context it used
- Which tools it invoked
- Whether it stayed within scope
- Whether the evidence is real and reproducible
- Which human accepted accountability for the change

## Required control points

### 1. Intent

Every meaningful agent task should start with a bounded intent.

Minimum fields:

- Goal
- Non-goals
- Allowed files or systems
- Disallowed files or systems
- Risk tier
- Review owner
- Required evidence

Use `examples/agent-task-contract.md` for medium and high-risk work.

### 2. Context

Context is part of the trusted computing base for agent-assisted delivery.

Teams should define:

- Which repository files were provided
- Which logs, issues, tickets, or external references were used
- Whether generated or retrieved context was stale
- Whether context came from trusted or untrusted sources
- Whether MCP/tool responses could influence code generation

Failure mode: an agent modifies production behavior based on stale docs, poisoned issue comments, fabricated tool output, or unrelated legacy code.

### 3. Identity and authority

Agents, humans, tools, and platforms should have distinct identities.

Avoid collapsing these into one broad token or shared workstation identity.

Recommended separation:

| Actor | Typical authority |
| --- | --- |
| Human operator | Defines intent, reviews, approves |
| Delivery agent | Proposes, edits, tests, explains |
| Tool runtime | Executes bounded commands |
| CI system | Validates and records evidence |
| Release system | Deploys through existing gates |

Agents should not self-approve their own work or hold production deployment authority.

### 4. Tool access

Agent tool access should be explicit and revocable.

Default posture:

- Read-only repository access before task approval
- Scoped write access after task approval
- No production secrets
- No cloud admin credentials
- No mobile signing keys
- Network disabled unless needed
- Dependency installation controlled by lockfiles

For sensitive tasks, require command allowlists and human approval before write or deployment operations.

### 5. Evidence

Agent evidence must be verifiable. A statement like "tests pass" is not sufficient unless it includes the actual command, environment, and result.

Expected evidence includes:

- Files changed
- Commands run
- Test results
- Static analysis results where relevant
- Security impact
- Scope exceptions
- Known risks
- Rollback path

Use `docs/delivery-evidence-standard.md` as the standard evidence shape.

### 6. Review and approval

Reviewers should treat agent output as untrusted generated code.

Review must verify:

- Scope stayed bounded
- Tests are meaningful
- Generated code follows local architecture
- Security invariants were preserved
- Dependency changes are intentional
- No secrets or sensitive data were exposed
- Rollback is realistic

Medium and high-risk work requires a human owner. Critical or restricted work remains human-led, with agents limited to planning, documentation, or checklist generation.

### 7. Audit and provenance

The organization should be able to answer:

- Who requested the task?
- What was the approved scope?
- Which agent or model produced the change?
- What context was provided?
- What tools were invoked?
- What evidence was produced?
- Who reviewed and approved the result?
- How can the change be rolled back?

This does not require heavyweight bureaucracy for every task. The evidence depth should scale with `docs/task-risk-matrix.md`.

## Governance requirements by risk tier

| Tier | Governance expectation |
| --- | --- |
| 0: Informational | Cite inspected files or sources; no writes |
| 1: Low | Normal review; basic evidence if files changed |
| 2: Medium | Task contract; scoped write access; CI evidence; human review |
| 3: High | Explicit approval; security/platform review; rollback plan; stronger evidence |
| 4: Restricted | Human-led execution; agent may assist with plans or docs only |

## AI-native SDLC failure modes

| Failure mode | Example | Control |
| --- | --- | --- |
| Shadow SDLC | Agent modifies code through side channels with no task record | Require task contracts and PR evidence |
| Context poisoning | Agent follows malicious issue comment or MCP response | Treat untrusted context explicitly; review context sources |
| Approval collapse | Same identity generates, approves, and deploys | Separate agent, human, CI, and release authority |
| Fabricated evidence | Agent claims tests passed without running them | Require command output or CI links |
| Scope creep | Agent changes unrelated modules | Allowed/disallowed paths and diff review |
| Secret exposure | Token pasted into prompt or logs | No production secrets in agent runtime |
| Supply-chain drift | Agent updates lockfiles or actions silently | Dependency and workflow diff review |
| Irreversible change | Agent executes migration or deletion | Human-led execution for restricted tasks |

## Good enough vs production-grade

Good enough for experimentation:

- Human prompts agent with a small task
- Agent opens a diff
- Human reviews and runs local tests

Production-grade for durable teams:

- Task risk classification
- Written task contracts for meaningful work
- Scoped identity and permissions
- Preserved evidence
- CI-backed validation
- Human accountability for merge and release
- Audit trail for agent-assisted changes

## Relationship to existing docs

Use this document with:

- `docs/secure-coding-agent-workflow.md` for the end-to-end loop
- `docs/task-risk-matrix.md` for risk classification
- `docs/threat-model.md` for adversarial thinking
- `docs/delivery-evidence-standard.md` for PR and workflow evidence
- `docs/trust-model.md` for identity and authority boundaries
