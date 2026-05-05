from bs4 import BeautifulSoup
import requests

# url='https://webscraper.io/test-sites/tables'


# response=requests.get(url)

# soup=BeautifulSoup(response.content,'html.parser')

# tables=soup.find_all('table')[1]
# rows=tables.find_all('tr')[1:]

# last_names=[]
# for row in rows:
#     last_names.append(row.find_all('td')[2].get_text())

# print(last_names)

url='https://en.wikipedia.org/wiki/Python_(programming_language)'

headers={
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
}
response=requests.get(url,headers=headers)

soup=BeautifulSoup(response.content,'html.parser')
table=soup.find('table',class_='wikitable')
body=table.find('tbody')
rows=body.find_all('tr')[1:]
immutable_data=[]
mutable_data=[]

for row in rows:
    data=row.find_all('td')
    if data[1].get_text() =='immutable\n':
        immutable_data.append(data[0].get_text().strip())
    else:
        mutable_data.append(data[0].get_text().strip())
    


print("immutabledata:",immutable_data)
print('mutabledata',mutable_data)

