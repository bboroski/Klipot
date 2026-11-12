import unittest

from klipot.temporal_graph import (
    KlipotEventNode, temporal_neighbors, topological_event_order,
    validate_event_graph,
)


class TemporalGraphTests(unittest.TestCase):
    def test_order_respects_declared_prerequisites(self):
        nodes = [
            KlipotEventNode("b", "2020-01-02T00:00:00Z", ("a",)),
            KlipotEventNode("a", "2020-01-01T00:00:00Z"),
        ]
        self.assertEqual(topological_event_order(nodes), ["a", "b"])
        self.assertEqual(validate_event_graph(nodes), [])

    def test_cycles_and_late_prerequisites_are_rejected(self):
        nodes = [
            KlipotEventNode("a", "2020-01-02T00:00:00Z", ("b",)),
            KlipotEventNode("b", "2020-01-01T00:00:00Z", ("a",)),
        ]
        errors = validate_event_graph(nodes)
        self.assertTrue(any("cycle" in error for error in errors))
        self.assertTrue(any("occurs later" in error for error in errors))

    def test_temporal_neighbor_is_not_a_causal_edge(self):
        nodes = [
            KlipotEventNode("x", "2020-01-01T00:00:00Z", labels=("signal",)),
            KlipotEventNode("y", "2020-01-01T00:00:20Z", labels=("signal",)),
        ]
        self.assertEqual(temporal_neighbors(nodes, 30), [("x", "y", ("signal",))])


if __name__ == "__main__":
    unittest.main()
