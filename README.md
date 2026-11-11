<p align="center"><img src="assets/duck-ui/duck-mark.svg" alt="Klipot mark" width="92"></p>
<h1 align="center">Klipot</h1>
<p align="center"><strong>Ecosystem Integration & Control Plane</strong></p>
<p align="center"><img src="https://img.shields.io/badge/STATUS-STATIC%20PORTAL%20%C2%B7%20HTML%20%2B%20JAVASCRIPT-FFD600?style=for-the-badge&labelColor=111111" alt="Static portal · HTML + JavaScript"></p>
<p align="center"><a href="README.md">🇺🇦 Українська</a> · <a href="README.en.md">🇬🇧 English</a> · <a href="README.ru.md">🇷🇺 Русский</a></p>
<sub>Оновлено: 2026-11-11</sub>



## NEON SYNDICATE — portal visual overview

<p align="center"><img src="assets/neon-syndicate/overview.svg" alt="Klipot NEON SYNDICATE high-resolution vector portal preview" width="1200"></p>
<p align="center"><em>Static vector design preview, not a browser screenshot. The live portal is implemented in index.html.</em></p>

[Brand and interface specification](design/NEON_SYNDICATE.md) · [Design tokens](design/neon-syndicate.tokens.json)

## Поточні можливості
- Каталог репозиторіїв із пошуком і фільтрами.
- Machine-readable registry та versioned integration protocol.
- Browser-labs для локальної демонстрації allocation, lifecycle і capability-gate моделей.
- CI-перевірки метаданих, схем, контрактів і JavaScript.
- Оновлений cross-repository roadmap та quality contracts.

## Швидкий старт і перевірка
```bash
python -m http.server 8080
# open http://localhost:8080
python one.py check
```

## Архітектура, межі та достовірність
Browser-labs використовують локальну модель і synthetic data; вони не запускають native C, не читають hardware telemetry і не керують пристроями. Каталог не перетворює незалежні репозиторії на моноліт.

## Прев'ю порталу

Статичне векторне прев'ю концепції Klipot у стилі NEON SYNDICATE. Це дизайн-макет, а не скриншот запущеного порталу.

<p align="center"><img src="assets/neon-syndicate/overview.svg" alt="Klipot: векторне прев'ю порталу з каталогом репозиторіїв і навігацією" width="960"></p>
<p align="center"><em>Портал, каталог репозиторіїв і швидкі переходи до лабораторій</em></p>

## Інженерна якість
- Перевіряйте збірку й тести саме для цільової платформи; host CI не замінює hardware qualification.
- Статуси **implemented**, **partial**, **planned** мають підтверджуватися кодом, тестами та документацією.
- Не оголошуйте функцію production-ready лише на підставі макета, специфікації чи відкритого Pull Request.
- Зовнішні інтеграції мають бути явними, версіонованими, ізольованими й перевірюваними.

## Карта документації

- [Архітектура порталу](docs/ARCHITECTURE.md)
- [Контракти екосистеми](docs/CONTRACTS.md)
- [Інтеграційний протокол](docs/INTEGRATION_PROTOCOL.md)
- [Інтерфейс порталу](docs/PORTAL_UI.md)

## Ліцензія
Ліцензію не оголошено; файл LICENSE відсутній.

---

## Інженерний стандарт
Індекс аудиту, тестових воріт, безпеки, супроводу та критеріїв інтеграції: [Engineering Improvement Index](docs/ENGINEERING_IMPROVEMENT_INDEX.md).

## Інтеграційні межі
Зберігайте незалежні API, runtime та цикли випуску; інтегруйте через версіоновані контракти. [Hellduck Integration Playbook](https://github.com/bboroski/Hellduck/blob/main/docs/INTEGRATION_PLAYBOOK.md).

---
**「在天愿作比翼鸟，在地愿为连理枝。」**

*«У небі — птахами-нерозлучниками, на землі — гілками одного дерева».*
