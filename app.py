import os
from PIL import ImageGrab,ImageEnhance,ImageOps
import win32gui
import numpy as np
import pyocr
import pyocr.builders
import json
from collections import OrderedDict
import pyperclip

def windowOCR ():
    TARGET_NAME = 'umamusume'
    handle = win32gui.FindWindow(None, TARGET_NAME)

    rect = win32gui.GetWindowRect(handle)
    #print(rect)

    width = rect[2]-rect[0]
    height = rect[3]-rect[1]
    #print(width,height)

    left = rect[0] + width*0.16
    right = rect[2] - width*0.35
    top = rect[1] + height*0.21
    bottom = rect[3] - height*0.76
    #print(left,right,top,bottom)

    new_rect = [left,top,right,bottom]
    #print(new_rect)

    img = ImageEnhance.Sharpness(ImageEnhance.Brightness(ImageOps.invert(ImageGrab.grab(new_rect).convert('L'))).enhance(2)).enhance(2)
    img.save("PIL_capture_clip.png")

    # 1.インストール済みのTesseractのパスを通す
    path_tesseract = "C:\\Program Files\\Tesseract-OCR"
    if path_tesseract not in os.environ["PATH"].split(os.pathsep):
        os.environ["PATH"] += os.pathsep + path_tesseract

    # 2.OCRエンジンの取得
    tools = pyocr.get_available_tools()
    tool = tools[0]

    # 3.原稿画像の読み込み
    #img_org = Image.open("./card_image/zairyucard_omote.jpg")

    # 4.ＯＣＲ実行
    builder = pyocr.builders.TextBuilder()
    result = tool.image_to_string(img, lang="jpn", builder=builder)

    print(result)
    return result.split(' ',1)[0]

def eventsearch(eventName):
    print(eventName)
    f = open('uma_event_datas.js', 'r',encoding='utf-8')
    #w = open('uma_event.json','w',encoding='utf-8')
    event_datas = f.read().split(';',2)[0].split('\n',2)[2].rsplit('\n',2)[0].rsplit(',',1)[0].replace('\'','\"').replace(',]',']').replace(',}','}').replace('[br]','').split('\n')
    #w.write(event_datas)
    #w.close()
    f.close()

    ary = [];
    for s in event_datas:
        try:
            event = json.loads(s.rsplit(',',1)[0])
            #print(event)
            if eventName in event['e']:
                 print('match:',event['choices'])
                 ary += [event]
        except Exception as e:
            print(e)
            #print('err',s)

    print(ary)

#eventsearch(windowOCR ())
pyperclip.copy(windowOCR ())
