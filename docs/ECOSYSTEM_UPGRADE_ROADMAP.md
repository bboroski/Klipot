# Cross-repository upgrade roadmap

**Revision:** 2026-11-11  
**Scope:** the eleven repositories in the connected workspace  
**Naming rule:** repository names and their public technical identities are canonical and must not be renamed.

This document consolidates the current cross-project engineering direction. It is a coordination contract and delivery plan, not a statement that every roadmap item is already implemented.

## Product direction

Build a coherent, modular engineering ecosystem with a shared black/graphite and yellow visual language, explicit project boundaries, testable interfaces, reproducible builds, verifiable platform claims and useful user-facing documentation.

The product ambition may be tracked as a large capability catalogue (including future CAP-xxxxx entries), but a target of 10,000 capabilities is not a count of implemented features. Each capability must have an owner, status, contract, test and evidence link before it is marketed as available.

## Canonical repository responsibilities

| Repository | Primary responsibility | Boundary and next proof |
|---|---|---|
| **SAMBU** | Shared ecosystem methods, language/domain tooling, desktop utilities and integration patterns | Keep creative/domain capabilities separate from native device diagnostics; attach provenance and tests to every generated assessment |
| **ToolNG** | Local Windows-side device/backup diagnostics with a portable C17 core and Win32 presentation | Preserve local-first and read-only defaults; distinguish observed, not found, unknown and failed evidence |
| **ReaperCripple** | Runtime substrate, board support and hardware-specific lifecycle/boot integration | Qualify each BSP by board revision, compiler, linker, emulator or hardware evidence; do not infer hardware support from host builds |
| **Kloz** | Portable low-level primitives, resource budgets, platform callbacks and architecture detection | Keep allocation and platform boundaries deterministic; validate ABI, ELF machine, compiler and target flags separately |
| **CO** | Bounded component lifecycle and polling state machine | Keep lifecycle transitions explicit, re-entrancy-safe and independently testable |
| **SaintSI** | Health, heartbeat and integrity observation | Report status; never promote a heartbeat or CRC into proof of functional/electrical safety or an automatic reset authority |
| **Klipot** | Public portal, ecosystem registry, manifests and integration planning | Render only evidence-backed capability states; keep interactive browser labs clearly distinct from native execution |
| **NUN** | Minimal kernel/runtime integration substrate | Grow boot, memory, privilege, interrupt and process contracts independently; host runtime tests do not prove a bootable OS |
| **NUNLauncher** | Kernel-image validation and future firmware-to-kernel handoff | Keep the image validator separate from a finished bootloader; architecture handoff and bootable images require emulator and target proof |
| **Fragile-Baby** | Elbrus/E2K toolchain, ABI and platform qualification workstream | Publish a target matrix with compiler/linker versions, ABI and memory-map evidence; no E2K support claim without native target results |
| **Luci** | Local catalog, manifest, registry and capability-policy inspection | Preserve default-deny, local-first operation and bounded inputs; a manifest declaration never grants permission by itself |

## Shared system contracts

### 1. Duck Black / Yellow UI

Use graphite surfaces as the structural base and yellow as the primary action, focus, selection and progress accent. Preserve each repository's identity and product-specific accent only as a semantic secondary signal. Avoid broad yellow panels and status that depends on color alone.

The shared stylesheet and tokens are the implementation source of truth:
- `assets/duck-ui/duck-ui.css`
- `design/duck-ui.tokens.json`
- `design/DUCK_UI_SYSTEM.md`

Optional material surfaces:
- **Glass:** translucent layered surfaces and backdrop blur, with an opaque fallback. CSS blur is not physical refraction; GPU refraction must be implemented and budgeted separately.
- **Metal:** restrained directional highlights. Static rendering is the safe default; motion must respect reduced-motion settings.
- **Paper:** notes, annotations and document previews; any day/night tint must be an explicit user preference.

All material treatments require contrast, keyboard focus, reduced-motion and no-filter fallback verification. Do not present SVG previews as screenshots of running applications.

### 2. Documentation and language policy

Every repository maintains:
- `README.md` — Ukrainian;
- `README.en.md` — English;
- `README.ru.md` — Russian.

Keep each README at or below 10,000 characters, retain language navigation and use the exact canonical repository name. Describe implemented, experimental, specified, hardware-dependent and unavailable capabilities separately. Marketing copy must lead with the actual user benefit, then show the proof and limitations; never invent compatibility, benchmarks, customer adoption or deployment status.

End user-facing README editions with a short wish of love, community or care, localized naturally.

### 3. Evidence and capability maturity

Use these states consistently:

| State | Meaning |
|---|---|
| `implemented` | Code exists, tests pass and a reproducible usage path is documented |
| `experimental` | A working implementation exists but coverage or compatibility is limited |
| `specified` | Contract/design exists; operational implementation is incomplete |
| `hardware_dependent` | Depends on a target toolchain, emulator, board or physical device |
| `unavailable` | No implementation or verified integration exists |

