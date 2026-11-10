<p align="center"><img src="assets/duck-ui/duck-mark.svg" alt="Klipot mark" width="92"></p>
<h1 align="center">Klipot</h1>
<p align="center"><strong>Ecosystem Integration &amp; Control Plane</strong></p>
<p align="center"><img src="https://img.shields.io/badge/STATUS-STATIC%20PORTAL-FFD600?style=for-the-badge&labelColor=111111"><img src="https://img.shields.io/badge/CORE-HTML%20%2B%20JS-FFD600?style=for-the-badge&labelColor=111111"><img src="https://img.shields.io/badge/LICENSE-NOT%20DECLARED-FFD600?style=for-the-badge&labelColor=111111"></p>
<p align="center"><a href="README.md">🇺🇦 Українська</a> · <a href="README.en.md">🇬🇧 English</a> · <a href="README.ru.md">🇷🇺 Русский</a></p>

---

**Klipot — центральний каталог і контрольна площина інженерної екосистеми.** Він показує модулі, межі відповідальності, інтеграційні контракти й точки входу в документацію, не зливаючи незалежні runtime в один моноліт.

## Можливості порталу

- Каталог модулів із фільтрами за доменом і пошуком.
- Посилання на вихідний код, GUI-документацію та інструкції запуску.
- Копіювання команд clone.
- Machine-readable registry та versioned integration protocol.
- Browser-labs для демонстрації allocation, lifecycle, heartbeat і capability-gate моделей.
- CI-перевірка метаданих, контрактів, схем і синтаксису статичного порталу.

**Межа симуляції:** browser-labs не виконують C-код, не читають телеметрію обладнання, не керують fixtures і не доводять фізичний стан пристрою.

## Карта екосистеми

| Репозиторій | Роль | Поточний статус |
|---|---|---|
| [SAMBU](https://github.com/bboroski/SAMBU) | Мова, IDE, modeling і workflow | Experimental alpha |
| [ToolNG](https://github.com/bboroski/ToolNG) | Локальна діагностика Windows | Windows desktop utility |
| [ReaperCripple](https://github.com/bboroski/ReaperCripple) | Embedded bring-up та manufacturing lifecycle | Host-tested; target qualification окремо |
| [Kloz](https://github.com/bboroski/Kloz) | Bare-metal C11 substrate та platform ABI | Host-tested core |
| [CO](https://github.com/bboroski/CO) | Життєвий цикл компонентів | Host-tested core |
| [SaintSI](https://github.com/bboroski/SaintSI) | Heartbeat-нагляд і CRC | Host-tested core |
| [Klipot](https://github.com/bboroski/Klipot) | Каталог і control plane | Static portal |
| [NUN](https://github.com/bboroski/NUN) | Специфікація мінімального ядра ОС | Specification only |
| [NUNLauncher](https://github.com/bboroski/NUNLauncher) | Специфікація bootstrap і handoff | Specification only |
| [Fragile-Baby](https://github.com/bboroski/Fragile-Baby) | Архітектурний напрям Elbrus/E2K | Proposal; target evidence pending |
| [Luci](https://github.com/bboroski/Luci) | Developer workspace/tooling direction | Product/runtime contract pending |

## Локальний запуск

Відкрийте <code>index.html</code> у браузері або запустіть локальний сервер:

~~~bash
python -m http.server 8080
~~~

Перейдіть на <code>http://localhost:8080</code>. Зовнішній framework або пакет JavaScript не потрібен.

## Публікація та перевірки

Workflow публікації: <code>.github/workflows/pages.yml</code>. Для GitHub Pages потрібно вибрати **Settings → Pages → GitHub Actions**.

~~~bash
python one.py
python one.py check
~~~

Перевірка охоплює портал, маніфести, схеми та JavaScript; вона не є підтвердженням коректності кожного зовнішнього репозиторію.

## Системне управління

1. **Володіння доменом:** кожен модуль відповідає за власний код, API, тести та реліз.
2. **Явні зв'язки:** інтеграції проходять через версіоновані контракти.
3. **Докази перед статусом:** passed, observed, not found, unknown і failed не змішуються.
4. **Обмежене виконання:** capacity, ownership, timeout і cleanup описуються явно.
5. **Чесна зрілість:** host-тест не підміняє emulator або hardware qualification.

Документація: [Integration Protocol](docs/INTEGRATION_PROTOCOL.md) · [Ecosystem Registry](registry/ecosystem.json) · [Portal UI](docs/PORTAL_UI.md).

## Ліцензія

Файл <code>LICENSE</code> відсутній; ліцензію не оголошено. Визначте умови використання перед публічним розповсюдженням.

---

**Створено з любов'ю до системності, відкритої інженерії та людей.**