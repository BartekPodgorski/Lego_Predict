# login zwroci hasha
"""
1. Cena z polski katalogowa ze strony klocki
2. Jak wziac liste wsystkich zestawow
2.1 Mozna wziac z api theme i poleceic po wsystkich np.
2.2 Poszukac na stronie lego oficial
3. Dalsze pole rozwoju branie danych z instrukcji
4. zrobienie automatyzacji na hasha
https://brickset.com/article/52664/api-version-3-documentation
Dokumentajca do API
"""

import pandas as pd
import json
import requests
from datetime import datetime
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

req = Request(
    url='https://promoklocki.pl/lego-friends-41709-wakacyjny-domek-na-plazy-h21745',
    headers={'User-Agent': 'Mozilla/5.0'}
)
webpage = urlopen(req).read().decode("utf-8")


df = pd.DataFrame(columns=['Date','Price'])

soup = BeautifulSoup(webpage, 'html.parser')
title = soup.title.get_text().split()
id_set = title[1] + '-1'
print(id_set)

apiKey = 'Tu daj apikey'
userHash = 'Tu daj hash'

url = 'https://brickset.com/api/v3.asmx/getSets'
setNumber = {'setNumber': id_set}
setNumber = json.dumps(setNumber)
querystring = {'apiKey': apiKey, 'userHash': userHash, 'params': setNumber}

response = requests.request("GET", url, params=querystring)
x = response.json()
print(json.dumps(x, indent=4))


setNumber = {"setID": 32333}
#setNumber = json.dumps(setNumber)
querystring = {'apiKey': apiKey, 'setID': 32333}
url2 = 'https://brickset.com/api/v3.asmx/getInstructions'
instra = requests.request("GET", url2, params=querystring)
x = instra.json()
print(json.dumps(x, indent=4))