#NIE DZIAŁA :))))

from urllib.request import Request, urlopen
import pandas as pd


req = Request(
    url='https://promoklocki.pl/lego-friends-41709-wakacyjny-domek-na-plazy-p21745',
    headers={'User-Agent': 'Mozilla/5.0'}
)
webpage = urlopen(req).read().decode("utf-8")
#print(type(webpage))
#print(webpage)

df = pd.DataFrame(columns=['Catalog_price'])
from bs4 import BeautifulSoup
soup = BeautifulSoup(webpage, 'html.parser')
#print(soup.prettify())
#print("##################")
comments = soup.findAll("dd", {"class":"col-6 col-lg-7"})

#print(len(comments))
comments = list(comments)
#print(comments)


price = comments[6]
#print(price)
price = str(price)

i = price.split('<')
i = str(i)
j = i.split('>')
j = list(j)


z = j[1]
z= str(z)
catalog_price = z[:9]

#print(catalog_price)