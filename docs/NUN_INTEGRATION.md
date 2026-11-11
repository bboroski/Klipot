# NUN integration — federation registry and control portal

## Assigned responsibility

Klipot is the ecosystem registry and integration-control portal. Its NUN role is to display repository ownership, contract versions, dependency edges and evidence status. It is not the kernel debugger, native IDE or LSP server.

## Current verified state

- The repository provides a static HTML/JavaScript portal and machine-readable registries.
- Browser labs use local/synthetic models; they do not execute native C or inspect hardware.
- The portal can represent maturity and integration metadata, but the presence of a registry entry is not proof of a working component.

## Integration contract

1. Treat each NUN subsystem as an independently versioned repository/module with an explicit owner.
2. Display implementation status separately from design status, CI status and target qualification.
3. Link evidence to exact commits, workflow runs and test artifacts; do not infer readiness from a README badge alone.
4. Validate JSON schema and reject unknown or incompatible ABI versions rather than guessing.
5. Never execute participant repository code from the portal.
6. Keep future editor/LSP/debugger adapters separate from the static registry until native protocol implementations exist.

## Dependency order

Klipot may track the [NUN](https://github.com/bboroski/NUN) Phase A workflow immediately, but must display QEMU boot as pending until a successful run is linked. Higher layers should not be marked ready while lower boot/memory/interrupt gates remain open.

## ABI status

This change adds documentation only; no Klipot portal API or NUN kernel ABI is changed. Record any later NUN-facing contract change in `CHANGELOG.NUN`.
