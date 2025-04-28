# import datetime
import json
import logging
import os

# from collections import defaultdict
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

LOG_PATH = os.path.join(os.path.dirname(__file__), "../logs/utils.log")
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOG_PATH, mode="a", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s)")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def hello_client(current_time=None):
    """Приветствие клиента с добрым утром и т.д. В зависимости от времени дня"""
    if current_time is None:
        current_time = datetime.now()
    hour = current_time.hour

    if 0 < hour <= 6:
        return "Доброй ночи"
    elif 6 < hour <= 12:
        return "Доброе утро"
    elif 12 < hour <= 18:
        return "Добрый день!"
    elif 18 < hour <= 24:
        return "Добрый вечер"


def read_transactions_excel_and_output_main(file_path: str, date: str) -> pd.DataFrame:
    """Функция для считывания финансовых операций из Excel"""

    bas_dir = os.path.dirname(__file__)
    full_path = os.path.join(bas_dir, file_path)

    excel_data = pd.read_excel(full_path)
    # Заменяем NaN(null) на пустые строки
    excel_data = excel_data.fillna(value="")
    # Преобразуем строки в datetime
    excel_data["Дата операции"] = pd.to_datetime(excel_data["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    # Преобразование из datetime во входной параметр
    date_obj = datetime.strptime(date, "%d.%m.%Y %H:%M:%S").date()

    # Получаем первый день месяца
    first_day = date_obj.replace(day=1)

    date_df = excel_data[
        (excel_data["Дата операции"].dt.date >= first_day) & (excel_data["Дата операции"].dt.date <= date_obj)
    ]

    return date_df


list_dicts = read_transactions_excel_and_output_main("../data/operations.xlsx", "31.12.2021 16:44:00")
# print(list_dicts)


def enter_input_main() -> pd.DataFrame:
    """Функция для ввода пользователем даты и время"""

    while True:
        try:
            date_enter = input("Введите дату в формате d.m.Y H:M:S \n")
            datetime.strptime(date_enter, "%d.%m.%Y %H:%M:%S")
            logger.info("Верный формат даты d.m.Y H:M:S")
            break
        except ValueError:
            logger.info("Неверный формат даты. Используйте d.m.Y H:M:S")
            print("Неверный формат даты. Используйте d.m.Y H:M:S")

    struct_file_json = read_transactions_excel_and_output_main("../data/operations.xlsx", date_enter)
    return struct_file_json


def cards(data_frame: pd.DataFrame) -> list:
    """Словарь, где ключ карта, а значение сумма транзакций по карте"""

    sum_dict = data_frame.groupby("Номер карты")["Сумма операции с округлением"].sum().to_dict()
    new_dict = {}
    for card, value in sum_dict.items():
        if card:
            new_dict[card[1:]] = value

    new_list_dict = list()
    for card, value in new_dict.items():
        new_list_dict.append({"last_digits": card, "total_spent": round(value, 2), "cashback": round(value / 100, 2)})

    return new_list_dict


# print(cards(list_dicts))


def top_transactions(last_dict: list[dict[str, str]]) -> list:
    """Функция возвращает топ 5 транзакций"""

    top_5 = last_dict.sort_values("Сумма операции с округлением", ascending=False).head(5)
    result_top = top_5.rename(
        columns={
            "Дата платежа": "date",
            "Сумма операции с округлением": "amount",
            "Категория": "category",
            "Описание": "description",
        }
    )[["date", "amount", "category", "description"]].to_dict("records")

    logger.info("Получение топ 5 транзакций")
    return result_top


# print(top_transactions(list_dicts))


def currency_rate(file_path: str) -> list:
    """Функция определяет курс в зависимости от валюты"""

    base_dir = os.path.dirname(__file__)
    full_path = os.path.join(base_dir, file_path)

    with open(full_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    currencies = data["user_currencies"]  # ['USD', 'EUR']

    amount = 1
    to_forex = "RUB"

    # Определяем курс в зависимости от валюты
    results = []
    for currency in currencies:
        load_dotenv()
        api_key = os.getenv("API_KEY")

        # Делаем запрос к API
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_forex}&from={currency}&amount={amount}"
        headers = {"apikey": api_key}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            json_data = response.json()
            results.append({"currency": currency, "rate": round(json_data["result"], 2)})

        except requests.exceptions.RequestException:
            logger.info(f"Ошибка при получении курса для {currency}")
            print(f"Ошибка при получении курса для {currency}")
            results.append({"currency": currency, "rate": 0.0})

    return results


# print(currency_rate("../data/user_settings.json"))


def user_stocks(file_path: str) -> list:
    """Функция возвращает стоимость акций в формате списка словарей"""
    base_dir = os.path.dirname(__file__)
    full_path = os.path.join(base_dir, file_path)
    with open(full_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Исправляем обработку данных
    st_prices = data.get("user_stocks", [])
    results = []

    for st_pr in st_prices:
        load_dotenv()
        api_key = os.getenv("Alpha_Vantage_API")
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={st_pr}&apikey={api_key}"
        headers = {"apikey": api_key}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            json_data = response.json()
            cost = json_data["Global Quote"]["05. price"]
            cost = float(cost)
            results.append({"stock": st_pr, "price": cost})
        except requests.exceptions.RequestException:
            print(f"Ошибка при получении стоимости {st_pr}")
            results.append({"stock": st_pr, "price": 0.0})
    return results


# def user_stocks(file_path: str) -> list:
#     """Функция возвращает стоимость акций в формате списка словарей"""
#     base_dir = os.path.dirname(__file__)
#     full_path = os.path.join(base_dir, file_path)
#
#     with open(full_path, "r", encoding="utf-8") as f:
#         data = json.load(f)
#
#     if "user_stocks" in data:
#         st_prices = data["user_stocks"]
#
#     results = []
#     for st_pr in st_prices:
#         load_dotenv()
#         api_key = os.getenv("Alpha_Vantage_API")
#
#         # Делаем запрос к API
#         url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={st_pr}&apikey={api_key}"
#         headers = {"apikey": api_key}
#
#         try:
#             response = requests.get(url, headers=headers)
#             response.raise_for_status()
#             json_data = response.json()
#             cost = json_data["Global Quote"]["05. price"]
#             cost = float(cost)
#
#             results.append({"stock": st_pr, "price": cost})
#
#         except requests.exceptions.RequestException:
#             print(f"Ошибка при получении стоимости {st_pr}")
#             results.append({"stock": st_pr, "price": 0.0})
#     return results


# print(user_stocks("../data/user_settings.json"))

# def cards(list_dict: list[dict[str, str]]) -> list:
#     """Создаю список с уникальными значениями карт"""
#     number_of_cards = set()
#     for operation in list_dict:
#         if operation.get("Номер карты") not in number_of_cards:
#             card_numer = operation.get("Номер карты")
#             number_of_cards.add(card_numer[1:])
#     number = list(number_of_cards)
#     # return number
#     # Создаю словарь из списка в формате {'last_digits': '7197'} ПОСЛЕДНИИ 4 ЦИФРЫ КАРТЫ
#     new = []
#     for i in number:
#         if i:  # пропускаем пустые строки
#             new.append({"last_digits": i})
#     return new
