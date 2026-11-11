# Beelzebub Nexus — Fleet Federation and Integrity Stage

**Status:** design contract / implementation gate. This document does not claim that a live P2P network, central service, AST engine, healer, or signing pipeline is deployed.

## 1. Goals and non-goals

This stage connects repository-local Beelzebub agents under one auditable control plane while keeping source code and secrets inside their owning repositories. The Nexus coordinates identity, policy, threat intelligence, evidence, and signed release metadata. It is not a remote shell, code-exfiltration service, or autonomous production operator.

**Initial fleet scope:** the 13 repositories owned by `bboroski`: SAMBU, ToolNG, ReaperCripple, Kloz, CO, SaintSI, Klipot, NUN, NUNLauncher, Fragile-Baby, Luci, Hellduck, and 9circ. Klipot is the policy/control-plane reference repository. Discovery must still reconcile this allowlist against the live GitHub installation before onboarding anything.

## 2. Topology: Central Nexus + P2P Gossip

- **Nexus (Klipot):** canonical policy, repository registry, trust roots, schema versions, revocations, quorum policy, audit index, and signed threat-feed checkpoints.
- **Repository tentacle:** a small local agent/CI adapter. It scans locally, emits minimized evidence, verifies feed signatures, and applies only repository-scoped policy.
- **Gossip peers:** exchange signed, bounded threat envelopes and Merkle checkpoints. Peers never exchange source trees, secrets, raw environment variables, or unrestricted filesystem contents.
- **Transport:** start with HTTPS GitHub artifacts/releases or a pinned relay. Add libp2p only after identity, NAT, abuse controls, and operational monitoring are proven. Gossip is an optimization; Nexus-signed checkpoints remain authoritative.
- **Partition behavior:** agents cache the last valid policy/feed, mark data stale after its TTL, and fail closed for release signing when required trust metadata is stale. No peer can silently rewrite global policy.

### Message envelope

Every exchanged record must carry:
- `schema_version`, `event_id`, `issuer_repo_id`, `issuer_key_id`, `created_at`, `expires_at`;
- `event_type`, `severity`, `confidence`, `taxonomy`, `indicator_hashes`;
- `evidence_digest`, `provenance`, `policy_version`, `signature`.

Reject unknown critical schema versions, expired events, oversized payloads, replayed IDs, invalid signatures, revoked issuers, and records exceeding rate/size limits. Deduplicate by event ID and canonical content hash. Use deterministic serialization before signing.

## 3. Central Nexus responsibilities

1. Maintain an inventory of repository ID, canonical name, default branch, visibility, archived status, languages, owner, adapter version, last-seen time, and trust state.
2. Publish versioned, signed policy bundles and threat-feed checkpoints.
3. Record enrollment, key rotation, revocation, policy changes, appeals, and remediation outcomes in append-only audit events.
4. Enforce repository-scoped authorization: a repo agent may publish only for its own identity and read only approved fleet intelligence.
5. Expose health and staleness state; do not infer that an agent is healthy merely because a repository exists.

Nexus must not store repository contents, credentials, private keys, raw secret values, or unredacted scanner output.

## 4. Automatic repository discovery and enrollment

- Enumerate repositories visible to the installed GitHub App using read-only repository metadata permissions.
- Reconcile discovered repositories against the explicit owner allowlist and exclusions (archived, forks, disabled, or unsupported repositories).
- New repositories enter **QUARANTINED / PENDING ENROLLMENT**; discovery alone never grants trust or write permissions.
- Inspect default branch, languages, existing workflows, CODEOWNERS, security policy, and repository visibility before generating an adapter.
- Open a draft PR containing the adapter and manifest. Require owner review and successful CI before activation.
- Reconcile periodically; detect rename, transfer, archive, deletion, visibility changes, default-branch changes, and installation permission loss.
- Use stable GitHub repository IDs as identity; names are display metadata and may change.

## 5. Cross-repository Threat Memory

Threat Memory stores normalized intelligence, not copied malware or source code.

Record classes:
- **Indicator:** cryptographic hashes, package coordinates, domains/IPs only when legally and operationally appropriate, rule IDs, and AST/behavior fingerprints.
- **Observation:** repo ID, scanner version, timestamp, evidence digest, confidence, and disposition.
- **Verdict:** provisional / corroborated / rejected / revoked, with rationale and signer.
- **Remediation:** advisory, patch reference, verification result, and rollback reference.

