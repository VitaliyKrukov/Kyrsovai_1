# Учебный проект Python для "Bank employee".

## Описание:

Проект "Bank employee" - это веб-приложение на Python для работы с банковскими картами и счетами клиентов.

## Установка:

1. Клонируйте репозиторий:
`git clone https://github.com/VitaliyKrukov/PythonProject.git`

2. Установите зависимости:
`pip install -r requirements.txt`

3. Создайте базу данных и выполните миграции:
`python manage.py migrate`

4. Запустите локальный сервер:
`python manage.py runserver`

## Использование:

## Модуль masks
Модуль `masks` предоставляет функции для маскировки номеров банковских карт и счетов.

### Примеры использования
```python
from src.masks import get_mask_card_number, get_mask_account

# Маскировка номера карты
card_number = 7000792289606361
masked_card = get_mask_card_number(card_number)
print(masked_card)  # Вывод: 7000 79** **** 6361

# Маскировка номера счета
account_number = 73654108430135874305
masked_account = get_mask_account(account_number)
print(masked_account)  # Вывод: **4305
```
## Модуль widget
Модуль `widget` предоставляет функции для работы с банковскими картами и счетами, включая маскировку номеров и преобразование форматов дат.

## Примеры использования

### Маскировка номера карты
```python
from src.widget import mask_account_card

card_info = "Visa Platinum 7000792289606361"
masked_card = mask_account_card(card_info)
print(masked_card)  # Вывод: Visa Platinum 7000 79** **** 6361
```

### Преобразование даты
```python
from src.widget import get_date

date_string = "2024-03-11T02:26:18.671407"
formatted_date = get_date(date_string)
print(formatted_date)  # Вывод: 11.03.2024
```

## Модуль processing

Модуль предоставляет функции для работы с банковскими операциями:

- `filter_by_state`: фильтрует операции по заданному состоянию.
- `sort_by_date`: сортирует операции по дате.

### Примеры использования:

```python
from src.processing import filter_by_state, sort_by_date

operations = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 59402872, 'state': 'CANCELLED', 'date': '2018-09-17T21:27:25.241241'}
]

# Фильтрация операций с состоянием "EXECUTED"
executed_operations = filter_by_state(operations)

# Сортировка операций по дате в порядке убывания
sorted_operations = sort_by_date(operations)
```

## Модуль generators

Модуль generators предоставляет функции для работы с массивами транзакций. Он включает в себя следующие функции:

- filter_by_currency(transactions, currency): фильтрует транзакции по заданной валюте и возвращает итератор.
- transaction_descriptions(transactions): генератор, возвращающий описания транзакций.
- card_number_generator(start, stop): генератор, который выводит номера банковских карт в формате ХХХХ ХХХХ ХХХХ ХХХХ.

### Примеры использования:

```python
# Пример использования filter_by_currency
usd_transactions = filter_by_currency(transactions, 'USD')
for transaction in usd_transactions:
    print(transaction)

# Пример использования transaction_descriptions
for description in transaction_descriptions(transactions):
    print(description)

# Пример использования card_number_generator
for card in card_number_generator(4000123456789010, 4000123456789015):
    print(card)
```

## Модуль decorators

Модуль decorators предоставляет декораторы для работы с функциями. Он включает в себя следующие декораторы:

- log(filename): декоратор, который логирует работу функции.

### Примеры использования:
```python
@log(filename="mylog.txt")
def my_function(x, y):
    return x + y
my_function(1, 2)
```

## Модуль utils

Этот модуль содержит функции для работы с JSON-файлами, включая чтение данных о финансовых транзакциях.

### Пример использования:
```python
from src.utils import function_accepts_json

transactions = function_accepts_json('data/operations.json')
print(transactions)
```
## Модуль external_api

Этот модуль содержит функции для конвертации валют с использованием внешнего API.

### Пример использования:
```python
from src.external_api import return_amount

transaction = {
    "amount": "100",
    "currency": "USD"
}

amount_in_rub = return_amount(transaction)
print(amount_in_rub)
```
## Настройка файла .env

Для работы с внешними API необходимо создать файл `.env` в корне проекта и добавить в него следующие переменные окружения:

```
API_KEY=ваш_ключ_доступа
API_URL=https://api.example.com
```

Убедитесь, что файл `.env` добавлен в `.gitignore`, чтобы избежать случайного попадания конфиденциальной информации в репозиторий.

## Модуль file_processing

### Модуль для работы с CSV и Excel файлами

- `read_transactions_from_csv(file_path: str) -> List[Dict]`: Считывает финансовые операции из CSV файла и возвращает список словарей с транзакциями.
- `read_transactions_from_excel(file_path: str) -> List[Dict]`: Считывает финансовые операции из Excel файла и возвращает список словарей с транзакциями.

### Примеры использования

```python
from my_module import read_transactions_from_csv, read_transactions_from_excel

# Пример использования функции для CSV
transactions_csv = read_transactions_from_csv('path/to/transactions.csv')
print(transactions_csv)

# Пример использования функции для Excel
transactions_excel = read_transactions_from_excel('path/to/transactions.xlsx')
print(transactions_excel)
```

## Модуль main
Функция main реализована головная функция, отвечающая за общую логику проекта, 
связывающая остальные функциональности между собой.

## Логирование
Добавлено сохранение логов в файл для модулей masks, utils. Логи сохранены в директории logs в корне проекта.

## Тестирование
Этот раздел описывает, как запускать тесты для модуля. Мы используем pytest в качестве фреймворка для тестирования.

### Установка зависимостей для тестирования
Перед запуском тестов убедитесь, что установлены все необходимые зависимости. Вы можете установить их с помощью файла requirements.txt или вручную:

### Установите зависимости для тестирования
`pip install -r requirements.txt`

### Или установите pytest вручную
`pip install pytest`
### Запуск тестов
Чтобы запустить все тесты, выполните следующую команду в корневой директории проекта:

`pytest tests/`

Если вы хотите запустить конкретный тестовый файл или тестовую функцию, используйте:

### Запуск конкретного тестового файла
`pytest tests/test_my_module.py`

### Покрытие кода (Coverage)
Если вы хотите измерить покрытие кода тестами, установите `pytest-cov` и запустите тесты с параметром `--cov`:

`pip install pytest-cov`
`pytest --cov=my_module tests/`

## Документация:

Дополнительную информацию о структуре проекта и API можно найти в [документации](docs/README.md).

## Лицензия:

Проект распространяется под [лицензией MIT](LICENSE).
