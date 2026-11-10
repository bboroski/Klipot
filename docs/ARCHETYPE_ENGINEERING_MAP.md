# Archetype-to-engineering map

Character and myth references are design prompts only. They are not implementation specifications and do not override engineering evidence.

## Five mechanisms

| Archetype | Engineering principle | Concrete mechanism | Failure rule |
|---|---|---|---|
| Alucard | Power is useful only behind controls | Hard resource ceilings, admission control, bounded pools, circuit breakers and critical reserves | Emergency mode sheds optional work; it never removes CPU, memory or queue ceilings |
| Shanks | Coordination should be deliberate and small | Independent components, health signals, gossip for non-critical metadata, epochs and fencing for ownership | Eventual consistency is not accepted for safety decisions or destructive operations |
| Nun | Structure emerges from a traceable substrate | Append-only event records, checkpoints, deterministic replay and controlled fault injection | Logs have retention, privacy, capacity and integrity policy; they are not infinite or automatically immutable |
| Ging Freecss | Complex behavior should be declarative and inspectable | Typed DSL/AST, explicit rules, versioned schemas, deterministic planning and reproducible fixtures | No opaque rules, undocumented side effects or dynamic evaluation of untrusted input |
| Jinn | Background capability must remain contained | Bounded workers, explicit mailboxes, watchdogs and least-privilege process/VM isolation | On bare metal, use cooperative bounded work; do not claim process isolation without an MMU/OS or VM boundary |

## Alucard: resource seals

Use `NORMAL`, `CONSTRAINED` and `EMERGENCY` policy bands. The band changes admission and priority, not the hard ceiling. Each workload declares maximum memory, queue slots and work units. A reserve is held for fault reporting, shutdown and recovery.

The Kloz budget API accounts for caller-reserved memory, queue capacity and cumulative work. It does not intercept arbitrary allocations or preempt an overlong callback; callers must reserve before allocation and keep callbacks bounded.

## Shanks: decentralized but fenced

Gossip and eventual consistency suit fleet inventory, non-critical telemetry and replicated dashboards. A node that loses an authoritative lease must stop side effects requiring exclusive ownership. Use monotonic epochs or fencing tokens to prevent a stale node from resuming a write after a partition.

Kloz, CO and SaintSI remain independently usable libraries. Their adapters are explicit; they do not require a global singleton or central lock.

## Nun: event history and recovery

Represent state transitions as versioned events and periodically store validated checkpoints. Replay must be deterministic for the recorded input, schema version and policy version. Rotate or expire logs according to privacy and storage rules. Signed records or authenticated hashes are required when adversarial tampering is in scope; CRC alone is not authentication.

Chaos experiments belong in host simulation, staging or a controlled hardware fixture. They need a stop condition, bounded blast radius and known safe-state path. Do not inject destructive faults into a live production unit to imitate a mythic cycle.

## Ging: declarative systems

SAMBU is the policy-authoring candidate; Klipot validates exported contracts before they enter a plan. Rules should be typed, deterministic, versioned and inspectable. Document intent and invariants directly: intentionally obscure documentation is not a resilience feature.

## Jinn: isolated workers

Heavy host-side work can be delegated to a bounded process or WASM worker with explicit file, network and CPU permissions. Embedded work should use fixed-size queues and cooperative steps under CO; a bare-metal callback is not a daemon process. A watchdog can detect missing progress but cannot prove that a worker's result is correct.

## Repository allocation

- Kloz: resource accounting and machine-level platform contracts.
- CO: deterministic lifecycle and cooperative work dispatch.
- SaintSI: health observations and explicit degraded-state signals.
- ReaperCripple: board profiles, production gates, rollback and MES evidence.
- SAMBU: declarative policy and workflow authoring.
- ToolNG: local diagnostic evidence and privacy-preserving reports.
- Klipot: manifest validation, capability resolution and cross-repository planning.
