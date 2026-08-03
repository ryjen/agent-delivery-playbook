#!/usr/bin/env python3
"""Validate task-envelope examples without external dependencies.

The parser intentionally supports only the YAML subset used by this repository.
It is a smoke test, not a general YAML or JSON Schema implementation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "task-envelope.schema.json"
EXAMPLE_DIRS = [ROOT / "examples" / "task-envelope", ROOT / "examples" / "golden-path"]
VALID_TIERS = {"T1", "T2", "T3", "T4"}
VALID_LEVELS = {"E1", "E2", "E3", "E4"}
REQUIRED_TOP_LEVEL = ["task", "classification", "context", "constraints", "execution", "evidence", "review", "status"]


def fail(path: Path, line: int, message: str) -> None:
    raise ValueError(f"{path}:{line}: {message}")


def indent_of(raw: str) -> int:
    return len(raw) - len(raw.lstrip(" "))


def is_quoted(value: str) -> bool:
    return len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}


def strip_quotes(value: str) -> str:
    return value[1:-1] if is_quoted(value) else value


def coerce_scalar(value: str) -> Any:
    if value == "true":
        return True
    if value == "false":
        return False
    if value == "[]":
        return []
    if value == "{}":
        return {}
    return strip_quotes(value)


def split_scalar(line: str, path: Path, line_number: int) -> tuple[str, str]:
    if ":" not in line:
        fail(path, line_number, "expected key/value pair")
    key, value = line.split(":", 1)
    key = key.strip()
    if not key:
        fail(path, line_number, "mapping key must not be empty")
    return key, value.strip()


def parse_block(lines: list[tuple[int, str, int]], index: int, indent: int, path: Path) -> tuple[Any, int]:
    if index >= len(lines):
        return {}, index
    current_indent, content, line_number = lines[index]
    if current_indent < indent:
        return {}, index
    if current_indent > indent:
        fail(path, line_number, f"unexpected indentation; expected {indent} spaces")
    return parse_list(lines, index, indent, path) if content.startswith("- ") else parse_mapping(lines, index, indent, path)


def parse_mapping(lines: list[tuple[int, str, int]], index: int, indent: int, path: Path) -> tuple[dict[str, Any], int]:
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
        if key in mapping:
            fail(path, line_number, f"duplicate mapping key: {key}")
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


def parse_list(lines: list[tuple[int, str, int]], index: int, indent: int, path: Path) -> tuple[list[Any], int]:
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
        if is_quoted(item):
            items.append(strip_quotes(item))
            index += 1
            continue
        if ":" in item:
            key, value = split_scalar(item, path, line_number)
            entry: dict[str, Any] = {key: coerce_scalar(value) if value else {}}
            index += 1
            if index < len(lines) and lines[index][0] > current_indent:
                nested, index = parse_mapping(lines, index, lines[index][0], path)
                for nested_key, nested_value in nested.items():
                    if nested_key in entry:
                        fail(path, line_number, f"duplicate mapping key: {nested_key}")
                    entry[nested_key] = nested_value
            items.append(entry)
        else:
            items.append(coerce_scalar(item))
            index += 1
    return items, index


def parse_subset_yaml(path: Path) -> dict[str, Any]:
    lines = [
        (indent_of(raw), raw.strip(), line_number)
        for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if raw.strip() and not raw.lstrip().startswith("#")
    ]
    value, index = parse_block(lines, 0, 0, path)
    if index != len(lines):
        fail(path, lines[index][2], "unexpected trailing content")
    if not isinstance(value, dict):
        raise ValueError(f"{path}:1: envelope root must be a mapping")
    return value


def schema_evidence_field() -> str:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    if "example.com" in schema.get("$id", ""):
        raise ValueError("schema $id must not use the example.com placeholder")
    required = schema["properties"]["evidence"].get("required", [])
    if "required_levels" in required:
        return "required_levels"
    if "required_level" in required:
        return "required_level"
    raise ValueError("schema evidence section must require required_level or required_levels")


def require_mapping(value: Any, name: str, errors: list[str]) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    errors.append(f"{name} must be a section")
    return {}


def require_list_of_strings(section: dict[str, Any], key: str, name: str, errors: list[str], required: bool = False) -> list[str]:
    value = section.get(key)
    if value is None:
        if required:
            errors.append(f"{name} is required")
        return []
    if not isinstance(value, list):
        errors.append(f"{name} must be a list")
        return []
    invalid = [item for item in value if not isinstance(item, str)]
    if invalid:
        errors.append(f"{name} must contain only strings; quote values like 'issue: APP-1234' if needed")
    return [item for item in value if isinstance(item, str)]


def require_list_of_mappings(section: dict[str, Any], key: str, name: str, errors: list[str]) -> list[dict[str, Any]]:
    value = section.get(key, [])
    if not isinstance(value, list):
        errors.append(f"{name} must be a list")
        return []
    if any(not isinstance(item, dict) for item in value):
        errors.append(f"{name} must contain only mappings")
    return [item for item in value if isinstance(item, dict)]


def validate(path: Path, evidence_field: str) -> list[str]:
    errors: list[str] = []
    try:
        envelope = parse_subset_yaml(path)
    except ValueError as exc:
        return [str(exc)]
    for key in REQUIRED_TOP_LEVEL:
        if key not in envelope:
            errors.append(f"missing top-level section: {key}")
    classification = require_mapping(envelope.get("classification", {}), "classification", errors)
    if classification.get("risk_tier") not in VALID_TIERS:
        errors.append(f"invalid classification.risk_tier: {classification.get('risk_tier')!r}")
    context = require_mapping(envelope.get("context", {}), "context", errors)
    require_list_of_strings(context, "repositories", "context.repositories", errors, required=True)
    require_list_of_strings(context, "references", "context.references", errors)
    provenance = context.get("provenance")
    if provenance is not None:
        provenance_mapping = require_mapping(provenance, "context.provenance", errors)
        for key in ["approved_sources", "included", "summarized", "deferred", "stale_context_caveats"]:
            require_list_of_strings(provenance_mapping, key, f"context.provenance.{key}", errors)
        for item in require_list_of_mappings(provenance_mapping, "excluded", "context.provenance.excluded", errors):
            if not isinstance(item.get("path"), str): errors.append("context.provenance.excluded[].path must be a string")
            if not isinstance(item.get("reason"), str): errors.append("context.provenance.excluded[].reason must be a string")
        for item in require_list_of_mappings(provenance_mapping, "escalations", "context.provenance.escalations", errors):
            if not isinstance(item.get("source"), str): errors.append("context.provenance.escalations[].source must be a string")
            if not isinstance(item.get("reason"), str): errors.append("context.provenance.escalations[].reason must be a string")
            if item.get("status") not in {"not_requested", "requested", "approved", "denied"}:
                errors.append(f"invalid context.provenance.escalations[].status: {item.get('status')!r}")
    constraints = require_mapping(envelope.get("constraints", {}), "constraints", errors)
    require_list_of_strings(constraints, "allowed", "constraints.allowed", errors, required=True)
    require_list_of_strings(constraints, "prohibited", "constraints.prohibited", errors, required=True)
    execution = require_mapping(envelope.get("execution", {}), "execution", errors)
    require_list_of_strings(execution, "tools", "execution.tools", errors, required=True)
    require_list_of_strings(execution, "actions", "execution.actions", errors, required=True)
    evidence = require_mapping(envelope.get("evidence", {}), "evidence", errors)
    if evidence_field == "required_levels":
        levels = require_list_of_strings(evidence, "required_levels", "evidence.required_levels", errors, required=True)
        invalid = [level for level in levels if level not in VALID_LEVELS]
        if invalid:
            errors.append(f"invalid evidence.required_levels: {invalid!r}")
    elif evidence.get("required_level") not in VALID_LEVELS:
        errors.append(f"invalid evidence.required_level: {evidence.get('required_level')!r}")
    require_list_of_strings(evidence, "tests", "evidence.tests", errors)
    require_list_of_strings(evidence, "artifacts", "evidence.artifacts", errors)
    review = require_mapping(envelope.get("review", {}), "review", errors)
    if not isinstance(review.get("required"), bool):
        errors.append("review.required must be true or false")
    require_list_of_strings(review, "approvers", "review.approvers", errors)
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
