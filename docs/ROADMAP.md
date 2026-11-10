# Roadmap

This roadmap distinguishes the implemented foundation from work that still requires design, implementation, and target hardware.

## Foundation — implemented in this change

- Rust workspace with a core runtime, CLI, and separate no_std kernel crate.
- Arm manifest and versioned API contract.
- Artifact model and external SystemAdapter boundary.
- DAG validation, stable topological scheduling, fan-in/fan-out composition.
- Cancellation checks between nodes and bounded node/artifact/byte budgets.
- Reversible KLP1 bundle encoder/decoder.
- Built-in identity, prefix, UTF-8 uppercase, merge, and FNV-1a diagnostic arms.
- CLI demo, arm catalog, and smoke-test command.
- CI for formatting, workspace tests, and compilation.

## Phase 2 — robust application runtime

- Workflow manifest format with strict schema versioning.
- Persistent module and workflow registry.
- Structured tracing, metrics, per-arm health and error taxonomy.
- Concurrency with bounded worker pools and deterministic result collection.
- Timeouts, retries, circuit breakers, idempotency keys, and dead-letter handling.
- Configurable data retention and secure secret-provider interface.

## Phase 3 — isolated integration ecosystem

- Out-of-process plugin host over local IPC.
- Handshake for ABI/API versions, capabilities, resource limits, and health.
- Capability-scoped filesystem and network access.
- Signed plugin packages, provenance, SBOM, and reproducible build metadata.
- Concrete adapters for Git, SQL, REST/gRPC, queues, filesystems, industrial gateways, and MES.

## Phase 4 — systems engineering and hardware

- Target-specific BSP crates for selected STM32, ESP32, AVR, RISC-V and x86/ARM boards.
- Generated peripheral register maps and pin-mux validation.
- Cross-compilation matrix and QEMU-based tests where appropriate.
- Hardware test fixtures, serial/USB probes, power-cycle control, and HIL result storage.
- Kernel startup, interrupt, DMA and memory-management components only where a real deployment requires them.

## Phase 5 — operator platform

- Visual DAG designer and module catalog.
- Live execution graph, logs, traces and health dashboard.
- Deployment profiles, environment promotion and rollback.
- Audit trails, policy editor, role-based access and integration approvals.

## Release gates

A phase is not considered complete because a directory or interface exists. Each production milestone needs executable tests, compatibility tests, security review, reproducible builds, and hardware evidence where physical devices are involved.
