import pytest
from src.widget import mask_account_card, get_date

class TestWidget:
    @pytest.mark.parametrize(
        "input_string, expected_mask",
        [
            ("Visa 1234567890123456", "Visa 1234 **** **** 3456"),  # Карта
            ("Visa Platinum 7000792289606361", "Visa Plat **** **** 6361"),  # Карта
            ("Счет 12345678901234567890", "Счет ****7890"),  # Счет
            ("MasterCard 1234567890", "MasterCard 1234567890"), # Неполная карта
            ("Счет 123", "Счет 123"), # Короткий счет
            ("Invalid Input", "Invalid Input"),  # Не карта и не счет
            ("", ""), # Пустая строка
            (None, None), # None
        ],
    )
    def test_mask_account_card(self, input_string, expected_mask):
        assert mask_account_card(input_string) == expected_mask

    @pytest.mark.parametrize(
        "date_string, expected_date",
        [
            ("2023-10-26T10:00:00.000Z", "26.10.2023"),
            ("2023-1-1", "01.01.2023"),  # Другой формат
            ("2023-10-26", "26.10.2023"),  # Без времени
            ("", None),  # Пустая строка
            (None, None),  # None
        ],
    )
    def test_get_data(self, date_string, expected_date):
        assert get_date(date_string) == expected_date
