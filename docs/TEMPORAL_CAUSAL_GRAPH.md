# Causal chronology graph

Klipot adds a time-aware event graph for planning and forensic review. Explicit prerequisites are validated for missing nodes, cycles and impossible timestamp order. Label/time proximity is reported only as **co-occurrence**; it never becomes a causal edge automatically.

The record format intentionally stores timezone-aware timestamps. Unknown event time must remain unknown rather than being replaced by ingestion time. The incomplete 666-event source list is not treated as a factual dataset.

Run `python -m unittest discover -s tests -v`.
