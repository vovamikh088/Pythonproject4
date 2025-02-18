# generators.py
def filter_by_currency(transactions, currency_code):
    """
    Фильтрует список транзакций по коду валюты.

    Args:
        transactions (list): Список словарей, представляющих транзакции.
        currency_code (str): Код валюты для фильтрации (например, "USD").

    Yields:
        dict: Транзакция, соответствующая заданному коду валюты.
    """
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions):
    """
    Возвращает описание каждой операции из списка транзакций.

    Args:
        transactions (list): Список словарей, представляющих транзакции.

    Yields:
        str: Описание операции.
    """
    for transaction in transactions:
        yield transaction.get("description")


def card_number_generator(start, end):
    """
    Генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX.
    ограничивая диапазон до максимально возможного номера карты (9999 9999 9999 9999).

    Args:
        start (int): Начальное значение диапазона номеров карт.
        end (int): Конечное значение диапазона номеров карт.

    Yields:
        str: Номер банковской карты в формате XXXX XXXX XXXX XXXX.
    """
    max_card_number = 9999999999999999
    start = max(0, start)
    end = min(end, max_card_number)

    for i in range(start, end + 1):
        card_number = str(i).zfill(16)  # Дополняем 0 до 16
        formatted_card_number = " ".join([card_number[i:i+4] for i in range(0, 16, 4)])
        yield formatted_card_number