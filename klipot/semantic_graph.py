"""Bounded cross-domain relation expansion for the Klipot control plane.

Scores represent curated conceptual relationships, not scientific causation.
Operational reactor control, weapon targeting and animal-harassment workflows
are intentionally outside this semantic index.
"""
from __future__ import annotations

import math
from collections.abc import Iterable

MAX_DEPTH = 5
DOMAINS = (
    "quantum-foundations",
    "scientific-computing",
    "spatial-modeling",
    "sensor-integrity",
    "pipeline-integrity",
    "waterfowl-ecology",
    "wetland-conservation",
    "systems-engineering",
)
# Undirected links are expanded into a directed row-normalized matrix.
_LINKS = (
    ("quantum-foundations", "scientific-computing", 0.92),
    ("scientific-computing", "spatial-modeling", 0.78),
    ("spatial-modeling", "sensor-integrity", 0.76),
    ("sensor-integrity", "pipeline-integrity", 0.90),
    ("systems-engineering", "sensor-integrity", 0.82),
    ("systems-engineering", "scientific-computing", 0.70),
    ("waterfowl-ecology", "wetland-conservation", 0.96),
    ("wetland-conservation", "spatial-modeling", 0.54),
)


class SemanticGraphError(ValueError):
    """Raised for invalid seeds or unbounded expansion requests."""


def expand_domains(seeds: Iterable[str], *, depth: int = 2,
                   damping: float = 0.6) -> list[dict[str, float | str]]:
    """Return a deterministic ranked list of related domains."""
    seed_list = list(seeds)
    if not seed_list or any(not isinstance(item, str) or item not in DOMAINS for item in seed_list):
        raise SemanticGraphError("seeds must contain known domain identifiers")
    if len(set(seed_list)) != len(seed_list):
        raise SemanticGraphError("seeds must be unique")
    if not isinstance(depth, int) or isinstance(depth, bool) or not 1 <= depth <= MAX_DEPTH:
        raise SemanticGraphError(f"depth must be between 1 and {MAX_DEPTH}")
    damping = float(damping)
    if not math.isfinite(damping) or not 0.0 <= damping <= 1.0:
        raise SemanticGraphError("damping must be between 0 and 1")

    index = {name: pos for pos, name in enumerate(DOMAINS)}
    n = len(DOMAINS)
    adjacency = [[0.0] * n for _ in range(n)]
    for left, right, weight in _LINKS:
        adjacency[index[left]][index[right]] = weight
        adjacency[index[right]][index[left]] = weight
    for row in adjacency:
        total = sum(row)
        if total:
            for col in range(n):
                row[col] /= total

    frontier = [[0.0] * n for _ in range(n)]
    for seed in seed_list:
        frontier[index[seed]][index[seed]] = 1.0 / len(seed_list)
    scores = [0.0] * n
    factor = 1.0
    for _ in range(depth):
        next_frontier = [0.0] * n
        for source in range(n):
            mass = frontier[source][source]
            if mass:
                for target in range(n):
                    next_frontier[target] += mass * adjacency[source][target]
        for target in range(n):
            scores[target] += factor * next_frontier[target]
            frontier[target][target] = next_frontier[target]
        factor *= damping

    for seed in seed_list:
        scores[index[seed]] = 0.0
    ranked = [
        {"domain": name, "score": round(scores[index[name]], 8)}
        for name in DOMAINS if scores[index[name]] > 0.0
    ]
    return sorted(ranked, key=lambda item: (-float(item["score"]), str(item["domain"])))
