import pandas as pd
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
pd.set_option('display.max_columns', 10)
df_url = pd.read_excel('C:/Users/user/Desktop/lego_data_with_link_good_kurwa.xlsx')

list_of_url_all = df_url['url_chart'].values.tolist()

price_all = []
ile = len(list_of_url_all)
i = 0

for url in list_of_url_all:
    i += 1
    print((i/ile) * 100)
    if url.startswith('https'):
        tmp_link = url.split('-')
        tmp_link[-1] = tmp_link[-1].replace('h', 'p')
        url = '-'.join(tmp_link)
    try:
        if url == 'Brak danych':
            price_all.append('Brak danych')
            continue
        else:
            req = Request(
                url=url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, 'html.parser')
            comments = soup.findAll("td")
            try:
                price = str(comments[23])

                price = price.replace('<', '')
                price = price.replace('td', '')
                price = price.replace('>', '')
                price = price.replace('/', '')
                price = price[:-3]
                price_all.append(price)
            except IndexError:
                price_all.append('Za swiezy set')
    except HTTPError:
        price_all.append('Brak danych')
        continue

df_url['PL_retailPrice'] = price_all
df_url.to_excel('C:/Users/user/Desktop/lego_data_with_price_final.xlsx', index=False)