#!/usr/bin/env python3
"""Negative and positive tests for the glossary identifier check."""

from __future__ import annotations

import importlib.util
import json
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_glossary", ROOT / "scripts/validate-glossary.py")
assert SPEC and SPEC.loader
glossary = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(glossary)


class GlossaryValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.body = (ROOT / "docs/glossary.md").read_text(encoding="utf-8")
        cls.schema = json.loads((ROOT / "schemas/task-envelope.schema.json").read_text(encoding="utf-8"))

    def test_actual_glossary_matches_normative_schema(self) -> None:
        self.assertEqual(glossary.validate(self.body, self.schema), [])

    def test_duplicate_canonical_heading_fails(self) -> None:
        changed = self.body.replace("### Task envelope\n", "### Task envelope\n\n### Task-envelope\n", 1)
        self.assertTrue(any("duplicate canonical concept" in x for x in glossary.validate(changed, self.schema)))

    def test_deprecated_alias_cannot_become_canonical_term(self) -> None:
        changed = self.body.replace("### Agent\n", "### required_level\n\n### Agent\n", 1)
        self.assertTrue(any("legacy alias used as canonical heading" in x for x in glossary.validate(changed, self.schema)))

    def test_missing_evidence_identifier_is_rejected(self) -> None:
        changed = self.body.replace("| `E3` | Operational evidence |", "| Operational | Operational evidence |", 1)
        self.assertTrue(any("evidence identifiers differ" in x for x in glossary.validate(changed, self.schema)))

    def test_duplicate_risk_identifier_is_rejected(self) -> None:
        line = next(x for x in self.body.splitlines() if x.startswith("| `T3` |"))
        changed = self.body.replace(line, line + "\n" + line, 1)
        self.assertTrue(any("duplicate T identifier" in x for x in glossary.validate(changed, self.schema)))

    def test_risk_schema_drift_fails_instead_of_redefining_tiers(self) -> None:
        changed = deepcopy(self.schema)
        changed["properties"]["classification"]["properties"]["risk_tier"]["enum"].append("T5")
        errors = glossary.validate(self.body, changed)
        self.assertTrue(any("risk identifiers differ" in x for x in errors))
        self.assertTrue(any("risk-tier schema changed" in x for x in errors))

    def test_duplicate_alias_fails(self) -> None:
        first = next(x for x in self.body.splitlines() if x.startswith("| `required_level` |"))
        changed = self.body.replace(first, first + "\n" + first, 1)
        self.assertTrue(any("duplicate legacy alias" in x for x in glossary.validate(changed, self.schema)))

    def test_missing_concept_cannot_silently_pass(self) -> None:
        changed = self.body.replace("### Runtime identity\n", "### Runtime process\n", 1)
        self.assertTrue(any("missing canonical concept: runtime identity" in x for x in glossary.validate(changed, self.schema)))


if __name__ == "__main__":
    unittest.main()
