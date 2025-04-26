import pandas as pd
import json
from utils import cards, currency_rate, hello_client, top_transactions, user_stocks, enter_input_main



def page_main():
    """Функция главной страницы возвращает основную информацию"""
    # period_date = get_period_date(date)
    # date_enter = input("Введите дату в формате d.m.Y H:M:S \n"  )
    # struct_file_json = read_transactions_excel_and_output(
    #     "../data/operations.xlsx", date_enter
    # )  # read_finance_exel_operastion
    tabl_new = enter_input_main()
    json_response = {
        "greeting": hello_client(),
        "cards": cards(tabl_new),  # main_cards(struct_file_json)
        "top_transactions": top_transactions(tabl_new),
        # "currency_rates": currency_rate("../data/user_settings.json"),
        # "stock_prices": user_stocks("../data/user_settings.json"),
    }
    json_data = json.dumps(json_response, indent=4, ensure_ascii=False)
    return json_data


print(page_main())
