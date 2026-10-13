# 📘 База знаний Flutter-разработчика

Материалы для подготовки и саморазвития Flutter-разработчиков: от Git и ООП до собственных RenderObject,
плагинов и FFI. Темы разбиты по грейдам Junior / Middle / Senior, примеры — из мира мобильного банкинга
(счета, карты, платежи).

## Для кого

| Твой грейд | Как пользоваться |
|------------|------------------|
| ⭐ Junior | Начни с тем ⭐ во всех разделах, затем переходи к ⭐⭐ |
| ⭐⭐ Middle | Закрой пробелы в ⭐ и ⭐⭐, затем изучи теорию тем ⭐⭐⭐ |
| ⭐⭐⭐ Senior | Освежи знания: пройди «Самопроверку» и прочитай ресурсы уровня ⭐⭐⭐ |

## Что значат грейды тем

- ⭐ — Junior должен **применять на практике**
- ⭐⭐ — Middle должен **применять на практике**, Junior — знать теорию
- ⭐⭐⭐ — Senior должен **применять на практике**, Middle — знать теорию

## Разделы

Разделы стоят в рекомендуемом порядке изучения.

1. [Базовые знания разработчика](01-developer-fundamentals/_index.md)
2. [Dart](02-dart/_index.md)
3. [Flutter](03-flutter/_index.md)
4. [Архитектура](04-architecture/_index.md)
5. [Нативная разработка](05-native/_index.md)
6. [Качество и безопасность](06-quality-and-security/_index.md) — дополнение к основным темам

## Устройство каждой страницы

1. **📚 Ресурсы** — лучшие материалы по теме без воды, сначала на русском
2. **🎓 Лекция** — теория с примерами на банковском домене (счета, карты, платежи), диаграммы, частые ошибки,
   задачи с собеседования
3. **✅ Самопроверка** — вопросы по уровням Junior / Middle / Senior с ответами, чтобы понять, что тема закрыта

---

## 🛠 О репозитории

Исходники базы знаний в Markdown. Отсюда страницы переносятся в Confluence, а на GitHub их можно читать
как есть: ссылки между разделами и диаграммы работают.

### Статус

| Раздел | Готово |
|--------|--------|
| 01 Базовые знания разработчика | ✅ 8 / 8 |
| 02 Dart | ✅ 6 / 6 |
| 03 Flutter | ✅ 10 / 10 |
| 04 Архитектура | ✅ 7 / 7 |
| 05 Нативная разработка | ✅ 9 / 9 |
| 06 Качество и безопасность | 3 / 12, в работе |

Основные разделы 01–05 готовы.

### Оглавление

**01. [Базовые знания разработчика](01-developer-fundamentals/_index.md)**

| Тема | Грейд |
|------|-------|
| [GIT](01-developer-fundamentals/01-git.md) | ⭐ |
| [ООП](01-developer-fundamentals/02-oop.md) | ⭐ |
| [SOLID / DRY / KISS / YAGNI](01-developer-fundamentals/03-solid-dry-kiss.md) | ⭐⭐ |
| [Паттерны проектирования](01-developer-fundamentals/04-design-patterns.md) | ⭐⭐ |
| [Оценка сложности вычислений](01-developer-fundamentals/05-algorithmic-complexity.md) | ⭐ |
| [Сетевые протоколы](01-developer-fundamentals/06-network-protocols.md) | ⭐ |
| [Парадигмы программирования](01-developer-fundamentals/07-programming-paradigms.md) | ⭐⭐⭐ |
| [Проектирование API](01-developer-fundamentals/08-api-design.md) | ⭐⭐⭐ |

**02. [Dart](02-dart/_index.md)**

| Тема | Грейд |
|------|-------|
| [Основы синтаксиса и коллекции](02-dart/01-syntax.md) | ⭐ |
| [Event Loop](02-dart/02-event-loop.md) | ⭐⭐ |
| [Streams](02-dart/03-streams.md) | ⭐⭐ |
| [Расширенные возможности типизации](02-dart/04-type-system.md) | ⭐⭐ |
| [Изоляты](02-dart/05-isolates.md) | ⭐⭐⭐ |
| [Кодогенерация](02-dart/06-code-generation.md) | ⭐⭐⭐ |

**03. [Flutter](03-flutter/_index.md)**

