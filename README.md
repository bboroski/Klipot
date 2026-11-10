# Klipot

**Klipot is the NUN ecosystem integration control plane.** It discovers declared components, verifies dependency and capability contracts, and produces a deterministic integration plan across independently maintained repositories.

Klipot does not absorb the business logic, firmware, operating-system integration, or release lifecycle of the projects it coordinates.

## Ecosystem

| Project | Responsibility | Contract boundary |
|---|---|---|
| [Kloz](https://github.com/bboroski/Kloz) | C11 machine-near substrate | Platform ABI, fixed memory and resource budgets |
| [CO](https://github.com/bboroski/CO) | Deterministic lifecycle control | Init / step / shutdown state machine |
| [SaintSI](https://github.com/bboroski/SaintSI) | Runtime health and integrity | Heartbeats, degraded-state reporting, CRC |
| [ReaperCripple](https://github.com/bboroski/ReaperCripple) | Embedded manufacturing and lifecycle engineering | BSP, board profiles, fixtures, calibration and MES |
| [SAMBU](https://github.com/bboroski/SAMBU) | Language, DSL and policy authoring | Declarative workflow and versioned policy artifacts |
| [ToolNG](https://github.com/bboroski/ToolNG) | Local Windows diagnostics | Evidence-driven, privacy-preserving workflows |

## What works in 0.1

- Loads a JSON ecosystem manifest using the Python standard library.
- Validates component IDs, dependency references and duplicate declarations.
- Detects dependency cycles.
- Resolves required capabilities only from declared dependency ancestors; unrelated providers are not silently accepted.
- Rejects ambiguous providers.
- Produces a deterministic dependency-first plan with stable ordering.
- Exposes the planner as a Python API and CLI.

The current release is a **manifest validator and planner**, not yet a deployment engine, plugin executor, process sandbox, distributed consensus system, or hardware controller. A declared adapter is not hardware-qualified until its own tests and board evidence exist.

## Quick start

Requires Python 3.10+.

```bash
python -m pip install -e .
klipot validate manifests/nun-ecosystem.json
klipot plan manifests/nun-ecosystem.json
klipot plan manifests/nun-ecosystem.json --json
python -m unittest discover -s tests -v
```

Without installation:

```bash
python -m klipot.cli validate manifests/nun-ecosystem.json
```

## Architecture

```text
Manifest → validation → dependency/capability resolution → cycle detection → stable plan
```

See [Architecture](docs/ARCHITECTURE.md), [Archetype Engineering Map](docs/ARCHETYPE_ENGINEERING_MAP.md), and [Contract Rules](docs/CONTRACTS.md).

Versioned schemas:
- [Ecosystem manifest](schemas/ecosystem-manifest.schema.json)
- [Component declaration](schemas/component.schema.json)
- [Capability manifest](schemas/capability-manifest.schema.json)
- [Resource profile](schemas/resource-profile.schema.json)
- [Event envelope](schemas/event-envelope.schema.json)

## Safety and trust

- A manifest is data, never executable code.
- A capability declaration is a claim to validate, not proof that a physical device supports it.
- Missing required capabilities block the plan.
- Resource limits are ceilings, not targets. Emergency operation never removes them.
- Untrusted extensions must not be loaded into the control-plane process.
- Telemetry consistency does not authorize safety-critical actions. Flashing, power control, destructive tests and reset decisions require authoritative local policy.

## Status

The NUN ecosystem contract set is versioned independently from component releases. The planner validates the core dependency and capability graph. Full JSON Schema validation, signed manifests, persistent event storage, worker execution, distributed discovery and sandbox enforcement remain future work.

**Klipot — connect capabilities, not codebases.**
