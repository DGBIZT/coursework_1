# import datetime
# import os
# import pandas as pd
# from collections import defaultdict
# from datetime import datetime
from utils import hello_client, cards, read_transactions_excel_and_output,top_transactions, currency_rate, user_stocks
import json

def page_main():
    """Функция главной страницы возвращает основную информацию"""
    # period_date = get_period_date(date)
    struct_file_json = read_transactions_excel_and_output("../data/operations.xlsx", "31.12.2021 16:44:00") #read_finance_exel_operastion
    json_response = {
        "greeting": hello_client(),
        "cards": cards(struct_file_json), #main_cards(struct_file_json)
        "top_transactions": top_transactions(struct_file_json),
        "currency_rates": currency_rate("../data/user_settings.json"),
        "stock_prices": user_stocks("../data/user_settings.json"),
    }
    json_data = json.dumps(json_response, indent=4, ensure_ascii=False)
    return json_data
print(page_main())



