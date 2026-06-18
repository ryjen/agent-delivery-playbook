#!/usr/bin/env python3
"""Validate task envelope examples without external dependencies.

This intentionally validates the repository's current YAML subset rather than
becoming a general-purpose YAML or JSON Schema implementation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "task-envelope.schema.json"
EXAMPLE_DIRS = [
    ROOT / "examples" / "task-envelope",
    ROOT / "examples" / "golden-path",
]

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


def parse_subset_yaml(path: Path) -> dict[str, Any]:
    """Parse the small mapping/list YAML subset used by examples.

    Supported forms:
    - nested mappings using indentation;
    - scalar values;
    - lists of scalars;
    - lists of small mappings.
    """
    lines = [
        (indent_of(raw), raw.strip(), line_number)
        for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if raw.strip() and not raw.lstrip().startswith("#")
    ]
    value, index = parse_block(lines, 0, 0, path)
    if index != len(lines):
        _, _, line_number = lines[index]
        fail(path, line_number, "unexpected trailing content")
    if not isinstance(value, dict):
        raise ValueError(f"{path}:1: envelope root must be a mapping")
    return value


def parse_block(
    lines: list[tuple[int, str, int]],
    index: int,
    indent: int,
    path: Path,
) -> tuple[Any, int]:
    if index >= len(lines):
        return {}, index

    current_indent, content, line_number = lines[index]
    if current_indent < indent:
        return {}, index
    if current_indent > indent:
        fail(path, line_number, f"unexpected indentation; expected {indent} spaces")

    if content.startswith("- "):
        return parse_list(lines, index, indent, path)
    return parse_mapping(lines, index, indent, path)


def parse_mapping(
    lines: list[tuple[int, str, int]],
    index: int,
    indent: int,
    path: Path,
) -> tuple[dict[str, Any], int]:
    mapping: dict[str, Any] = {}

    while index < len(lines):
        current_indent, content, line_number = lines[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            fail(path, line_number, f"unexpected nested mapping item: {content}")
        if content.startswith("- "):
            break

        key, value = split_scalar(content, path, line_number)
        if value == "":
            if index + 1 < len(lines) and lines[index + 1][0] > current_indent:
                nested, index = parse_block(lines, index + 1, lines[index + 1][0], path)
                mapping[key] = nested
            else:
                mapping[key] = []
                index += 1
        else:
            mapping[key] = coerce_scalar(value)
            index += 1

    return mapping, index


def parse_list(
    lines: list[tuple[int, str, int]],
    index: int,
    indent: int,
    path: Path,
) -> tuple[list[Any], int]:
    items: list[Any] = []

    while index < len(lines):
        current_indent, content, line_number = lines[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            fail(path, line_number, "unexpected list indentation")
        if not content.startswith("- "):
            break

        item = content[2:]
        if item == "":
            if index + 1 >= len(lines) or lines[index + 1][0] <= current_indent:
                items.append({})
                index += 1
            else:
                nested, index = parse_block(lines, index + 1, lines[index + 1][0], path)
                items.append(nested)
            continue

        if ":" in item:
            key, value = split_scalar(item, path, line_number)
            entry: dict[str, Any] = {key: coerce_scalar(value) if value else {}}
            index += 1
            if index < len(lines) and lines[index][0] > current_indent:
                nested, index = parse_mapping(lines, index, lines[index][0], path)
                entry.update(nested)
            items.append(entry)
        else:
            items.append(coerce_scalar(item))
            index += 1

    return items, index


def indent_of(raw: str) -> int:
    return len(raw) - len(raw.lstrip(" "))


def split_scalar(line: str, path: Path, line_number: int) -> tuple[str, str]:
    if ":" not in line:
        fail(path, line_number, "expected key/value pair")
    key, value = line.split(":", 1)
    return key.strip(), value.strip()


def coerce_scalar(value: str) -> str | bool:
    if value == "true":
        return True
    if value == "false":
        return False
    return value


def fail(path: Path, line_number: int, message: str) -> None:
    raise ValueError(f"{path}:{line_number}: {message}")


def schema_evidence_field() -> str:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    schema_id = schema.get("$id", "")
    if "example.com" in schema_id:
        raise ValueError("schema $id must not use the example.com placeholder")

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


def example_files() -> list[Path]:
    files: list[Path] = []
    for directory in EXAMPLE_DIRS:
        if directory.exists():
            files.extend(directory.rglob("task-envelope.yaml"))
            if directory.name == "task-envelope":
                files.extend(directory.glob("*.yaml"))
    return sorted(set(files))


def main() -> int:
    evidence_field = schema_evidence_field()
    files = example_files()
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
