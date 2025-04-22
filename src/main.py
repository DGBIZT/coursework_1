import datetime
import os
import pandas as pd


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

print(hello_client())

def read_transactions_excel_and_output(file_path: str) -> list[dict[str, str]]:
    """Функция для считывания финансовых операций из Excel"""

    bas_dir = os.path.dirname(__file__)
    full_path = os.path.join(bas_dir, file_path)

    excel_data = pd.read_excel(full_path)
    # Заменяем NaN на пустые строки
    excel_data = excel_data.fillna(value='')
    list_of_dicts = excel_data.to_dict('records')

    return list_of_dicts

list_dicts = read_transactions_excel_and_output("../data/operations.xlsx")
# print(list_dicts)


def start_date(list_with_dictionary: list[dict[str, str]]) -> str:
    pass



def cards(list_dict: list[dict[str, str]]) -> list:
    """Создаю список с уникальными значениями карт"""
    number_of_cards = set()
    for operation in list_dicts:
        if operation.get("Номер карты") not in number_of_cards:
            card_numer = operation.get("Номер карты")
            number_of_cards.add(card_numer[1:])
    number = list(number_of_cards)
    return number

numer = cards(list_dicts)


def last_digits(card_list: list) -> list[dict[str, str]]:
    """Создаю словарь из списка в формате {'last_digits': '7197'} ПОСЛЕДНИИ 4 ЦИФРЫ КАРТЫ"""
    new = []
    for i in numer:
        if i:  # пропускаем пустые строки
            new.append({"last_digits": i})
    return new

four_digits = last_digits(numer)

def total_spent(list_dict: list[dict[str, str]]) -> list[dict[str,float]]:
    list_top = []
    for operator in list_dicts:

        for num in numer:

            if num in operator.get("Номер карты"):
                sum_total = float(operator.get("Сумма платежа"))
                positive_number = abs(sum_total)
                list_top.append({num: positive_number})

    result_dict = {}
    for item in list_top:
        for name, score in item.items():
            if name in result_dict:
                result_dict[name] += score
            else:
                result_dict[name] = score
    # result = [{k: v} for k, v in result_dict.items()]
    result = []
    for k, v in result_dict.items():
        if k:
            result.append({k: v})
    return result


total_spent =total_spent(list_dicts)

def cashback(list_dict: list[dict[str,float]]) -> list[dict[str,float]]:
    new_cashback = {}
    for item in list_dict:
        for name, score in item.items():
            new_cashback[name] = score / 100

    return new_cashback


print(cashback(total_spent))
