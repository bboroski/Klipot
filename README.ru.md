<p align="center"><img src="assets/duck-ui/duck-mark.svg" alt="Klipot mark" width="92"></p>
<h1 align="center">Klipot</h1>
<p align="center"><strong>Ecosystem Integration & Control Plane</strong></p>
<p align="center"><strong>Статический портал · HTML + JavaScript</strong></p>
<p align="center"><a href="README.md">🇺🇦 Українська</a> · <a href="README.en.md">🇬🇧 English</a> · <a href="README.ru.md">🇷🇺 Русский</a></p>
<sub>Обновлено: 2026-11-11</sub>


## Навигация

- [Текущие возможности](#текущие-возможности)
- [Быстрый старт и проверка](#быстрый-старт-и-проверка)
- [Архитектура и подтверждённые границы](#архитектура-и-подтверждённые-границы)
- [Превью портала](#превью-портала)
- [Инженерное качество](#инженерное-качество)
- [Карта документации](#карта-документации)
- [NUN Mesh и связанные репозитории](#nun-mesh-и-связанные-репозитории)
- [Дизайн и документация](#дизайн-и-документация)
- [Лицензия](#лицензия)

> **Klipot** — Klipot — центральный каталог и control plane инженерной экосистемы: репозитории, роли, контракты, ссылки и проверяемые границы интеграции.

## Текущие возможности
- Каталог репозиториев с поиском и фильтрами.
- Machine-readable registry и versioned integration protocol.
- Browser labs для локальной демонстрации allocation, lifecycle и capability gates.
- CI-проверки метаданных, схем, контрактов и JavaScript; cross-repository roadmap.

## Быстрый старт и проверка
```bash
python -m http.server 8080
# открыть http://localhost:8080
python one.py check
```

## Архитектура и подтверждённые границы
Browser labs используют локальные модели и synthetic data. Они не запускают native C, не читают аппаратную телеметрию и не управляют устройствами. Каталог не объединяет независимые репозитории в монолит.

## Превью портала

Статическое векторное превью концепции Klipot в стиле Duck Black / Yellow. Это дизайн-макет, а не скриншот работающего портала.

<p align="center"><img src="assets/portal-ui-preview.svg" alt="Klipot: векторное превью портала с каталогом репозиториев и навигацией" width="960"></p>
<p align="center"><em>Портал, каталог репозиториев и быстрые переходы к лабораториям</em></p>

## Инженерное качество
- Запускайте проверки для целевой платформы; host CI не заменяет аппаратную квалификацию.
- Статусы implemented, partial и planned должны подтверждаться кодом, тестами и доказательствами.
- Макет, спецификация или открытый Pull Request не доказывают production-ready реализацию.
- Внешние интеграции должны быть явными, версионированными, изолированными и тестируемыми.

## Карта документации

- [Архитектура портала](docs/ARCHITECTURE.md)
- [Контракты экосистемы](docs/CONTRACTS.md)
- [Протокол интеграции](docs/INTEGRATION_PROTOCOL.md)
- [Интерфейс портала](docs/PORTAL_UI.md)

## NUN Mesh и связанные репозитории
[SAMBU](https://github.com/bboroski/SAMBU) · [ToolNG](https://github.com/bboroski/ToolNG) · [ReaperCripple](https://github.com/bboroski/ReaperCripple) · [Kloz](https://github.com/bboroski/Kloz) · [CO](https://github.com/bboroski/CO) · [SaintSI](https://github.com/bboroski/SaintSI) · [Klipot](https://github.com/bboroski/Klipot) · [NUN](https://github.com/bboroski/NUN) · [NUNLauncher](https://github.com/bboroski/NUNLauncher)

Каждый репозиторий сохраняет каноническое имя, собственный код, API, цикл выпуска и границы ответственности. Интеграция означает версионированные контракты, а не автоматическое слияние независимых runtime.

## Дизайн и документация
Общее направление интерфейсов — **Duck Black / Yellow**: тёмные поверхности, жёлтые акценты для действий и состояний, читаемая типографика, доступный контраст, клавиатурная навигация и поддержка reduced motion. Подробности — в [design/DUCK_UI_SYSTEM.md](design/DUCK_UI_SYSTEM.md), если файл присутствует.

## Лицензия
Лицензия не объявлена; файл LICENSE отсутствует.

---
**Создано с любовью к инженерии, системности и людям.**
