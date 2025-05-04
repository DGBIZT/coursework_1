import json
import os
from datetime import datetime
from unittest.mock import mock_open, patch

import pandas as pd
import pytest
import requests

from src.utils import cards, currency_rate, enter_input_main, hello_client, top_transactions, user_stocks


# Создадим тестовые данные для проверки
def create_test_excel(filename):
    # Создаем тестовый DataFrame "%d.%m.%Y %H:%M:%S"
    test_data = {
        "date": ["31.12.2021 16:44:00", "31.12.2021 16:42:04", "31.12.2021 00:12:53"],
        "amount": [100.0, 200.0, 300.0],
        "description": ["Покупка", "Продажа", "Перевод"],
    }
    df = pd.DataFrame(test_data)

    # Сохраняем в Excel
    df.to_excel(filename, index=False)


# Тест на корректное получение данных
def test_enter_input_main_correct_data():
    # Задаем тестовую дату
    test_date = "31.12.2021 16:44:00"

    # Вызываем тестируемую функцию
    result_df = enter_input_main(test_date)

    # Проверяем, что результат - DataFrame
    assert isinstance(result_df, pd.DataFrame)

    # Проверяем количество столбцов
    assert len(result_df.columns) == 15

    # Проверяем наличие необходимых столбцов
    assert "Дата операции" in result_df.columns
    assert "Сумма операции с округлением" in result_df.columns

    # Проверяем, что данные соответствуют заданной дате
    assert result_df["Дата операции"][0] == pd.to_datetime(test_date)

    # Проверяем значение первой строки
    assert result_df["Сумма операции с округлением"][0] == 160.89


def test_night_greeting():
    """Тест для времени с 0:00 до 6:00"""
    # Создаем фиктивное время в 3:00
    mock_time = datetime(2025, 4, 27, 3, 0)
    assert hello_client(mock_time) == "Доброй ночи"


def test_morning_greeting():
    """Тест для времени с 6:00 до 12:00"""
    # Создаем фиктивное время в 9:00
    mock_time = datetime(2025, 4, 27, 9, 0)
    assert hello_client(mock_time) == "Доброе утро"


def test_day_greeting():
    """Тест для времени с 12:00 до 18:00"""
    # Создаем фиктивное время в 15:00
    mock_time = datetime(2025, 4, 27, 15, 0)
    assert hello_client(mock_time) == "Добрый день!"


def test_evening_greeting():
    """Тест для времени с 18:00 до 24:00"""
    # Создаем фиктивное время в 21:00
    mock_time = datetime(2025, 4, 27, 21, 0)
    assert hello_client(mock_time) == "Добрый вечер"


# Тест для функции cards()
def test_cards(test_data_frame):
    result = cards(test_data_frame)
    expected = [
        {"last_digits": "1111", "total_spent": 250.5, "cashback": 2.5},
        {"last_digits": "2222", "total_spent": 200.3, "cashback": 2.00},
    ]
    assert result == expected


# Тест на проверку обработки пустых данных для cards()
def test_cards_empty_data():
    empty_df = pd.DataFrame(columns=["Номер карты", "Сумма операции с округлением"])
    result = cards(empty_df)
    assert result == []


# Тест для функции top_transactions()
def test_top_transactions(test_transactions_df):
    result = top_transactions(test_transactions_df)
    expected = [
        {"date": "2025-04-25", "amount": 1500, "category": "Одежда", "description": "Магазин"},
        {"date": "2025-04-27", "amount": 1000, "category": "Еда", "description": "Ресторан"},
        {"date": "2025-04-23", "amount": 900, "category": "Еда", "description": "Кафе"},
        {"date": "2025-04-24", "amount": 800, "category": "Развлечения", "description": "Кино"},
        {"date": "2025-04-26", "amount": 500, "category": "Транспорт", "description": "Метро"},
    ]
    assert result == expected


# Тест на проверку обработки пустых данных для top_transactions()
def test_top_transactions_empty_data():
    empty_df = pd.DataFrame(columns=["Дата платежа", "Сумма операции с округлением", "Категория", "Описание"])
    result = top_transactions(empty_df)
    assert result == []


# Тест на проверку currency_rate
# Создаем тестовые данные для файла
TEST_CONFIG = {"user_currencies": ["USD", "EUR"]}

# Тестовый API ответ
TEST_API_RESPONSE_USD = {"result": 90.1234}
TEST_API_RESPONSE_EUR = {"result": 100.5678}


