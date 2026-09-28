# Replayable Evidence — T3 CI Change

This synthetic example shows how evidence coverage and evidence trust/binding remain separate for a high-risk but bounded CI change.

## Task Reference

- Envelope: `examples/task-envelope/t3-ci-change.yaml`
- Risk tier: T3
- Required evidence levels: E2 + E3

## Change Reference

- PR: example CI-hardening PR
- Repository: `example/service`
- Ref: `feature/ci-permission-hardening`
- Exact commit: `<reviewed-commit-sha>`
- Changed paths:
  - `.github/workflows/validate.yml`

## Execution Identity and Authority

- Candidate producer: coding assistant with branch-scoped repository write access
- Human operator: platform maintainer
- Privileged credentials: none
- Approval boundary: platform-owner approval required before the CI-control patch
- Release/deployment authority: explicitly out of scope

## Evidence Records

| Coverage | Check | Evidence source / producer | Subject binding | Environment / run | Trust/binding properties | Result |
| --- | --- | --- | --- | --- | --- | --- |
| E2 | workflow policy/unit validation | coding assistant summary | mutable branch | agent session | unverified claim | Agent reports tests passed; does **not** satisfy required E2 alone |
| E2 | `nix flake check` | local shell output captured by candidate producer | `<reviewed-commit-sha>` recorded manually | developer workstation | captured + subject-declared; producer is not independent | Passed; useful supporting evidence |
| E2 | required validation workflow | protected CI runner | repository + exact `<reviewed-commit-sha>` + run `<ci-run-id>` | protected CI configuration | subject-bound + trusted-runner | Passed; satisfies the required technical check if CI configuration is itself trusted |
| E3 | pull-request event/permission-path exercise | protected CI / test harness | exact `<reviewed-commit-sha>` | isolated CI test environment, run `<operational-run-id>` | subject-bound + trusted-runner | Confirmed read-only token and expected event path |
| E4-style independent review | platform owner review | reviewer distinct from candidate producer | exact `<reviewed-commit-sha>` | review record `<review-id>` | independent review; approval authority only where repository policy grants it | Approved the bounded CI change after reviewing exact-subject evidence |

## Interpretation

The rows do not form a single trust score:

- the agent claim is useful context but does not prove execution;
- captured local output can show what the producer observed but remains self-produced evidence;
- protected CI provides stronger provenance and exact-subject binding for the checks it actually runs;
- the distinct platform review establishes separation of duties and, if repository policy says so, the approval needed to admit the change;
- none of these proves properties that were not checked.

No attestation is required in this example. If the repository later requires signed provenance, the attestation would add producer/input/result integrity properties; it would not replace technical verification or accountable approval.

## Known Limits

- Synthetic placeholders stand in for real immutable commit/run/review identifiers.
- The example does not claim that a generic hosted runner is trusted for every organization; trust depends on protected workflow configuration and the adopting repository's threat model.
- No production deployment or release evidence is included because those effects are outside this task.
