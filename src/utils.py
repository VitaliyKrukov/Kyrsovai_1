import os
from datetime import datetime

import pandas as pd
from mypy.build import compute_hash


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


def get_month_date_range(input_date):
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


def get_time_based_greeting():
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


def return_amount(transaction):
    """Функция отображающая курс валют"""
    curancy = transaction["operationAmount"]["currency"]["code"]
    amount = transaction["operationAmount"]["amount"]
    if curancy == "RUB":
        return float(amount)
    else:
        load_dotenv()
        api_key = os.getenv("API_KEY")
        url = (
            f"https://api.apilayer.com/exchangerates_data/convert"
            f"?to=RUB&from={curancy}&amount={amount}"
        )
        headers = {"apikey": api_key}
        try:
            respons = requests.get(url, headers=headers)
        except requests.exceptions.RequestException:
            print("ошибка http запроса")
            return 0.0
        else:
            if respons.status_code != 200:
                print("ошибка кода")
                return 0.0
            info = respons.json()
            return float(info["result"])
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



def map_filter(transactions):
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
