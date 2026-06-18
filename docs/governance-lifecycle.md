# Governance Lifecycle

This repository contains normative docs, guidance, templates, schemas, examples, and policy artifacts. Changes to one category often require updates to the others. The lifecycle exists to prevent silent drift without adding heavyweight process.

## Artifact classes

| Class | Meaning | Examples |
| --- | --- | --- |
| Normative policy | Defines required behavior or review expectations | task risk matrix, evidence standard, task envelope |
| Schema/policy artifact | Machine-readable policy or validation input | JSON Schema, sensitive path policy |
| Template | Copyable artifact used by downstream repositories | PR template, AGENTS.md, review checklist |
| Guidance | Explanatory or adoption documentation | quickstart, rollout, trust model |
| Example | Non-normative demonstration of expected use | golden-path bundles, sample envelopes |

## Lifecycle states

| State | Meaning |
| --- | --- |
| Draft | Proposed or exploratory; useful but not stable |
| Recommended | Good default for new adopters; may still evolve |
| Stable | Intended to remain compatible except for explicit migrations |
| Deprecated | Still present, but new adopters should not copy it |
| Superseded | Replaced by a newer artifact; retained only for history or migration |

## Default state by artifact type

| Artifact type | Default state |
| --- | --- |
| README adoption guidance | Recommended |
| Normative policy docs | Recommended unless explicitly marked stable |
| Schemas | Recommended until validation and examples settle |
| Templates | Recommended |
| Examples | Draft or recommended depending on coverage |

## Change rules

| Change | Required checks |
| --- | --- |
| Normative policy change | Update related templates, examples, README/index links, and evidence expectations |
| Schema change | Update examples and validation docs/scripts |
| Template change | Confirm it still asks for required envelope, evidence, scope, risk, and rollback information |
| Example change | Confirm it does not contradict risk matrix, evidence standard, or task envelope schema |
| New doc | Add it to `docs/index.md`; add README link when it affects adoption path |
| Deprecation | Add replacement pointer and migration note |
| Sensitive-path or authority guidance change | Review trust model, task risk matrix, evidence standard, and capability catalog guidance |

## Migration notes

Add a migration note when a change affects downstream adopters, including:

- renamed fields;
- changed evidence requirements;
- new required PR sections;
- changed sensitive-path behavior;
- changed approval or review expectations;
- deprecated templates or examples.

A short section in the PR body is enough for small changes.

## Drift prevention checklist

Before merging governance-affecting changes, check:

- [ ] README adoption path still points to the right first steps.
- [ ] `docs/index.md` includes new or renamed docs.
- [ ] Schemas and examples still agree.
- [ ] PR template still captures minimum evidence.
- [ ] Examples still show constrained agent behavior.
- [ ] Deprecated artifacts point to replacements.
- [ ] Human approval remains required for merge and release decisions.

## Non-goals

This lifecycle is not an RFC program, release train, or approval bureaucracy. It is a lightweight maintenance rule set for keeping policy, templates, and examples aligned.