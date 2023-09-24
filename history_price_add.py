# Fifth file to run
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
df = pd.read_excel('lego_retail_price.xlsx')
list_url = df['url_all_history'].to_list()
list_url_final = []

final_df = pd.DataFrame(columns=['Date', 'Price','url'])

for i in list_url:
    if i.startswith('https'):
        list_url_final.append(i)

for x, url in enumerate(list_url_final):
    value = x / len(list_url_final)
    print(f'{round(value * 100, 3)} %')
    try:
        df = pd.DataFrame(columns=['Date', 'Price'])
        req = Request(
            url=url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        try:
            webpage = urlopen(req).read().decode("utf-8")
            soup = BeautifulSoup(webpage, 'lxml')
            comments = soup.findAll('script', attrs={"type": "text/javascript"})
            string_name = ''
            for i in comments:
                if len(i.attrs) == 1:
                    string_name = str(i)
                else:
                    continue
            tmp_list = string_name.split(';')
            for i in tmp_list:
                if i.startswith('data.addRow'):
                    # print(i.split(')'))
                    if i.endswith('null])'):
                        x = i.split(',')
                        date = x[0].split("'")[1]
                        date = datetime.fromisoformat(date).date()
                        price = '0,00'
                        tmp_dict = {'Date': date, 'Price': price}
                        df_dictionary = pd.DataFrame([tmp_dict])
                        df = pd.concat([df, df_dictionary], ignore_index=True)
                    else:
                        x = i.split('parse')
                        date = x[0].split("'")[1]
                        date = datetime.fromisoformat(date).date()
                        y = x[1].split('(')
                        price = y[1].split(')')[0]
                        tmp_dict = {'Date': date, 'Price': price}

                        df_dictionary = pd.DataFrame([tmp_dict])
                        df = pd.concat([df, df_dictionary], ignore_index=True)

            df['Date'] = pd.to_datetime(df['Date'])
            df['Price'] = df['Price'].apply(lambda x: x.replace(',', '.'))
            df['Price'] = df['Price'].astype(float)
            df = df.groupby(pd.PeriodIndex(df['Date'], freq="M"))['Price'].max()
            price = df.to_list()
            index_date = df.index.to_list()
            index_date_str = [str(i) for i in index_date]
            url_to_add = []
            for i in range(len(price)):
                url_to_add.append(url)
            df_to_add = pd.DataFrame(data={'Date':index_date_str, 'Price':price,'url':url_to_add})
            final_df = pd.concat([final_df, df_to_add], ignore_index=True)
        except IndexError:
            print(url)
            continue
    except ValueError:
        continue

final_df.to_excel('lego_data_price_history.xlsx', index=False) # to merge on url
