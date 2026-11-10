# Duck UI system — Klipot

**Status:** applied to the existing single-file HTML/CSS/JavaScript control portal in `index.html`.

## Product surface

Klipot is the operator-facing control plane for the seven-project engineering mesh. The actual portal contains four client-side views: Overview, Projects, Interactive labs and Mesh protocol. Search/filter, navigation, clone-copy actions and browser-side concept labs remain implemented in the page itself. The labs are simulations; they do not run embedded C code or produce hardware evidence.

## Applied visual system

The canonical machine-readable source of truth is [`design/duck-ui.tokens.json`](../design/duck-ui.tokens.json). The live CSS variables in `index.html` use the matching palette:

- Canvas: `#0D0D0D`
- Elevated surfaces: `#1A1A1A` and `#141414`
- Signal yellow: `#FFD600`
- Secondary yellow: `#BFA100`
- Selected state: `#332B00`
- Primary text: `#E6E6E6`
- Muted text: `#999999`
- Dividers: `#262626`
- Success / error: `#4CAF50` / `#FF4444`

Yellow is reserved for the duck mark, primary actions, active navigation, focus and priority signals. The visual layer respects responsive layout and reduced-motion preferences. New interactions must preserve visible hover, pressed and keyboard-focus states.

## Interaction and accessibility

- Keep the existing four views and URL-hash navigation.
- Preserve project search/filter and working copy controls.
- Keep every lab outcome labelled as a simulation, with no claim of live device or hardware access.
- Use semantic elements and keyboard-visible focus.
- Respect reduced-motion preferences.
- Keep essential documentation in portal views where practical; external links are used only for source repositories and explicitly external resources.
- Never introduce inert buttons or mock controls that appear operational.

## Vector preview policy

[`assets/portal-ui-preview.svg`](../assets/portal-ui-preview.svg) is a high-resolution static vector layout preview, not a screenshot of the live portal. It must remain labelled as a preview. Runtime screenshots require a browser capture of the running page at a stated viewport size and must be kept distinct from the SVG illustration.

## Validation

After any portal change, run the repository's Pages workflow or equivalent local checks for inline JavaScript syntax, required interaction markers, SVG parsing, and responsive/reduced-motion rules. A successful browser demo is not firmware or hardware qualification evidence.
