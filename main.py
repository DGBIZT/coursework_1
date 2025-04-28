from src.reports import read_xlsx_file, spending_by_category
from src.services import simple_search
from src.views import page_main


def basic_logic():
    """Функция отвечающая за основную логику проекта и связывает функциональности между собой"""

    print("Данные для анализа и вывода на веб-страницах.")
    start_basic_logic = page_main()
    print(start_basic_logic)

    print("Так же вы можете осуществить поиск по всем транзакциям.")
    start_simple_search = simple_search("../data/operations.xlsx")
    print(start_simple_search)

    print("Получите отчет за последние три месяца по категориям")
    data_frame_new = read_xlsx_file("../data/operations.xlsx")
    you_сategory = input("Введити категорию по которой вы хотите получить отчет. \n")
    print("Если дата не будет введена, то берется текущая дата")
    you_date = input("Введите дату \n")
    you_report = spending_by_category(data_frame_new, you_сategory, you_date)
    print(you_report)


basic_logic()
