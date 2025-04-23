import datetime
import os
import pandas as pd
import json

def hello_client():
    """ Приветствие клиента с добрым утром и т.д. В зависимости от времени дня """
    now = datetime.datetime.now()
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

def read_transactions_excel_and_output(file_path: str) -> list[dict[str, str]]:
    """Функция для считывания финансовых операций из Excel"""

    bas_dir = os.path.dirname(__file__)
    full_path = os.path.join(bas_dir, file_path)

    excel_data = pd.read_excel(full_path)
    # Заменяем NaN на пустые строки
    excel_data = excel_data.fillna(value='')
    list_of_dicts = excel_data.to_dict('records')

    return list_of_dicts

def cards(list_dict: list[dict[str, str]]) -> list:
    """Создаю список с уникальными значениями карт"""
    number_of_cards = set()
    for operation in list_dict:
        if operation.get("Номер карты") not in number_of_cards:
            card_numer = operation.get("Номер карты")
            number_of_cards.add(card_numer[1:])
    number = list(number_of_cards)
    # return number
    # Создаю словарь из списка в формате {'last_digits': '7197'} ПОСЛЕДНИИ 4 ЦИФРЫ КАРТЫ
    new = []
    for i in number:
        if i:  # пропускаем пустые строки
            new.append({"last_digits": i})
    return new

