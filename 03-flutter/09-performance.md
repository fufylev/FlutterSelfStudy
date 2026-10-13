# Производительность и профилирование

| Грейд | Время на изучение | Статус |
|-------|-------------------|--------|
| ⭐⭐⭐ | ~35 мин лекция + практика | ✅ Готово |

---

## 📚 Ресурсы

| Ресурс | Формат | Язык | Уровень | Зачем читать |
|--------|--------|------|---------|--------------|
| [Как улучшить производительность вашего Flutter приложения](https://habr.com/ru/articles/502882/) | Статья (Habr, перевод) | 🇷🇺 | ⭐⭐ | Шесть базовых приёмов: отдельные виджеты вместо методов, `const`, `itemExtent`, `child` у `AnimatedBuilder`, замена `Opacity`. Статья 2020 года, но приёмы актуальны |
| [Оптимизация Flutter-приложения: списки, build() и утечки памяти](https://habr.com/ru/companies/friflex/articles/1018320/) | Статья (Habr) | 🇷🇺 | ⭐⭐ | Списки, стоимость `build`, источники утечек |
| [Flutter: Performance best practices](https://docs.flutter.dev/perf/best-practices) | Документация | 🇬🇧 | ⭐⭐ → ⭐⭐⭐ | Официальный список: стоимость `build`, `saveLayer`, прозрачность и обрезка, ленивые списки, intrinsic-проходы |
| [Flutter: Measure performance with an integration test](https://docs.flutter.dev/cookbook/testing/integration/profiling) | Документация | 🇬🇧 | ⭐⭐⭐ | Бенчмарк прокрутки и сводка по кадрам — основа для проверки в CI |
| [Flutter: Performance metrics](https://docs.flutter.dev/perf/metrics) | Документация | 🇬🇧 | ⭐⭐⭐ | Какие метрики считает команда Flutter: время до первого кадра, перцентили времени кадра |

---

## 🎓 Лекция

> ℹ️ **Важно:** как измерять — в теме «Инструменты отладки (DevTools)», как устроены кадр, слои и Impeller — в теме
> «Flutter под капотом». Здесь — что именно оптимизировать и насколько это помогает. Все цифры на странице — из замеров.

### 1. Карта проблем

| Проблема | Симптом у пользователя | Где видно | Раздел |
|----------|------------------------|-----------|--------|
| Jank | Рывки при прокрутке и анимациях | Performance: красные кадры UI или Raster | 2–6 |
| Память | Приложение тормозит со временем, падает, ОС выгружает его в фоне | Memory: рост кучи и Native, Highlight Oversized Images | 7 |
| Старт | Долгий белый или splash-экран | `--trace-startup`, аналитика времени старта | 8 |
| Регрессия | «Раньше было быстрее» | Бенчмарк в CI | 9 |

### 2. Jank: откуда берутся рывки

Кадр нужно подготовить за **16 мс** при 60 Гц и за **8 мс** при 120 Гц. Причины опоздания делятся по этапам:

| Вид | Поток | Типичные причины |
|-----|-------|------------------|
| **Build** | UI | `setState` высоко в дереве, тяжёлая работа в `build` (сортировка, форматирование, разбор), нет `const`, подписка на весь объект состояния вместо нужного поля |
| **Layout** | UI | Intrinsic-проходы (`IntrinsicHeight`, `IntrinsicWidth`, таблицы с выравниванием по самой широкой ячейке), `shrinkWrap` у длинных списков, глубокая вложенность |
| **Raster** | Raster | `saveLayer` — отрисовка во временный буфер: `ShaderMask`, `ColorFilter`, `Opacity` над группой детей, `Clip.antiAliasWithSaveLayer`; размытие (`BackdropFilter`); тени; огромные картинки |
| **Компиляция шейдеров** | Raster | Первая анимация с новым эффектом дёргается. С Impeller (iOS, Android API 29+) этой проблемы нет: шейдеры скомпилированы заранее. Старый способ — прогрев шейдеров SkSL (`--cache-sksl`) — с Impeller не работает и нужен только там, где Flutter рисует через Skia |
| **Работа между кадрами** | UI | Разбор JSON после `await`, синхронное чтение файлов, тяжёлые обработчики. Кадр не может начаться (vsync overhead) — подробно в теме DevTools |

> 💡 **Совет:** сначала определи поток по графику кадров, потом выбирай раздел ниже. `RepaintBoundary` не спасёт
> медленный `build`, а `const` не поможет медленной растеризации.

### 3. `const` и снижение перестроений

**Что на самом деле делает `const`.** `const`-конструктор создаёт объект при компиляции, и одинаковые `const`-выражения —
это **один и тот же объект**. При перестроении родителя Flutter сравнивает старый и новый виджет: если это тот же объект
(`identical`), элемент ребёнка не обновляется и его `build` не вызывается — поддерево пропускается целиком.

```dart
import 'package:flutter/material.dart';

/// Значок тарифа: не зависит от состояния экрана
class PremiumBadge extends StatelessWidget {
  const PremiumBadge({super.key});

  @override
  Widget build(BuildContext context) => const Chip(label: Text('Премиум'));
}

class ProfileHeader extends StatefulWidget {
  const ProfileHeader({super.key});

  @override
  State<ProfileHeader> createState() => _ProfileHeaderState();
}

class _ProfileHeaderState extends State<ProfileHeader> {
  var _balance = 0;

  /// Каждое пополнение перестраивает шапку
  void topUp(int rubles) => setState(() => _balance += rubles);

  @override
  Widget build(BuildContext context) => Column(
        children: [
          Text('Баланс: $_balance ₽'),
          // С const этот виджет не строится заново при каждом setState
          const PremiumBadge(),
        ],
      );
}
```

Замер (виджет-тест, 10 вызовов `setState` у родителя, считаем вызовы `build` у значка):

```text
без const: Badge.build вызван 11 раз
const: Badge.build вызван 1 раз
```

Остальные приёмы:
- **Держи состояние ниже.** `setState` перестраивает всё поддерево своего виджета. Таймер, курс, счётчик — в отдельный
  маленький виджет (пример с лентой операций — в теме DevTools).
- **Отдельный виджет, а не метод.** `Widget _buildHeader()` выполняется при каждом `build` родителя. Отдельный
  `StatelessWidget` можно сделать `const`, и у него свой элемент: Flutter может пропустить его перестроение.
- **Параметр `child` у builder-ов.** `AnimatedBuilder`, `ListenableBuilder`, `ValueListenableBuilder`:
  всё, что не зависит от значения, передаётся в `child` и строится один раз. У `StreamBuilder` и `FutureBuilder`
  параметра `child` нет — неизменную часть выносят в отдельный `const`-виджет.
- **Подписка на нужное поле, а не на весь объект.** `context.select((Cart c) => c.total)` в provider,
  `BlocSelector` в bloc, `ValueListenableBuilder` на конкретный `ValueNotifier`.
- **Линтеры.** `prefer_const_constructors`, `prefer_const_literals_to_create_immutables` подсказывают, где можно
  поставить `const`.

> ⚠️ **Внимание:** не переопределяй `operator ==` у виджетов «для оптимизации»: документация Flutter предупреждает,
> что это даёт квадратичную сложность при сравнении деревьев и замедляет всё приложение.

### 4. `RepaintBoundary`

`RepaintBoundary` выделяет поддерево в свой слой (тема «Flutter под капотом»). Перерисовка внутри не задевает соседей,
и наоборот.

```dart
import 'package:flutter/material.dart';

/// Экран аналитики: большой статичный график и маленький индикатор загрузки рядом
class AnalyticsScreen extends StatelessWidget {
  const AnalyticsScreen({super.key, required this.chart});

  final CustomPainter chart;

  @override
  Widget build(BuildContext context) => Column(
        children: [
          CustomPaint(size: const Size(300, 300), painter: chart),
          // Индикатор перерисовывается 60 раз в секунду. Без границы вместе с ним перерисовывается график
          const RepaintBoundary(child: CircularProgressIndicator()),
        ],
      );
}
```

Замер (виджет-тест, анимированный индикатор рядом с графиком, считаем вызовы `paint` у графика):

```text
Без RepaintBoundary: график перерисован 60 раз за 60 кадров
С RepaintBoundary: график перерисован 0 раз за 60 кадров
```

**Когда ставить:**
- маленькая часть экрана меняется часто, а остальное — нет: индикаторы, таймеры, анимированные иконки, видео;
- сложная статичная отрисовка (график, карта) рядом с чем-то анимированным — граница вокруг **любой** из частей.

**Когда не ставить:**
- вокруг всего подряд — каждый слой стоит памяти и работы на композицию;
- вокруг того, что меняется вместе с соседями: граница ничего не отсекает, а слой добавляется;
- в элементах `ListView`, `GridView` — там границы уже стоят (`addRepaintBoundaries: true`).

Проверить эффект: Highlight Repaints в DevTools — рамка вокруг перерисованных областей меняет цвет.

### 5. Дорогие эффекты и их замена

| Дорого | Почему | Дешевле |
|--------|--------|---------|
| `Opacity` в анимации | Виджет перестраивается на каждом кадре, дети перерисовываются | `FadeTransition` или `AnimatedOpacity`: меняется только прозрачность слоя, дети нарисованы один раз |
| `Opacity` вокруг простой фигуры или картинки | Лишний слой | Цвет с прозрачностью (`color.withValues(alpha: …)`), `Image(opacity: animation)` |
| `Opacity(opacity: 0)` чтобы скрыть | Ребёнок не рисуется, но продолжает строиться, раскладываться и занимать место | `Visibility(visible: false)` или не строить виджет совсем |
| `ClipRRect` вокруг карточки ради скруглённых углов | Обрезка всего содержимого | `BoxDecoration(borderRadius: …)`; обрезку — только где без неё содержимое вылезает |
| `Clip.antiAliasWithSaveLayer` | `saveLayer` | `Clip.antiAlias` (гладкие края без слоя) или `Clip.hardEdge` (самый дешёвый) |
| Обрезка в анимации | Пересчёт обрезки на каждом кадре | Обрезать картинку заранее, анимировать готовую |
| `BackdropFilter` (размытие) на весь экран | Размытие всего, что под ним, на каждом кадре | Ограничить область (`ClipRect` вокруг), статичный размытый фон картинкой |
| `ShaderMask`, `ColorFilter` над большими поддеревьями | `saveLayer` | Применять к картинке (`Image(color:, colorBlendMode:)`), уменьшить область |
| Тени с большим размытием на десятках элементов списка | Дорогая растеризация | Меньше размытие, тень картинкой, `elevation` только у ключевых элементов |

### 6. Списки

Ленивость и вред `shrinkWrap` разобраны в теме «Стандартные виджеты». Дополнительно:
- **`itemExtent` или `prototypeItem`.** Если высота строки известна, список не раскладывает каждую строку, чтобы узнать
  её высоту: быстрее прокрутка и мгновенный переход в конец (`jumpTo`).

```dart
import 'package:flutter/material.dart';

/// Выписка: 1000 операций в ленивом списке
class StatementApp extends StatelessWidget {
  const StatementApp({super.key});

  @override
  Widget build(BuildContext context) => MaterialApp(
        home: Scaffold(
          appBar: AppBar(title: const Text('Выписка')),
          body: ListView.builder(
            key: const ValueKey('statement'),
            itemCount: 1000,
            itemExtent: 56,
            itemBuilder: (context, index) => ListTile(
              key: ValueKey('operation_$index'),
              title: Text('Операция $index'),
              trailing: Text('−${index * 10} ₽'),
            ),
          ),
        ),
      );
}
```

- **`cacheExtent`** — сколько пикселей строить за краем экрана. Больше — плавнее быстрая прокрутка, но больше работы и памяти.
- **`addAutomaticKeepAlives`** и `AutomaticKeepAliveClientMixin` — сохранять состояние строк, ушедших с экрана,
  только там, где это нужно (поле ввода в строке), иначе память растёт.
- **Ключи** у строк, которые переставляются или удаляются, — чтобы состояние не «переезжало» на соседей.
- **Без тяжёлой работы в `itemBuilder`**: форматирование дат и сумм — заранее, в модели.

### 7. Изображения и память

**Сколько весит картинка в памяти.** Сжатый файл (PNG, JPEG) декодируется в пиксели: **ширина × высота × 4 байта**
(красный, зелёный, синий, прозрачность). Размер файла не важен — важно разрешение.

Фото с камеры 4000×3000, показанное аватаром 80×60, — замер `imageCache.currentSizeBytes` в виджет-тесте:

```text
cacheWidth=null: imageCache.currentSizeBytes=48000000 (45.8 МБ)
cacheWidth=160: imageCache.currentSizeBytes=76800 (0.1 МБ)
```

Без подсказки движок декодирует фото целиком: **48 МБ ради аватара**. Десяток таких в ленте — и приложение
под угрозой выгрузки системой. С `cacheWidth` картинка декодируется сразу в нужном размере: 160×120×4 = 76 800 байт.

```dart
import 'package:flutter/material.dart';

/// Аватар получателя: декодируем ровно под размер на экране с учётом плотности пикселей
class RecipientAvatar extends StatelessWidget {
  const RecipientAvatar({super.key, required this.url, this.size = 48});

  final String url;
  final double size;

  @override
  Widget build(BuildContext context) {
    final pixels = (size * MediaQuery.devicePixelRatioOf(context)).round();
    return ClipOval(
      child: Image.network(
        url,
        width: size,
        height: size,
        fit: BoxFit.cover,
        // Достаточно одной стороны: вторая посчитается с сохранением пропорций
        cacheWidth: pixels,
      ),
    );
  }
}
```

Остальное про картинки:
- **`ResizeImage(provider, width: …)`** — то же для любого `ImageProvider`, например, в `DecorationImage`.
- **`imageCache`** — кеш декодированных картинок в памяти. По умолчанию до 1000 картинок и до 100 МБ
  (`maximumSize`, `maximumSizeBytes`). Для приложения с тяжёлыми галереями лимиты можно уменьшить при старте.
- **Сетевые картинки** кешируются в памяти, но не на диске. Дисковый кеш — пакет `cached_network_image`
  (у него тоже есть `memCacheWidth`).
- **`precacheImage`** — заранее загрузить картинку следующего экрана, чтобы она не появлялась с задержкой.
- **Формат и размер на сервере.** Отдавать превью нужного размера и WebP дешевле, чем уменьшать на телефоне.
- **Проверка:** Highlight Oversized Images в DevTools переворачивает картинки, декодированные крупнее, чем показаны;
  вкладка Memory — рост Dart/Flutter Native.
- **Свои `ui.Image`** (из `toImage`, `decodeImageFromList`) освобождаются вручную: `image.dispose()`.

### 8. Старт приложения

| Вид старта | Что происходит | Что ускорять |
|------------|----------------|--------------|
| **Холодный** | Процесса нет: ОС создаёт его, загружается движок, Dart VM, код приложения, строится первый кадр | Всё ниже — это главный сценарий |
| **Тёплый** | Процесс жив, но экран пересоздан (например, после выгрузки активности на Android) | Восстановление состояния |
| **Горячий** | Приложение просто возвращается из фона | Обычно быстро; следить за работой в обработчике `resumed` |

**Как измерить.** `flutter run --profile --trace-startup` запускает приложение, записывает старт и создаёт
`build/start_up_info.json`:
- `timeToFrameworkInitMicros` — от входа в движок до инициализации фреймворка;
- `timeAfterFrameworkInitMicros` — от инициализации фреймворка до первого кадра (здесь работает ваш `main`);
- `timeToFirstFrameMicros` — до первого построенного кадра;
- `timeToFirstFrameRasterizedMicros` — до первого кадра на экране.

В продакшене время старта собирают аналитикой (Firebase Performance, Android Vitals, своя метрика от старта процесса
до `WidgetsBinding.instance.firstFrameRasterized`).

**Главная причина медленного старта в Flutter-приложениях — `main`, который ждёт всё подряд.** Два варианта `main`:

```dart
import 'package:flutter/material.dart';

/// Имитация SDK, которые инициализируются при старте (аналитика, крэш-репорты, удалённый конфиг)
Future<void> initAnalytics() => Future.delayed(const Duration(milliseconds: 300));
Future<void> initCrashReports() => Future.delayed(const Duration(milliseconds: 200));
Future<void> loadRemoteConfig() => Future.delayed(const Duration(milliseconds: 400));

// ❌ Первый кадр ждёт все SDK по очереди
Future<void> mainSlow() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initAnalytics();
  await initCrashReports();
  await loadRemoteConfig();
  runApp(const MaterialApp(home: Scaffold(body: Center(child: Text('Главный экран')))));
}

// ✅ Обязательное — до runApp, остальное — параллельно и после первого кадра
Future<void> mainFast() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initCrashReports(); // крэш-репорты нужны с самого начала
  runApp(const MaterialApp(home: Scaffold(body: Center(child: Text('Главный экран')))));
  WidgetsBinding.instance.addPostFrameCallback((_) {
    // Не ждём: экран уже показан, SDK догружаются параллельно
    Future.wait([initAnalytics(), loadRemoteConfig()]);
  });
}
```

Замер `--trace-startup` (macOS, profile):

```text
❌ Всё в main:      timeToFirstFrameMicros = 970110   (≈ 0,97 с)
✅ После 1-го кадра: timeToFirstFrameMicros = 260952   (≈ 0,26 с)
```

Разница — ровно 300 + 400 мс аналитики и конфига, которые больше не задерживают первый кадр.

Что ещё ускоряет старт:
- **Нативный splash** (`flutter_native_splash`) — экран показывается ОС мгновенно, пока грузится движок. Он не ускоряет
  старт, но убирает белый экран.
- **Лёгкий первый экран.** Скелетон или кеш вместо ожидания сети; тяжёлые экраны — после навигации.
- **Отложенная загрузка кода:** `import '…' deferred as …` (на Android — deferred components) для редких больших
  разделов.
- **Меньше плагинов**, которые инициализируются при регистрации, и меньше синхронной работы в `initState` первого экрана.
- **Тяжёлую подготовку данных** (разбор кеша, миграции БД) — в изолят или после первого кадра.

### 9. Защита от регресса: бенчмарк в CI

Оптимизация живёт до первого неосторожного коммита. Ключевые сценарии (прокрутка ленты, открытие выписки)
проверяют автоматически: `integration_test` записывает Timeline во время действия, драйвер считает сводку.

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

import 'package:bank_app/statement_app.dart';

void main() {
  final binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('прокрутка выписки', (tester) async {
    await tester.pumpWidget(const StatementApp());

    // Записываем Timeline, пока прокручиваем до 300-й операции
    await binding.traceAction(
      () => tester.scrollUntilVisible(
        find.byKey(const ValueKey('operation_300')),
        500,
        scrollable: find.byType(Scrollable),
      ),
      reportKey: 'statement_scroll',
    );
  });
}
```

```dart
import 'package:flutter_driver/flutter_driver.dart' as driver;
import 'package:integration_test/integration_test_driver.dart';

/// Получает Timeline из теста, считает сводку и пишет её в build/
Future<void> main() => integrationDriver(
      responseDataCallback: (data) async {
        if (data == null) return;
        final timeline = driver.Timeline.fromJson(data['statement_scroll'] as Map<String, dynamic>);
        final summary = driver.TimelineSummary.summarize(timeline);
        await summary.writeTimelineToFile('statement_scroll', pretty: true, includeSummary: true);
      },
    );
```

```bash
flutter drive --profile --driver=test_driver/perf_driver.dart --target=integration_test/statement_scroll_test.dart
```

Фрагмент `build/statement_scroll.timeline_summary.json` (лента из 1000 операций, macOS):

```text
"frame_count": 67,
"average_frame_build_time_millis": 2.70,
"90th_percentile_frame_build_time_millis": 6.48,
"worst_frame_build_time_millis": 7.32,
"missed_frame_build_budget_count": 0,
"average_frame_rasterizer_time_millis": 1.54,
"worst_frame_rasterizer_time_millis": 23.30,
"missed_frame_rasterizer_budget_count": 2
```

В CI сравнивают перцентили и число пропущенных кадров с прошлым запуском или порогом: выросли — сборка красная.
Средние значения обманчивы, смотрят **90-й и 99-й перцентили** и **worst**: пользователь замечает именно редкие длинные кадры.

> ℹ️ **Важно:** на реальных устройствах `flutter drive` запускают с `--no-dds`; бенчмарки гоняют в profile на одних и
> тех же устройствах, иначе цифры не сравнимы. На вебе запись Timeline так не работает.

### ⚠️ Частые ошибки

- **Оптимизация без замера** и замер в debug или на эмуляторе.
- **`RepaintBoundary` «везде на всякий случай».** Память и композиция растут, пользы нет.
- **`Opacity` в анимации** вместо `FadeTransition`/`AnimatedOpacity`.
- **`ClipRRect` ради скруглённых углов карточки** вместо `borderRadius` в декорации.
- **Картинки без `cacheWidth`/`cacheHeight`**: 48 МБ памяти на одну аватарку.
- **`main`, который ждёт все SDK** перед `runApp`.
- **Методы `_buildX()` вместо отдельных виджетов** и отсутствие `const` там, где он возможен.
- **Переопределение `operator ==` у виджетов.**
- **Смотреть только на средние значения** времени кадра вместо перцентилей и худших кадров.
- **Прогрев шейдеров SkSL в проекте на Impeller** — с Impeller не работает и не нужен.

### 🎤 Задача с собеседования: «Лента операций тормозит на старых Android. Твой план?»

| Уровень | Как выглядит ответ |
|---------|--------------------|
| ⭐ Junior | `ListView.builder` вместо `Column`, `const` у виджетов, убрать лишние `setState` |
| ⭐⭐ Middle | Воспроизвести на слабом устройстве в profile, определить поток. UI: Trace widget builds, локализовать состояние, `const`, `itemExtent`, вынести форматирование из `itemBuilder`, тяжёлое — в изолят. Raster: Highlight Repaints, убрать `Opacity`/`ClipRRect`/тени в строках, картинки с `cacheWidth`. Повторный замер |
| ⭐⭐⭐ Senior | Всё из Middle, плюс: данные из продакшена (какие модели, какой процент медленных кадров), проверка рендерера на этих устройствах (API ниже 29 или без Vulkan — откат с Impeller на OpenGL, возможен jank компиляции шейдеров), память (картинки, кеши — на слабых устройствах ОС выгружает приложение), бенчмарк прокрутки в CI с порогом по 90/99 перцентилям, мониторинг медленных кадров после релиза |

---

## ✅ Самопроверка

**⭐ Junior**
1. Почему `const`-виджет не перестраивается при `setState` родителя?
2. Чем `ListView.builder` лучше `ListView(children: …)` для длинного списка?
3. Сколько памяти займёт картинка 4000×3000 после декодирования?

**⭐⭐ Middle**
1. Как отличить jank на этапе build от jank на этапе растеризации? Какие причины у каждого?
2. Когда `RepaintBoundary` помогает, а когда вредит?
3. Чем `FadeTransition` лучше `Opacity` в анимации?
4. Почему отдельный `StatelessWidget` лучше метода `_buildHeader()`?
5. Как уменьшить память под картинки в ленте?

**⭐⭐⭐ Senior**
1. Что такое `saveLayer` и какие виджеты его вызывают? Чем заменить?
2. Что такое shader compilation jank? Нужен ли прогрев шейдеров в проекте на Impeller? Где проблема ещё возможна?
3. Как измерить и ускорить холодный старт?
4. Как защитить производительность от регресса? Почему смотреть на перцентили, а не на среднее?
5. Лента тормозит только на старых Android. Какие причины проверишь в первую очередь?

<details>
<summary>Ответы</summary>

**Junior**
1. `const`-выражение — один и тот же объект. При перестроении родителя Flutter видит тот же объект (`identical`)
   и пропускает обновление поддерева. Замер: 11 вызовов `build` без `const` против 1 с `const`.
2. Строит только видимые строки и небольшой запас; `ListView(children:)` создаёт все виджеты сразу.
3. 4000 × 3000 × 4 байта = 48 000 000 байт, около 46 МБ, независимо от размера файла.

**Middle**
1. По графику кадров: красный UI — build/layout (лишние перестроения, тяжёлый `build`, intrinsic-проходы,
   `shrinkWrap`); красный Raster — дорогая сцена (`saveLayer`, размытие, тени, большие картинки, обрезка со слоем).
2. Помогает, когда маленькая часть меняется часто, а соседи — нет (замер: 60 перерисовок графика против 0).
   Вредит, если стоит везде или вокруг того, что меняется вместе с соседями: слой без пользы.
3. `Opacity` в анимации перестраивается на каждом кадре и перерисовывает детей. `FadeTransition` меняет только
   прозрачность слоя, дети нарисованы один раз.
4. Метод выполняется при каждом `build` родителя. У отдельного виджета свой элемент, его можно сделать `const`,
   и Flutter может пропустить его перестроение.
5. `cacheWidth`/`cacheHeight` (или `ResizeImage`) под размер на экране с учётом `devicePixelRatio`, превью нужного
   размера с сервера, дисковый кеш, при необходимости — меньшие лимиты `imageCache`.

**Senior**
1. `saveLayer` — отрисовка группы во временный буфер с последующим смешиванием: выделение памяти и переключение цели
   отрисовки на GPU. Вызывают `ShaderMask`, `ColorFilter`, `Opacity` над несколькими детьми, `Clip.antiAliasWithSaveLayer`,
   некоторые эффекты. Замена: прозрачность в цвете или `FadeTransition`, `borderRadius` вместо обрезки,
   `Clip.antiAlias`/`hardEdge`, эффект на картинке, а не на поддереве, меньшая область.
2. Рывок при первом появлении эффекта, пока компилируется шейдер. Impeller компилирует шейдеры при сборке движка,
   прогрев SkSL с ним не работает и не нужен. Проблема возможна там, где рисует не Impeller: старые Android
   (API ниже 29 или без Vulkan — откат на OpenGL), веб.
3. Измерить: `flutter run --profile --trace-startup` (`start_up_info.json`), в продакшене — метрика до первого кадра.
   Ускорить: в `main` до `runApp` только обязательное, остальное параллельно и после первого кадра
   (замер: 0,97 с → 0,26 с); нативный splash; лёгкий первый экран; deferred-импорты; меньше синхронной работы и плагинов.
4. Бенчмарки ключевых сценариев через `integration_test` + `traceAction` + `TimelineSummary` в profile на постоянных
   устройствах, порог в CI. Среднее скрывает редкие длинные кадры, а пользователь замечает именно их — поэтому
   90-й/99-й перцентили, worst и число пропущенных кадров.
5. Рендерер (Impeller или откат на OpenGL), память (картинки без `cacheWidth`, кеши — ОС выгружает приложение),
   тяжёлый `itemBuilder` и лишние перестроения, дорогие эффекты в строках (тени, обрезка, прозрачность), всё — замером
   в profile на таком устройстве.

</details>
