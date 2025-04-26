import json
import os
from unittest.mock import patch

import pytest
import requests

from src.utils import processing_function_excel, get_time_based_greeting, map_filter, top_5_transactions, \
    function_accepts_json, get_month_date_range, exchange_rate, stock_price


@patch("pandas.read_excel")
def test_processing_function_excel(test_mock_excel, data_frame):
    test_mock_excel.return_value = data_frame
    assert processing_function_excel("") == data_frame.to_dict("records")


@patch("pandas.read_excel")
def test_processing_function_excel_wrong_value(test_mock_excel):
    test_mock_excel.side_effect = ValueError
    assert processing_function_excel("") == []


def test_processing_function_excel_open():
    assert processing_function_excel("") == []


def test_get_month_date_range(excel_list_dict):
    input_data = "2021-12-31 23:59:59"
    assert get_month_date_range(excel_list_dict, input_data) == excel_list_dict


def test_get_month_date_range_nothing():
    input_data = "2021-12-31 23:59:59"
    assert get_month_date_range([], input_data) == []


@pytest.mark.parametrize("hour, expected", [
    (5, "Доброе утро"),
    (12, "Добрый день"),
    (17, "Добрый вечер"),
    (22, "Доброй ночи"),
])
def test_get_time_based_greeting_with_mock(hour, expected):
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value.hour = hour
        assert get_time_based_greeting() == expected


def test_map_filter(excel_list_dict):
    assert map_filter(excel_list_dict) == [{'last_digits': '7197', 'total_spent': 421.06, 'cashback': 2},
                                           {'last_digits': '5091', 'total_spent': 564.0, 'cashback': 5}]


def test_map_filter_nothing():
    assert map_filter([]) == []


def test_top_5_transactions(excel_list_dict):
    assert top_5_transactions(excel_list_dict) == [
        {'date': '31.12.2021', 'amount': 564.0, 'category': 'Различные товары', 'description': 'Ozon.ru'},
        {'date': '31.12.2021', 'amount': 160.89, 'category': 'Супермаркеты', 'description': 'Колхоз'},
        {'date': '31.12.2021', 'amount': 118.12, 'category': 'Супермаркеты', 'description': 'Магнит'},
        {'date': '31.12.2021', 'amount': 78.05, 'category': 'Супермаркеты', 'description': 'Колхоз'},
        {'date': '31.12.2021', 'amount': 64.0, 'category': 'Супермаркеты', 'description': 'Колхоз'}]


def test_top_5_transactions_nothing():
    assert top_5_transactions([]) == []


def test_function_accepts_json(file_name):
    data = {'Дата операции': '31.12.2021 16:44:00', 'Дата платежа': '31.12.2021', 'Номер карты': '*7197',
            'Статус': 'OK',
            'Сумма операции': -160.89, 'Валюта операции': 'RUB', 'Сумма платежа': -160.89, 'Валюта платежа': 'RUB',
            'Кэшбэк': '', 'Категория': 'Супермаркеты', 'MCC': 5411.0, 'Описание': 'Колхоз',
            'Бонусы (включая кэшбэк)': 3,
            'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 160.89}

    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file)
    assert function_accepts_json(file_name) == data
    os.remove(file_name)


def test_function_accepts_json_type(file_name):
    data = [
        {'Дата операции': '31.12.2021 16:44:00', 'Дата платежа': '31.12.2021', 'Номер карты': '*7197', 'Статус': 'OK',
         'Сумма операции': -160.89, 'Валюта операции': 'RUB', 'Сумма платежа': -160.89, 'Валюта платежа': 'RUB',
         'Кэшбэк': '', 'Категория': 'Супермаркеты', 'MCC': 5411.0, 'Описание': 'Колхоз', 'Бонусы (включая кэшбэк)': 3,
         'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 160.89}]
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file)
    assert function_accepts_json(file_name) == {}
    os.remove(file_name)


def test_function_accepts_json_open(file_name):
    assert function_accepts_json("") == {}


def test_function_accepts_json_error(file_name):
    data = {'Дата операции': '31.12.2021 16:44:00', 'Дата платежа': '31.12.2021', 'Номер карты': '*7197',
            'Статус': 'OK',
            'Сумма операции': -160.89, 'Валюта операции': 'RUB', 'Сумма платежа': -160.89, 'Валюта платежа': 'RUB',
            'Кэшбэк': '', 'Категория': 'Супермаркеты', 'MCC': 5411.0, 'Описание': 'Колхоз',
            'Бонусы (включая кэшбэк)': 3,
            'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 160.89}

    with open(file_name, "w", encoding="utf-8") as file:
        file.write(str(data))
    assert function_accepts_json(file_name) == {}
    os.remove(file_name)


@patch("requests.get")
def test_exchange_rate(test_mock_get):
    data = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    }
    test_mock_get.return_value.json.return_value = {
        "base": "USD",
        "date": "2021-03-17",
        "rates": {
            "EUR": 0.813399,
            "GBP": 0.72007,
            "JPY": 107.346001
        },
        "success": 'true',
        "timestamp": 1519296206
    }
    test_mock_get.return_value.status_code = 200
    assert exchange_rate(data) == [{'currency': 'EUR', 'rate': 1.23},
                                   {'currency': 'GBP', 'rate': 1.39},
                                   {'currency': 'JPY', 'rate': 0.01}]


@patch("requests.get")
def test_exchange_rate_exept(test_mock_get, capsys):
    data = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    }
    test_mock_get.side_effect = requests.exceptions.RequestException
    assert exchange_rate(data) == []


@patch("requests.get")
def test_exchange_rate_status_code(test_mock_get, capsys):
    data = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    }
    test_mock_get.return_value.status_code = 100
    assert exchange_rate(data) == []


@patch("requests.get")
def test_stock_price(test_mock_get):
    data = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    }
    test_mock_get.return_value.json.return_value = {'AAPL': {'price': '209.28000'},
                                                    'AMZN': {'price': '188.99001'},
                                                    'GOOGL': {'price': '161.96001'},
                                                    'MSFT': {'price': '391.85001'},
                                                    'TSLA': {'price': '284.95001'}}
    test_mock_get.return_value.status_code = 200
    assert stock_price(data) == [{'price': 209.28, 'stock': 'AAPL'},
                                 {'price': 188.99, 'stock': 'AMZN'},
                                 {'price': 161.96, 'stock': 'GOOGL'},
                                 {'price': 391.85, 'stock': 'MSFT'},
                                 {'price': 284.95, 'stock': 'TSLA'}]


@patch("requests.get")
def test_stock_price_exept(test_mock_get, capsys):
    data = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    }
    test_mock_get.side_effect = requests.exceptions.RequestException
    assert stock_price(data) == []


@patch("requests.get")
def test_stock_price_status_code(test_mock_get, capsys):
    data = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    }
    test_mock_get.return_value.status_code = 100
    assert stock_price(data) == []
