# Klipot portal UI and interaction design

## Application surface

The portal is a dependency-free HTML/CSS/JavaScript application. It is intentionally the single graphical front door for the mesh: embedded libraries receive focused API-concept sandboxes, while SAMBU and ToolNG retain their existing desktop applications.

## Interaction contract

- **Navigation:** overview, project directory, interactive labs and integration protocol are real client-side views.
- **Project directory:** text search and domain filters update repository cards immediately.
- **Repository actions:** external links open the project; clone controls copy the HTTPS clone URL and show a fallback when clipboard access is unavailable.
- **Kloz lab:** validates positive allocation sizes, power-of-two alignment, padding and fixed capacity.
- **CO lab:** demonstrates guarded lifecycle transitions, bounded poll steps, failure retention and explicit stop.
- **SaintSI lab:** advances a 32-bit tick counter, refreshes a heartbeat and reports stale state without taking an actuator action.
- **ReaperCripple lab:** validates a capability set before showing the boot gate as eligible.

Every lab is marked as a browser simulation. None calls the C libraries, probes a board, queries Windows, scans a device or records manufacturing evidence.

## Visual system

| Token | Use |
|---|---|
| Deep navy / graphite | Canvas and navigation surfaces |
| Elevated blue-grey | Cards, panels and focus regions |
| Mint | Primary actions, active route and positive state |
| Soft blue | Secondary emphasis and information |
| Amber | Review or blocked-by-policy status |
| Red | Validation rejection or failed operation |

Buttons have visible hover and pressed feedback. Cards lift slightly on hover. View transitions use a short opacity/vertical entrance. Focus-visible outlines are retained for keyboard navigation. Status updates use polite live regions. The layout collapses to a compact top navigation on mobile and two responsive grids at intermediate widths.

The application honors prefers-reduced-motion by minimizing animations and transitions. Inputs have labels, nav has an accessible name, and interactive actions are native buttons or links.

## Deployment

GitHub Actions validates the portal asset and control markers, then publishes the repository root using GitHub Pages. A repository administrator must enable Settings → Pages → GitHub Actions before the first deployment. Until that setting is enabled and a deployment succeeds, the authoritative copy is the source at index.html.

## Future GUI work

Do not force a generic desktop GUI into a low-level static library. Kloz, CO and SaintSI are better served by tests, host simulators and board adapters. ReaperCripple's future factory UI must be bound to real fixture/recipe evidence. SAMBU Duck Studio and ToolNG should evolve within their native Tkinter and Win32 design systems.
