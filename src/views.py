import json

from src.utils import processing_function_excel, get_time_based_greeting, map_filter, top_5_transactions, \
    function_accepts_json, exchange_rate, get_month_date_range, stock_price


def get_views(date: str) -> str:
    """Функция, создающая словарь в требуемом формате"""
    read_excel = processing_function_excel("..\\data\\operations.xlsx")
    read_json = function_accepts_json('..\\user_settings.json')
    greeting = get_time_based_greeting()
    range_transactions = get_month_date_range(read_excel, date)
    cards = map_filter(range_transactions)
    top_transactions = top_5_transactions(range_transactions)
    currency_rates = exchange_rate(read_json)
    stock_prices = stock_price(read_json)
    dct_result = {"greeting": greeting,
                  "cards": cards,
                  "top_transactions": top_transactions,
                  "currency_rates": currency_rates,
                  "stock_prices": stock_prices
    }
    return json.dumps(dct_result, ensure_ascii=False, indent=4)
