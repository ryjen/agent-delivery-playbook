# Task Envelope Validation

This repository includes a lightweight local validator for task envelope examples:

```bash
python3 scripts/validate-task-envelopes.py
```

The validator checks envelope examples in `examples/task-envelope/` and golden-path bundle envelopes under `examples/golden-path/**/task-envelope.yaml` against the structural expectations in `schemas/task-envelope.schema.json`.

## What It Checks

- required top-level sections exist;
- `classification.risk_tier` is one of `T1`, `T2`, `T3`, or `T4`;
- the schema declares either `evidence.required_level` or `evidence.required_levels`;
- evidence levels are one of `E1`, `E2`, `E3`, or `E4`;
- the schema `$id` does not use the `example.com` placeholder;
- nested context/provenance examples can be parsed by the repository's supported YAML subset;
- malformed example structure fails with a path and reason.

## What It Does Not Check

This script is intentionally not a full YAML parser, JSON Schema implementation, or policy engine.

It does not infer semantic risk, decide whether evidence is sufficient, or replace reviewer judgment.

## Expected Failure Modes

Validation should fail when an example:

- omits a required section;
- uses an unknown risk tier;
- uses an unknown evidence level;
- has malformed YAML in the subset used by the examples;
- drifts from the schema's expected evidence field;
- adds a nested envelope shape the local validator cannot parse.

## CI Posture

Validation is documented as a local/manual command for now. Making it advisory or blocking in CI should be handled by the policy-to-CI enforcement strategy.

## Contributor rule

Run the validator after changing:

- `schemas/task-envelope.schema.json`;
- `examples/task-envelope/*.yaml`;
- `examples/golden-path/**/task-envelope.yaml`;
- context/provenance ledger fields.