import logging
import os
from unittest.mock import patch

import pandas as pd
import pytest

from src.services import simple_search

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/services.log", mode="w", encoding="utf-8", delay=False)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Подготовка тестовых данных
TEST_DATA = {
    "Категория": ["Продукты", "Одежда", "Продукты"],
    "Описание": ["Молоко", "Футболка", "Хлеб"],
    "Сумма": [100, 200, 150],
}


@pytest.fixture
def temp_excel_file(tmpdir):
    excel_path = os.path.join(tmpdir, "test_data.xlsx")
    df = pd.DataFrame(TEST_DATA)
    df.to_excel(excel_path, index=False)
    return excel_path


# Тестовый кейс 1: успешный поиск по категории
def test_search_by_category(temp_excel_file):
    with patch("builtins.input", return_value="Продукты"):
        result = simple_search(temp_excel_file)
        expected = (
            pd.DataFrame(TEST_DATA)
            .query("Категория == 'Продукты'")
            .to_json(orient="records", force_ascii=False, indent=4)
        )
        assert result == expected


# Тестовый кейс 2: успешный поиск по описанию
def test_search_by_description(temp_excel_file):
    with patch("builtins.input", return_value="Молоко"):
        result = simple_search(temp_excel_file)
        expected = (
            pd.DataFrame(TEST_DATA)
            .query("Описание == 'Молоко'")
            .to_json(orient="records", force_ascii=False, indent=4)
        )
        assert result == expected


# Тестовый кейс 3: отсутствие данных
def test_no_data_found(temp_excel_file):
    with patch("builtins.input", return_value="Неверный запрос"):
        result = simple_search(temp_excel_file)
        assert result == "По данному запросу отсутствуют транзакции"


# Тестовый кейс 4: проверка вывода логов
def test_logging(temp_excel_file, caplog):
    with patch("builtins.input", return_value="Продукты"):
        simple_search(temp_excel_file)
        assert "преобразования данных в строку в формате JSON" in caplog.text


# Тестовый кейс 5: проверка обработки пустого ввода
def test_empty_input(temp_excel_file):
    with patch("builtins.input", return_value=""):
        result = simple_search(temp_excel_file)
        assert result is None  # Функция должна вернуть None при пустом вводе


# Тестовый кейс 6: проверка обработки несуществующего файла
def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        simple_search("несуществующий_файл.xlsx")
