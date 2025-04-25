import os
import pandas as pd
import datetime
import json
import os
# from collections import defaultdict
from datetime import datetime


import requests
from dotenv import load_dotenv

def simple_search(file_path: str, ): #, search: str

    bas_dir = os.path.dirname(__file__)
    full_path = os.path.join(bas_dir, file_path)

    excel_data = pd.read_excel(full_path)

    print("Осуществляется по категории или по описанию")
    search_enter = ("Введите запрос \n")

    if search_enter:
        # sum_dict = excel_data.groupby("Дата платежа")["Статус"].sum().to_dict()
        sim_sea = excel_data[excel_data['Категория'] == search_enter]





        return sim_sea


list_dicts = simple_search("../data/operations.xlsx") #", Супермаркеты"
print(list_dicts)