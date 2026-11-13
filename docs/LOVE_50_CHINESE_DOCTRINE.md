# LOVE-50 — Chinese maxims as an engineering doctrine

**Version:** 1.0.0  
**Status:** SPECIFIED — policy and repository mappings only; not a claim of runtime conformance  
**Canonical home:** Klipot · SAMBU ecosystem control plane  
**Scope:** all repositories that explicitly adopt this profile

## Intent

This doctrine translates the supplied 50 Chinese-language expressions about fate, fidelity, affection, harmony and wisdom into practical software-engineering behaviours. It is a design and review aid, not sentiment analysis, a product theme, a requirement to add romantic UI, or permission to change a system's authority model.

The collection is mixed: it includes chengyu, folk expressions, classical poetic lines and modern formulations. Item 50 is a Chinese rendering of 1 Corinthians 13:4, not a traditional Chinese folk proverb. The source notes preserve that distinction; no unattributed phrase is assigned a historical author.

## Five engineering domains

| Collection | Engineering interpretation | Quality outcome |
|---|---|---|
| I. Fate (1–10) | Stable identity, explicit contracts, compatibility and traceability | Components connect only through verified interfaces |
| II. Fidelity (11–20) | Backward compatibility, data integrity, lifecycle guarantees and resilience | Promises survive upgrades and partial failure |
| III. Affection (21–30) | Responsiveness, accessible UX, bounded resource use and clear feedback | The product respects time, attention and user context |
| IV. Harmony (31–40) | Module ownership, event semantics, coordinated releases and recovery | Independent components cooperate without hidden coupling |
| V. Wisdom (41–50) | Safety, least privilege, privacy, restraint and maintainability | Changes remain reversible, explainable and supportable |

## The 50 maxims

