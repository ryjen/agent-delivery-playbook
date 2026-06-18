#!/usr/bin/env python3
"""Validate task envelope examples without external dependencies.

This intentionally validates the repository's current YAML subset rather than
becoming a general-purpose YAML or JSON Schema implementation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "task-envelope.schema.json"
EXAMPLES = ROOT / "examples" / "task-envelope"

VALID_TIERS = {"T1", "T2", "T3", "T4"}
VALID_LEVELS = {"E1", "E2", "E3", "E4"}
REQUIRED_TOP_LEVEL = [
    "task",
    "classification",
    "context",
    "constraints",
    "execution",
    "evidence",
    "review",
    "status",
]


def parse_subset_yaml(path: Path) -> dict[str, dict[str, object] | str]:
    """Parse the simple mapping/list subset used by task envelope examples."""
    root: dict[str, dict[str, object] | str] = {}
    current_section: str | None = None
    current_key: str | None = None

    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue

        if not raw.startswith(" "):
            if not raw.endswith(":"):
                key, value = split_scalar(raw, path, line_number)
                root[key] = value
                current_section = None
                current_key = None
                continue
            current_section = raw[:-1]
            root[current_section] = {}
            current_key = None
            continue

        if current_section is None or not isinstance(root.get(current_section), dict):
            fail(path, line_number, "nested value without a section")

        stripped = raw.strip()
        section = root[current_section]
        assert isinstance(section, dict)

        if stripped.startswith("- "):
            if current_key is None:
                fail(path, line_number, "list item without a key")
            section.setdefault(current_key, [])
            value = stripped[2:]
            existing = section[current_key]
            if not isinstance(existing, list):
                fail(path, line_number, f"key {current_key!r} is not a list")
            existing.append(value)
            continue

        key, value = split_scalar(stripped, path, line_number)
        if value == "":
            section[key] = []
            current_key = key
        elif value in {"true", "false"}:
            section[key] = value == "true"
            current_key = None
        else:
            section[key] = value
            current_key = None

    return root


def split_scalar(line: str, path: Path, line_number: int) -> tuple[str, str]:
    if ":" not in line:
        fail(path, line_number, "expected key/value pair")
    key, value = line.split(":", 1)
    return key.strip(), value.strip()


def fail(path: Path, line_number: int, message: str) -> None:
    raise ValueError(f"{path}:{line_number}: {message}")


def schema_evidence_field() -> str:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    required = schema["properties"]["evidence"].get("required", [])
    if "required_levels" in required:
        return "required_levels"
    if "required_level" in required:
        return "required_level"
    raise ValueError("schema evidence section must require required_level or required_levels")


def validate(path: Path, evidence_field: str) -> list[str]:
    errors: list[str] = []
    try:
        envelope = parse_subset_yaml(path)
    except ValueError as exc:
        return [str(exc)]

    for key in REQUIRED_TOP_LEVEL:
        if key not in envelope:
            errors.append(f"missing top-level section: {key}")

    classification = envelope.get("classification", {})
    if isinstance(classification, dict):
        tier = classification.get("risk_tier")
        if tier not in VALID_TIERS:
            errors.append(f"invalid classification.risk_tier: {tier!r}")
    else:
        errors.append("classification must be a section")

    evidence = envelope.get("evidence", {})
    if isinstance(evidence, dict):
        value = evidence.get(evidence_field)
        if evidence_field == "required_levels":
            if not isinstance(value, list) or not value:
                errors.append("evidence.required_levels must be a non-empty list")
            else:
                invalid = [level for level in value if level not in VALID_LEVELS]
                if invalid:
                    errors.append(f"invalid evidence.required_levels: {invalid!r}")
        else:
            if value not in VALID_LEVELS:
                errors.append(f"invalid evidence.required_level: {value!r}")
    else:
        errors.append("evidence must be a section")

    return errors


def main() -> int:
    evidence_field = schema_evidence_field()
    files = sorted(EXAMPLES.glob("*.yaml"))
    if not files:
        print("No task envelope examples found", file=sys.stderr)
        return 1

    failed = False
    for path in files:
        errors = validate(path, evidence_field)
        if errors:
            failed = True
            print(f"FAIL {path.relative_to(ROOT)}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK   {path.relative_to(ROOT)}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())