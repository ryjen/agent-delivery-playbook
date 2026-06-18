# Adoption Quickstart

Use this quickstart to apply the playbook to an existing software repository in the first 30-60 minutes. The goal is not to automate everything; the goal is to make one agent-assisted change bounded, reviewable, and replayable.

## Starting assumption

You have an existing repository with normal human review and CI. You want to let an AI coding agent help with one small task without giving it broad authority.

## Step 1: Copy the minimum controls

Copy or adapt these files first:

| Source | Target | Why |
| --- | --- | --- |
| `templates/AGENTS.md` | repository root | Persistent agent instructions and boundaries |
| `templates/SECURITY_INVARIANTS.md` | repository root or docs/security | System-specific constraints the agent must not violate |
| `.github/PULL_REQUEST_TEMPLATE.md` | active PR template location | Evidence and review structure |
| `templates/REVIEW_CHECKLIST.md` | reviewer docs or PR checklist | Human review expectations |

Good-enough manual adoption is acceptable at this stage. Do not start by building custom policy engines, autonomous merge flows, or broad agent permissions.

## Step 2: Pick one low-risk task

Choose a task that is easy to bound and easy to review.

Good first task:

```text
Update README setup instructions to match the current npm scripts.
```

Avoid as the first task:

```text
Modernize authentication, update dependencies, and fix CI.
```

The first task is documentation-only and should classify as `T1`. The second crosses auth, dependencies, and CI, so it needs decomposition and likely higher controls.

## Step 3: Classify the task

Use `docs/task-risk-matrix.md`.

For the README update:

| Field | Value |
| --- | --- |
| Task type | docs |
| Risk tier | T1 |
| Required evidence | E1 |
| Review | lightweight human review |
| Sensitive paths | not applicable unless docs describe secrets, auth, release, or production operations |

If classification changes during execution, stop and update the envelope before continuing.

## Step 4: Fill a small task envelope

For T1 work, the envelope can be short, but it still needs objective, scope, prohibited actions, evidence, and review.

```yaml
task:
  id: ADOPT-001
  title: Update README setup instructions
  objective: Align README setup commands with existing package scripts.
  owner: repo-maintainer

classification:
  type: docs
  risk_tier: T1

context:
  repositories:
    - example-app
  references:
    - README.md
    - package.json

constraints:
  allowed:
    - inspect README.md
    - inspect package.json scripts
    - update setup instructions
  prohibited:
    - changing package scripts
    - editing CI workflows
    - adding dependencies

execution:
  tools:
    - repo_read
    - editor
  actions:
    - inspect
    - patch
    - summarize

evidence:
  required_levels:
    - E1
  tests:
    - markdown review
  artifacts:
    - PR diff

review:
  required: true
  approvers:
    - human-maintainer
  notes: Documentation-only; no runtime behavior changes.

status: proposed
```

## Step 5: Run the agent inside the envelope

Give the agent only the files and instructions required for the task.

The agent may:

- inspect the approved files;
- propose a minimal patch;
- summarize what changed;
- report checks it actually performed.

The agent must not:

- modify scripts to make docs easier;
- change CI or package-manager configuration;
- claim tests ran when they did not;
- broaden the task without approval.

## Step 6: Open the PR with evidence

Use the governed PR template. For this example, the evidence can be simple:

```text
command/check: manual diff review
result: README commands match package.json scripts
scope: README setup section and package.json scripts only
```

Unsupported claims must be marked as unverified rather than omitted. For example:

```text
Full setup was not executed locally; command accuracy was verified against package.json only.
```

## Step 7: Human approval remains the gate

Humans remain accountable for merge and release decisions. The agent may prepare the change and evidence, but it does not approve its own work.

## Good-enough vs production-grade

| Adoption level | What to do |
| --- | --- |
| Good-enough manual | Copy templates, classify tasks manually, require PR evidence, and keep human merge control |
| Production-grade CI enforcement | Validate task envelopes, check required PR sections, enforce sensitive-path review, and preserve audit artifacts |

Move to CI only after the manual path is stable. Premature automation can hide policy drift instead of reducing it.

## What not to automate first

- merge approval;
- release promotion;
- production credential access;
- broad dependency upgrades;
- auth, cryptography, payment, privacy, or signing changes;
- policy reclassification decisions.

Start with bounded execution, visible evidence, and boring rollback. Then promote repeated controls into CI or repository policy.