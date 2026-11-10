# Uncertainty → Feature Contract

Klipot turns unresolved requirements into explicit engineering actions. It does
not guess missing facts, grant capabilities, or mutate other repositories.

## Operational rules

1. Every uncertainty has a stable ID, owning domain, precise statement, named
   feature, resolution mode, safe behavior while unknown, and acceptance checks.
2. A resolved item must cite evidence. A README assertion alone is not evidence
   of a working runtime, target port, boot image, or production integration.
3. Ambiguous providers, unknown architecture, missing toolchains, absent hardware
   measurements, and unspecified permissions block dependent operations.
4. A probe may report a fact; it may not silently change configuration.
5. Configuration and approval gates are explicit. No automatic destructive
   action, privileged operation, or external side effect is inferred.
6. Each repository owns its implementation, tests, and release evidence.

## Resolution modes

| Mode | Feature behavior |
|---|---|
| `probe` | Run a read-only capability or evidence probe |
| `explicit-config` | Require a declared value; no default is guessed |
| `human-gate` | Require an owner/operator decision |
| `fail-closed` | Block dependent operations while the fact is unknown |
| `staged-implementation` | Create a bounded implementation task and acceptance tests |
| `feature-flag` | Keep the feature disabled until target evidence exists |

## Executable interface

- `klipot.uncertainty.validate_registry(document)` validates the contract.
- `klipot.uncertainty.build_resolution_plan(document)` emits a deterministic
  plan with one next step per item.
- `schemas/uncertainty-registry.schema.json` describes the machine-readable form.
- `registry/uncertainties.json` is the initial cross-repository backlog.
- `python -m unittest discover -s tests` runs planner and contract tests.

The planner is intentionally pure: it does not execute probes, change branches,
install software, approve permissions, or claim that an implementation exists.
