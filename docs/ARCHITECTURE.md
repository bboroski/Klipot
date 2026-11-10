# NAUN architecture

## 1. Design objective

NAUN composes heterogeneous systems without turning the central runtime into a monolith. The core owns contracts, validation, ordering, resource budgets, and execution reports. Arms own domain logic. System adapters own protocol translation at external boundaries.

| Biological reference | Software mechanism |
|---|---|
| Mantle / central nervous system | Runtime, registry, scheduler, policy |
| Arms | Independently versioned modules |
| Suckers | Input/output contracts and capability declarations |
| Distributed neurons | Per-node state, telemetry, event messages |
| Chemosensory feedback | Health checks and adapter diagnostics |
| Regeneration | Replaceable modules and restartable workers |
| Coordination | DAG workflow and deterministic fan-in |

The platform is not limited to eight modules; eight arms is the design metaphor, not an artificial capacity limit.

## 2. Execution model

A workflow consists of nodes:
- id: stable node identifier.
- arm: registered module identifier.
- needs: zero or more upstream node IDs.

Nodes without dependencies receive the original input artifacts. Nodes with dependencies receive the concatenated outputs of those dependencies. A node may emit zero, one, or many artifacts.

Before execution, the graph validator checks identifiers, duplicate nodes, duplicate or missing dependencies, self-dependencies, and cycles. Kahn's algorithm yields a deterministic topological order; ties are resolved lexicographically by node ID.

The current executor is synchronous and in-process. It executes nodes sequentially in that stable order. The graph model supports independent branches, but actual parallel scheduling is a later milestone: it requires explicit concurrency limits, cancellation propagation, memory accounting, and deterministic error aggregation.

## 3. Core contracts

### Artifact

An artifact is a byte payload plus a media type and string labels. Data is treated as immutable by convention; arms receive shared references and create new artifacts for transformed output. The core validates media types and enforces per-artifact and aggregate byte limits.

### Arm

An arm provides an ArmManifest and an execute method. The manifest declares its API version, ID, release version, description, and capabilities. A registered arm is trusted code inside the current process; the trait does not sandbox or isolate it.

### SystemAdapter

An adapter translates one NAUN artifact request into one external-system response. The AdapterArm wrapper makes it usable in a workflow. Concrete adapters should own authentication, protocol framing, retry policy, timeout policy, and mapping external errors to ArmError.

The core intentionally has no dependency on a particular database, cloud, device SDK, message broker, or MES vendor.

## 4. Failure and resource model

- Workflow validation happens before any arm is invoked.
- Unknown arm IDs are reported before that node executes.
- Arm failures include the node ID.
- A cancellation token is checked between nodes.
- Policy limits include maximum graph nodes, one artifact size, and total input plus produced bytes.
- Integer accounting uses checked addition to reject overflow.

Current limitations: an arm cannot be forcibly interrupted while its synchronous execute method is running; per-node wall-clock deadlines and OS-level memory isolation are not implemented yet.

## 5. Extension boundaries

Recommended future boundaries:
1. **Transport:** framed local IPC, Unix domain sockets, named pipes, then authenticated network transport.
2. **Plugin host:** separate processes with explicit capability grants and versioned handshake.
3. **System adapters:** database, filesystem, compiler, Git, message bus, industrial gateway, and MES.
4. **Control plane:** persisted workflow definitions, registry, lifecycle, audit log, health and metrics.
5. **Hardware plane:** board support packages, device discovery, DMA and interrupt abstractions, safe register maps.
6. **User interface:** visual graph editor, module catalog, runtime inspector, logs and deployment views.

External systems should never gain ambient access to secrets, filesystem paths, network sockets, or device memory merely because they are registered as an arm.
