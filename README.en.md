# Klipot — Modular Integration Orchestrator

**Klipot** is the composition layer for integrating independent software and hardware subsystems into larger, verifiable solutions.

> **Status:** the repository is at an initial stage. This README defines target architecture and boundaries; a component registry, dependency solver, execution engine and production sandbox must not be treated as implemented without corresponding code and tests.

## Architectural role

Klipot coordinates integration without replacing components, taking ownership of their resources or bypassing local policy.

| Subsystem | Technical responsibility |
|---|---|
| **Manifest Registry** | Versioned component declarations, ABI, capabilities and resource budgets |
| **Dependency Solver** | Acyclic dependency graph and version compatibility checks |
| **Contract Validator** | Schema, layout, message-type, contract and migration validation |
| **Capability Policy** | Least-privilege grants; unknown capabilities are denied by default |
| **Integration Planner** | Reproducible composition plan, initialization order and conflict analysis |
| **Recovery Coordinator** | Rollback plan, retry ceilings and failure-cause preservation |
| **Evidence Journal** | Versioned records, artifact hashes, verification results and configuration provenance |
| **Adapter Boundary** | Isolation of platform, network, filesystem and hardware integrations |

## Target composition

```text
          Product / Firmware / Desktop Application
                           |
                    Integration Plan
                           |
        +------------------+------------------+
        |                  |                  |
   Language & DSL    Lifecycle Control   Runtime Assurance
      SAMBU                CO                SaintSI
        |                  |                  |
   Local UI/Tools     Production Runtime   Platform ABI
     ToolNG           ReaperCripple           Kloz
        \                  |                  /
         +----------- Versioned Adapters -----+
                           |
                    Klipot Coordinator
```

This is a target boundary map. It does not claim that every repository currently imports every other repository or that every edge has been build-verified. See the [unified integration contract](docs/PLATFORM_INTEGRATION.md).

## Engineering rules

1. **Contract first:** begin with versioned APIs/ABIs and schemas.
2. **Acyclic dependencies:** cycles block the integration plan.
3. **Least privilege:** each component receives only explicitly granted capabilities.
4. **Bounded execution:** memory, queues, time, retries and logs have limits.
5. **Transactional lifecycle:** partial initialization is cleaned up in reverse order.
6. **Immutable evidence:** append new verification records; do not rewrite past results.
7. **Reversible changes:** every integration step has a tested rollback plan.
8. **Human-controlled release:** the coordinator may prepare and validate a plan, but must not bypass approval, merge or deployment policy.

## Implementation sequence

- [ ] Component manifest schema and version registry.
- [ ] ABI, capability-set and resource-budget validator.
- [ ] Deterministic dependency solver with cycle detection.
- [ ] Integration-plan format with artifact checksums.
- [ ] Compatible lifecycle and fault-report adapters.
- [ ] Tests for missing capabilities, incompatible versions and partial rollback.
- [ ] Isolated worker runner only after OS-level enforcement and adversarial tests.
- [ ] UI for graph inspection, plan diff, risk review and verification results.

A feature is implemented only when code, positive and negative tests, usage examples, resource limits, compatibility notes and actual CI evidence exist.

**Goal:** compose systems through explicit contracts, not hidden magic.
