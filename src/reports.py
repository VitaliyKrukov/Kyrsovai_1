import logging
import os
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd


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


def func_write(filename="File_reports"):
    """Декоратор записи."""
    def wrapper(func):
        def decorator(*args, **kwargs):
            result = func(*args, **kwargs)
            result.to_json(filename, orient='records', force_ascii=False, indent=4)
            logger.info(f"записываем данные в {filename}")
            return result
        return decorator
    return wrapper


@func_write("file_reports")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция, принимающая датафрайм, категорию и дату и возвращающая данные за 3 месяца до указанной даты."""
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], dayfirst=True)
    date = pd.to_datetime(date)
    start_date = date - timedelta(days=90)
    filter_data = (transactions["Дата платежа"] >= start_date) & (transactions["Дата платежа"] <= date)
    if category:
        filter_data &= transactions["Категория"] == category
    filtered = transactions.loc[filter_data]
    logger.info(f"возвращаем данные за 3 месяца до указанной даты")
    return filtered


# df = pd.read_excel("..\\data\\operations.xlsx")


#print(spending_by_category(pd.read_excel("..\\data\\operations.xlsx"), "Супермаркеты", "2021-12-12 00:00:00"))

