import pandas as pd

df1 = pd.read_excel('lego_data_with_status1.xlsx')
df2 = pd.read_excel('lego_data_with_status2.xlsx')
df3 = pd.read_excel('lego_data_with_status3.xlsx')
df4 = pd.read_excel('lego_data_with_status4.xlsx')
df_price = pd.read_excel('lego_data_with_price_final.xlsx')

correct_len = len(df1['status'])
first_part = df1['status'].values.tolist()[:313]
second_part = df2['status'].values.tolist()[:313]
third_part = df3['status'].values.tolist()[:313]
fourth_part = df4['status'].values.tolist()[:313]
final_status_list = first_part + second_part + third_part + fourth_part
rest_of_list = ['Produkt wycofany'] * (correct_len - len(final_status_list))
final_status_list = final_status_list + rest_of_list

df1.drop(['status'], axis=1, inplace=True)
df1['status'] = final_status_list

#potencjalny error
for i, price in enumerate(df_price['PL_retailPrice']):
  if isinstance(price, str) and price != 'Brak danych':
    x = price.split('"')[-1]
    y = x.strip().split()[0].replace('zł','')
    df_price['PL_retailPrice'][i] = y

df_price_to_move = df_price[['setID','PL_retailPrice']]
final_df = pd.merge(df1, df_price_to_move, on='setID')
final_df.to_excel('final_lego.xlsx',index=False)