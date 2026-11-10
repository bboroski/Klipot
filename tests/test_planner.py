import unittest

from klipot.planner import ManifestError, build_plan, validate_manifest


class PlannerTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {
            "schema_version": "nun.ecosystem.v1",
            "system": {"id": "test"},
            "components": [
                {
                    "id": "foundation",
                    "repo": "org/foundation",
                    "role": "foundation",
                    "depends_on": [],
                    "provides": ["clock.v1"],
                    "requires": [],
                },
                {
                    "id": "worker",
                    "repo": "org/worker",
                    "role": "worker",
                    "depends_on": ["foundation"],
                    "provides": ["work.v1"],
                    "requires": ["clock.v1"],
                },
            ],
        }

    def test_stable_dependency_order(self):
        plan = build_plan(self.manifest)
        self.assertEqual(plan["ordered_components"], ["foundation", "worker"])
        self.assertEqual(plan["system"], "test")

    def test_missing_dependency_rejected(self):
        self.manifest["components"][1]["depends_on"] = ["missing"]
        with self.assertRaises(ManifestError):
            validate_manifest(self.manifest)

    def test_missing_capability_rejected(self):
        self.manifest["components"][1]["requires"] = ["memory.v1"]
        with self.assertRaises(ManifestError):
            validate_manifest(self.manifest)

    def test_dependency_cycle_rejected(self):
        self.manifest["components"][0]["depends_on"] = ["worker"]
        with self.assertRaises(ManifestError):
            validate_manifest(self.manifest)

    def test_duplicate_capabilities_rejected(self):
        self.manifest["components"][0]["provides"] = [
            "clock.v1", "clock.v1"
        ]
        with self.assertRaises(ManifestError):
            validate_manifest(self.manifest)

    def test_unrelated_provider_is_not_accepted(self):
        self.manifest["components"].append({
            "id": "unrelated",
            "repo": "org/unrelated",
            "role": "unrelated",
            "depends_on": [],
            "provides": ["memory.v1"],
            "requires": [],
        })
        self.manifest["components"][1]["requires"] = ["memory.v1"]
        with self.assertRaises(ManifestError):
            validate_manifest(self.manifest)


if __name__ == "__main__":
    unittest.main()
