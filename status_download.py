# Second file to run
import pandas as pd
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests

# variables
year = 2014

df_brick_set = pd.read_excel('lego_brickset.xlsx')
df = df_brick_set.sort_values('year', ascending=False)
list_of_sets_all = df['number'].values.tolist()
df_after_year = df[df['year'] > year]
list_of_sets = df_after_year['number'].values.tolist()
status_all = []
error_list = []

print('Loading status from Lego.com')
for x, number in enumerate(list_of_sets):
    value = x / len(list_of_sets)
    print(f'{round(value * 100, 3)} %')
    try:
        url = f'https://www.lego.com/pl-pl/product/{number}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(req.content, 'lxml')
        div_one = soup.find("div", {"class": "ProductOverviewstyles__PriceAvailabilityWrapper-sc-1a1az6h-10 fCBTFc"})
        status = div_one.find("span", {"class": "Markup__StyledMarkup-nc8x20-0 epIXnJ"}).text
        status_all.append(status)
    except (HTTPError, requests.exceptions.TooManyRedirects, AttributeError) as e:
        status_all.append('Lack of data')
        error_list.append(number)
        continue

death_status = 'Produkt wycofany'
list_death = [death_status] * (len(list_of_sets_all) - len(status_all))
final_list_of_status = status_all + list_death

df['status'] = final_list_of_status
df.to_excel('lego_status.xlsx', index=False)

with open('lack_in_system.txt','w') as f:
    for i in error_list:
        f.write(i)
        f.write('\n')