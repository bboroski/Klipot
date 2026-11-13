"""Structural checks for the canonical LOVE-50 policy manifest."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "ecosystem" / "love-50.json"


class Love50ManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_policy_identity_and_status(self) -> None:
        self.assertEqual(self.data["policy_id"], "love-50.chinese-maxims")
        self.assertEqual(self.data["version"], "1.0.0")
        self.assertEqual(self.data["status"], "specified")

    def test_exactly_fifty_ordered_maxims(self) -> None:
        maxims = self.data["maxims"]
        self.assertEqual(len(maxims), 50)
        self.assertEqual([item["id"] for item in maxims], list(range(1, 51)))

    def test_five_groups_of_ten(self) -> None:
        groups = self.data["groups"]
        self.assertEqual(len(groups), 5)
        self.assertEqual([group["id"] for group in groups],
                         ["fate", "fidelity", "passion", "harmony", "wisdom"])
        counts = {group["id"]: 0 for group in groups}
        for item in self.data["maxims"]:
            counts[item["group"]] += 1
        self.assertEqual(counts, {key: 10 for key in counts})

    def test_each_entry_has_traceable_content(self) -> None:
        required = ("zh", "pinyin", "gloss", "engineering_practice", "verification")
        for item in self.data["maxims"]:
            with self.subTest(maxim=item["id"]):
                for field in required:
                    self.assertIsInstance(item[field], str)
                    self.assertTrue(item[field].strip(), field)

    def test_chinese_expressions_are_unique(self) -> None:
        expressions = [item["zh"] for item in self.data["maxims"]]
        self.assertEqual(len(expressions), len(set(expressions)))

    def test_source_caveat_is_explicit(self) -> None:
        note = self.data["source_note"]
        self.assertIn("1 Corinthians 13:4", note)
        self.assertIn("classical poetic lines", note)


if __name__ == "__main__":
    unittest.main()
