import unittest

from klipot.consensus import ConsensusError, evaluate_consensus


class ConsensusTests(unittest.TestCase):
    def setUp(self):
        self.eligible = ["maintainer-a", "maintainer-b", "maintainer-c", "maintainer-d"]

    def test_quorum_approval_is_deterministic_and_evidence_linked(self):
        votes = [
            {"reviewer": "maintainer-c", "decision": "approve", "evidence_refs": ["ci:run/42"]},
            {"reviewer": "maintainer-a", "decision": "approve", "evidence_refs": ["review:17"]},
            {"reviewer": "maintainer-b", "decision": "abstain"},
        ]
        result = evaluate_consensus("change-42", self.eligible, votes, quorum_percent=75)
        self.assertEqual(result["status"], "approved")
        self.assertTrue(result["quorum_reached"])
        self.assertEqual(result["participation"], 3)
        self.assertEqual(result["approve"], 2)
        self.assertEqual(result["abstain"], 1)
        self.assertEqual(result["decision_scope"], "review_only")
        self.assertEqual(
            result["digest_sha256"],
            evaluate_consensus("change-42", self.eligible, list(reversed(votes)),
                               quorum_percent=75)["digest_sha256"],
        )

    def test_missing_quorum_does_not_produce_approval(self):
        result = evaluate_consensus(
            "change-43", self.eligible,
            [{"reviewer": "maintainer-a", "decision": "approve", "evidence_refs": ["ci:1"]}],
            quorum_percent=75,
        )
        self.assertEqual(result["status"], "no_quorum")
        self.assertFalse(result["quorum_reached"])

    def test_rejection_requires_evidence_and_dominant_rejection(self):
        result = evaluate_consensus(
            "change-44", self.eligible,
            [
                {"reviewer": "maintainer-a", "decision": "reject", "evidence_refs": ["security: finding-2"]},
                {"reviewer": "maintainer-b", "decision": "reject", "evidence_refs": ["test:failed-9"]},
                {"reviewer": "maintainer-c", "decision": "approve", "evidence_refs": ["ci:green"]},
            ],
            quorum_percent=75,
        )
        self.assertEqual(result["status"], "rejected")

    def test_tie_and_all_abstain_remain_pending(self):
        tied = evaluate_consensus(
            "change-45", self.eligible,
            [
                {"reviewer": "maintainer-a", "decision": "approve", "evidence_refs": ["a"]},
                {"reviewer": "maintainer-b", "decision": "reject", "evidence_refs": ["b"]},
                {"reviewer": "maintainer-c", "decision": "abstain"},
            ],
            quorum_percent=75,
        )
        self.assertEqual(tied["status"], "pending")
        abstained = evaluate_consensus(
            "change-46", self.eligible,
            [{"reviewer": name, "decision": "abstain"} for name in self.eligible],
        )
        self.assertEqual(abstained["status"], "pending")

    def test_duplicate_or_ineligible_reviewer_is_rejected(self):
        vote = {"reviewer": "maintainer-a", "decision": "approve", "evidence_refs": ["ci:1"]}
        with self.assertRaises(ConsensusError):
            evaluate_consensus("x", self.eligible, [vote, vote])
        with self.assertRaises(ConsensusError):
            evaluate_consensus("x", self.eligible, [
                {"reviewer": "outsider", "decision": "approve", "evidence_refs": ["ci:1"]}
            ])

    def test_decisive_votes_require_evidence(self):
        with self.assertRaises(ConsensusError):
            evaluate_consensus("x", self.eligible, [
                {"reviewer": "maintainer-a", "decision": "approve"}
            ])
        with self.assertRaises(ConsensusError):
            evaluate_consensus("x", self.eligible, [
                {"reviewer": "maintainer-a", "decision": "reject", "evidence_refs": ["", "a"]}
            ])

    def test_invalid_policy_and_vote_shape_are_rejected(self):
        for kwargs in ({"quorum_percent": 0}, {"quorum_percent": 101}, {"minimum_votes": 0},
                       {"minimum_votes": 5}, {"minimum_votes": True}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ConsensusError):
                evaluate_consensus("x", self.eligible, [], **kwargs)
        with self.assertRaises(ConsensusError):
            evaluate_consensus("x", self.eligible, {})
        with self.assertRaises(ConsensusError):
            evaluate_consensus("", self.eligible, [])
        with self.assertRaises(ConsensusError):
            evaluate_consensus("x", ["one", "one"], [])


if __name__ == "__main__":
    unittest.main()
