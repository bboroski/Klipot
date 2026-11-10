# NUN contracts and event rules

## Versioning

Contract identifiers use `nun.<domain>.v1`. Each schema is versioned independently of the producer's application version. Additive optional fields may be introduced only when older consumers safely ignore them. Changes to required meaning, units, ordering or safety semantics require a new major contract version.

## Capability semantics

- `provides` declares an interface a component can actually expose.
- `requires` declares interfaces that must be available before the component is admitted.
- A provider must be in the declared dependency closure.
- Capability names are stable identifiers, not free-form feature descriptions.
- A manifest entry is not qualification evidence. Hardware support still requires the actual board, package, toolchain, fixtures and test records.

## Resource profiles

A resource profile is an upper bound for memory, queue slots and caller-defined work units. Zero means no work is admitted for that resource; it never means unlimited. `reserve_percent` is held back for critical reporting and recovery and is not available to optional tasks.

Overflow policy is domain-specific:
- `reject_new` is the safe default for commands and work admission.
- `backpressure` is appropriate when a producer can slow down.
- `drop_oldest_telemetry` is permitted only for explicitly lossy telemetry.
- `shed_optional` may discard optional work; critical actions are never silently downgraded.

## Event envelope

The event envelope provides producer identity, a per-producer sequence number and a monotonic clock sample. It does not establish a global total order. Consumers should be idempotent on `(producer, sequence)` and detect gaps. Wall-clock timestamps may be added by an adapter, but must not replace monotonic ordering for duration measurement.

Events are observations, not commands. A critical event cannot by itself authorize a firmware flash, reset, voltage change, unlock or destructive test. Such actions need an authenticated command path and the local policy that owns the actuator.

## Data and integrity

Classify exported payloads as public, internal, sensitive or restricted. Redact serial numbers, hardware identifiers, user paths and device content unless explicitly required and authorized. CRC-32 is for accidental corruption detection only. For adversarial integrity, use a reviewed cryptographic signature/MAC and protected key handling.

Append-only journals still need capacity, rotation, retention, erasure and crash-recovery rules. WORM storage is an optional storage property, not something implied by writing JSONL.

## Execution trust

Declarations do not run code. Future plugin execution must use least-privilege capabilities, pinned versions, resource limits and an isolated process or VM. Native in-process loading is not a sandbox. On targets without process isolation, accept only reviewed firmware built into the trusted image.
