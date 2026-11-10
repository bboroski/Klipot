# Reaper Domain Transfer Profile — Klipot

**Status:** cross-repository catalog and contract projection  
**Role:** ontology index, capability mapping and evidence-aware portal presentation

## Objective

Klipot becomes the discovery layer for a 500-entry bilingual Reaper terminology reference without turning the ecosystem into a Reaper-themed monolith. SAMBU owns the reusable term record schema; Klipot owns the cross-repository mapping that explains where an engineering analogue belongs and where it does not.

The initial registry projection is `registry/reaper-domain.json`.

## Catalog structure

The source taxonomy has five domains:

1. Reaper biology, harvesting and cybernetics.
2. Element Zero and mass-effect physics.
3. Reaper weapons, defense and infrastructure.
4. Lore, history, philosophy and cycles.
5. Synthetic biology, AI and related concepts.

Every entry must distinguish a canonical name, established in-universe mechanic, descriptive extension, speculative fiction or neutral engineering analogy. Search and filters should expose this classification; they must not collapse all 500 labels into “official lore”.

## Repository mapping

| Repository | Valid mapping |
|---|---|
| SAMBU | bilingual vocabulary, typed ontology, provenance and deterministic import/export |
| ToolNG | read-only signal evidence, source coverage, anomaly and report integrity |
| ReaperCripple | manufacturing genealogy, process stages, calibration and MES provenance |
| Kloz | fixed-width capability/resource contracts and explicit units |
| CO | bounded lifecycle phases and rollback semantics |
| SaintSI | health observations, timebase, sequence and accidental-corruption checks |
| NUN | capability identity, permissions, isolation and composition |
| NUNLauncher | image metadata, ABI/memory-map checks and boot handoff evidence |
| Klipot | catalog, compatibility matrix, status projection and navigation |

## Portal behavior

A useful catalog view should support category, English/Russian search, lore classification, related-term navigation, project mapping and evidence/maturity state. It must display whether an item is a lore label, analogy, implemented contract, planned specification or simulation. Filters must not imply that a planned capability exists.

## Interoperability rules

- Stable term IDs are language-independent.
- The SAMBU schema is the source contract; this file is a projection, not a competing schema.
- Project mappings are versioned and reviewed by the owning repository.
- Browser-lab values are illustrative simulations, never live hardware evidence.
- Unknown, not found, failed and passed remain distinct.
- Repository status is based on linked evidence and must not be inferred from terminology coverage.

The registry is intentionally a transfer map, not a claim that all 500 source entries have already been imported or that any fictional Reaper technology exists in the software.
