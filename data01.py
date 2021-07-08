import requests
from bs4 import BeautifulSoup
import os
import sqlite3

url = 'https://www.ptt.cc/bbs/hotboards.html'
urlbase = 'https://www.ptt.cc'

r = requests.get(url)
web_content = r.text
soup = BeautifulSoup(web_content, 'html.parser')
boardElements = soup.find_all('a', class_='board')

#print (boardElements)
boardNames = [e.text for e in boardElements] #becomes a  list
#print (boardNames)
boardURLs = []

for index in range(len(boardNames)):
    url = urlbase + boardElements[index].get('href')
    print (url)
    boardURLs.append(url)

boardNameElements = soup.find_all('div', class_='board-name')
boardNames = [e.text for e in boardNameElements] #becomes a  list
#print (boardNames)

popularityElements = soup.find_all('div', class_="board-nuser")
# 取出的文字的類型是字串, 我們可用int()轉成數字類型
popularities = [int(e.text) for e in popularityElements]

for pop, bn , url in zip(popularities, boardNames , boardURLs):
    print(pop, bn , url)

dbPath = 'ptt.db'

connection = sqlite3.connect(dbPath)
cursor = connection.cursor()
sqlstmt = 'CREATE TABLE records (boardnames text, popularity int, url text)'
cursor.execute(sqlstmt)

for bn, pop, url in zip(boardNames, popularities, boardURLs):
    cursor.execute('INSERT INTO records VALUES (?,?,?)' , (bn, pop, url))

connection.commit()
connection.close()


