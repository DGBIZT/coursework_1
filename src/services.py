import json
import logging

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/services.log", mode="w", encoding="utf-8", delay=False)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s)")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def simple_search(transactions: list, search_query: str) -> str:
    """
    Функция осуществляет простой поиск по списку транзакций.
    Поиск производится по полям 'Описание' и 'Категория'.

    Параметры:
    transactions (list): список словарей с транзакциями
    search_query (str): строка для поиска

    """

    # Создаем пустой список для хранения результатов поиска
    search_results = []

    # Проходим по всем транзакциям
    for transaction in transactions:
        # Проверяем, есть ли поисковый запрос в описании или категории
        if search_query in transaction["Описание"] or search_query in transaction["Категория"]:
            search_results.append(transaction)

    # Если результаты найдены
    if search_results:
        # Преобразуем результаты в JSON
        # Добавляем параметр default для обработки Timestamp
        json_data = json.dumps(search_results, ensure_ascii=False, indent=4, default=str)
        return json_data
    else:
        return "По данному запросу отсутствуют транзакции"
