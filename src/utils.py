import datetime
import os
import pandas as pd
from collections import defaultdict
from datetime import datetime

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

