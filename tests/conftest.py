import pytest
import logging
from unittest.mock import patch, mock_open
import os, json
import tempfile
import pandas as pd


# Создаем заглушку для input, так как в тестах нельзя использовать реальный ввод
@pytest.fixture
def mock_input():
    with patch('builtins.input', autospec=True) as mocked_input:
        yield mocked_input

# Создаем заглушку для чтения файла Excel
@pytest.fixture
def mock_read_excel():
    with patch('pandas.read_excel') as mocked_read_excel:
        yield mocked_read_excel

# Создаем заглушку для логгера
@pytest.fixture(autouse=True)
def mock_logging(monkeypatch):
    # Замокаем FileHandler чтобы не создавать реальные файлы
    monkeypatch.setattr('logging.FileHandler', mock_open())

# Фикстура для def cards(data_frame: pd.DataFrame) -> list:
# Тестовые данные для функции cards()
@pytest.fixture
def test_data_frame():
    return pd.DataFrame({
        'Номер карты': ['*1111', '*2222', '*1111'],
        'Сумма операции с округлением': [100.5, 200.3, 150.0]
    })

# Тестовые данные для функции top_transactions()
@pytest.fixture
def test_transactions_df():
    return pd.DataFrame({
        'Дата платежа': ['2025-04-27', '2025-04-26', '2025-04-25', '2025-04-24', '2025-04-23', '2025-04-22'],
        'Сумма операции с округлением': [1000, 500, 1500, 800, 900, 400],
        'Категория': ['Еда', 'Транспорт', 'Одежда', 'Развлечения', 'Еда', 'Транспорт'],
        'Описание': ['Ресторан', 'Метро', 'Магазин', 'Кино', 'Кафе', 'Автобус']
    })

@pytest.fixture
def test_stocks_file(tmp_path):
    file_path = tmp_path / "test_stocks.json"
    data = [
        {"stock": "AAPL", "price": 150.25},
        {"stock": "GOOGL", "price": 150.25}
    ]
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return file_path



# Для services def simple_search(file_path: str ):
@pytest.fixture
def mock_input():
    # Создаем фиктивный ввод для функции input()
    with patch('builtins.input') as mocked_input:
        yield mocked_input

@pytest.fixture(autouse=True)
def ensure_log_dir():
    log_dir = os.path.join(os.path.dirname(__file__), '../logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

# Reports def spending_by_category
@pytest.fixture
def test_transactions():
    data = {
        'Дата платежа': ['01.01.2025', '01.02.2025', '01.03.2025', '01.04.2025'],
        'Категория': ['Еда', 'Транспорт', 'Еда', 'Развлечения'],
        'Сумма': [1000, 2000, 1500, 3000]
    }
    return pd.DataFrame(data)

# services.py функция simple_search
# Подготовка тестовых данных
