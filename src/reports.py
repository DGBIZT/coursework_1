import pandas as pd
import json
import datetime
from datetime import datetime
from typing import Optional
import os



def read_xlsx_file(file_path: str) -> pd.DataFrame:
    bas_dir = os.path.dirname(__file__)
    full_path = os.path.join(bas_dir, file_path)

    excel_data = pd.read_excel(full_path)
    # Заменяем NaN(null) на пустые строки
    excel_data = excel_data.fillna(value="")

    return excel_data

def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:

    """Функция создает отчет траты по категориям"""
    # Преобразуем строки в datetime
    transactions['Дата платежа'] = pd.to_datetime(transactions['Дата платежа'], format='%d.%m.%Y')
    if date is not None:
        # Конечная дата
        end_date = pd.to_datetime(date, format='%d.%m.%Y')
        # Начальная дата, отнимаем от конечной даты 3 месяца
        start_date = end_date - pd.DateOffset(months=3)
    else:
        now = datetime.now()
        # Создал переменную hour, куда получил значение текущего времени в часах now.hour
        hour = now
        end_date = pd.to_datetime(hour, format='%d.%m.%Y')
        # Начальная дата, отнимаем от конечной даты 3 месяца
        start_date = end_date - pd.DateOffset(months=3)

    filtered_data = transactions[(transactions['Дата платежа'] >= start_date) & (transactions['Дата платежа'] <= end_date)]

    # Осуществляем поиск по category
    sim_sea = filtered_data[(filtered_data["Категория"] == category)]
    # Затем проверяем свойство .empty у DataFrame - оно возвращает True, если DataFrame пустой
    if sim_sea.empty:
        return "По данному запросу отсутствуют транзакции"
    else:
        json_data = sim_sea.to_json(orient='records', force_ascii=False, indent=4)
        return json_data


data_frame_new = read_xlsx_file("../data/operations.xlsx")

report_category = spending_by_category(data_frame_new, "ЖКХ", "16.12.2021")
print(report_category)