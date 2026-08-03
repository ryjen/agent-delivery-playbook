#!/usr/bin/env python3
"""Validate dependency-free repository integrity checks.

This script intentionally covers deterministic checks available in the Python
standard library. Standards-based YAML and JSON Schema validation are tracked
separately so this baseline remains small and auditable.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRS = {".git"}
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
MERMAID_FENCE = re.compile(r"^```mermaid\s*$", re.MULTILINE)


def repository_files(pattern: str) -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob(pattern)
        if not any(part in IGNORED_DIRS for part in path.relative_to(ROOT).parts)
    )


def validate_json() -> list[str]:
    errors: list[str] = []
    for path in repository_files("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
    return errors


def local_link_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip()
    if not target or target.startswith("#") or target.startswith("mailto:"):
        return None

    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return None

    path_text = unquote(parsed.path)
    if not path_text:
        return None

    if path_text.startswith("/"):
        return ROOT / path_text.lstrip("/")
    return source.parent / path_text


def validate_markdown_links() -> list[str]:
    errors: list[str] = []
    for source in repository_files("*.md"):
        try:
            content = source.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{source.relative_to(ROOT)}: cannot read Markdown: {exc}")
            continue

        for raw_target in MARKDOWN_LINK.findall(content):
            target = local_link_target(source, raw_target)
            if target is None:
                continue
            if not target.resolve().is_relative_to(ROOT.resolve()):
                errors.append(
                    f"{source.relative_to(ROOT)}: local link escapes repository: {raw_target}"
                )
                continue
            if not target.exists():
                errors.append(
                    f"{source.relative_to(ROOT)}: missing local link target: {raw_target}"
                )
    return errors


def validate_mermaid_fences() -> list[str]:
    errors: list[str] = []
    for path in repository_files("*.md"):
        content = path.read_text(encoding="utf-8")
        openings = len(MERMAID_FENCE.findall(content))
        if openings == 0:
            continue
        fence_count = sum(1 for line in content.splitlines() if line.strip().startswith("```"))
        if fence_count % 2 != 0:
            errors.append(f"{path.relative_to(ROOT)}: unbalanced fenced code block")
    return errors


def main() -> int:
    checks = {
        "JSON syntax": validate_json(),
        "Markdown local links": validate_markdown_links(),
        "Mermaid fences": validate_mermaid_fences(),
    }

    failed = False
    for name, errors in checks.items():
        if errors:
            failed = True
            print(f"FAIL {name}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK   {name}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
