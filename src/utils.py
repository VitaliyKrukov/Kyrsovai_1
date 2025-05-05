import json
import logging
import os
from datetime import datetime
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

logger = logging.getLogger("utils")
file_handler = logging.FileHandler(
    os.path.join(os.path.dirname(__file__), "..\\logs\\", "utils.log"),
    mode="w",
    encoding="utf-8",
)
file_formatter = logging.Formatter("%(asctime)s %(module)s.%(funcName)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def processing_function_excel(file_path: str) -> list[dict]:
    """Функция, которая принимает путь файла excel
    и обрабатывает в список словарей"""
    try:
        reader = pd.read_excel(file_path)
        reader = reader.fillna(value="")
    except FileNotFoundError as e:
        logger.error(f"{e}")
        return []
    except ValueError as e:
        logger.error(f"{e}")
        return []
    transact = reader.to_dict("records")
    logger.info("выводим обработанный файл")
    return transact


def get_month_date_range(lst_transaction: list[dict], input_date_str: str) -> list[Any]:
    """Возвращает диапазон дат с 1-го дня месяца входной даты по саму дату."""

    if isinstance(input_date_str, str):
        input_date = datetime.strptime(input_date_str, "%Y-%m-%d %H:%M:%S")
    first_day_of_month = input_date.replace(day=1)
    month_date_range = []
    for transaction in lst_transaction:
        if not str(transaction["Дата платежа"]).strip():
            continue
        date_transaction = datetime.strptime(str(transaction["Дата платежа"]), "%d.%m.%Y")
        if first_day_of_month <= date_transaction <= input_date:
            month_date_range.append(transaction)
    logger.info("выводим обработанные данные")
    return month_date_range


def get_time_based_greeting() -> str:
    """Возвращает приветствие в зависимости от текущего времени"""
    present_date = datetime.now().hour

    if 5 <= present_date < 12:
        logger.info("Выводим доброе утро")
        return "Доброе утро"
    elif 12 <= present_date < 17:
        logger.info("Выводим добрый день")
        return "Добрый день"
    elif 17 <= present_date < 22:
        logger.info("Выводим добрый вечер")
        return "Добрый вечер"
    else:
        logger.info("Выводим доброй ночи")
        return "Доброй ночи"


def map_filter(transactions: list[dict]) -> list[dict]:
    """Функция, которая отображает последние 4 цифры карты,
    общую сумму расходов и кешбэк"""
    lis_transactions = []
    result: dict[str, list] = {}
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
    logger.info("Выводим обработанные данные")
    return lis_transactions


def top_5_transactions(transactions: list[dict]) -> list[dict]:
    """Функция возвращает новый список, отсортированный по Сумме платежей"""
    sorted_list = sorted(transactions, key=lambda x: x.get("Сумма платежа", ""))
    result = sorted_list[0:5]
    lis_transactions = []
    for res_transaction in result:
        dct_transaction = {
            "date": res_transaction["Дата операции"][0:10],
            "amount": abs(res_transaction["Сумма платежа"]),
            "category": res_transaction["Категория"],
            "description": res_transaction["Описание"],
        }
        lis_transactions.append(dct_transaction)
    logger.info("Выводи отсортированные данные по сумме платежей")
    return lis_transactions


def function_accepts_json(file_name: str) -> dict:
    """Функция обрабатывающая json файл"""
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            try:
                file_dct = json.load(file)
                if type(file_dct) is not dict:
                    logger.critical(f"Проверка {file_dct} на словарь")
                    return {}
                logger.info(f"Вернул обработанный {file_name} в формате python")
                return file_dct
            except json.JSONDecodeError as e:
                logger.error(f"{e}")
                return {}
    except FileNotFoundError as e:
        logger.error(f"{e}")
        return {}


def exchange_rate(user_data: dict) -> list[dict]:
    """Функция отображающая курс валют"""
    load_dotenv()
    api_key = os.getenv("API_KEY")
    url = (
        f"https://api.apilayer.com/exchangerates_data/latest?symbols={",".join(user_data["user_currencies"])}&base=RUB"
    )
    headers = {"apikey": api_key}
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        logger.error(f"{e}")
        return []
    if response.status_code != 200:
        logger.critical(f"Ошибка проверки на статус кода {response.status_code}")
        return []
    responses = response.json().get("rates", {})
    list_responses = []
    for key, value in responses.items():
        dct_responses = {}
        dct_responses["currency"] = key
        dct_responses["rate"] = round(1 / float(value), 2)
        list_responses.append(dct_responses)
    logger.info(f"Выводим результат запроса{list_responses}")
    return list_responses


def stock_price(user_data: dict[str, list]) -> list[dict]:
    """Функция отображающая курс акций"""
    stock = user_data.get("user_stocks", [])
    load_dotenv()
    api_key = os.getenv("API_KEY_2")
    API_KEY = api_key
    url = f"https://api.twelvedata.com/price?symbol={','.join(stock)}&apikey={API_KEY}"
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        logger.error(f"{e}")
        return []
    if response.status_code != 200:
        logger.critical(f"Ошибка проверки на статус кода {response.status_code}")
        return []
    data = response.json()
    lis_stocks = []
    for key, value in data.items():
        dct_stock = {}
        dct_stock["stock"] = key
        dct_stock["price"] = round(float(value.get("price", 0)), 2)
        lis_stocks.append(dct_stock)
    logger.info(f"Выводим результат запроса{lis_stocks}")
    return lis_stocks
