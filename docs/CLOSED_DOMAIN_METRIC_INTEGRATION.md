# Closed-Domain Boundary Profile — Klipot

**Role:** ecosystem registry, integration contracts, and operator-facing control plane.

## Transfer into the control plane

Represent each repository and module as a declared boundary with explicit owned interfaces, permissions, dependencies, state, and evidence. Visualized isolation is metadata unless backed by an independently measured runtime control.

| CDM-1 concept | Klipot feature |
|---|---|
| Bounded domain | Repository/module node and its declared interface set |
| Boundary | Versioned contract, permissions, dependencies, and allowed data flows |
| Metric snapshot | Timestamped registry/configuration snapshot with schema version |
| Boundary stress | Dependency drift, missing contract, version mismatch, and failed health evidence |
| Conservation ledger | Count declared, observed, unknown, failed, and verified integration edges |
| Isolation | Static policy declaration plus a separately sourced runtime-evidence status |

## Required invariants

1. Every edge has a source module, target module, contract version, and direction.
2. A declared dependency is not proof that a runtime connection exists.
3. A successful metadata/schema check is not proof of hardware qualification or production readiness.
4. Unknown, missing, failed, and verified evidence must render distinctly.
5. Browser labs remain simulations; they must not imply control of real devices or collection of real telemetry.
6. Repository identity remains canonical: SAMBU, ToolNG, ReaperCripple, Kloz, CO, SaintSI, Klipot, NUN, NUNLauncher, Fragile-Baby, and Luci.

## Acceptance tests to add

- Reject duplicate module IDs, dangling edges, invalid contract versions, and cycles where the declared policy forbids them.
- Detect missing evidence separately from a failed check.
- Verify that a registry snapshot is schema-versioned and reproducible.
- Ensure every dashboard metric exposes its unit, source, timestamp, and evidence state.
- Ensure simulations carry an explicit simulation label.

## Scope

Klipot may present CDM-1 as an architecture/invariant model. It must not claim to calculate spacetime curvature or infer physical mass from repository topology.
