"""Deterministic dependency and capability planner for NUN manifests."""
from __future__ import annotations

import heapq
from collections.abc import Mapping
from typing import Any


class ManifestError(ValueError):
    """Raised when an ecosystem manifest violates its integration contract."""


def _string_list(value: Any, field: str, component_id: str) -> list[str]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise ManifestError(
            f"{component_id}: '{field}' must be an array of non-empty strings"
        )
    if len(set(value)) != len(value):
        raise ManifestError(f"{component_id}: '{field}' contains duplicates")
    return value


def validate_manifest(document: Any) -> dict[str, dict[str, Any]]:
    """Validate shape, references, acyclicity, and dependency capability closure."""
    if not isinstance(document, Mapping):
        raise ManifestError("manifest root must be an object")
    if document.get("schema_version") != "nun.ecosystem.v1":
        raise ManifestError("schema_version must be 'nun.ecosystem.v1'")
    components = document.get("components")
    if not isinstance(components, list) or not components:
        raise ManifestError("components must be a non-empty array")

    index: dict[str, dict[str, Any]] = {}
    for raw in components:
        if not isinstance(raw, Mapping):
            raise ManifestError("each component must be an object")
        component_id = raw.get("id")
        if not isinstance(component_id, str) or not component_id.strip():
            raise ManifestError("each component must have a non-empty id")
        if component_id in index:
            raise ManifestError(f"duplicate component id: {component_id}")
        for field in ("repo", "role"):
            if not isinstance(raw.get(field), str) or not raw[field].strip():
                raise ManifestError(
                    f"{component_id}: '{field}' must be a non-empty string"
                )
        item = dict(raw)
        item["depends_on"] = _string_list(
            raw.get("depends_on", []), "depends_on", component_id
        )
        item["provides"] = _string_list(
            raw.get("provides", []), "provides", component_id
        )
        item["requires"] = _string_list(
            raw.get("requires", []), "requires", component_id
        )
        index[component_id] = item

    for component_id, item in index.items():
        for dependency in item["depends_on"]:
            if dependency == component_id:
                raise ManifestError(f"{component_id}: self-dependency is not allowed")
            if dependency not in index:
                raise ManifestError(
                    f"{component_id}: unknown dependency '{dependency}'"
                )

    # Stable topological sort also detects dependency cycles.
    indegree = {key: len(item["depends_on"]) for key, item in index.items()}
    dependents: dict[str, list[str]] = {key: [] for key in index}
    for child, item in index.items():
        for parent in item["depends_on"]:
            dependents[parent].append(child)
    ready = [key for key, degree in indegree.items() if degree == 0]
    heapq.heapify(ready)
    ordered: list[str] = []
    while ready:
        current = heapq.heappop(ready)
        ordered.append(current)
        for child in sorted(dependents[current]):
            indegree[child] -= 1
            if indegree[child] == 0:
                heapq.heappush(ready, child)
    if len(ordered) != len(index):
        cyclic = sorted(key for key, degree in indegree.items() if degree > 0)
        raise ManifestError(
            f"dependency cycle detected involving: {', '.join(cyclic)}"
        )

    ancestors_cache: dict[str, set[str]] = {}

    def ancestors(component_id: str) -> set[str]:
        if component_id not in ancestors_cache:
            result: set[str] = set()
            for dependency in index[component_id]["depends_on"]:
                result.add(dependency)
                result.update(ancestors(dependency))
            ancestors_cache[component_id] = result
        return ancestors_cache[component_id]

    for component_id, item in index.items():
        available: dict[str, list[str]] = {}
        for ancestor in ancestors(component_id):
            for capability in index[ancestor]["provides"]:
                available.setdefault(capability, []).append(ancestor)
        for capability in item["requires"]:
            matches = sorted(set(available.get(capability, [])))
            if not matches:
                raise ManifestError(
                    f"{component_id}: required capability '{capability}' "
                    "is not provided by a dependency"
                )
            if len(matches) > 1:
                raise ManifestError(
                    f"{component_id}: capability '{capability}' has "
                    f"ambiguous providers: {', '.join(matches)}"
                )

    return index


def build_plan(document: Any) -> dict[str, Any]:
    """Return a stable, dependency-first integration plan."""
    index = validate_manifest(document)
    indegree = {key: len(item["depends_on"]) for key, item in index.items()}
    dependents: dict[str, list[str]] = {key: [] for key in index}
    for child, item in index.items():
        for parent in item["depends_on"]:
            dependents[parent].append(child)
    ready = [key for key, degree in indegree.items() if degree == 0]
    heapq.heapify(ready)
    steps: list[dict[str, Any]] = []
    while ready:
        current = heapq.heappop(ready)
        item = index[current]
        steps.append({
            "id": current,
            "repo": item["repo"],
            "role": item["role"],
            "depends_on": sorted(item["depends_on"]),
            "provides": sorted(item["provides"]),
            "requires": sorted(item["requires"]),
            "integration_status": item.get(
                "integration_status", "contract-only"
            ),
        })
        for child in sorted(dependents[current]):
            indegree[child] -= 1
            if indegree[child] == 0:
                heapq.heappush(ready, child)
    system = document.get("system", {})
    return {
        "schema_version": "klipot.plan.v1",
        "system": system.get("id", "unnamed")
        if isinstance(system, Mapping) else "unnamed",
        "ordered_components": [step["id"] for step in steps],
        "steps": steps,
    }
