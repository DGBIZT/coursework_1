import datetime
import os
import pandas as pd
<<<<<<< HEAD
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
=======
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

# print(hello_client())

def read_transactions_excel_and_output(file_path: str) -> list[dict[str, str]]:
>>>>>>> 6e92d4403e4047d4f4fffed8974b8824f5335486
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

<<<<<<< HEAD
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
=======
def date(list_with_dictionary: list[dict[str, str]]) -> str:
    pass



def cards(list_dict: list[dict[str, str]]) -> list:
    """Создаю список с уникальными значениями карт"""
    number_of_cards = set()
    for operation in list_dicts:
        if operation.get("Номер карты") not in number_of_cards:
            card_numer = operation.get("Номер карты")
            number_of_cards.add(card_numer[1:])
    number = list(number_of_cards)
    # return number
    """Создаю словарь из списка в формате {'last_digits': '7197'} ПОСЛЕДНИИ 4 ЦИФРЫ КАРТЫ"""
    new = []
    for i in number:
        if i:  # пропускаем пустые строки
            new.append({"last_digits": i})
    return new
print(cards(list_dicts ))
# numer = cards(list_dicts)


# def last_digits(card_list: list) -> list[dict[str, str]]:
#     """Создаю словарь из списка в формате {'last_digits': '7197'} ПОСЛЕДНИИ 4 ЦИФРЫ КАРТЫ"""
#     new = []
#     for i in numer:
#         if i:  # пропускаем пустые строки
#             new.append({"last_digits": i})
#     return new

# four_digits = last_digits(numer)
# print(four_digits)

def total_spent(list_dict: list[dict[str, str]]) -> list[dict[str,float]]:
    """Функция рассчитывает общую сумму расходов"""
    list_top = []
    for operator in list_dicts:

        for num in numer:

            if num in operator.get("Номер карты"):
                sum_total = float(operator.get("Сумма платежа"))
                positive_number = abs(sum_total)
                pos_number_round = round(positive_number, 2)
                list_top.append({num: pos_number_round})

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
# print(f"\n Сумма, {total_spent} \n")

def cashback(list_dict: list[dict[str,float]]) -> list[dict[str,float]]:
    """Возвращает кешбэк 1 рубль на каждые 100 рублей"""
    result = []
    for item in list_dict:
        for score in item.values():
            result.append({"cashback": round(score / 100, 2)})
    return result

# print(cashback(total_spent))

def page_main():
    """Функция главной страницы возвращает основную информацию"""
    # period_date = get_period_date(date)
    # struct_file_json = read_transactions_excel_and_output(period_date) #read_finance_exel_operastion
    json_response = {
        "greeting": hello_client(),
        "cards": last_digits(numer), #main_cards(struct_file_json)
        # "top_transactions": top_transactions(struct_file_json)
        # "currency_rates": curency_raters(),
        # "stock_prices": user_stocks(),
    }
    return json_response
print(page_main())
# def start_date():
#     new_dict = {}
#     salute = hello_client()
#     new_dict["greeting"] = str(salute)
#     json_data = json.dumps(new_dict, ensure_ascii=False)
#
#     return json_data
# print(start_date())

# СЕРВИСЫ
# def main() -> None:
#     """запрос дат и вывод информации за указанный период"""
#     list_dicts = read_transactions_excel_and_output("../data/operations.xlsx")
#     to_date = input("Введите дату")
#     from_date = datetime.datetime.strptime(to_date, "%d.%m.%Y")
#     date_replace = from_date.replace(day=1)
#     list_dicts["Дата операции"] = pd.to_datetime(list_dicts["Дата операции"], format="%d.%m.%Y %H:%M:%S")
#     df_for_date = list_dicts[(list_dicts["Дата операции"] <= to_date) & (list_dicts["Дата операции"]>= from_date)]
#     print(df_for_date)
#
# main()

>>>>>>> 6e92d4403e4047d4f4fffed8974b8824f5335486