| # | Chinese | Pinyin | Engineering application | Evidence / acceptance check |
|---:|---|---|---|---|
| 1 | 千里姻缘一线牵 | Qiānlǐ yīnyuán yīxiàn qiān | Стабильные идентификаторы и явные контракты связывают компоненты без жёсткой сцепки. | Проверять интеграцию по публичному интерфейсу, а не по внутренним деталям. |
| 2 | 有缘千里来相会，无缘对面不相逢 | Yǒuyuán qiānlǐ lái xiānghuì, wúyuán duìmiàn bù xiāngféng | Интеграция разрешается только при явном совпадении версии, возможностей и условий. | Несовместимость должна давать понятный отказ, а не случайный fallback. |
| 3 | 百年修得同船渡，千年修得共枕眠 | Bǎinián xiū dé tóng chuán dù, qiānnián xiū dé gòng zhěn mián | Проверять не только вызов API, но и полный жизненный цикл взаимодействующих модулей. | Добавлять интеграционные тесты на запуск, работу, сбой и завершение. |
| 4 | 天作之合 | Tiān zuò zhī hé | Подбирать минимальные интерфейсы под реальные роли компонентов. | Контракты должны быть типизированными, версионированными и документированными. |
| 5 | 在天愿作比翼鸟，在地愿为连理枝 | Zài tiān yuàn zuò bǐyìniǎo, zài dì yuàn wéi liánlǐzhī | Связанные модули развиваются синхронно по совместимой матрице версий. | Проверять совместимость provider/consumer и не сливать независимые runtime. |
| 6 | 缘分天注定 | Yuánfèn tiān zhùdìng | Воспроизводимость важнее случайного autodiscovery: фиксировать версии, конфигурацию и входные условия. | Повторный запуск с теми же входами должен давать сопоставимый результат. |
| 7 | 不是冤家不聚头 | Bù shì yuānjiā bù jùtóu | Коллизии зависимостей, циклы и несовместимые требования должны выявляться явно. | Тестировать конфликтующие версии и исключать молчаливое перезаписывание настроек. |
| 8 | 前世有缘，今生相见 | Qiánshì yǒuyuán, jīnshēng xiāngjiàn | Сохранять происхождение данных, историю изменений и миграционный контекст. | Обеспечить provenance, version metadata и проверяемые миграции. |
| 9 | 红线牵情 | Hóngxiàn qiān qíng | Использовать безопасные correlation IDs для сквозной диагностики. | Один запрос прослеживается между компонентами; идентификаторы не содержат персональных данных. |
| 10 | 门当户对 | Mén dāng hù duì | До интеграции проверять capability matrix, платформу, ABI и ресурсные требования. | Несовпадающие возможности не должны объявляться поддерживаемыми. |
| 11 | 执子之手，与子偕老 | Zhí zǐ zhī shǒu, yǔ zǐ xiélǎo | Сохранять пользовательские и межмодульные обещания на протяжении жизненного цикла продукта. | Изменения публичного API сопровождаются deprecation policy и migration path. |
| 12 | 海枯石烂 | Hǎi kū shí làn | Защищать целостность и восстанавливаемость данных при сбоях. | Тестировать повреждение, частичную запись, восстановление и отказоустойчивость. |
| 13 | 白头偕老 | Báitóu xiélǎo | Проектировать версии и поддержку так, чтобы обновление не ломало существующих пользователей без предупреждения. | Проверять миграции и backward compatibility на поддерживаемых версиях. |
| 14 | 矢志不渝 | Shǐzhì bùyú | Документированные гарантии должны соответствовать реальному поведению кода. | Каждое публичное обещание подкреплено тестом или явно помечено как planned. |
| 15 | 山盟海誓 | Shānméng hǎishì | Надёжность подтверждается проверками, а не лозунгами. | Для критических контрактов использовать регрессионные, негативные и fault-injection тесты. |
| 16 | 一心一意 | Yīxīn yīyì | Избегать конкурирующих источников истины и неоднозначного владения состоянием. | Определить canonical owner для каждой записи, настройки и перехода состояния. |
| 17 | 生死契阔，与子成说 | Shēngsǐ qìkuò, yǔ zǐ chéng shuō | Явно описывать lifecycle, shutdown, rollback и восстановление после частичного отказа. | Покрывать все состояния и переходы, включая interrupted/failed initialization. |
| 18 | 情比金坚 | Qíng bǐ jīn jiān | Проверять целостность, происхождение и границы достоверности данных. | Хеш подтверждает совпадение содержимого, но не подменяет аутентификацию или авторство. |
| 19 | 相濡以沫 | Xiāngrú yǐ mò | Компоненты должны деградировать контролируемо, сохраняя минимально полезную функцию. | При недоступности зависимости выдавать ограниченный результат и план восстановления. |
| 20 | 患难与共 | Huànnàn yǔ gòng | Сбой одного участника не должен бесконтрольно распространяться на всю систему. | Тестировать fault isolation, bounded retries, timeout и rollback. |
| 21 | 一日不见，如隔三秋 | Yī rì bù jiàn, rú gé sān qiū | Уважать latency budget и своевременно сообщать о длительной операции. | Устанавливать измеримые таймауты, progress states и cancellation. |
| 22 | 情人眼里出西施 | Qíngrén yǎnlǐ chū Xīshī | Оценивать удобство глазами разных пользователей, не полагаясь на вкус разработчика. | Проверять доступность, читаемость, локализацию и сценарии реального пользователя. |
| 23 | 爱屋及乌 | Ài wū jí wū | Учитывать реальные edge cases, старые данные и соседние компоненты, а не только идеальный сценарий. | Добавлять тесты на неизвестные, частичные и нестандартные входы. |
| 24 | 心有灵犀一点通 | Xīn yǒu língxī yīdiǎn tōng | Контекст и смысл передачи должны быть явными в API, событиях и ошибках. | Не полагаться на скрытое глобальное состояние или неформальные соглашения. |
| 25 | 两情若是久长时，又岂在朝朝暮暮 | Liǎng qíng ruò shì jiǔcháng shí, yòu qǐ zài zhāozhāo mùmù | Использовать асинхронность и слабую связанность там, где синхронное взаимодействие не нужно. | Компоненты сохраняют корректность при задержке, повторе и временном отсутствии соседа. |
| 26 | 入骨相思知不知 | Rùgǔ xiāngsī zhī bù zhī | Собирать только необходимую диагностику и не путать наблюдаемость с наблюдением за личной жизнью. | Telemetry минимальна, локальна/opt-in там, где уместно, и не включает секреты. |
| 27 | 衣带渐宽终不悔，为伊消得人憔悴 | Yīdài jiàn kuān zhōng bù huǐ, wèi yī xiāo dé rén qiáocuì | Не допускать незаметного истощения памяти, CPU, батареи и других ресурсов. | Использовать профилирование, нагрузочные тесты и проверки утечек. |
| 28 | 问世间情为何物，直教生死相许 | Wèn shìjiān qíng wèi héwù, zhí jiào shēngsǐ xiāngxǔ | Для необратимых действий требовать явного намерения и проверяемых preconditions. | Опасные операции требуют подтверждения, ограниченного scope и recovery plan. |
| 29 | 刻骨铭心 | Kègǔ míngxīn | Сохранять важную историю изменений и аудируемые результаты, не записывая лишние личные данные. | Для значимых операций доступны provenance и понятный audit trail. |
| 30 | 一见钟情 | Yījiàn zhōngqíng | Сделать первый запуск и базовый сценарий ясными с минимальным порогом входа. | Проверять onboarding, sensible defaults и понятную пустую/ошибочную страницу. |
| 31 | 琴瑟和鸣 | Qínsè hémíng | Согласовывать интерфейсы и форматы сообщений на границах модулей. | Интеграционный тест подтверждает совместную работу реальных контрактов. |
| 32 | 举案齐眉 | Jǔ àn qíméi | Уважать ownership модулей, авторов API и границы полномочий. | Не менять чужие контракты и данные без владельца и миграционного плана. |
| 33 | 相敬如宾 | Xiāngjìng rú bīn | Интеграция не должна иметь скрытых побочных эффектов или захватывать чужие ресурсы. | Проверять side effects, permissions и очистку временных ресурсов. |
| 34 | 夫唱妇随 | Fū chàng fù suí | События и callbacks имеют предсказуемый порядок, правила владения и возврата ошибок. | Проверять порядок вызовов, re-entrancy и повторное событие. |
| 35 | 家和万事兴 | Jiā hé wànshì xīng | Собирать локальные quality gates в непрерывный интеграционный процесс. | PR CI проверяет тесты, схемы, форматирование и документацию, когда они затронуты. |
| 36 | 比翼双飞 | Bǐyì shuāngfēi | Согласовывать выпуск связанных компонентов и их матрицу совместимости. | Release artifacts фиксируют версии и доказательства совместимости. |
| 37 | 恩爱夫妻 | Ēn'ài fūqī | Поддерживать понятную политику поддержки и окончания жизненного цикла. | Объявлять deprecation, security support window и владельца сопровождения. |
| 38 | 同甘共苦 | Tónggān gòngkǔ | Интеграционные тесты должны проверять и успех, и отказ соседнего компонента. | Тестировать partial failure, stale data и восстановление. |
| 39 | 床头打架床尾和 | Chuángtóu dǎjià chuángwěi hé | Предусмотреть детерминированное разрешение конфликтов и безопасное повторение операций. | Повторяемая команда не создаёт дубликаты; rollback и retry имеют чёткую семантику. |
| 40 | 嫁鸡随鸡，嫁狗随狗 | Jià jī suí jī, jià gǒu suí gǒu | Миграции и обновления должны учитывать пользователя, оставляя понятный путь возврата. | Предусматривать export, backup и migration notes; не принуждать к скрытому переходу. |
| 41 | 真金不怕火炼，真爱不怕考验 | Zhēnjīn bù pà huǒ liàn, zhēn'ài bù pà kǎoyàn | Проверять систему при нагрузке, некорректных входах и внешних отказах. | Добавлять boundary, stress и fault-injection тесты для критических путей. |
| 42 | 爱之深，责之切 | Ài zhī shēn, zé zhī qiè | Ошибки и review findings должны быть точными, доброжелательными и исправимыми. | Сообщение содержит причину, безопасный следующий шаг и границы уверенности. |
| 43 | 距离产生美 | Jùlí chǎnshēng měi | Использовать модульные границы, least privilege и минимальную передачу данных. | Проверять, что компонент получает только необходимые права и поля. |
| 44 | 宁缺毋滥 | Nìng quē wú làn | Не добавлять зависимости, функции и автоматизацию без доказанной потребности. | Новое усложнение требует задачи, сравнения вариантов и сопровождения. |
| 45 | 得成比目何辞死，愿作鸳鸯不羡仙 | Dé chéng bǐmù hé cí sǐ, yuàn zuò yuānyāng bù xiàn xiān | Использовать резервирование только при независимом fallback и доказанной пользе. | Тестировать отказ основного пути и автономность резервного. |
| 46 | 君子之交淡如水，小人之交甘若醴 | Jūnzǐ zhī jiāo dàn rú shuǐ, xiǎorén zhī jiāo gān ruò lǐ | Держать интерфейсы простыми, прозрачными и свободными от скрытых действий. | Побочные эффекты и сбор данных документируются и проверяются. |
| 47 | 落花有意，流水无情 | Luòhuā yǒuyì, liúshuǐ wúqíng | Не предполагать поддержку или согласие другой системы, если этого не подтверждают факты. | Несовместимость, отказ и отсутствие ответа отображаются как разные состояния. |
| 48 | 天长地久 | Tiāncháng dìjiǔ | Поддерживать сопровождение, обновляемость и понятное владение проектом. | Проверять зависимости, сроки поддержки, документацию и reproducible builds. |
| 49 | 愿得一心人，白首不相离 | Yuàn dé yīxīn rén, báishǒu bù xiānglí | Сохранять стабильные публичные API и заранее сообщать о несовместимых изменениях. | Нужны contract tests, versioning и migration guide. |
| 50 | 爱是恒久忍耐，又有恩慈 | Ài shì héngjiǔ rěnnài, yòu yǒu ēncí | Обеспечивать понятные подсказки, ограниченные повторы, доступность и не обвиняющие сообщения. | Повтор не бесконечен; UX учитывает ошибки и людей с разными возможностями. |

