#!/usr/bin/env python3
"""Unit tests for the dependency-free task-envelope validator."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate-task-envelopes.py"
SPEC = importlib.util.spec_from_file_location("validate_task_envelopes", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


VALID_ENVELOPE = """\
task:
  id: T-test
  title: Test envelope
  objective: Exercise validator behavior.
  owner: tester
classification:
  type: test
  risk_tier: T2
context:
  repositories:
    - example/repo
  references: []
constraints:
  allowed:
    - inspect
  prohibited:
    - release
execution:
  tools:
    - repo_read
  actions:
    - inspect
evidence:
  required_levels:
    - E2
  tests: []
  artifacts: []
review:
  required: true
  approvers: []
status: proposed
"""


class TemporaryYamlTestCase(unittest.TestCase):
    def write_yaml(self, content: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "fixture.yaml"
        path.write_text(content, encoding="utf-8")
        return path


class ParserTests(TemporaryYamlTestCase):
    def test_parses_supported_mapping_and_list_subset(self) -> None:
        parsed = validator.parse_subset_yaml(self.write_yaml(VALID_ENVELOPE))
        self.assertEqual(parsed["classification"]["risk_tier"], "T2")
        self.assertEqual(parsed["context"]["references"], [])
        self.assertIs(parsed["review"]["required"], True)

    def test_parses_inline_empty_mapping(self) -> None:
        parsed = validator.parse_subset_yaml(self.write_yaml("root: {}\n"))
        self.assertEqual(parsed["root"], {})

    def test_rejects_duplicate_mapping_keys(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate mapping key: task"):
            validator.parse_subset_yaml(self.write_yaml("task: one\ntask: two\n"))

    def test_rejects_empty_mapping_key(self) -> None:
        with self.assertRaisesRegex(ValueError, "mapping key must not be empty"):
            validator.parse_subset_yaml(self.write_yaml(": value\n"))

    def test_rejects_unexpected_indentation(self) -> None:
        with self.assertRaisesRegex(ValueError, "unexpected nested mapping item"):
            validator.parse_subset_yaml(self.write_yaml("root: value\n  child: value\n"))

    def test_quoted_colon_value_remains_scalar(self) -> None:
        parsed = validator.parse_subset_yaml(
            self.write_yaml('references:\n  - "issue: APP-1234"\n')
        )
        self.assertEqual(parsed["references"], ["issue: APP-1234"])

    def test_unquoted_colon_list_item_becomes_mapping(self) -> None:
        parsed = validator.parse_subset_yaml(
            self.write_yaml("references:\n  - issue: APP-1234\n")
        )
        self.assertEqual(parsed["references"], [{"issue": "APP-1234"}])

    def test_comments_and_blank_lines_are_ignored(self) -> None:
        parsed = validator.parse_subset_yaml(
            self.write_yaml("# comment\n\nroot: true\n")
        )
        self.assertIs(parsed["root"], True)


class ValidationTests(TemporaryYamlTestCase):
    def validate_text(self, content: str) -> list[str]:
        return validator.validate(self.write_yaml(content), "required_levels")

    def test_valid_envelope_has_no_errors(self) -> None:
        self.assertEqual(self.validate_text(VALID_ENVELOPE), [])

    def test_missing_top_level_section_is_reported(self) -> None:
        errors = self.validate_text(VALID_ENVELOPE.replace("status: proposed\n", ""))
        self.assertIn("missing top-level section: status", errors)

    def test_unknown_risk_tier_is_reported(self) -> None:
        errors = self.validate_text(VALID_ENVELOPE.replace("risk_tier: T2", "risk_tier: T9"))
        self.assertIn("invalid classification.risk_tier: 'T9'", errors)

    def test_unknown_evidence_level_is_reported(self) -> None:
        errors = self.validate_text(VALID_ENVELOPE.replace("    - E2", "    - E9"))
        self.assertIn("invalid evidence.required_levels: ['E9']", errors)

    def test_scalar_only_list_rejects_mapping_item(self) -> None:
        errors = self.validate_text(
            VALID_ENVELOPE.replace("  references: []", "  references:\n    - issue: APP-1234")
        )
        self.assertTrue(any("context.references must contain only strings" in error for error in errors))

    def test_review_required_must_be_boolean(self) -> None:
        errors = self.validate_text(VALID_ENVELOPE.replace("required: true", "required: yes"))
        self.assertIn("review.required must be true or false", errors)

    def test_invalid_provenance_escalation_status_is_reported(self) -> None:
        with_provenance = VALID_ENVELOPE.replace(
            "  references: []",
            "  references: []\n  provenance:\n    escalations:\n      - source: docs/policy.md\n        reason: Needs review\n        status: unknown",
        )
        errors = self.validate_text(with_provenance)
        self.assertIn("invalid context.provenance.escalations[].status: 'unknown'", errors)

    def test_required_list_missing_is_reported(self) -> None:
        errors = self.validate_text(
            VALID_ENVELOPE.replace("  repositories:\n    - example/repo\n", "")
        )
        self.assertIn("context.repositories is required", errors)


class HelperTests(unittest.TestCase):
    def test_example_discovery_contains_all_risk_tier_examples(self) -> None:
        names = {path.name for path in validator.example_files()}
        self.assertTrue({"t1-doc-change.yaml", "t2-bugfix.yaml", "t4-auth-change.yaml"}.issubset(names))

    def test_schema_uses_plural_evidence_field(self) -> None:
        self.assertEqual(validator.schema_evidence_field(), "required_levels")

    def test_string_list_helper_filters_invalid_items(self) -> None:
        errors: list[str] = []
        result = validator.require_list_of_strings(
            {"items": ["valid", {"invalid": "mapping"}]},
            "items",
            "section.items",
            errors,
        )
        self.assertEqual(result, ["valid"])
        self.assertEqual(len(errors), 1)


if __name__ == "__main__":
    unittest.main()
