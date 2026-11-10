# AI-Generated Ecosystem Metadata Policy

**Scope:** Klipot registry, capability manifests, schemas and static portal.  
**Status:** governance policy; the portal remains a static control plane.

## Trust boundary

Gemini and other models may draft registry entries, capability descriptions, integration diagrams and documentation. Generated metadata is untrusted until validated against the versioned schema, checked against the canonical repository and reviewed by a maintainer.

A model-generated entry is not proof that a repository exists, a feature is implemented, a workflow passed or a deployment is live.

## Required admission checks

1. Validate JSON against the versioned schema and reject unknown properties where the schema requires strictness.
2. Resolve every canonical repository name and URL; preserve case-sensitive project IDs such as SAMBU, ToolNG, ReaperCripple, Kloz, CO, SaintSI, Klipot, NUN and NUNLauncher.
3. Compare provides, consumes, ABI and maturity claims with actual source files, tests and release evidence.
4. Keep planned, documented, host-tested, hardware-tested and deployed states separate.
5. Validate all local image/document references and run the existing mesh-contract checks.
6. Review the final diff before updating the public registry.

## Evidence model

The portal may display curated repository metadata and linked CI pages. It must not label a cached description or browser-lab simulation as a live device measurement or current CI result. If evidence is missing or stale, show that limitation instead of filling the gap with model-generated text.

## Provenance

For material changes, retain a short review record in the pull request: source repository/ref, schema version, authoring tool if relevant, reviewer and verification commands. Do not commit private prompts, access tokens or personal data.

## Publication rule

No generated content may autonomously publish to the default branch or change GitHub permissions, Pages settings, secrets or workflow trust. A maintainer reviews and merges the change; the existing CI remains the acceptance gate.
