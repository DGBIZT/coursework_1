import datetime
import os
import pandas as pd

# a = "hello world"
# date_obj = datetime.datetime.now()
# print(a, date_obj.strftime("%H:%M.%S"))
#
# time_only = date_obj.time().replace(microsecond=0)
# print(time_only)

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
    list_of_dicts = excel_data.to_dict('records')
    # Переделываем <null> в None
    for item in list_of_dicts:
        if pd.isna(item.get('Кэшбэк')):
            item['Кэшбэк'] = None
        if pd.isna(item.get("Номер карты")):
            item["Номер карты"] = None
        if pd.isna(item.get("МСС")):
            item["MCC"] = None

    return list_of_dicts[0:7]

list_dicts = read_transactions_excel_and_output("../data/operations.xlsx")
print(list_dicts)

def start_date(list_with_dictionary: list[dict[str, str]]) -> str:
    pass
