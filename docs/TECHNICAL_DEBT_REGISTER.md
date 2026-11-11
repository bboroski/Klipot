# Technical Debt Register — Klipot

**Review scope:** initial review of the Duck System 3.0 pull request, changed documentation/design assets and PR-triggered GitHub Actions visible on 2026-11-11.  
**Audit status:** partial baseline; this is not a comprehensive architecture, security, dependency, performance or accessibility audit.  
**Rule:** absence of a recorded item does not mean absence of technical debt.

## Findings

| ID | Domain | Impact | Likelihood | Risk | Effort (1–5) | Owner | Target | Acceptance decision | Status | Evidence | Next action |
|---|---|---:|---:|---:|---:|---|---|---|---|---|---|
| KLIPOT-DOC-001 | Documentation / mesh contract | 2 | 4 | Moderate (8 before mitigation) | 1 | TBD (maintainer) | After sibling README PRs merge | Pending CI confirmation | mitigated — CI confirmation pending | Earlier cross-repository validation reported that the README variants lacked a local `nun-mesh*.svg` reference. This branch now includes `assets/nun-mesh-overview.svg` in all three Klipot README variants and updates the mesh validator to accept and validate token schemas 2.1.0 and 3.0.0. | Confirm the next cross-repository mesh-contract run after the sibling README diagram PRs are merged; close only when all seven checkout diagrams and token compatibility checks pass. |

## Risk method

Score impact and likelihood independently from 1 to 5; risk = impact × likelihood. Bands: 1–4 Low, 5–9 Moderate, 10–16 High, 17–25 Critical. Scores are preliminary triage, not a substitute for owner review. Re-score after mitigation and when exposure changes.

## Required record fields

Every new item must include a stable ID, subsystem, reproducible evidence, impact, likelihood, risk, remediation estimate, owner, mitigation, target milestone, acceptance decision and status. Allowed statuses: `identified`, `triaged`, `planned`, `in_progress`, `mitigated`, `resolved`, `accepted`.

Accepted debt requires a documented reason, owner, mitigation and review/expiry date. Security-critical debt cannot be accepted solely to meet a release date. Close an item only after the fix is merged and verification evidence is linked.

## Next audit

Complete the repository-wide baseline before the next major release and refresh at least quarterly. Cover architecture, security/privacy, dependencies/supply chain, testing, error handling, resource use, accessibility, documentation drift, build/release automation and public-contract compatibility. Mark unreviewed areas **not assessed**; do not populate speculative findings.
