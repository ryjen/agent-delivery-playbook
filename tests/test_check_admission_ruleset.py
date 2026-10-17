#!/usr/bin/env python3
"""Read-only ruleset admission preflight tests; no GitHub API calls."""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_admission_ruleset", ROOT / "scripts" / "check-admission-ruleset.py"
)
assert SPEC and SPEC.loader
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


def proposal() -> dict:
    return json.loads(checker.PROPOSAL_PATH.read_text(encoding="utf-8"))


def observed(value: dict, timestamp: str = checker.ORIGINAL_UPDATE) -> dict:
    return {
        "id": checker.RULESET_ID,
        "source": checker.REPOSITORY,
        "updated_at": timestamp,
        **copy.deepcopy(value),
    }


class AdmissionRulesetTests(unittest.TestCase):
    def test_expected_proposal_is_structurally_valid(self) -> None:
        self.assertEqual(checker.validate_proposal(proposal()), [])

    def test_baseline_matches_snapshot(self) -> None:
        self.assertEqual(
            checker.validate_observed(observed(checker.BASELINE), checker.BASELINE,
                                      require_original_timestamp=True), []
        )

    def test_previous_unscoped_admin_bypass_rejected_after_activation(self) -> None:
        result = checker.validate_observed(
            observed(checker.BASELINE), proposal(), require_original_timestamp=False
        )
        self.assertIn("observed provider ruleset differs from expected policy", result)

    def test_required_check_missing_does_not_qualify(self) -> None:
        item = proposal()
        item["rules"][3]["parameters"]["required_status_checks"].pop()
        self.assertIn("required check contexts drifted", checker.validate_proposal(item))

    def test_pull_request_requirement_cannot_be_omitted(self) -> None:
        item = proposal()
        item["rules"] = [r for r in item["rules"] if r["type"] != "pull_request"]
        self.assertIn("expected exactly four admission rule types",
                      checker.validate_proposal(item))

    def test_strict_validation_and_no_bypass_required(self) -> None:
        item = proposal()
        item["bypass_actors"] = checker.BASELINE["bypass_actors"]
        item["rules"][3]["parameters"]["strict_required_status_checks_policy"] = False
        errors = checker.validate_proposal(item)
        self.assertIn("proposal has an ambient bypass actor", errors)
        self.assertIn("required checks must enforce current base", errors)

    def test_base_snapshot_is_stale_after_provider_change(self) -> None:
        result = checker.validate_observed(
            observed(checker.BASELINE, "2026-10-18T00:00:00Z"),
            checker.BASELINE, require_original_timestamp=True
        )
        self.assertTrue(any("updated since" in message for message in result))

    def test_wrong_ruleset_identity_never_qualifies(self) -> None:
        item = observed(proposal())
        item["id"] += 1
        self.assertIn("wrong ruleset identity/source", checker.validate_observed(
            item, proposal(), require_original_timestamp=False
        ))

    def test_equivalent_utc_timestamp_does_not_reject_unchanged_baseline(self) -> None:
        snapshot = observed(checker.BASELINE, "2026-06-18T08:09:46.285Z")
        self.assertEqual(checker.validate_observed(
            snapshot, checker.BASELINE, require_original_timestamp=True
        ), [])

    def test_provider_inert_defaults_and_order_normalize(self) -> None:
        item = observed(proposal(), "2026-10-17T20:00:00Z")
        item["rules"].reverse()
        pr = next(x for x in item["rules"] if x["type"] == "pull_request")
        pr["parameters"]["automatic_copilot_code_review_enabled"] = False
        pr["parameters"]["required_reviewers"] = []
        pr["parameters"]["dismissal_restriction"] = {"enabled": False, "allowed_actors": []}
        pr["parameters"]["allowed_merge_methods"].reverse()
        checks = next(x for x in item["rules"] if x["type"] == "required_status_checks")
        checks["parameters"]["do_not_enforce_on_create"] = False
        checks["parameters"]["required_status_checks"].reverse()
        self.assertEqual(checker.validate_observed(
            item, proposal(), require_original_timestamp=False
        ), [])

    def test_semantically_material_provider_default_is_not_ignored(self) -> None:
        item = observed(proposal())
        checks = next(x for x in item["rules"] if x["type"] == "required_status_checks")
        checks["parameters"]["do_not_enforce_on_create"] = True
        self.assertIn("observed provider ruleset differs from expected policy",
                      checker.validate_observed(
                          item, proposal(), require_original_timestamp=False
                      ))

    def test_unknown_provider_rule_parameter_fails_closed(self) -> None:
        item = observed(proposal())
        pr = next(x for x in item["rules"] if x["type"] == "pull_request")
        pr["parameters"]["unknown_rule"] = False
        self.assertIn("observed provider ruleset differs from expected policy",
                      checker.validate_observed(
                          item, proposal(), require_original_timestamp=False
                      ))

    def test_operator_runbook_has_real_shell_fences(self) -> None:
        runbook = (ROOT / "docs" / "operations" / "main-admission.md").read_text(
            encoding="utf-8"
        )
        self.assertGreaterEqual(runbook.count("```bash"), 3)
        self.assertNotIn("\\```bash", runbook)

    def test_read_only_cli_active_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "ruleset.json"
            source.write_text(json.dumps(observed(proposal())), encoding="utf-8")
            self.assertEqual(checker.main(["--mode", "active", "--observed", str(source)]), 0)
            self.assertNotEqual(checker.main(["--mode", "baseline", "--observed", str(source)]), 0)


if __name__ == "__main__":
    unittest.main()
