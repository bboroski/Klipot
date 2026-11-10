# Klipot — Ecosystem Integration & Control Plane

**A module catalog, contract registry, and operator portal for independent engineering components.**

Klipot connects documentation, capability registries, versioned integration contracts, and browser labs. It helps users explore architecture and responsibility boundaries without collapsing distinct runtime components into an indistinguishable monolith.

[Українська](README.md) · [English](README.en.md) · [Русский](README.ru.md) · [Repository](https://github.com/bboroski/Klipot) · [Public portal](https://bboroski.github.io/Klipot/)

## The nine repositories

| Repository | Responsibility | Current state |
|---|---|---|
| [SAMBU](https://github.com/bboroski/SAMBU) | Language, IDE, Studio, and workflow tooling | Experimental alpha |
| [ToolNG](https://github.com/bboroski/ToolNG) | Native Windows diagnostics and local evidence reports | Desktop application |
| [ReaperCripple](https://github.com/bboroski/ReaperCripple) | Embedded BSP, calibration, and manufacturing engineering | Host-tested; target validation required |
| [Kloz](https://github.com/bboroski/Kloz) | C11 platform ABI, bounded memory, and CPU/board services | Host-tested core |
| [CO](https://github.com/bboroski/CO) | Deterministic component lifecycle runtime | Host-tested core |
| [SaintSI](https://github.com/bboroski/SaintSI) | Heartbeat supervision and accidental-corruption checks | Host-tested core |
| [Klipot](https://github.com/bboroski/Klipot) | Repository catalog, contracts, and integration portal | Static portal |
| [NUN](https://github.com/bboroski/NUN) | Minimal operating-system kernel specification | Documentation scaffold; no kernel implementation |
| [NUNLauncher](https://github.com/bboroski/NUNLauncher) | Kernel bootstrap and handoff specification | Documentation scaffold; no loader implementation |

NUN and NUNLauncher are not yet a bootable OS or a bootloader. Their READMEs describe proposed boundaries and do not claim missing implementations as completed features.

## Portal capabilities

- module directory with domain filters and search;
- links to source repositories, GUI documentation, and run instructions;
- copyable clone commands;
- machine-readable registry and versioned integration protocol;
- interactive browser labs demonstrating allocation, lifecycle, heartbeat, and capability-gate concepts;
- CI validation of metadata, contracts, and static-portal syntax.

**Browser labs are simulations.** They do not execute C code, read telemetry from physical hardware, control production fixtures, or prove a device's physical state.

## Run locally

Open <code>index.html</code> in a modern browser. No external framework or JavaScript package is required.

~~~bash
python -m http.server 8080
~~~

Then open <code>http://localhost:8080</code>.

## Publish

The portal is published through the GitHub Pages workflow at <code>.github/workflows/pages.yml</code>. Configure **Settings → Pages → GitHub Actions** once in repository settings. Subsequent changes to the default branch are handled by the workflow.

## Architecture rules

1. **Domain ownership:** each module owns its code, API, tests, and release decisions.
2. **Explicit coupling:** integrations use versioned interfaces, not hidden global state.
3. **Evidence before status:** observed, not found, unknown, failed, and passed are distinct.
4. **Bounded execution:** capacity, ownership, timeout, and cleanup are documented explicitly.
5. **Honest maturity:** an adapter-ready contract is not described as a finished production integration.

## Verification and boundaries

A host test validates portable software invariants only. Target compiler, linker map, board revision, fixtures, measurement provenance, and hardware-in-the-loop checks are separate evidence gates. Klipot displays these boundaries; it does not waive them.

- [Shared integration protocol](docs/INTEGRATION_PROTOCOL.md)
- [Module registry](registry/ecosystem.json)
- [Portal UI guide](docs/PORTAL_UI.md)

## Technical identity

**Klipot** is the canonical portal and control-plane name. The current GitHub path and public Pages URL remain stable addresses.

## License

MIT. See [LICENSE](LICENSE).


## One-knob launch

- **Windows:** double-click `one.cmd`; on any OS use `python one.py`.
- `python one.py check` validates the portal, manifests, schemas and JavaScript without opening a browser.
- When all nine repositories are checked out as sibling directories, mesh mode also runs `one.py check` in every module and validates cross-repository contracts. The default run opens the portal after checks.