## Adoption rules

1. **Map, do not imitate.** Select only practices relevant to the repository's purpose. A bare-metal library does not need a GUI; a read-only diagnostic tool must not gain repair authority; a kernel does not gain an installer because a metaphor suggests it.
2. **Do not weaken existing guarantees.** Existing safety, privacy, platform, ABI, licensing and release requirements remain authoritative. This doctrine is additive.
3. **Keep capabilities evidence-backed.** Use the repository's existing maturity vocabulary. Documentation alone means SPECIFIED, not IMPLEMENTED or VERIFIED.
4. **Respect ownership.** A shared contract does not merge independent runtimes or authorize writing to another project's state.
5. **Prefer bounded behaviour.** Timeouts, retries, buffers, queues, memory and telemetry need explicit limits where relevant.
6. **Preserve user agency.** Destructive, privileged, external or irreversible actions need explicit scope and confirmation. No silent collection of secrets or personal data.
7. **Make failure humane and technical.** Report the observed condition, uncertainty, safe next step and recovery path without pretending an unknown state is healthy.

## Conformance model

- **NOT_ADOPTED:** no repository-specific mapping exists.
- **SPECIFIED:** a mapping and acceptance checks exist; implementation is not implied.
- **IMPLEMENTED:** code/configuration implements a mapped control.
- **VERIFIED:** relevant automated tests and target-specific evidence pass.
- **ACTIVE:** verified controls are enabled in the intended release/runtime.

Promotion must be supported by repository-local evidence. A green host test does not prove hardware, firmware, kernel, cryptographic identity or production readiness beyond the tested scope.

## Canonical machine-readable source

[`ecosystem/love-50.json`](../ecosystem/love-50.json) contains the 50 supplied expressions, categories, glosses, engineering interpretations and verification checks. [`tests/test_love_50.py`](../tests/test_love_50.py) guards the count, identifiers, group distribution and required fields.

## Security and ethics boundary

LOVE-50 is not an emotional model and must not score, infer or classify a user's feelings, relationships, health or personality. Do not use it to create manipulative engagement, coercive retention, emotional profiling or dark patterns. Care means transparent behaviour, privacy, accessibility, consent, and reliable recovery.

---
*LOVE-50: a metaphor is useful only when it becomes a testable promise.*
