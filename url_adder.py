import pandas as pd
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
pd.set_option('display.max_columns', 10)
df_brick_set = pd.read_excel('C:/Users/user/Desktop/lego_data_brikset.xlsx')
df = df_brick_set.sort_values('year', ascending=False)
list_of_sets_all = df['number'].values.tolist()
url_all = []
ile = len(list_of_sets_all)
i =0
for number in list_of_sets_all:
    i +=1
    print((i/ile) * 100)
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
            tmp_link = link.split('-')
            tmp_link[-1] = tmp_link[-1].replace('p', 'h')
            link = '-'.join(tmp_link)
            url_all.append(link)
        else:
            url_all.append(link)
    except HTTPError:
        url_all.append('Brak danych')
        continue

df['url_chart'] = url_all
df.to_excel('C:/Users/user/Desktop/lego_data_with_link_good_kurwa.xlsx', index=False)