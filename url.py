from urllib.request import Request, urlopen
import pandas as pd


req = Request(
    url='https://promoklocki.pl/lego-duplo-10928-piekarnia-p18711',
    #url='https://promoklocki.pl/lego-duplo-10924-zygzak-mcqueen-na-wyscigach-p19316',
    headers={'User-Agent': 'Mozilla/5.0'}
)
webpage = urlopen(req).read().decode("utf-8")

df = pd.DataFrame(columns=['Status'])
from bs4 import BeautifulSoup
soup = BeautifulSoup(webpage, 'html.parser')
#print(soup.prettify())
print("##################")
comments = soup.findAll('meta',{'property':"og:url"})
comments = str(comments)

comments = comments.split('>')

link= comments[3]
link= str(link)

link= link.replace('<meta content="','')
link= link.replace('" property="og:image"/','')

print(link)


