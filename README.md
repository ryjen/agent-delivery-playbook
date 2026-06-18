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

| Path | Purpose |
| --- | --- |
| `.github/PULL_REQUEST_TEMPLATE.md` | Active governed PR template auto-applied by GitHub |
| `docs/ai-native-sdlc.md` | Governance concern for AI-native software delivery |
| `docs/secure-coding-agent-workflow.md` | End-to-end secure agent workflow |
| `docs/trust-model.md` | Identity, authority, and separation-of-duties model for agents and humans |
| `docs/delivery-evidence-standard.md` | Evidence standard for agent-assisted pull requests and workflows |
| `docs/threat-model.md` | Threat model for agent-assisted delivery |
| `docs/task-risk-matrix.md` | Risk tiers and required controls |
| `docs/mobile-agent-safe-checklist.md` | Mobile/client-specific guardrails |
| `templates/` | Drop-in repo templates for agent instructions and review controls |
| `examples/` | Example task and PR contracts |
| `diagrams/secure-agent-workflow.mmd` | Mermaid workflow diagram |

## Recommended adoption path

1. Read `docs/ai-native-sdlc.md` to establish the governance concern
2. Copy `templates/AGENTS.md` into the target repository root
3. Add `templates/SECURITY_INVARIANTS.md` and adapt it to the system
4. Use `docs/task-risk-matrix.md` to classify agent tasks before execution
5. Require `examples/agent-task-contract.md` for medium/high-risk agent work
6. Use `docs/delivery-evidence-standard.md` for PR evidence expectations
7. Apply `docs/trust-model.md` when granting tool, repository, or CI access
8. Add `.github/PULL_REQUEST_TEMPLATE.md` or adapt it into the target repository's active PR template location
9. Add `templates/REVIEW_CHECKLIST.md` to PR review expectations
10. Move repeated controls into CI, pre-commit hooks, branch protection, and release gates

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
