"""Deterministic uncertainty-to-feature planner.

Unknown facts are never silently promoted to confirmed capabilities. This module
turns each registered uncertainty into a concrete next action while keeping
execution and approval in the owning repository.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

SCHEMA_VERSION = "klipot.uncertainty.v1"
RESOLUTION_MODES = {
    "probe", "explicit-config", "human-gate", "fail-closed",
    "staged-implementation", "feature-flag",
}
STATUSES = {"open", "resolved", "blocked"}
IMPLEMENTATION_STATES = {"planned", "implemented", "verified"}
NEXT_STEPS = {
    "probe": "run-probe",
    "explicit-config": "request-explicit-configuration",
    "human-gate": "request-owner-approval",
    "fail-closed": "block-dependent-operation",
    "staged-implementation": "implement-and-test-feature",
    "feature-flag": "keep-disabled-until-verified",
}


class UncertaintyError(ValueError):
    """Raised when an uncertainty registry is incomplete or contradictory."""


def _required_text(item: Mapping[str, Any], key: str, item_id: str) -> str:
    value = item.get(key)
    if not isinstance(value, str) or not value.strip():
        raise UncertaintyError(f"{item_id}: '{key}' must be a non-empty string")
    return value.strip()


def validate_registry(document: Any) -> list[dict[str, Any]]:
    """Validate the registry and return normalized items in stable ID order."""
    if not isinstance(document, Mapping):
        raise UncertaintyError("registry root must be an object")
    if document.get("schema_version") != SCHEMA_VERSION:
        raise UncertaintyError(f"schema_version must be '{SCHEMA_VERSION}'")
    repository = document.get("repository")
    if not isinstance(repository, str) or "/" not in repository:
        raise UncertaintyError("repository must use owner/name form")
    raw_items = document.get("items")
    if not isinstance(raw_items, list):
        raise UncertaintyError("items must be an array")

    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in raw_items:
        if not isinstance(raw, Mapping):
            raise UncertaintyError("each item must be an object")
        item = dict(raw)
        item_id = _required_text(item, "id", "registry item")
        if item_id in seen:
            raise UncertaintyError(f"duplicate uncertainty id: {item_id}")
        seen.add(item_id)
        for key in ("domain", "statement", "feature", "unknown_behavior"):
            _required_text(item, key, item_id)
        mode = _required_text(item, "resolution_mode", item_id)
        if mode not in RESOLUTION_MODES:
            raise UncertaintyError(f"{item_id}: unsupported resolution_mode '{mode}'")
        status = item.get("status", "open")
        if status not in STATUSES:
            raise UncertaintyError(f"{item_id}: status must be one of {sorted(STATUSES)}")
        implementation = item.get("implementation_status", "planned")
        if implementation not in IMPLEMENTATION_STATES:
            raise UncertaintyError(
                f"{item_id}: implementation_status must be one of "
                f"{sorted(IMPLEMENTATION_STATES)}"
            )
        verification = item.get("verification")
        if not isinstance(verification, list) or not verification or any(
            not isinstance(value, str) or not value.strip() for value in verification
        ):
            raise UncertaintyError(
                f"{item_id}: verification must contain non-empty acceptance checks"
            )
        evidence = item.get("evidence", [])
        if not isinstance(evidence, list) or any(
            not isinstance(value, str) or not value.strip() for value in evidence
        ):
            raise UncertaintyError(f"{item_id}: evidence must be an array of strings")
        if status == "resolved" and not evidence:
            raise UncertaintyError(
                f"{item_id}: resolved items require at least one evidence reference"
            )
        if implementation == "verified" and not evidence:
            raise UncertaintyError(
                f"{item_id}: verified implementations require evidence references"
            )
        item["status"] = status
        item["implementation_status"] = implementation
        item["verification"] = list(verification)
        item["evidence"] = list(evidence)
        normalized.append(item)
    return sorted(normalized, key=lambda value: value["id"])


def _make_action(item: Mapping[str, Any], repository: str | None = None) -> dict[str, Any]:
    status = item["status"]
    implementation = item["implementation_status"]
    mode = item["resolution_mode"]
    if status == "resolved":
        next_step = "none"
    elif implementation == "implemented":
        next_step = "run-acceptance-checks"
    elif implementation == "verified":
        next_step = "request-owner-closure"
    else:
        next_step = NEXT_STEPS[mode]
    action = {
        "id": item["id"],
        "domain": item["domain"],
        "feature": item["feature"],
        "status": status,
        "implementation_status": implementation,
        "resolution_mode": mode,
        "next_step": next_step,
        "unknown_behavior": item["unknown_behavior"],
        "verification": item["verification"],
        "evidence": item["evidence"],
    }
    if repository is not None:
        action["repository"] = repository
    return action


def _counts(items: list[Mapping[str, Any]]) -> tuple[dict[str, int], dict[str, int]]:
    status_counts = {
        status: sum(1 for item in items if item["status"] == status)
        for status in sorted(STATUSES)
    }
    implementation_counts = {
        state: sum(
            1 for item in items if item["implementation_status"] == state
        )
        for state in sorted(IMPLEMENTATION_STATES)
    }
    return status_counts, implementation_counts


def build_resolution_plan(document: Any) -> dict[str, Any]:
    """Build an actionable plan without probing, changing files, or guessing."""
    items = validate_registry(document)
    actions = [_make_action(item) for item in items]
    counts, implementation_counts = _counts(items)
    return {
        "schema_version": "klipot.resolution-plan.v1",
        "repository": document["repository"],
        "total": len(items),
        "counts": counts,
        "implementation_counts": implementation_counts,
        "actions": actions,
    }


def build_workspace_plan(documents: Iterable[Any]) -> dict[str, Any]:
    """Aggregate repository registries into one deterministic workspace plan."""
    if isinstance(documents, (str, bytes, Mapping)):
        raise UncertaintyError("workspace registries must be an iterable of documents")

    repositories: set[str] = set()
    item_ids: set[str] = set()
    normalized: list[dict[str, Any]] = []

    for document in documents:
        items = validate_registry(document)
        repository = document["repository"].strip()
        if repository in repositories:
            raise UncertaintyError(f"duplicate repository registry: {repository}")
        repositories.add(repository)
        for item in items:
            item_id = item["id"]
            if item_id in item_ids:
                raise UncertaintyError(f"duplicate workspace uncertainty id: {item_id}")
            item_ids.add(item_id)
            normalized.append({**item, "repository": repository})

    normalized.sort(key=lambda value: (value["repository"], value["id"]))
    actions = [_make_action(item, item["repository"]) for item in normalized]
    counts, implementation_counts = _counts(normalized)

    return {
        "schema_version": "klipot.workspace-plan.v1",
        "repository_count": len(repositories),
        "repositories": sorted(repositories),
        "total": len(normalized),
        "counts": counts,
        "implementation_counts": implementation_counts,
        "actions": actions,
    }
