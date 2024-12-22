# X-MAS Hackathon
 
*MISIS PRISHVARTOVALSYA team*

Team Members:

1. **Вишневский Марк** - Data Engineer
2. **Москвин Владимир** - Analyst
3. **Рыжичкин Кирилл** - Frontend

Презентация: [тык](https://drive.google.com/)

Демонстрация веб-сервиса: [тык](https://drive.google.com/)

## Кейс "Высокоэффективный платежный конвейер"

> Необходимо разработать систему оценки уровня эксперта по резюме. Для подсчёта финальной оценки можно учитывать любые факторы, информация о которых дана в резюме. Для реализации можно использовать как готовые модели с подключением по API, так и дообучать open-source модели или создавать свои.

## Оглавление

1. [Блок-схема решения](#блок-схема-решения)
2. [Идея решения](#идея-решения)
3. [Инструкция по запуску](#инструкция-по-запуску)
4. [Наши преимущества](#наши-преимущества)

## Блок-схема решения:

![scheme](images/scheme.jpg)

## Идея решения:

### 0. Основная идея
Мы проводим транзакции через конвейер терминалов, чтобы симулировать обработку операций и подсчитать различные метрики. Каждая транзакция обрабатывается через последовательность терминалов, при этом выбираются только те терминалы, которые могут удовлетворить условиям транзакции, таким как валюта, лимит по сумме и другие параметры.

### 1. Процесс обработки транзакций
Каждая транзакция, проходящая через систему, обрабатывается следующим образом:

- Для каждой строки данных `[transaction] + [flow]` рассчитываются метрики:
  - `money_passed_in_usd` — сумма денег, прошедшая через систему в долларах США.
  - `time_spent` — время, потраченное на выполнение транзакции.
  - `success` — успешность операции.

- Для всего датасета рассчитываются:
  - Сумма `money_passed_in_usd`.
  - Сумма `time_spent`.
  - Среднее значение `success` (процент успешных операций).
  - Общий штраф `fine_in_usdt`, исходя из лимитов, которые были закрыты или не закрыты. Это штраф составляет 1% от первого лимита `LIMIT_MIN` для каждого терминала, если суммарная сумма у терминала меньше `LIMIT_MIN`.

### 2. Предобработка данных
Предобработка данных происходит следующим образом:

1. **Инициализация терминалов**:
   - Терминалы, описанные на момент времени `t = 0` (до начала транзакций), инициализируются.
   
2. **События типа "TERMINAL" и "TRANSACTION"**:
   - Записи терминалов, начиная с момента времени `t = 0`, воспринимаются как события типа "TERMINAL".
   - Каждая запись с транзакцией считается событием типа "TRANSACTION".

3. **Создание таблицы событий**:
   - Создается датафрейм, в котором события отсортированы по времени. Если в одно время поступают данные как по транзакции, так и по терминалу, терминал обновляется первым.

4. **Обработка событий**:
   - Когда все события отсортированы, данные обрабатываются по порядку:
     - Если событие типа "TERMINAL", то обновляется информация о терминале.
     - Если событие типа "TRANSACTION", то проводится обработка транзакции и рассчитываются результаты для метрик.

### 3. Функции

- **`proceed_transaction(transaction, conveyor)`**:
  Симулирует проведение транзакции через конвейер терминалов и возвращает информацию о результатах операции для подсчета метрик.

- **`create_conveyor_naive(transaction, all_terminals)`**:
  Создает конвейер из всех доступных терминалов в случайном порядке, чтобы показать наихудший вариант работы.

- **`create_conveyor(transaction, all_terminals, coeffs)`**:
  Создает конвейер из терминалов, которые могут обработать транзакцию, с учетом валюты, суммы платежа и лимита терминала по общей сумме. Также устанавливается приоритет терминалов с использованием коэффициентов.

- **`get_ids_from_conveyor(conveyor)`**:
  Возвращает список ID терминалов для заполнения столбца `flow`.

- **`terminal_random(conv)`**:
  Проверяет успех проведения транзакции через оператора с заданным коэффициентом конверсии.

- **`calculate_next_line(actual_terminals_list, last_transation, koefs)`**:
  Симуляция проведения транзакции с учетом информации о существующих терминалах. Возвращает информацию о конвейере и результатах операции.

### 4. Обработка всего датасета
Функция **`proceed_dataset(providers, ex_rates, payments, koefs)`** выполняет следующее:

- Загружает данные о терминалах, обменных курсах и платежах.
- Инициализирует терминалы на момент времени `t = 0`.
- Обрабатывает обновления терминалов и транзакции, используя коэффициенты для оптимизации работы конвейера.
- Считает метрики и сохраняет их в датафреймы.

Метрики:
 - money_passed_in_usd: Сумма, которая прошла через терминал в долларах США.
 - time_spent: Время, которое потребовалось для обработки транзакции.
 - success: Успешность выполнения транзакции.
 - success_rate: Процент успешных транзакций.
 - fee_in_usd: Платежи, которые необходимо сделать из-за лимитов по сумме.

### 5. Оптимизация
Функции **`money_optimization(k, providers, ex_rates, payments)`** и **`time_optimization(k, providers, ex_rates, payments)`** проводят оптимизацию параметров на основе сумм и времени, потраченного на операции. Они используются в **`optimization(providers, payments, ex_rates)`**, которая с помощью библиотеки `optuna` оптимизирует коэффициенты, чтобы максимизировать результаты.

- Оптимизация заключается в подборе коэффициентов, которые определяют приоритет терминалов в конвейере.
- Результаты оптимизации сохраняются и выводятся в графике.

### 6. Выводы
В результате работы системы получаем:
- Оптимизированные параметры терминалов.
- Сводные метрики по транзакциям.
- Графики и результаты оптимизации.

Также создаются файлы с результатами, например, `optimization_history.html` для отслеживания процесса оптимизации.

## Инструкция по запуску:

### Основной скрипт оптимизации цепочек:

Срипт использует argparse для передачи аргументов через командную строку. Он позволяет выбирать файлы с данными и решать, какой из наборов данных использовать для выполнения оптимизации.

Структура команд:
1. Основной синтаксис:
   ```bash
   python main.py
   ```

3. Аргументы:
   - `--providers`: Путь к CSV файлу с данными поставщиков (по умолчанию 'data\providers_1.csv').
   - `--payments`: Путь к CSV файлу с данными о платежах (по умолчанию 'data\payments_1.csv').
   - `--ex_rates`: Путь к CSV файлу с данными о валютных курсах (по умолчанию 'data\ex_rates.csv').
   - `--dataset_1`: Флаг для использования первого набора данных (если установлен, используются предрасчитанные веса для первого набора).
   - `--dataset_2`: Флаг для использования второго набора данных (если установлен, используются предрасчитанные веса для второго набора).

Пример запуска с использованием параметров:
1. Запуск с параметрами по умолчанию:
   ```bash
   python main.py
   ```
   В этом случае будут использованы файлы по умолчанию ('data\providers_1.csv', 'data\payments_1.csv', 'data\ex_rates.csv') и байесовская оптимизация будет запущена заново.

3. Запуск с указанием путей к файлам:
   ```bash
   python main.py --providers 'path\to\your\providers.csv' --payments 'path\to\your\payments.csv' --ex_rates 'path\to\your\ex_rates.csv'
   ```
   В этом случае будут использованы указанные вами пути к файлам данных и байесовская оптимизация также будет запущена с нуля.

5. Запуск с выбором первого набора данных:
   ```bash
   python main.py --dataset_1
   ```
   Здесь будут использоваться предрасчитанные веса для первого набора данных, чтобы не тратить время на повторную оптимизацию.

7. Запуск с выбором второго набора данных:
   ```bash
   python main.py --dataset_2
   ```
   Здесь будут использоваться предрасчитанные веса для второго набора данных, чтобы не тратить время на повторную оптимизацию.

### Фронтенд:

```bash
docker build -t xmas-hack-transactions .
docker run -d -p 8501:8501 xmas-hack-transactions
```

## Наши преимущества:
- байесовская оптимизация под любой датасет (не зависим от данных нам датасетов, а подстраиваемся под любой новый)
- адаптивный и удобный фронтенд
- парсинг текущих курсов валют с `exchangerate`, который можно использовать вместо статичного файла 
