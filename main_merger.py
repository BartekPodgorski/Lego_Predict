import pandas as pd
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
pd.set_option('display.max_columns', 10)
df_brick_set = pd.read_excel('C:/Users/user/Desktop/lego_data_brikset.xlsx')
print(df_brick_set.head())
df = df_brick_set.sort_values('year', ascending=False)
#print(df.head())
#print(df.info())
list_of_sets_all = df['number'].values.tolist()
#print(list_of_sets[-1])
df_after_2014 = df[df['year'] > 2014]
list_of_sets = df_after_2014['number'].values.tolist()
ile = len(list_of_sets)
first_part = ile/4 # 313
print(first_part)  # 313:626
second_part = ile/4 * 2
print(second_part) # 626:939
third_part = ile/4 * 3 # 939:
print(third_part)
print(ile)

j = 0
status_all = []
error_list = []
for number in list_of_sets[939:]:
    print(number)
    j += 1
    print((j/ile) * 100)
    try:
        req = Request(
            url=f'https://www.lego.com/pl-pl/product/{number}',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        webpage = urlopen(req).read().decode("utf-8")
        soup = BeautifulSoup(webpage, 'html.parser')
        comments = soup.findAll("span", {"class": "Markup__StyledMarkup-sc-nc8x20-0 dbPAWk"})
        comments = str(comments)
        ncomments = list(comments.split('<'))
        a = 'teraz'
        b = 'niedostępne'
        c = 'Wyprzedano'
        d = 'wycofany'
        e = '2023'
        f = 'zakupie'

        status = ''
        print(ncomments)
        try:
            for i in ncomments:
                if i.endswith(a) or i.endswith(b) or i.endswith(c) or i.endswith(d) or i.endswith(e) or i.endswith(f):
                    status = str(i)
                    print(status)
            info_status = status.split('>')[1]
            status_all.append(info_status)
        except IndexError:
            print(f'Error with set {number}')
            status_all.append('Potential_error')
            error_list.append(number)
    except HTTPError:
        status_all.append('Brak danych')
        continue

death_status = 'Produkt wycofany'
list_death = [death_status] * (len(list_of_sets_all) - len(status_all))
final_list_of_status = status_all + list_death

df['status'] = final_list_of_status
df.to_excel('C:/Users/user/Desktop/lego_data_with_status4.xlsx', index=False)

print(error_list)
with open('C:/Users/user/Desktop/zjebane4.txt','w') as f:
    for i in error_list:
        f.write(i)