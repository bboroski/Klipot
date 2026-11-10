# Multilingual Signal Contract — Control Plane View

Klipot publishes the discovery and operator-facing view of the shared SAMBU metadata contract. The canonical implementation and schema remain in SAMBU:

- [Pipeline specification](https://github.com/bboroski/SAMBU/blob/main/docs/MULTILINGUAL_SIGNAL_PIPELINE.md)
- [JSON Schema v1](https://github.com/bboroski/SAMBU/blob/main/schemas/text-signal-envelope.schema.json)
- [Unicode script diagnostics](https://github.com/bboroski/SAMBU/blob/main/docs/text_craft.md)

## What the contract means

A signal record separates source representation, caller-supplied script/language hints, transliteration or transcription type, structural repetition, translation state, and semantic-review state. It is metadata-only: raw and translated text do not belong in the envelope.

Klipot may display:
- contract version and validation status;
- representation kinds and declared script sets;
- `not_performed`, `caller_supplied`, and `human_reviewed` state distinctions;
- repeated-section counters and provenance references;
- links to the repository that owns each processing or assurance responsibility.

## What the portal does not do

The static portal is not a production language detector, translator, semantic classifier, or embedded transport. A browser lab or preview is a UI simulation, not proof that an external model, C runtime, board, or factory fixture executed.

## Responsibility chain

| Layer | Owner |
|---|---|
| Source text retention and normalization policy | Calling application |
| Unicode script and text-structure diagnostics | SAMBU |
| Bounded host/firmware memory | Kloz |
| Deterministic stage lifecycle | CO |
| Heartbeat and accidental-corruption observation | SaintSI |
| Embedded event codes and manufacturing records | ReaperCripple |
| Local Windows diagnostic presentation and recurrence | ToolNG |
| Discovery, contract navigation, compatibility summary | Klipot |

## Compatibility rules

The schema is versioned independently of module releases. Additive optional metadata may remain within v1; changing the meaning of a required field needs a new major contract version. A missing language hint is not an error, and no consumer may manufacture a translation or a semantic label from writing-system counts alone.