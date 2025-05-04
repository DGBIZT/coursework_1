import json
import logging

from src.utils import cards, currency_rate, enter_input_main, hello_client, top_transactions, user_stocks

logger = logging.getLogger("views")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/views.log", mode="w", encoding="utf-8", delay=False)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s)")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def page_main(date: str) -> dict:
    """Функция главной страницы возвращает основную информацию"""

    # tabl_new = enter_input_main()
    period_date = enter_input_main(date)
    json_response = {
        "greeting": hello_client(),
        "cards": cards(period_date),  # main_cards(struct_file_json)
        "top_transactions": top_transactions(period_date),
        "currency_rates": currency_rate("../data/user_settings.json"),
        "stock_prices": user_stocks("../data/user_settings.json"),
    }
    logger.info("Осуществлет JSON-ответ с данными ")
    json_data = json.dumps(json_response, indent=4, ensure_ascii=False)
    return json_data


# print(page_main(date_enter))
