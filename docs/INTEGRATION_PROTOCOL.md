# SAMBU Ecosystem Integration Protocol

**Ecosystem authority:** [SAMBU](https://github.com/bboroski/SAMBU)  
**Canonical architecture:** [ECOSYSTEM_ARCHITECTURE.md](https://github.com/bboroski/SAMBU/blob/main/docs/ECOSYSTEM_ARCHITECTURE.md)  
**Canonical registry:** [ecosystem/registry.json](https://github.com/bboroski/SAMBU/blob/main/ecosystem/registry.json)  
**Manifest schema:** [ecosystem/module.schema.json](https://github.com/bboroski/SAMBU/blob/main/ecosystem/module.schema.json)

SAMBU is the umbrella engineering platform for nine coordinated repositories: seven implemented engineering projects and two specification-only system projects (NUN and NUNLauncher). Each project owns its implementation or specification, API, tests, release cadence and safety boundary. Klipot is the discovery and operator-facing control plane; it is not a runtime dependency of embedded firmware.

## Responsibility graph

| Project | Owns | Consumes | Must not silently do |
|---|---|---|---|
| **SAMBU** | Language, engineering tooling, architecture models, policy/workflow descriptions, canonical module registry | Versioned module manifests, adapter descriptors and evidence reports | Treat a workflow description as proof that an external action ran |
| **Kloz** | Fixed-width status ABI, caller-owned memory and versioned platform operations | Board/CPU port | Guess MMIO ordering, allocate hidden heap memory or claim untested target support |
| **CO** | Deterministic component lifecycle, bounded polling and partial-init cleanup | Application callbacks; optional Kloz services through caller context | Spawn threads, schedule interrupts or retry faults implicitly |
| **SaintSI** | Bounded heartbeat observation and CRC-32 corruption checks | Caller-supplied monotonic ticks; optional Kloz clock and CO heartbeat bridges | Reset hardware, feed watchdogs or claim cryptographic authenticity |
| **ReaperCripple** | BSP integrations, staged bootstrap, pinout governance, calibration, fixture tests and MES events | Exact board profile, fixture evidence and optional Kloz/CO/SaintSI adapters | Invent pinouts/limits, write undocumented registers or approve its own profiles |
| **ToolNG** | Windows-side Apple connection diagnostics, local reports and evidence quality gates | Windows PnP/service signals and a native C17 policy/workflow port | Change a device silently, upload private evidence or confuse unknown with failed |
| **Klipot** | Registry projection, project navigation, contract catalog and browser workbench | Canonical SAMBU registry and public repository metadata | Become a hidden firmware dependency or report mock data as live hardware state |\n| **NUN** | Minimal kernel architecture, boot handoff, memory and execution contracts | Versioned boot-information block and architecture-specific loader handoff | Claim a bootable OS, target support or runtime integration before implementation and evidence exist |\n| **NUNLauncher** | Kernel image validation and controlled boot-information handoff contract | NUN image contract and platform memory-map evidence | Flash automatically, bypass image validation or replace the kernel recovery path |

## Contract layers

1. **Discovery:** each repository publishes `sambu.module.json` using the shared SAMBU module schema. The manifest records role, runtime, maturity, capabilities, optional adapters, boundaries and validation evidence.
2. **Native C interfaces:** embedded interfaces use fixed-width fields, explicit structure size/version, caller-owned buffers and documented ownership. A module must remain independently buildable unless a required dependency is explicitly declared.
3. **Policy/workflow:** SAMBU describes bounded, reviewable actions. A host adapter separately reports whether an action was available, attempted, completed or rejected.
4. **Evidence:** ToolNG and ReaperCripple reports preserve provenance, sequence, timebase, status and quality/coverage. Unknown, not checked, not found, failed and passed are distinct states.
5. **Presentation:** Klipot offers navigation and educational simulations. A browser simulation is never evidence of a real firmware run.
6. **Multilingual signal metadata:** the canonical SAMBU Text Signal Contract v1 separates Unicode script profiles, caller-supplied language hints, representation kinds, translation state, and human semantic review. The envelope is metadata-only and does not carry raw or translated text. See [contract specification](https://github.com/bboroski/SAMBU/blob/main/docs/MULTILINGUAL_SIGNAL_PIPELINE.md) and [JSON Schema](https://github.com/bboroski/SAMBU/blob/main/schemas/text-signal-envelope.schema.json).\n7. **System boot and kernel layers:** NUNLauncher validates the image and produces a versioned handoff; NUN owns the kernel contract and must revalidate that handoff. Both repositories currently publish specifications only.\n8. **Update and recovery:** Dependabot proposes dependency and GitHub Actions updates as pull requests. Repository CI is the compatibility gate; automatic merge and automatic installation remain disabled.

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


## Layered autonomy and composition

The ecosystem is connected, not fused. Each repository owns its source tree, build, tests, configuration, release and rollback. The shared registry describes relationships; it does not make every module a mandatory dependency.

- **System entry:** NUNLauncher defines image validation and the boot-information handoff.
- **Kernel core:** NUN defines architecture entry, memory, execution, protection and device boundaries.
- **Platform substrate:** Kloz provides fixed-capacity memory and versioned platform operations.
- **Runtime services:** CO owns deterministic component lifecycle; optional integration is passed through caller-owned context.
- **Assurance:** SaintSI observes heartbeat progress and accidental corruption. It does not actuate or reset hardware.
- **Manufacturing:** ReaperCripple owns board-specific BSP, calibration, fixtures and production evidence.
- **Engineering tooling:** SAMBU owns the language, developer tooling, models and canonical registry.
- **Desktop diagnostics:** ToolNG owns Windows-side evidence collection and local diagnostic reports.
- **Control plane:** Klipot projects metadata, contracts and navigation without entering any firmware or kernel runtime.

Optional adapters must be versioned, declared in module manifests, and testable in isolation. A consumer must report an unavailable or incompatible optional adapter without corrupting its independent core. No cyclic required dependency is permitted. Compatibility is reported separately from local build status.

## Software update and rollback policy

1. Dependabot checks GitHub Actions weekly in every repository and Python package dependencies in SAMBU.
2. Updates are delivered as pull requests. Repository CI must pass before an update can be accepted; auto-merge and automatic installation are disabled.
3. Application releases are distributed through versioned GitHub Releases when artifacts are published. A release consumer must verify repository provenance, artifact integrity/signature, supported platform and contract compatibility before installation.
4. Desktop application updates require explicit operator approval and retain a previous known-good version for rollback.
5. Kernel, bootloader and firmware updates additionally require a target-specific recovery path and explicit approval. No unattended flashing or boot-chain replacement is allowed.
6. Failed, unavailable and unknown checks remain distinct. A missing test result is not a pass.

The two system repositories are specification-only today. Their manifests and update policy are machine-readable architecture contracts, not evidence of a working kernel, bootloader or in-app updater.
