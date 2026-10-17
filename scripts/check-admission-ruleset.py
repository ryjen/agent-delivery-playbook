#!/usr/bin/env python3
"""Read-only preflight of the GitHub main ruleset for issue #60.

This checks the observed/proposed provider configuration; it neither changes
GitHub settings nor demonstrates an enforced negative-admission test.
"""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import datetime
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL_PATH = ROOT / "examples" / "provider-admission" / "main.ruleset.json"
RULESET_ID = 17832277
REPOSITORY = "ryjen/agent-delivery-playbook"
ORIGINAL_UPDATE = "2026-06-18T01:09:46.285-07:00"
BASELINE = {
    "name": "default",
    "target": "branch",
    "enforcement": "active",
    "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
    "bypass_actors": [
        {"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}
    ],
    "rules": [{"type": "deletion"}, {"type": "non_fast_forward"}],
}
FIELDS = tuple(BASELINE)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("ruleset must be a JSON object")
    return value


def project(value: dict[str, Any]) -> dict[str, Any]:
    """Normalize only known semantically inert provider defaults.

    Unknown provider fields must NOT be discarded: unexpected policy is drift.
    """
    result = deepcopy({key: value.get(key) for key in FIELDS})
    rules = result.get("rules")
    if isinstance(rules, list) and all(isinstance(rule, dict) for rule in rules):
        for rule in rules:
            params = rule.get("parameters")
            if not isinstance(params, dict):
                continue
            if rule.get("type") == "required_status_checks":
                if params.get("do_not_enforce_on_create") is False:
                    params.pop("do_not_enforce_on_create")
                checks = params.get("required_status_checks")
                if isinstance(checks, list) and all(isinstance(x, dict) for x in checks):
                    checks.sort(key=lambda x: str(x.get("context")))
            if rule.get("type") == "pull_request":
                # GitHub defaults extra approval for unattributed Copilot PRs to true.
                # GitHub documents this as having no effect when zero approvals are
                # required. Normalize only that exact inert combination; otherwise
                # retain the field so review/admission policy drift fails closed.
                if (
                    params.get("required_approving_review_count") == 0
                    and type(params.get("required_approving_review_count")) is int
                    and params.get("require_extra_approval_for_unattributed_changes") is True
                ):
                    params.pop("require_extra_approval_for_unattributed_changes")
                if params.get("automatic_copilot_code_review_enabled") is False:
                    params.pop("automatic_copilot_code_review_enabled")
                if params.get("required_reviewers") == []:
                    params.pop("required_reviewers")
                if params.get("dismissal_restriction") == {"enabled": False, "allowed_actors": []}:
                    params.pop("dismissal_restriction")
                methods = params.get("allowed_merge_methods")
                if isinstance(methods, list) and all(isinstance(x, str) for x in methods):
                    methods.sort()
        rules.sort(key=lambda x: str(x.get("type")))
    actors = result.get("bypass_actors")
    if isinstance(actors, list) and all(isinstance(x, dict) for x in actors):
        actors.sort(key=lambda x: (str(x.get("actor_type")), str(x.get("actor_id")), str(x.get("bypass_mode"))))
    return result


def same_instant(left: Any, right: str) -> bool:
    if not isinstance(left, str):
        return False
    try:
        a = datetime.fromisoformat(left.replace("Z", "+00:00"))
        b = datetime.fromisoformat(right.replace("Z", "+00:00"))
    except ValueError:
        return False
    return a.tzinfo is not None and b.tzinfo is not None and a == b


def validate_proposal(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(value) != set(FIELDS):
        errors.append("proposal must contain only the six provider ruleset fields")
    if value.get("name") != "default" or value.get("target") != "branch":
        errors.append("proposal must target the repository default branch ruleset")
    if value.get("enforcement") != "active":
        errors.append("ruleset must use active enforcement")
    if value.get("conditions") != BASELINE["conditions"]:
        errors.append("default-branch matching has drifted")
    if value.get("bypass_actors") != []:
        errors.append("proposal has an ambient bypass actor")
    rules = value.get("rules")
    if not isinstance(rules, list):
        return errors + ["rules must be an array"]

    names = [x.get("type") if isinstance(x, dict) else None for x in rules]
    if len(names) != 4 or any(not isinstance(name, str) for name in names) or len(set(names)) != 4 or set(names) != {
        "deletion", "non_fast_forward", "pull_request", "required_status_checks"
    }:
        return errors + ["expected exactly four admission rule types"]
    rule_map = {r["type"]: r for r in rules}
    if rule_map["deletion"] != {"type": "deletion"} or rule_map["non_fast_forward"] != {"type": "non_fast_forward"}:
        errors.append("existing deletion / non-fast-forward controls must remain unchanged")

    pr = rule_map["pull_request"].get("parameters")
    if not isinstance(pr, dict):
        errors.append("pull_request parameters missing")
    else:
        methods = pr.get("allowed_merge_methods")
        if not isinstance(methods, list) or any(not isinstance(x, str) for x in methods) or len(methods) != 3 or set(methods) != {"merge", "squash", "rebase"}:
            errors.append("unexpected permitted merge methods")
        for field, required in [
            ("dismiss_stale_reviews_on_push", True),
            ("require_code_owner_review", False),
            ("require_last_push_approval", False),
            ("required_approving_review_count", 0),
            ("required_review_thread_resolution", True),
        ]:
            if type(pr.get(field)) is not type(required) or pr[field] != required:
                errors.append(f"pull_request.{field} unexpected")
    checks = rule_map["required_status_checks"].get("parameters")
    if not isinstance(checks, dict):
        errors.append("required_status_checks parameters missing")
    else:
        if checks.get("strict_required_status_checks_policy") is not True:
            errors.append("required checks must enforce current base")
        expected_checks = {("Repository integrity", 15368), ("Task envelopes", 15368)}
        actual_checks = checks.get("required_status_checks")
        if (
            not isinstance(actual_checks, list)
            or len(actual_checks) != 2
            or any(
                not isinstance(x, dict) or set(x) != {"context", "integration_id"} or
                not isinstance(x.get("context"), str) or type(x.get("integration_id")) is not int
                for x in actual_checks
            )
            or {(x["context"], x["integration_id"]) for x in actual_checks} != expected_checks
        ):
            errors.append("required check contexts drifted")
    return errors


def validate_observed(
    observed: dict[str, Any], expected: dict[str, Any], *, require_original_timestamp: bool
) -> list[str]:
    errors: list[str] = []
    if observed.get("id") != RULESET_ID or observed.get("source") != REPOSITORY:
        errors.append("wrong ruleset identity/source")
    if require_original_timestamp and not same_instant(observed.get("updated_at"), ORIGINAL_UPDATE):
        errors.append("ruleset updated since the 2026-10-17 baseline; reconcile before PUT")
    if project(observed) != project(expected):
        errors.append("observed provider ruleset differs from expected policy")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--observed", type=Path, help="read-only GitHub API ruleset JSON")
    parser.add_argument(
        "--mode", required=True, choices=["proposal", "baseline", "active"],
        help="check proposed policy, unchanged prior baseline, or provider enforcement",
    )
    args = parser.parse_args(argv)
    try:
        proposal = read_json(PROPOSAL_PATH)
        errors = validate_proposal(proposal)
        if args.mode != "proposal":
            if args.observed is None:
                parser.error("--observed is required for baseline/active")
            observed = read_json(args.observed)
            if args.mode == "baseline":
                errors += validate_observed(observed, BASELINE, require_original_timestamp=True)
            else:
                errors += validate_observed(observed, proposal, require_original_timestamp=False)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"FAIL admission preflight: {exc}")
        return 1
    for error in errors:
        print(f"FAIL {error}")
    if errors:
        return 1
    print(f"OK {args.mode}: ruleset structural preflight only; no live rejection proved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
