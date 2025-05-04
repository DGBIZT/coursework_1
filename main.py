from datetime import datetime

from src.reports import read_xlsx_file, spending_by_category
from src.services import simple_search
from src.utils import enter_input_main
from src.views import page_main


def basic_logic_2():
    while True:
        try:
            date_enter = input("Введите дату в формате YYYY-MM-DD HH:MM:SS \n")
            # Преобразуем введенную дату в объект datetime
            date_obj = datetime.strptime(date_enter, "%Y-%m-%d %H:%M:%S")
            # Форматируем дату в нужный формат и сохраняем в date_enter
            date_enter = date_obj.strftime("%d.%m.%Y %H:%M:%S")
            # print(f"Дата преобразована: {date_enter}")
            break
        except ValueError:
            print("Неверный формат даты. Используйте YYYY-MM-DD HH:MM:SS")

    start_basic_logic = page_main(date_enter)
    print(start_basic_logic)

    print("Поиск осуществляется по категории или по описанию.")
    search_enter = input("Введите запрос. \n")
    period_date = enter_input_main(date_enter)
    transactions = period_date.to_dict("records")
    transactions_json = simple_search(transactions, search_enter)
    print(transactions_json)

    print("Получите отчет за последние три месяца по категориям")
    data_frame_new = read_xlsx_file("../data/operations.xlsx")
    you_сategory = input("Введити категорию по которой вы хотите получить отчет. \n")
    print("Если дата не будет введена, то берется текущая дата")
    you_date = input("Введите дату формата %dd.%mm.%YYYY\n")
    you_report = spending_by_category(data_frame_new, you_сategory, you_date)
    print(you_report)


basic_logic_2()
