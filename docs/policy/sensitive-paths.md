# Sensitive Path Policy

Sensitive paths are repository locations that should raise the minimum task risk tier regardless of how small the diff appears.

This policy prevents high-risk work from being disguised as a small refactor, cleanup, or documentation update.

## Machine-Readable Companion

The structured companion policy lives at:

```text
policy/sensitive-paths.yaml
```

Use the Markdown document for human review guidance and the YAML file as policy input for future local validation or CI checks. The YAML does not enforce anything by itself.

Broad name-based patterns, such as `**/*auth*`, are review prompts unless a validator implements allowlists, downgrade handling, and human confirmation.

## Default Rule

If a changed file matches a sensitive path, the task MUST be classified at least as the minimum tier listed below.

If multiple rules match, use the highest tier.

## Policy Map

| Path Pattern | Minimum Tier | Required Evidence Levels | Review |
| --- | --- | --- | --- |
| `.github/workflows/**` | T4 | E2, E3, E4 | CI/security owner |
| `.github/actions/**` | T4 | E2, E3, E4 | CI/security owner |
| `**/*auth*` | T4 | E2, E3, E4 | security owner |
| `**/*authorization*` | T4 | E2, E3, E4 | security owner |
| `**/*permission*` | T4 | E2, E3, E4 | security owner |
| `**/*secret*` | T4 | E2, E3, E4 | security owner |
| `**/.env*` | T4 | E2, E3, E4 | security owner |
| `**/Dockerfile` | T3 | E2, E3 | runtime owner |
| `docker-compose*.yml` | T3 | E2, E3 | runtime owner |
| `infra/**` | T4 | E2, E3, E4 | infra owner |
| `terraform/**` | T4 | E2, E3, E4 | infra owner |
| `kubernetes/**` | T4 | E2, E3, E4 | infra owner |
| `helm/**` | T4 | E2, E3, E4 | infra owner |
| `migrations/**` | T3 | E2, E3 | data owner |
| `schemas/**` | T2 | E2 | code owner |
| `package.json` | T3 | E2, E3 | code owner |
| `package-lock.json` | T3 | E2, E3 | code owner |
| `pnpm-lock.yaml` | T3 | E2, E3 | code owner |
| `yarn.lock` | T3 | E2, E3 | code owner |
| `Cargo.toml` | T3 | E2, E3 | code owner |
| `Cargo.lock` | T3 | E2, E3 | code owner |
| `go.mod` | T3 | E2, E3 | code owner |
| `go.sum` | T3 | E2, E3 | code owner |

## T4 Examples

T4 is required for changes that can affect:

- authentication
- authorization
- secrets
- CI permissions
- deployment authority
- production data
- infrastructure state
- release signing
- audit logging

## Reviewer Guidance

Reviewers should challenge low-risk classifications when sensitive paths are present.

The question is not whether the diff is large. The question is whether the path gives the agent access to a high-impact control surface.

## Safe Downgrade Rule

A sensitive-path match MAY be downgraded only when all of the following are true:

1. the diff is clearly non-semantic;
2. the reviewer documents why the minimum tier does not apply;
3. no workflow, runtime, permission, or security behavior changes;
4. the downgrade is visible in the PR evidence.

Examples of possible downgrades:

- comment-only typo in a workflow file
- schema documentation note with no schema behavior change
- formatting-only lockfile normalization with reproducible evidence

Downgrades should be rare.