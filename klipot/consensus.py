"""Deterministic, evidence-linked voting for high-impact integration changes.

This module computes a review result only. It does not merge code, deploy systems,
grant capabilities, or establish the identity of a reviewer.
"""
from __future__ import annotations

from collections.abc import Mapping
from hashlib import sha256
import json
import math
from typing import Any


class ConsensusError(ValueError):
    """Raised when a review proposal or its voting record is malformed."""


def _identifier(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 128:
        raise ConsensusError(f"{field} must be a non-empty string of at most 128 characters")
    return value.strip()


def _unique_identifiers(values: Any, field: str, *, minimum: int = 1) -> tuple[str, ...]:
    if not isinstance(values, (list, tuple)):
        raise ConsensusError(f"{field} must be an array of identifiers")
    if not minimum <= len(values) <= 256:
        raise ConsensusError(f"{field} must contain {minimum} to 256 entries")
    normalized = tuple(_identifier(item, field) for item in values)
    if len(set(normalized)) != len(normalized):
        raise ConsensusError(f"{field} contains duplicate identifiers")
    return tuple(sorted(normalized))


def evaluate_consensus(
    proposal_id: str,
    eligible_reviewers: Any,
    votes: Any,
    *,
    quorum_percent: int = 60,
    minimum_votes: int = 1,
) -> dict[str, Any]:
    """Evaluate an auditable one-person-one-vote review record.

    Every submitted vote (including abstention) contributes to participation
    quorum. Only approve/reject votes determine the outcome. Approve/reject votes
    must cite evidence. A tie, or a quorum with no decisive votes, stays pending.
    """
    proposal = _identifier(proposal_id, "proposal_id")
    eligible = _unique_identifiers(eligible_reviewers, "eligible_reviewers")

    if isinstance(quorum_percent, bool) or not isinstance(quorum_percent, int):
        raise ConsensusError("quorum_percent must be an integer from 1 to 100")
    if not 1 <= quorum_percent <= 100:
        raise ConsensusError("quorum_percent must be an integer from 1 to 100")
    if isinstance(minimum_votes, bool) or not isinstance(minimum_votes, int):
        raise ConsensusError("minimum_votes must be an integer within the eligible set")
    if not 1 <= minimum_votes <= len(eligible):
        raise ConsensusError("minimum_votes must be between 1 and the eligible reviewer count")
    if not isinstance(votes, (list, tuple)) or len(votes) > len(eligible):
        raise ConsensusError("votes must be an array no larger than the eligible reviewer set")

    normalized_votes: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(votes):
        if not isinstance(raw, Mapping):
            raise ConsensusError(f"votes[{index}] must be an object")
        reviewer = _identifier(raw.get("reviewer"), f"votes[{index}].reviewer")
        if reviewer not in eligible:
            raise ConsensusError(f"reviewer '{reviewer}' is not eligible")
        if reviewer in seen:
            raise ConsensusError(f"reviewer '{reviewer}' submitted more than one vote")
        seen.add(reviewer)

        decision = raw.get("decision")
        if decision not in {"approve", "reject", "abstain"}:
            raise ConsensusError(f"votes[{index}].decision must be approve, reject, or abstain")

        references = raw.get("evidence_refs", [])
        if not isinstance(references, (list, tuple)) or len(references) > 128:
            raise ConsensusError(f"votes[{index}].evidence_refs must be an array of at most 128 references")
        refs = tuple(sorted({_identifier(ref, f"votes[{index}].evidence_refs") for ref in references}))
        if decision in {"approve", "reject"} and not refs:
            raise ConsensusError(f"votes[{index}] requires evidence_refs for {decision}")
        normalized_votes.append({
            "reviewer": reviewer,
            "decision": decision,
            "evidence_refs": list(refs),
        })

    normalized_votes.sort(key=lambda item: item["reviewer"])
    approvals = sum(item["decision"] == "approve" for item in normalized_votes)
    rejections = sum(item["decision"] == "reject" for item in normalized_votes)
    abstentions = sum(item["decision"] == "abstain" for item in normalized_votes)
    participation = len(normalized_votes)
    percentage_required = math.ceil(len(eligible) * quorum_percent / 100)
    required = max(minimum_votes, percentage_required)
    quorum_reached = participation >= required

    if not quorum_reached:
        status = "no_quorum"
    elif approvals > rejections:
        status = "approved"
    elif rejections > approvals:
        status = "rejected"
    else:
        status = "pending"

    payload = {
        "schema_version": "klipot.consensus.v1",
        "proposal_id": proposal,
        "status": status,
        "decision_scope": "review_only",
        "eligible_reviewers": list(eligible),
        "participation": participation,
        "required_participation": required,
        "quorum_percent": quorum_percent,
        "quorum_reached": quorum_reached,
        "approve": approvals,
        "reject": rejections,
        "abstain": abstentions,
        "votes": normalized_votes,
    }
    canonical = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    )
    payload["digest_sha256"] = sha256(canonical.encode("utf-8")).hexdigest()
    return payload


__all__ = ["ConsensusError", "evaluate_consensus"]
