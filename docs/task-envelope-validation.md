# Task Envelope Validation

This repository includes a lightweight validator for task envelope examples.

Run the complete dependency-free validation baseline with:

```bash
mise run validate
```

Run only the validator unit tests with:

```bash
mise run test
```

The equivalent commands are:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate-repository.py
python3 scripts/validate-task-envelopes.py
```

The task-envelope validator checks examples in `examples/task-envelope/` and golden-path bundle envelopes under `examples/golden-path/**/task-envelope.yaml` against the structural expectations in `schemas/task-envelope.schema.json`.

## Supported YAML Subset

The dependency-free parser deliberately supports only the structures used by the checked-in examples:

- indentation-based mappings;
- scalar values;
- booleans `true` and `false`;
- inline empty lists and mappings (`[]` and `{}`);
- lists of scalars;
- lists of small mappings;
- single- or double-quoted scalar values;
- comments on otherwise empty lines.

It rejects duplicate mapping keys, empty keys, unexpected indentation, and structures outside this subset. Values containing a colon must be quoted when they are intended to remain strings.

## What It Checks

- required top-level sections exist;
- `classification.risk_tier` is one of `T1`, `T2`, `T3`, or `T4`;
- the schema declares either `evidence.required_level` or `evidence.required_levels`;
- evidence levels are one of `E1`, `E2`, `E3`, or `E4`;
- schema-compatible scalar lists contain only strings;
- keyed-looking scalar values such as `"issue: APP-1234"` are quoted instead of parsed as YAML objects;
- the schema `$id` does not use the `example.com` placeholder;
- nested context/provenance examples can be parsed by the repository's supported YAML subset;
- malformed example structure fails with a path and reason.

The unit test suite covers parser behavior, semantic validation, schema-field alignment, and example discovery using positive and negative fixtures generated in temporary directories.

The repository-integrity validator additionally checks:

- JSON files parse successfully;
- local Markdown links remain inside the repository and resolve to existing paths;
- Markdown files containing Mermaid fences do not have unbalanced fenced code blocks.

## What It Does Not Check

The task-envelope script is intentionally not a full YAML parser, JSON Schema implementation, or policy engine.

The dependency-free baseline does not infer semantic risk, decide whether evidence is sufficient, validate external links, or replace reviewer judgment. Standards-based YAML and JSON Schema validation are tracked separately.

## Expected Failure Modes

Validation should fail when an example:

- omits a required section;
- uses an unknown risk tier;
- uses an unknown evidence level;
- has malformed YAML in the subset used by the examples;
- repeats a mapping key;
- drifts from the schema's expected evidence field;
- places an object in a scalar-only list;
- adds a nested envelope shape the local validator cannot parse.

Repository-integrity validation should fail when:

- a JSON file cannot be parsed;
- a local Markdown link points outside the repository or to a missing path;
- a Markdown document has unbalanced code fences around Mermaid content.

## CI Posture

`.github/workflows/validate.yml` runs the validator unit tests and both dependency-free validators for pull requests and pushes to `main`.

The workflow:

- declares read-only repository permissions;
- disables persisted checkout credentials;
- pins actions to immutable commit SHAs;
- cancels superseded runs for the same pull request or ref;
- uses stable `Repository integrity` and `Task envelopes` job names suitable for branch protection.

Subjective policy interpretation remains a human review responsibility.

## Contributor Rule

Run `mise run validate` after changing:

- `scripts/validate-task-envelopes.py`;
- `tests/test_validate_task_envelopes.py`;
- `schemas/task-envelope.schema.json`;
- `examples/task-envelope/*.yaml`;
- `examples/golden-path/**/task-envelope.yaml`;
- context/provenance ledger fields;
- Markdown links or diagrams;
- JSON policy or schema artifacts.
