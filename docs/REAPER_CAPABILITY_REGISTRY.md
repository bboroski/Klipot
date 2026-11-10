# Klipot — Reaper cycle capability registration

## Registry identity

Register the ReaperCripple synthesis model as a versioned, optional simulation capability. Do not register it as a processor backend, hardware controller, bootloader, biological processor, or trusted executable merely because its scenario vocabulary uses those terms.

Suggested capability identity:

- ID: reapercripple.synthetic-cycle
- ABI family: c11.fixed-width.v1
- Inputs: non-zero 64-bit seed and 1–6666 iteration budget
- Outputs: phase trace, completed count, deterministic state digest, verification flag
- Side effects: none outside caller-owned output and checkpoint callback
- Trust state: quarantined until artifact provenance, schema, and tests pass

## Admission policy

Use Klipot's existing manifest and dependency contracts. Validate schema and digest before planning; reject cycles and ambiguous providers; stage in an isolated namespace; publish a new registry snapshot atomically; preserve the previous snapshot for rollback.

Never let a simulation report claim hardware support or bypass the explicit permissions of its consumer.

## Interoperability

The implementation and normative phase contract are maintained in ReaperCripple. Klipot is the catalog and integration control plane, not the runtime that executes the C model.
