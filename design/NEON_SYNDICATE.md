# NEON SYNDICATE — Klipot portal visual specification

**Project:** Klipot — Ecosystem Integration & Control Plane  
**Surface:** Responsive web portal and browser-safe interactive labs.

## Identity and color
Use Void Black `#050505`, Warning Yellow `#FCEE0A`, System Red `#FF003C`, Data Blue `#00F0FF`, and Interface White `#FFFFFF`. Carbon surfaces are `#0D1115` and `#11171C`, with `#A6B2BC` for muted data. Preserve clear contrast and pair state colors with text/icons.

## Typography and layout
Orbitron/Rajdhani for display headings, Rajdhani/system sans-serif for content, Roboto Mono/Share Tech Mono for technical labels and IDs. Retain Klipot's responsive portal, project registry, mesh map, interactive labs and protocol views; apply chamfered cards, restrained hex patterns and thin technical lines without compromising mobile navigation.

## Interaction and motion
Use 120–260 ms transitions, subtle hover lift and clear focus states. Respect `prefers-reduced-motion`. Keep browser labs explicit, isolated and labelled as demonstrations where appropriate. Do not use visual status as a substitute for actual API results.

## Screenshot policy
Capture the running portal in a browser at a stated viewport. Prefer 1920×1080 or higher, plus a compact mobile/desktop layout. Actual captures must be browser screenshots (PNG/WebP); SVGs are design previews, never runtime evidence. Redact tokens, private data and local paths.

## Files
- `index.html` and `web/index.html`: live portal surfaces, palette refreshed.
- `assets/neon-syndicate/overview.svg`: static design preview.
- `assets/neon-syndicate/theme.css`: reusable theme layer.
- `design/neon-syndicate.tokens.json`: machine-readable design tokens.
