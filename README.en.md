<p align="center"><img src="assets/duck-ui/duck-mark.svg" alt="Klipot mark" width="92"></p>
<h1 align="center">Klipot</h1>
<p align="center"><strong>Ecosystem Integration &amp; Control Plane</strong></p>
<p align="center"><img src="https://img.shields.io/badge/STATUS-STATIC%20PORTAL-FFD600?style=for-the-badge&labelColor=111111"><img src="https://img.shields.io/badge/CORE-HTML%20%2B%20JS-FFD600?style=for-the-badge&labelColor=111111"><img src="https://img.shields.io/badge/LICENSE-NOT%20DECLARED-FFD600?style=for-the-badge&labelColor=111111"></p>
<p align="center"><a href="README.md">🇺🇦 Українська</a> · <a href="README.en.md">🇬🇧 English</a> · <a href="README.ru.md">🇷🇺 Русский</a></p>
<p align="center"><sub><a href="design/DUCK_UI_SYSTEM.md">Duck Black / Yellow UI standard</a> · <a href="assets/duck-ui/duck-ui-preview.svg">Vector UI preview</a></sub></p>

---

**Klipot is the central catalog and control plane for the engineering ecosystem.** It maps modules, ownership boundaries, integration contracts, and documentation entry points without merging independent runtimes into one monolith.

## Portal capabilities

- Module catalog with domain filters and search.
- Links to source code, GUI documentation, and run instructions.
- Clone-command copy actions.
- Machine-readable registry and versioned integration protocol.
- Browser labs demonstrating allocation, lifecycle, heartbeat, and capability-gate models.
- CI checks for metadata, contracts, schemas, and static portal syntax.

**Simulation boundary:** browser labs do not execute C code, read hardware telemetry, control fixtures, or prove physical device state.

## Ecosystem map

| Repository | Role | Current status |
|---|---|---|
| [SAMBU](https://github.com/bboroski/SAMBU) | Language, IDE, modeling, and workflows | Experimental alpha |
| [ToolNG](https://github.com/bboroski/ToolNG) | Local Windows diagnostics | Windows desktop utility |
| [ReaperCripple](https://github.com/bboroski/ReaperCripple) | Embedded bring-up and manufacturing lifecycle | Host-tested; target qualification separate |
| [Kloz](https://github.com/bboroski/Kloz) | Bare-metal C11 substrate and platform ABI | Host-tested core |
| [CO](https://github.com/bboroski/CO) | Component lifecycle runtime | Host-tested core |
| [SaintSI](https://github.com/bboroski/SaintSI) | Heartbeat observer and CRC | Host-tested core |
| [Klipot](https://github.com/bboroski/Klipot) | Catalog and control plane | Static portal |
| [NUN](https://github.com/bboroski/NUN) | Minimal OS kernel specification | Specification only |
| [NUNLauncher](https://github.com/bboroski/NUNLauncher) | Bootstrap and handoff specification | Specification only |
| [Fragile-Baby](https://github.com/bboroski/Fragile-Baby) | Elbrus/E2K architecture workstream | Proposal; target evidence pending |
| [Luci](https://github.com/bboroski/Luci) | Documentation scaffold for design tokens and integration boundaries | Scope pending |

## NUN Mesh

<p align="center"><img src="assets/nun-mesh-overview.svg" alt="NUN Mesh — seven connected engineering repositories coordinated through versioned contracts" width="100%"></p>

**NUN Mesh** is the seven-repository contract core: Kloz, CO, SaintSI, ReaperCripple, SAMBU, ToolNG, and Klipot. Four additional catalog tracks — NUN, NUNLauncher, Fragile-Baby, and Luci — retain distinct maturity boundaries: specifications, architecture proposals, or documentation scaffolds. They are not represented as verified runtimes or hardware support.

Each component retains ownership of its code and lifecycle. Integrations use versioned contracts, explicit adapters, and verifiable evidence.

## Run locally

Open <code>index.html</code> or start a local server:

~~~bash
python -m http.server 8080
~~~

Then visit <code>http://localhost:8080</code>. No external framework or JavaScript package is required.

## Publishing and checks

Workflow: <code>.github/workflows/pages.yml</code>. For GitHub Pages, select **Settings → Pages → GitHub Actions**.

~~~bash
python one.py
python one.py check
~~~

Checks cover the portal, manifests, schemas, and JavaScript; they do not validate every external repository.

## Ecosystem governance

1. **Domain ownership:** each module owns its code, API, tests, and release.
2. **Explicit links:** integrations use versioned contracts.
3. **Evidence before status:** passed, observed, not found, unknown, and failed remain distinct.
4. **Bounded execution:** capacity, ownership, timeout, and cleanup are explicit.
5. **Honest maturity:** host tests do not replace emulator or hardware qualification.

Documentation: [Integration Protocol](docs/INTEGRATION_PROTOCOL.md) · [Ecosystem Registry](registry/ecosystem.json) · [Portal UI](docs/PORTAL_UI.md).

## License

No <code>LICENSE</code> file is present; no license is declared. Define the terms before public distribution.

---

**Built with love for systems thinking, engineering, and people.**