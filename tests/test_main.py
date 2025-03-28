import pytest
from unittest.mock import patch
from main import print_transaction, get_user_choice, process_transactions


def test_print_transaction(capsys):
    """Тест форматированного вывода одной транзакции"""
    # Подготовка тестовых данных - ОДНА транзакция (словарь)
    transaction = {
        "date": "2023-05-15T14:30:00",
        "description": "Payment for services",
        "from": "Visa 1234567812345678",
        "to": "Счет 1234567890123456",
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "USD"
            }
        }
    }

    # Мокируем зависимые функции
    with patch('main.get_date', return_value="15.05.2023"), \
            patch('main.mask_account_card', side_effect=["Visa 1234 56** **** 5678", "Счет **3456"]), \
            patch('main.calculate_transaction_amount', return_value=7500.00):
        print_transaction(transaction)
        captured = capsys.readouterr()

        # Проверяем вывод
        assert "15.05.2023 Payment for services" in captured.out
        assert "Visa 1234 56** **** 5678 -> Счет **3456" in captured.out
        assert "Сумма: 7500.00 руб." in captured.out

def test_get_user_choice_valid_input():
    """Тест получения корректного выбора пользователя"""
    with patch('builtins.input', side_effect=['1']):
        assert get_user_choice("Выбор: ", ["1", "2", "3"]) == "1"


def test_get_user_choice_retry_on_invalid(capsys):
    """Тест повторного запроса при неверном вводе"""
    with patch('builtins.input', side_effect=['4', '2']):
        result = get_user_choice("Выбор: ", ["1", "2", "3"])
        captured = capsys.readouterr()
        assert "" in captured.out
        assert result == "2"


@patch('main.filter_by_state')
@patch('main.sort_by_date')
@patch('main.filter_transactions_by_description')
@patch('main.count_transactions_by_category')
def test_process_transactions(mock_count, mock_filter_desc, mock_sort, mock_filter_state, capsys, main_transactions):
    """Тест обработки транзакций с различными фильтрами"""
    # Настраиваем моки
    mock_filter_state.return_value = main_transactions
    mock_sort.return_value = main_transactions[::-1]
    mock_filter_desc.return_value = [main_transactions[0]]
    mock_count.return_value = {"Payment": 1}

    # Эмулируем ввод пользователя
    input_values = [
        'executed',  # статус
        'да',  # сортировать
        'убыванию',  # порядок
        'нет',  # рублевые
        'да',  # фильтр по описанию
        'payment',  # текст поиска
        'нет'  # статистика
    ]

    with patch('builtins.input', side_effect=input_values):
        process_transactions(main_transactions)

    captured = capsys.readouterr()
    assert "Найдено 2 операций" in captured.out
    assert "Результаты:" in captured.out
    mock_filter_state.assert_called_once_with(main_transactions, "EXECUTED")
    mock_sort.assert_called_once()
    mock_filter_desc.assert_called_once()


@patch('main.load_transactions')
@patch('main.process_transactions')
def test_main_menu_json(mock_process, mock_load):
    """Тест главного меню для JSON"""
    mock_load.return_value = [{"test": "data"}]
    with patch('builtins.input', side_effect=['1', 'test.json']):
        with patch('main.print') as mock_print:
            from main import main_menu
            main_menu()
    mock_load.assert_called_once_with("test.json")
    mock_process.assert_called_once()


@patch('main.csv_to_list')
@patch('main.process_transactions')
def test_main_menu_csv(mock_process, mock_csv):
    """Тест главного меню для CSV"""
    mock_csv.return_value = [{"test": "data"}]
    with patch('builtins.input', side_effect=['2', 'test.csv']):
        with patch('main.print') as mock_print:
            from main import main_menu
            main_menu()
    mock_csv.assert_called_once_with("test.csv")
    mock_process.assert_called_once()

