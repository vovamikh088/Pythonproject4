import pytest
from typing import List, Dict, Any, Generator
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Provides sample transactions for testing."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01", "description": "USD Transaction 1", "operationAmount": {"amount": 100, "currency": {"code": "USD"}}},
        {"id": 2, "state": "EXECUTED", "date": "2024-01-02", "description": "USD Transaction 2", "operationAmount": {"amount": 200, "currency": {"code": "USD"}}},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-03", "description": "EUR Transaction 1", "operationAmount": {"amount": 300, "currency": {"code": "EUR"}}},
        {"id": 4, "state": "EXECUTED", "date": "2024-01-04", "description": "Other Transaction", "operationAmount": {"amount": 400, "currency": {"code": "RUB"}}},
    ]


@pytest.mark.parametrize(
    "currency_code, expected_count, expected_descriptions",
    [
        ("USD", 2, ["USD Transaction 1", "USD Transaction 2"]),
        ("EUR", 1, ["EUR Transaction 1"]),
        ("GBP", 0, []),
    ],
)
def test_filter_by_currency(sample_transactions: List[Dict[str, Any]], currency_code: str, expected_count: int, expected_descriptions: List[str]):
    transactions: List[Dict[str, Any]] = list(filter_by_currency(sample_transactions, currency_code))
    assert len(transactions) == expected_count
    descriptions: List[str] = [t["description"] for t in transactions]
    assert descriptions == expected_descriptions


def test_filter_by_currency_empty_list():
    filtered_transactions: List[Dict[str, Any]] = list(filter_by_currency([], "USD"))
    assert len(filtered_transactions) == 0


def test_filter_by_currency_missing_currency_code():
    transactions: List[Dict[str, Any]] = [
        {"id": 1, "operationAmount": {}},
        {"id": 2, "description": "Test"},
        {"id": 3},
    ]
    filtered_transactions: List[Dict[str, Any]] = list(filter_by_currency(transactions, "USD"))
    assert len(filtered_transactions) == 0


@pytest.mark.parametrize(
    "transactions, expected_descriptions",
    [
        ([{"description": "Desc1"}, {"description": "Desc2"}], ["Desc1", "Desc2"]),
        ([], []),
        ([{"id": 1}, {"description": None}, {"description": ""}], ["", "", ""]), # Corrected expected output
    ],
)
def test_transaction_descriptions(transactions: List[Dict[str, Any]], expected_descriptions: List[str]):
    descriptions: List[str] = list(transaction_descriptions(transactions))
    assert descriptions == expected_descriptions


@pytest.mark.parametrize(
    "start, end, expected_count, expected_first, expected_last",
    [
        (1, 5, 5, "0000 0000 0000 0001", "0000 0000 0000 0005"),
        (10, 12, 3, "0000 0000 0000 0010", "0000 0000 0000 0012"),
        (1, 1, 1, "0000 0000 0000 0001", "0000 0000 0000 0001"),
        (0, 2, 3, "0000 0000 0000 0000", "0000 0000 0000 0002"), # Added test case for 0 start
    ],
)
def test_card_number_generator(start: int, end: int, expected_count: int, expected_first: str, expected_last: str):
    card_numbers: List[str] = list(card_number_generator(start, end))
    assert len(card_numbers) == expected_count
    if expected_count > 0:
        assert card_numbers[0] == expected_first
        assert card_numbers[-1] == expected_last

def test_card_number_generator_zero_start():
    card_numbers: List[str] = list(card_number_generator(0, 2))
    assert card_numbers == ["0000 0000 0000 0000", "0000 0000 0000 0001", "0000 0000 0000 0002"]