# Базовый тест на корректную работу
def test_currency_rate_success(monkeypatch):
    # Мокаем открытие файла
    monkeypatch.setattr("builtins.open", mock_open(read_data=json.dumps(TEST_CONFIG)))

    # Мокаем получение API ключа
    monkeypatch.setattr("os.getenv", lambda x: "TEST_API_KEY")

    # Мокаем запросы к API
    def mocked_get(url, headers):
        response = requests.Response()
        response.status_code = 200  # Устанавливаем статус код ДО возврата

        if "USD" in url:
            response.json = lambda: TEST_API_RESPONSE_USD
        elif "EUR" in url:
            response.json = lambda: TEST_API_RESPONSE_EUR

        return response

    monkeypatch.setattr(requests, "get", mocked_get)

    # Вызываем тестируемую функцию
    result = currency_rate("test_file.json")

    # Проверяем результат
    assert len(result) == 2
    assert result[0] == {"currency": "USD", "rate": 90.12}
    assert result[1] == {"currency": "EUR", "rate": 100.57}


# Тест на отсутствие файла
def test_currency_rate_file_not_found():
    with pytest.raises(FileNotFoundError):
        currency_rate("non_existent_file.json")


# Тест на некорректный формат файла
def test_currency_rate_invalid_json(monkeypatch):
    monkeypatch.setattr("builtins.open", mock_open(read_data="{invalid json"))
    with pytest.raises(json.JSONDecodeError):
        currency_rate("test_file.json")


# Тест на отсутствие валюты в конфиге
def test_currency_rate_no_currencies(monkeypatch):
    config_without_currencies = {"user_currencies": []}
    monkeypatch.setattr("builtins.open", mock_open(read_data=json.dumps(config_without_currencies)))
    result = currency_rate("test_file.json")
    assert result == []


# Тест на ошибку API
def test_currency_rate_api_error(monkeypatch):
    monkeypatch.setattr("builtins.open", mock_open(read_data=json.dumps(TEST_CONFIG)))
    monkeypatch.setattr("os.getenv", lambda x: "TEST_API_KEY")

    def mocked_get_with_error(url, headers):
        response = requests.Response()
        response.status_code = 500
        return response

    monkeypatch.setattr(requests, "get", mocked_get_with_error)

    result = currency_rate("test_file.json")
    assert len(result) == 2
    assert result[0] == {"currency": "USD", "rate": 0.0}
    assert result[1] == {"currency": "EUR", "rate": 0.0}


# Тест на отсутствие API ключа
def test_currency_rate_no_api_key(monkeypatch):
    monkeypatch.setattr("builtins.open", mock_open(read_data=json.dumps(TEST_CONFIG)))
    monkeypatch.setattr("os.getenv", lambda x: None)

    result = currency_rate("test_file.json")
    assert result == [{"currency": "USD", "rate": 0.0}, {"currency": "EUR", "rate": 0.0}]


# Тест на проверку user_stocks
TEST_JSON = [{"stock": "AAPL"}, {"stock": "GOOGL"}]

# Создаем тестовый файл
TEST_FILE_PATH = os.path.join(os.path.dirname(__file__), "test_stocks.json")


# Функция для создания тестового JSON файла
def create_test_file(data):
    with open(TEST_FILE_PATH, "w", encoding="Utf-8") as f:
        json.dump({"user_stocks": data["user_stocks"]}, f)


# Функция для удаления тестового файла
def delete_test_file():
    if os.path.exists(TEST_FILE_PATH):  # Проверяем путь, а не данные
        os.remove(TEST_FILE_PATH)


# Тестовый класс
class TestUserStocks:
    def setup_method(self):
        self.test_data = {"user_stocks": ["AAPL", "GOOGL"]}
        create_test_file(self.test_data)  # или просто create_test_file()

    def teardown_method(self):
        delete_test_file()

    @pytest.fixture(autouse=True)
    def mock_env(self):
        with patch.dict("os.environ", {"Alpha_Vantage_API": "test_api_key"}):
            yield

    @pytest.fixture
    def mock_requests(self):
        with patch("requests.get") as mock_get:
            mock_response = {"Global Quote": {"05. price": "150.25"}}
            mock_get.return_value.json.return_value = mock_response
            mock_get.return_value.status_code = 200
            yield mock_get

    def test_user_stocks_success(self, mock_requests):
        print("Мок вызван с аргументами:", mock_requests.call_args_list)
        print("Файл существует:", os.path.exists(TEST_FILE_PATH))
        print("Полный путь:", os.path.abspath(TEST_FILE_PATH))

        # Добавляем проверку существования файла
        assert os.path.exists(TEST_FILE_PATH)

        result = user_stocks(TEST_FILE_PATH)
        assert len(result) == 2
        assert result[0] == {"stock": "AAPL", "price": 150.25}
        assert result[1] == {"stock": "GOOGL", "price": 150.25}
        assert mock_requests.call_count == 2

    def test_user_stocks_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            user_stocks("non_existent_file.json")

    def test_user_stocks_api_error(self, mock_requests):

        mock_requests.side_effect = requests.exceptions.RequestException

        result = user_stocks(TEST_FILE_PATH)

        assert len(result) == 2
        assert result[0] == {"stock": "AAPL", "price": 0.0}
        assert result[1] == {"stock": "GOOGL", "price": 0.0}
