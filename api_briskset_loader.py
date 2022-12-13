# Problems API can get 100 request per getSets
# We have to merge two files_with_data

# Packages
import json
import numpy as np
import pandas as pd
import requests

# Variables
apiKey = 'your_apiKey'
username = 'your_username'
password = 'your_password'

# Getting user hash
url_for_hash = 'https://brickset.com/api/v3.asmx/login'
query_string = {'apiKey': apiKey, 'username': username, 'password': password}
userHash = requests.request("GET", url_for_hash, params=query_string).json()['hash']

# Getting themes (number of sets)
themes_all = []
query_string = {'apiKey': apiKey}
url_for_themes = 'https://brickset.com/api/v3.asmx/getThemes'
themes = requests.request("GET", url_for_themes, params=query_string).json()

for theme in themes['themes']:
    themes_all.append(theme['theme'])

first_part = themes_all[:100]  # sets from 0 to 99 themes
second_part = themes_all[100:]  # sets from 100 to 152 themes

# Getting sets with data
df = pd.DataFrame()  # Dataframe with data
list_of_keys = ['setID', 'number', 'numberVariant', 'name', 'year', 'theme', 'themeGroup', 'subtheme', 'category',
                'released', 'pieces', 'minifigs', 'collections', 'LEGOCom', 'rating', 'reviewCount', 'packagingType',
                'availability', 'instructionsCount', 'ageRange', 'extendedData', 'lastUpdated']

url_for_sets = 'https://brickset.com/api/v3.asmx/getSets'

for theme in second_part:  # here change for part of sets
    setTheme = {'extendedData': 1, 'theme': theme}
    setTheme = json.dumps(setTheme)
    query_string = {'apiKey': apiKey, 'userHash': userHash, 'params': setTheme}
    set_series = requests.request("GET", url_for_sets, params=query_string).json()
    for single_set in range(len(set_series['sets'])):
        tmp_dict_data = {}
        for element in list_of_keys:
            try:
                if isinstance(set_series['sets'][single_set][element], dict):
                    for el in set_series['sets'][single_set][element].items():
                        if isinstance(el[1], dict):
                            values = ['retailPrice', 'dateFirstAvailable', 'dateLastAvailable']
                            for value in values:
                                if el[1].get(value) is None:
                                    col_name = el[0] + '_' + value
                                    tmp_dict_data[col_name] = np.NaN
                                else:
                                    col_name = el[0] + '_' + value
                                    tmp_dict_data[col_name] = el[1].get(value)
                        else:
                            if el[0] == 'description' or el[0] == 'notes':
                                continue
                            else:
                                tmp_dict_data[el[0]] = el[1]
                else:
                    tmp_dict_data[element] = set_series['sets'][single_set][element]
            except KeyError:
                tmp_dict_data[element] = np.NaN
        df_tmp = pd.DataFrame([tmp_dict_data])
        df = pd.concat([df, df_tmp], ignore_index=True)

df.to_excel('C:/Users/user/Desktop/second_part_test.xlsx', index=False) # here change
