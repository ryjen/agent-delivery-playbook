#!/usr/bin/env python3
"""Validate synthetic agent-configuration regression fixtures (not real agent evaluation)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "examples" / "agent-regression"

STATUSES = {"pass", "fail", "indeterminate", "unsupported", "infrastructure_failed"}
TIERS = {"T1", "T2", "T3", "T4"}
FAMILIES = {
    "ordinary-code-change",
    "ci-failure-analysis",
    "security-auth-change",
    "prompt-injection",
    "fabricated-or-detached-evidence",
    "verifier-unavailability",
    "approval-or-effect-bypass",
}
DISPOSITIONS = {"no-regression-found", "escalate", "block"}


def is_synthetic_ref(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("synthetic:") and len(value) > len("synthetic:")


def classify(fixture: dict[str, Any]) -> str:
    """Conservative comparison of *recorded synthetic observations*, not authority."""
    candidates = [case["candidate"] for case in fixture["cases"]]
    if "fail" in candidates:
        return "block"
    if any(result != "pass" for result in candidates):
        return "escalate"
    change = fixture["change"]
    evaluation = fixture["evaluation"]
    if (
        change["risk_tier"] in {"T3", "T4"}
        or change["capability_expanded"]
        or evaluation["oracle_producer_writable"]
    ):
        return "escalate"
    return "no-regression-found"


def validate_fixture(fixture: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(fixture, dict):
        return ["fixture must be an object"]
    if fixture.get("schema_version") != "playbook.agent-regression-fixture.v1":
        errors.append("invalid schema_version")
    if fixture.get("synthetic") is not True:
        errors.append("fixture must be explicitly synthetic")
    if not isinstance(fixture.get("id"), str) or not fixture["id"]:
        errors.append("missing id")

    change = fixture.get("change")
    evaluation = fixture.get("evaluation")
    cases = fixture.get("cases")
    expected = fixture.get("expected")
    if not isinstance(change, dict):
        errors.append("change must be an object")
    if not isinstance(evaluation, dict):
        errors.append("evaluation must be an object")
    if not isinstance(cases, list) or not cases:
        errors.append("cases must be a nonempty array")
    if not isinstance(expected, dict):
        errors.append("expected must be an object")
    if errors:
        return errors

    if not isinstance(change.get("kind"), str) or change["kind"] not in {"skill", "prompt", "model", "tool-contract", "context", "verifier"}:
        errors.append("invalid change kind")
    if not isinstance(change.get("risk_tier"), str) or change["risk_tier"] not in TIERS:
        errors.append("invalid risk tier")
    if type(change.get("capability_expanded")) is not bool:
        errors.append("capability_expanded must be boolean")
    if not isinstance(change.get("changed_surfaces"), list) or not change["changed_surfaces"] or not all(
        isinstance(x, str) and x for x in change["changed_surfaces"]
    ):
        errors.append("changed_surfaces must be a nonempty string array")
    for key in ("baseline_revision", "candidate_revision"):
        if not is_synthetic_ref(change.get(key)):
            errors.append(f"invalid {key}")

    for key in ("candidate_subject_ref", "verifier_plan_ref", "dataset_ref", "verifier_ref"):
        if not is_synthetic_ref(evaluation.get(key)):
            errors.append(f"invalid {key}")
    if evaluation.get("candidate_subject_ref") != change.get("candidate_revision"):
        errors.append("evaluation detached from candidate revision")
    if type(evaluation.get("oracle_producer_writable")) is not bool:
        errors.append("oracle_producer_writable must be boolean")
    if not isinstance(evaluation.get("independence_status"), str) or evaluation["independence_status"] not in {"claimed", "independently_verified"}:
        errors.append("invalid independence_status")

    case_ids: set[str] = set()
    for index, case in enumerate(cases):
        prefix = f"case[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix} must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{prefix} missing id")
        elif case_id in case_ids:
            errors.append(f"{prefix} duplicate id")
        else:
            case_ids.add(case_id)
        if not isinstance(case.get("family"), str) or case["family"] not in FAMILIES:
            errors.append(f"{prefix} invalid family")
        for phase in ("baseline", "candidate"):
            if not isinstance(case.get(phase), str) or case[phase] not in STATUSES:
                errors.append(f"{prefix} invalid {phase} status")
        if case.get("evidence_subject_ref") != evaluation.get("candidate_subject_ref"):
            errors.append(f"{prefix} evidence subject detached")
        if case.get("evidence_plan_ref") != evaluation.get("verifier_plan_ref"):
            errors.append(f"{prefix} evidence plan detached")

    if not isinstance(expected.get("regression_disposition"), str) or expected["regression_disposition"] not in DISPOSITIONS:
        errors.append("invalid expected regression_disposition")
    if expected.get("effect_authorized") is not False:
        errors.append("fixture must not authorize any effects")
    if not errors:
        observed = classify(fixture)
        if observed != expected["regression_disposition"]:
            errors.append(
                f"disposition mismatch: expected {expected['regression_disposition']!r}, got {observed!r}"
            )
    return errors


def fixture_files() -> list[Path]:
    return sorted(FIXTURE_DIR.glob("*.json")) if FIXTURE_DIR.is_dir() else []


def main() -> int:
    paths = fixture_files()
    if len(paths) < 2:
        print(f"FAIL regression fixtures: expected at least 2 examples, found {len(paths)}")
        return 1
    errors: list[str] = []
    covered: set[str] = set()
    for path in paths:
        try:
            fixture = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"{path.name}: invalid JSON: {exc}")
            continue
        local_errors = validate_fixture(fixture)
        errors.extend(f"{path.name}: {msg}" for msg in local_errors)
        if not local_errors:
            covered.update(case["family"] for case in fixture["cases"])
            print(f"OK   {path.relative_to(ROOT)}")
    missing = FAMILIES - covered
    if missing:
        errors.append(f"missing required task families: {sorted(missing)}")
    for message in errors:
        print(f"FAIL {message}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
