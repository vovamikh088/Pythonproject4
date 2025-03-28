import os

import requests
from dotenv import load_dotenv

load_dotenv()


def calculate_transaction_amount(transaction):
    """
    Вычисляет сумму транзакции в рублях.
    Args:
        transaction (dict): Словарь, представляющий транзакцию.
                         Обязательные ключи: 'amount' (float), 'currency','code' (str).
    Returns:
        float: Сумма транзакции в рублях.
               Возвращает None в случае ошибки.
    """
    try:
        amount = transaction['operationAmount']["amount"]
        currency = transaction['operationAmount']["currency"]["code"]

        if not isinstance(amount, str) or not isinstance(currency, str):
            print("Ошибка: Некорректные данные транзакции")
            return None

        try:
            amount = float(amount)
        except ValueError:
            print("Ошибка: Некорректный формат суммы транзакции")
            return None

        if currency == "RUB":
            return amount

        api_key = os.getenv("API_KEY")
        if currency not in ("USD", "EUR"):
            print(f"Ошибка: Неподдерживаемая валюта: {currency}")
            return None

        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
        # print(url)
        response = requests.get(url, headers={"apikey": api_key})
        response.raise_for_status()
        data = response.json()
        return float(data["result"])

    except (KeyError, TypeError) as e:
        print(f"Ошибка: Некорректная структура данных транзакции: {e}")
        return None
