# Versioning, releases, and compatibility

**Status:** pre-1.0 policy proposal. No tagged playbook release exists as of 2026-10-17, and this document is not an instruction to publish one.

## Version authority

- The **signed-off Git commit / annotated release tag** is the immutable version of the *whole playbook package*: normative policies, schemas, templates, examples, docs, validators and Nix lock.
- Public releases use `v0.MINOR.PATCH` until a production-proven compatibility commitment justifies `v1.0.0`. A Git tag and its exact commit—not README text, a generated date or latest/default-branch URL—identify the accepted release.
- During `0.x`, increment **MINOR** for externally observable changes to the policy, schema, template, evidence, or normative semantics (whether additive or breaking). Increment **PATCH** only for backwards-compatible bug fixes, clarifications and tooling/documentation repairs that do not weaken or redefine requirements.
- Release candidates may use `v0.MINOR.PATCH-rc.N` if a real candidate is being qualified. An untagged `main` checkout is always **unreleased** and may change.

**No automatic adoption:** An adopter is responsible for choosing/pinning the intended release; pulling `main` silently does not provide a stable compatibility contract.

## Contract and compatibility ownership

| Artifact | Compatibility meaning | Change rules |
| --- | --- | --- |
| `schemas/task-envelope.schema.json` | Accepted input envelope structure at the tagged revision | Adding a required field, tightening enum/constraints, changing field meaning, removing a field, or rejecting previously valid input is **breaking** |
| Task risk / evidence / approval policies | Controls an adopter must follow | Tightening or weakening previously normative behaviour is a **semantic contract change**, even with unchanged JSON Schema |
| Validator / conformance checks | Observable acceptance behaviour of the tagged package | A new failing condition for previously accepted input requires migration notes; bug fixes must distinguish correcting a documented invariant from introducing a new requirement |
| PR / agent templates | Human-facing submission contract | New required sections or changed responsibilities require migration notes; optional clarifications may be patch-level |
| Examples / fixtures | Illustration of the tagged schema and policy | Must validate with the same tagged toolchain; examples are **not** authorization certificates |
| Security/admission runtime | Outside playbook package | A release tag does not attest a live GitHub ruleset, sandbox, verifier, CI host or authorization system |

There is **no new `playbook_version` field** in the current task envelope: its schema sets `additionalProperties: false`. Adding an undocumented field would break examples and validation. A tag/release manifest can identify an example's target version externally; a future in-envelope version discriminator requires its own reviewed schema migration.

The schema currently has a main-branch `$id` URL. That URL is **not** immutable. Consumers should pin a released Git ref and preferably an artifact digest; publishing `v0.x` does not retroactively make the existing `$id` versioned. Do not silently rewrite the current `$id` or claim compatibility across schema revisions without tests.

## Change classification

- **Breaking:** required-property additions/removals, enum removals, stricter validation, changed policy meaning/risk thresholds, changes to who may approve or act, changed evidence sufficiency, previously legal consumer workflows becoming invalid.
- **Additive, still MINOR pre-1.0:** new optional examples, template sections or validation features, expanded documented capabilities, new optional schema fields that truly preserve old acceptance.
- **Patch:** typo/link fixes, documentation clarification with unchanged semantics, repair that restores already documented behaviour, deterministic test refactoring with no new requirements.
- **Security repair:** urgency does not justify hiding impact. Document the incompatibility, affected versions, workaround/rollback and required migration even when shipping a security fix.

A candidate change is classified from observed contract effects, not the author's intended changelog category. If impact is uncertain, treat it as potentially breaking and ask for independent review.

## Migration and deprecation

A MINOR or security-affecting release must include a release note with:
1. Previous and target versions, the exact affected artifact paths, and the changed acceptance/authority semantics.
2. An explicit **before/after** example when a schema, policy or template migration is required.
3. A consumer action (pin old version, update envelope, adjust CI, rerun checks, or defer adoption).
4. Evidence of compatibility or a statement of **unknown/unverified**; do not claim past versions accept new templates without replay.
5. Deprecation status and an alternative/pointer. Before 1.0, no fixed calendar grace period is promised; deprecation may remain supported only for specifically documented versions.

Keep released tags immutable. Fix a defect through a new tag and explicit supersession/erratum rather than moving an existing tag.

## Release checklist and execution

**First candidate:** `v0.1.0` (tentative; not published). See the [draft readiness dossier](releases/v0.1.0-readiness.md) and [draft release notes](releases/v0.1.0-notes.md). Do not publish merely because this file or its PR merges; a new exact-commit qualification is required after the readiness PR merges.

Required evidence before a tag:
- [x] [#60](https://github.com/ryjen/agent-delivery-playbook/issues/60) is qualified for the tested failing-check path by a live provider ruleset read-back and blocked disposable PR #87. Missing-check and direct-push rejection remain untested, and administrator ruleset-edit authority persists.
- [ ] Exact candidate commit and current-base PR checks pass through the repository-owned Nix flake; results reference the candidate and validation toolchain.
- [ ] Normative policies, schema, examples and validators are internally consistent; execute `nix flake check --print-build-logs` on the candidate.
- [ ] The reference adoption and negative adversarial fixtures remain valid or their limitations are disclosed.
- [ ] `CHANGELOG.md`, migration notes, version name, release contents and unsupported areas are reviewed.
- [ ] An accountable release operator approves the **exact commit**, then creates the annotated tag and release through authorized credentials outside untrusted agent/CI runtimes.
- [ ] Verify release tag -> commit -> content/lock and published release notes. Preserve immutable links and required CI references.

The workflow currently uses SHA-pinned Actions and `contents: read`. **Do not add a privileged release job** to make this convenient. If automation is proposed later, its signing/release permissions and protected admission paths require an independent design, credentials review and tests.

The main ruleset presently covers branches, **not release tags**; tag immutability therefore depends on operator controls until a separate tag ruleset is explicitly reviewed and enabled. A release is not evidence of production runtime enforcement.

## Change and release record

`CHANGELOG.md` tracks **Unreleased** changes until a tagged version is qualified. Each published release entry should include the date, exact tag/commit, the control or compatibility changes, migrations, security consequences, verification references and known limitations.

Existing example YAML/JSON files are examples **of the tree containing them**. At a released tag, link to the tagged tree; do not insert extra fields invalid under the task-envelope schema.

## Relationship to other work

- [#43](https://github.com/ryjen/agent-delivery-playbook/issues/43): policy and first-release decision.
- [#60](https://github.com/ryjen/agent-delivery-playbook/issues/60): provider-enforced repository admission.
- [#45](https://github.com/ryjen/agent-delivery-playbook/issues/45): optional portable conformance interface.
- [Governance lifecycle](governance-lifecycle.md): draft/recommended/stable/deprecated artifact state. The **version number** identifies the release, while the artifact lifecycle state describes its maturity; these are independent dimensions.

This is a standalone playbook package. It does not version Anthesis, Dubnium, ops-cadence, or other consumer projects.
