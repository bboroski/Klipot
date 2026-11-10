import unittest

from klipot.uncertainty import (
    UncertaintyError,
    build_resolution_plan,
    validate_registry,
)


class UncertaintyPlannerTests(unittest.TestCase):
    def setUp(self):
        self.registry = {
            "schema_version": "klipot.uncertainty.v1",
            "repository": "org/example",
            "items": [
                {
                    "id": "hardware.clock",
                    "domain": "platform",
                    "statement": "The platform clock contract is not configured.",
                    "feature": "Platform capability probe",
                    "resolution_mode": "probe",
                    "unknown_behavior": "Do not schedule time-dependent work.",
                    "verification": ["A monotonic clock probe passes on target."],
                    "status": "open",
                }
            ],
        }

    def test_open_unknown_becomes_concrete_probe_action(self):
        plan = build_resolution_plan(self.registry)
        self.assertEqual(plan["actions"][0]["next_step"], "run-probe")
        self.assertEqual(plan["counts"]["open"], 1)

    def test_order_is_deterministic(self):
        self.registry["items"].append({
            "id": "a11y",
            "domain": "ui",
            "statement": "Accessibility behavior is not verified.",
            "feature": "Accessibility audit",
            "resolution_mode": "staged-implementation",
            "unknown_behavior": "Do not claim accessibility conformance.",
            "verification": ["Keyboard-only navigation is tested."],
        })
        ids = [item["id"] for item in validate_registry(self.registry)]
        self.assertEqual(ids, ["a11y", "hardware.clock"])

    def test_duplicate_ids_are_rejected(self):
        self.registry["items"].append(dict(self.registry["items"][0]))
        with self.assertRaises(UncertaintyError):
            validate_registry(self.registry)

    def test_unknown_resolution_mode_is_rejected(self):
        self.registry["items"][0]["resolution_mode"] = "guess"
        with self.assertRaises(UncertaintyError):
            validate_registry(self.registry)

    def test_resolved_item_requires_evidence(self):
        self.registry["items"][0]["status"] = "resolved"
        with self.assertRaises(UncertaintyError):
            validate_registry(self.registry)

    def test_unknown_behavior_is_mandatory(self):
        del self.registry["items"][0]["unknown_behavior"]
        with self.assertRaises(UncertaintyError):
            validate_registry(self.registry)


if __name__ == "__main__":
    unittest.main()
