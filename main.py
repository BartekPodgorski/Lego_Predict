
from urllib.request import Request, urlopen
import pandas as pd
from datetime import datetime
#<script type="text/javascript">google.charts.load( wazna linia w chuj wykres z google na date mamy czas a na float mamy cene minimalna na niej mozna sie dobrze oprzec
req = Request(
    url='https://promoklocki.pl/lego-promocyjne-5007427-przejazdzka-statkiem-pirackim-h22067',
    headers={'User-Agent': 'Mozilla/5.0'}
)
webpage = urlopen(req).read().decode("utf-8")
#print(type(webpage))
#print(webpage)

df = pd.DataFrame(columns=['Date','Price'])

from bs4 import BeautifulSoup
soup = BeautifulSoup(webpage, 'html.parser')
print(soup.prettify())
print("##################")
comments = soup.findAll('script')
print(len(comments))



j = 0

string_name = ''

for i in comments:
    print('###############################')
    if j == 5:
        string_name = str(i)
    j+=1
#print(type(soup.findAll('script')))
tmp_list = string_name.split(';')
for i in tmp_list:
    if i.startswith('data.addRow'):
        #print(i.split(')'))
        x = i.split('parse')
        date = x[0].split("'")[1]
        date = datetime.fromisoformat(date).date()
        y = x[1].split('(')
        price = y[1].split(')')[0]
        tmp_dict = {'Date': date, 'Price': price}
        df_dictionary = pd.DataFrame([tmp_dict])
        df = pd.concat([df, df_dictionary], ignore_index=True)

print(df.tail())
"""
zestaw
1 stycznia 200 # minimalna cena danego dnia 
2 stycznia 300

output = pd.DataFrame()
df_dictionary = pd.DataFrame([dictionary])
output = pd.concat([output, df_dictionary], ignore_index=True)
print(output.head())
 datetime.fromisoformat
"""