# Secure Agent Workflows

Practical patterns, templates, and threat models for secure AI-assisted software delivery.

This repository treats AI coding agents as semi-autonomous delivery participants, not smarter autocomplete. The goal is to help senior engineers, platform teams, AppSec teams, and mobile/client teams adopt coding agents without weakening delivery controls.

## Project goals

- Codify repeatable, bounded agent delivery workflows for software engineering teams.
- Make AI-assisted delivery safer, more consistent, and easier to review.
- Provide practical controls for task scoping, context curation, sandboxing, credentials, evidence, and rollback.
- Bridge agent workflows into normal engineering systems such as GitHub, CI/CD, local development environments, and review gates.
- Move from ad hoc chat prompts to durable workflow definitions with clear inputs, outputs, controls, and ownership.

## Non-goals

- Career workflows, resume tailoring, recruiter replies, or application tracking.
- Replacing Hermes, n8n, GitHub Actions, CI/CD platforms, or existing SDLC governance.
- Becoming a generic prompt dump, chatbot recipe collection, or agent framework.
- Encouraging autonomous merge, release, credential, or production access without human accountability.

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

Agents can accelerate work, but they also introduce new failure modes: over-broad changes, hidden dependency updates, credential exposure, generated code that bypasses architectural constraints, fabricated evidence, and insecure defaults. This repository gives teams reusable controls rather than generic advice.

## Repository map

| Path | Purpose |
| --- | --- |
| `docs/secure-coding-agent-workflow.md` | End-to-end secure agent workflow |
| `docs/threat-model.md` | Threat model for agent-assisted delivery |
| `docs/task-risk-matrix.md` | Risk tiers and required controls |
| `docs/mobile-agent-safe-checklist.md` | Mobile/client-specific guardrails |
| `templates/` | Drop-in repo templates for agent instructions and review controls |
| `examples/` | Example task and PR contracts |
| `diagrams/secure-agent-workflow.mmd` | Mermaid workflow diagram |

## Recommended adoption path

1. Copy `templates/AGENTS.md` into the target repository root
2. Add `templates/SECURITY_INVARIANTS.md` and adapt it to the system
3. Use `docs/task-risk-matrix.md` to classify agent tasks before execution
4. Require `examples/agent-task-contract.md` for medium/high-risk agent work
5. Add `templates/REVIEW_CHECKLIST.md` to PR review expectations
6. Move repeated controls into CI, pre-commit hooks, branch protection, and release gates

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
- Make rollback boring
- Keep humans accountable for merge and release decisions

## Status

Early public starter structure. Expect the templates to evolve as teams apply them to real repositories and CI/CD systems.
