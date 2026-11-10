"""Deterministic lifecycle and recovery helpers for domain capability plans."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from collections.abc import Iterable, Mapping


class CycleState(str, Enum):
    DORMANT = "dormant"
    STAGED = "staged"
    VERIFIED = "verified"
    ACTIVE = "active"
    DEGRADED = "degraded"
    ROLLING_BACK = "rolling_back"
    RETIRED = "retired"


class CycleEvent(str, Enum):
    STAGE = "stage"
    VERIFY = "verify"
    ACTIVATE = "activate"
    DEGRADE = "degrade"
    RECOVER = "recover"
    ROLLBACK = "rollback"
    COMPLETE_ROLLBACK = "complete_rollback"
    RETIRE = "retire"
    CANCEL = "cancel"


_TRANSITIONS: Mapping[tuple[CycleState, CycleEvent], CycleState] = {
    (CycleState.DORMANT, CycleEvent.STAGE): CycleState.STAGED,
    (CycleState.STAGED, CycleEvent.VERIFY): CycleState.VERIFIED,
    (CycleState.STAGED, CycleEvent.CANCEL): CycleState.DORMANT,
    (CycleState.VERIFIED, CycleEvent.ACTIVATE): CycleState.ACTIVE,
    (CycleState.VERIFIED, CycleEvent.ROLLBACK): CycleState.ROLLING_BACK,
    (CycleState.ACTIVE, CycleEvent.DEGRADE): CycleState.DEGRADED,
    (CycleState.ACTIVE, CycleEvent.ROLLBACK): CycleState.ROLLING_BACK,
    (CycleState.ACTIVE, CycleEvent.RETIRE): CycleState.RETIRED,
    (CycleState.DEGRADED, CycleEvent.RECOVER): CycleState.ACTIVE,
    (CycleState.DEGRADED, CycleEvent.ROLLBACK): CycleState.ROLLING_BACK,
    (CycleState.DEGRADED, CycleEvent.RETIRE): CycleState.RETIRED,
    (CycleState.ROLLING_BACK, CycleEvent.COMPLETE_ROLLBACK): CycleState.DORMANT,
}


def advance_cycle(state: CycleState, event: CycleEvent) -> CycleState:
    """Advance one named step; unknown or unsafe transitions raise ValueError."""
    try:
        return _TRANSITIONS[(state, event)]
    except KeyError as exc:
        raise ValueError(f"invalid cycle transition: {state.value}/{event.value}") from exc


class RecoveryAction(str, Enum):
    RESUME = "resume"
    ROLLBACK = "rollback"
    HOLD = "hold"
    ESCALATE = "escalate"


@dataclass(frozen=True)
class RecoveryPlan:
    action: RecoveryAction
    reason: str
    attempt: int
    maximum_attempts: int


def plan_recovery(
    *,
    state: CycleState,
    verified_snapshot: bool,
    attempt: int,
    maximum_attempts: int,
) -> RecoveryPlan:
    """Produce a recommendation only; this function never activates or rolls back."""
    if maximum_attempts < 1 or attempt < 0:
        raise ValueError("attempt must be non-negative and maximum_attempts positive")
    if attempt >= maximum_attempts:
        return RecoveryPlan(
            RecoveryAction.ESCALATE, "retry budget exhausted",
            attempt, maximum_attempts,
        )
    if verified_snapshot:
        return RecoveryPlan(
            RecoveryAction.ROLLBACK, "verified recovery snapshot is available",
            attempt, maximum_attempts,
        )
    if state in {CycleState.ACTIVE, CycleState.VERIFIED}:
        return RecoveryPlan(
            RecoveryAction.RESUME, "current state is eligible for supervised resume",
            attempt, maximum_attempts,
        )
    return RecoveryPlan(
        RecoveryAction.HOLD, "state or evidence is insufficient for safe recovery",
        attempt, maximum_attempts,
    )


@dataclass(frozen=True)
class EvolutionDecision:
    approved: bool
    missing_evidence: tuple[str, ...]
    rollback_ready: bool
    reason: str


def evaluate_evolution(
    required_evidence: Iterable[str],
    available_evidence: Iterable[str],
    *,
    rollback_ready: bool,
) -> EvolutionDecision:
    required = {item.strip() for item in required_evidence}
    available = {item.strip() for item in available_evidence}
    if "" in required or "" in available:
        raise ValueError("evidence identifiers cannot be empty")
    missing = tuple(sorted(required - available))
    approved = not missing and rollback_ready
    reason = (
        "all evidence present and rollback ready" if approved
        else "missing evidence" if missing
        else "rollback is not ready"
    )
    return EvolutionDecision(approved, missing, rollback_ready, reason)


def validate_event_sequences(events: Iterable[Mapping[str, object]]) -> list[str]:
    """Check monotonic sequence per producer; return actionable validation errors."""
    last_sequence: dict[str, int] = {}
    errors: list[str] = []
    for index, event in enumerate(events):
        producer = event.get("producer")
        sequence = event.get("sequence")
        if not isinstance(producer, str) or not producer.strip():
            errors.append(f"event {index}: producer must be a non-empty string")
            continue
        if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 0:
            errors.append(f"event {index}: sequence must be a non-negative integer")
            continue
        previous = last_sequence.get(producer)
        if previous is not None and sequence <= previous:
            errors.append(
                f"event {index}: sequence {sequence} is not greater than {previous} "
                f"for producer {producer}"
            )
            continue
        last_sequence[producer] = sequence
    return errors
