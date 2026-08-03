# Task Envelope Validation

The repository uses two independent validation paths:

1. a dependency-free smoke validator for the intentionally small checked-in YAML subset;
2. a standards-based validator using PyYAML and JSON Schema draft 2020-12.

## Local Commands

Install the pinned standards-validation dependencies once:

```bash
mise run install-validation
```

Run all validation:

```bash
mise run validate
```

Run focused checks with:

```bash
mise run test
mise run validate-standard
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

The standards dependencies are pinned in `requirements-validation.txt`. Dependency updates should be isolated, reviewed, and validated in CI.

## What Validation Does Not Decide

Neither path infers semantic risk, determines whether evidence is sufficient, approves authority expansion, or replaces reviewer judgment.

## CI Posture

`.github/workflows/validate.yml` runs for pull requests and pushes to `main`. The `Task envelopes` job:

- installs pinned validation dependencies;
- runs all validator unit tests;
- runs both lightweight and standards-based validators.

The workflow remains read-only, uses `pull_request` rather than `pull_request_target`, disables persisted checkout credentials, and SHA-pins third-party actions.

## Contributor Rule

Run `mise run validate` after changing:

- either task-envelope validator;
- validator tests;
- `requirements-validation.txt`;
- `schemas/task-envelope.schema.json`;
- task-envelope or golden-path examples;
- context/provenance fields.
