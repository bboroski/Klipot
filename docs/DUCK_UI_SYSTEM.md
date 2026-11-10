# Duck UI foundation — Klipot

**Status:** visual foundation only. This repository had no application source or UI to redesign when the theme was added. No working desktop or web application is claimed by this document.

## Shared visual contract

The canonical machine-readable tokens are in [`design/duck-ui.tokens.json`](../design/duck-ui.tokens.json). Use deep graphite `#0D0D0D`, panels `#1A1A1A` / `#141414`, primary yellow `#FFD600`, secondary yellow `#BFA100`, text `#E6E6E6`, muted text `#999999`, dividers `#262626`, success `#4CAF50` and errors `#FF4444`.

## Rules for future application screens

- Create a shared shell: header, collapsible sidebar, workspace, contextual inspector and durable status region.
- Yellow is reserved for primary actions, active navigation, focus and progress.
- Support 85–150% application zoom and OS DPI scaling; test 1366×768, 1920×1080 and 4K.
- Prefer vector icons and SVG illustrations. Avoid low-resolution bitmap logos.
- Keep reports and help content inside the application; external browser navigation is opt-in.
- Keyboard navigation, 2 px focus indication, high-contrast mode and reduced motion are requirements.
- Do not claim screenshots of a live application until a real build has been launched and captured.
