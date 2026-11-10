# Abstract UI Grammar — Nine Product Surfaces

**Status:** design-system specification  
**Scope:** the nine repositories in the Klipot engineering mesh  
**Implementation note:** each repository owns its own UI implementation, palette and release cadence.

## 1. Read the sketch as a composition

The abstract drawing contributes five reusable spatial ideas:

1. **Status rail** — a narrow top zone for identity, time, session and important state.
2. **Open field** — a large uncluttered workspace rather than a stack of equal cards.
3. **Independent nodes** — distinct outlined objects placed around a focal point, with visible relationships.
4. **Context boundary** — a selected node reveals its detail, evidence or contract without hiding the whole field.
5. **Action rail** — a compact bottom zone for navigation, tools and current session state.

The rough curves in the sketch are translated into a domain graph, not copied as decorative scribbles. Every connector must explain a real relationship. A connector is not proof of a runtime dependency.

## 2. Nine independent interpretations

| Repository | Application surface | Spatial translation | Palette |
|---|---|---|---|
| [SAMBU](https://github.com/bboroski/SAMBU/tree/feat/abstract-ui-suite-20261111/ui) | Scientific IDE / Studio | Source → AST → model → result pipeline with file explorer and inspector | Graphite, mineral grey, acid lime, scientific blue |
| [ToolNG](https://github.com/bboroski/ToolNG/tree/feat/abstract-ui-suite-20261111/ui) | Windows evidence desk | PnP, service and backup observations connected into an evidence path | Slate, ice cyan, amber and restrained red |
| [ReaperCripple](https://github.com/bboroski/ReaperCripple/tree/feat/abstract-ui-suite-20261111/ui) | Manufacturing bring-up console | COLD → PROBED → profile/fixture gates → manufacturing event tape | Industrial navy, copper-orange, fixture mint |
| [Kloz](https://github.com/bboroski/Kloz/tree/feat/abstract-ui-suite-20261111/ui) | Bare-metal contract inspector | Caller-owned arena, alignment gate, versioned platform ABI and target-port boundary | Mineral parchment, forest green, brass |
| [CO](https://github.com/bboroski/CO/tree/feat/abstract-ui-suite-20261111/ui) | Lifecycle state inspector | STOPPED, STARTING, RUNNING, STEPPING and FAULTED transition graph | Steel, violet and mint |
| [SaintSI](https://github.com/bboroski/SaintSI/tree/feat/abstract-ui-suite-20261111/ui) | Heartbeat / integrity observatory | Component heartbeat nodes, monotonic timeout states and CRC sample | Marine blue, teal and coral |
| [Klipot](https://github.com/bboroski/Klipot/tree/feat/abstract-ui-suite-20261111/ui) | Ecosystem constellation | Eight repository nodes orbit the integration control plane | Graphite, warm mineral, restrained signal brass |
| [NUN](https://github.com/bboroski/NUN/tree/feat/abstract-ui-suite-20261111/ui) | Engineering desktop | Architecture blueprint, component inventory and project workspace | Evergreen graphite, mineral ivory, copper and jade |
| [NUNLauncher](https://github.com/bboroski/NUNLauncher/tree/feat/abstract-ui-suite-20261111/ui) | Mobile home environment | Status strip, orbital widget, app collection, drawer and quick-control sheet | Midnight indigo, lavender, cyan and soft coral |

## 3. Interaction contract

- Hover may raise a control; press must visibly sink it with an inset shadow.
- A selected node must be distinguishable without colour alone.
- Focus indicators remain visible to keyboard users.
- Motion must respect `prefers-reduced-motion`.
- Search and category filters must change visible content, not act as decoration.
- Modal detail panels must have a clear close action and remain keyboard-accessible.
- A demo action must state that it is a preview and must not silently mutate the host.

## 4. Evidence and safety semantics

The design system preserves each product's real trust boundary:

- ToolNG separates confirmed, not-found, unknown and failed observations. An aggregate score never hides incomplete evidence coverage.
- ReaperCripple shows host workflow progression separately from board/fixture qualification. A simulated event cannot promote a physical board to READY.
- Kloz distinguishes portable host invariants from target-specific MMIO, DMA, cache, IRQ and linker guarantees.
- CO exposes explicit lifecycle transitions; one poll represents one step callback, not a scheduler or background worker.
- SaintSI reports heartbeat timeout and CRC observations. It does not restart components, service a watchdog or provide cryptographic authenticity.
- NUN and NUNLauncher UI previews are not bootable OS or bootloader implementations.
- Klipot connection lines are catalog relationships, not proof of an automatically linked runtime.

## 5. Review checklist

- [ ] Product purpose is apparent before the user opens a detail panel.
- [ ] The main workspace has one dominant focal surface and a clear hierarchy.
- [ ] Nodes describe actual domain concepts, not generic filler cards.
- [ ] The selected-node inspector explains status, contract and limitations.
- [ ] Bottom actions map to genuine navigation or clearly-labelled local preview actions.
- [ ] Layout adapts to narrow screens.
- [ ] Static UI previews do not claim native runtime integration.
