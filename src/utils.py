import datetime
import os
import pandas as pd
from collections import defaultdict
from datetime import datetime
import json
import requests
from dotenv import load_dotenv

def hello_client():
    """ Приветствие клиента с добрым утром и т.д. В зависимости от времени дня """
    now = datetime.now()
    # Создал переменную hour, куда получил значение текущего времени в часах now.hour
    hour = now.hour

    if  0 < hour <= 6:
        return "Доброй ночи"
    elif 6 < hour <= 12:
        return "Доброе утро"
    elif 12 < hour <= 18:
        return "Добрый день!"
    elif 18 < hour <= 24:
        return "Добрый вечер"


def read_transactions_excel_and_output(file_path: str, date: str) -> pd.DataFrame:
    """Функция для считывания финансовых операций из Excel"""


    bas_dir = os.path.dirname(__file__)
    full_path = os.path.join(bas_dir, file_path)

    excel_data = pd.read_excel(full_path)
    # Заменяем NaN(null) на пустые строки
    excel_data = excel_data.fillna(value='')
    # Преобразуем строки в datetime
    excel_data['Дата операции'] = pd.to_datetime(excel_data['Дата операции'],
                                                 format='%d.%m.%Y %H:%M:%S')
    # Преобразование из datetime во входной параметр
    date_obj = datetime.strptime(date, '%d.%m.%Y %H:%M:%S').date()

    # Получаем первый день месяца
    first_day = date_obj.replace(day=1)

    date_df = excel_data[(excel_data['Дата операции'].dt.date >= first_day) &
                         (excel_data['Дата операции'].dt.date <= date_obj) ]


    return date_df
# list_dicts = read_transactions_excel_and_output("../data/operations.xlsx", "31.12.2021 16:44:00")
# print(list_dicts)

def cards(last_dict: list[dict[str, str]]) -> list:
    """Словарь, где ключ карта, а значение сумма транзакций по карте"""
    sum_dict = last_dict.groupby("Номер карты")["Сумма операции с округлением"].sum().to_dict()
    new_dict = {}
    for card, value in sum_dict.items():
        if card:
            new_dict[card[1:]] = value

    new_list_dict = list()
    for card, value in new_dict.items():
        new_list_dict.append({"last_digits": card, "total_spent": round(value, 2), "cashback": round(value / 100, 2)})

    return new_list_dict

def top_transactions(last_dict: list[dict[str, str]]) -> list:
    top_5 = last_dict.sort_values('Сумма операции с округлением', ascending=False).head(5)
    result_top = top_5.rename(columns={
            'Дата платежа': 'date',
            'Сумма операции с округлением': 'amount',
            'Категория': 'category',
            'Описание': 'description'
        })[['date', 'amount', 'category', 'description']].to_dict('records')

    return result_top

# print(top_transactions(list_dicts))


def currency_rate(file_path: str) -> list:
    """Функция определяет курс в зависимости от валюты"""

    base_dir = os.path.dirname(__file__)
    full_path = os.path.join(base_dir, file_path)

    with open(full_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    currencies = data['user_currencies']  # ['USD', 'EUR']

    amount = 1
    to_forex = "RUB"

    # Определяем курс в зависимости от валюты
    results = []
    for currency in currencies:
        load_dotenv()
        api_key = os.getenv("API_KEY")

        # Делаем запрос к API
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_forex}&from={currency}&amount={amount}"
        headers = {"apikey": api_key}  # API_KEY=NIhGoFiN8rFXWNgk9DnsJdN6GffOV2wq

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            json_data = response.json()
            results.append({
                'currency': currency,
                "rate": round(json_data['result'], 2)
            })

        except requests.exceptions.RequestException:
            print(f"Ошибка при получении курса для {currency}")
            results.append({
                'currency': currency,
                "rate": 0.0
            })

    return results
# print(currency_rate("../data/user_settings.json"))

def user_stocks(file_path: str) -> list:
    """Функция возвращает стоимость акций в формате списка словарей """
    base_dir = os.path.dirname(__file__)
    full_path = os.path.join(base_dir, file_path)

    with open(full_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if 'user_stocks' in data:
        st_prices = data['user_stocks']

    results = []
    for st_pr in st_prices:
        load_dotenv()
        api_key = os.getenv("Alpha_Vantage_API") #YN0YFHQ94W7TF9N8

        # Делаем запрос к API
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={st_pr}&apikey={api_key}'
        headers = {"apikey": api_key}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            json_data = response.json()
            # a = json_data["Global Quote"]["05. price"]
            return json_data
            # results.append({
            #     "stock": st_pr,
            #     "price": json_data["Global Quote"]["05. price"]
            # })

        except requests.exceptions.RequestException:
            print(f"Ошибка при получении стоимости {st_pr}")
            results.append({
                "stock": st_pr,
                "price": 0.0
            })
    return results
print(user_stocks("../data/user_settings.json"))
# def transaction_amount(transaction_dict: dict) -> float:
#     """Функция принимает на вход транзакцию и возвращает сумму транзакции в рублях"""
#
#     amount = transaction_dict["operationAmount"]["amount"]
#     currency = transaction_dict["operationAmount"]["currency"]["code"]
#     to_forex = "RUB"
#
#     if currency == "RUB":
#
#         return round(float(amount), 2)
#
#     else:
#         load_dotenv()
#         api_key = os.getenv("API_KEY")
#
#         url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_forex}&from={currency}&amount={amount}"
#         payload = {}
#         headers = {"apikey": api_key}
#         try:
#             response = requests.request("GET", url, headers=headers, data=payload)
#
#         except requests.exceptions.RequestException:
#             print("ошибка http запроса")
#             return 0
#         else:
#             result = response.text
#             json_data = json.loads(result)
#             return round(json_data["result"], 2)
#             # return json_data
#
#
# print(
#     transaction_amount(
#         {
#             "id": 41428829,
#             "state": "EXECUTED",
#             "date": "2019-07-03T18:35:29.512364",
#             "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
#             "description": "Перевод организации",
#             "from": "MasterCard 7158300734726758",
#             "to": "Счет 35383033474447895560",
#         }
#     )
# )
# print(
#     transaction_amount(
#         {
#             "id": 41428829,
#             "state": "EXECUTED",
#             "date": "2019-07-03T18:35:29.512364",
#             "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
#             "description": "Перевод организации",
#             "from": "MasterCard 7158300734726758",
#             "to": "Счет 35383033474447895560",
#         }
#     )
# )

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

