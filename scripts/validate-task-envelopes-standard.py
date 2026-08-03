#!/usr/bin/env python3
"""Validate task envelopes with real YAML and JSON Schema implementations."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "task-envelope.schema.json"
LIGHTWEIGHT_PATH = ROOT / "scripts" / "validate-task-envelopes.py"


class UniqueKeySafeLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def construct_unique_mapping(
    loader: UniqueKeySafeLoader,
    node: yaml.nodes.MappingNode,
    deep: bool = False,
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeySafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_unique_mapping,
)


def load_lightweight_module() -> Any:
    spec = importlib.util.spec_from_file_location(
        "validate_task_envelopes_lightweight", LIGHTWEIGHT_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load lightweight validator: {LIGHTWEIGHT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_schema(path: Path = SCHEMA_PATH) -> dict[str, Any]:
    schema = json.loads(path.read_text(encoding="utf-8"))
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ValueError("schema must declare JSON Schema draft 2020-12")
    Draft202012Validator.check_schema(schema)
    return schema


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeySafeLoader)
    except yaml.YAMLError as exc:
        raise ValueError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path}: envelope root must be a mapping")
    return value


def format_error(error: Any) -> str:
    location = ".".join(str(part) for part in error.absolute_path) or "<root>"
    return f"{location}: {error.message}"


def validate_file(
    path: Path,
    schema: dict[str, Any],
    lightweight: Any,
) -> list[str]:
    errors: list[str] = []
    try:
        standard_value = load_yaml(path)
    except ValueError as exc:
        return [str(exc)]

    validator = Draft202012Validator(schema)
    errors.extend(
        format_error(error)
        for error in sorted(
            validator.iter_errors(standard_value),
            key=lambda item: list(item.absolute_path),
        )
    )

    try:
        lightweight_value = lightweight.parse_subset_yaml(path)
    except ValueError as exc:
        errors.append(f"lightweight validator rejected standard-valid YAML: {exc}")
    else:
        if lightweight_value != standard_value:
            errors.append(
                "lightweight and standards-based parsers produced different values"
            )

    return errors


def main() -> int:
    try:
        schema = load_schema()
    except (OSError, ValueError, json.JSONDecodeError, SchemaError) as exc:
        print(f"FAIL schema\n  - {exc}")
        return 1

    lightweight = load_lightweight_module()
    files = lightweight.example_files()
    if not files:
        print("No task-envelope examples found", file=sys.stderr)
        return 1

    failed = False
    for path in files:
        errors = validate_file(path, schema, lightweight)
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
