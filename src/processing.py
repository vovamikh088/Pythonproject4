from typing import List, Dict, Any


def filter_by_state(operations: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Фильтрует список операций по заданному статусу.

    Args:
        operations (List[Dict[str, Any]]): Список операций, каждая операция представлена словарем.
        state (str): Статус, по которому нужно отфильтровать операции. По умолчанию "EXECUTED".

    Returns:
        List[Dict[str, Any]]: Список операций с заданным статусом.
    """
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(operations: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список операций по дате.

    Args:
        operations (List[Dict[str, Any]]): Список операций, каждая операция представлена словарем.
        reverse (bool): True для сортировки в порядке убывания, False - в порядке возрастания.

    Returns:
        List[Dict[str, Any]]: Отсортированный список операций.
    """
    return sorted(operations, key=lambda x: x.get("date", ""), reverse=reverse)
