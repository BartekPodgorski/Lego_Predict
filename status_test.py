from urllib.request import Request, urlopen
import pandas as pd


req = Request(
    url='https://www.lego.com/pl-pl/product/grand-piano-21323',
    headers={'User-Agent': 'Mozilla/5.0'}
)
webpage = urlopen(req).read().decode("utf-8")
#print(type(webpage))
#print(webpage)

df = pd.DataFrame(columns=['Status'])
from bs4 import BeautifulSoup
soup = BeautifulSoup(webpage, 'html.parser')
#print(soup.prettify())
print("##################")
comments = soup.findAll("span", {"class":"Markup__StyledMarkup-sc-nc8x20-0 dbPAWk"})

print(len(comments))
comments = str(comments)


ncomments =list(comments.split('<'))
print(ncomments)


a='teraz'
b='niedostepne'

status =''
for i in ncomments:
    if i.endswith(a or b):
       status = str(i)

print(status)

#info_status = status.split('>')[1]

#print(info_status)