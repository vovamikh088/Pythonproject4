import pytest
from src.masks import mask_card, mask_account

class TestMasks:
    @pytest.mark.parametrize(
        "card_number, expected_mask",
        [
            ("1234567890123456", "1234 **** **** 3456"),
            ("7675496749576475", "7675 **** **** 6475"),
            ("1234 5678 9012 3456", "1234 **** **** 3456"),  # С пробелами
            ("123456789012345", "1234 **** **** 2345"), # Неполная длина
            ("123", "123"),  # Менее 16 цифр
            ("", ""),  # Пустая строка
            (None, None),  # None
        ],
    )
    def test_get_mask_card_number(self, card_number, expected_mask):
        assert mask_card(card_number) == expected_mask

    @pytest.mark.parametrize(
        "account_number, expected_mask",
        [
            ("12345678901234567890", "****7890"),
            ("1234567890", "****7890"),  # Меньше 20 символов
            ("123", "123"), # Меньше 4 цифр
            ("", ""),  # Пустая строка
            (None, None),  # None
        ],
    )
    def test_get_mask_account(self, account_number, expected_mask):
        assert mask_account(account_number) == expected_mask

    def test_get_mask_card_number_type_error(self):
        with pytest.raises(TypeError):
            mask_card(1234567890123456) # Передача числа вместо строки

    def test_get_mask_account_type_error(self):
        with pytest.raises(TypeError):
            mask_account(12345678901234567890)  # Передача числа вместо строки
