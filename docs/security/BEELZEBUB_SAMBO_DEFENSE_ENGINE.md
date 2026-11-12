# BEELZEBUB — SAMBO Defense Engine

**Status:** architecture specification; implementation is capability-gated and not yet a claim of deployed endpoint protection.  
**Owner/control plane:** `bboroski/Klipot`  
**Policy version:** 1.0.0  
**Scope:** the `bboroski` repository fleet and explicitly enrolled endpoints.

## 1. Mission

Beelzebub is a behavior-first defensive system inspired by sambo principles: observe an adversary's momentum, preserve evidence, redirect harmful actions into controlled sinks, isolate the actor, and recover trusted state. The metaphor describes defensive orchestration; it does not authorize destructive counterattacks, resource exhaustion, kernel patching, or interference with unrelated processes.

**Primary invariant:** protect host availability, user data, and evidence before attempting remediation. Unknown activity is observed and contained proportionately; it is never automatically treated as malicious solely because it is unfamiliar.

## 2. System topology

- **Fleet Control Plane (Klipot):** signed policy distribution, repository/endpoint inventory, enrollment, capability registry, fleet telemetry aggregation, rollout rings, revocation, and audit.
- **Repository adapters:** small, versioned policy and CI integrations in each repository. They do not contain privileged endpoint code.
- **Endpoint sensor:** least-privilege user-mode collectors for process, file, registry/configuration, module, and network events.
- **Decision engine:** deterministic rules plus explainable heuristic scoring; optional ML is advisory and version-pinned.
- **Containment broker:** applies reversible OS-native controls through documented interfaces.
- **Analysis sandbox:** disposable, network-restricted execution with synthetic services and no access to production secrets.
- **Evidence vault:** immutable event timeline, hashes, metadata, and access-controlled memory captures where legally and technically permitted.
- **Recovery engine:** snapshots/journals and verified restoration of protected files and configuration.

Control plane outage must not disable local protection. Endpoints keep the last valid signed policy and fail safely.

## 3. Six sambo disciplines translated into defensive controls

### I. Off-balancing and momentum capture — rules 1–12

1. **Foreign impulse:** rate-limit and queue hostile ingress at controlled boundaries; never feed attacker data back to exhaust an attacker buffer.
2. **Executing sweep:** use a disposable sandbox identity and synthetic privilege boundary; never fabricate a live PID or impersonate a privileged process.
3. **Uniform grab:** validate executable identity using canonical path, signer, hash, image metadata, and process lineage; a familiar process name is not proof.
4. **Thread twist:** collect execution and call-stack telemetry through supported instrumentation; verify module and code integrity before policy decisions.
5. **Sticky hook:** use documented file/registry/network filters with bounded queues and timeouts; avoid unbounded hooks or artificial deadlocks.
6. **Support-leg removal:** quarantine the suspect module and prevent new loads; do not unload arbitrary dependencies from a running process.
7. **Re-grab:** a tampering attempt triggers evidence preservation and protected-service recovery, not an unsafe in-process memory dump by default.
8. **Energy drop:** use guard pages, isolated test allocations, and exploit mitigations in a sandbox; never create an infinite overflow.
9. **Sandbox drag:** detonate unknown files only in disposable, network-restricted environments with explicit resource ceilings.
10. **CPU throttling:** apply bounded job-object/cgroup quotas to confirmed or high-confidence suspicious workloads; never starve the host scheduler.
11. **Capture decoy:** use synthetic decoy credentials/data and isolated honeypot services; never poison real packet streams or third-party systems.
12. **Vector reversal:** expose controlled honeypot SMB/RDP-like services only in an isolated network segment; no lateral movement or unsolicited scanning.

### II. Throws from standing — rules 13–24

