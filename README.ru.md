<p align="center"><img src="assets/duck-ui/duck-mark.svg" alt="Klipot mark" width="92"></p>
<h1 align="center">Klipot</h1>
<p align="center"><strong>Ecosystem Integration & Control Plane</strong></p>
<p align="center"><strong>Статический портал · HTML + JavaScript</strong></p>
<p align="center"><a href="README.md">🇺🇦 Українська</a> · <a href="README.en.md">🇬🇧 English</a> · <a href="README.ru.md">🇷🇺 Русский</a></p>

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

## Инженерное качество
- Запускайте проверки для целевой платформы; host CI не заменяет аппаратную квалификацию.
- Статусы implemented, partial и planned должны подтверждаться кодом, тестами и доказательствами.
- Макет, спецификация или открытый Pull Request не доказывают production-ready реализацию.
- Внешние интеграции должны быть явными, версионированными, изолированными и тестируемыми.

## NUN Mesh и связанные репозитории

<p align="center"><img src="assets/nun-mesh-overview.svg" alt="NUN Mesh architecture diagram connecting independent repositories through versioned contracts" width="960"></p>
[SAMBU](https://github.com/bboroski/SAMBU) · [ToolNG](https://github.com/bboroski/ToolNG) · [ReaperCripple](https://github.com/bboroski/ReaperCripple) · [Kloz](https://github.com/bboroski/Kloz) · [CO](https://github.com/bboroski/CO) · [SaintSI](https://github.com/bboroski/SaintSI) · [Klipot](https://github.com/bboroski/Klipot) · [NUN](https://github.com/bboroski/NUN) · [NUNLauncher](https://github.com/bboroski/NUNLauncher) · [Fragile-Baby](https://github.com/bboroski/Fragile-Baby) · [Luci](https://github.com/bboroski/Luci)

Каждый репозиторий сохраняет каноническое имя, собственный код, API, цикл выпуска и границы ответственности. Интеграция означает версионированные контракты, а не автоматическое слияние независимых runtime.

## Дизайн и документация
Общее направление интерфейсов — **Duck Black / Yellow**: тёмные поверхности, жёлтые акценты для действий и состояний, читаемая типографика, доступный контраст, клавиатурная навигация и поддержка reduced motion. Подробности — в [design/DUCK_UI_SYSTEM.md](design/DUCK_UI_SYSTEM.md), если файл присутствует.

## Лицензия
Лицензия не объявлена; файл LICENSE отсутствует.

---
**Создано с любовью к инженерии, системности и людям.**


## Палитра Duck Black / Yellow
Совместимые цвета прежних badges и marks: `#FFD600` (жёлтый) и `#111111` (почти чёрный). Текущий фон интерфейса — `#0D0D0D`. Полная палитра из шести цветов, четырнадцати функциональных оттенков и значения RGB/HSL находятся в `design/duck-ui.tokens.json` (schema 3.0.0). Жёлтый зарезервирован для основных действий, фокуса и выделения; красный и голубой обозначают семантические ошибки и информационные состояния.
