# Beelzebub — security profile for Klipot

**Federation status:** registered member of Hellduck
**Policy version:** 0.1.0
**Security status:** SPECIFIED — this file declares a target profile; it does not claim that scanners, enforcement, or endpoint protection are already enabled.

Canonical policy: https://github.com/bboroski/Hellduck/blob/main/ecosystem/beelzebub.policy.json
Architecture: https://github.com/bboroski/Hellduck/blob/main/docs/BEELZEBUB_SECURITY_ARCHITECTURE.md

## Repository role
Static HTML/JavaScript portal, contract catalog, and device-local opt-in preferences.

## Protected scope
The profile protects browser-delivered code and its dependencies. It does not introduce a server-side execution plane or transfer private device-local data to the federation hub.

## Target checks
- JavaScript static analysis and dependency audit
- Browser security review, safe DOM handling, and CSP review
- No remote personalization or unapproved telemetry
- Static asset and release-integrity checks

## Response boundaries
- Unknown code and malware samples must not execute on a developer workstation or production host.
- Dynamic analysis, when added, must use an ephemeral isolated environment with no production secrets and deny-by-default network egress.
- Automatic actions are limited to findings, CI failure, and isolation of test artifacts.
- Deletion, credential revocation, permission changes, Git-history rewriting, endpoint process control, and driver deployment require separate operator authorization.
- No PID spoofing, IDT/SSDT/IRP patching, arbitrary EIP/RIP rewriting, false-success API spoofing, or unbounded resource traps.

## Evidence contract
Record repository name, commit SHA, workflow run, check version, finding category, confidence, severity, and an evidence link. Never copy secret values or private device data into central reports.

## Implementation status
This profile is a specification and review contract. Mark a control implemented only after code/configuration, a successful CI run, and target-specific evidence exist. A repository profile alone is not an antivirus deployment.
