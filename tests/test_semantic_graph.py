import unittest

from klipot.semantic_graph import SemanticGraphError, expand_domains


class SemanticGraphTests(unittest.TestCase):
    def test_related_domains_are_ranked_and_repeatable(self):
        first = expand_domains(["waterfowl-ecology"], depth=2)
        second = expand_domains(["waterfowl-ecology"], depth=2)
        self.assertEqual(first, second)
        self.assertEqual(first[0]["domain"], "wetland-conservation")
        self.assertTrue(all(item["domain"] != "waterfowl-ecology" for item in first))

    def test_cross_step_expansion_reaches_indirect_domains(self):
        one = {item["domain"] for item in expand_domains(["quantum-foundations"], depth=1)}
        two = {item["domain"] for item in expand_domains(["quantum-foundations"], depth=2)}
        self.assertIn("scientific-computing", one)
        self.assertIn("spatial-modeling", two)

    def test_invalid_and_unbounded_requests_fail_closed(self):
        with self.assertRaises(SemanticGraphError):
            expand_domains(["not-a-domain"])
        with self.assertRaises(SemanticGraphError):
            expand_domains(["quantum-foundations"], depth=99)
        with self.assertRaises(SemanticGraphError):
            expand_domains(["quantum-foundations"], damping=2)


if __name__ == "__main__":
    unittest.main()
