from typing import List, Dict, Any
from src.processing import (
    filter_by_state,
    sort_by_date,
    count_transactions_by_category,
)
from src.regex_utils import filter_transactions_by_description
from src.transaction_reader import csv_to_list, xlsx_to_list
from src.utils import load_transactions
from src.widget import mask_account_card, get_date
from src.external_api import calculate_transaction_amount


def print_transaction(transaction: Dict[str, Any]) -> None:
    """Форматирует и печатает информацию о транзакции."""
    date = get_date(transaction.get("date", ""))
    description = transaction.get("description", "No description")
    from_ = mask_account_card(transaction.get("from"))
    to = mask_account_card(transaction.get("to"))
    amount = calculate_transaction_amount(transaction) or 0

    print(f"{date} {description}")
    if from_:
        print(f"{from_} -> {to}")
    else:
        print(f"{to}")
    print(f"Сумма: {amount:.2f} руб.\n")


def get_user_choice(prompt: str, options: List[str]) -> str:
    """Получает и валидирует выбор пользователя."""
    while True:
        try:
            choice = input(prompt).strip().lower()
            if choice in options:
                return choice
        except:
            print(f"Некорректный ввод. Допустимые варианты: {', '.join(options)}")


def main_menu() -> None:
    """Основное меню программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = get_user_choice("Ваш выбор: ", ["1", "2", "3"])
    file_types = {"1": "JSON", "2": "CSV", "3": "XLSX"}
    print(f"\nДля обработки выбран {file_types[choice]}-файл.")

    filename = input("Введите путь к файлу: ").strip()

    if choice == "1":
        transactions = load_transactions(filename)
    elif choice == "2":
        transactions = csv_to_list(filename)
    else:
        transactions = xlsx_to_list(filename)

    if not transactions:
        print("Не удалось загрузить транзакции. Проверьте путь к файлу.")
        return

    process_transactions(transactions)


def process_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Обрабатывает и фильтрует транзакции по выбору пользователя."""
    valid_states = ["executed", "canceled", "pending"]
    state = get_user_choice(
        "Введите статус для фильтрации (executed/canceled/pending): ",
        valid_states
    ).upper()

    filtered = filter_by_state(transactions, state)
    print(f"\nНайдено {len(filtered)} операций со статусом {state}.")

    if not filtered:
        return

    if get_user_choice("Отсортировать по дате? (да/нет): ", ["да", "нет"]) == "да":
        order = get_user_choice(
            "По возрастанию или убыванию? (возрастанию/убыванию): ",
            ["возрастанию", "убыванию"]
        )
        filtered = sort_by_date(filtered, order == "убыванию")

    if get_user_choice("Только рублевые транзакции? (да/нет): ", ["да", "нет"]) == "да":
        filtered = [tx for tx in filtered
                    if tx.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"]

    if get_user_choice("Фильтровать по описанию? (да/нет): ", ["да", "нет"]) == "да":
        search_term = input("Введите текст для поиска: ")
        filtered = filter_transactions_by_description(filtered, search_term)

    print("\nРезультаты:")
    for tx in filtered[:10]:  # Ограничиваем вывод 10 транзакциями
        print_transaction(tx)

    if get_user_choice("Показать статистику по категориям? (да/нет): ", ["да", "нет"]) == "да":
        categories = input("Введите категории через запятую: ").split(",")
        stats = count_transactions_by_category(filtered, [c.strip() for c in categories])
        print("\nСтатистика:")
        for category, count in stats.items():
            print(f"{category}: {count}")


if __name__ == "__main__":
    main_menu()