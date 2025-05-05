from unittest.mock import patch

from src.services import get_services
from src.services_utils import search_by_phone_number, search_transactions


def test_get_services_1(list_search, capsys):
    with patch("builtins.input") as mock_input, patch("src.services.processing_function_excel") as mock_excel:
        mock_input.side_effect = ["3", "1", "", "Колхоз"]
        mock_excel.return_value = list_search
        get_services()
    params = capsys.readouterr().out
    assert '"Описание": "Колхоз"' in params


def test_get_services_2(list_search, capsys):
    with patch("builtins.input") as mock_input, patch("src.services.processing_function_excel") as mock_excel:
        mock_input.return_value = "2"
        mock_excel.return_value = list_search
        get_services()
        params = capsys.readouterr().out
        assert '"Описание": "МТС +7 981 976-14-20"' in params


def test_search_transactions():
    assert search_transactions([], "") == ""


def test_search_by_phone_number():
    assert search_by_phone_number([]) == ""
