import os
import pandas as pd
import pytest
from src.reports import read_xlsx_file, spending_by_category
from datetime import datetime
from typing import Optional

# Функция для создания временного тестового файла
def create_test_excel(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

    data = {
        'Name': ['John', 'Alice', None, 'Bob'],
        'Age': [25, 30, None, 45],
        'City': ['New York', None, 'Paris', 'Tokyo']
    }
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)

    assert os.path.getsize(file_path) > 0, "Файл пустой"


# Тестовый файл для проверки
TEST_FILE = 'test_data.xlsx'


def test_read_xlsx_file():
    # Создаем тестовый файл
    create_test_excel(TEST_FILE)

    # Получаем абсолютный путь к тестовому файлу
    from pathlib import Path  # Добавляем импорт здесь
    test_file_path = Path(TEST_FILE).absolute()

    # Проверяем права доступа
    assert os.access(test_file_path, os.R_OK), f"Нет прав на чтение файла {test_file_path}"

    # Добавляем проверку существования файла
    assert os.path.exists(test_file_path), f"Файл {test_file_path} не существует"

    # Проверяем, что функция возвращает DataFrame
    result = read_xlsx_file(test_file_path)
    assert isinstance(result, pd.DataFrame)

    # Проверяем размерность DataFrame
    assert result.shape == (4, 3)

    # Проверяем, что все NaN заменены на пустые строки
    assert result.isnull().sum().sum() == 0

    # Проверяем конкретные значения
    expected_data = {
        'Name': ['John', 'Alice', '', 'Bob'],
        'Age': ['25', '30', '', '45'],
        'City': ['New York', '', 'Paris', 'Tokyo']
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result, expected_df)

    # Проверяем обработку несуществующего файла
    with pytest.raises(FileNotFoundError):
        read_xlsx_file('non_existent_file.xlsx')


# Удаляем тестовый файл после теста
def teardown_module():
    from pathlib import Path  # Добавляем импорт здесь
    test_file_path = Path(TEST_FILE).absolute()
    if os.path.exists(test_file_path):
        os.remove(test_file_path)

#reports def spending_by_category

# Тест на корректную работу с существующими категориями

def test_existing_category(test_transactions):
    # Проверяем существующую категорию
    result = spending_by_category(test_transactions, 'Еда')

    # Создаем ожидаемый DataFrame с правильными датами
    expected = pd.DataFrame({
        'Дата платежа': ['2025-01-01', '2025-01-03'],  # Исправленные даты
        'Категория': ['Еда', 'Еда'],
        'Сумма': [1000, 1500]
    })

    # Проверяем, что результат - JSON строка
    assert isinstance(result, str)

    # Преобразуем JSON обратно в DataFrame
    # Указываем правильные имена столбцов
    result_df = pd.read_json(result, orient='records')
    result_df.columns = ['Дата платежа', 'Категория', 'Сумма']  # Восстанавливаем имена столбцов

    # Проверяем формат дат в полученном DataFrame
    result_df['Дата платежа'] = pd.to_datetime(result_df['Дата платежа'])
    expected['Дата платежа'] = pd.to_datetime(expected['Дата платежа'])

    # Проверяем равенство DataFrames
    pd.testing.assert_frame_equal(
        result_df.sort_values('Дата платежа').reset_index(drop=True),
        expected.sort_values('Дата платежа').reset_index(drop=True),
        check_dtype=True,
        check_like=True
    )

    # Дополнительно проверяем:
    assert result_df.shape == (2, 3)
    assert 'Дата платежа' in result_df.columns
    assert 'Категория' in result_df.columns
    assert 'Сумма' in result_df.columns
    assert result_df['Категория'].nunique() == 1  # Должна быть только категория 'Еда'
    assert result_df['Сумма'].sum() == 2500  # Сумма всех транзакций



# Тест на обработку отсутствующей категории
def test_non_existing_category(test_transactions):
    result = spending_by_category(test_transactions, 'Одежда')
    assert result == "По данному запросу отсутствуют транзакции"

# Тест с указанием даты
def test_with_date(test_transactions):
    result = spending_by_category(test_transactions, 'Транспорт', '01.02.2025')
    expected = pd.DataFrame({
        'Дата платежа': ['01.02.2025'],
        'Категория': ['Транспорт'],
        'Сумма': [2000]
    })
    assert isinstance(result, str)
    assert pd.DataFrame(pd.read_json(result)).equals(expected)

# Тест на некорректный формат даты
def test_invalid_date_format(test_transactions):
    with pytest.raises(ValueError):
        spending_by_category(test_transactions, 'Еда', '01-01-2025')

# Тест на пустые входные данные
def test_empty_dataframe():
    empty_df = pd.DataFrame(columns=['Дата платежа', 'Категория', 'Сумма'])
    result = spending_by_category(empty_df, 'Еда')
    assert result == "По данному запросу отсутствуют транзакции"

# Тест на граничные значения дат
def test_edge_dates(test_transactions):
    # Проверяем транзакции за последний месяц
    result = spending_by_category(test_transactions, 'Развлечения', '01.04.2025')
    expected = pd.DataFrame({
        'Дата платежа': ['01.04.2025'],
        'Категория': ['Развлечения'],
        'Сумма': [3000]
    })
    assert isinstance(result, str)
    assert pd.DataFrame(pd.read_json(result)).equals(expected)

# Тест на обработку некорректных данных в столбце даты
def test_invalid_date_data(test_transactions):
    test_transactions['Дата платежа'] = ['некорректная дата', '01.02.2025', '01.03.2025', '01.04.2025']
    with pytest.raises(ValueError):
        spending_by_category(test_transactions, 'Еда')

# Тест на проверку типа входных данных
def test_incorrect_input_type():
    with pytest.raises(TypeError):
        spending_by_category('не DataFrame', 'Еда')

# Тест на проверку обработки None в данных
def test_none_values(test_transactions):
    test_transactions['Категория'].iloc[0] = None
    result = spending_by_category(test_transactions, 'Еда')
    expected = pd.DataFrame({
        'Дата платежа': ['01.03.2025'],
        'Категория': ['Еда'],
        'Сумма': [1500]
    })
    assert isinstance(result, str)
    assert pd.DataFrame(pd.read_json(result)).equals(expected)