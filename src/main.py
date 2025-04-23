import datetime
import os
import pandas as pd
from collections import defaultdict
from datetime import datetime

#
# def hello_client():
#     """ Приветствие клиента с добрым утром и т.д. В зависимости от времени дня """
#     now = datetime.datetime.now()
#     # Создал переменную hour, куда получил значение текущего времени в часах now.hour
#     hour = now.hour
#
#     if  0 < hour <= 6:
#         return "Доброй ночи"
#     elif 6 < hour <= 12:
#         return "Доброе утро"
#     elif 12 < hour <= 18:
#         return "Добрый день!"
#     elif 18 < hour <= 24:
#         return "Добрый вечер"
#
# print(hello_client())
#
def read_transactions_excel_and_output(file_path: str, date: str) -> list[dict[str, str]]:
    """Функция для считывания финансовых операций из Excel"""


    bas_dir = os.path.dirname(__file__)
    full_path = os.path.join(bas_dir, file_path)

    excel_data = pd.read_excel(full_path)
    # Заменяем NaN на пустые строки
    excel_data = excel_data.fillna(value='')
    # Преобразуем строки в datetime
    excel_data['Дата операции'] = pd.to_datetime(excel_data['Дата операции'],
                                                 format='%d.%m.%Y %H:%M:%S')

    date_obj = datetime.strptime(date, '%d.%m.%Y').date()
    date_df = excel_data[excel_data['Дата операции'].dt.date == date_obj]
    # petr_df = excel_data[excel_data['Дата операции'] == date]

    # Преобразование таблицы в список словарей
    # list_of_dicts = petr_df.to_dict('records')

    # Уникальные значения
    # unique_cards = excel_data["Номер карты"].unique()

    # Сумма значений каждого столбика
    # sum_cards = excel_data.apply(pd.Series.mean)

    # Преобразование в словарь
    # result_dict = date_df.set_index("Номер карты")["Сумма операции с округлением"].to_dict()

    #
    # result_dict = defaultdict(list)
    # for key, value in zip(date_df["Номер карты"], date_df["Сумма операции с округлением"]):
    #     result_dict[key].append(value)
    return date_df

list_dicts = read_transactions_excel_and_output("../data/operations.xlsx", "31.12.2021")
# print(list_dicts)

def cards(last_dict: list[dict[str, str]]) -> dict:
    """Словарь, где ключ карта, а значение сумма транзакций по карте"""
    sum_dict = last_dict.groupby("Номер карты")["Сумма операции с округлением"].sum().to_dict()
    new_dict = {}
    for card, value in sum_dict.items():
        if card:
            new_dict[card[1:]] = value

    return new_dict
cards_list = cards(list_dicts)
print(cards_list)

# df = pd.DataFrame({
#     'A': ["Петр", "Николай", "Иван", "Петр", "Николай", "Иван","Петр", "Николай", "Иван"],
#     'B': [25, 30, 15, 26, 31, 16, 27, 32, 17],
#     'C': ["Москва", "Питер", "Краснодар","Москва", "Питер", "Краснодар","Москва", "Питер", "Краснодар"]
# })
# print(df)
# result_dict = df.set_index("A")["B"].to_dict()
#
# result_dict = defaultdict(list)
# for key, value in zip(df['A'], df['B']):
#     result_dict[key].append(value)
#
# print(result_dict)

