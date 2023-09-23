# Third file to run
import pandas as pd
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

df_brick_set = pd.read_excel('lego_status.xlsx')
df = df_brick_set.sort_values('year', ascending=False)
list_of_sets_all = df['number'].values.tolist()
url_all_history = []
url_all_retail = []

print('Loading links from promokolocki.pl')
for x, number in enumerate(list_of_sets_all):
    value = x / len(list_of_sets_all)
    print(f'{round(value * 100, 3)} %')
    try:
        req = Request(
            url=f'https://promoklocki.pl/{number}',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        webpage = urlopen(req).read().decode("utf-8")
        soup = BeautifulSoup(webpage, 'html.parser')
        comments = soup.findAll('meta', {'property': "og:url"})
        comments = str(comments)
        comments = comments.split('>')
        link = str(comments[0])
        link = link.replace('[<meta content="', '')
        link = link.replace('" property="og:url"', '')
        if link.startswith('https'):
            url_all_retail.append(link)
            tmp_link = link.split('-')
            tmp_link[-1] = tmp_link[-1].replace('p', 'h')
            link = '-'.join(tmp_link)
            url_all_history.append(link)
        else:
            url_all_history.append(link)
            url_all_retail.append(link)
    except HTTPError:
        url_all_history.append('Lack of data')
        url_all_retail.append('Lack of data')
        continue

df['url_all_history'] = url_all_history
df['url_all_retail'] = url_all_retail
df.to_excel('lego_links.xlsx', index=False)