# Klipot — Ecosystem Integration & Control Plane

**Каталог модулів, реєстр контрактів і операторський портал для незалежних інженерних компонентів.**

Klipot пов'язує документацію, реєстри можливостей, версійовані інтеграційні контракти та browser-labs. Він допомагає дослідити архітектуру й межі відповідальності, не зливаючи окремі runtime-компоненти в один нерозрізнений моноліт.

[Українська](README.md) · [English](README.en.md) · [Русский](README.ru.md) · [Репозиторій](https://github.com/bboroski/Klipot) · [Публічний портал](https://bboroski.github.io/Klipot/)
<p align="center"><img src="assets/nun-mesh-overview.svg" alt="Nine-repository integration map" width="100%"></p>

## Дев'ять репозиторіїв

| Репозиторій | Відповідальність | Поточний стан |
|---|---|---|
| [SAMBU](https://github.com/bboroski/SAMBU) | Мова, IDE, Studio та workflow-інструменти | Experimental alpha |
| [ToolNG](https://github.com/bboroski/ToolNG) | Нативна діагностика Windows і локальні звіти доказів | Desktop application |
| [ReaperCripple](https://github.com/bboroski/ReaperCripple) | Embedded BSP, калібрування та виробнича інженерія | Host-tested; target validation required |
| [Kloz](https://github.com/bboroski/Kloz) | C11 platform ABI, пам'ять фіксованої місткості та платформи CPU/board | Host-tested core |
| [CO](https://github.com/bboroski/CO) | Детермінований життєвий цикл компонентів | Host-tested core |
| [SaintSI](https://github.com/bboroski/SaintSI) | Heartbeat-нагляд і перевірка випадкового пошкодження | Host-tested core |
| [Klipot](https://github.com/bboroski/Klipot) | Каталог, контракти та портал інтеграції | Static portal |
| [NUN](https://github.com/bboroski/NUN) | Специфікація мінімального ядра ОС | Documentation scaffold; no kernel implementation |
| [NUNLauncher](https://github.com/bboroski/NUNLauncher) | Специфікація bootstrap і передачі керування ядру | Documentation scaffold; no loader implementation |

NUN і NUNLauncher поки що не є завантажуваною ОС або завантажувачем. Їхні README описують заплановані межі та не заявляють відсутні реалізації як готові функції.

## Можливості порталу

- каталог модулів із фільтрами за доменом і пошуком;
- посилання на вихідний код, GUI-документацію та інструкції запуску;
- копіювання clone-команд;
- machine-readable registry і versioned integration protocol;
- інтерактивні browser-labs для демонстрації allocation, lifecycle, heartbeat і capability-gate концепцій;
- CI-перевірка метаданих, контрактів і синтаксису статичного порталу.

**Browser-labs є симуляціями.** Вони не виконують C-код, не читають телеметрію реального обладнання, не керують виробничими fixtures і не доводять фізичний стан пристрою.

## Локальний запуск

Відкрийте <code>index.html</code> у сучасному браузері. Зовнішній framework або пакет JavaScript не потрібен.

~~~bash
python -m http.server 8080
~~~

Потім відкрийте <code>http://localhost:8080</code>.

## Публікація

Портал публікується через GitHub Pages workflow у <code>.github/workflows/pages.yml</code>. У налаштуваннях репозиторію потрібно один раз вибрати **Settings → Pages → GitHub Actions**. Подальші зміни основної гілки проходять через workflow автоматично.

## Архітектурні правила

1. **Володіння доменом:** кожен модуль володіє своїм кодом, API, тестами та релізом.
2. **Явний зв'язок:** інтеграція йде через версійовані інтерфейси, а не приховані глобальні змінні.
3. **Докази перед статусом:** розрізняються observed, not found, unknown, failed і passed.
4. **Обмежене виконання:** capacity, ownership, timeout і cleanup документуються явно.
5. **Чесна зрілість:** adapter-ready контракт не називається завершеною production-інтеграцією.

## Перевірка та межі

Host-тест доводить лише переносні програмні інваріанти. Перевірка цільового компілятора, linker map, board revision, fixtures, походження вимірювань і hardware-in-the-loop — окремі evidence gates. Klipot показує ці межі, а не скасовує їх.

- [Спільний протокол інтеграції](docs/INTEGRATION_PROTOCOL.md)
- [Реєстр модулів](registry/ecosystem.json)
- [Посібник з UI порталу](docs/PORTAL_UI.md)

## Технічна ідентичність

**Klipot** — канонічна назва порталу й control plane. Поточний GitHub-шлях і публічний Pages URL збережені як стабільні адреси.

## Ліцензія

MIT. Див. [LICENSE](LICENSE).


## Запуск однією командою

- **Windows:** двічі клацніть `one.cmd`; на будь-якій ОС використовуйте `python one.py`.
- `python one.py check` перевіряє портал, маніфести, схеми та JavaScript без відкриття браузера.
- Якщо всі дев'ять репозиторіїв розташовані поруч, mesh-runner додатково запускає `one.py check` кожного модуля та перевіряє міжрепозиторні контракти. Звичайний запуск після перевірки відкриває портал.

## Академический биологический словарь

- [500 академических терминов EN–RU](data/biology/academic_terms_500.tsv)
- [Контракт и правила использования](docs/BIOLOGY_DOMAIN_PACK.md)

Справочный офлайн-набор для обучения и метаданных; он не управляет системами, устройствами и диагностикой.
