import json
from unittest.mock import patch

from src.views import get_views


def test_get_views():
    with (
        patch("src.views.processing_function_excel"),
        patch("src.views.function_accepts_json"),
        patch("src.views.get_time_based_greeting") as mock_greeting,
        patch("src.views.get_month_date_range") as mock_month,
        patch("src.views.map_filter") as mock_map,
        patch("src.views.top_5_transactions") as mock_top_5,
        patch("src.views.exchange_rate") as mock_exchange_rate,
        patch("src.views.stock_price") as mock_stock_price,
    ):
        mock_greeting.return_value = "Доброе утро"
        mock_month.return_value = []
        mock_map.return_value = []
        mock_top_5.return_value = []
        mock_exchange_rate.return_value = []
        mock_stock_price.return_value = []
        params = get_views("2018-12-31 00:00:00")
    assert json.loads(params) == {
        "greeting": "Доброе утро",
        "cards": [],
        "top_transactions": [],
        "currency_rates": [],
        "stock_prices": [],
    }
