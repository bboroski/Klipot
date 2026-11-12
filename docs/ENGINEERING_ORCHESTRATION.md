# Klipot engineering orchestration

Klipot is the control plane for the repository family, not a shared runtime. Its job is to reconcile identity, contracts, release maturity and verification evidence across independently built projects.

## Multi-stage control loop

1. **Inventory:** load canonical repository IDs and maturity records.
2. **Schema validation:** parse registry, ecosystem manifests and capability contracts.
3. **Dependency planning:** reject unknown dependencies, cycles and missing capability providers.
4. **Compatibility check:** compare ABI/schema versions and explicit adapter contracts.
5. **Build/test evidence:** gather repository CI results; never infer a pass from a manifest.
6. **State reconciliation:** preserve PASS, FAIL, UNKNOWN, NOT_APPLICABLE and NOT_RUN separately.
7. **Release gate:** promote only modules whose required evidence is present.
8. **Presentation:** render project cards, progress animations and operator summaries from the reconciled snapshot.

## Monolith without shared mutable state

The ecosystem is monolithic at the operator/orchestration level and modular at the code/runtime level. Each repository owns its implementation, tests and release. Cross-project calls use versioned contracts; no hidden global state or direct memory sharing is assumed.

## Compaction and markers

Portal summaries may compact verbose event histories into bounded snapshots, but must retain a digest, source repository, commit/ref, schema version and capture time. A summary is not a substitute for the raw CI artifact or hardware measurement.

## Inventory states

Nine currently registered modules retain their existing maturity. Fragile-Baby and Luci are added to the repository inventory as incubating placeholders with no published capabilities and no integration eligibility until their product boundaries are defined.

## Verification

`python tests/validate_mesh.py` verifies registry membership, active manifests, local diagrams and portal controls. The CI workflow also compiles the shared C header smoke test and checks portal JavaScript syntax.
