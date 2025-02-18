from datetime import datetime

from .masks import mask_account, mask_card


def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в строке.
    Args:
        account_info: Строка, содержащая тип и номер карты или счета.
            Примеры: "Visa Platinum 7000792289606361", "Maestro 7000792289606361", "Счет 73654108430135874305"

    Returns:
        Строка с замаскированным номером.
    """
    if account_info == None:
        return account_info
    parts = account_info.split()
    if not parts:
        return account_info  # Если строка пустая, возвращаем ее без изменений.

    if parts[0].lower() in ("visa", "maestro"):
        return f"{parts[0]} {mask_card(''.join(parts[1:]))}"
    elif parts[0].lower() == "счет":
        return f"{parts[0]} {mask_account(''.join(parts[1:]))}"
    else:
        return account_info  # Если тип не распознан, возвращаем исходную строку

def get_date(date_str: str | None) -> str | None:
    """
    Преобразует строку с датой в формате "ГГГГ-ММ-ДДTчч:мм:сс.миллисекунды" в формат "ДД.ММ.ГГГГ".

    Args:
        date_str: Строка с датой в формате "ГГГГ-ММ-ДДTчч:мм:сс.миллисекунды".
            Пример: "2024-03-11T02:26:18.671407"

    Returns:
        Строка с датой в формате "ДД.ММ.ГГГГ" или None, если date_str равен None или пустой строке.
        Пример: "11.03.2024"
    """
    if not date_str:
        return None

    try:
        # Попытка обработать разные форматы дат
        date_object = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError:
        date_object = datetime.strptime(date_str, "%Y-%m-%d")

    return date_object.strftime("%d.%m.%Y")
