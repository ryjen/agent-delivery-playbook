#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate-task-envelopes-standard.py"
SPEC = importlib.util.spec_from_file_location("standard_validator", MODULE_PATH)
assert SPEC and SPEC.loader
standard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(standard)


class StandardValidationTests(unittest.TestCase):
    def write_yaml(self, content: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "fixture.yaml"
        path.write_text(content, encoding="utf-8")
        return path

    def test_schema_declares_and_validates_as_draft_2020_12(self) -> None:
        schema = standard.load_schema()
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")

    def test_duplicate_yaml_keys_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate key"):
            standard.load_yaml(self.write_yaml("task: one\ntask: two\n"))

    def test_unknown_fields_fail_closed(self) -> None:
        lightweight = standard.load_lightweight_module()
        source = ROOT / "examples" / "task-envelope" / "t2-bugfix.yaml"
        content = source.read_text(encoding="utf-8").replace("status: proposed", "unexpected: value\nstatus: proposed")
        errors = standard.validate_file(self.write_yaml(content), standard.load_schema(), lightweight)
        self.assertTrue(any("Additional properties are not allowed" in error for error in errors))

    def test_checked_in_examples_are_standard_valid(self) -> None:
        schema = standard.load_schema()
        lightweight = standard.load_lightweight_module()
        for path in lightweight.example_files():
            with self.subTest(path=path):
                self.assertEqual(standard.validate_file(path, schema, lightweight), [])


if __name__ == "__main__":
    unittest.main()
