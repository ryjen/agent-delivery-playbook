#!/usr/bin/env python3
"""Contract and adversarial tests for the read-only conformance kit."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("conformance_kit", ROOT / "scripts/conformance-kit.py")
assert SPEC and SPEC.loader
kit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(kit)
CANDIDATE = "a" * 40


def example_manifest() -> dict:
    return {
        "candidate_sha": CANDIDATE,
        "capabilities": {
            "tools": ["repo.read"],
            "resources": ["repository"],
            "effects": ["read-only"],
        },
        "evidence": [
            {"check": "unit", "subject_sha": CANDIDATE, "source": "synthetic:run-1"}
        ],
        "approval": {"required": True, "reference": "synthetic:human-approval"},
    }


class ConformanceKitTests(unittest.TestCase):
    def test_self_repo_end_to_end(self) -> None:
        report = kit.evaluate(ROOT, [], [], None, True)
        self.assertEqual(report["schema_version"], "playbook.conformance-report.v1")
        self.assertEqual(report["overall"], "pass")
        self.assertIs(report["effect_authorized"], False)
        statuses = {x["id"]: x["status"] for x in report["checks"]}
        self.assertEqual(statuses["task_envelopes"], "pass")
        self.assertEqual(statuses["reference_integrity"], "pass")
        self.assertEqual(statuses["sensitive_paths"], "not_applicable")
        self.assertEqual(statuses["approval_presence"], "skipped")

    def test_explicit_broken_envelope_fails(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / "bad.yaml").write_text("task:\n  id: 123\n", encoding="utf-8")
            outcome = kit.evaluate(root, ["bad.yaml"], [], None, False)
            self.assertEqual(outcome["overall"], "fail")
            self.assertEqual(outcome["checks"][0]["status"], "fail")

    def test_empty_evidence_does_not_mint_success(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            report = kit.evaluate(Path(name), [], [], None, False)
            self.assertEqual(report["overall"], "unverified")
            self.assertFalse(report["effect_authorized"])

    def test_escape_via_symlink_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as name, tempfile.TemporaryDirectory() as elsewhere:
            root = Path(name).resolve()
            (root / "escape").symlink_to(elsewhere, target_is_directory=True)
            with self.assertRaises(ValueError):
                kit.within(root, "escape/private.json")

    def test_auto_discovered_envelope_symlink_escape_fails_even_with_green_integrity(self) -> None:
        with tempfile.TemporaryDirectory() as name, tempfile.TemporaryDirectory() as other:
            root = Path(name).resolve()
            examples = root / "examples" / "task-envelope"
            examples.mkdir(parents=True)
            foreign = Path(other) / "untrusted.yaml"
            foreign.write_text("untrusted: true\n", encoding="utf-8")
            (examples / "hidden.yaml").symlink_to(foreign)
            report = kit.evaluate(root, [], [], None, True)
            self.assertEqual(report["overall"], "fail")
            states = {x["id"]: x["status"] for x in report["checks"]}
            self.assertEqual(states["task_envelopes"], "fail")
            self.assertEqual(states["reference_integrity"], "pass")
            self.assertIn("hidden.yaml", report["checks"][0]["details"][0])

    def test_absolute_and_parent_path_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name).resolve()
            with self.assertRaises(ValueError):
                kit.within(root, "../elsewhere")
            with self.assertRaises(ValueError):
                kit.within(root, "/etc/passwd")

    def test_sensitive_paths_are_advisory_not_authority(self) -> None:
        result = kit.sensitive([".github/workflows/validate.yml", "src/auth.py"])
        self.assertEqual(result["status"], "warning")
        self.assertTrue(any("github-workflows" in x for x in result["details"]))
        self.assertTrue(any("access-control-keywords" in x for x in result["details"]))

    def test_invalid_changed_path_fails(self) -> None:
        self.assertEqual(kit.sensitive(["../../file"])["status"], "fail")

    def test_manifest_binding_and_approval_are_structural(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name).resolve()
            (root / "manifest.json").write_text(json.dumps(example_manifest()), encoding="utf-8")
            report = kit.evaluate(root, [], [], "manifest.json", False)
            self.assertFalse(report["effect_authorized"])
            self.assertEqual(report["overall"], "pass")
            states = {x["id"]: x["status"] for x in report["checks"]}
            self.assertEqual(states["evidence_binding"], "pass")
            self.assertEqual(states["approval_presence"], "pass")

    def test_detached_evidence_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name).resolve()
            value = example_manifest()
            value["evidence"][0]["subject_sha"] = "b" * 40
            (root / "manifest.json").write_text(json.dumps(value), encoding="utf-8")
            report = kit.evaluate(root, [], [], "manifest.json", False)
            self.assertEqual(report["overall"], "fail")
            self.assertEqual(next(x for x in report["checks"] if x["id"] == "evidence_binding")["status"], "fail")

    def test_missing_required_approval_is_warning(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name).resolve()
            value = example_manifest()
            value["approval"].pop("reference")
            (root / "manifest.json").write_text(json.dumps(value), encoding="utf-8")
            report = kit.evaluate(root, [], [], "manifest.json", False)
            self.assertEqual(report["overall"], "warning")
            self.assertEqual(next(x for x in report["checks"] if x["id"] == "approval_presence")["status"], "warning")

    def test_capability_incomplete_is_fail(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name).resolve()
            value = example_manifest()
            value["capabilities"].pop("resources")
            (root / "manifest.json").write_text(json.dumps(value), encoding="utf-8")
            report = kit.evaluate(root, [], [], "manifest.json", False)
            self.assertEqual(report["overall"], "fail")

    def test_cli_json_and_markdown_render_and_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name).resolve()
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                status = kit.main(["--root", str(root), "--format", "json"])
            self.assertEqual(status, 1)
            self.assertEqual(json.loads(output.getvalue())["overall"], "unverified")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                status = kit.main(["--root", str(ROOT), "--format", "markdown", "--changed-path",
                                   ".github/workflows/validate.yml"])
            self.assertEqual(status, 0)
            self.assertIn("| sensitive_paths | warning |", output.getvalue())
            self.assertIn("no effect authority", output.getvalue())


if __name__ == "__main__":
    unittest.main()
