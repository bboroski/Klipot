# GUI / Visual System Standard

> Web-portal specification for Klipot. Browser labs are simulations and must remain clearly distinguished from external runtimes and hardware.

## Visual identity

| Token | Value | Use |
|---|---|---|
| Primary yellow | `#FFCC00` | Main action, selected module and key emphasis |
| Highlight yellow | `#FFE600` | Hover, focus and active progress |
| Deep black / graphite | `#000000` / `#1A1A1A` | Navigation, header and structural surfaces |
| Alert red | `#E53935` | Errors and destructive warnings |
| Signal cyan | `#29B6F6` | Live activity, links and data-flow indicators |
| White | `#FFFFFF` | Text and high-contrast details |

Existing Duck UI tokens, CSS and marks remain the canonical implementation where already present. Do not fork them silently; token changes require matching CSS, preview and check updates.

## Portal layout

- Header: canonical Klipot mark/name, global status, actual progress/activity and local time.
- Main workspace: searchable module catalog, registry/dependency view, contract/documentation details.
- Context panel: selected module metadata, maturity, owner, evidence links and supported actions.
- Footer/pager: route/page navigation where required.

The sample `55 / ~~~ / 21:33` is conceptual only. Never display fabricated availability, build status, live telemetry or progress. If information is cached, show source and updated time.

## Interaction and data integrity

- Search and filters remain keyboard-operable, URL/deep-linkable where appropriate and clearable.
- Cards distinguish implemented, experimental, specification-only and proposal status.
- Browser labs must carry a persistent **Simulation** label; they do not execute embedded C code, control fixtures or prove device state.
- Clone/open/copy actions show success or failure; external repository facts are linked to their source.
- Errors use red; active data flow uses cyan; yellow marks primary action/focus. Pair color with text/icon.
- Long-running registry refreshes are asynchronous, cancellable where safe and expose stale/failed results.

## Accessibility and responsive behavior

Provide semantic landmarks, labels, keyboard navigation, visible focus, reduced motion, zoom support and WCAG AA contrast (4.5:1 normal text; 3:1 large text). Target 44×44 CSS-pixel hit areas for touch. Test narrow layouts, keyboard-only workflows and 200% zoom.

## Release gate

Verify navigation, filters, module deep links, copy feedback, loading/empty/error states, simulation disclaimers and provenance. Screenshots must be from the deployed/current portal; wireframes are marked **concept**. A portal check does not certify every linked repository.

## Українська

Klipot — статичний портал-каталог. Основний макет: верхня панель, пошук і каталог модулів, контекстна панель обраного модуля, навігація. Жовтий `#FFCC00` позначає головні дії, `#FFE600` — фокус, червоний `#E53935` — помилки, блакитний `#29B6F6` — активність. Значення `55 / ~~~ / 21:33` не можна видавати за реальну телеметрію. Browser-labs завжди позначаються як симуляції та не керують обладнанням.

## Русский

Klipot — статический портал-каталог. Основной макет: верхняя панель, поиск и каталог модулей, контекстная панель выбранного модуля, навигация. Жёлтый `#FFCC00` обозначает главные действия, `#FFE600` — фокус, красный `#E53935` — ошибки, голубой `#29B6F6` — активность. Значения `55 / ~~~ / 21:33` нельзя выдавать за реальную телеметрию. Browser-labs всегда маркируются как симуляции и не управляют оборудованием.
