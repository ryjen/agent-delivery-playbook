#!/usr/bin/env python3
"""Evaluate deterministic adversarial governance fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "examples" / "adversarial"
VALID_TIERS = {"T1": 1, "T2": 2, "T3": 3, "T4": 4}


def evaluate(facts: dict[str, Any], declared_tier: str) -> dict[str, Any]:
    reject: list[str] = []
    escalate: list[str] = []

    requested = facts.get("requested_effect")
    granted = set(facts.get("granted_effects", []))
    if facts.get("authority_from_untrusted_content") is True:
        reject.append("untrusted-content-cannot-grant-authority")
    if requested and requested not in granted:
        reject.append("requested-effect-outside-grant")
    if facts.get("evidence_subject_match") is False:
        reject.append("evidence-subject-mismatch")
    if facts.get("stale_required_context") is True:
        reject.append("required-context-stale-or-revoked")
    if facts.get("child_within_parent") is False:
        reject.append("delegation-exceeds-parent-grant")
    if facts.get("retry_scope_match") is False:
        reject.append("retry-exceeds-original-scope")
    if facts.get("approval_by_candidate_actor") is True:
        reject.append("self-approval-not-independent")

    if facts.get("dependency_install_script") is True:
        escalate.append("dependency-install-script-requires-review")
    if facts.get("workflow_permission_expansion") is True:
        escalate.append("workflow-authority-change-requires-review")
    if facts.get("context_scope_match") is False:
        escalate.append("context-expansion-requires-approval")
    if facts.get("self_modifying_control") is True:
        escalate.append("self-modifying-governance-requires-independent-review")

    minimum_tier = facts.get("minimum_risk_tier")
    if minimum_tier:
        if minimum_tier not in VALID_TIERS or declared_tier not in VALID_TIERS:
            reject.append("invalid-risk-tier")
        elif VALID_TIERS[declared_tier] < VALID_TIERS[minimum_tier]:
            escalate.append("declared-risk-below-minimum")

    if facts.get("required_approval_present") is False:
        escalate.append("required-approval-missing")

    if reject:
        decision = "reject"
    elif escalate:
        decision = "escalate"
    else:
        decision = "allow"

    permitted_effects: list[str] = []
    if decision == "allow" and requested and requested in granted:
        permitted_effects.append(requested)

    return {
        "decision": decision,
        "reasons": sorted(set(reject + escalate)),
        "permitted_effects": sorted(permitted_effects),
    }


def validate_fixture(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        fixture = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid JSON: {exc}"]

    for key in ["id", "scenario", "declared_risk_tier", "facts", "expected"]:
        if key not in fixture:
            errors.append(f"missing field: {key}")
    if errors:
        return errors

    tier = fixture["declared_risk_tier"]
    if tier not in VALID_TIERS:
        errors.append(f"invalid declared_risk_tier: {tier!r}")
        return errors
    if not isinstance(fixture["facts"], dict):
        return ["facts must be an object"]
    expected = fixture["expected"]
    if not isinstance(expected, dict):
        return ["expected must be an object"]

    result = evaluate(fixture["facts"], tier)
    if result["decision"] != expected.get("decision"):
        errors.append(f"decision mismatch: expected {expected.get('decision')!r}, got {result['decision']!r}")

    expected_reasons = sorted(expected.get("reasons", []))
    if result["reasons"] != expected_reasons:
        errors.append(f"reason mismatch: expected {expected_reasons!r}, got {result['reasons']!r}")

    forbidden = set(expected.get("forbidden_effects", []))
    leaked = forbidden.intersection(result["permitted_effects"])
    if leaked:
        errors.append(f"forbidden terminal effects permitted: {sorted(leaked)!r}")

    return errors


def fixture_files() -> list[Path]:
    return sorted(FIXTURE_DIR.glob("*.json")) if FIXTURE_DIR.exists() else []


def main() -> int:
    files = fixture_files()
    if len(files) < 8:
        print(f"FAIL adversarial fixtures\n  - expected at least 8 fixtures, found {len(files)}")
        return 1
    failed = False
    for path in files:
        errors = validate_fixture(path)
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
