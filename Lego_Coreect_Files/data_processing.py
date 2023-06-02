# Sixth file to run
import warnings
import pandas as pd
from pandas.errors import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

df_main = pd.read_excel('lego_retail_price.xlsx')
df_history = pd.read_excel('lego_data_price_history.xlsx')

# Processing data in df_main

for i, price in enumerate(df_main['PL_retailPrice']):
    if isinstance(price, str) and price != 'Lack of data':
        x = price.split('"')[-1]
        y = x.strip().split()[0].replace('zł', '')
        df_main['PL_retailPrice'][i] = y

for i, price in enumerate(df_main['PL_retailPrice']):
    if isinstance(price, str) and price != 'Lack of data':
        x = price.replace(',', '.')
        df_main['PL_retailPrice'][i] = x

df_merge = pd.merge(df_main, df_history, left_on='url_all_history', right_on='url')
df_merge.drop('url', axis=1, inplace=True)
df_merge.to_excel('lego_merge_main_with_history_prices.xlsx', index=False)

correct_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 26, 27, 28, 29, 30, 31, 34, 32, 33, 37, 14, 15, 16, 17,
                 18, 19, 20, 21, 22, 23, 24, 25, 38, 39, 40, 35, 36]

df_correct_order = df_merge.iloc[:, correct_order]

df_correct_order.rename(columns={'min': 'minAge', 'max': 'maxAge', 'url_all_retail': 'urlRetailPriceCheckPLN',
                                 'url_all_history': 'urlRetailPriceHistoryPLN', 'Price': 'PriceMonthPLN'}, inplace=True)

to_change = []
for el in df_merge['status']:
    if el == 'Produkt wycofany':
        to_change.append('Retired Product')
    elif el == 'Dostępne teraz':
        to_change.append('Available now')
    elif el == 'Wyprzedano':
        to_change.append('Sold out')
    elif el == 'Chwilowo niedostępne':
        to_change.append('Temporarily out of stock')
    elif el == 'Upominek przy zakupie':
        to_change.append('A gift upon purchase')
    elif el == 'Zabawa zaczyna się… teraz':
        to_change.append('Available now')
    elif el == 'Lack of data':
        to_change.append('Lack of data')
    elif el.startswith('Wkrótce'):
        to_change.append('Coming Soon')
    elif el.startswith('Przyjmujemy'):
        to_change.append('Backorders Accepted')
    elif el.startswith('Zamów'):
        to_change.append('Pre-Order')

df_correct_order['status'] = to_change

df_correct_order.to_excel('lego_final_data.xlsx', index=False)
