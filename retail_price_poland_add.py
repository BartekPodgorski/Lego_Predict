# Fourth file to run
import pandas as pd
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

df_url = pd.read_excel('lego_links.xlsx')
list_of_url_all = df_url['url_all_retail'].values.tolist()
price_all = []

print('Loading polish retail price from promokolocki.pl in PLN')
for x, url in enumerate(list_of_url_all):
    value = x / len(list_of_url_all)
    print(f'{round(value * 100, 3)} %')
    try:
        if url == 'Lack of data':
            price_all.append('Lack of data')
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
                price_all.append('Too fresh set')
    except HTTPError:
        price_all.append('Lack of data')
        continue

df_url['PL_retailPrice'] = price_all
df_url.to_excel('lego_retail_price.xlsx', index=False)