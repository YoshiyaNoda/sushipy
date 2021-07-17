import moji
import pyautogui as pa
import time
start = time.time()
pa.mouseDown(x = 765, y = 588, button = 'left')
pa.mouseUp()
pa.typewrite(" ", interval = 0.0)
nowtime = time.time()
while True:
    if time.time() - nowtime > 1.5:
        break
i = 0
while True:
    if time.time() - nowtime > 300:
        break
    print(i)
    img = pa.screenshot(
        imageFilename="./images/screenshot" + str(i) + ".png",    # 保存先ファイル名
        region=(797, 588, 275, 30)    # 撮影範囲(x,y,width,height)
    )
    string = moji.moji("./images/screenshot" + str(i))
    pa.typewrite(string, interval = 0.0)
    print(string)
    nowtime1 = time.time()
    while True:
        if time.time() - nowtime1 > 0.25:
            break
    i += 1
