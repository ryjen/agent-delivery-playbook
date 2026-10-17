# Lightweight governed-delivery conformance kit

**Status:** pilot, read-only local/CI prototype. Versioned output: `playbook.conformance-report.v1`. It is not the Anthesis policy engine, a runtime verifier, a release gate or an authorization service.

## Contract and execution

The canonical implementation is `scripts/conformance-kit.py`; it **reuses** existing PyYAML/JSON Schema and repository-integrity validators plus `policy/sensitive-paths.yaml` from the pinned playbook checkout. Python is retained for this existing validator ecosystem; there is no separately tracked replacement plan for this script.

```bash
# In the checked-out playbook repository, using its pinned flake:
nix develop --command python3 scripts/conformance-kit.py --root . --integrity --format json
nix develop --command python3 scripts/conformance-kit.py --root . --integrity --format markdown

# In an adopter repository, invoking the pinned playbook script:
python3 /path/to/pinned/playbook/scripts/conformance-kit.py \
  --root . --envelope path/to/task-envelope.yaml \
  --changed-path .github/workflows/build.yml \
  --manifest .governed/adoption.json \
  --format json
```

For an adopter, install/use the canonical playbook Nix development shell, which already supplies `pyyaml` and `jsonschema`. Never fetch `main` or install unpinned tool versions inside CI as a workaround. The script does not run `git`, execute arbitrary tasks or touch network/credentials.

## Objective checks

| Check ID | Rule | Boundary |
| --- | --- | --- |
| `task_envelopes` | Parse provided/discovered local YAML, validate current playbook JSON Schema and compare with lightweight parser | Structural envelope validity only; risk tier truth unverified |
| `reference_integrity` | Optional `--integrity`: reuse repository JSON syntax, local Markdown links and Mermaid fence checks | Does not audit contents or verify linked remote sources |
| `sensitive_paths` | Match explicit normalized `--changed-path` strings against **existing** sensitive-path policy | Matches are warnings, including broad keyword matches; no semantic approval or downgrade |
| `capabilities` | Validate the presence of nonempty `tools`, `resources`, `effects` lists in optional manifest | Does not check that a grant was actually enforced |
| `evidence_binding` | Validate a claimed 40/64 hex `candidate_sha` against each evidence record's `subject_sha`; require `check` and `source` metadata | Textual equality only, not commit existence, check execution, signature or independent provenance |
| `approval_presence` | Check whether a manifest-declared required approval has a nonblank reference | Reference presence is **not** approval validity or effect authorization |

Without explicit envelope files, the kit looks for the playbook's checked-in `examples/task-envelope/*.yaml` and `examples/golden-path/**/task-envelope.yaml`; if none exist, this check is **skipped**, not treated as success.

Sample optional metadata, **synthetic**, not proof:

```json
{
  "candidate_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "capabilities": {
    "tools": ["repository.read"],
    "resources": ["example/repo"],
    "effects": ["read-only"]
  },
  "evidence": [
    {
      "check": "unit",
      "subject_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "source": "synthetic:ci-run"
    }
  ],
  "approval": {
    "required": true,
    "reference": "synthetic:review"
  }
}
```

These fields are **advisory conformance inputs**, not a replacement for task-envelope schema, `Evidence` in Anthesis, a signed approval record, or another canonical evidence envelope. Treat any manifest sourced from the candidate itself as untrusted.

## Report contract and exits

`--format json` emits one deterministic object:

- `schema_version`: `playbook.conformance-report.v1`;
- `subject`: minimal local source label (not a cryptographic identity);
- `overall`: `pass`, `warning`, `fail`, or `unverified`;
- `effect_authorized`: **always `false`**;
- `checks`: stable list of `id`, `status`, `summary`, `details` where each status is `pass`, `fail`, `warning`, `skipped`, or `not_applicable`;
- `limitations`: boundaries of the checking environment and provenance.

`--format markdown` renders the same checks for human review.

**Exit code 1** for objective failures, invalid inputs, or an `unverified` run with no passing check. **Exit code 0** for `pass` or advisory `warning`, so a path match or missing claimed approval is **not automatically accepted**: downstream review must interpret warnings and apply its own policy. No automatic approval/merge is included.

## Scope and negative tests

Checked-in tests include a playbook self-conformance path, invalid task envelopes, symlink/root escapes, invalid changed paths, sensitive-path match, missing approval reference, malformed capability inventory, exact-subject evidence mismatch, empty/unverified inputs and both output formats. The flake runs the same tests and an end-to-end self-conformance command.

This prototype does **not** implement independent remote check verification, actual role-identity binding, GitHub required-check admission, signed provenance, dynamic context selection, CODEOWNERS semantics, or inference about risk. GitHub provider admission for **this repository** was separately activated and tested under [#60](https://github.com/ryjen/agent-delivery-playbook/issues/60); it does not derive from this kit or transfer to adopters. This kit's passing self-test does **not** independently qualify `v0.1.0` for release.

## Evidence and ownership

- [#45](https://github.com/ryjen/agent-delivery-playbook/issues/45) — small portable conformance interface.
- [Task envelope schema](../schemas/task-envelope.schema.json) and [validation](task-envelope-validation.md) — authoritative structure.
- [Enforcement map](policy-enforcement-map.md) — sources of authority and control boundaries.
- [Delivery evidence standard](delivery-evidence-standard.md) — evidence sufficiency remains risk and policy controlled.
- [#60](https://github.com/ryjen/agent-delivery-playbook/issues/60) — GitHub's live default-branch ruleset enforces admission for this repository; conformance-kit output is not an equivalent control.

A future independently accepted adapter could verify immutable GitHub check runs or a trusted Anthesis approval using their actual source APIs. That requires a separate reviewed scope and must not be inferred from this report format.
