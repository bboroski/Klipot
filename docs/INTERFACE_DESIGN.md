# Klipot — Amber–Obsidian interface specification

## Product boundary

**Klipot** — Engineering ecosystem integration and control portal.

Klipot is the real HTML/CSS/JavaScript portal. Apply the amber palette directly to its CSS tokens and retain semantic controls, URL hash navigation, keyboard focus and reduced-motion support.

The preview is a static concept illustration. It is not an implemented runtime surface, executable kernel, bootloader or live telemetry dashboard.

## Visual system

- Obsidian canvas `#0B0B0D`; graphite surfaces `#141416`, `#1C1C1E`, `#2C2C30`.
- Borders `#34343A`; text `#F5F3EE`; muted metadata `#A6A3AB`.
- Project accent `#FF9F0A`, pressed accent `#D97706`, secondary signal `#A78BFA`.
- State vocabulary: passed `#64C787`, caution `#FFBF47`, fault `#F16D65`, unknown `#A78BFA`.

## Information hierarchy

1. **OVERVIEW** — the highest-priority project boundary.
2. **PROJECT DIRECTORY** — the measurable internal contract.
3. **INTERACTIVE LABS** — proof, diagnostics or readiness evidence.

Use a fixed identity rail, compact left navigation, four compact metric cards, and docked detail panels. All state labels must be explicit; colour is never the only carrier. Use monospaced tabular numerals for addresses, sizes, ticks and versions. Use visible focus, at least 36×36 px targets when interactive controls eventually exist, and reduced-motion-aware transitions.

## Readiness and honesty

The UI must show `NOT IMPLEMENTED`, `UNKNOWN`, `UNVERIFIED` or `SPECIFICATION ONLY` when no test result exists. A mockup, documentation gate or host-side test must never be presented as evidence of bootability or target hardware support.

## Artwork

- [Project mark](../assets/amber-obsidian-mark.svg)
- [Interface concept preview](../assets/amber-obsidian-preview.svg)

## Tokens

```css
:root {
  color-scheme: dark;
  --ao-canvas: #0B0B0D;
  --ao-surface-1: #141416;
  --ao-surface-2: #1C1C1E;
  --ao-surface-3: #2C2C30;
  --ao-border: #34343A;
  --ao-text: #F5F3EE;
  --ao-muted: #A6A3AB;
  --ao-accent: #FF9F0A;
  --ao-accent-pressed: #D97706;
  --ao-secondary: #A78BFA;
  --ao-success: #64C787;
  --ao-warning: #FFBF47;
  --ao-danger: #F16D65;
}
```
