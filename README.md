<p align="center"><img src="assets/duck-ui/duck-mark.svg" alt="Duck mark" width="104" /></p>
<h1 align="center">Klipot</h1>
<p align="center"><strong>Ecosystem Integration & Control Plane</strong></p>
<p align="center"><img src="https://img.shields.io/badge/STATUS-STATIC%20PORTAL-FFD600?style=for-the-badge&labelColor=111111" /><img src="https://img.shields.io/badge/CORE-HTML%20%2B%20JS-FFD600?style=for-the-badge&labelColor=111111" /><img src="https://img.shields.io/badge/LICENSE-TEXT%20MISSING-FFD600?style=for-the-badge&labelColor=111111" /></p>
<p align="center"><a href="README.md">🇺🇦 Українська</a> · <a href="README.en.md">🇬🇧 English</a> · <a href="README.ru.md">🇷🇺 Русский</a></p>
<hr />

**Єдина карта інженерної екосистеми: модулі, контракти, документація та операторський портал — без штучного злиття незалежних runtime.**

## Продуктова роль

Klipot допомагає командам бачити, як пов'язані компоненти, хто володіє кожною зоною відповідальності та які інтеграційні контракти вже описані. Це каталог і control plane для прозорої координації, а не прихований моноліт.

## Що надає портал

- Каталог модулів із фільтрами за доменом і пошуком.
- Посилання на вихідний код, GUI-документацію та інструкції запуску.
- Копіювання clone-команд.
- Machine-readable registry та versioned integration protocol.
- Browser-labs для демонстрації allocation, lifecycle, heartbeat і capability-gate концепцій.
- CI-перевірку метаданих, контрактів, схем і синтаксису статичного порталу.

**Важливо:** browser-labs є симуляціями. Вони не виконують C-код, не читають телеметрію реального обладнання, не керують виробничими fixtures і не доводять фізичний стан пристрою.

## Дев'ять проєктів екосистеми

| Репозиторій | Роль | Поточна зрілість |
|---|---|---|
| [SAMBU](https://github.com/bboroski/SAMBU) | Мова, IDE, modeling і workflow | Experimental alpha |
| [ToolNG](https://github.com/bboroski/ToolNG) | Windows-діагностика та локальні докази | Windows desktop utility |
| [ReaperCripple](https://github.com/bboroski/ReaperCripple) | Embedded BSP, калібрування й виробництво | Host-tested; target validation required |
| [Kloz](https://github.com/bboroski/Kloz) | Переносний C11 substrate та platform ABI | Host-tested core |
| [CO](https://github.com/bboroski/CO) | Детермінований життєвий цикл компонентів | Host-tested core |
| [SaintSI](https://github.com/bboroski/SaintSI) | Heartbeat-нагляд і CRC | Host-tested core |
| [Klipot](https://github.com/bboroski/Klipot) | Каталог, контракти та портал | Static portal |
| [NUN](https://github.com/bboroski/NUN) | Специфікація мінімального ядра ОС | Documentation scaffold |
| [NUNLauncher](https://github.com/bboroski/NUNLauncher) | Специфікація bootstrap і handoff | Documentation scaffold |
| [Fragile-Baby](https://github.com/bboroski/Fragile-Baby) | Робочий напрям підтримки архітектури Ельбрус | Proposal; toolchain і target evidence потрібні |
| [Luci](https://github.com/bboroski/Luci) | Каркас програмістського workspace/tooling | Documentation scaffold; runtime contract не визначений |

NUN і NUNLauncher наразі не є завантажуваною ОС або завантажувачем: у цих репозиторіях ще немає відповідних реалізацій.

## Локальний запуск

Відкрийте <code>index.html</code> у сучасному браузері або запустіть локальний сервер:

~~~bash
python -m http.server 8080
~~~

Потім відкрийте <code>http://localhost:8080</code>. Зовнішній framework чи пакет JavaScript не потрібен.

## Публікація та перевірки

Портал використовує GitHub Pages workflow у <code>.github/workflows/pages.yml</code>. У налаштуваннях репозиторію має бути вибрано **Settings → Pages → GitHub Actions**.

~~~bash
python one.py
python one.py check
~~~

Перевірка не відкриває браузер: вона перевіряє портал, маніфести, схеми та JavaScript.

## Управління екосистемою

1. **Володіння доменом:** кожен модуль володіє своїм кодом, API, тестами та релізом.
2. **Явний зв'язок:** інтеграції проходять через версійовані інтерфейси, а не приховані глобальні змінні.
3. **Докази перед статусом:** відрізняються observed, not found, unknown, failed і passed.
4. **Обмежене виконання:** capacity, ownership, timeout і cleanup документуються явно.
5. **Чесна зрілість:** adapter-ready контракт не називається завершеною production-інтеграцією.

## Критерії готовності

Host-тест доводить лише переносні програмні інваріанти. Перевірка цільового компілятора, linker map, board revision, fixtures, походження вимірювань і hardware-in-the-loop — окремі evidence gates.

Документація:
- [Спільний протокол інтеграції](docs/INTEGRATION_PROTOCOL.md)
- [Реєстр модулів](registry/ecosystem.json)
- [Посібник з UI порталу](docs/PORTAL_UI.md)

## Технічна ідентичність

**Klipot** — канонічна назва порталу й control plane. GitHub-шлях і публічний Pages URL є стабільними адресами проєкту.

## Екосистема

[ SAMBU ](https://github.com/bboroski/SAMBU) · [ToolNG](https://github.com/bboroski/ToolNG) · [ReaperCripple](https://github.com/bboroski/ReaperCripple) · [Kloz](https://github.com/bboroski/Kloz) · [CO](https://github.com/bboroski/CO) · [SaintSI](https://github.com/bboroski/SaintSI) · [NUN](https://github.com/bboroski/NUN) · [NUNLauncher](https://github.com/bboroski/NUNLauncher).

## Ліцензія

Проєктна документація раніше заявляла MIT, але окремого файлу LICENSE у репозиторії немає. Підтвердіть ліцензію та додайте її повний текст перед розповсюдженням.


## Reaper-inspired engineering integration

- [Project-specific architecture mapping](docs/REAPER_DOMAIN_INTEGRATION.md)
- [Canonical 50-pattern catalogue in SAMBU](https://github.com/bboroski/SAMBU/blob/main/data/reaper/engineering_patterns_50.tsv)

## Closed-domain metric and boundary model

- [Project-specific boundary and invariant mapping](docs/CLOSED_DOMAIN_METRIC_INTEGRATION.md)
- [Canonical CDM-1 specification and validator](https://github.com/bboroski/SAMBU/blob/main/docs/CLOSED_DOMAIN_METRIC.md)


## Продуктова система та реєстр можливостей

Єдині правила дизайну Duck, тримовної документації, маркетингових заяв, пріоритетів, життєвого циклу функцій і випусків: [docs/PRODUCT_SYSTEM.md](docs/PRODUCT_SYSTEM.md). Каталог допускає до 10 000 ідентифікаторів можливостей; реалізованими вважаються лише функції з кодом, критеріями приймання та перевірними тестами.
