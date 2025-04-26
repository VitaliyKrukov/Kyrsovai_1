import json
import re


def search_transactions(
    list_transactions: list[dict], search_bar: str
) -> list[dict]:

    if not list_transactions or not search_bar:
        return []

    pattern = re.compile(re.escape(search_bar), re.IGNORECASE)
    list_result = []

    for transactions in list_transactions:
        description = transactions.get("Описание")
        categorie = transactions.get("Категория")
        if description and pattern.search(description) or categorie and pattern.search(categorie):
            list_result.append(transactions)
    json_list_result = json.dumps(list_result, indent=4, ensure_ascii=False)
    return json_list_result


def search_by_phone_number(list_transactions: list[dict]) -> list[dict]:
    if not list_transactions:
        return []
    saerch_bar = r'(?:\+7|7|8)?[\s\-]?\(?(9\d{2}|[1-8]\d{2})\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}'
    pattern = re.compile(saerch_bar, re.IGNORECASE)
    lst_result = []
    for transactions in list_transactions:
        description = transactions.get("Описание")
        if description and pattern.search(description):
            lst_result.append(transactions)
    json_list_result = json.dumps(lst_result, indent=4, ensure_ascii=False)
    return json_list_result
