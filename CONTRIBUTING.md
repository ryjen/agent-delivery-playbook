# Contributing

Contributions should preserve the repository's central invariant: agent-assisted delivery must remain bounded by explicit authority, review, and evidence rather than trusted by default.

## Before Starting

Use an existing issue when one covers the work. For material design changes, open or update an issue before implementation so scope, terminology, and compatibility impact are visible. Add or update an [architecture decision record](docs/adr/README.md) when a security/authority boundary, schema/compatibility contract, or established governance principle changes or needs an explicit trade-off; routine edits do not need an ADR. An ADR is a decision history, not an alternative policy or provider configuration.

A contribution should state:

- the problem being solved;
- the affected artifact or trust boundary;
- whether the change is normative policy, guidance, template, schema, example, or tooling;
- security and compatibility implications;
- how the result will be validated.

Keep this repository standalone. Do not require another project, hosted service, proprietary agent runtime, or vendor-specific control unless the contribution is explicitly an optional integration example.

## Development Setup

The repository owns its executable validation environment through a Nix flake. `mise` remains the convenient task entry point but does not own dependency resolution.

Prerequisite: Nix with flakes enabled.

Run the complete validation suite:

```bash
nix flake check --print-build-logs
```

or equivalently:

```bash
mise run validate
```

Focused commands are also available:

```bash
mise run test
mise run validate-standard
mise run validate-lightweight
mise run validate-repository
```

Focused `mise` tasks enter the flake-owned development environment so local and CI validation use the same Python and standards-validation dependencies.

The equivalent commands and environment contract are documented in [`docs/task-envelope-validation.md`](docs/task-envelope-validation.md).

## Contribution Boundaries

### Documentation and policy

- Distinguish normative requirements from guidance and examples.
- Use the [canonical glossary](docs/glossary.md) for governance terminology; link to a canonical heading rather than creating competing definitions.
- Review the glossary and relevant normative documents whenever a term, alias, risk/evidence identifier, or authority boundary changes; document migration and deprecated naming where applicable.
- Run the glossary consistency check through the flake suite (or `python3 scripts/validate-glossary.py`); it checks structural drift, not semantic agreement.
- Avoid claims stronger than the repository's demonstrated enforcement.
- Include realistic failure modes, escalation paths, and rejection outcomes.
- Keep examples synthetic and free of secrets or personal data.

### Schemas and examples

- Treat schema fields and enum values as compatibility-sensitive interfaces.
- Update all affected examples and documentation in the same pull request.
- Add positive and negative tests for new validation behavior.
- Preserve duplicate-key rejection and fail-closed handling of unknown fields.
- Do not weaken `additionalProperties: false` without an explicit design decision.

### Validation tooling and CI

- Prefer deterministic, auditable checks.
- Keep workflow permissions at least privilege.
- Do not use `pull_request_target` to execute pull-request code.
- Disable persisted checkout credentials unless a justified write operation requires them.
- Pin third-party Actions to immutable commit SHAs.
- Keep validation dependencies in the repository flake/lock state and isolate dependency updates for review.
- Never introduce production secrets into validation jobs or fixtures.

## Pull Requests

Keep pull requests focused and reviewable. Include:

- summary and motivation;
- changed behavior and affected artifacts;
- threat-model or security impact;
- validation evidence;
- compatibility or migration notes;
- follow-up work intentionally left out.

Draft pull requests are appropriate for incomplete work. Mark a pull request ready only when its intended checks pass and its documentation matches the implemented behavior.

## Provider admission (current status)

The GitHub default-branch ruleset now **configures** required pull requests and the two stable jobs (`Repository integrity` and `Task envelopes`) as strict admission gates with no bypass actors. This is verified by a live ruleset readback and deliberately failing [PR #87](https://github.com/ryjen/agent-delivery-playbook/pull/87), which GitHub blocked with `mergeable_state: blocked`. Missing-check/direct-push paths were not independently tested; administrative ruleset changes remain a separate high-trust boundary. See [`docs/operations/main-admission.md`](docs/operations/main-admission.md). Do not weaken checks, treat a model review as provider approval, or use administrator authority to bypass the proof.

## Validation Expectations

At minimum, run:

```bash
mise run validate
```

Changes to validators should include unit coverage. Changes to schemas should include valid and invalid fixtures or tests. Changes to workflows should be reviewed for token permissions, event safety, credential persistence, third-party actions, and untrusted-code execution.

A passing validator proves structural conformance only. It does not prove that risk classification, evidence sufficiency, authority, or approval decisions are semantically correct.

## Commit and Review Guidance

- Use concise, outcome-oriented commit messages.
- Do not mix unrelated cleanup into functional changes.
- Resolve review feedback with code, tests, or documentation rather than commentary alone.
- Preserve reviewer independence for changes that alter security policy, authorization semantics, CI authority, or evidence requirements.

## Security Reports

Do not disclose credible vulnerabilities or governance bypasses in a public issue. Follow [`SECURITY.md`](SECURITY.md).

## Code of Conduct

No separate code of conduct is currently adopted. Participate professionally, focus review on the work and its risks, and avoid including confidential or personally identifying information.