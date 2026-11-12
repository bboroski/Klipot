"""Temporal and causal graph primitives for evidence-aware planning."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
from typing import Sequence


def _moment(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timestamps require an explicit UTC offset")
    return parsed


@dataclass(frozen=True)
class KlipotEventNode:
    node_id: str
    occurred_at: str
    prerequisites: tuple[str, ...] = field(default_factory=tuple)
    labels: tuple[str, ...] = field(default_factory=tuple)


def validate_event_graph(nodes: Sequence[KlipotEventNode]) -> list[str]:
    errors: list[str] = []
    by_id: dict[str, KlipotEventNode] = {}
    for node in nodes:
        if not node.node_id or node.node_id in by_id:
            errors.append(f"missing or duplicate node_id: {node.node_id!r}")
            continue
        by_id[node.node_id] = node
        try:
            _moment(node.occurred_at)
        except (TypeError, ValueError):
            errors.append(f"{node.node_id}: invalid timezone-aware occurred_at")
    for node in by_id.values():
        for parent_id in node.prerequisites:
            parent = by_id.get(parent_id)
            if parent is None:
                errors.append(f"{node.node_id}: missing prerequisite {parent_id}")
                continue
            try:
                if _moment(parent.occurred_at) > _moment(node.occurred_at):
                    errors.append(f"{node.node_id}: prerequisite {parent_id} occurs later")
            except (TypeError, ValueError):
                pass
    try:
        topological_event_order(nodes)
    except ValueError as exc:
        errors.append(str(exc))
    return errors


def topological_event_order(nodes: Sequence[KlipotEventNode]) -> list[str]:
    by_id = {node.node_id: node for node in nodes}
    if len(by_id) != len(nodes) or any(not key for key in by_id):
        raise ValueError("event graph contains missing or duplicate identifiers")
    indegree = {key: 0 for key in by_id}
    children: dict[str, list[str]] = defaultdict(list)
    for node in nodes:
        for parent in node.prerequisites:
            if parent not in by_id:
                raise ValueError(f"unresolved prerequisite: {parent}")
            indegree[node.node_id] += 1
            children[parent].append(node.node_id)
    ready = sorted((key for key, degree in indegree.items() if degree == 0),
                   key=lambda key: (_moment(by_id[key].occurred_at), key))
    ordered: list[str] = []
    while ready:
        current = ready.pop(0)
        ordered.append(current)
        for child in sorted(children[current]):
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
                ready.sort(key=lambda key: (_moment(by_id[key].occurred_at), key))
    if len(ordered) != len(nodes):
        raise ValueError("causal hypothesis graph contains a cycle")
    return ordered


def temporal_neighbors(
    nodes: Sequence[KlipotEventNode], window_seconds: float
) -> list[tuple[str, str, tuple[str, ...]]]:
    """Find label-based time neighbors. Similarity does not prove causation."""
    if window_seconds < 0:
        raise ValueError("window_seconds must be non-negative")
    ordered = sorted(nodes, key=lambda node: (_moment(node.occurred_at), node.node_id))
    result: list[tuple[str, str, tuple[str, ...]]] = []
    for index, left in enumerate(ordered):
        left_time = _moment(left.occurred_at)
        for right in ordered[index + 1:]:
            delta = (_moment(right.occurred_at) - left_time).total_seconds()
            if delta > window_seconds:
                break
            shared = tuple(sorted(set(left.labels) & set(right.labels)))
            if shared:
                result.append((left.node_id, right.node_id, shared))
    return result
