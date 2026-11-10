# Reaper-Domain Integration — Klipot

**Role:** ecosystem catalogue, contract graph, and operator portal  
**Canonical catalogue:** [SAMBU — 50 curated engineering patterns](https://github.com/bboroski/SAMBU/blob/main/data/reaper/engineering_patterns_50.tsv)

## Catalogue semantics

Klipot may expose the five Reaper-inspired subject areas as searchable documentation tags:

1. biosynthetic transformation and cybernetics;
2. mass-effect physics as fictional simulation vocabulary;
3. infrastructure, protection, and fault containment;
4. cycles, evolution, and dependency risk;
5. synthetic intelligence and distributed consensus.

These tags are metadata only. They are not capability identifiers, permission grants, runtime plugins, or evidence that a component implements the named concept.

## Contract and graph rules

- Keep stable IDs, version constraints, provenance, licenses, and artifact digests separate from display terminology.
- Use the existing deterministic DAG planner for dependency closure; reject cycles, unknown references, and ambiguous providers.
- A catalogue record cannot grant filesystem, network, device, or execution permissions.
- Browser labs remain simulations and must not imply access to firmware, fixtures, or real telemetry.

## Acceptance

The portal may provide filters, glossary search, and cross-links to project integration notes. Any future ingestion pipeline must validate the schema and source provenance before publishing a record. Keep project ownership, independent releases, and safety authority with each repository.