13. **Runtime throw:** terminate or suspend a contained process through documented OS APIs; do not rewrite live instruction pointers as a generic response.
14. **Filesystem trip:** redirect sandbox writes to copy-on-write storage; protect originals with snapshots and transactional recovery.
15. **Socket sweep:** block or sinkhole confirmed malicious destinations at the endpoint/network policy layer; preserve DNS and connection evidence.
16. **Microarchitectural defense:** rely on vendor/OS mitigations and configuration checks for Spectre-class issues; do not zero CPU registers.
17. **Interrupt wheel:** detect unexpected kernel integrity changes and invoke supported recovery/reboot workflows; never modify or loop the IDT.
18. **Parent-child takedown:** correlate process trees and suspend/quarantine the whole malicious lineage as a unit using supported interfaces.
19. **Spin-lock trap:** detect pathological loops and sandbox evasion through time-budgeted analysis; do not create permanent scheduler loops.
20. **Registry overthrow:** monitor persistence locations and deny/quarantine unauthorized changes through supported policy/filter interfaces.
21. **Guest elevation counter:** run untrusted content with restricted tokens, AppContainer/sandboxing, or equivalent least-privilege controls.
22. **Hollowing neutralization:** detect image/section mismatches and suspicious remote writes; suspend, capture evidence, and restart from a trusted image when safe.
23. **API redirection:** prefer policy enforcement and explicit denial over deceptive success responses; compatibility shims must be scoped to the sandbox.
24. **Hard crash termination:** stop confirmed malicious execution cleanly and record the reason; do not deliberately corrupt process state to imitate a crash.

### III. Joint locks and controlled restrictions — rules 25–36

25. **Handle armbar:** protect critical objects with ACLs and supported handle controls; do not freeze an entire handle table.
26. **Memory lock knot:** use OS memory protections, DEP, CFG, and W^X; do not mark all process memory read-only.
27. **Socket entanglement:** apply per-process network policy and protocol-aware telemetry; avoid redirecting all traffic blindly.
28. **Stack canary pressure:** use compiler stack protection, ASLR, CFG, and platform exploit mitigations; do not inject canaries into arbitrary stacks.
29. **Driver armbar:** block vulnerable/unsigned drivers using Secure Boot, HVCI/Memory Integrity, WDAC or platform equivalents; do not patch IRP dispatch tables.
30. **NTFS stream lock:** inventory and scan alternate data streams; quarantine suspicious content through supported filesystem APIs.
31. **Entry-point twist:** never rewrite a PE entry point on disk; quarantine the file and preserve a hash/evidence record.
32. **IOCTL pain:** enforce device access policy and validate driver/device telemetry; do not indiscriminately block hardware I/O.
33. **Key-lock:** detect mass encryption behavior early, suspend the process, preserve volatile evidence when authorized, and restore from protected backups. Key extraction is best-effort forensic work, never a recovery guarantee.
34. **Parent-child split:** restrict token inheritance and cross-process access with OS security descriptors and sandbox boundaries.
35. **DLL side-load lock:** enforce safe DLL search paths, signature validation, and application control; allow explicit signed application-local dependencies.
36. **Socket double-lock:** isolate the process network namespace or apply a deny policy; never loop attacker traffic into itself on a production interface.

### IV. Ground control and resource discipline — rules 37–48

37. **RAM starvation:** set safe memory ceilings for sandbox jobs and alert on allocation abuse; do not impose a 4 KiB cap on arbitrary live processes.
38. **I/O choke:** use bounded I/O quotas only for contained workloads; preserve host responsiveness and recovery access.
39. **Port blockade:** block confirmed malicious flows/destinations with scoped firewall rules; do not close every port.
40. **IPC isolation:** restrict suspicious IPC endpoints selectively and preserve required OS/service channels.
41. **VSS protection:** protect backup services and shadow-copy deletion through least privilege, tamper protection, and monitored policy.
42. **Bandwidth choking:** rate-limit isolated analysis workloads; never degrade unrelated host or fleet traffic.
43. **Clock desync:** use virtual time only inside the sandbox; never alter the host clock.
44. **Mutex control:** detect mutex-based single-instance behavior as telemetry; do not seize global mutexes.
45. **Shadow paging:** use hypervisor/sandbox snapshots and copy-on-write memory views; never substitute live physical pages with zeros.
46. **Process suspension:** suspend a contained process tree with watchdog and timeout; ensure recovery paths can resume or terminate it.
47. **Registry protection:** apply ACLs, application control, and supported registry callbacks/policies; no hardware-controller write blocking.
48. **Environment isolation:** provide a minimal sandbox environment; never delete host environment variables.

