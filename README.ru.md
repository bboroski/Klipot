<p align="center"><img src="assets/duck-ui/duck-mark.svg" alt="Duck mark" width="104" /></p>
<h1 align="center">Klipot</h1>
<p align="center"><strong>Ecosystem Integration & Control Plane</strong></p>
<p align="center"><img src="https://img.shields.io/badge/STATUS-STATIC%20PORTAL-FFD600?style=for-the-badge&labelColor=111111" /><img src="https://img.shields.io/badge/CORE-HTML%20%2B%20JS-FFD600?style=for-the-badge&labelColor=111111" /><img src="https://img.shields.io/badge/LICENSE-TEXT%20MISSING-FFD600?style=for-the-badge&labelColor=111111" /></p>
<p align="center"><a href="README.md">🇺🇦 Українська</a> · <a href="README.en.md">🇬🇧 English</a> · <a href="README.ru.md">🇷🇺 Русский</a></p>
<hr />

**Единая карта инженерной экосистемы: модули, контракты, документация и операторский портал — без принудительного слияния независимых runtime в монолит.**

## Позиционирование

Klipot помогает командам видеть связи между компонентами, понимать зоны ответственности и находить описанные интеграционные контракты. Это каталог и control plane для прозрачной координации, а не скрытый монолит.

## Возможности портала

- Каталог модулей с фильтрами по доменам и поиском.
- Ссылки на исходный код, документацию GUI и инструкции запуска.
- Копирование clone-команд.
- Machine-readable registry и versioned integration protocol.
- Browser-labs для демонстрации allocation, lifecycle, heartbeat и capability-gate.
- CI-проверки метаданных, контрактов, схем и синтаксиса статического портала.

**Важно:** browser-labs — симуляции. Они не исполняют C-код, не читают телеметрию реального оборудования, не управляют производственными fixtures и не подтверждают физическое состояние устройства.

## Одиннадцать проектов экосистемы

| Репозиторий | Роль | Текущая зрелость |
|---|---|---|
| [SAMBU](https://github.com/bboroski/SAMBU) | Язык, IDE, моделирование и workflow | Experimental alpha |
| [ToolNG](https://github.com/bboroski/ToolNG) | Диагностика Windows и локальные доказательства | Windows desktop utility |
| [ReaperCripple](https://github.com/bboroski/ReaperCripple) | Embedded BSP, калибровка и производство | Host-tested; target validation required |
| [Kloz](https://github.com/bboroski/Kloz) | Переносной C11 substrate и platform ABI | Host-tested core |
| [CO](https://github.com/bboroski/CO) | Детерминированный жизненный цикл компонентов | Host-tested core |
| [SaintSI](https://github.com/bboroski/SaintSI) | Heartbeat-мониторинг и CRC | Host-tested core |
| [Klipot](https://github.com/bboroski/Klipot) | Каталог, контракты и портал | Static portal |
| [NUN](https://github.com/bboroski/NUN) | Спецификация минимального ядра ОС | Documentation scaffold |
| [NUNLauncher](https://github.com/bboroski/NUNLauncher) | Спецификация bootstrap и handoff | Documentation scaffold |

NUN и NUNLauncher пока не являются загружаемой ОС или загрузчиком: соответствующих реализаций в этих репозиториях нет.

## Локальный запуск

Откройте <code>index.html</code> в современном браузере или запустите локальный сервер:

~~~bash
python -m http.server 8080
~~~

Затем откройте <code>http://localhost:8080</code>. Внешний JavaScript framework или пакет не требуется.

## Публикация и проверки

Портал использует workflow GitHub Pages в <code>.github/workflows/pages.yml</code>. В настройках репозитория необходимо выбрать **Settings → Pages → GitHub Actions**.

~~~bash
python one.py
python one.py check
~~~

Команда проверки валидирует портал, manifests, схемы и JavaScript без открытия браузера.

## Управление экосистемой

1. **Владение доменом:** каждый модуль отвечает за свой код, API, тесты и релиз.
2. **Явные связи:** интеграции используют версионируемые интерфейсы, а не скрытые глобальные переменные.
3. **Доказательства важнее статуса:** observed, not found, unknown, failed и passed различаются.
4. **Ограниченное выполнение:** capacity, ownership, timeout и cleanup документируются явно.
5. **Честная зрелость:** adapter-ready контракт не называется завершённой production-интеграцией.

## Критерии готовности

Host-тест доказывает только переносимые программные инварианты. Проверка целевого компилятора, linker map, board revision, fixtures, происхождения измерений и hardware-in-the-loop — отдельные evidence gates.

Документация:
- [Общий протокол интеграции](docs/INTEGRATION_PROTOCOL.md)
- [Реестр модулей](registry/ecosystem.json)
- [Руководство по UI портала](docs/PORTAL_UI.md)

## Техническая идентичность

**Klipot** — каноническое имя портала и control plane. GitHub-путь и публичный Pages URL являются стабильными адресами проекта.

## Экосистема

[ SAMBU ](https://github.com/bboroski/SAMBU) · [ToolNG](https://github.com/bboroski/ToolNG) · [ReaperCripple](https://github.com/bboroski/ReaperCripple) · [Kloz](https://github.com/bboroski/Kloz) · [CO](https://github.com/bboroski/CO) · [SaintSI](https://github.com/bboroski/SaintSI) · [NUN](https://github.com/bboroski/NUN) · [NUNLauncher](https://github.com/bboroski/NUNLauncher).

## Лицензия

В прежней документации проекта была указана MIT, но отдельного файла LICENSE в репозитории нет. Подтвердите лицензию и добавьте её полный текст до распространения.


## Продуктовая система

Единые правила дизайна Duck, реестра возможностей, трёхъязычной документации, маркетинговых заявлений и релизов: [docs/PRODUCT_SYSTEM.md](docs/PRODUCT_SYSTEM.md). Каталог рассчитан на 10 000 ID; реализованными считаются только возможности с кодом и проверочными тестами.
