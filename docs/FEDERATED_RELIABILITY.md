# Federated reliability model

Klipot is the deterministic integration planner and review-policy layer for the NUN ecosystem.

## Dependency coordination

- Manifests declare component identity, role, dependencies, provided capabilities and required capabilities.
- Stable topological planning rejects missing dependencies, cycles and ambiguous capability providers.
- Required capabilities are resolved only through the declaring component's dependency ancestry, not unrelated registry entries.

## Evidence-linked review

The `klipot consensus` command evaluates one-person-one-vote review records:

```bash
klipot consensus review.json --quorum-percent 75 --minimum-votes 2
```

Eligible reviewers are fixed before evaluating a record. Duplicate or ineligible votes are rejected. Approve/reject votes require evidence references; abstentions count toward participation but not toward the result. A tie remains pending, and insufficient participation produces `no_quorum`.

The report contains a canonical SHA-256 digest for deterministic comparison. That digest is not a signature and does not verify reviewer identity. Consensus output is review-only: it cannot merge, deploy or grant runtime permissions.

## Verification gate

Run `python -m unittest discover -s tests` and validate representative ecosystem manifests with `klipot validate`.
