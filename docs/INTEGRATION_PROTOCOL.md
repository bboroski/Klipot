# NUN Mesh integration protocol

NUN Mesh links seven repositories without turning them into one monolith. Each project owns its domain, tests, release cadence and safety boundary. Klipot is the discovery/control plane; it is not a runtime dependency of embedded firmware.

## Responsibility graph

| Project | Owns | Consumes | Must not silently do |
|---|---|---|---|
| **Kloz** | Stable low-level ABI, caller-owned memory and platform callbacks | Board/CPU port | Guess MMIO ordering, allocate hidden heap memory or claim target support |
| **CO** | Deterministic component lifecycle | Application callbacks; optional Kloz platform services | Spawn threads, schedule interrupts or retry faults implicitly |
| **SaintSI** | Bounded health observation and CRC-32 | Caller-supplied monotonic ticks; optional Kloz clock adapter | Reset hardware, feed watchdogs or claim cryptographic authenticity |
| **ReaperCripple** | BSP integration, staged bootstrap, calibration, fixture tests and MES events | Kloz platform services, CO lifecycle policy and SaintSI observations through explicit adapters | Invent pinouts/limits, write undocumented registers or approve its own profiles |
| **SAMBU** | Language, developer tooling, deterministic workflows and policy descriptions | Versioned schemas and external project adapters | Treat a workflow description as proof that an external action ran |
| **ToolNG** | Windows-side Apple connection evidence and local UX | Its embedded portable SAMBU policy/workflow core; optionally exports evidence summaries | Change a device silently, upload private evidence or confuse unknown with failed |
| **Klipot** | Registry, shared contracts, portal, integration map and project navigation | Versioned manifests and repository metadata | Become a hidden firmware dependency or report mock data as live hardware state |

## Contract layers

1. **Discovery:** each project publishes an ecosystem manifest with a stable project ID, contract version, provided capabilities, consumed capabilities, maturity and evidence links.
2. **C ABI:** embedded interfaces use fixed-width fields, explicit structure size/version, caller-owned buffers and documented ownership. The header at contracts/mesh-envelope.h defines a neutral envelope reference.
3. **Policy/workflow:** SAMBU workflow files describe bounded, reviewable actions. A host adapter must separately report whether an action was available, attempted, completed or rejected.
4. **Evidence:** ToolNG and ReaperCripple reports keep provenance, sequence, timebase, status and quality/coverage. Unknown, not checked, not found, failed and passed are distinct states.
5. **Presentation:** Klipot offers navigation and educational sandboxes. A browser simulation is never evidence of a real firmware run.

## Integration status

| Link | Status | Meaning |
|---|---|---|
| Kloz → CO | **Contract-ready** | CO remains standalone; callback owners can use Kloz platform services without CO reaching into registers |
| Kloz → SaintSI | **Adapter-ready** | Tick bridge is optional; tick units and wrap interval remain integrator responsibilities |
| Kloz → ReaperCripple | **Adapter-ready** | Reaper BSP remains authoritative for board-specific measurement and safety callbacks |
| CO → SaintSI | **Adapter-ready** | A host can report CO state/heartbeats to SaintSI; observation does not trigger a reset |
| SaintSI → ReaperCripple | **Adapter-ready** | Reaper runtime health can be observed through an explicit bridge; policy stays with the application |
| SAMBU → ToolNG | **Existing integration** | ToolNG contains a portable policy/workflow core; it does not embed the Python interpreter or creative-text modules |
| All projects → Klipot | **Registry/documentation** | Registry and portal describe capabilities; they do not claim one binary or a shared runtime |

## Compatibility rules

- Increment a contract major version for incompatible layout or semantics changes.
- Append fields only when old consumers can safely ignore them and struct_size is honored.
- Do not serialize native C structs by copying their memory. Define byte order, widths and canonical encoding in the transport adapter.
- Do not assume monotonic clock frequencies match between projects. Convert units explicitly and bound wrap intervals.
- Keep optional adapters outside portable cores so each repository remains independently buildable.
- Mark every hardware profile with exact MCU/SoC, package, board revision, schematic revision, fixture and evidence source.
- Test adapters with host tests first, then cross-compile and validate on the target. A successful host build is not hardware qualification.

## Local validation

The portal's browser labs are simulations of API concepts only. Run each repository's native build/test instructions for implementation evidence. Hardware-in-the-loop checks, calibration approvals and production qualification remain separate gates.
