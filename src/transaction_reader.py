import csv
import pandas as pd


def csv_to_list(filepath, delimiter=","):
    """
    Считывает CSV файл и преобразует его в список строк, где каждая строка -
    это список значений.

    Аргументы:
      filepath: Путь к CSV файлу.
      delimiter: Разделитель значений в CSV файле (по умолчанию запятая).

    Возвращает:
      Список списков, представляющих данные из CSV файла.  Возвращает пустой список
      в случае ошибки.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=delimiter)
            data = list(csv_reader)
            return data
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filepath}' не найден.")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


def xlsx_to_list(filepath):
    """
    Считывает XLSX файл и преобразует его в список списков.

    Аргументы:
        filepath (str): Путь к XLSX файлу.

    Возвращает:
        list of lists: Список списков, представляющих данные из XLSX файла.
                       Возвращает пустой список в случае ошибки.
    """
    try:
        df = pd.read_excel(filepath)
        data = df.values.tolist()
        return data
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filepath}' не найден.")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []
