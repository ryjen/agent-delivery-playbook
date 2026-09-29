#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate-adversarial-fixtures.py"
SPEC = importlib.util.spec_from_file_location("validate_adversarial_fixtures", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class AdversarialFixtureTests(unittest.TestCase):
    def test_checked_in_fixtures_are_valid(self) -> None:
        files = validator.fixture_files()
        self.assertGreaterEqual(len(files), 8)
        for path in files:
            with self.subTest(path=path):
                self.assertEqual(validator.validate_fixture(path), [])

    def test_untrusted_content_cannot_grant_authority(self) -> None:
        result = validator.evaluate(
            {
                "authority_from_untrusted_content": True,
                "requested_effect": "merge",
                "granted_effects": ["repository.read"],
            },
            "T2",
        )
        self.assertEqual(result["decision"], "reject")
        self.assertNotIn("merge", result["permitted_effects"])

    def test_child_delegation_cannot_exceed_parent(self) -> None:
        result = validator.evaluate({"child_within_parent": False}, "T3")
        self.assertEqual(result["decision"], "reject")

    def test_self_modifying_governance_escalates(self) -> None:
        result = validator.evaluate({"self_modifying_control": True}, "T3")
        self.assertEqual(result["decision"], "escalate")

    def test_detached_evidence_rejected(self) -> None:
        result = validator.evaluate({"evidence_subject_match": False}, "T2")
        self.assertEqual(result["decision"], "reject")

    def test_fixture_with_forged_allow_expectation_fails(self) -> None:
        source = validator.fixture_files()[0]
        fixture = json.loads(source.read_text(encoding="utf-8"))
        fixture["expected"]["decision"] = "allow"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            errors = validator.validate_fixture(path)
        self.assertTrue(any("decision mismatch" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