### V. Defensive self-protection — rules 49–60

49. **Counter-exploit:** use exploit mitigations, patch guidance, and safe protocol rejection; never attack the exploit author's infrastructure.
50. **ASLR boost:** require platform ASLR and randomized service layouts; do not relocate live security modules ad hoc.
51. **Decoy body:** use clearly isolated decoy processes and honeypot artifacts for detection; never hide the actual security core in arbitrary drivers.
52. **Trusted signature:** verify signed binaries, measured boot, Secure Boot, and TPM-backed attestation where supported; document trust limitations.
53. **Anti-anti-debugging:** identify debugger-evasion behavior in the sandbox; do not falsify system-wide debugger APIs.
54. **Unhooking defense:** verify critical module integrity and restore from trusted OS servicing sources; avoid blind overwrites of loaded code.
55. **C2 sinkholing:** sinkhole only confirmed malicious domains under authorized DNS/network policy; retain original indicators and audit decisions.
56. **Dual-process self-heal:** use a protected watchdog/service recovery mechanism with bounded restart backoff; never promise 1 ms recovery or create an uncontrolled respawn loop.
57. **Kernel integrity:** rely on Secure Boot, HVCI, code signing, OS integrity facilities, and vendor-supported telemetry; do not patch SSDT.
58. **Polymorphism response:** combine behavior graphs, control-flow features, provenance, and reputation; CFG similarity is evidence, not proof of identical intent.
59. **W^X enforcement:** prevent writable-and-executable memory where supported and monitor legitimate JIT exceptions with explicit allowlists.
60. **Transactional rollback:** journal protected-file/configuration changes and restore from verified snapshots; rollback must be atomic, tested, and preserve user data.

### VI. Match discipline and fleet strategy — rules 61–66

61. **Clean mat:** remove only verified temporary artifacts owned by the sandbox; retain forensic evidence according to retention policy.
62. **Referee integrity:** protect Beelzebub services with least privilege, code signing, ACLs, watchdogs, and OS security boundaries—not absolute priority over the OS or user.
63. **Zero false-positive ambition:** minimize false positives through staged response, confidence thresholds, allowlists, explainability, and human review. Zero false positives is a target, not a guarantee.
64. **Heuristic score:** score independent signals with calibrated weights, decay, provenance, and confidence. A score threshold triggers containment/review, not automatic destruction. Example: persistence attempt +3; security-control tampering +5; verified malicious payload +5; benign admin activity subtracts or suppresses correlated signals.
65. **Fleet reflex:** share signed indicators, policy versions, and privacy-minimized behavior summaries across enrolled nodes. Never distribute raw secrets or unreviewed samples fleet-wide.
66. **Continuous bout:** support atomic hot policy/model updates with signature verification, compatibility checks, rollback, and no mandatory service restart where the platform supports it.

## 4. Response state machine

`OBSERVE → SCORE → CONTAIN → COLLECT → ANALYZE → REMEDIATE → VERIFY → RELEASE`

- **Observe:** passive telemetry; no destructive action.
- **Score:** correlate independent signals and provenance.
- **Contain:** reversible network/process/file isolation, with host safety limits.
- **Collect:** timestamped evidence, hashes, event lineage, optional authorized memory capture.
- **Analyze:** sandbox and deterministic rules; ML is advisory.
- **Remediate:** quarantine, remove persistence, patch, or restore verified state.
- **Verify:** rerun integrity checks and relevant regression tests.
- **Release:** require policy criteria or operator approval; retain audit trail.

Emergency containment may occur before full analysis only for high-confidence, high-impact behavior, and must be reversible.

## 5. Risk model and non-negotiable safety limits

