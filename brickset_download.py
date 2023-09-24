# First file to run
# Documentation
# https://brickset.com/article/52664/api-version-3-documentation
# https://brickset.com/tools/webservices/requestkey
# packages
# need to install openpyxl , lxml
import requests
import json
import pandas as pd
import numpy as np

# variables
apiKey = ''
username = ''
password = ''
page_size = 1000

url_for_hash = 'https://brickset.com/api/v3.asmx/login'
query_string = {'apiKey': apiKey, 'username': username, 'password': password}
userHash = requests.request("GET", url_for_hash, params=query_string).json()['hash']

url_for_years = 'https://brickset.com/api/v3.asmx/getYears'
query_string = {'apiKey': apiKey, 'theme': ''}
all_years = requests.request("GET", url_for_years, params=query_string).json()

years_list = []
years_counts = []
total_number_of_sets = 0
for year_pair in all_years['years']:
    years_list.append(year_pair['year'])
    years_counts.append(year_pair['setCount'])
    total_number_of_sets += year_pair['setCount']

# Getting sets with data
df = pd.DataFrame()  # Dataframe with data
list_of_keys = ['setID', 'number', 'numberVariant', 'name', 'year', 'theme', 'themeGroup', 'subtheme', 'category',
                'released', 'pieces', 'minifigs', 'collections', 'LEGOCom', 'rating', 'reviewCount', 'packagingType',
                'availability', 'instructionsCount', 'ageRange', 'extendedData', 'lastUpdated']

url_for_sets = 'https://brickset.com/api/v3.asmx/getSets'

print('Loading data from Brickset.com')
for x, year in enumerate(years_list):
    value = x / len(years_counts)
    print(f'{round(value * 100, 3)} %')
    setYear = {'extendedData': 1, 'year': year, 'pageSize':page_size}
    setYear = json.dumps(setYear)
    query_string = {'apiKey': apiKey, 'userHash': userHash, 'params': setYear}
    set_series = requests.request("GET", url_for_sets, params=query_string).json()
    for set in set_series['sets']:
        tmp_dict_data = {}
        for key in list_of_keys:
            try:
                if isinstance(set[key], dict):
                    for i in set[key].items():
                        if isinstance(i[1], dict):
                            values = ['retailPrice', 'dateFirstAvailable', 'dateLastAvailable']
                            for value in values:
                                if i[1].get(value) is None:
                                    col_name = i[0] + '_' + value
                                    tmp_dict_data[col_name] = np.NaN
                                else:
                                    col_name = i[0] + '_' + value
                                    tmp_dict_data[col_name] = i[1].get(value)
                        else:
                            if i[0] == 'description' or i[0] == 'notes':
                                continue
                            else:
                                tmp_dict_data[i[0]] = i[1]
                else:
                    tmp_dict_data[key] = set[key]
            except KeyError:
                tmp_dict_data[key] = np.NaN
                continue
        df_tmp = pd.DataFrame([tmp_dict_data])
        df = pd.concat([df, df_tmp], ignore_index=True)

df.to_excel('lego_brickset.xlsx', index=False)
print(total_number_of_sets)
