import re
from typing import List, Dict, Any


def filter_transactions_by_description(transactions: List[Dict[str, Any]], search_pattern: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по совпадению с регулярным выражением в описании.

    Args:
        transactions: Список словарей с транзакциями.
        search_pattern: Строка с регулярным выражением для поиска.

    Returns:
        Список транзакций, где описание содержит совпадение с шаблоном.

    Example:
        transactions = [{"description": "Payment for services"},
                         {"description": "Grocery shopping"}]
        filter_transactions_by_description(transactions, "payment")
        [{'description': 'Payment for services'}]
    """
    if not transactions or not search_pattern:
        return []

    try:
        pattern = re.compile(search_pattern, re.IGNORECASE)
    except re.error:
        return []

    return [tx for tx in transactions if tx.get("description") and pattern.search(tx["description"])]