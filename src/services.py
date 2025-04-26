import pandas as pd
import os
import logging

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/services.log", mode="w", encoding="utf-8", delay=False)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s)")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def simple_search(file_path: str ): #, search: str
    """Функция создает поиск по категории или по описанию"""
    bas_dir = os.path.dirname(__file__)
    full_path = os.path.join(bas_dir, file_path)

    excel_data = pd.read_excel(full_path)

    print("Поиск осуществляется по категории или по описанию")
    search_enter = input("Введите запрос \n")

    if search_enter:
        # Осуществляем поиск по двум столбцам
        sim_sea = excel_data[(excel_data["Описание"] == search_enter) | (excel_data["Категория"] == search_enter)]
        # Затем проверяем свойство .empty у DataFrame - оно возвращает True, если DataFrame пустой
        if sim_sea.empty:
            logger.info(f"Данные отсутствуют по данному запросу ")
            return "По данному запросу отсутствуют транзакции"
        else:
            logger.info(f"преобразования данных в строку в формате JSON ")
            json_data = sim_sea.to_json(orient='records', force_ascii=False, indent=4)
            return json_data


file_path = simple_search("../data/operations.xlsx")
print(file_path)