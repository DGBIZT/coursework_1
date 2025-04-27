# import os, logging
# import pandas as pd
# import pytest
# from unittest.mock import patch
# from io import StringIO
# from src.services import simple_search
#
#
# @pytest.fixture(autouse=True)
# def disable_logging():
#     logging.disable(logging.CRITICAL)
#     yield
#     logging.disable(logging.NOTSET)
#
#
#
# # Создаем тестовый Excel файл в памяти
# TEST_EXCEL_DATA = StringIO('''
# Описание,Категория,Значение
# Тест,Категория1,100
# Пример,Категория2,200
# Поиск,Категория1,300
# ''')
#
# # Создаем тестовый файл в директории тестов
# TEST_FILE_PATH = 'test_data.xlsx'
#
# def setup_module():
#     # Создаем тестовый Excel файл
#     df = pd.read_csv(TEST_EXCEL_DATA)
#     df.to_excel(TEST_FILE_PATH, index=False)
#
#
# def teardown_module():
#     # Удаляем тестовый файл после тестов
#     if os.path.exists(TEST_FILE_PATH):
#         os.remove(TEST_FILE_PATH)
#
#
# def test_simple_search_existing_data(mock_input):
#     # Тестируем поиск существующего значения
#     mock_input.return_value = 'Тест'
#     result = simple_search(TEST_FILE_PATH)
#     assert '"Описание":"Тест"' in result
#     assert '"Категория":"Категория1"' in result
#
#
# def test_simple_search_non_existing_data(mock_input):
#     # Тестируем поиск несуществующего значения
#     mock_input.return_value = 'Не существует'
#     result = simple_search(TEST_FILE_PATH)
#     assert result == "По данному запросу отсутствуют транзакции"
#
#
# def test_simple_search_empty_input(mock_input):
#     # Тестируем пустой ввод
#     mock_input.return_value = ''
#     result = simple_search(TEST_FILE_PATH)
#     assert result is None  # Функция должна вернуть None при пустом вводе
#
#
# def test_simple_search_wrong_file_path():
#     # Тестируем неверный путь к файлу
#     with pytest.raises(FileNotFoundError):
#         simple_search('неверный_путь.xlsx')
#
#
# def test_simple_search_missing_columns(mock_input):
#     # Тестируем отсутствие необходимых столбцов
#     mock_input.return_value = 'Тест'
#     wrong_columns_df = pd.DataFrame({'Неверное_описание': ['Тест'], 'Неверная_категория': ['Категория1']})
#     wrong_columns_df.to_excel('wrong_columns.xlsx', index=False)
#
#     with pytest.raises(KeyError):
#         simple_search('wrong_columns.xlsx')