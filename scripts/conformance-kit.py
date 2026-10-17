#!/usr/bin/env python3
"""Read-only governed delivery conformance prototype; no effect authority."""

from __future__ import annotations

import argparse
import fnmatch
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

PLAYBOOK = Path(__file__).resolve().parents[1]
SHA = re.compile(r"^(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})$")
STATUSES = {"pass", "fail", "warning", "skipped", "not_applicable"}


def check(name: str, state: str, message: str, detail: list[str] | None = None) -> dict:
    assert state in STATUSES
    return {"id": name, "status": state, "summary": message, "details": sorted(detail or [])}


def module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def within(root: Path, name: str) -> Path:
    if Path(name).is_absolute():
        raise ValueError("absolute target path not permitted")
    try:
        target = (root / name).resolve()
    except (RuntimeError, OSError) as exc:
        raise ValueError("target cannot be resolved safely") from exc
    if not target.is_relative_to(root):
        raise ValueError("target escapes repository root")
    return target


def envelopes(root: Path, names: list[str]) -> dict:
    if names:
        paths = sorted({within(root, name) for name in names})
    else:
        paths = sorted(set((root / "examples/task-envelope").glob("*.yaml")) |
                       set((root / "examples/golden-path").glob("**/task-envelope.yaml")))
        invalid = []
        for path in paths:
            try:
                resolved = path.resolve(strict=True)
            except (RuntimeError, OSError):
                invalid.append(str(path.relative_to(root)) + ": unresolved or cyclic symlink")
                continue
            if not resolved.is_relative_to(root):
                invalid.append(str(path.relative_to(root)) + ": escapes repository root")
        if invalid:
            return check("task_envelopes", "fail",
                         "Auto-discovered envelope is not safely contained", invalid)
    if not paths:
        return check("task_envelopes", "skipped", "No envelopes supplied or discovered")
    standard = module("standard_checker", PLAYBOOK / "scripts/validate-task-envelopes-standard.py")
    schema = standard.load_schema()
    lightweight = standard.load_lightweight_module()
    errors = []
    for path in paths:
        label = str(path.relative_to(root))
        if not path.is_file():
            errors.append(label + ": missing file")
            continue
        try:
            errors.extend(label + ": " + msg for msg in standard.validate_file(path, schema, lightweight))
        except (OSError, ValueError, TypeError, UnicodeError) as exc:
            errors.append(label + ": checker error " + type(exc).__name__)
    return check("task_envelopes", "fail" if errors else "pass",
                 str(len(paths)) + " envelope(s) checked against existing validators", errors)


def integrity(root: Path, enabled: bool) -> dict:
    if not enabled:
        return check("reference_integrity", "skipped", "Repository scan not requested")
    # The existing validator scans local paths; do not let an adopter's symlinks
    # silently import evidence from outside the chosen repository.
    invalid = []
    for pattern in ("*.json", "*.md"):
        for file in sorted(root.rglob(pattern)):
            relative = file.relative_to(root)
            if ".git" in relative.parts:
                continue
            try:
                resolved = file.resolve(strict=True)
            except (RuntimeError, OSError):
                invalid.append(str(relative) + ": unavailable or cyclic file")
                continue
            if not resolved.is_relative_to(root):
                invalid.append(str(relative) + ": escapes repository root")
    if invalid:
        return check("reference_integrity", "fail",
                     "Repository scan includes unsafe or unresolved files", invalid)
    existing = module("integrity_checker", PLAYBOOK / "scripts/validate-repository.py")
    previous = existing.ROOT
    existing.ROOT = root
    try:
        errors = existing.validate_json() + existing.validate_markdown_links() + existing.validate_mermaid_fences()
    finally:
        existing.ROOT = previous
    return check("reference_integrity", "fail" if errors else "pass",
                 "Reused JSON, local Markdown link and Mermaid checks", errors)


def sensitive(paths: list[str]) -> dict:
    if not paths:
        return check("sensitive_paths", "not_applicable", "No changed paths supplied")
    policy = yaml.safe_load((PLAYBOOK / "policy/sensitive-paths.yaml").read_text(encoding="utf-8"))
    warnings = []
    for path in sorted(set(paths)):
        parts = path.split("/")
        if path.startswith("/") or "\\" in path or any(x in {"", ".", ".."} for x in parts):
            return check("sensitive_paths", "fail", "Invalid changed path", [path])
        for rule in policy["rules"]:
            if any(fnmatch.fnmatchcase(path, pattern) or
                   (pattern.startswith("**/") and fnmatch.fnmatchcase(path, pattern[3:]))
                   for pattern in rule["patterns"]):
                warnings.append(path + ": " + rule["id"] + " (" + rule["mode"] + ")")
    return check("sensitive_paths", "warning" if warnings else "pass",
                 "Sensitive paths are review signals, never automatic authority", warnings)


