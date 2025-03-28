from unittest.mock import mock_open, patch
import pandas as pd
from src.transaction_reader import csv_to_list, xlsx_to_list


def test_csv_to_list_success():
    """Тест для успешного чтения CSV файла."""
    csv_data = "header1,header2\nvalue1,value2\nvalue3,value4"
    mock_file = mock_open(read_data=csv_data)

    with patch("builtins.open", mock_file):
        data = csv_to_list("dummy_path.csv")
        assert data == [{"header1": "value1", "header2": "value2"}, {"header1": "value3", "header2": "value4"}]


def test_csv_to_list_file_not_found():
    """Тест для обработки FileNotFoundError."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        data = csv_to_list("nonexistent_file.csv")
        assert data == []


def test_csv_to_list_generic_exception():
    """Тест для обработки общего исключения при чтении файла."""
    with patch("builtins.open", side_effect=Exception("Generic error")):
        data = csv_to_list("faulty_file.csv")
        assert data == []


def test_xlsx_to_list_success():
    """Тест для успешного чтения XLSX файла."""
    # Создаем DataFrame в памяти и мокаем read_excel, чтобы возвращать его
    data = {"col1": [1, 2], "col2": [3, 4]}
    df = pd.DataFrame(data)

    with patch("pandas.read_excel", return_value=df):
        result = xlsx_to_list("dummy_file.xlsx")
        assert result == [[1, 3], [2, 4]]


def test_xlsx_to_list_file_not_found():
    """Тест для обработки FileNotFoundError при чтении XLSX."""
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        result = xlsx_to_list("nonexistent_file.xlsx")
        assert result == []


def test_xlsx_to_list_generic_exception():
    """Тест для обработки общего исключения при чтении XLSX."""
    with patch("pandas.read_excel", side_effect=Exception("Generic error")):
        result = xlsx_to_list("faulty_file.xlsx")
        assert result == []
