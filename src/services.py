from src.services_utils import search_by_phone_number, search_transactions
from src.utils import processing_function_excel


def get_services() -> None:
    """Общая функция для получения сервисов"""
    print("Выберите номер сервисной функции")
    print("1 - Простой поиск")
    print("2 - Поиск по номеру телефона")
    while True:
        user_input = input().strip()
        if user_input in ("1", "2"):
            break
        else:
            print("Введите 1 или 2")
    if user_input == "1":
        print("Введите слово поиска")
        while True:
            user_word = input().strip()
            if user_word:
                break
            else:
                print("Слово не должно быть пустым")
        print(search_transactions(processing_function_excel("..\\data\\operations.xlsx"), user_word))
    elif user_input == "2":
        print(search_by_phone_number(processing_function_excel("..\\data\\operations.xlsx")))