def manifest_checks(root: Path, filename: str | None) -> list[dict]:
    categories = ("capabilities", "evidence_binding", "approval_presence")
    if filename is None:
        return [check(x, "skipped", "Optional adoption manifest absent") for x in categories]
    try:
        value = json.loads(within(root, filename).read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError, json.JSONDecodeError):
        return [check("manifest", "fail", "Cannot read valid local JSON manifest")] + [
            check(x, "skipped", "Manifest unreadable") for x in categories]
    if not isinstance(value, dict):
        return [check("manifest", "fail", "Manifest must be an object")] + [
            check(x, "skipped", "Manifest malformed") for x in categories]
    caps = value.get("capabilities")
    if caps is None:
        capability = check("capabilities", "skipped", "No capability inventory")
    elif (not isinstance(caps, dict) or any(
        not isinstance(caps.get(k), list) or not caps[k] or
        not all(isinstance(item, str) and item.strip() for item in caps[k])
        for k in ("tools", "resources", "effects")
    )):
        capability = check("capabilities", "fail", "Incomplete capability declaration")
    else:
        capability = check("capabilities", "pass", "Capability fields structurally present, grants unverified")
    evidence = value.get("evidence")
    candidate = value.get("candidate_sha")
    if evidence is None:
        binding = check("evidence_binding", "skipped", "No evidence supplied")
    elif not isinstance(candidate, str) or SHA.fullmatch(candidate) is None:
        binding = check("evidence_binding", "fail", "Candidate SHA must be a 40/64 hex digest")
    elif (not isinstance(evidence, list) or not evidence or any(
        not isinstance(row, dict) or row.get("subject_sha") != candidate or
        not isinstance(row.get("check"), str) or not row["check"].strip() or
        not isinstance(row.get("source"), str) or not row["source"].strip()
        for row in evidence
    )):
        binding = check("evidence_binding", "fail", "Evidence subject/source metadata detached or incomplete")
    else:
        binding = check("evidence_binding", "pass", "Declared evidence subjects match; no independent attestation")
    approval = value.get("approval")
    if approval is None:
        review = check("approval_presence", "skipped", "No approval declaration")
    elif not isinstance(approval, dict) or type(approval.get("required")) is not bool:
        review = check("approval_presence", "fail", "Malformed approval declaration")
    elif approval["required"] and (not isinstance(approval.get("reference"), str) or
                                   not approval["reference"].strip()):
        review = check("approval_presence", "warning", "Required approval reference is absent")
    elif approval["required"]:
        review = check("approval_presence", "pass", "Approval reference present; authority unverified")
    else:
        review = check("approval_presence", "not_applicable", "No approval required was claimed; not policy-verified")
    return [capability, binding, review]


def evaluate(root: Path, names: list[str], paths: list[str], manifest: str | None,
             scan: bool) -> dict:
    checks = [envelopes(root, names), integrity(root, scan), sensitive(paths),
              *manifest_checks(root, manifest)]
    states = [item["status"] for item in checks]
    overall = ("fail" if "fail" in states else
               "unverified" if "pass" not in states else
               "warning" if "warning" in states else "pass")
    return {
        "schema_version": "playbook.conformance-report.v1",
        "subject": {"root": root.name, "source": "local-filesystem"},
        "overall": overall,
        "effect_authorized": False,
        "checks": checks,
        "limitations": [
            "Structural/advisory only: no approval, authorization or policy sufficiency",
            "Local records, evidence and approval references are not independently attested",
            "Sensitive-path matching requires human semantic risk review",
        ],
    }


def markdown(report: dict) -> str:
    lines = ["# Governed Delivery Conformance (pilot)", "",
             "Outcome: **" + report["overall"] + "**; no effect authority.", "",
             "| Check | Status | Description |", "| --- | --- | --- |"]
    details = []
    for item in report["checks"]:
        lines.append("| " + item["id"] + " | " + item["status"] + " | " +
                     item["summary"].replace("|", "/").replace("\n", " ") + " |")
        details.extend("- " + item["id"] + ": " + detail.replace("\\r", " ").replace("\\n", " ").replace("|", "/") for detail in item["details"])
    if details:
        lines += ["", "## Check details", "", *details]
    lines += ["", "Limitations:"] + ["- " + text for text in report["limitations"]]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--envelope", action="append", default=[])
    parser.add_argument("--changed-path", action="append", default=[])
    parser.add_argument("--manifest")
    parser.add_argument("--integrity", action="store_true")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve(strict=True)
        if not root.is_dir():
            raise ValueError("Root is not a directory")
        report = evaluate(root, args.envelope, args.changed_path, args.manifest, args.integrity)
    except (ValueError, OSError, RuntimeError, UnicodeError, TypeError, KeyError, yaml.YAMLError):
        report = {
            "schema_version": "playbook.conformance-report.v1",
            "subject": {"source": "local-filesystem"},
            "overall": "fail", "effect_authorized": False,
            "checks": [check("input", "fail", "Invalid conformance input")],
            "limitations": ["No conformance verdict for invalid input"],
        }
    print(json.dumps(report, sort_keys=True, indent=2) if args.format == "json" else markdown(report))
    return 1 if report["overall"] in {"fail", "unverified"} else 0


if __name__ == "__main__":
    sys.exit(main())
