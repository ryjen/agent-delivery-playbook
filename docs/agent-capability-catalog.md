# Agent Capability Catalog

An agent capability catalog records what an agent or tool is allowed to do before it is trusted inside a delivery workflow.

Do not treat model identity as authority identity. A model name tells you what generated text. It does not tell you which credentials, tools, repositories, networks, or approval gates were available during execution.

## What to catalog

Catalog durable agent/tool configurations, not every prompt. Examples:

- coding assistant in an IDE;
- repository automation bot;
- CI workflow that can open PRs;
- MCP server exposed to an agent;
- local shell executor used by an agent;
- hosted agent service with GitHub permissions.

## Authority dimensions

| Dimension | Questions |
| --- | --- |
| Read authority | Which repositories, files, issues, docs, logs, or tickets can it read? |
| Write authority | Can it edit files, push branches, create PRs, apply labels, or change issues? |
| Execution authority | Can it run shell commands, tests, builds, package managers, or deployment tools? |
| Credential authority | Which token class does it use: none, read-only, repo-scoped, CI-scoped, privileged? |
| Network authority | Can it call external services, package registries, SaaS APIs, or internal systems? |
| Approval authority | Can it approve, merge, release, or only propose? |
| Evidence authority | What artifacts must it produce before review? |

## Review cadence

Capability catalogs should be reviewed regularly because stale authority is a common agent risk.

| Authority level | Suggested cadence |
| --- | --- |
| Read-only docs/repo context | Quarterly or on repository ownership change |
| PR creation or issue mutation | Monthly or when workflow permissions change |
| Shell execution or CI token use | Monthly plus incident-driven review |
| Sensitive-path, secrets, release, or production-adjacent access | Per task or per change window |

## Minimum adoption path

1. Copy `templates/AGENT_CAPABILITY_CATALOG.md`.
2. Add one entry for each durable agent/tool configuration.
3. Link the catalog from the repo's `AGENTS.md` or engineering handbook.
4. Require catalog updates when tool permissions change.
5. Review stale entries during access reviews or SDLC control reviews.

## Boundary rule

Agents can use tools only through the authority granted to their configured runtime. A stronger model does not imply stronger authority, and a weaker model does not make broad credentials safe.