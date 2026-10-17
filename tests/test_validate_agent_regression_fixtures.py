#!/usr/bin/env python3
"""Regression tests for the *synthetic* configuration evaluation examples."""

from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate-agent-regression-fixtures.py"
SPEC = importlib.util.spec_from_file_location("validate_agent_regression_fixtures", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def fixture(name: str) -> dict:
    return json.loads((ROOT / "examples" / "agent-regression" / name).read_text(encoding="utf-8"))


class AgentRegressionFixtureTests(unittest.TestCase):
    def test_checked_in_suite_validates_all_required_families(self) -> None:
        self.assertEqual(validator.main(), 0)

    def test_benign_change_finds_no_regression_but_never_authorizes(self) -> None:
        item = fixture("01-skill-guidance.json")
        self.assertEqual(validator.validate_fixture(item), [])
        self.assertEqual(validator.classify(item), "no-regression-found")
        self.assertIs(item["expected"]["effect_authorized"], False)

    def test_security_change_blocks_on_new_failures(self) -> None:
        item = fixture("02-tool-permission-change.json")
        self.assertEqual(validator.validate_fixture(item), [])
        self.assertEqual(validator.classify(item), "block")

    def test_unavailable_mandatory_verifier_never_passes(self) -> None:
        item = fixture("01-skill-guidance.json")
        item["cases"][0]["candidate"] = "infrastructure_failed"
        item["expected"]["regression_disposition"] = "escalate"
        self.assertEqual(validator.validate_fixture(item), [])

    def test_changed_verifier_plan_invalidates_evidence(self) -> None:
        item = fixture("01-skill-guidance.json")
        item["evaluation"]["verifier_plan_ref"] = "synthetic:new-evaluator"
        self.assertIn("case[0] evidence plan detached", validator.validate_fixture(item))

    def test_candidate_drift_invalidates_evidence(self) -> None:
        item = fixture("01-skill-guidance.json")
        item["change"]["candidate_revision"] = "synthetic:changed-candidate"
        self.assertIn("evaluation detached from candidate revision", validator.validate_fixture(item))

    def test_expected_green_cannot_hide_fail(self) -> None:
        item = fixture("02-tool-permission-change.json")
        item["expected"]["regression_disposition"] = "no-regression-found"
        self.assertTrue(any("disposition mismatch" in x for x in validator.validate_fixture(item)))

    def test_self_approval_cannot_be_inferred_from_evaluation(self) -> None:
        item = fixture("01-skill-guidance.json")
        item["expected"]["effect_authorized"] = True
        self.assertIn("fixture must not authorize any effects", validator.validate_fixture(item))

    def test_high_risk_green_still_requires_review(self) -> None:
        item = fixture("01-skill-guidance.json")
        item["change"]["risk_tier"] = "T3"
        item["expected"]["regression_disposition"] = "escalate"
        self.assertEqual(validator.validate_fixture(item), [])

    def test_producer_writable_oracle_escalates(self) -> None:
        item = fixture("01-skill-guidance.json")
        item["evaluation"]["oracle_producer_writable"] = True
        item["expected"]["regression_disposition"] = "escalate"
        self.assertEqual(validator.validate_fixture(item), [])

    def test_unknown_status_is_rejected_not_converted_to_pass(self) -> None:
        item = fixture("01-skill-guidance.json")
        item["cases"][0]["candidate"] = "success"
        self.assertIn("case[0] invalid candidate status", validator.validate_fixture(item))

    def test_duplicate_case_id_rejected(self) -> None:
        item = fixture("01-skill-guidance.json")
        item["cases"][1]["id"] = item["cases"][0]["id"]
        self.assertIn("case[1] duplicate id", validator.validate_fixture(item))


if __name__ == "__main__":
    unittest.main()
