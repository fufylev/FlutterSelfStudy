# Java / Kotlin

| Грейд | Время на изучение | Статус |
|-------|-------------------|--------|
| ⭐⭐⭐ | ~60 мин | ✅ Готово |

---

## 📚 Ресурсы

| Ресурс | Формат | Язык | Уровень | Зачем читать |
|--------|--------|------|---------|--------------|
| [Изучите язык программирования Kotlin](https://developer.android.com/kotlin/learn?hl=ru) | Документация | 🇷🇺 | ⭐ | Ускоренный курс Kotlin от Android: переменные, null, функции, классы |
| [Руководство по Kotlin (METANIT)](https://metanit.com/kotlin/tutorial/) | Учебник | 🇷🇺 | ⭐ → ⭐⭐ | Подробно и по порядку, если нужно глубже |
| [Руководство по Java (METANIT)](https://metanit.com/java/tutorial/) | Учебник | 🇷🇺 | ⭐ → ⭐⭐ | Справочник по Java для чтения чужого кода и SDK |
| [kotlinlang.ru](https://kotlinlang.ru/) | Документация (перевод) | 🇷🇺 | ⭐⭐ | Перевод официальной документации, раздел «Сравнение с Java» |
| [Kotlin-Java interop guide](https://developer.android.com/kotlin/interop?hl=ru) | Документация | 🇷🇺 | ⭐⭐ → ⭐⭐⭐ | Как писать Java и Kotlin, которые удобно вызывать друг из друга |
| [Корутины Kotlin на Android](https://developer.android.com/kotlin/coroutines?hl=ru) | Документация | 🇷🇺 | ⭐⭐ | Корутины на Android: потоки, отмена |
| [Comparison to Java](https://kotlinlang.org/docs/comparison-to-java.html) | Документация | 🇬🇧 | ⭐⭐ | Официальный короткий список отличий |

---

## 🎓 Лекция

> ℹ️ **Важно:** это не учебник по двум языкам, а то, что нужно Flutter-разработчику, чтобы читать и писать нативный
> Android-код: `MainActivity`, плагины, обёртки над SDK. Сами примеры такого кода — в «Platform Channels»,
> «Нативных API Android» и «Разработке плагинов». В таблицах третья колонка — **Dart**: «знаю это в Dart → так это
> в Java и Kotlin». Весь код собран (Kotlin 2.2.20, Java 17, AGP 8.11) и запущен на эмуляторе Android 16; результаты —
> рядом с кодом.

### 1. Зачем и где это встречается

| | Java | Kotlin |
|---|---|---|
| Статус в Android | Поддерживается, но новые API и примеры Google — на Kotlin | Основной язык Android с 2019 года |
| Во Flutter-проекте | Старые проекты (`MainActivity.java`), плагины старше ~2020 | `flutter create` создаёт Kotlin |
| SDK банков и вендоров | Часто: Java совместима со всем | Новые SDK |
| Совместимость | Вызывает Kotlin | Вызывает Java напрямую |

Оба языка компилируются в байт-код JVM и **живут в одном модуле**: `MainActivity.kt` спокойно вызывает
`AntiFraudSdk.java`, и наоборот. Переписывать Java-код ради Kotlin не нужно.

Файлы: `android/app/src/main/kotlin/…/*.kt` и `android/app/src/main/java/…/*.java`.

### 2. Основной синтаксис

#### Переменные и строки

| Что | Java | Kotlin | Dart |
|-----|------|--------|------|
| Неизменяемая ссылка | `final String name = "Иван";` | `val name = "Иван"` | `final name = 'Иван';` |
| Изменяемая переменная | `int count = 3;` | `var count = 3` | `var count = 3;` |
| Вывод типа | `var total = 1_250L;` (Java 10+, только локальные) | Везде: `val total = 1_250L` | `final total = 1250;` |
| Константа | `static final int MAX = 15;` | `const val MAX = 15` (в `object` / `companion`) | `const max = 15;` |
| Тип явно | `String name` (тип слева) | `name: String` (тип справа) | `String name` |
| Шаблон строки | `String.format("%s: %d", name, count)` | `"$name: $count"`, `"${a + b}"` | `'$name: $count'`, `'${a + b}'` |
| Многострочная строка | `"""…"""` (Java 15+) | `"""…""".trimIndent()` | `'''…'''` |
| Точка с запятой | Обязательна | Не нужна | Обязательна |
| Создание объекта | `new Account(…)` | `Account(…)` | `Account(…)` |

#### Условия и циклы

| Что | Java | Kotlin | Dart |
|-----|------|--------|------|
| `if` как значение | Тернарный `a > b ? a : b` | `if (a > b) a else b` (тернарного нет) | `a > b ? a : b` |
| Выбор по значению | `switch (x) { case 1, 2 -> "мало"; default -> "много"; }` (Java 14+) | `when (x) { 1, 2 -> "мало"; else -> "много" }` | `switch (x) { 1 => 'мало', _ => 'много' }` |
| Проверка типа | `if (o instanceof String s)` (Java 16+) | `if (o is String)` — дальше `o` уже `String` | `if (o is String)` |
| Приведение типа | `(String) o` | `o as String`, безопасно: `o as? String` | `o as String` |
| Цикл со счётчиком | `for (int i = 1; i <= 3; i++)` | `for (i in 1..3)`, `until`, `step`, `downTo` | `for (var i = 1; i <= 3; i++)` |
| Перебор коллекции | `for (String c : list)` | `for (c in list)` | `for (final c in list)` |

Выбор по значению на трёх языках, результат один — `много` при `count = 4`:

```java
String level = switch (count) {        // switch-выражение (Java 14+)
    case 0 -> "нет";
    case 1, 2, 3 -> "мало";
    default -> "много";
};
```

```kotlin
val level = when (count) {   // when — выражение, как switch-выражение Java
    0 -> "нет"
    1, 2, 3 -> "мало"
    else -> "много"
}
```

```dart
final level = switch (count) { 0 => 'нет', 1 || 2 || 3 => 'мало', _ => 'много' };
```

#### Функции и лямбды

| Что | Java | Kotlin | Dart |
|-----|------|--------|------|
| Объявление | `static String fee(long amount) { … }` | `fun fee(amount: Long): String { … }` | `String fee(int amount) { … }` |
| В одну строку | — | `fun fee(a: Long) = "…"` | `String fee(int a) => '…';` |
| Параметр по умолчанию | Нет — перегрузка методов | `percent: Double = 0.5` | `{double percent = 0.5}` |
| Именованные аргументы | Нет | `fee(percent = 1.0, amount = 10_000)` | `fee(10000, percent: 1)` |
| Лямбда | `x -> x * 2` | `{ x: Int -> x * 2 }`, один параметр — `it` | `(x) => x * 2` |
| Ссылка на метод | `String::toLowerCase` | `String::lowercase` | Имя без скобок: `print` |
| Ничего не возвращает | `void` | `Unit` (можно не писать) | `void` |

```java
// Параметров по умолчанию нет — перегрузка
static String fee(long amount) { return fee(amount, 0.5); }
static String fee(long amount, double percent) { return amount + " → комиссия " + (long) (amount * percent / 100); }
```

```kotlin
// Параметр по умолчанию вместо перегрузки; функция-выражение в одну строку
fun fee(amount: Long, percent: Double = 0.5): String = "$amount → комиссия ${(amount * percent / 100).toLong()}"
```

```console
java fee:   10000 → комиссия 50 / 10000 → комиссия 100
kotlin fee: 10000 → комиссия 50 / 10000 → комиссия 100
```

#### Коллекции

| Что | Java | Kotlin | Dart |
|-----|------|--------|------|
| Список только для чтения | `List.of("RUB", "USD")` | `listOf("RUB", "USD")` | `const ['RUB', 'USD']` |
| Изменяемый список | `new ArrayList<>(…)` | `mutableListOf(…)`, `.toMutableList()` | `['RUB', 'USD']` |
| Словарь | `Map.of("USD", 90)` | `mapOf("USD" to 90)` | `{'USD': 90}` |
| Добавить | `list.add("EUR")` | `list += "EUR"` или `add` | `list.add('EUR')` |
| Фильтр и map | `list.stream().filter(…).map(…).collect(Collectors.toList())` | `list.filter { … }.map { … }` | `list.where(…).map(…).toList()` |
| Элемент словаря | `map.get("USD")` | `map["USD"]` | `map['USD']` |

```kotlin
val fixed = listOf("RUB", "USD")                 // только чтение
val currencies = fixed.toMutableList()           // изменяемый
currencies += "EUR"
val rates = mapOf("USD" to 90, "EUR" to 98)
val lower = currencies.filter { it != "RUB" }.map { it.lowercase() }
```

```console
java collections:   [RUB, USD, EUR] 90 [usd, eur] | List.of нельзя менять
kotlin collections: [RUB, USD, EUR] 90 [usd, eur] | listOf нельзя менять
```

> ⚠️ **Внимание:** в Java на Android доступны не все методы современной Java. `Stream.toList()` (Java 16) есть только
> с Android 14 (API 34), `String.lines()` — с Android 13 (API 33): при `minSdk 24` на старых телефонах будет
> `NoSuchMethodError`. Такие вызовы находит Android Lint (`./gradlew :app:lintDebug`, проверка `NewApi`); вместо
> `toList()` — `collect(Collectors.toList())`. В Kotlin этой проблемы нет: `filter`, `map`, `lines()` — функции
> стандартной библиотеки Kotlin, они попадают в приложение вместе с ним.

В Kotlin `List` — интерфейс **только для чтения**: методов изменения у него нет. Если привести `listOf(…)` к
`MutableList` и вызвать `add`, на JVM будет `UnsupportedOperationException` — проверено.

#### Исключения

| Что | Java | Kotlin | Dart |
|-----|------|--------|------|
| Checked-исключения | Есть: `throws IOException` — компилятор заставит поймать | Нет: ловить не обязательно | Нет |
| Поймать | `try { … } catch (IOException e) { … }` | `try { … } catch (e: IOException) { … }` | `try { … } on IOException catch (e) { … }` |
| `try` как значение | Нет | `val x = try { … } catch (…) { … }` | Нет |

Из-за отсутствия checked-исключений Kotlin не напомнит, что Java-метод SDK объявляет `throws`. Читайте сигнатуры
Java-методов и ловите исключения сами.

### 3. Типы и null

#### Числа и примитивы

| Dart | Java | Kotlin | Из канала Flutter |
|------|------|--------|-------------------|
| `int` | `int` (32 бита) / `long` (64 бита) | `Int` / `Long` | До 2³¹ — `Integer`/`Int`, больше — `Long` |
| `double` | `double` | `Double` | `Double` |
| `bool` | `boolean` | `Boolean` | `Boolean` |
| `String` | `String` | `String` | `String` |
| — | Обёртки `Integer`, `Long` — объекты, могут быть `null` | Один тип `Int`; `Int?` компилируется в `Integer` | — |

В Java два мира: примитивы (`int`, не бывают `null`) и обёртки (`Integer`, могут быть `null`). В Kotlin тип один,
компилятор сам выбирает примитив или обёртку. Число из Dart берите через `Number` — так безопасно на обоих языках
(подробно — «Platform Channels», раздел 2):

```java
// Число из Dart: Integer до 2^31, Long — больше. Приводим через Number
Number amount = call.argument("amount");
```

```kotlin
val amount = call.argument<Number>("amount")?.toLong()
    ?: return result.error("BAD_ARGS", "Нет суммы", null)
```

#### Null-безопасность

| Что | Java | Kotlin | Dart |
|-----|------|--------|------|
| Тип допускает null | Любой объект (контроль — аннотации `@Nullable`) | `String?` | `String?` |
| Безопасный вызов | `s != null ? s.length() : 0` | `s?.length ?: 0` | `s?.length ?? 0` |
| Значение по умолчанию | `s != null ? s : "нет"` | `s ?: "нет"` (Elvis) | `s ?? 'нет'` |
| «Точно не null» | `Objects.requireNonNull(s)` | `s!!` | `s!` |
| Выполнить, если не null | `if (s != null) { … }` | `s?.let { … }` | `if (s != null) { … }` |
| Инициализировать позже | Поле без значения | `lateinit var token: String` | `late String token;` |

**Платформенные типы — главная ловушка совместимости.** Когда Kotlin вызывает Java-метод **без** аннотаций
nullability, он не знает, может ли вернуться `null`, и не заставляет проверять (тип `String!`):

```java
/** С аннотацией: Kotlin увидит тип String? и заставит проверить null */
@Nullable
public static String deviceIdOrNull(boolean known) { return known ? "dev-42" : null; }

/** Без аннотации: Kotlin увидит «платформенный тип» String! и не заставит проверять */
public static String legacyDeviceId(boolean known) { return known ? "dev-42" : null; }
```

```kotlin
val known: String? = AntiFraudSdk.deviceIdOrNull(false)   // @Nullable → String?, проверка обязательна
val length = known?.length ?: 0                           // ?. и ?: — как в Dart
val legacy = AntiFraudSdk.legacyDeviceId(false)           // платформенный тип String! — компилятор молчит
val id: String = legacy                                   // присвоили null в не-null тип
```

```console
kotlin null: length=0 | NullPointerException на присваивании платформенного типа
```

Kotlin вставляет проверку там, где значение попадает в не-null тип, и падает **там**, а не где-то дальше. Правило:
результат Java-метода без аннотаций сразу кладите в `String?` и проверяйте.

### 4. Классы

#### Сравнение

| Что | Java | Kotlin | Dart |
|-----|------|--------|------|
| Класс с конструктором | Поля + конструктор + геттеры руками | `class Transfer(val from: Account, val amount: Long)` | `class Transfer { Transfer(this.from, this.amount); final … }` |
| Класс данных | `record` (Java 16+) или класс на ~30 строк | `data class Account(val id: String, …)` | Вручную или `freezed` |
| Копия с изменением | Метод `withBalance(…)` руками | `a.copy(balanceKopecks = 0)` | `copyWith` руками |
| Сравнение содержимого | `a.equals(b)`; `==` — сравнение ссылок | `a == b` (вызывает `equals`); `===` — ссылки | `a == b` (если переопределён `==`) |
| Наследование | Разрешено, запрет — `final` | **Запрещено**, разрешение — `open` | Разрешено |
| Переопределить | `@Override` (желательно) | `override` (обязательно) | `@override` |
| Статические члены | `static` | `companion object { … }` | `static` |
| Синглтон | Приватный конструктор + `static` экземпляр | `object Formatter { … }` | Фабрика или верхний уровень |
| Закрытая иерархия | `sealed interface … permits` (Java 17+) | `sealed interface` / `sealed class` | `sealed class` |
| Перечисление | `enum Verdict { ALLOW, DENY }` | `enum class Currency(val symbol: String)` | `enum Currency { … }` |
| Расширение чужого класса | Нет (утилитные `static` методы) | `fun Long.asRub(): String = …` | `extension Rub on int { … }` |
| Видимость | `public`, `protected`, пакетная, `private` | `public` (по умолчанию), `internal` (модуль), `protected`, `private` | `_` — приватно для библиотеки |

#### Пример: модель счёта

Java — класс модели, всё руками:

```java
// Классический Java-класс модели: поля, конструктор, геттеры, equals/hashCode/toString — всё руками
public final class AccountPojo {
    private final String id;
    private final long balanceKopecks;

    public AccountPojo(String id, long balanceKopecks) {
        this.id = id;
        this.balanceKopecks = balanceKopecks;
    }

    public String getId() { return id; }

    public long getBalanceKopecks() { return balanceKopecks; }

    public AccountPojo withBalance(long balanceKopecks) { return new AccountPojo(id, balanceKopecks); }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof AccountPojo)) return false;
        AccountPojo other = (AccountPojo) o;
        return balanceKopecks == other.balanceKopecks && id.equals(other.id);
    }

    @Override
    public int hashCode() { return Objects.hash(id, balanceKopecks); }

    @Override
    public String toString() { return "AccountPojo{id=" + id + ", balanceKopecks=" + balanceKopecks + "}"; }
}
```

Java 16+ — `record`:

```java
// Java 16+: record — неизменяемый класс данных. Конструктор, геттеры id(), equals/hashCode/toString создаются сами
public record AccountRecord(String id, long balanceKopecks) {
    public AccountRecord {
        if (balanceKopecks < 0) throw new IllegalArgumentException("Отрицательный баланс");
    }
}
```

Kotlin — `data class`:

```kotlin
// data class: конструктор, свойства, equals/hashCode/toString/copy — одной строкой
data class Account(val id: String, val balanceKopecks: Long) {
    init {
        require(balanceKopecks >= 0) { "Отрицательный баланс" } // проверка в конструкторе
    }
}

val a = Account("40817", 125_000)
val b = a.copy(balanceKopecks = 0)                       // копия с изменением — как copyWith в Dart
val same = a == Account("40817", 125_000)                // == сравнивает содержимое (equals)
val (id, balance) = a                                    // деструктуризация data class
```

```console
Account(id=40817, balanceKopecks=125000) | 0 | equals=true/true | AccountRecord[id=40817, balanceKopecks=125000] | 40817/125000
validation: record=Отрицательный баланс, data=Отрицательный баланс
```

#### Пример: остальные виды классов в Kotlin

```kotlin
// Обычный класс: основной конструктор в заголовке, свойства через val/var
class Transfer(val from: Account, val to: Account, val amount: Long) {
    // Вторичный конструктор
    constructor(from: Account, to: Account) : this(from, to, 0)

    val isEmpty: Boolean get() = amount == 0L // вычисляемое свойство, как геттер
}

// Классы закрыты по умолчанию: наследовать можно только open
open class Card(val number: String) {
    open fun masked(): String = "*" + number.takeLast(4)
}

class VirtualCard(number: String) : Card(number) {
    override fun masked(): String = "V" + super.masked()
}

interface Notifier {
    fun send(text: String): String
    fun sendAll(texts: List<String>): String = texts.joinToString { send(it) } // метод с реализацией
}

enum class Currency(val symbol: String) { RUB("₽"), USD("$") }

// sealed: все наследники известны компилятору — when без else проверяется на полноту
sealed interface PaymentResult {
    data class Success(val id: String) : PaymentResult
    data class Declined(val reason: String) : PaymentResult
    data object Pending : PaymentResult
}

fun describe(result: PaymentResult): String = when (result) {
    is PaymentResult.Success -> "Успех ${result.id}"   // smart cast: result уже Success
    is PaymentResult.Declined -> "Отказ: ${result.reason}"
    PaymentResult.Pending -> "В обработке"
}

// object — синглтон, создаётся один раз при первом обращении
object Formatter {
    fun rub(kopecks: Long): String = "%d,%02d ₽".format(kopecks / 100, kopecks % 100)
}

class Session private constructor(val token: String) {
    // companion object — аналог static в Java. @JvmStatic — чтобы из Java звать Session.create(...)
    companion object {
        const val MAX_MINUTES = 15
        @JvmStatic fun create(token: String): Session = Session(token)
    }
}

// Функция-расширение: «добавить метод» в чужой класс без наследования
fun Long.asRub(): String = Formatter.rub(this)
```

```console
V*5678 | [a], [b] | ₽ | Отказ: лимит | В обработке | 1250,50 ₽ | t/15
```

Анонимный объект, реализующий интерфейс, — `object : Notifier { override fun send(text: String) = "[$text]" }`
(в Java — анонимный класс `new Notifier() { … }`).

### 5. Один и тот же код на двух языках

#### Обработчик MethodChannel

```java
// Обработчик MethodChannel на Java — то же, что DeviceSecurityPlugin.onMethodCall на Kotlin
public final class JavaSecurityHandler implements MethodChannel.MethodCallHandler {
    private final Context context;

    public JavaSecurityHandler(Context context) {
        this.context = context;
    }

    @Override
    public void onMethodCall(@NonNull MethodCall call, @NonNull MethodChannel.Result result) {
        switch (call.method) {
            case "isDeviceSecure": {
                KeyguardManager keyguard = context.getSystemService(KeyguardManager.class);
                result.success(keyguard.isDeviceSecure());
                break;
            }
            case "checkAmount": {
                // Число из Dart: Integer до 2^31, Long — больше. Приводим через Number
                Number amount = call.argument("amount");
                if (amount == null) {
                    result.error("BAD_ARGS", "Нет суммы", null);
                    return;
                }
                AntiFraudSdk.check(amount.longValue(), verdict -> result.success(verdict.name()));
                break;
            }
            default:
                result.notImplemented();
        }
    }
}
```

```kotlin
// Тот же обработчик на Kotlin. Для фоновой работы — корутины вместо Executor + Handler
class KotlinSecurityHandler(private val context: Context) : MethodChannel.MethodCallHandler {
    // Область корутин обработчика: по умолчанию главный поток; cancel() — при отключении от движка
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main)

    override fun onMethodCall(call: MethodCall, result: MethodChannel.Result) {
        when (call.method) {
            "isDeviceSecure" -> {
                val keyguard = context.getSystemService(KeyguardManager::class.java)
                result.success(keyguard.isDeviceSecure)
            }
            "checkAmount" -> {
                val amount = call.argument<Number>("amount")?.toLong()
                    ?: return result.error("BAD_ARGS", "Нет суммы", null)
                // Java-колбэк SDK — лямбдой (SAM-преобразование)
                AntiFraudSdk.check(amount) { verdict -> result.success(verdict.name) }
            }
            "hashStatement" -> scope.launch {
                // Тяжёлое — в фоновом пуле; после withContext снова главный поток — можно звать result
                val hash = withContext(Dispatchers.Default) {
                    (1..200_000).fold(0L) { acc, i -> (acc * 31 + i) % 1_000_000_007 }
                }
                result.success("$hash on ${Thread.currentThread().name}")
            }
            else -> result.notImplemented()
        }
    }

    fun dispose() = scope.cancel()
}
```

Что заметно при сравнении:

- Kotlin: `keyguard.isDeviceSecure` — геттер Java `isDeviceSecure()` читается как свойство.
- Kotlin: `when` без `break`; `?: return …` — ранний выход прямо в выражении.
- Kotlin: `KeyguardManager::class.java` вместо `KeyguardManager.class`.
- В обоих: лямбда вместо анонимного класса для колбэка с одним методом.

Вызов из Dart на эмуляторе — оба обработчика отвечают одинаково:

```console
ktcheck: java isDeviceSecure=true, checkAmount 1 500 ₽=ALLOW, 500 000 000 ₽=REVIEW
ktcheck: kotlin isDeviceSecure=true, checkAmount 1 500 ₽=ALLOW, 500 000 000 ₽=REVIEW
ktcheck: kotlin hashStatement=851862047 on main
```

`500 000 000 ₽` = 50 000 000 000 копеек — больше 2³¹, пришло как `Long`; через `Number` обработалось без ошибки.

#### SDK на Java с колбэком — из Kotlin

```java
// Так обычно выглядит SDK банка или вендора на Java: статический вход, колбэк-интерфейс, работа в фоне
public final class AntiFraudSdk {
    public enum Verdict { ALLOW, REVIEW, DENY }

    /** Колбэк с одним методом — из Kotlin его можно передать лямбдой (SAM-преобразование) */
    public interface Callback {
        void onResult(@NonNull Verdict verdict);
    }

    private static final ExecutorService executor = Executors.newSingleThreadExecutor();
    private static final Handler main = new Handler(Looper.getMainLooper());

    private AntiFraudSdk() {}

    public static void check(long amountKopecks, Callback callback) {
        executor.execute(() -> {                      // тяжёлая работа — в фоне
            Verdict verdict = amountKopecks > 10_000_000 ? Verdict.REVIEW : Verdict.ALLOW;
            main.post(() -> callback.onResult(verdict)); // ответ — на главном потоке
        });
    }
}
```

Из Kotlin: `AntiFraudSdk.check(amount) { verdict -> result.success(verdict.name) }` — интерфейс с одним методом
превращается в лямбду (SAM — Single Abstract Method), статический метод вызывается как обычный.

### 6. Асинхронность коротко

| Что | Java | Kotlin |
|-----|------|--------|
| Работа в фоне | `ExecutorService.execute(() -> …)` | `withContext(Dispatchers.IO / Default) { … }` |
| Вернуться на главный поток | `new Handler(Looper.getMainLooper()).post(…)` | Автоматически после `withContext`, если корутина запущена на `Dispatchers.Main` |
| Отмена | Флаги и `Future.cancel` вручную | `scope.cancel()` — отменяет все корутины области |
| Функция «может ждать» | Колбэк или `Future` | `suspend fun` |

Главное правило для плагинов то же, что в «Platform Channels»: `result` и `eventSink` — только с главного потока.
В примере `hashStatement` считается на `Dispatchers.Default`, а ответ ушёл с потока `main` — видно в логе.
Корутины подключаются библиотекой `org.jetbrains.kotlinx:kotlinx-coroutines-android`.

### 7. Совместимость Java ↔ Kotlin

| Нужно | Как |
|-------|-----|
| Вызвать из Java метод `companion object` как `static` | `@JvmStatic` (в примере: `Session.create(...)`) |
| Параметры по умолчанию видны из Java перегрузками | `@JvmOverloads fun fee(amount: Long, percent: Double = 0.5)` |
| Константа видна из Java как `static final` | `const val` или `@JvmField` |
| Kotlin правильно понимает null из Java | `@Nullable` / `@NonNull` из `androidx.annotation` в Java-коде |
| Java вызывает функцию верхнего уровня Kotlin | Через класс файла: `ModelsKt.describe(…)` |
| Геттер Java как свойство Kotlin | `getId()` → `id`, `isDeviceSecure()` → `isDeviceSecure` — автоматически |

### ⚠️ Частые ошибки

- **Результат Java-метода без аннотаций кладут в не-null тип** — `NullPointerException` в Kotlin, хотя «у Kotlin же null-безопасность».
- **`!!` «чтобы скомпилировалось»** — то же падение, только явное. Нужна обработка `null`.
- **`call.argument<Int>` / `(Integer)` для числа из Dart** — большие суммы приходят как `Long`. Брать `Number`.
- **`==` в Java для строк и объектов** — сравнивает ссылки. Нужен `equals`. В Kotlin `==` — это `equals`.
- **Нельзя наследоваться от Kotlin-класса** — классы `final` по умолчанию, нужен `open`.
- **`lateinit` читается до присваивания** — `UninitializedPropertyAccessException`.
- **Изменяемость путают со ссылкой** — `val list = mutableListOf()` можно менять, нельзя переприсвоить.
- **Checked-исключения Java-SDK не ловятся в Kotlin** — компилятор не напомнит.
- **`result` из корутины на `Dispatchers.IO`** — ответ не с главного потока.
- **Область корутин не отменяется** — работа продолжается после отключения плагина от движка.
- **`static`-состояние в Java / `companion object` в Kotlin в плагине** — общее для всех движков («Разработка плагинов», раздел 3).

### 🎤 На собеседовании: «Как Kotlin работает с null, если вызывает Java-код?»

| Уровень | Как выглядит ответ |
|---------|--------------------|
| ⭐ Junior | В Kotlin есть `String?` и `String`, операторы `?.`, `?:`, `!!` |
| ⭐⭐ Middle | Java-типы без аннотаций Kotlin видит как платформенные (`String!`): проверку не требует, ответственность на разработчике. С `@Nullable` / `@NonNull` — обычные `String?` / `String`. Результат такого вызова сразу в `String?` |
| ⭐⭐⭐ Senior | Всё из Middle, плюс: Kotlin вставляет проверку при присваивании в не-null тип и падает там (проверено); аннотации разных пакетов (`androidx.annotation`, JSR-305, JetBrains), которые понимает компилятор; при написании своей Java-обёртки — аннотировать все публичные методы; в плагине — не доверять ни Java-SDK, ни Dart: всё, что пришло извне, — nullable |

---

## ✅ Самопроверка

**⭐ Junior**
1. Чем `val` отличается от `var`? Что соответствует им в Java и Dart?
2. Как в Kotlin записать «если не null — длина, иначе 0»?
3. Чем `data class` отличается от обычного класса?

**⭐⭐ Middle**
1. Почему в Kotlin нет тернарного оператора и чем его заменить?
2. Чем `companion object` отличается от `object`? Как в Java зовут метод `companion object`?
3. Почему от Kotlin-класса по умолчанию нельзя наследоваться?
4. Почему число из `MethodCall` нужно читать как `Number`?
5. Чем Java `record` похож на Kotlin `data class` и чем отличается?

**⭐⭐⭐ Senior**
1. Что такое платформенный тип и где Kotlin упадёт, если Java вернёт `null`?
2. Как передать Java-колбэк из Kotlin лямбдой и когда это работает?
3. Как в обработчике канала сделать тяжёлую работу в фоне и ответить правильно на Java и на Kotlin?
4. Какие аннотации помогают совместимости Java ↔ Kotlin?

<details>
<summary>Ответы</summary>

**Junior**
1. `val` — ссылку нельзя переприсвоить (Java `final`, Dart `final`), `var` — можно (Java обычная переменная, Dart `var`).
2. `s?.length ?: 0`.
3. Компилятор сам создаёт `equals`, `hashCode`, `toString`, `copy` и деструктуризацию по свойствам основного
   конструктора.

**Middle**
1. `if` в Kotlin — выражение: `val max = if (a > b) a else b`. Для выбора из многих — `when`.
2. `object` — синглтон сам по себе; `companion object` — объект внутри класса, его члены зовут через имя класса.
   Из Java — `Session.Companion.create(…)` или `Session.create(…)` с `@JvmStatic`.
3. Классы `final` по умолчанию, чтобы наследование было осознанным: нужен `open` у класса и у переопределяемых методов.
4. Кодек передаёт `int` до 2³¹ как `Integer`/`Int`, больше — как `Long`. Приведение к одному типу упадёт на другом.
5. Оба — неизменяемые классы данных с автоматическими `equals`, `hashCode`, `toString`. У `record` геттеры `id()`,
   нет `copy` и деструктуризации; у `data class` — свойства `id`, `copy`, деструктуризация, можно `var`.

**Senior**
1. Тип Java-значения без аннотаций nullability (`String!`): компилятор не требует проверки. При присваивании в
   не-null тип или передаче в не-null параметр Kotlin вставляет проверку и бросает `NullPointerException` там.
2. Если Java-интерфейс содержит ровно один абстрактный метод (SAM), Kotlin принимает лямбду:
   `AntiFraudSdk.check(amount) { verdict -> … }`. Для Kotlin-интерфейсов нужен `fun interface`.
3. Java: `ExecutorService` для работы, `Handler(Looper.getMainLooper()).post` для `result`. Kotlin: корутина на
   `Dispatchers.Main`, тяжёлое — в `withContext(Dispatchers.Default/IO)`, `result` после него; область отменять
   при отключении.
4. `@Nullable` / `@NonNull` в Java; `@JvmStatic`, `@JvmOverloads`, `@JvmField`, `const val` в Kotlin.

</details>
