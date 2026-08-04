# Security Policy

## Scope

This repository contains governance guidance, schemas, examples, and validation tooling for agent-assisted software delivery. Security reports may concern either implementation defects or governance bypasses.

Examples include:

- validation that accepts malformed or policy-breaking task envelopes;
- schema or parser inconsistencies that weaken fail-closed behavior;
- workflow changes that expose credentials, grant write permissions, or execute untrusted code with elevated authority;
- examples or guidance that normalize unsafe authority, secret handling, evidence fabrication, or approval bypass;
- dependency or supply-chain weaknesses in repository validation tooling.

General design disagreements, documentation improvements, and non-sensitive bugs should be reported as normal GitHub issues.

## Supported Versions

The default branch is the only supported version until tagged releases and a compatibility policy are introduced.

| Version | Supported |
|---|---|
| `main` | Yes |
| Earlier commits or copied templates | No |

Consumers are responsible for recording the exact commit or release they adopt.

## Reporting a Vulnerability

Do not open a public issue for a vulnerability that could enable credential exposure, authorization bypass, unsafe workflow execution, or a credible governance-control bypass.

Use GitHub's private vulnerability reporting for this repository when available. Include:

- affected file, schema, workflow, or commit;
- threat scenario and required attacker capabilities;
- reproduction steps or a minimal failing example;
- expected and observed behavior;
- likely impact;
- any proposed mitigation;
- whether public disclosure is already known or time-sensitive.

Do not include real secrets, production credentials, private repository content, or personal data. Use synthetic examples and redact sensitive values.

## Response Expectations

A report will be evaluated for:

1. reproducibility;
2. affected trust boundary;
3. realistic impact;
4. whether the issue is implementation, documentation, or adopter configuration;
5. whether a coordinated fix or advisory is required.

No fixed response-time commitment is currently offered. Confirmed issues will be handled proportionally to severity and project maturity.

## Disclosure and Fixes

For confirmed vulnerabilities, the preferred sequence is:

1. reproduce and classify the issue;
2. identify affected versions or commits;
3. prepare a minimal fix and regression test;
4. update affected guidance or examples;
5. publish an advisory or release note when warranted;
6. credit the reporter unless anonymity is requested.

The repository does not claim that its policies or validators constitute a complete security boundary. Human review, repository permissions, CI isolation, runtime authorization, and operational controls remain necessary.