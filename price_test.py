#ALE ZA TO TEST DZIAŁA :))))

from urllib.request import Request, urlopen
import pandas as pd


req = Request(
    url='https://promoklocki.pl/lego-okolicznosciowe-40499-sanie-swietego-mikolaja-p21527',
    #url='https://promoklocki.pl/lego-friends-41448-kino-w-heartlake-city-p21135 ',
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
comments = soup.findAll("td")

z= comments[23]
z= str(z)

z= z.replace('<','')
z= z.replace('td','')
z= z.replace('>','')
z= z.replace('/','')
print(z)




