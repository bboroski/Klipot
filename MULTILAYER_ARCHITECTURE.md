# Multi-Axis Layer Architecture

**Architecture:** NUN Mesh — Multi-Axis Layer Fabric (MALF)  
**Repository:** `bboroski/Klipot`  
**Role:** Static web portal, ecosystem registry and integration control plane  
**Maturity:** HTML/CSS/JavaScript portal and local browser simulations; not a device runtime or autonomous deployment control plane.  
**Status:** Target boundary contract; source and test evidence determine implementation status.

## Purpose

MALF adds depth without entangling concerns. It defines structural layers, vertical product slices, trust boundaries, lifecycle stages and an independent assurance/observability plane. It does not require source files to be moved into matching directories.

## Structural layers

| ID | Layer | Responsibility |
|---|---|---|
| L0 | **Experience** | User or operator surface. |
| L1 | **Interface contracts** | Versioned APIs, schemas, event formats and public data types. |
| L2 | **Application orchestration** | Use cases, sequencing and workflow composition. |
| L3 | **Domain kernel** | Deterministic domain models, algorithms and invariants. |
| L4 | **Policy and capabilities** | Authorization, guardrails, bounds and allowed operations. |
| L5 | **Ports and contracts** | Abstract clocks, storage, sources, external APIs and platform services. |
| L6 | **Adapters and platform** | Concrete browser, OS, hardware and external-service implementations. |
| L7 | **State and data** | Registries, persisted settings, events, artifacts and provenance. |
| L8 | **Runtime and delivery** | Build, packaging, browser/runtime composition and deployment. |
| L9 | **Assurance and evidence** | Tests, schemas, coverage, observability and verification records. |

## Dependency direction

- L0 presents L2 use cases through L1; it contains no policy or domain rules.
- L2 coordinates L3 and L4 through L5 contracts.
- L6 implements L5; L3 never imports a concrete browser/OS/device/vendor adapter.
- L7 is accessed through explicit, versioned storage or registry ports.
- L8 composes and delivers the system; it depends inward.
- L9 tests observable behavior and boundary properties, not just happy paths.

**Allowed:** surface → application → domain/policy → port → adapter.  
**Forbidden:** domain → UI/OS/browser adapter; implicit global state; unversioned cross-repository runtime coupling.

## Multi-axis model

1. **Structural axis:** L0–L9.
2. **Vertical-slice axis:** end-to-end features cross only the layers needed for the capability.
3. **Trust axis:** external/untrusted input → parse → validate → policy gate → authorized effect → auditable result.
4. **Lifecycle axis:** design → configure → build → verify → package → publish/deploy → operate → recover → retire.
5. **Observability axis:** every meaningful result has provenance and confidence; telemetry is bounded and privacy-aware.

## Repository layer allocation

### L0 — Portal experience
Searchable project catalog, filters, navigation, diagrams and browser-lab screens.

### L1 — Registry and web contracts
Versioned module manifests, registry schemas, integration protocol and browser-lab API shapes.

### L2 — Portal orchestration
Load local catalog, normalize records, filter projects, build dependency views and route operator navigation.

### L3 — Ecosystem metadata domain
Repository identity, module roles, provided/consumed contracts, optionality, maturity and integration edges.

### L4 — Integration governance
Validate evidence and compatibility before representing a connection as implemented; distinguish reference, adapter-ready and verified.

### L5 — Registry/metadata ports
Explicit loaders and schema interfaces for manifests, registry snapshots and public repository metadata.

### L6 — Browser and source adapters
Static fetch/browser adapters and local simulation adapters. No arbitrary native-code or device execution.

### L7 — Registry and view state
Canonical local registry, module manifests, design tokens, filters and optional non-authoritative UI state.

### L8 — Static portal delivery
Static hosting, browser compatibility, asset loading and Pages workflow.

### L9 — Portal and contract assurance
Schema validation, duplicate/edge checks, link checks, browser-lab tests and static asset validation.

## Vertical slices

1. **Repository discovery:** Registry input → schema validation → metadata domain → searchable catalog → detail/navigation link.
2. **Dependency visualization:** Versioned provides/consumes → contract compatibility policy → graph model → portal visualization with confidence labels.
3. **Browser simulation:** Synthetic input → local model → validation → visible result clearly labeled as simulation, never live hardware telemetry.

## Cross-cutting planes

- **Security/trust:** validate external data, least privilege, explicit user intent and default-deny for unknown effects.
- **Resilience:** bounded queues, explicit fault/degraded results, controlled retries and recoverability.
- **Compatibility:** version APIs, events, manifests and stored data; reject unsupported versions visibly.
- **Observability:** structured, redacted, attributable events with limited retention.
- **Accessibility:** keyboard navigation, focus, contrast and reduced motion for operator surfaces.
- **Performance:** measure real browser/runtime behavior and avoid speculative optimization.

## NUN Mesh federation

Klipot/Luci catalogue and coordinate contracts; they do not become runtime authorities for independent modules. Cross-repository links require provider, consumer, contract version, optionality, trust boundary, failure behavior and verification evidence. A registry card or link does not prove that a runtime integration executed.

## Incremental implementation

1. Map existing files/APIs into the layers.
2. Identify circular imports, direct side effects, hidden state and unvalidated inputs.
3. Stabilize public L1 schemas and L5 ports.
4. Keep deterministic L3 rules independent of UI and external adapters.
5. Evaluate effects at L4, implement them at L6 and persist state at L7.
6. Make L8 packaging/deployment reproducible.
7. Add L9 contract, privacy, error-path and compatibility tests.
8. Refactor one vertical slice at a time.

## Definition of done

Every component has a clear owner; dependencies point inward; contracts are versioned; policy and failure cases are tested; telemetry is honest and bounded; and maturity labels match evidence.

## Repository guardrails

The portal is not an autonomous GitHub controller, plugin loader, firmware runtime or hardware telemetry source. Browser labs use synthetic/local models. The canonical registry source and its mirrors must be distinguished; a visual edge is not proof of a live integration.
