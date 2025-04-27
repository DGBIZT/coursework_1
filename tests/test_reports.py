import os
import pandas as pd
import pytest
from pandas._testing import assert_frame_equal
from src.reports import read_xlsx_file


# Создадим тестовый файл Excel для проверки
def create_test_excel(file_path):
    data = {
        'Column1': [1, 2, None],
        'Column2': ['a', None, 'c']
    }
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)


# Тестовый случай 1: успешный кейс с валидным файлом
def test_read_xlsx_valid_file():
    # Создаем временный файл
    file_path = 'test_file.xlsx'
    create_test_excel(file_path)

    # Читаем файл
    result = read_xlsx_file(file_path)

    # Проверяем результат
    expected_data = {
        'Column1': [1, 2, ''],
        'Column2': ['a', '', 'c']
    }
    expected_df = pd.DataFrame(expected_data)

    assert_frame_equal(result, expected_df)

    # Удаляем созданный файл
    os.remove(file_path)


# Тестовый случай 2: проверка обработки пустых значений
def test_read_xlsx_null_values():
    file_path = 'test_file_with_nulls.xlsx'
    create_test_excel(file_path)

    result = read_xlsx_file(file_path)

    # Проверяем, что все NaN заменены на пустые строки
    assert result.isnull().values.sum() == 0

    os.remove(file_path)


# Тестовый случай 3: проверка обработки несуществующего файла
def test_read_xlsx_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_xlsx_file('non_existent_file.xlsx')


# Тестовый случай 4: проверка обработки некорректного расширения
def test_read_xlsx_wrong_extension():
    with pytest.raises(ValueError):
        read_xlsx_file('wrong_extension.txt')


# Тестовый случай 5: проверка типа возвращаемого значения
def test_read_xlsx_return_type():
    file_path = 'test_file_type.xlsx'
    create_test_excel(file_path)

    result = read_xlsx_file(file_path)

    assert isinstance(result, pd.DataFrame)

    os.remove(file_path)