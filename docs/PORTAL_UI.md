# Klipot portal UI and interaction design

## Product surface

Klipot is the operator-facing entry point for the modular engineering mesh. The portal is a dependency-free HTML/CSS/JavaScript application published from the repository root with GitHub Pages.

The interface is deliberately split into four real views:

- **Overview:** product positioning, capability summary and ecosystem map.
- **Projects:** searchable and filterable seven-repository directory with direct source links, GUI guides and copyable clone URLs.
- **Interactive labs:** browser-side API concept demonstrations for Kloz, CO, SaintSI and ReaperCripple.
- **Mesh protocol:** integration boundaries, evidence vocabulary, version and safety rules.

The quick-start action copies the Klipot clone command. All actions are native links or buttons; there are no inert decorative controls.

## Visual system

The live portal has been normalized to the Amber–Obsidian v2 palette. CSS variables in `index.html` map to the machine-readable `design/duck-ui.tokens.json` values: canvas `#0B0B0D`, elevated surfaces `#1C1C1E` / `#141416`, signal amber `#FF9F0A`, secondary accent `#D97706`, selected state `#3A2408`, text `#F5F3EE`, muted text `#A6A3AB`, borders `#34343A`, success `#64C787` and error `#F16D65`. The visual language is strict obsidian / graphite / signal amber:

| Token | Use |
|---|---|
| Near-black | Page canvas, navigation and deepest surfaces |
| Graphite | Cards, panels and elevated surfaces |
| Signal yellow | Brand mark, primary actions, active navigation, focus and key system lines |
| Warm grey | Supporting copy and secondary labels |
| Green / amber / red | Lab outcomes only: accepted, review or rejected |

The page uses a responsive top navigation, layered hero, system-map illustration, metric strip, capability cards, project cards, labs and protocol panels. `assets/portal-ui-preview.svg` is a high-resolution vector design reference, not a screenshot of the running page. Hover and pressed states are visible. Cards lift subtly; view transitions are short and can be reduced by the operating-system preference.

## Interaction contract

- **Navigation:** Overview, Projects, Interactive labs and Mesh protocol switch real client-side views and preserve the selected route in the URL hash.
- **Project directory:** text search and domain filters update repository cards immediately.
- **Repository actions:** project links open the source; clone controls copy the HTTPS URL.
- **Quick start:** copies `git clone https://github.com/bboroski/Klipot.git`.
- **Kloz lab:** validates positive allocation sizes, power-of-two alignment, padding and fixed capacity.
- **CO lab:** demonstrates guarded lifecycle transitions, bounded poll steps, failure retention and explicit stop.
- **SaintSI lab:** advances a 32-bit tick counter, refreshes a heartbeat and reports stale state without taking an actuator action.
- **ReaperCripple lab:** validates a declared capability set before showing a bootstrap gate as eligible.

## Accessibility and safety

The portal uses semantic sections, labelled inputs, keyboard-visible focus, native buttons and links, and polite live regions for lab output. The layout adapts to narrow screens. Reduced-motion preferences are respected.

Every lab is a browser simulation. None executes the C libraries, probes a board, queries Windows, scans a device or records manufacturing evidence. A passing browser demo is not host-test evidence or hardware qualification.

## Deployment

The workflow at `.github/workflows/pages.yml` validates the page, key interaction markers, SVG assets and inline JavaScript syntax, then deploys the repository root using GitHub Pages.

The repository must have **Settings → Pages → Build and deployment → GitHub Actions** selected for the first deployment. After that setting is active, pushes to `main` that change the portal or its assets trigger deployment automatically.


## Amber–Obsidian v2 update

The live portal CSS now uses obsidian canvas `#0B0B0D`, graphite surfaces `#1C1C1E` / `#141416`, amber action/focus `#FF9F0A`, and explicit warning/unknown states. Interactive targets were raised to a 36 px minimum for compact controls; pressed states include an inset response, and numeric readouts use tabular figures. The full reusable token and accessibility contract is in [INTERFACE_DESIGN.md](INTERFACE_DESIGN.md).
