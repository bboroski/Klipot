<p align="center"><img src="assets/duck-ui/duck-mark.svg" alt="Duck mark" width="104" /></p>
<h1 align="center">Klipot</h1>
<p align="center"><strong>Ecosystem Integration & Control Plane</strong></p>
<p align="center"><img src="https://img.shields.io/badge/STATUS-STATIC%20PORTAL-FFD600?style=for-the-badge&labelColor=111111" /><img src="https://img.shields.io/badge/CORE-HTML%20%2B%20JS-FFD600?style=for-the-badge&labelColor=111111" /><img src="https://img.shields.io/badge/LICENSE-TEXT%20MISSING-FFD600?style=for-the-badge&labelColor=111111" /></p>
<p align="center"><a href="README.md">🇺🇦 Українська</a> · <a href="README.en.md">🇬🇧 English</a> · <a href="README.ru.md">🇷🇺 Русский</a></p>
<hr />

**A single map of the engineering ecosystem: modules, contracts, documentation, and an operator portal—without forcing independent runtimes into one monolith.**

## Product position

Klipot helps teams understand how components relate, who owns each responsibility, and which integration contracts are documented. It is a catalog and control plane for transparent coordination, not a hidden monolith.

## Portal capabilities

- Module catalog with domain filters and search.
- Links to source code, GUI documentation, and run instructions.
- Copyable clone commands.
- Machine-readable registry and versioned integration protocol.
- Per-repository uncertainty registers, a deterministic workspace planner, and evidence-gated implementation states.
- Browser labs demonstrating allocation, lifecycle, heartbeat, and capability-gate concepts.
- CI checks for metadata, contracts, schemas, and static-portal syntax.

**Important:** browser labs are simulations. They do not execute C code, read live hardware telemetry, control manufacturing fixtures, or prove physical device state.

## The eleven ecosystem projects

| Repository | Role | Current maturity |
|---|---|---|
| [SAMBU](https://github.com/bboroski/SAMBU) | Language, IDE, modeling, and workflows | Experimental alpha |
| [ToolNG](https://github.com/bboroski/ToolNG) | Windows diagnostics and local evidence | Windows desktop utility |
| [ReaperCripple](https://github.com/bboroski/ReaperCripple) | Embedded BSP, calibration, and manufacturing | Host-tested; target validation required |
| [Kloz](https://github.com/bboroski/Kloz) | Portable C11 substrate and platform ABI | Host-tested core |
| [CO](https://github.com/bboroski/CO) | Deterministic component lifecycle | Host-tested core |
| [SaintSI](https://github.com/bboroski/SaintSI) | Heartbeat monitoring and CRC | Host-tested core |
| [Klipot](https://github.com/bboroski/Klipot) | Catalog, contracts, and portal | Static portal |
| [NUN](https://github.com/bboroski/NUN) | Minimal OS-kernel specification | Documentation scaffold |
| [NUNLauncher](https://github.com/bboroski/NUNLauncher) | Image and handoff metadata validation | Host contract; no CPU transfer |
| [Fragile-Baby](https://github.com/bboroski/Fragile-Baby) | Elbrus E2K toolchain/ABI/target qualification | Host qualification contract; target pending |
| [Luci](https://github.com/bboroski/Luci) | Offline repository audit and feature planning | Early Python implementation |

NUN validates boot metadata on the host but is not a bootable OS. NUNLauncher validates image and handoff structures but does not yet transfer CPU control or act as a complete bootloader. Fragile-Baby does not claim verified E2K hardware support until target evidence is supplied.

## Run locally

Open <code>index.html</code> in a modern browser or start a local server:

~~~bash
python -m http.server 8080
~~~

Then open <code>http://localhost:8080</code>. No external JavaScript framework or package is required.

## Publishing and checks

The portal uses the GitHub Pages workflow at <code>.github/workflows/pages.yml</code>. The repository setting must be **Settings → Pages → GitHub Actions**.

~~~bash
python one.py
python one.py check
~~~

The check command validates the portal, manifests, schemas, and JavaScript without opening a browser.

## Ecosystem governance

1. **Domain ownership:** each module owns its code, API, tests, and release.
2. **Explicit links:** integrations use versioned interfaces rather than hidden globals.
3. **Evidence before status:** observed, not found, unknown, failed, and passed remain distinct.
4. **Bounded execution:** capacity, ownership, timeout, and cleanup are documented.
5. **Honest maturity:** an adapter-ready contract is not described as a completed production integration.

## Readiness criteria

A host test proves portable software invariants only. Target compiler checks, linker maps, board revisions, fixtures, measurement provenance, and hardware-in-the-loop are separate evidence gates.

Documentation:
- [Shared integration protocol](docs/INTEGRATION_PROTOCOL.md)
- [Module registry](registry/ecosystem.json)
- [Portal UI guide](docs/PORTAL_UI.md)

## Technical identity

**Klipot** is the canonical portal and control-plane name. The GitHub path and public Pages URL are stable project addresses.

## Ecosystem

[ SAMBU ](https://github.com/bboroski/SAMBU) · [ToolNG](https://github.com/bboroski/ToolNG) · [ReaperCripple](https://github.com/bboroski/ReaperCripple) · [Kloz](https://github.com/bboroski/Kloz) · [CO](https://github.com/bboroski/CO) · [SaintSI](https://github.com/bboroski/SaintSI) · [NUN](https://github.com/bboroski/NUN) · [NUNLauncher](https://github.com/bboroski/NUNLauncher).

## License

Earlier project documentation declared MIT, but this repository has no LICENSE file. Confirm the license and add its full text before distribution.
