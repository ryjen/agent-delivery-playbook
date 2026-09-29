#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "reference-adoption" / "project" / "tag_normalizer.py"
SPEC = importlib.util.spec_from_file_location("reference_tag_normalizer", MODULE_PATH)
assert SPEC and SPEC.loader
normalizer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(normalizer)


class ReferenceProjectTests(unittest.TestCase):
    def test_normalizes_simple_tag(self) -> None:
        self.assertEqual(normalizer.normalize_tag(" Hello World "), "hello-world")

    def test_preserves_already_normalized_tag(self) -> None:
        self.assertEqual(normalizer.normalize_tag("release-notes"), "release-notes")

    def test_collapses_repeated_whitespace(self) -> None:
        self.assertEqual(normalizer.normalize_tag("  release   candidate  "), "release-candidate")

    def test_normalizes_mixed_whitespace(self) -> None:
        self.assertEqual(normalizer.normalize_tag("release\tcandidate notes"), "release-candidate-notes")


if __name__ == "__main__":
    unittest.main()
