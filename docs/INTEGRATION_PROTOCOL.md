# SAMBU Ecosystem Integration Protocol

**Ecosystem authority:** [SAMBU](https://github.com/bboroski/SAMBU)  
**Canonical architecture:** [ECOSYSTEM_ARCHITECTURE.md](https://github.com/bboroski/SAMBU/blob/main/docs/ECOSYSTEM_ARCHITECTURE.md)  
**Canonical registry:** [ecosystem/registry.json](https://github.com/bboroski/SAMBU/blob/main/ecosystem/registry.json)  
**Manifest schema:** [ecosystem/module.schema.json](https://github.com/bboroski/SAMBU/blob/main/ecosystem/module.schema.json)

SAMBU is the umbrella engineering platform for seven independently buildable repositories. Each project owns its implementation, API, tests, release cadence and safety boundary. Klipot is the discovery and operator-facing control plane; it is not a runtime dependency of embedded firmware.

## Responsibility graph

| Project | Owns | Consumes | Must not silently do |
|---|---|---|---|
| **SAMBU** | Language, engineering tooling, architecture models, policy/workflow descriptions, canonical module registry | Versioned module manifests, adapter descriptors and evidence reports | Treat a workflow description as proof that an external action ran |
| **Kloz** | Fixed-width status ABI, caller-owned memory and versioned platform operations | Board/CPU port | Guess MMIO ordering, allocate hidden heap memory or claim untested target support |
| **CO** | Deterministic component lifecycle, bounded polling and partial-init cleanup | Application callbacks; optional Kloz services through caller context | Spawn threads, schedule interrupts or retry faults implicitly |
| **SaintSI** | Bounded heartbeat observation and CRC-32 corruption checks | Caller-supplied monotonic ticks; optional Kloz clock and CO heartbeat bridges | Reset hardware, feed watchdogs or claim cryptographic authenticity |
| **ReaperCripple** | BSP integrations, staged bootstrap, pinout governance, calibration, fixture tests and MES events | Exact board profile, fixture evidence and optional Kloz/CO/SaintSI adapters | Invent pinouts/limits, write undocumented registers or approve its own profiles |
| **ToolNG** | Windows-side Apple connection diagnostics, local reports and evidence quality gates | Windows PnP/service signals and a native C17 policy/workflow port | Change a device silently, upload private evidence or confuse unknown with failed |
| **Klipot** | Registry projection, project navigation, contract catalog and browser workbench | Canonical SAMBU registry and public repository metadata | Become a hidden firmware dependency or report mock data as live hardware state |

## Contract layers

1. **Discovery:** each repository publishes `sambu.module.json` using the shared SAMBU module schema. The manifest records role, runtime, maturity, capabilities, optional adapters, boundaries and validation evidence.
2. **Native C interfaces:** embedded interfaces use fixed-width fields, explicit structure size/version, caller-owned buffers and documented ownership. A module must remain independently buildable unless a required dependency is explicitly declared.
3. **Policy/workflow:** SAMBU describes bounded, reviewable actions. A host adapter separately reports whether an action was available, attempted, completed or rejected.
4. **Evidence:** ToolNG and ReaperCripple reports preserve provenance, sequence, timebase, status and quality/coverage. Unknown, not checked, not found, failed and passed are distinct states.
5. **Presentation:** Klipot offers navigation and educational simulations. A browser simulation is never evidence of a real firmware run.

## Integration status

| Link | Status | Meaning |
|---|---|---|
| SAMBU → all modules | **Contract defined** | Shared manifests and ownership rules exist; this is not a universal plugin loader |
| SAMBU → ToolNG | **Existing native policy port** | Selected engineering rules are implemented in C17; no Python interpreter is embedded |
| SAMBU → Klipot | **Registry mirrored** | The portal presents a local projection of the canonical SAMBU registry |
| Kloz → CO | **Adapter-ready** | Application callbacks may use Kloz platform services without CO touching registers |
| Kloz → SaintSI | **Adapter-ready** | Optional clock bridge; tick units and rollover intervals remain integrator responsibilities |
| Kloz → ReaperCripple | **Adapter-ready** | The board-specific BSP remains authoritative for measurement and safety callbacks |
| CO → SaintSI | **Adapter-ready** | The application may refresh a heartbeat only after a successful completed poll |
| SaintSI → ReaperCripple | **Adapter-ready** | Health observations inform policy; they do not trigger a reset or actuator action |

## Compatibility rules

- Increment the manifest schema major version for incompatible field or meaning changes.
- Increment native ABI versions for incompatible C structure or callback changes.
- Append fields only when old consumers can safely ignore them and structure size is honored.
- Do not serialize native C structs by copying their memory. Define byte order, widths and canonical encoding in the transport adapter.
- Convert monotonic clock units explicitly and document wrap intervals.
- Keep optional adapters outside portable cores.
- Mark every hardware profile with exact MCU/SoC, package, board revision, schematic revision, fixture, calibration set and evidence source.
- Test adapters with host tests first, then cross-compile and validate on the target. A successful host build is not hardware qualification.

## Validation boundaries

The browser labs simulate API concepts only. Run each repository's native build and test instructions for implementation evidence. Hardware-in-the-loop checks, calibration approvals and production qualification remain separate gates. The registry describes ownership and integration state; it does not confer privileges or grant hardware access.
