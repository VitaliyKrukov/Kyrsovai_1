import re

import pandas as pd

from src.reports import spending_by_category
from src.services import get_services
from src.views import get_views


def main()->None:
    """Общая функция объеденяющая функции"""
    print("Выберите номер функции котора вам необходима")
    print("1 - Главная")
    print("2 - Поиск по ключевому слову описания или по номерам телефонов")
    print("3 - Отчет за 3 месяца по указанной дате, а так же запись в отдельный файл")
    while True:
        user_input = input().strip()
        if user_input in ("1", "2", "3"):
            break
        else:
            print("Введите 1, 2 или 3")
    if user_input == "1":
        print("Введите дату по которой будет найдена информация на примере 2021-12-12 00:00:00")
        while True:
            user_date = input().strip()
            if user_date and re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', user_date):
                break
            else:
                print("Слово не должно быть пустым")
        print(get_views( user_date))
    elif user_input == "2":
        get_services()
    elif user_input == "3":
        print("Введите категорию по которой будет обработан отчет")
        while True:
            user_category = input().strip()
            if user_category:
                break
            else:
                print("Слово не должно быть пустым")
        print("Введите дату по которой будет обработан отчет на примере 2021-12-12 00:00:00")
        while True:
            user_date = input().strip()
            if user_date and re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', user_date):
                break
            else:
                print("Слово не должно быть пустым")
        print(spending_by_category(pd.read_excel("..\\data\\operations.xlsx"), user_category, user_date))

if __name__ == "__main__":
    main()