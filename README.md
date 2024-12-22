# X-MAS Hackathon
 
*MISIS PRISHVARTOVALSYA team*

Team Members:

1. **Вишневский Марк** - Data Engineer
2. **Москвин Владимир** - Analyst
3. **Рыжичкин Кирилл** - Frontend

Презентация: [тык](https://drive.google.com/)

Демонстрация веб-сервиса: [тык](https://drive.google.com/)

Демонстрация Swagger: [тык](https://drive.google.com/)

## Кейс "Высокоэффективный платежный конвейер"

> Необходимо разработать систему оценки уровня эксперта по резюме. Для подсчёта финальной оценки можно учитывать любые факторы, информация о которых дана в резюме. Для реализации можно использовать как готовые модели с подключением по API, так и дообучать open-source модели или создавать свои.

## Оглавление

...

## Блок-схема решения:

...

## Идея решения:



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

...

## Структура репозитория

...
