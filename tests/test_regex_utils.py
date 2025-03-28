import pytest
from src.regex_utils import filter_transactions_by_description


def test_filter_by_description(simple_transactions):
    result = filter_transactions_by_description(simple_transactions, "payment")
    assert len(result) == 1
    assert result[0]["description"] == "Payment for services"


def test_filter_by_description_no_match(simple_transactions):
    result = filter_transactions_by_description(simple_transactions, "taxi")
    assert len(result) == 0


def test_filter_by_description_empty_input():
    assert filter_transactions_by_description([], "test") == []
    assert filter_transactions_by_description(None, "test") == []


@pytest.mark.parametrize("pattern,expected_count", [
    ("payment", 1),
    ("shopping", 1),
    ("nonexistent", 0),
    ("(", 0),  # невалидное regex
    ("[a-z", 0),  # невалидное regex
    ("", 0),  # пустой паттерн
])
def test_with_parameters(simple_transactions, pattern, expected_count):
    result = filter_transactions_by_description(simple_transactions, pattern)
    assert len(result) == expected_count