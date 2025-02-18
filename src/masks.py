def mask_card(card_number: str) -> str:
    """
    Маскирует номер банковской карты, оставляя видимыми только первые 4 и последние 4 цифры.

    Args:
        card_number: Номер банковской карты в виде строки.

    Returns:
        Маскированный номер карты в виде строки.
        Пример: "1234 **** **** 5678"
    """
    if card_number == None or len(card_number) < 8:
        return card_number  # Or raise ValueError, depending on desired behavior
    return f"{card_number[:4]} **** **** {card_number[-4:]}"


def mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета, оставляя видимыми только последние 4 цифры.

    Args:
        account_number: Номер банковского счета в виде строки.

    Returns:
        Маскированный номер счета в виде строки.
        Пример: "****5678"
    """
    if account_number == None or len(account_number) < 4:
        return account_number # Or raise ValueError, depending on desired behavior
    return f"****{account_number[-4:]}"
