import datetime
import os
import pandas as pd
from collections import defaultdict
from datetime import datetime
from utils import read_transactions_excel_and_output

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


list_dicts = read_transactions_excel_and_output("../data/operations.xlsx", "31.12.2021 16:44:00")
# print(list_dicts)
#
def cards(last_dict: list[dict[str, str]]) -> dict:
    """Словарь, где ключ карта, а значение сумма транзакций по карте"""
    sum_dict = last_dict.groupby("Номер карты")["Сумма операции с округлением"].sum().to_dict()
    new_dict = {}
    for card, value in sum_dict.items():
        if card:
            new_dict[card[1:]] = value

    new_list_dict = list()
    for card, value in new_dict.items():
        new_list_dict.append({"last_digits": card, "total_spent": value, "cashback": value / 100})

    return sum_dict
cards_list = cards(list_dicts)
# print(cards_list)

def top_transactions(last_dict: list[dict[str, str]]) -> list:
    top_2 = last_dict.sort_values('Сумма операции с округлением', ascending=False).head(2)
    result = {
        "top_operation": top_2.rename(columns={
            'Дата платежа': 'date',
            'Сумма операции с округлением': 'amount',
            'Категория': 'category',
            'Описание': 'description'
        })[['date', 'amount', 'category', 'description']].to_dict('records')
    }
    # result_dict = {"date": last_dict['Сумма операции с округлением'].max()['Дата платежа'].tolist(),}
      # {'Петр': [25, 26, 27]}
    return result

print(top_transactions(list_dicts))

# person = {'name': 'John', 'age': 25, 'gender': 'male'}
# new_list = []
# for key, value in person.items():
#     new_list.append({"ключ": key,"meaning": value , "back": value})
# print(new_list)

# df = pd.DataFrame({
#     'A': ["Петр", "Николай", "Иван", "Петр", "Николай", "Иван","Петр", "Николай", "Иван"],
#     'B': [25, 30, 15, 26, 31, 16, 27, 32, 17],
#     'C': ["Москва", "Питер", "Краснодар","Москва", "Питер", "Краснодар","Москва", "Питер", "Краснодар"]
# })
# # print(df)
# result_dict = {"date": df[df['A'] == 'Петр']['B'].max().tolist()}
# print(result_dict)  # {'Петр': [25, 26, 27]}
# petr_row = df[df['A'] == "Петр"].loc[0]
# niko_row = df[df['A'] == "Николай"].loc[2]
# result_dict = {petr_row["Петр"]: int(petr_row['B']) & niko_row["Николай"]: int(niko_row['B'])}
# print(result_dict)
# result_dict = df.set_index("A")["B"].to_dict()
#
# result_dict = defaultdict(list)
# for key, value in zip(df['A'], df['B']):
#     result_dict[key].append(value)
#
# print(result_dict)

