# Secure Agent Workflows

Practical patterns, templates, and threat models for secure AI-assisted software delivery.

This repository treats AI coding agents as semi-autonomous delivery participants, not smarter autocomplete. The goal is to help senior engineers, platform teams, AppSec teams, and mobile/client teams adopt coding agents without weakening delivery controls.

## Goals

- Provide a practical playbook for secure AI-assisted software delivery.
- Treat coding agents as constrained delivery participants inside normal SDLC controls.
- Define reusable workflows for bounded coding, testing, documentation, CI/CD triage, and repository maintenance tasks.
- Provide risk classification, task contracts, review checklists, and evidence expectations for agent-authored changes.
- Help teams preserve security, auditability, rollback paths, and human accountability when using coding agents.

## Non-goals

- General-purpose personal automation workflows.
- CareerOps, resume tailoring, recruiter messaging, or application tracking.
- Replacing Hermes, n8n, GitHub Actions, CI/CD systems, or human reviewers.
- Fully autonomous production deployment.
- Generic prompt collections unrelated to software delivery controls.

## Who this is for

- Senior, staff, and principal engineers introducing agent-assisted delivery
- Platform teams defining paved paths for AI coding tools
- AppSec teams reviewing agent risk, credentials, evidence, and auditability
- Mobile/client teams using agents in React Native, iOS, Android, and Kotlin Multiplatform repositories

## Core model

A secure agent workflow is a constrained delivery loop:

1. Define a bounded task
2. Provide curated repository context
3. Run the agent in a sandbox with scoped credentials
4. Require tests, evidence, and review notes
5. Apply normal SDLC gates
6. Preserve audit trails and rollback paths

Agents can accelerate work, but they also introduce new failure modes: over-broad changes, hidden dependency updates, credential exposure, generated code that bypasses architectural constraints, fabricated evidence, insecure defaults, stale context decisions, and approval collapse. This repository gives teams reusable controls rather than generic advice.

## AI-native SDLC concern

AI-assisted delivery changes the SDLC because the delivery artifact is no longer only source code.

Teams also need to govern:

- Prompts and task contracts
- Context supplied to agents
- Tool invocations
- Agent-generated plans and evidence
- Model/runtime metadata where practical
- Human approval records
- Audit and rollback paths

The repo's operating assumption is simple:

> Agents may propose, modify, test, and explain changes. Humans remain accountable for approval, merge, and release decisions.

## Repository map

For navigation by reader intent, see `docs/index.md`.

| Path | Purpose |
| --- | --- |
| `CONTRIBUTING.md` | Contribution boundaries, validation requirements, and review expectations |
| `SECURITY.md` | Vulnerability scope, private reporting guidance, and disclosure process |
| `.github/PULL_REQUEST_TEMPLATE.md` | Active governed PR template auto-applied by GitHub |
| `docs/index.md` | Documentation index and adoption map |
| `docs/architecture.md` | Canonical primitives, artifact authority, trust boundaries, control locations, and implementation limits |
| `docs/adoption/quickstart.md` | First 30-60 minute adoption path for one existing repo |
| `docs/ai-native-sdlc.md` | Governance concern for AI-native software delivery |
| `docs/secure-coding-agent-workflow.md` | End-to-end secure agent workflow |
| `docs/trust-model.md` | Identity, authority, and separation-of-duties model for agents and humans |
| `docs/agent-capability-catalog.md` | Guidance for documenting durable agent/tool authority |
| `docs/context-budget-and-provenance.md` | Context selection and provenance ledger guidance |
| `docs/replayable-evidence-envelope.md` | Replayable evidence envelope for agent-assisted PRs |
| `docs/delivery-evidence-standard.md` | Evidence standard for agent-assisted pull requests and workflows |
| `docs/threat-model.md` | Threat model for agent-assisted delivery |
| `docs/task-risk-matrix.md` | Risk tiers and required controls |
| `docs/governance-lifecycle.md` | Lifecycle rules for policies, templates, schemas, and examples |
| `docs/mobile-agent-safe-checklist.md` | Mobile/client-specific guardrails |
| `policy/` | Machine-readable policy artifacts for future validation |
| `templates/` | Drop-in repo templates for agent instructions and review controls |
| `templates/AGENT_CAPABILITY_CATALOG.md` | Drop-in template for agent/tool authority inventory |
| `examples/` | Example task and PR contracts |
| `diagrams/secure-agent-workflow.mmd` | Mermaid workflow diagram |

## Recommended adoption path

1. Start with `docs/adoption/quickstart.md` for the first manual adoption loop
2. Use `docs/index.md` to choose deeper reading paths
3. Read `docs/architecture.md` to understand artifact authority, trust boundaries, and current enforcement limits
4. Read `docs/ai-native-sdlc.md` to establish the governance concern
5. Copy `templates/AGENTS.md` into the target repository root
6. Add `templates/SECURITY_INVARIANTS.md` and adapt it to the system
7. Use `docs/task-risk-matrix.md` to classify agent tasks before execution
8. Require `examples/agent-task-contract.md` for medium/high-risk agent work
9. Use `docs/context-budget-and-provenance.md` for context expansion decisions
10. Use `docs/delivery-evidence-standard.md` and `docs/replayable-evidence-envelope.md` for PR evidence expectations
11. Apply `docs/trust-model.md` and `docs/agent-capability-catalog.md` when granting tool, repository, or CI access
12. Add `.github/PULL_REQUEST_TEMPLATE.md` or adapt it into the target repository's active PR template location
13. Add `templates/REVIEW_CHECKLIST.md` to PR review expectations
14. Move repeated controls into CI, pre-commit hooks, branch protection, and release gates only after the manual path stabilizes

## Good first use cases

- Test generation for well-scoped modules
- Documentation updates from existing code
- Dependency update preparation with human review
- Refactors constrained to one package or feature flag
- Static analysis finding remediation where the finding is already understood
- Mobile UI test scaffolding with explicit platform constraints

## Avoid as first use cases

- Authentication, authorization, cryptography, payment, or privacy-sensitive rewrites
- Broad architecture migrations without a human-authored plan
- Release automation changes without rollback testing
- Mobile build/signing/provisioning changes using production credentials
- Large dependency upgrades with transitive supply-chain risk

## Operating principles

- Bound the task before invoking the agent
- Provide only the context needed for the task
- Prefer read-only credentials by default
- Never expose production secrets to the agent runtime
- Treat agent output as untrusted until reviewed and tested
- Require evidence, not claims
- Separate generation from approval and release authority
- Make rollback boring
- Keep humans accountable for merge and release decisions

## Status

Early public starter structure. Expect the templates to evolve as teams apply them to real repositories and CI/CD systems.
