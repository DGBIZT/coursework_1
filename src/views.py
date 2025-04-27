import json
from utils import cards, currency_rate, hello_client, top_transactions, user_stocks, enter_input_main
import logging

logger = logging.getLogger("views")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/views.log", mode="w", encoding="utf-8", delay=False)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s)")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def page_main():
    """Функция главной страницы возвращает основную информацию"""

    tabl_new = enter_input_main()
    json_response = {
        "greeting": hello_client(),
        "cards": cards(tabl_new),  # main_cards(struct_file_json)
        "top_transactions": top_transactions(tabl_new),
        "currency_rates": currency_rate("../data/user_settings.json"),
        "stock_prices": user_stocks("../data/user_settings.json"),
    }
    logger.info(f"Осуществлет JSON-ответ с данными ")
    json_data = json.dumps(json_response, indent=4, ensure_ascii=False)
    return json_data


print(page_main())
