# Security model

## Current trust boundary

The current runtime executes registered Arm implementations in-process. A Rust trait is an extension point, not a security sandbox. Only register code that is trusted by the application operator.

## Required rules for adapters and future plugins

- Do not embed access tokens, passwords, private keys, or production credentials in manifests or source.
- Keep secrets in an external secret provider and pass short-lived scoped credentials only to the adapter that needs them.
- Validate all external lengths, encodings, identifiers, and protocol states.
- Use TLS with peer verification for remote transports.
- Set connection, request, and execution deadlines.
- Treat device input, files, network responses, and MES payloads as untrusted.
- Never expose raw MMIO or unrestricted filesystem/network access to a general-purpose workflow arm.
- Use an out-of-process plugin host before executing third-party modules.
- Log security-relevant actions without logging secret values or full sensitive payloads.
- Pin and review dependencies; generate an SBOM before production packaging.

## Hardware warning

MMIO calls are unsafe by design. A wrong address or access width can hang, corrupt, or damage a device or system. Use board vendor documentation and verified memory maps. The generic kernel crate does not discover hardware or validate a caller-supplied physical address.

## Reporting

Do not publish credentials or exploit details in an issue. Report security concerns privately to the repository maintainer using GitHub's supported private vulnerability reporting workflow.