| Тема | Грейд |
|------|-------|
| [Виджеты, элементы, контекст](03-flutter/01-widgets-elements-context.md) | ⭐ |
| [Стандартные виджеты](03-flutter/02-standard-widgets.md) | ⭐ |
| [Навигация](03-flutter/03-navigation.md) | ⭐ |
| [Локальное хранение данных](03-flutter/04-local-storage.md) | ⭐⭐ |
| [Анимации](03-flutter/05-animations.md) | ⭐⭐ |
| [Инструменты отладки (DevTools)](03-flutter/06-devtools.md) | ⭐⭐ |
| [Flutter под капотом](03-flutter/07-under-the-hood.md) | ⭐⭐ |
| [Собственные RenderObject](03-flutter/08-custom-render-object.md) | ⭐⭐⭐ |
| [Производительность и профилирование](03-flutter/09-performance.md) | ⭐⭐⭐ |
| [Компиляция (AOT/JIT, сборка)](03-flutter/10-compilation.md) | ⭐⭐⭐ |

**04. [Архитектура](04-architecture/_index.md)**

| Тема | Грейд |
|------|-------|
| [Слои приложения](04-architecture/01-app-layers.md) | ⭐ |
| [Паттерн Repository](04-architecture/02-repository.md) | ⭐ |
| [Паттерны презентационного слоя (BLoC, MVVM…)](04-architecture/03-presentation-patterns.md) | ⭐⭐ |
| [Внедрение зависимостей (DI)](04-architecture/04-dependency-injection.md) | ⭐⭐ |
| [Многомодульность](04-architecture/05-multimodularity.md) | ⭐⭐⭐ |
| [Технический долг и рефакторинг](04-architecture/06-tech-debt-refactoring.md) | ⭐⭐⭐ |
| [Архитектура с нуля](04-architecture/07-architecture-from-scratch.md) | ⭐⭐⭐ |

**05. [Нативная разработка](05-native/_index.md)**

| Тема | Грейд |
|------|-------|
| [Различия Android / iOS](05-native/01-android-vs-ios.md) | ⭐ |
| [Настройка нативных проектов](05-native/02-native-project-setup.md) | ⭐ |
| [Platform Channels](05-native/03-platform-channels.md) | ⭐⭐ |
| [Нативные API Android](05-native/04-android-native-api.md) | ⭐⭐ |
| [Нативные API iOS](05-native/05-ios-native-api.md) | ⭐⭐ |
| [Разработка плагинов](05-native/06-plugin-development.md) | ⭐⭐ |
| [Java / Kotlin](05-native/07-kotlin-java.md) | ⭐⭐⭐ |
| [Swift](05-native/08-swift.md) | ⭐⭐⭐ |
| [Работа с FFI](05-native/09-ffi.md) | ⭐⭐⭐ |

**06. [Качество и безопасность](06-quality-and-security/_index.md)** — дополнение, полный список тем — на странице раздела

| Тема | Грейд |
|------|-------|
| [Стратегия тестирования и unit-тесты](06-quality-and-security/01-testing-strategy-unit.md) | ⭐ |
| [Widget- и golden-тесты](06-quality-and-security/02-widget-golden-tests.md) | ⭐⭐ |
| [Интеграционные и E2E-тесты](06-quality-and-security/03-integration-e2e-tests.md) | ⭐⭐ |

### Как сделаны материалы

- **Код проверен запусками.** Примеры собираются в отдельных проектах на актуальном стабильном Flutter
  и прогоняются: `dart analyze` / `flutter analyze`, тесты, эмулятор Android, симулятор iOS, Android Lint для
  нативного кода. Выводы программ и тексты ошибок на страницах взяты из реальных запусков.
- **Ресурсы проверены.** Ссылки открывались и читались по содержанию, описание в таблице ресурсов соответствует
  материалу.
- **Диаграммы — Mermaid.** Исходник `.mmd` и отрендеренный PNG лежат рядом, в папке `diagrams/` раздела.

### Структура

```text
NN-раздел/
├── _index.md            — страница раздела: как проходить, список тем
├── NN-тема.md           — страница темы
└── diagrams/
    ├── NN-тема--имя.mmd — исходник диаграммы (Mermaid)
    └── NN-тема--имя.png — картинка для страницы
_templates/              — шаблон страницы темы
_prototypes/             — прототипы кода для будущих тем
tools/                   — рендер диаграмм и конвертер в Confluence
scriprts_use.md          — инструкция к скриптам
```

### Перенос в Confluence и диаграммы

```bash
cd tools && npm install && cd ..   # один раз: Mermaid CLI для рендера диаграмм
tools/render-diagrams.sh           # .mmd → .png (только новые и изменённые)
python3 tools/md2confluence.py     # Markdown → Confluence Wiki Markup в _build/confluence/
```

В Confluence: **Insert markup** (Cmd/Ctrl+Shift+D) → **Confluence Wiki** → вставить текст из `_build/confluence/…/*.txt`,
затем загрузить PNG этой страницы во вложения. Подробно — в [scriprts_use.md](scriprts_use.md).
