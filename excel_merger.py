import pandas as pd

df_part_1 = pd.read_excel('C:/Users/user/Desktop/first_part.xlsx')
df_part_2 = pd.read_excel('C:/Users/user/Desktop/second_part_test.xlsx')

df = pd.concat([df_part_1, df_part_2], ignore_index=True)
df.to_excel('C:/Users/user/Desktop/lego_data_brikset.xlsx', index=False)
