import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category():
    df = pd.DataFrame([{"Дата платежа": "2021.12.31", "Категория": "Супермаркеты"}])
    assert spending_by_category(df, "Супермаркеты", "2021-12-31 00:00:00").to_dict(orient="records") == [
        {"Дата платежа": "2021.12.31", "Категория": "Супермаркеты"}
    ]
