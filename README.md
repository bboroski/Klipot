<!-- Title: Klipot — static ecosystem catalog and integration control portal -->
<p align="center"><img src="assets/duck-ui/duck-mark.svg" alt="Логотип Klipot" width="76"></p>

# Klipot — каталог репозиторіїв та портал інтеграції екосистеми

[![CI](https://github.com/bboroski/Klipot/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/bboroski/Klipot/actions/workflows/ci.yml) [![Pages](https://github.com/bboroski/Klipot/actions/workflows/pages.yml/badge.svg?branch=main)](https://github.com/bboroski/Klipot/actions/workflows/pages.yml)

**Klipot** — статичний HTML/CSS/JavaScript-портал для пошуку репозиторіїв, перегляду модулів, контрактів та інтеграційних зв'язків у програмній екосистемі.

<sub>Оновлено: 2026-11-11 · Версія пакета: 0.1.0 · Тип: static web portal</sub>

> **TL;DR:** запустіть локальний HTTP-сервер із кореня репозиторію та відкрийте сторінку на localhost:8080. Backend або окремий application server для локального preview не потрібен.

[Українська](README.md) · [English](README.en.md) · [Русский](README.ru.md)

## Зміст

- [Призначення](#призначення)
- [Можливості порталу](#можливості-порталу)
- [Локальний запуск](#локальний-запуск)
- [Перевірки та CI](#перевірки-та-ci)
- [Дані та межі довіри](#дані-та-межі-довіри)
- [Архітектура й документація](#архітектура-й-документація)
- [Пов'язані репозиторії](#повязані-репозиторії)
- [FAQ](#faq)
- [Підтримка та ліцензія](#підтримка-та-ліцензія)

## Призначення

Klipot — точка навігації по екосистемі. Він показує структуру й версіоновані зв'язки між незалежними проєктами, але не зливає їх у моноліт і не виконує код інших репозиторіїв.

## Можливості порталу

- Каталог репозиторіїв із пошуком і фільтрами.
- Machine-readable registry та versioned integration protocol.
- Граф залежностей і картки контрактів модулів.
- Browser labs для локальної демонстрації allocation, lifecycle та capability-gate моделей.
- CI-перевірки metadata, схем, контрактів і JavaScript.
- Документація інтеграцій та roadmap екосистеми.

## Локальний запуск

Потрібен сучасний браузер. Для простого локального preview — Python 3 або будь-який статичний HTTP-сервер. Обов'язкових runtime-пакетів у pyproject немає.

~~~bash
python -m http.server 8080
~~~

Потім відкрийте http://localhost:8080. Сервер запускається в поточному каталозі репозиторію; зупиніть його через Ctrl+C.

## Перевірки та CI

~~~bash
python one.py check
~~~

У CI також перевіряються [основний workflow](.github/workflows/ci.yml), [GitHub Pages deployment](.github/workflows/pages.yml), [mesh contracts](.github/workflows/mesh-contracts.yml) і [Duck quality gate](.github/workflows/duck-quality-gate.yml).

## Дані та межі довіри

- Browser labs використовують локальну модель і synthetic data.
- Демонстрації не запускають native C, не читають апаратну телеметрію й не керують пристроями.
- Каталог репозиторіїв не є підтвердженням того, що їхній код зібрано, протестовано або запущено.
- Klipot не є sandbox, plugin executor або production control system.
- Не додавайте секрети чи токени до registry та публічних конфігурацій.

## Архітектура й документація

Почніть із [архітектури порталу](docs/ARCHITECTURE.md), [контрактів екосистеми](docs/CONTRACTS.md), [integration protocol](docs/INTEGRATION_PROTOCOL.md) та [опису UI](docs/PORTAL_UI.md). Дані модуля та залежностей: [sambu.module.json](sambu.module.json), [registry](registry) та [schemas](schemas).

## Пов'язані репозиторії

- [SAMBU](https://github.com/bboroski/SAMBU) — джерело canonical module manifest та registry contracts, які Klipot відображає як локальну проєкцію.
- [Luci](https://github.com/bboroski/Luci) — локальна CLI-площина доменів і перевірки manifest/policy.
- [NUN](https://github.com/bboroski/NUN) та [NUNLauncher](https://github.com/bboroski/NUNLauncher) — системні контракти й перевірка boot metadata.
- [ReaperCripple](https://github.com/bboroski/ReaperCripple), [Kloz](https://github.com/bboroski/Kloz), [CO](https://github.com/bboroski/CO) і [SaintSI](https://github.com/bboroski/SaintSI) — embedded, platform, lifecycle та integrity модулі.

## FAQ

**Чи потрібен Node.js для preview?** Ні. Для поточного статичного порталу достатньо браузера та HTTP-сервера.

**Чи запускають browser labs реальний C-код?** Ні. Вони демонструють локальні синтетичні моделі.

**Чи має портал backend?** У поточному описаному setup основний портал є статичним HTML/CSS/JavaScript.

## Підтримка та ліцензія

Баги: [Issue tracker](https://github.com/bboroski/Klipot/issues) · [bug report](https://github.com/bboroski/Klipot/issues/new). PR має включати відтворюваний сценарій, перевірку JavaScript/schema та оновлення відповідної документації. Профіль супроводу: [bboroski](https://github.com/bboroski).

**Ліцензія не оголошена:** файл LICENSE не знайдено в репозиторії. Узгодьте умови використання та розповсюдження з правовласником.
