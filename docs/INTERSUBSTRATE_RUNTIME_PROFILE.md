# Inter-substrate runtime profile — Klipot

**Contract:** [SAMBU runtime API v1](https://github.com/bboroski/SAMBU/blob/feat/substrate-runtime-contract-v1/docs/INTERSUBSTRATE_RUNTIME_API_V1.md)  
**Status:** repository-specific integration profile; not a blanket implementation claim.

## Ownership
Static HTML/JavaScript ecosystem portal and registry projection.

## Existing evidence
Repository catalog/search, machine-readable registry, versioned integration documentation, browser labs with synthetic data and CI checks for registry/contracts/assets.

## Integration slice
Add read-only views for envelope schemas, resource descriptors, feature maturity, evidence links and adapter compatibility. Treat each repository as an independently versioned node record, not a process to orchestrate. Show transport, auth, encryption, latency, queue and target-validation status separately. Add schema validation and stale-registry warnings; preserve source provenance and last-verified timestamps.

## Explicit non-goals
The static portal is not a message broker, database cluster, microservice orchestrator, secrets store, authentication provider or live hardware monitor. Browser-lab values remain synthetic unless an explicit, verified data adapter is added.

## Acceptance tests
Test registry schema and duplicate module IDs; reject unknown schema versions; verify source URL/provenance; test accessible status labels and stale/unknown states; ensure browser labs do not claim live operations.

## Capability maturity
- Existing features retain their current maturity and evidence.
- The central envelope, descriptor validator, JSON codec, and bounded local queue are a SAMBU host reference, not a distributed runtime service.
- This profile does not authorize hardware changes, network egress, process execution, or access to another repository.
