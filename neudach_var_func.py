#def cards(list_dict: list[dict[str, str]]) -> list:
#     """Создаю список с уникальными значениями карт"""
#     number_of_cards = set()
#     for operation in list_dicts:
#         if operation.get("Номер карты") not in number_of_cards:
#             card_numer = operation.get("Номер карты")
#             number_of_cards.add(card_numer[1:])
#     number = list(number_of_cards)
#     return number
#
# numer = cards(list_dicts)
# # print(numer)
#
#
# def last_digits(card_list: list) -> list[dict[str, str]]:
#     """Создаю словарь из списка в формате {'last_digits': '7197'} ПОСЛЕДНИИ 4 ЦИФРЫ КАРТЫ"""
#     new = []
#     for i in numer:
#         if i:  # пропускаем пустые строки
#             new.append({"last_digits": i})
#     return new
#
# four_digits = last_digits(numer)
#
# def total_spent(list_dict: list[dict[str, str]]) -> list[dict[str,float]]:
#     list_top = []
#     for operator in list_dicts:
#
#         for num in numer:
#
#             if num in operator.get("Номер карты"):
#                 sum_total = float(operator.get("Сумма платежа"))
#                 positive_number = abs(sum_total)
#                 list_top.append({num: positive_number})
#
#     result_dict = {}
#     for item in list_top:
#         for name, score in item.items():
#             if name in result_dict:
#                 result_dict[name] += score
#             else:
#                 result_dict[name] = score
#     # result = [{k: v} for k, v in result_dict.items()]
#     result = []
#     for k, v in result_dict.items():
#         if k:
#             result.append({k: v})
#     return result
#
#
# total_spent =total_spent(list_dicts)
#
# def cashback(list_dict: list[dict[str,float]]) -> list[dict[str,float]]:
#     new_cashback = {}
#     for item in list_dict:
#         for name, score in item.items():
#             new_cashback[name] = score / 100
#
#     return new_cashback


# print(cashback(total_spent))


#########################################
# a = "hello world"
# date_obj = datetime.datetime.now()
# print(a, date_obj.strftime("%H:%M.%S"))
#
# time_only = date_obj.time().replace(microsecond=0)
# print(time_only)

# def read_transactions_excel_and_output(file_path: str) -> list[dict[str, str]]:
#     """Функция для считывания финансовых операций из Excel"""
#
#     bas_dir = os.path.dirname(__file__)
#     full_path = os.path.join(bas_dir, file_path)
#
#     excel_data = pd.read_excel(full_path)
#     list_of_dicts = excel_data.to_dict('records')
#     # Переделываем <null> в None
#     for item in list_of_dicts:
#         if pd.isna(item.get('Кэшбэк')):
#             item['Кэшбэк'] = None
#         if pd.isna(item.get("Номер карты")):
#             item["Номер карты"] = None
#         if pd.isna(item.get("МСС")):
#             item["MCC"] = None
#
#     return list_of_dicts
#
# list_dicts = read_transactions_excel_and_output("../data/operations.xlsx")
# print(list_dicts)

# def start_date():
#     new_dict = {}
#     salute = hello_client()
#     new_dict["greeting"] = str(salute)
#     json_data = json.dumps(new_dict, ensure_ascii=False)
#
#     return json_data
# print(start_date())

# new_dict_rate = list()
    # for key, value in data.items():
    #     if key == 'user_currencies':
    #         for val in value:
    #             new_dict_rate.append({"currency": val})
################## pandas ##################################
# date_df = excel_data[excel_data['Дата операции'] == date]

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