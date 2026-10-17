#!/usr/bin/env python3
"""Check glossary term/alias uniqueness and public risk/evidence identifiers.

This is a structural consistency check, not semantic policy evaluation or authority.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLOSSARY = ROOT / "docs/glossary.md"
SCHEMA = ROOT / "schemas/task-envelope.schema.json"

REQUIRED_CONCEPTS = {
    "agent", "principal", "runtime identity", "task contract", "task envelope",
    "risk tier", "evidence level", "capability", "permission", "authority",
    "effect", "context", "provenance", "memory", "evidence", "claim",
    "captured output", "attestation", "replay", "approval", "review",
    "operator", "accountable human", "policy", "control", "invariant",
    "exception", "downgrade", "escalation", "rejection", "rollback", "outcome",
}


def normal(term: str) -> str:
    return re.sub(r"[\s_-]+", " ", term.strip().casefold())


def section(text: str, heading: str) -> tuple[str | None, str | None]:
    """Return a unique H2 section body or a precise structural error."""
    hits = list(re.finditer(r"(?m)^## " + re.escape(heading) + r"[ \t]*$", text))
    if len(hits) != 1:
        return None, f"expected one ## {heading} section; found {len(hits)}"
    tail = text[hits[0].end():]
    next_heading = re.search(r"(?m)^## ", tail)
    return (tail if next_heading is None else tail[:next_heading.start()]), None


def collect_identifiers(table: str, prefix: str, errors: list[str]) -> set[str]:
    observed: list[str] = []
    for line in table.splitlines():
        item = re.match(r"^\|\s*`([A-Z][0-9]+)`\s*\|", line)
        if item:
            observed.append(item.group(1))
    for name in sorted(set(observed)):
        if observed.count(name) > 1:
            errors.append(f"duplicate {prefix} identifier: {name}")
    bad = sorted(x for x in observed if not x.startswith(prefix))
    if bad:
        errors.append(f"unexpected identifier(s) in {prefix} table: {', '.join(bad)}")
    return set(observed)


def validate(text: str, schema: dict) -> list[str]:
    errors: list[str] = []

    concepts, err = section(text, "Canonical concepts")
    if err:
        errors.append(err)
        concepts = ""
    headings = re.findall(r"(?m)^### ([^\n]+?)\s*$", concepts)
    keys = [normal(h) for h in headings]
    for key in sorted(set(keys)):
        if keys.count(key) > 1:
            errors.append(f"duplicate canonical concept heading: {key}")
    for required in sorted(REQUIRED_CONCEPTS - set(keys)):
        errors.append(f"missing canonical concept: {required}")

    aliases, err = section(text, "Legacy and deprecated aliases")
    if err:
        errors.append(err)
        aliases = ""
    alias_names = []
    for line in aliases.splitlines():
        match = re.match(r"^\|\s*`([^`]+)`\s*\|", line)
        if match:
            alias_names.append(normal(match.group(1)))
    for name in sorted(set(alias_names)):
        if alias_names.count(name) > 1:
            errors.append(f"duplicate legacy alias: {name}")
        if name in keys:
            errors.append(f"legacy alias used as canonical heading: {name}")

    risk, err = section(text, "Risk tier identifiers")
    if err:
        errors.append(err)
        risk = ""
    evidence, err = section(text, "Evidence identifiers")
    if err:
        errors.append(err)
        evidence = ""
    actual_risk = collect_identifiers(risk, "T", errors)
    actual_evidence = collect_identifiers(evidence, "E", errors)

    try:
        props = schema["properties"]
        expected_risk = set(props["classification"]["properties"]["risk_tier"]["enum"])
        expected_evidence = set(props["evidence"]["properties"]["required_levels"]["items"]["enum"])
    except (KeyError, TypeError):
        return errors + ["task envelope schema identifier locations are malformed"]

    for name, actual, expected in (
        ("risk", actual_risk, expected_risk),
        ("evidence", actual_evidence, expected_evidence),
    ):
        if actual != expected:
            errors.append(
                f"{name} identifiers differ from schema; missing={sorted(expected - actual)}, "
                f"extra={sorted(actual - expected)}"
            )
    if expected_risk != {"T1", "T2", "T3", "T4"}:
        errors.append("risk-tier schema changed; review normative tier definitions")
    if expected_evidence != {"E1", "E2", "E3", "E4"}:
        errors.append("evidence-level schema changed; review normative coverage definitions")
    return errors


def main() -> int:
    try:
        text = GLOSSARY.read_text(encoding="utf-8")
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        errors = validate(text, schema)
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError) as exc:
        print(f"FAIL glossary consistency: {type(exc).__name__}: {exc}")
        return 1
    for error in errors:
        print(f"FAIL glossary consistency: {error}")
    if errors:
        return 1
    print("OK glossary: unique canonical headings/aliases; risk/evidence identifiers match schema")
    return 0


if __name__ == "__main__":
    sys.exit(main())
