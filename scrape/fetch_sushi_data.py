import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# URLの指定
html = urlopen("https://e-akane.com/blog/post-18198/")
bsObj = BeautifulSoup(html, "html.parser")

# テーブルを指定
tables = bsObj.findAll("table", {"class":""})
rows = []
for table in tables:
    rows += table.findAll("tr")

with open("data.csv", "w", encoding='utf-8') as file:
    writer = csv.writer(file)
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text())
        writer.writerow(csvRow)