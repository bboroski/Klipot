# Klipot control-plane architecture

## Purpose

Klipot coordinates independent systems through declared dependencies, capability contracts and resource profiles. It does not replace their local runtimes or own hardware-specific policy.

## Control path

1. **Discover** — load a versioned manifest from an explicitly trusted source.
2. **Validate** — verify schema version, identifiers, dependency references and duplicate declarations.
3. **Resolve** — ensure every required capability is provided by an explicit dependency or one of its ancestors.
4. **Plan** — reject cycles and emit a stable dependency-first order.
5. **Admit** — a future executor checks resource profiles before admitting work; limits are never silently widened.
6. **Dispatch** — a future adapter invokes a component through its declared contract.
7. **Observe** — components publish bounded events using the versioned event envelope.
8. **Recover** — the component's own supervisor applies an explicit local policy; Klipot records orchestration state but does not improvise hardware actions.

The 0.1 implementation covers steps 2–4. The remaining stages are contracts and architecture, not implemented behavior.

## Ownership boundaries

| Component | Owns | Must not take over |
|---|---|---|
| Klipot | Manifest validation, dependency graph, capability resolution, integration plan | Component internals, device registers, credentials, arbitrary code execution |
| Kloz | Freestanding C ABI, memory primitives, resource counters, platform contracts | Component lifecycle and fault policy |
| CO | Deterministic lifecycle transitions and one bounded caller-driven step | RTOS scheduling, threads, hardware register access |
| SaintSI | Heartbeat and integrity observations | Reset authority, watchdog servicing, safety certification |
| ReaperCripple | BSP profiles, board bring-up, fixtures, calibration and MES | Unreviewed electrical limits or vendor-unsafe register changes |
| SAMBU | Language, declarative policy and workflow authoring | Privileged host execution or claiming OS-level isolation |
| ToolNG | Local Windows device diagnostics and evidence reports | iOS repair, backup payload inspection, hidden remote control |

## Dependency rules

- The graph is directed and acyclic.
- A component may consume only capabilities provided by its declared dependency closure.
- A capability with multiple providers in the same dependency closure is ambiguous and blocks planning until an explicit adapter selects one provider.
- Repository relationships do not imply source-level linking. Adapters translate APIs and map result codes explicitly.
- Contracts use independent semantic versions. A breaking contract change is a new major schema version.
- Manifest declarations do not prove that target hardware, firmware or external services were qualified.

## Runtime state model

A future executor may use:

`DISCOVERED → VALIDATED → ADMITTED → ACTIVE → DEGRADED → STOPPED`

Invalid declarations are `REJECTED`; unavailable dependencies are `BLOCKED`; untrusted extensions are `QUARANTINED`. State transitions must be auditable and idempotent. The current CLI emits a plan only and does not execute these states.

## Failure containment

- Missing required capability: reject the affected component before side effects.
- Missing optional capability: allow only under an explicit degraded profile.
- Resource ceiling reached: reject new work, apply the declared queue policy, and preserve reserved recovery capacity.
- Dependency failure: block dependent work; a stale heartbeat is not proof of recovery.
- Manifest cycle or ambiguous provider: reject the complete plan.
- Event delivery loss: increment a loss counter; never convert missing telemetry into a healthy result.

## Trust boundary

A manifest is data, not code. The planner never imports a module named by a manifest, loads a DLL, starts a process, opens a device, or downloads a plugin. A future extension host must isolate untrusted code in an OS process, container or WASM runtime with explicit capabilities, resource quotas and a watchdog. That enforcement is not part of Klipot 0.1.

Hardware safety interlocks and production approval remain local to ReaperCripple's validated board/fixture policy. No distributed event or eventual-consistency result may authorize power, firmware, reset or destructive test actions.
