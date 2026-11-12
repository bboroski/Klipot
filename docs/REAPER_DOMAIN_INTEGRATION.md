# Engineering Pattern Integration — Klipot

**Role:** ecosystem catalogue, contract graph and operator portal  
**Reference catalogue:** [SAMBU — 50 engineering patterns](https://github.com/bboroski/SAMBU/blob/main/data/reaper/engineering_patterns_50.tsv)

## Catalogue taxonomy

Klipot may expose five searchable technical domains:

1. data pipelines and controlled state transformation;
2. physical modeling and parameter provenance;
3. infrastructure resilience and fault containment;
4. lifecycle governance and dependency risk;
5. distributed intelligence and integrity verification.

These labels are metadata only. They are not capability identifiers, permission grants, runtime plugins or evidence that a component implements a named function.

## Contract and graph rules

- Keep stable IDs, version constraints, provenance, licenses and artifact digests separate from display terminology.
- Use the existing deterministic DAG planner for dependency closure; reject cycles, unknown references and ambiguous providers.
- A catalogue record cannot grant filesystem, network, device or execution permissions.
- Browser labs remain simulations and must not imply access to firmware, fixtures or live telemetry.

## Acceptance

The portal may provide filters, glossary search and cross-links to integration notes. Any ingestion pipeline must validate schema and source provenance before publishing. Project ownership, independent releases and safety authority remain with each repository.
