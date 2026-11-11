
> **Фирменная палитра:** сигнальный жёлтый `#FFD600`; глубокий чёрный `#111111`.
<p align="center"><img src="assets/duck-ui/duck-mark.svg" alt="Klipot mark" width="92"></p>
<h1 align="center">Klipot</h1>
<p align="center"><strong>Ecosystem Integration &amp; Control Plane</strong></p>
<p align="center"><img src="https://img.shields.io/badge/STATUS-STATIC%20PORTAL-FFD600?style=for-the-badge&labelColor=111111"><img src="https://img.shields.io/badge/CORE-HTML%20%2B%20JS-FFD600?style=for-the-badge&labelColor=111111"><img src="https://img.shields.io/badge/LICENSE-NOT%20DECLARED-FFD600?style=for-the-badge&labelColor=111111"></p>
<p align="center"><a href="README.md">🇺🇦 Українська</a> · <a href="README.en.md">🇬🇧 English</a> · <a href="README.ru.md">🇷🇺 Русский</a></p>
<p align="center"><sub><a href="design/DUCK_UI_SYSTEM.md">Duck Black / Yellow UI standard</a> · <a href="assets/duck-ui/duck-ui-preview.svg">Vector UI preview</a></sub></p>

---

**Klipot — центральный каталог и control plane инженерной экосистемы.** Он показывает модули, границы ответственности, интеграционные контракты и входы в документацию, не объединяя независимые runtime в монолит.

## Возможности портала

- Каталог модулей с фильтрами по доменам и поиском.
- Ссылки на исходный код, GUI-документацию и инструкции запуска.
- Копирование clone-команд.
- Machine-readable registry и versioned integration protocol.
- Browser-labs с демонстрациями allocation, lifecycle, heartbeat и capability-gate.
- CI-проверки метаданных, контрактов, схем и синтаксиса статического портала.

**Граница симуляции:** browser-labs не исполняют C-код, не читают телеметрию оборудования, не управляют fixtures и не подтверждают физическое состояние устройства.

## Карта экосистемы

| Репозиторий | Роль | Текущий статус |
|---|---|---|
| [SAMBU](https://github.com/bboroski/SAMBU) | Язык, IDE, modeling и workflow | Experimental alpha |
| [ToolNG](https://github.com/bboroski/ToolNG) | Локальная диагностика Windows | Windows desktop utility |
| [ReaperCripple](https://github.com/bboroski/ReaperCripple) | Embedded bring-up и manufacturing lifecycle | Host-tested; target qualification отдельно |
| [Kloz](https://github.com/bboroski/Kloz) | Bare-metal C11 substrate и platform ABI | Host-tested core |
| [CO](https://github.com/bboroski/CO) | Жизненный цикл компонентов | Host-tested core |
| [SaintSI](https://github.com/bboroski/SaintSI) | Heartbeat-наблюдение и CRC | Host-tested core |
| [Klipot](https://github.com/bboroski/Klipot) | Каталог и control plane | Static portal |
| [NUN](https://github.com/bboroski/NUN) | Спецификация минимального ядра ОС | Specification only |
| [NUNLauncher](https://github.com/bboroski/NUNLauncher) | Спецификация bootstrap и handoff | Specification only |
| [Fragile-Baby](https://github.com/bboroski/Fragile-Baby) | Архитектурное направление Elbrus/E2K | Proposal; target evidence pending |
| [Luci](https://github.com/bboroski/Luci) | Документационный каркас дизайн-системы и интеграционных границ | Scope pending |

## NUN Mesh

<p align="center"><img src="assets/nun-mesh-overview.svg" alt="NUN Mesh — семь инженерных репозиториев, связанных версионированными контрактами" width="100%"></p>

**NUN Mesh** — это контрактное ядро из семи репозиториев: Kloz, CO, SaintSI, ReaperCripple, SAMBU, ToolNG и Klipot. Ещё четыре направления каталога — NUN, NUNLauncher, Fragile-Baby и Luci — сохраняют отдельные статусы зрелости: спецификации, архитектурные предложения или документационные каркасы. Они не выдаются за проверенные runtime или аппаратную поддержку.

Каждый компонент сохраняет владение собственным кодом и жизненным циклом. Интеграции используют версионированные контракты, явные адаптеры и проверяемые доказательства.

## Локальный запуск

Откройте <code>index.html</code> или запустите локальный сервер:

~~~bash
python -m http.server 8080
~~~

Затем перейдите на <code>http://localhost:8080</code>. Внешний framework или пакет JavaScript не требуется.

## Публикация и проверки

Workflow: <code>.github/workflows/pages.yml</code>. Для GitHub Pages выберите **Settings → Pages → GitHub Actions**.

~~~bash
python one.py
python one.py check
~~~

Проверки охватывают портал, манифесты, схемы и JavaScript; они не валидируют каждый внешний репозиторий.

## Управление экосистемой

1. **Владение доменом:** каждый модуль отвечает за собственный код, API, тесты и релиз.
2. **Явные связи:** интеграции используют версионированные контракты.
3. **Доказательства важнее статуса:** passed, observed, not found, unknown и failed не смешиваются.
4. **Ограниченное выполнение:** capacity, ownership, timeout и cleanup описываются явно.
5. **Честная зрелость:** host-тесты не заменяют emulator или hardware qualification.

Документация: [Integration Protocol](docs/INTEGRATION_PROTOCOL.md) · [Ecosystem Registry](registry/ecosystem.json) · [Portal UI](docs/PORTAL_UI.md).

## Лицензия

Файл <code>LICENSE</code> отсутствует; лицензия не объявлена. Определите условия до публичного распространения.

---

**Создано с любовью к системности, инженерии и людям.**