Unknown is not absent. A failed check is not healthy. A passing host build is not target qualification. CRC is not a signature. A static browser lab is not native execution. Keep screenshots, benchmark data and release claims tied to a dated, reproducible environment.

### 4. Resource, autonomy and privacy boundaries

Every queue, event ring, cache, retry loop and background task needs a hard limit, timeout, cancellation path, overflow behavior and retention rule. Default to local-first processing. Network access, sensors, clipboard integration, file mutation and external actions require an explicit, revocable capability. Destructive, security-sensitive and external actions require human confirmation.

Use versioned event envelopes with stable source names, monotonically increasing sequence numbers, bounded payloads and no credentials or raw sensitive data. Preserve source content and show diffs before transformation.

## CPU and platform qualification

Architecture family detection is only one input to target qualification. Record architecture, ABI, endianness, pointer width, ELF machine, compiler, linker, sysroot, runtime libraries, target board and test environment separately.

| Family | Qualification path |
|---|---|
| Intel / AMD x86 and x86-64 | GCC/Clang/MSVC build lanes as relevant; vendor-specific extensions require a separate feature probe |
| ARM32 / AArch64 | Explicit ABI and target triples; Apple Silicon is an AArch64 ISA target but macOS/Linux platform support is distinct |
| RISC-V 32 / 64 | Record ISA extensions, ABI and toolchain flags; do not infer from the base architecture macro |
| Elbrus E2K | LCC compiler, linker/sysroot and native E2K runner or emulator; retain a manual native qualification gate until runner availability is reliable |

A workflow file that targets a self-hosted E2K runner is only prepared infrastructure. It is not a successful test result.

## NUN, NUNLauncher and Windows executable compatibility

Keep three separate layers:

1. **NUNLauncher** validates the NUN kernel image and prepares a future boot handoff.
2. **NUN** owns kernel/runtime, memory, privilege, scheduling, process and device contracts.
3. A future **user-space Windows PE compatibility subsystem** may provide PE32/PE32+ inspection, a native loader, a documented Win32/Win64 API surface, process isolation and graphics/audio/input adapters.

Windows `.exe` games cannot be launched merely by validating a kernel image. Native x86/x64 execution, AArch64 compatibility and translation on RISC-V/E2K are different engineering paths. No translation/JIT or broad game compatibility should be claimed until it exists and is tested per title.

## Delivery sequence and release gates

### Stage A — shared foundation
- Keep UI tokens, material styles, language navigation and canonical names consistent.
- Run the documentation/UI quality workflow on every push and pull request.
- Ensure every README is under 10,000 characters.
- Review privacy, accessibility, reduced-motion and default-deny behavior.

### Stage B — portable engineering
- Build host cores with GCC and Clang where relevant.
- Run unit tests, sanitizers, static analysis and malformed-input tests.
- Validate versioned interfaces and cross-module compatibility.
- Publish per-target compiler/ABI matrices.

### Stage C — hardware and boot qualification
- Build with native E2K/LCC only on a verified runner.
- Test the boot-image format, linker map, memory map and architecture handoff in emulators.
- Qualify each supported board/CPU combination separately.
- Keep failed or unavailable target checks visible in release notes.

### Stage D — user-facing platform capabilities
- Implement NUN's boot and process foundations before advertising an operating system.
- Implement PE metadata inspection before allowing executable loading.
- Add isolation and a minimal application ABI before launching Windows programs.
- Add graphics/audio/input bridges and a per-title compatibility suite before advertising game support.

### Stage E — release and growth
- Provide a release checklist, changelog, known limitations, support matrix and rollback plan.
- Measure startup, memory, throughput and latency on a fixed workload before claiming improvements.
- Maintain a public capability registry with an owner, status, test and evidence link.
- Keep the portal, onboarding, product copy and release material synchronized with verified capability states.

## Repository acceptance checklist

- [ ] Repository identity and public interfaces remain unchanged.
- [ ] Ukrainian, English and Russian READMEs exist and each is no longer than 10,000 characters.
- [ ] Duck tokens, CSS and design documentation agree.
- [ ] Material surfaces have opaque fallbacks and accessible interaction states.
- [ ] CI checks the relevant build, tests, docs and manifest/schema contracts.
- [ ] Platform claims include compiler/ABI/target evidence.
- [ ] Security-sensitive actions are default-deny and explicitly authorized.
- [ ] Logs, queues, caches and retries are bounded.
- [ ] Marketing claims match the implementation maturity table.
- [ ] Release notes record what changed, what passed and what remains unverified.

**The goal is one coherent engineering ecosystem: measurable, maintainable, accessible and built with care.**
