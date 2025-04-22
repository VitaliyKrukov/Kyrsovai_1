import json
import os
from datetime import datetime

import pandas as pd
import logging

import requests
from dotenv import load_dotenv


logger = logging.getLogger("utils")
file_handler = logging.FileHandler(
    os.path.join(os.path.dirname(__file__), "..\\logs\\", "utils.log"),
    mode="w",
    encoding="utf-8",
)
file_formatter = logging.Formatter(
    "%(asctime)s %(module)s.%(funcName)s %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def processing_function_excel(file_path: str) -> list[dict]:
    """Функция, которая принимает путь файла excel
    и обрабатывает в список словарей"""
    try:
        reader = pd.read_excel(file_path)
        reader = reader.fillna(value="")
    except FileNotFoundError:
        return []
    except ValueError:
        return []
    transact = reader.to_dict("records")
    return transact


print(processing_function_excel("..\\data\\operations.xlsx")[0:5])

data = {'Дата операции': '31.12.2021 16:44:00',
        'Дата платежа': '31.12.2021',
        'Номер карты': '*7197',
        'Статус': 'OK',
        'Сумма операции': -160.89,
        'Валюта операции': 'RUB',
        'Сумма платежа': -160.89,
        'Валюта платежа': 'RUB',
        'Кэшбэк': '',
        'Категория': 'Супермаркеты',
        'MCC': 5411.0,
        'Описание': 'Колхоз',
        'Бонусы (включая кэшбэк)': 3,
        'Округление на инвесткопилку': 0,
        'Сумма операции с округлением': 160.89}


def get_month_date_range(input_date:str)->tuple:
    """Возвращает диапазон дат с 1-го дня месяца входной даты по саму дату."""

    if isinstance(input_date, str):
        input_date = datetime.strptime(input_date, "%d.%m.%Y")

    first_day_of_month = input_date.replace(day=1)

    start_date_str = first_day_of_month.strftime("%d.%m.%Y")
    end_date_str = input_date.strftime("%d.%m.%Y")

    return start_date_str, end_date_str

input_data = "12.12.2012"
one_date, two_date = get_month_date_range(input_data)
print(f"период дат: {one_date}, {two_date}")


def get_time_based_greeting()->str:
    """Возвращает приветствие в зависимости от текущего времени"""
    present_date = datetime.now().hour

    if 5 <= present_date < 12:
        return "Доброе утро"
    elif 12 <= present_date < 17:
        return "Добрый день"
    elif 17 <= present_date < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"

print(get_time_based_greeting())


def map_filter(transactions:list[dict]) -> list[dict]:
    """Функция котрая отоброжает последние 4 цифры карты,
    общую сумму расходов и кешбэк"""
    lis_transactions = []
    result = {}
    for transaction in transactions:
        num_card = transaction.get("Номер карты")
        amount_operation = transaction.get("Сумма операции")
        if (num_card and amount_operation) and amount_operation < 0:
            amount_operation = abs(amount_operation)
            if num_card in result:
                result[num_card][0] += amount_operation
                result[num_card][1] += amount_operation // 100
            else:
                result[num_card] = [amount_operation, amount_operation // 100]
    for key, value in result.items():

        dict_temper = {
            "last_digits": key[-4:],
            "total_spent": round(value[0], 2),
            "cashback": int(value[1]),
        }
        lis_transactions.append(dict_temper)

    return lis_transactions


print(map_filter(processing_function_excel("..\\data\\operations.xlsx")))


def top_5_transactions(
    transactions: list[dict], direction: bool = True
) -> list[dict]:
    """Функция возвращает новый список, отсортированный по Сумме платежей"""
    sorted_list = sorted(
        transactions, key=lambda x: str(x.get("Сумма платежа", "")))
    result = sorted_list[0:5]
    lis_transactions = []
    for res_transaction in result:
        dct_transaction = {"date": res_transaction["Дата операции"][0:10],
        "amount": res_transaction["Сумма платежа"],
        "category": res_transaction["Категория"],
        "description": res_transaction["Описание"]}
        lis_transactions.append(dct_transaction)
    return lis_transactions

print(top_5_transactions(processing_function_excel("..\\data\\operations.xlsx")))


def function_accepts_json(file_name: str) -> dict:
    """Функция обрабатывающая json файл"""
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            try:
                file_dct = json.load(file)
                if type(file_dct) is not dict:
                    logger.critical(f"Проверка {file_dct} на словарь")
                    return {}
                logger.info(
                    f"Вернул обработанный {file_name} в формате python"
                )
                return file_dct
            except json.JSONDecodeError as e:
                logger.error(f"{e}")
                return {}
    except FileNotFoundError as e:
        logger.error(f"{e}")
        return {}


def exchange_rate(user_data: dict, requests=None)->list[dict]:
    """Функция отображающая курс валют"""
    curancy = user_data["user_currencies"]

    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={curancy}&base=RUB"
    payload = {}
    headers= {
      "apikey": "wlZ7nTggLZ2OKRXkuenEJ96LTXGGTWSG"
    }
    # try:
    response = requests.get(url, headers=headers, data = payload)
    # except requests.exceptions.RequestException:
    #     print("ошибка http запроса")
    #     return 0.0
    # if response.status_code != 200:
    #     print("ошибка кода")
    #     return 0.0
    # info = response.json()
    return response

print(exchange_rate(function_accepts_json("..\\user_settings.json")))





# import requests
#
# response = requests.get("https://api.twelvedata.com/time_series?apikey=5f8c818123fd470584a9c926bcc4f89a&interval=1day&start_date=2025-04-09 21:24:00&end_date=2025-04-19 21:24:00&dp=2&outputsize=12&format=JSON&symbol=AAPL")
#
# print(response.text)

# {
# 	"meta": {
# 		"symbol": "AAPL",
# 		"interval": "1day",
# 		"currency": "USD",
# 		"exchange_timezone": "America/New_York",
# 		"exchange": "NASDAQ",
# 		"mic_code": "XNGS",
# 		"type": "Common Stock"
# 	},
# 	"values": [
# 		{
# 			"datetime": "2025-04-17",
# 			"open": "197.20",
# 			"high": "198.83",
# 			"low": "194.42",
# 			"close": "196.98",
# 			"volume": "51334300"
# 		}]}


# import requests
#
# url = "https://api.apilayer.com/exchangerates_data/latest?symbols=USD%2CEUR&base=RUB"
#
# payload = {}
# headers= {
#   "apikey": "wlZ7nTggLZ2OKRXkuenEJ96LTXGGTWSG"
# }
#
# response = requests.request("GET", url, headers=headers, data = payload)
#
# status_code = response.status_code
# result = response.text


# {
#   "base": "RUB",
#   "date": "2025-04-20",
#   "rates": {
#     "EUR": 0.010701, / 1
#     "USD": 0.012169 / 1
#   },
#   "success": true,
#   "timestamp": 1745174954
# }
