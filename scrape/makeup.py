import csv
from pykakasi import kakasi
import jaconv

kakasi = kakasi()

kakasi.setMode('H', 'a')
kakasi.setMode('K', 'a')
kakasi.setMode('J', 'a')

conv = kakasi.getConverter()

def convert(text):
    row0 = text
    row0 = (row0).replace('ー', '-')
    row0 = jaconv.z2h(row0, digit=True, ascii=True, kana=True) #全角？！に対処
    row0 = row0.replace('､', ',') #、と､ は違うらしい...
    alpha = conv.do(row0)
    return alpha

with open("alpha.csv", "w", encoding='utf-8') as file:
    writer = csv.writer(file)
    with open("data.csv") as f:
        for row in csv.reader(f):
            alpha = convert(row[0])
            print(alpha)
            writer.writerow([alpha])
        

