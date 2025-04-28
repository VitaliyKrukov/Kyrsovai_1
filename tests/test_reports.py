import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category():
    df = pd.DataFrame([{'Дата платежа': "31.12.2021 16:44:00", 'Категория': "Супермаркеты"}])
    assert spending_by_category(df, "Супермаркеты", "31.12.2021 16:44:00").to_dict(orient='records') == [{
        'Дата платежа': "31.12.2021 16:44:00", 'Категория': "Супермаркеты"}]
