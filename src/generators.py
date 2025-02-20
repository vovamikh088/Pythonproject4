from typing import Generator, List, Dict, Any

def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Generator[Dict[str, Any], None, None]:
    """
    Фильтрует список транзакций по коду валюты.

    Args:
        transactions: Список словарей, представляющих транзакции.
        currency_code: Код валюты для фильтрации (например, "USD").

    Yields:
        Транзакция, соответствующая заданному коду валюты.
    """
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """
    Возвращает описание каждой операции из списка транзакций.

    Args:
        transactions: Список словарей, представляющих транзакции.

    Yields:
        Описание операции.
    """
    for transaction in transactions:
        description = transaction.get("description")
        if description is None:
            yield ""
        elif isinstance(description, str):
            yield description
        else:
            yield str(description)


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX,
    ограничивая диапазон до максимально возможного номера карты (9999 9999 9999 9999).

    Args:
        start: Начальное значение диапазона номеров карт.
        end: Конечное значение диапазона номеров карт.

    Yields:
        Номер банковской карты в формате XXXX XXXX XXXX XXXX.
    """
    max_card_number: int = 9999999999999999
    start = max(0, start)
    end = min(end, max_card_number)

    for i in range(start, end + 1):
        card_number: str = str(i).zfill(16) # Дополняем 0 до 16 цифр
        formatted_card_number: str = " ".join([card_number[i:i+4] for i in range(0, 16, 4)])
        yield formatted_card_number