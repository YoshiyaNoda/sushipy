from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import timeout_decorator
import sys
import time

from PIL import Image
from io import BytesIO
import pyocr
import pyocr.builders

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

def ocr():
    element = driver.find_element_by_id('#canvas')
    location = element.location
    size = element.size
    png = driver.get_screenshot_as_png()
    im = Image.open(BytesIO(png)) # uses PIL library to open image in memory
    left = location['x']
    top = location['y'] + size['height'] + 165
    right = (location['x'] + size['width']) * 2
    bottom = location['y'] + size['height'] * 2 - 10
    # print([left, top, right, bottom])

    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save(image_path) # saves new cropped image

    txt = tool.image_to_string( # ここでOCRの対象や言語，オプションを指定する
        Image.open(image_path),
        lang = 'eng',
        builder = pyocr.builders.TextBuilder()
    )
    return txt


@timeout_decorator.timeout(1000)
def mainloop():
    before = ''
    while True:
        # text = ocr()
        # if before != text:
        #     reg_chars = list("abcdefghijklmnopqrstuvwyz-,!?")
        #     # keys = list(text)
        #     for k in text:
        #         if k in reg_chars:
        #             actions.send_keys(k).perform()
        #             print(k + " in " + text)
        #             time.sleep(0.005)
        #     # time.sleep(0.3)
        #     before = text
        actions.send_keys("abcdefghijklmnopqrstuvwyz-,!?").perform() #一文字ずつ売ったほうが良さそう


try:
    mainloop()
except:
    print('終了です')
else:
    print('終了できませんでした')
finally:
    driver.close()