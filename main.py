import json
from datetime import datetime

import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.progress import Progress
from rich.style import Style

from src.reports import spending_by_category
from src.services import investment_bank, description_filter
from src.views import main_sheet
from src.utils import XLSX_file_read, file_df

# Инициализация rich console
console = Console()

# Настройка цветовых стилей
STYLE_SUCCESS = Style(color="green", bold=True)
STYLE_ERROR = Style(color="red", bold=True)
STYLE_HEADER = Style(color="blue", bold=True)
STYLE_WARNING = Style(color="yellow", bold=True)


def show_main_menu():
    """Отображает главное меню"""
    console.print(Panel.fit("Выберите действие:", title="Главное меню", border_style="blue"))

    console.print("1. [cyan]Главная страница[/cyan]")
    console.print("2. [green]Инвесткопилка[/green]")
    console.print("3. [yellow]Поиск транзакций[/yellow]")
    console.print("4. [magenta]Отчет по категориям[/magenta]")
    console.print("0. [red]Выход[/red]")
    console.print()


def get_main_page():
    """Запрашивает данные для главной страницы"""
    console.print(Panel.fit("Введите дату и время для анализа", title="Главная страница", border_style="cyan"))

    date_input = Prompt.ask("Дата и время (YYYY-MM-DD HH:MM:SS)", default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    with Progress(transient=True) as progress:
        task = progress.add_task("Формирование отчета...", total=1)
        result = main_sheet(date_input)
        progress.update(task, completed=1)

    display_main_page(result)


def get_invest_page():
    """Запрашивает данные для инвесткопилки"""
    console.print(Panel.fit("Введите параметры для расчета", title="Инвесткопилка", border_style="green"))

    month_input = Prompt.ask("Месяц (YYYY-MM)", default=datetime.now().strftime("%Y-%m"))

    limit_input = IntPrompt.ask("Лимит округления", default=50)

    with Progress(transient=True) as progress:
        task = progress.add_task("Чтение данных...", total=1)
        transactions = XLSX_file_read()

        if isinstance(transactions, list):
            progress.update(task, description="Расчет...")
            result = investment_bank(month_input, transactions, limit_input)
            progress.update(task, completed=1)

            display_invest_result(result)
        else:
            console.print(f"[red]Ошибка:[/red] {transactions}")


def get_search_page():
    """Запрашивает данные для поиска"""
    console.print(Panel.fit("Введите параметры поиска", title="Поиск транзакций", border_style="yellow"))

    keyword = Prompt.ask("Ключевое слово для поиска")

    with Progress(transient=True) as progress:
        task = progress.add_task("Поиск...", total=1)
        transactions = XLSX_file_read()

        if isinstance(transactions, list):
            result = description_filter(transactions, keyword)
            progress.update(task, completed=1)

            display_search_results(result)
        else:
            console.print(f"[red]Ошибка:[/red] {transactions}")


def get_report_page():
    """Запрашивает данные для отчета"""
    console.print(Panel.fit("Введите параметры отчета", title="Отчет по категориям", border_style="magenta"))

    category = Prompt.ask("Категория для анализа")
    date_input = Prompt.ask("Дата отсчета (YYYY-MM-DD)", default=datetime.now().strftime("%Y-%m-%d"))

    with Progress(transient=True) as progress:
        task = progress.add_task("Формирование отчета...", total=1)
        df = file_df()

        if isinstance(df, pd.DataFrame):
            result = spending_by_category(df, category, date_input)
            progress.update(task, completed=1)

            display_report(result)
        else:
            console.print(f"[red]Ошибка:[/red] {df}")


def display_main_page(result):
    """Отображает результаты главной страницы"""
    data = json.loads(result)

    # Приветствие
    console.print(Panel.fit(data["greeting"], title="Приветствие", style=STYLE_HEADER))

    # Карты
    cards_table = Table(title="Ваши карты", show_header=True, header_style="bold magenta")
    cards_table.add_column("Карта", style="cyan")
    cards_table.add_column("Расходы", justify="right")
    cards_table.add_column("Кешбэк", justify="right")

    for card in data["cards"]:
        total_spent = f"{card['total_spent']:,.2f} ₽"
        cashback = f"{card['cashback']:,.2f} ₽"
        cards_table.add_row(f"•••• {card['last_digits']}", total_spent, cashback)

    console.print(cards_table)

    # Топ транзакции
    transactions_table = Table(title="Крупнейшие расходы", show_header=True, header_style="bold magenta")
    transactions_table.add_column("Дата")
    transactions_table.add_column("Сумма", justify="right")
    transactions_table.add_column("Категория")
    transactions_table.add_column("Описание")

    for tr in data["top_transactions"]:
        amount = f"{tr['amount']:,.2f} ₽"
        transactions_table.add_row(tr["date"], amount, tr["category"], tr["description"])

    console.print(transactions_table)

    # Курсы валют
    if data["currency_rates"]:
        currency_table = Table(title="Курсы валют", show_header=True, header_style="bold magenta")
        currency_table.add_column("Валюта")
        currency_table.add_column("Курс", justify="right")

        for currency in data["currency_rates"]:
            rate = f"{currency['rate']:,.2f} ₽"
            currency_table.add_row(currency["currency"], rate)

        console.print(currency_table)

    # Акции
    if data["stock_prices"]:
        stocks_table = Table(title="Ваши акции", show_header=True, header_style="bold magenta")
        stocks_table.add_column("Акция")
        stocks_table.add_column("Цена", justify="right")

        for stock in data["stock_prices"]:
            price = f"{stock['price']:,.2f} $"
            stocks_table.add_row(stock["stock"], price)

        console.print(stocks_table)


def display_invest_result(result):
    """Отображает результат инвесткопилки"""
    console.print(
        Panel.fit(
            f"Вы могли накопить: [bold green]{result:,.2f} ₽[/]",
            title="Результат Инвесткопилки",
            border_style="green",
            padding=(1, 4),
        )
    )


def display_search_results(result):
    """Отображает результаты поиска"""
    data = json.loads(result)

    if not data:
        console.print("[yellow]Ничего не найдено[/yellow]")
        return

    table = Table(title="Найденные транзакции", show_header=True, header_style="bold magenta")
    table.add_column("Дата")
    table.add_column("Сумма", justify="right")
    table.add_column("Категория")
    table.add_column("Описание")

    for item in data[:10]:  # Показываем первые 10 результатов
        amount = f"{item['Сумма операции']:,.2f} ₽" if "Сумма операции" in item else "N/A"
        date = item.get("Дата операции", "N/A")
        category = item.get("Категория", "N/A")
        description = (
            item.get("Описание", "N/A")[:50] + "..."
            if isinstance(item.get("Описание"), str) and len(item.get("Описание")) > 50
            else item.get("Описание", "N/A")
        )

        table.add_row(date, amount, category, description)

    console.print(table)

    if len(data) > 10:
        console.print(f"[dim]Показано 10 из {len(data)} результатов[/dim]")


def display_report(result):
    """Отображает отчет"""
    console.print(
        Panel.fit(result.to_string(index=False), title="Отчет по категории", border_style="blue", padding=(1, 2))
    )


def main():
    """Главная функция приложения"""

    while True:
        show_main_menu()
        choice = Prompt.ask("Выберите пункт меню", choices=["0", "1", "2", "3", "4"])

        try:
            if choice == "1":
                get_main_page()
            elif choice == "2":
                get_invest_page()
            elif choice == "3":
                get_search_page()
            elif choice == "4":
                get_report_page()
            elif choice == "0":
                if Confirm.ask("Вы уверены, что хотите выйти?"):
                    console.print("[green]До свидания![/green]")
                    break
        except Exception as e:
            console.print(f"[red]Ошибка: {str(e)}[/red]")

        if not Confirm.ask("Продолжить работу?", default=True):
            console.print("[green]До свидания![/green]")
            break


if __name__ == "__main__":
    main()
