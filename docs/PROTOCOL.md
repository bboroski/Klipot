# KLP1 bundle protocol

## Purpose

KLP1 is the first stable binary container used to combine multiple artifacts into one reversible output. It is intentionally small and architecture-neutral.

All integers are unsigned little-endian values. There is no implicit alignment or padding.

## Layout

| Offset | Size | Field |
|---:|---:|---|
| 0 | 4 | Magic bytes KLP1 |
| 4 | 4 | Artifact count (u32) |
| repeated | 4 | Media type byte length (u32) |
| repeated | 8 | Payload byte length (u64) |
| repeated | variable | Media type bytes (UTF-8) |
| repeated | variable | Raw payload bytes |

Artifact labels are runtime metadata and are not serialized in KLP1 version 1. A future format revision must add an explicit versioned extension area rather than silently changing this layout.

## Decoder requirements

A conforming decoder must:
- verify the magic;
- reject more than 65,536 entries;
- reject truncated headers and payloads;
- reject invalid UTF-8 media types;
- use checked length arithmetic;
- reject trailing bytes.

The current implementation meets those requirements. The runtime's execution policy separately limits total bytes before a bundle can be emitted.

## Compatibility

The media type emitted by the merge arm is application/vnd.klipot.bundle; version=1. Implementations should treat unknown media types as opaque bytes. KLP1 does not provide encryption, authentication, compression, checksums, or canonical signatures.