- No offensive counter-exploitation, worm propagation, credential theft, destructive payloads, or retaliatory traffic.
- No arbitrary Ring 0 hooks, SSDT/IDT patching, kernel structure rewriting, or unsigned driver loading.
- No deliberate CPU/RAM/disk/network exhaustion on the host.
- No fake PID or process identity on the host; synthetic identities exist only in isolated analysis.
- No automatic deletion of unknown files, user data, backups, or evidence.
- All containment is scoped, logged, reversible where possible, and bounded by resource/time ceilings.
- Kernel components, if ever required, remain minimal, signed, reviewed, platform-specific, and independently tested. Prefer user-mode and documented OS security facilities.
- Telemetry is data-minimized, encrypted in transit/at rest, access-controlled, and retention-bounded.

## 6. Implementation modules and contracts

| Module | Responsibility | Required contract |
|---|---|---|
| Sensor | process/file/registry/network events | bounded, timestamped, provenance-rich |
| Normalizer | canonical event schema | versioned, deterministic |
| Correlator | process tree and event sequences | stable entity IDs, no PID-only identity |
| Scorer | rules and confidence | explainable score + evidence references |
| Policy engine | decisions and rollout | signed policy, version, expiry, rollback |
| Containment broker | OS-native controls | least privilege, scoped, reversible |
| Sandbox | unknown-file detonation | disposable, isolated, quota-limited |
| Evidence vault | audit and forensic artifacts | integrity hashes, access log, retention |
| Recovery | rollback and repair | verified source, atomicity, restore tests |
| Fleet control | enrollment and intelligence | mutual authentication, signed updates |

## 7. Repository-fleet integration

Klipot is the canonical policy/control-plane home. Each enrolled repository carries a local adapter document and CI checks appropriate to its actual role. Repository adapters must not claim endpoint protection merely by containing this specification.

Each adapter must define:
1. owned assets and threat model;
2. relevant Beelzebub modules and unsupported capabilities;
3. data classification and telemetry boundary;
4. policy/config schema version;
5. CI checks (secret scan, dependency audit, static analysis, tests, artifact signing where applicable);
6. release/rollback owner and evidence path.

Repositories that build kernels, firmware, bootloaders, or low-level runtimes must treat Beelzebub as a build/release integrity and artifact-admission layer unless a separately qualified runtime sensor exists. Do not inject desktop endpoint-agent assumptions into bare-metal code.

## 8. Delivery stages and acceptance criteria

**Stage A — governance:** threat model, event schema, policy schema, ADRs, repo adapters, threat-to-control traceability.  
**Stage B — repository protection:** secret/dependency scanning, static analysis, signed build provenance, protected release artifacts, PR checks.  
**Stage C — user-mode prototype:** event collection, deterministic scoring, quarantine workflow, audit log, safe rollback.  
**Stage D — sandbox:** disposable execution, synthetic network services, resource quotas, test corpus.  
**Stage E — endpoint hardening:** platform-specific integrations and signed service; kernel driver only after a separate security review.  
**Stage F — fleet:** enrollment, signed policy distribution, staged rollout, revocation, privacy controls.

A stage is complete only with reproducible tests, threat-model coverage, documented limitations, and rollback evidence. A PR merged into a repository is not proof of a working antivirus.

## 9. Minimum test matrix

- Benign installer, updater, admin script, backup agent, and developer tool: no destructive false-positive response.
- Persistence attempt in a sandbox: detected, explained, and contained.
- Mass file rewrite/rename: originals remain recoverable; rollback is verified.
- Suspicious child process and injection simulation: lineage captured and process contained safely.
- DNS/HTTP beacon simulation: destination policy applied without disrupting unrelated traffic.
- Service tampering attempt: watchdog recovery is bounded and audited.
- Malformed event stream and sensor crash: host remains available; last valid policy persists.
- Invalid/expired policy signature: update rejected; prior policy remains active.
- Fleet partition: local protection continues; telemetry queues within bounded storage.

## 10. Status and claims

This document defines architecture and acceptance criteria. It does **not** assert that any endpoint sensor, sandbox, kernel driver, fleet service, or rollback engine is already implemented. Feature status must be backed by code, CI results, platform qualification, and reproducible tests.

## 11. Governance

Changes require an ADR for new privileged behavior, threat-model update, test evidence, security review, and the repository's existing CI. Preserve branch protection and required checks. Roll out first to a non-production ring, then expand only after measured stability.
