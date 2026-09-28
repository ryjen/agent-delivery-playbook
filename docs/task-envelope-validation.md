# Task Envelope Validation

The repository uses two independent validation paths:

1. a dependency-free smoke validator for the intentionally small checked-in YAML subset;
2. a standards-based validator using PyYAML and JSON Schema draft 2020-12.

## Reproducible Environment

`flake.nix` and `flake.lock` are the authoritative executable validation environment. The flake supplies Python plus the standards-based YAML and JSON Schema libraries used by CI and local focused checks.

`mise` is an orchestration/UX layer over that environment; it does not install or resolve validation dependencies.

## Local Commands

Run all validation directly through the flake:

```bash
nix flake check --print-build-logs
```

or through the repository task interface:

```bash
mise run validate
```

Run focused checks with:

```bash
mise run test
mise run validate-standard
mise run validate-lightweight
mise run validate-repository
```

## Lightweight Validator

`scripts/validate-task-envelopes.py` checks the checked-in examples without external dependencies. It supports only:

- indentation-based mappings;
- scalar values and booleans;
- inline empty lists and mappings (`[]` and `{}`);
- lists of scalars or small mappings;
- quoted scalar values;
- comments on otherwise empty lines.

It rejects duplicate or empty mapping keys, unexpected indentation, ambiguous scalar-list mappings, unknown risk/evidence levels, and malformed provenance fields.

This parser is intentionally not a general YAML implementation.

## Standards-Based Validator

`scripts/validate-task-envelopes-standard.py`:

- parses every example as real YAML using `yaml.SafeLoader` with duplicate-key rejection;
- verifies that the schema declares JSON Schema draft 2020-12;
- validates the schema itself with `Draft202012Validator.check_schema`;
- validates every envelope against `schemas/task-envelope.schema.json`;
- fails closed on unknown fields through the schema's `additionalProperties: false` rules;
- compares the standards-based parsed value with the lightweight parser output;
- reports parser drift when both paths interpret the same file differently.

The standards dependencies are supplied by the locked Nixpkgs input in `flake.lock`. Dependency/input updates should be isolated, reviewed, and validated in CI.

## What Validation Does Not Decide

Neither path infers semantic risk, determines whether evidence is sufficient, approves authority expansion, or replaces reviewer judgment.

## CI Posture

`.github/workflows/validate.yml` runs for pull requests and pushes to `main`. The workflow installs only the pinned Nix bootstrap action on the runner. Repository-specific Python and validation libraries come from the committed flake/lock state.

The `Repository integrity` and `Task envelopes` jobs build their corresponding flake checks. The task-envelope check runs all validator unit tests plus both lightweight and standards-based validators.

The workflow remains read-only, uses `pull_request` rather than `pull_request_target`, disables persisted checkout credentials, and SHA-pins third-party actions.

## Contributor Rule

Run `mise run validate` after changing:

- either task-envelope validator;
- validator tests;
- `flake.nix` or `flake.lock`;
- `schemas/task-envelope.schema.json`;
- task-envelope or golden-path examples;
- context/provenance fields.