Trust rules:
- A single peer report is provisional.
- Promotion to fleet-wide blocking requires independent corroboration or a signed maintainer decision under a documented quorum policy.
- Every verdict has provenance, expiry, revocation support, and an appeal path.
- False positives are retractable; downstream consumers receive revocation events.
- Share hashes and minimal metadata by default. Never upload source snippets, credentials, user data, or proprietary payloads to global memory.

## 6. AST and behavioral analysis

Use a language-plugin interface with explicit capability declarations. Start with parsers for languages actually detected in the fleet; do not claim universal parsing.

Static AST checks should identify risky constructs and suspicious combinations (dynamic execution, unsafe deserialization, shell/process creation, dynamic imports/loading, insecure crypto, path traversal, permission changes, and network-to-execution flows). A finding must include rule ID, file path, line/column, AST node category, confidence, and a redacted evidence digest.

Behavioral analysis runs only in disposable, resource-limited CI sandboxes:
- no host mounts, production credentials, privileged containers, or unrestricted network;
- CPU, memory, process count, wall-clock, and output limits;
- deterministic fixtures and explicit egress allowlists;
- record syscalls/process/network/file behavior as structured events;
- never execute untrusted code on the Nexus host or developer workstation.

AST/behavior results are signals for triage, not proof of malicious intent. No destructive action follows from one heuristic.

## 7. Auto-Healer: propose, verify, never silently mutate

The healer is a constrained remediation planner:
1. Map a finding to an approved, versioned fix recipe.
2. Generate a patch on a dedicated branch.
3. Run formatting, unit tests, security regression tests, dependency checks, and the relevant build.
4. Attach before/after evidence and a rollback commit reference.
5. Open a draft PR with a clear risk explanation and exact diff.
6. Require maintainer approval and normal branch protections before merge.

Forbidden: deleting files automatically, changing production state, force-pushing, disabling security controls, rotating credentials without an approved incident procedure, or merging its own patch. If validation fails, discard the candidate branch and preserve the evidence.

## 8. Artifact and commit signing

- Sign release artifacts and provenance attestations with Sigstore/cosign keyless OIDC where supported; use short-lived workload identity, not long-lived private keys in repository secrets.
- Bind each attestation to repository ID, commit SHA, workflow identity, builder identity, build inputs, dependency lock state, and artifact digest.
- Verify signature, certificate identity, issuer, transparency-log inclusion, repository/branch/workflow claims, and digest before publish/deploy.
- Protect release workflows with least-privilege permissions and pinned third-party actions.
- Never sign untrusted pull-request builds with release identity.
- Keep unsigned development artifacts clearly marked; production release gates require verified provenance.

## 9. Security invariants

- Least privilege; read-only by default.
- No source-code or secret exfiltration through gossip.
- Signed policy and threat records; explicit key rotation and revocation.
- Idempotent, bounded, replay-resistant message handling.
- Human approval for remediation merge and policy escalation.
- Local fail-safe behavior during Nexus outage; no fail-open release signing.
- Privacy-aware retention and redaction.
- Every automated decision is explainable, attributable, and reversible.

## 10. Rollout gates and acceptance tests

**Gate A — Contracts:** schemas, threat taxonomy, identity model, policy versioning, and test vectors are reviewed.

**Gate B — Read-only federation:** two test repositories exchange signed synthetic events; replay, tampering, expiry, revocation, oversized payload, and partition tests pass.

**Gate C — Discovery:** a newly created test repository is detected and remains pending until explicit enrollment; rename/archive/transfer are reconciled correctly.

**Gate D — Analysis:** AST fixtures cover true/false positives; sandbox tests prove network, CPU, memory, and process limits.

**Gate E — Healer:** only a draft PR is produced; invalid fixes cannot merge; rollback is demonstrated.

**Gate F — Supply chain:** artifact signature and provenance verify for an approved build; altered artifact, wrong workflow identity, and unsigned release are rejected.

No gate is considered passed from documentation alone. Each requires executable tests and retained CI evidence.
