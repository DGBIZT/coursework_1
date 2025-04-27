import pandas as pd
import json
import datetime
from datetime import datetime
from typing import Optional
import os
from functools import wraps
import logging

logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/reports.log", mode="w", encoding="utf-8", delay=False)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s)")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def report_to_file(func):
    @wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        now = datetime.now().strftime("%d-%m-%Y_%H-%M")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        reports_dir = os.path.join(base_dir, '../reports')
        os.makedirs(reports_dir, exist_ok=True)
        file_path = os.path.join(reports_dir, f"{now}_report.json")
        logger.info(f"Записываем данные в директорию {reports_dir}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(result)
        return result
    return inner


def read_xlsx_file(file_path: str) -> pd.DataFrame:
    bas_dir = os.path.dirname(__file__)
    if bas_dir:
        full_path = os.path.join(bas_dir, file_path)
    else:
        full_path = os.path.abspath(file_path)
    # full_path = os.path.join(bas_dir, file_path)
    # full_path = os.path.abspath(file_path)

    try:
        # Читаем файл и сразу преобразуем числа в строки
        excel_data = pd.read_excel(full_path, engine='openpyxl', converters={
            'Age': str  # явно указываем преобразование в строку
        })

        # Заменяем NaN на пустые строки
        excel_data = excel_data.fillna(value="")

        # Дополнительно преобразуем все числовые столбцы в строки
        for col in excel_data.columns:
            if excel_data[col].dtype == 'float64':
                excel_data[col] = excel_data[col].astype(str)

        return excel_data
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {full_path}")
    except PermissionError:
        raise PermissionError(f"Нет прав доступа к файлу: {full_path}")
    except Exception as e:
        raise ValueError(f"Ошибка чтения файла: {str(e)}")

@report_to_file
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
        end_date = now
        # Начальная дата, отнимаем от конечной даты 3 месяца
        start_date = end_date - pd.DateOffset(months=3)

    filtered_data = transactions[
        (transactions['Дата платежа'] >= start_date) & (transactions['Дата платежа'] <= end_date)]

    # Осуществляем поиск по category
    sim_sea = filtered_data[(filtered_data["Категория"] == category)]

    # Форматируем дату перед конвертацией в JSON
    # sim_sea.loc[:, 'Дата платежа'] = sim_sea['Дата платежа'].dt.strftime('%d.%m.%Y')
    sim_sea['Дата платежа'] = sim_sea['Дата платежа'].dt.strftime('%d.%m.%Y')

    # Затем проверяем свойство .empty у DataFrame - оно возвращает True, если DataFrame пустой
    if sim_sea.empty:
        return "По данному запросу отсутствуют транзакции"
    else:
        json_data = sim_sea.to_json(orient='records', force_ascii=False, indent=4)
        return json_data


# data_frame_new = read_xlsx_file("../data/operations.xlsx")
#
# report_category = spending_by_category(data_frame_new, "ЖКХ", "31.12.2021")
# print(report_category)