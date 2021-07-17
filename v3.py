from os import read
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import timeout_decorator
import sys
import time
import csv
import difflib

from PIL import Image
from io import BytesIO
import pyocr
import pyocr.builders

import pyautogui as pa

url = "http://typingx0.net/sushida/play.html"
driver = webdriver.Chrome("./chromedriver")
driver.get(url)

k = input("スタートするにはENTERを押してください")
print('終了するにはctrl+c')

clickaction = ActionChains(driver)
actions = ActionChains(driver)
clickaction.click()

image_path = './images/screenshot.png'

tools = pyocr.get_available_tools() # OCRツールの有無の確認
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]
lang = 'eng'

@timeout_decorator.timeout(2)
def ocr():
    element = driver.find_element_by_id('#canvas')
    location = element.location
    size = element.size
    png = driver.get_screenshot_as_png()
    im = Image.open(BytesIO(png)) # uses PIL library to open image in memory
    left = location['x'] + 310
    top = location['y'] + size['height'] + 165
    right = (location['x'] + size['width']) * 2 - 170
    bottom = location['y'] + size['height'] * 2 - 200
    # print([left, top, right, bottom])

    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save(image_path) # saves new cropped image

    txt = tool.image_to_string( # ここでOCRの対象や言語，オプションを指定する
        Image.open(image_path),
        lang = 'eng',
        builder = pyocr.builders.TextBuilder()
    )
    return txt

#元データ
data = []
with open("alpha.csv", "r", encoding='utf-8') as file:
    for row in csv.reader(file):
        data.append(row[0])

def sim(rt):
    text = ''
    m_score = 0
    for d in data:
        s = difflib.SequenceMatcher(None, d, rt).ratio()
        if s >= m_score:
            m_score = s
            text = d
    return text

@timeout_decorator.timeout(10000)
def mainloop():
    before = ''
    counter = 0
    while True:
        read_text = ocr()
        text = read_text
        print(text)
        # actions.send_keys(text).perform() #これうまくいかないのなんでだろ textそのまま入力したのがダメなのかな
        pa.typewrite(text, interval = 0.0)
        time.sleep(0.05)
        counter += 1
        if counter > 206:
            break
        


try:
    mainloop()
except:
    print('終了です')
else:
    print('終了できませんでした')
finally:
    driver.close()