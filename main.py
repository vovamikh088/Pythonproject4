from typing import Any, Dict, List, Optional, Union

from src import filter_by_state, sort_by_date
from src import get_date, mask_account_card
from src import transaction_descriptions, filter_by_currency


def process_operations(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Обрабатывает список операций: фильтрует выполненные, сортирует по дате и маскирует данные.

    Args:
        operations (List[Dict[str, Any]]): Список операций.

    Returns:
        List[Dict[str, Any]]: Список обработанных операций.
    """
    executed_operations = filter_by_state(operations)
    return list(sort_by_date(executed_operations))


def format_operation(operation: Dict[str, Any]) -> str:
    """Форматирует информацию об операции в строку."""
    date = operation.get("date")
    description = operation.get("description")
    from_account = operation.get("from")
    to_account = operation.get("to")
    amount = operation.get("operationAmount", {}).get("amount")
    currency_name = operation.get("operationAmount", {}).get("currency", {}).get("name")

    if not all([date, description, to_account, amount, currency_name]):
        return ""

    formatted_date = get_date(str(date))
    masked_from_account = mask_account_card(str(from_account)) if from_account else "Счет отправителя не указан"
    masked_to_account = mask_account_card(str(to_account))

    return (
        f"{formatted_date} {description}\n"
        f"{masked_from_account} -> {masked_to_account}\n"
        f"{amount} {currency_name}\n"
    )


def display_last_operations(operations: List[Dict[str, Any]], num_operations: int = 5, currency_filter: str = None) -> None:
    """
    Выводит информацию о последних нескольких операциях.

    Args:
        operations (List[Dict[str, Any]]): Список операций.
        num_operations (int): Количество операций для вывода. По умолчанию 5.
        currency_filter (str): Фильтр для валюты. Если есть
    """
    processed_operations = process_operations(operations)
    if currency_filter:
        processed_operations = list(filter_by_currency(processed_operations, currency_filter))

    for operation in processed_operations[:num_operations]:
        formatted_operation = format_operation(operation)
        if formatted_operation:
            print(formatted_operation)
            print()

def get_operation_descriptions(operations: List[Dict[str, Any]]) -> List[str]:
    """Извлекает описания всех операций."""
    return list(transaction_descriptions(operations))

if __name__ == "__main__":
    test_data = [
        {"id": 441945886345507595, "state": "EXECUTED", "date": "2019-12-07T06:15:55.770387", "description": "Перевод организации", "operationAmount": {"amount": "1000", "currency": {"name": "RUB", "code": "RUB"}}},
        {"id": 70721515976355673, "state": "EXECUTED", "date": "2018-03-03T02:26:14.430106", "description": "Перевод организации", "operationAmount": {"amount": "2000", "currency": {"name": "USD", "code": "USD"}}},
        {"id": 929468254717360747, "state": "CANCELED", "date": "2016-06-24T10:15:27.329734", "description": "Перевод организации", "operationAmount": {"amount": "3000", "currency": {"name": "EUR", "code": "EUR"}}},
        {"id": 579556847517945845, "state": "EXECUTED", "date": "2018-06-30T01:08:58.093740", "description": "Перевод организации", "operationAmount": {"amount": "4000", "currency": {"name": "GBP", "code": "GBP"}}},
        {"id": 957806819417790721, "state": "EXECUTED", "date": "2018-08-29T09:12:31.542756", "description": "Открытие вклада", "operationAmount": {"amount": "5000", "currency": {"name": "CHF", "code": "CHF"}}},
        {"id": 1234567890, "state": "EXECUTED", "date": "2023-10-26T12:00:00.000000", "description": "Покупка в магазине", "operationAmount": {"amount": "50.00", "currency": {"name": "EUR", "code": "EUR"}}},
    ]

    print("Последние операции (все валюты):")
    display_last_operations(test_data, num_operations=5)

    print("\nПоследние операции по USD:")
    display_last_operations(test_data, num_operations=5, currency_filter="USD")

    print("\nПоследние операции по EUR:")
    display_last_operations(test_data, num_operations=5, currency_filter="EUR")

    print("\nОписания всех операций:")
    descriptions = get_operation_descriptions(test_data)
    print(descriptions)