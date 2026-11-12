# Contributing to Klipot

Klipot owns semantic planning, graph construction, manifest validation, and cross-project integration contracts. Keep plans deterministic and preserve explicit provenance for generated results.

## Required workflow

1. Open or link an Issue and identify affected schema, manifest, planner, graph, or integration boundary.
2. Use a focused branch: `feat/<topic>`, `fix/<topic>`, `docs/<topic>`, or `security/<topic>`.
3. Keep schema changes backward-compatible or provide a versioned migration.
4. Do not turn an inferred dependency into an asserted fact; preserve uncertainty/provenance fields.
5. Never commit tokens, private source data, generated reports, or local build output.

## Required validation

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
klipot validate manifests/nun-ecosystem.json
klipot plan manifests/nun-ecosystem.json --json
```

## Commits and releases

Use Conventional Commit subjects (`feat:`, `fix:`, `docs:`, `refactor:`, `perf:`, `test:`, `build:`, `ci:`, `chore:`). Breaking changes require `!:` and a `BREAKING CHANGE:` footer. Use SemVer and update changelog plus schema migration notes before tagging.

## Pull request checklist

- Describe manifest/schema compatibility and affected consumers.
- Include deterministic test output or regression tests.
- Explain provenance and uncertainty handling.
- Document rollout and rollback for contract changes.
