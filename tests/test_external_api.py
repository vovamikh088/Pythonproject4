import os

import pytest
from unittest.mock import patch, Mock
import requests
from src.external_api import calculate_transaction_amount


# Создадим фиктивный .env для тестов
@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "test_api_key")
    yield
    monkeypatch.delenv("API_KEY", raising=False)


def test_rub_transaction():
    """Тест для транзакции в рублях (без конвертации)"""
    transaction = {
        "operationAmount": {
            "amount": "500.00",
            "currency": {
                "code": "RUB"
            }
        }
    }
    assert calculate_transaction_amount(transaction) == 500.00


def test_calculate_transaction_amount_usd(mock_env):
    """Тест для транзакции в USD с мокированным API."""
    api_key = os.getenv("API_KEY")
    with patch("requests.get") as mock_get:
        # Настройка мокированных объектов
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None  # Имитация успешного ответа
        mock_response.json.return_value = {"result": 8221.37 * 90.0}  # Мокируем результат конвертации USD в RUB

        data = {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
        }
        expected_result = 8221.37 * 90.0  # Ожидаемый результат (сумма в USD * курс)
        actual_result = calculate_transaction_amount(data)

        assert actual_result == expected_result
        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=8221.37",
            headers={"apikey": api_key},
        )


def test_invalid_amount_format():
    """Тест с некорректным форматом суммы"""
    transaction = {
        "operationAmount": {
            "amount": "not_a_number",
            "currency": {
                "code": "USD"
            }
        }
    }
    assert calculate_transaction_amount(transaction) is None


def test_unsupported_currency():
    """Тест с неподдерживаемой валютой"""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "GBP"
            }
        }
    }
    assert calculate_transaction_amount(transaction) is None


def test_missing_currency_code():
    """Тест с отсутствующим кодом валюты"""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {}
        }
    }
    assert calculate_transaction_amount(transaction) is None


def test_missing_operation_amount():
    """Тест с отсутствующим operationAmount"""
    transaction = {}
    assert calculate_transaction_amount(transaction) is None


@patch('src.external_api.requests.get')
def test_api_failure(mock_get, mock_transaction):
    """Тест с ошибкой API"""
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("API Error")
    mock_get.return_value = mock_response

    with patch('src.external_api.os.getenv', return_value="test_api_key"):
        result = calculate_transaction_amount(mock_transaction)

    assert result is None


def test_invalid_amount_type():
    """Тест с некорректным типом суммы (не строка)"""
    transaction = {
        "operationAmount": {
            "amount": 100.00,  # Должно быть строкой
            "currency": {
                "code": "USD"
            }
        }
    }
    assert calculate_transaction_amount(transaction) is None
