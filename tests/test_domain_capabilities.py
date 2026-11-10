import unittest

from klipot.domain import (
    CycleEvent, CycleState, RecoveryAction, advance_cycle,
    evaluate_evolution, plan_recovery, validate_event_sequences,
)


class DomainCapabilityTests(unittest.TestCase):
    def test_cycle_transitions_are_explicit(self):
        self.assertEqual(
            advance_cycle(CycleState.DORMANT, CycleEvent.STAGE),
            CycleState.STAGED,
        )
        with self.assertRaises(ValueError):
            advance_cycle(CycleState.DORMANT, CycleEvent.ACTIVATE)

    def test_verified_snapshot_recommends_rollback(self):
        plan = plan_recovery(
            state=CycleState.DEGRADED,
            verified_snapshot=True,
            attempt=1,
            maximum_attempts=3,
        )
        self.assertEqual(plan.action, RecoveryAction.ROLLBACK)

    def test_retry_budget_escalates(self):
        plan = plan_recovery(
            state=CycleState.ACTIVE,
            verified_snapshot=False,
            attempt=3,
            maximum_attempts=3,
        )
        self.assertEqual(plan.action, RecoveryAction.ESCALATE)

    def test_no_evidence_holds(self):
        plan = plan_recovery(
            state=CycleState.STAGED,
            verified_snapshot=False,
            attempt=0,
            maximum_attempts=2,
        )
        self.assertEqual(plan.action, RecoveryAction.HOLD)

    def test_evolution_requires_complete_evidence_and_rollback(self):
        result = evaluate_evolution(["build", "tests"], ["build"], rollback_ready=True)
        self.assertFalse(result.approved)
        self.assertEqual(result.missing_evidence, ("tests",))
        result = evaluate_evolution(["build"], ["build"], rollback_ready=True)
        self.assertTrue(result.approved)

    def test_event_sequence_is_monotonic_per_producer(self):
        errors = validate_event_sequences([
            {"producer": "node-a", "sequence": 4},
            {"producer": "node-b", "sequence": 1},
            {"producer": "node-a", "sequence": 3},
        ])
        self.assertEqual(len(errors), 1)
        self.assertIn("node-a", errors[0])

    def test_event_sequence_rejects_boolean(self):
        errors = validate_event_sequences([{"producer": "node-a", "sequence": True}])
        self.assertEqual(len(errors), 1)


if __name__ == "__main__":
    unittest.main()
