# Swift

| Грейд | Время на изучение | Статус |
|-------|-------------------|--------|
| ⭐⭐⭐ | ~60 мин | ✅ Готово |

> ℹ️ **Важно:** Objective-C в базе знаний не рассматриваем:
> новый код на нём давно не пишут, iOS-часть Flutter-проектов и плагинов создаётся на Swift. Из Objective-C здесь только
> одно — как Swift видит заголовок старого SDK (раздел 8).

---

## 📚 Ресурсы

| Ресурс | Формат | Язык | Уровень | Зачем читать |
|--------|--------|------|---------|--------------|
| [Руководство по Swift (METANIT)](https://metanit.com/swift/tutorial/) | Учебник | 🇷🇺 | ⭐ → ⭐⭐ | Язык по порядку, если нужно глубже, чем эта страница |
| [Списки захвата в Swift: weak, strong и unowned](https://habr.com/ru/post/444336/) | Статья (Habr) | 🇷🇺 | ⭐⭐ | Почему замыкание держит объект и как это исправить |
| [Память в Swift (куча, стек, ARC)](https://habr.com/ru/companies/otus/articles/649329/) | Статья (Habr) | 🇷🇺 | ⭐⭐ → ⭐⭐⭐ | Где живут struct и class, как работает подсчёт ссылок |
| [The Swift Programming Language](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/) | Книга (официальная) | 🇬🇧 | ⭐ → ⭐⭐⭐ | Первоисточник: язык целиком |
| [Automatic Reference Counting](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/automaticreferencecounting/) | Документация | 🇬🇧 | ⭐⭐ | ARC и циклы ссылок от авторов языка |
| [Concurrency](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/) | Документация | 🇬🇧 | ⭐⭐ | `async/await`, `Task`, акторы |
| [Importing Objective-C into Swift](https://developer.apple.com/documentation/swift/importing-objective-c-into-swift) | Документация | 🇬🇧 | ⭐⭐⭐ | Как Swift видит заголовки старых SDK |

---

## 🎓 Лекция

> ℹ️ **Важно:** как и «Java / Kotlin», это не учебник, а то, что нужно Flutter-разработчику для `AppDelegate`,
> плагинов, расширений и обёрток над SDK. Примеры такого кода — в «Platform Channels», «Нативных API iOS» и
> «Разработке плагинов». В таблицах колонки **Swift | Kotlin | Dart**: Swift по синтаксису ближе всего к Kotlin.
> Весь код собран (Xcode 26.5, Swift 5, минимальная iOS 13) и запущен на симуляторе iOS 26.5; колонки Kotlin и Dart —
> на эмуляторе Android и через `dart run`. Результаты — рядом с кодом.

### 1. Зачем и где это встречается

| Где | Что на Swift |
|-----|--------------|
| `ios/Runner/AppDelegate.swift` | Регистрация своих каналов, обработка ссылок и push |
| Плагины | Класс плагина, обработчики каналов |
| Расширения | Notification Service Extension, виджеты, Share Extension |
| SDK банка и вендоров | Новые — на Swift, старые — на Objective-C (Swift вызывает их напрямую) |

Файлы лежат в `ios/Runner/` (приложение) и `ios/<плагин>/Sources/` (плагин). Новый файл нужно добавить в цель
(target) Xcode — простого копирования в папку мало (подробно — «Базовая настройка нативных проектов»).

### 2. Основной синтаксис

#### Переменные и строки

| Что | Swift | Kotlin | Dart |
|-----|-------|--------|------|
| Неизменяемая | `let name = "Иван"` | `val name = "Иван"` | `final name = 'Иван';` |
| Изменяемая | `var count = 3` | `var count = 3` | `var count = 3;` |
| Тип явно | `let total: Int64 = 1_250` | `val total: Long = 1_250` | `const int total = 1250;` |
| Присвоить позже, один раз | `let level: String` + присваивание в каждой ветке | `val level: String` + присваивание | `final String level;` + присваивание |
| Интерполяция | `"\(name): \(count)"` | `"$name: $count"` | `'$name: $count'` |
| Многострочная | `"""…"""` | `"""…""".trimIndent()` | `'''…'''` |
| Точка с запятой | Не нужна | Не нужна | Обязательна |
| Неявное приведение чисел | **Нет**: `Int` и `Int64` — разные типы | Нет | `int` один |

Проверено при сборке: расширение для `Int64` не вызывается у литерала `125_050` — литерал по умолчанию `Int`,
ошибка `Value of type 'Int' has no member 'asRub'`. Нужно `Int64(125_050).asRub`.

#### Условия и циклы

| Что | Swift | Kotlin | Dart |
|-----|-------|--------|------|
| `if` | `if a > b { … }` — скобки не нужны, фигурные обязательны | `if (a > b) { … }` | `if (a > b) { … }` |
| Тернарный | `a > b ? a : b` | `if (a > b) a else b` | `a > b ? a : b` |
| Ранний выход | `guard let x = y else { return }` | `val x = y ?: return` | `if (y == null) return;` |
| Выбор | `switch x { case 0: …; case 1...3: …; default: … }` | `when (x) { 0 -> …; in 1..3 -> …; else -> … }` | `switch (x) { 0 => …, _ => … }` |
| `break` в `switch` | Не нужен; нужно покрыть все случаи | Не нужен | Не нужен (Dart 3) |
| Диапазоны | `1...3` (с 3), `1..<3` (без 3) | `1..3`, `1 until 3` | Нет, цикл `for` |
| Перебор | `for c in list` | `for (c in list)` | `for (final c in list)` |

```swift
let level: String              // let можно присвоить позже — но ровно один раз
switch count {                 // switch без break; должен покрыть все случаи
case 0: level = "нет"
case 1...3: level = "мало"     // диапазон в образце
default: level = "много"
}

let squares = (1...3).map { String($0 * $0) }.joined(separator: " ") // 1...3 включительно, 1..<3 — без 3
```

```kotlin
val level = when (count) {
    0 -> "нет"
    in 1..3 -> "мало"            // диапазон в when
    else -> "много"
}
```

```console
SW basics: Иван: 4 операции, 1250 ₽ | много | 1 4 9
```

**`guard`** — главный приём Swift в обработчиках каналов: проверить входные данные и выйти, если что-то не так.
После `guard let` переменная доступна до конца функции:

```swift
// call.arguments приходит как Any? — словарь [String: Any], числа внутри — NSNumber
guard let args = arguments as? [String: Any] else { return "нет аргументов" } // ранний выход
```

#### Функции и замыкания

| Что | Swift | Kotlin | Dart |
|-----|-------|--------|------|
| Объявление | `func fee(_ amount: Int64) -> String` | `fun fee(amount: Long): String` | `String fee(int amount)` |
| Метки аргументов | `fee(10_000, percent: 1)`; `_` — без метки | Именованные необязательны | Именованные `{}` |
| Значение по умолчанию | `percent: Double = 0.5` | `percent: Double = 0.5` | `{double percent = 0.5}` |
| Изменить переменную вызывающего | `inout` + `&balance` | Нет | Нет |
| Одно выражение | Тело из одного выражения — `return` не нужен | `= выражение` | `=> выражение` |
| Замыкание | `{ x in x * 2 }`, `$0` | `{ x -> x * 2 }`, `it` | `(x) => x * 2` |
| Последнее замыкание за скобками | `check(amount) { verdict in … }` | `check(amount) { verdict -> … }` | Нет |
| Замыкание переживёт вызов | `@escaping` | Обычная лямбда | Обычная функция |

```swift
// Метки аргументов: «_» — без метки при вызове; percent: — с меткой; значение по умолчанию
static func fee(_ amount: Int64, percent: Double = 0.5) -> String {
  "\(amount) → комиссия \(Int64(Double(amount) * percent / 100))" // одно выражение — return можно не писать
}

// inout: функция меняет переданную переменную вызывающего
static func addBonus(_ balance: inout Int64) { balance += 100 }

var balance: Int64 = 1_000
SwiftSamples.addBonus(&balance)                           // & — передаём переменную для изменения
```

```console
SW fee: 10000 → комиссия 50 / 10000 → комиссия 100
SW inout: 1100
```

**`@escaping`.** Замыкание, которое сохраняется и вызывается после выхода из функции (колбэк сети, SDK), помечают
`@escaping`. Именно так объявлен `FlutterResult` в обработчике канала: ответ можно отдать позже.

#### Коллекции — это значения

| Что | Swift | Kotlin | Dart |
|-----|-------|--------|------|
| Массив | `let a = ["RUB", "USD"]` (неизменяем), `var` — изменяем | `listOf` / `mutableListOf` | `const […]` / `[…]` |
| Словарь | `["USD": 90]` | `mapOf("USD" to 90)` | `{'USD': 90}` |
| Множество | `let s: Set = ["RUB"]` | `setOf("RUB")` | `{'RUB'}` |
| Элемент словаря | `rates["USD"]` → `Int?` | `rates["USD"]` → `Int?` | `rates['USD']` → `int?` |
| Присвоить другой переменной | **Копия** | Та же ссылка | Та же ссылка |
| Фильтр и map | `filter { $0 != "RUB" }.map { $0.lowercased() }` | `filter { … }.map { … }` | `where(…).map(…)` |

```swift
let fixed = ["RUB", "USD"]                 // let-массив неизменяем целиком
var currencies = fixed                     // КОПИЯ: массив — значение, а не ссылка
currencies.append("EUR")
```

```console
SW collections: ["RUB", "USD", "EUR"] ["RUB", "USD"] 90 ["usd", "eur"] set=2
```

`fixed` не изменился. В Kotlin и Dart та же операция меняет исходный список — проверено:
`val alias = list; alias += "USD"` → `[RUB, USD]`. Копия в Swift дешёвая: реальное копирование происходит только
при изменении (copy-on-write).

#### Ошибки

| Что | Swift | Kotlin | Dart |
|-----|-------|--------|------|
| Объявить, что функция бросает | `func transfer() throws -> String` | Не объявляют | Не объявляют |
| Вызов | `try transfer()` — `try` обязателен | Просто вызов | Просто вызов |
| Поймать | `do { try … } catch { … }` | `try { … } catch (e: …) { … }` | `try { … } on … catch (e) { … }` |
| Ошибка → nil | `try? transfer()` | `runCatching { … }.getOrNull()` | — |
| Тип ошибки | `enum TransferError: Error { … }` | `class … : Exception()` | `class … implements Exception` |

```swift
enum TransferError: Error {
  case limitExceeded(limit: Int64)
  case noConnection
}

do {
  _ = try transfer(500_000_00)                       // try обязателен перед вызовом throws-функции
} catch TransferError.limitExceeded(let limit) {     // catch по образцу со связанным значением
  log.append("лимит \(limit)")
} catch {
  log.append("другое: \(error)")
}
let quiet = try? transfer(500_000_00)                // try? — ошибка превращается в nil
```

```console
SW errors: лимит 10000000 | try?=nil
```

### 3. Типы и опционалы

#### Числа из канала Flutter

| Dart | Приходит в Swift | Как читать |
|------|------------------|------------|
| `int` | `NSNumber` (внутри `Any`) | `(args["amount"] as? NSNumber)?.int64Value` — для любых сумм |
| `double` | `NSNumber` | `as? Double` |
| `bool` | `NSNumber` | `as? Bool` |
| `String` | `String` | `as? String` |
| `List`, `Map` | `[Any]`, `[String: Any]` | `as? [String: Any]` |

`as? Int` и `as? Int64` у `NSNumber` тоже работают — проверено на 7 и 50 000 000 000. Но `NSNumber` с `int64Value` —
одно правило для всех сумм, как `Number` в Kotlin.

#### Опционалы

| Что | Swift | Kotlin | Dart |
|-----|-------|--------|------|
| Может быть nil | `String?` | `String?` | `String?` |
| Развернуть, если есть | `if let x = y { … }` | `y?.let { x -> … }` | `if (y != null) { … }` |
| Развернуть или выйти | `guard let x = y else { return }` | `val x = y ?: return` | `if (y == null) return;` |
| Значение по умолчанию | `y ?? "нет"` | `y ?: "нет"` | `y ?? 'нет'` |
| Цепочка | `y?.count` | `y?.length` | `y?.length` |
| «Точно не nil» | `y!` | `y!!` | `y!` |
| Привести тип | `as?` (nil при неудаче), `as!` (падение) | `as?`, `as` | `as` |
| Любое значение | `Any`, `Any?` | `Any?` | `Object?` / `dynamic` |

```swift
guard let args = arguments as? [String: Any] else { return "нет аргументов" } // ранний выход
let name = args["name"] as? String ?? "без имени"     // as? + ?? — значение по умолчанию
var parts = [name]
if let amount = (args["amount"] as? NSNumber)?.int64Value { // if let — развернуть, если не nil
  parts.append("amount=\(amount)")
}
let length = (args["comment"] as? String)?.count      // опциональная цепочка: nil, если comment нет
```

```console
SW optionals: Иван amount=150000 comment=nil small=7 big=50000000000 | нет аргументов
```

### 4. Структуры и классы

#### struct или class — главное отличие Swift

| | `struct` | `class` |
|---|---|---|
| Присваивание и передача | **Копия** | Ссылка на тот же объект |
| Наследование | Нет | Есть (`final` запрещает) |
| Инициализатор | Создаётся автоматически по полям | Пишут сами (`init`) |
| Менять поля | Только у `var`-экземпляра; метод — `mutating` | Всегда, даже через `let`-ссылку |
| Сравнение `===` (тот же объект) | Нет | Есть |
| Когда | Модели, значения — **по умолчанию** | Общее изменяемое состояние, наследование, `NSObject` (плагины, делегаты) |

В Kotlin и Dart все классы — ссылки; ближе всего к `struct` — неизменяемый `data class` / класс с `final`-полями и `copy`.

```swift
// struct — значение: при присваивании КОПИРУЕТСЯ
struct AccountValue {
  let id: String
  var balanceKopecks: Int64
}

// class — ссылка: при присваивании копируется ссылка на тот же объект
final class AccountRef {
  let id: String
  var balanceKopecks: Int64

  init(id: String, balanceKopecks: Int64) { // у class инициализатор пишут сами
    self.id = id
    self.balanceKopecks = balanceKopecks
  }
}

var a = AccountValue(id: "40817", balanceKopecks: 125_000) // у struct инициализатор создаётся сам
var b = a                                                 // копия
b.balanceKopecks = 0
a.balanceKopecks += 1
let r1 = AccountRef(id: "40817", balanceKopecks: 125_000)
let r2 = r1                                               // та же ссылка
r2.balanceKopecks = 0                                     // let-ссылка, но объект менять можно
```

```console
struct a=125001 b=0 | class r1=0 same=true
```

#### Остальное

| Что | Swift | Kotlin | Dart |
|-----|-------|--------|------|
| Класс данных | `struct` + `Equatable`, `Codable` | `data class` | Класс + `==`, `copyWith` |
| Закрытая иерархия | `enum` со связанными значениями | `sealed interface` | `sealed class` |
| Перечисление с значением | `enum Currency: String { case rub = "₽" }` | `enum class Currency(val symbol: String)` | `enum` с полями |
| Интерфейс | `protocol` | `interface` | `abstract class` / `interface class` |
| Реализация по умолчанию | `extension Протокол { func … }` | Метод с телом в `interface` | Метод в `abstract class` |
| Расширить чужой тип | `extension Int64 { var asRub: String { … } }` | `fun Long.asRub()` | `extension … on int` |
| Статические члены | `static let maxMinutes = 15` | `companion object` | `static` |
| Переопределить | `override` (обязательно) | `override` | `@override` |
| Запретить наследование | `final class` | По умолчанию | `final class` (Dart 3) |
| Неудачный конструктор | `init?(…)` возвращает `nil` | Исключение в `init` | Фабрика или исключение |
| JSON | `Codable` (встроено) | `kotlinx.serialization`, Moshi | `json_serializable` |

```swift
// Codable — модель в JSON и обратно без ручного кода; Equatable — == по содержимому
struct Account: Codable, Equatable {
  let id: String
  let balanceKopecks: Int64

  // Проверка в инициализаторе: init? вернёт nil при неверных данных
  init?(id: String, balanceKopecks: Int64) {
    guard balanceKopecks >= 0 else { return nil }
    self.id = id
    self.balanceKopecks = balanceKopecks
  }
}

// enum со связанными значениями — аналог sealed в Kotlin и Dart
enum PaymentResult {
  case success(id: String)
  case declined(reason: String)
  case pending
}

func describe(_ result: PaymentResult) -> String {
  switch result {                                 // компилятор проверяет, что разобраны все случаи
  case .success(let id): return "Успех \(id)"
  case .declined(let reason): return "Отказ: \(reason)"
  case .pending: return "В обработке"
  }
}

// Протокол — как interface
protocol Notifier {
  func send(_ text: String) -> String
}

// Реализация по умолчанию — через расширение протокола
extension Notifier {
  func sendAll(_ texts: [String]) -> String { texts.map(send).joined(separator: ", ") }
}

// Расширение чужого типа
extension Int64 {
  var asRub: String { String(format: "%lld,%02lld ₽", self / 100, self % 100) }
}
```

```console
{"id":"40817","balanceKopecks":125050} | decoded==true | invalid=nil | Отказ: лимит | В обработке | ₽ | [a], [b] | V*5678 | 1250,50 ₽ | 15
```

### 5. Память: ARC и `[weak self]`

В Kotlin и Dart объекты освобождает **сборщик мусора**, циклические ссылки ему не мешают. В Swift — **ARC**
(автоматический подсчёт ссылок): объект живёт, пока на него есть сильные ссылки. Если объект хранит замыкание,
а замыкание держит объект, счётчики никогда не станут нулём — **утечка**.

```swift
// ARC: объект живёт, пока на него есть сильные ссылки. Замыкание, которое хранит self, и self, который хранит
// замыкание, — цикл: счётчик никогда не станет 0, deinit не вызовется
final class TransferScreen {
  let name: String
  var onTimer: (() -> Void)?

  init(name: String) { self.name = name }

  func startLeaking() {
    onTimer = { print(self.name) }                 // сильная ссылка на self — цикл
  }

  func startSafe() {
    onTimer = { [weak self] in                     // слабая ссылка: цикла нет
      guard let self else { return }               // объект мог уже исчезнуть
      print(self.name)
    }
  }

  deinit { MemoryLog.deinited.append(name) }       // вызывается, когда объект освобождён
}

do {
  let leaking = TransferScreen(name: "с утечкой")
  leaking.startLeaking()
  let safe = TransferScreen(name: "без утечки")
  safe.startSafe()
}                                              // здесь обе локальные ссылки исчезают
```

```console
SW memory: освобождены: ["без утечки"]
```

Объект «с утечкой» так и остался в памяти. Правила:

- замыкание, которое **хранится** (свойство, подписка, таймер, колбэк SDK) и обращается к `self`, — `[weak self]`;
- разовое замыкание, которое выполнится и исчезнет (`map`, `DispatchQueue.main.async`), можно без `weak`;
- **делегаты** объявляют `weak var delegate` — иначе тот же цикл;
- `[unowned self]` — как `weak`, но без опционала; если объект уже исчез — падение. В банковском коде проще `weak`.

### 6. Обработчик канала: Swift рядом с Kotlin

```swift
// Обработчик MethodChannel на Swift — сравните с KotlinSecurityHandler
final class SwiftSecurityHandler {
  init(messenger: FlutterBinaryMessenger) {
    FlutterMethodChannel(name: "ru.bank/swift", binaryMessenger: messenger).setMethodCallHandler { call, result in
      switch call.method {
      case "isDeviceSecure":
        result(LAContext().canEvaluatePolicy(.deviceOwnerAuthentication, error: nil))
      case "checkAmount":
        // Числа из Dart приходят как NSNumber: берём int64Value — подходит и для малых, и для больших сумм
        guard let args = call.arguments as? [String: Any], let amount = (args["amount"] as? NSNumber)?.int64Value else {
          return result(FlutterError(code: "BAD_ARGS", message: "Нет суммы", details: nil))
        }
        // Блок Objective-C — замыкание Swift
        AntiFraudSDK.checkAmount(amount) { verdict in
          result(verdict == .review ? "REVIEW" : "ALLOW")
        }
      case "hashStatement":
        // async/await: тяжёлое — в фоновой задаче, ответ — на главном акторе (главный поток)
        Task { @MainActor in
          let hash = await Task.detached(priority: .utility) {
            (1...200_000).reduce(Int64(0)) { ($0 * 31 + Int64($1)) % 1_000_000_007 }
          }.value
          result("\(hash) main=\(isMainThread())")
        }
      default:
        result(FlutterMethodNotImplemented)
      }
    }
  }
}

private func isMainThread() -> Bool { Thread.isMainThread }
```

| | Swift | Kotlin |
|---|---|---|
| Ответ | `result(value)` — замыкание | `result.success(value)` — объект |
| Ошибка | `result(FlutterError(code:message:details:))` | `result.error(code, message, details)` |
| Нет метода | `result(FlutterMethodNotImplemented)` | `result.notImplemented()` |
| Аргументы | `call.arguments as? [String: Any]` | `call.argument<Number>("amount")` |
| Выйти с ошибкой | `guard … else { return result(…) }` | `?: return result.error(…)` |

Вызов из Dart — тот же результат и тот же хэш, что у Java и Kotlin:

```console
swcheck: isDeviceSecure=true, checkAmount 1 500 ₽=ALLOW, 500 000 000 ₽=REVIEW, hash=851862047 main=true
```

### 7. Асинхронность коротко

| Что | Swift: GCD | Swift: async/await | Kotlin |
|-----|-----------|--------------------|--------|
| В фоне | `DispatchQueue.global().async { … }` | `Task.detached { … }` | `withContext(Dispatchers.Default)` |
| На главный поток | `DispatchQueue.main.async { … }` | `@MainActor`, `await MainActor.run { … }` | `Dispatchers.Main` |
| Функция «может ждать» | Колбэк | `async func` | `suspend fun` |
| Минимальная iOS | Любая | 13 (с Xcode 13.2+) | — |

Правило для каналов то же: `result` и `eventSink` — с главного потока. В примере сумма считается в
`Task.detached`, ответ ушёл с главного (`main=true`). В старом коде и SDK встречается GCD — его стоит уметь читать.

### 8. Как Swift видит Objective-C SDK

Старый SDK на Objective-C подключается через bridging header (`Runner-Bridging-Header.h`) или модуль, и Swift строит
свои типы по заголовку. Главное — **аннотации nullability**:

```objc
#import <Foundation/Foundation.h>

// Так выглядит заголовок SDK на Objective-C. Swift читает его и строит свои типы
typedef NS_ENUM(NSInteger, AFVerdict) {
  AFVerdictAllow,
  AFVerdictReview,
};

@interface AntiFraudSDK : NSObject

/// Блок-колбэк: в Swift станет замыканием (AFVerdict) -> Void
+ (void)checkAmount:(int64_t)amountKopecks completion:(void (^_Nonnull)(AFVerdict verdict))completion;

/// С аннотацией nullable: в Swift — String?
+ (nullable NSString *)deviceIdOrNull:(BOOL)known;

/// Без аннотации: в Swift — String! (неявно развёрнутый опционал), аналог платформенного типа Kotlin
+ (NSString *)legacyDeviceId:(BOOL)known;

@end
```

| В заголовке | В Swift | В Kotlin из Java |
|-------------|---------|------------------|
| `nullable NSString *` | `String?` | `@Nullable` → `String?` |
| `nonnull NSString *` | `String` | `@NonNull` → `String` |
| Без аннотации | `String!` — неявно развёрнутый | `String!` — платформенный тип |
| `NS_ENUM(NSInteger, AFVerdict)` | `enum AFVerdict { case allow, review }` | — |
| Блок `void (^)(AFVerdict)` | Замыкание `(AFVerdict) -> Void` | SAM-интерфейс → лямбда |
| `NSString *`, `NSNumber *`, `NSArray *` | `String`, `NSNumber`, `[Any]` | — |

```swift
let maybe = AntiFraudSDK.deviceIdOrNull(false)            // String?
let legacy = AntiFraudSDK.legacyDeviceId(false)           // String! → при выводе типа становится String?
let id: String = AntiFraudSDK.legacyDeviceId(false)       // String! в не-опциональный String: nil → падение
```

```console
SW objc: nil nil type=Optional<String>
Fatal error: Unexpectedly found nil while implicitly unwrapping an Optional value
```

Ловушка та же, что в Kotlin: компилятор молчит, приложение падает при присваивании. Результат метода SDK без
аннотаций кладите в `String?` и проверяйте.

### ⚠️ Частые ошибки

- **`String!` из Objective-C-SDK в не-опциональный тип** — падение «Unexpectedly found nil».
- **`!` и `as!` «чтобы скомпилировалось»** — то же падение, только явное.
- **`as? Int` для суммы** без понимания, что пришло `NSNumber`; надёжно — `NSNumber.int64Value`.
- **Ожидать, что изменение копии массива или `struct` изменит оригинал** — в Swift это копия.
- **`class` для моделей по привычке Kotlin** — неожиданные изменения через общую ссылку; модели — `struct`.
- **Сильный `self` в хранимом замыкании, сильный делегат** — утечка, `deinit` не вызывается.
- **`[unowned self]` там, где объект может исчезнуть** — падение.
- **Смешивать `Int` и `Int64` без приведения** — ошибки компиляции («no member»), неявного приведения нет.
- **`result` из фоновой очереди или `Task.detached`** — ответ не с главного потока.
- **Забыть `try`** — ошибка компиляции; **`try?`, проглатывающий ошибку** — потеря причины сбоя.
- **`switch` по `enum` с `default`** — при добавлении случая компилятор уже не подскажет, где его обработать.
- **Новый `.swift`-файл только в папке**, без добавления в цель Xcode — «Cannot find type in scope».

### 🎤 На собеседовании: «Чем struct отличается от class в Swift и когда что выбрать?»

| Уровень | Как выглядит ответ |
|---------|--------------------|
| ⭐ Junior | `struct` копируется, `class` передаётся по ссылке; у `class` есть наследование |
| ⭐⭐ Middle | Всё из Junior, плюс: у `struct` автоматический инициализатор, изменение через `var` и `mutating`; `let`-ссылка на `class` не запрещает менять объект; `Array`, `String`, `Dictionary` — структуры; по умолчанию модели — `struct`, `class` — для общего состояния, наследования, `NSObject` (делегаты, плагины) |
| ⭐⭐⭐ Senior | Всё из Middle, плюс: copy-on-write делает копирование коллекций дешёвым; классы живут по ARC — циклы ссылок и `[weak self]`, у `struct` таких проблем нет; `===` только у классов; при общем изменяемом состоянии между потоками — `actor`; сравнение с Kotlin и Dart, где всё — ссылки |

---

## ✅ Самопроверка

**⭐ Junior**
1. Чем `let` отличается от `var`? Что им соответствует в Kotlin и Dart?
2. Как развернуть опционал и что делает `guard let`?
3. Как в Swift записать «длина строки или 0, если её нет»?

**⭐⭐ Middle**
1. Почему после `var b = a; b.append(…)` массив `a` не меняется?
2. Как прочитать сумму из `call.arguments` надёжно для любых значений?
3. Что такое метки аргументов и `_` в объявлении функции?
4. Чем `enum` со связанными значениями похож на `sealed` в Kotlin и Dart?
5. Зачем `@escaping`?

**⭐⭐⭐ Senior**
1. Почему в Swift возможна утечка через замыкание, а в Kotlin и Dart — нет? Как исправить?
2. Что такое `String!` в Swift и где приложение упадёт?
3. Как в обработчике канала выполнить тяжёлую работу и ответить правильно?
4. Когда `[unowned self]` опаснее `[weak self]`?

<details>
<summary>Ответы</summary>

**Junior**
1. `let` — константа (Kotlin `val`, Dart `final`), `var` — переменная (в обоих `var`).
2. `if let x = y { … }` — выполнить блок, если не `nil`; `guard let x = y else { return }` — выйти, если `nil`,
   а дальше `x` доступна до конца функции.
3. `text?.count ?? 0`.

**Middle**
1. Массивы в Swift — значения: присваивание создаёт копию (реально копируется при изменении — copy-on-write).
2. `(args["amount"] as? NSNumber)?.int64Value`: числа из Dart приходят как `NSNumber`, `int64Value` подходит для
   любых сумм.
3. Метка — имя аргумента при вызове (`fee(10_000, percent: 1)`); `_` — вызывать без метки.
4. Набор вариантов закрыт, у каждого свои данные, `switch` проверяется на полноту.
5. Замыкание сохраняется и вызывается после выхода из функции (колбэк SDK, `FlutterResult`).

**Senior**
1. Swift освобождает объекты по ARC — счётчику сильных ссылок; цикл «объект ↔ замыкание» не даёт счётчику
   дойти до нуля. Сборщик мусора Kotlin и Dart циклы находит сам. Исправление — `[weak self]` в хранимых замыканиях,
   `weak var delegate`.
2. Неявно развёрнутый опционал: тип из Objective-C-заголовка без аннотаций nullability. При присваивании в
   не-опциональный тип или обращении к значению, если там `nil`, — «Unexpectedly found nil while implicitly
   unwrapping an Optional value».
3. `Task { @MainActor in let x = await Task.detached { … }.value; result(x) }` или GCD:
   `DispatchQueue.global().async { …; DispatchQueue.main.async { result(x) } }`.
4. `unowned` предполагает, что объект жив; если он уже освобождён, обращение — падение. `weak` в этом случае даёт
   `nil`, и код может просто выйти.

</details>
