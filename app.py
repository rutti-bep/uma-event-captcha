import json
import os
from collections import OrderedDict

import numpy as np
import pyocr
import pyocr.builders
import pyperclip
import win32gui
from PIL import ImageEnhance, ImageGrab, ImageOps

import settings.py as st


def tesseract_init():
    # 1.インストール済みのTesseractのパスを通す
    if st.TESSERACT_PATH not in os.environ["PATH"].split(os.pathsep):
        os.environ["PATH"] += os.pathsep + st.TESSERACT_PATH

    # 2.OCRエンジンの取得
    tools = pyocr.get_available_tools()
    return tools[0]


def get_window_position():
    handle = win32gui.FindWindow(None, st.TARGET_NAME)
    rect = win32gui.GetWindowRect(handle)
    return rect


#TODO 本当は関数をループで回して、選択肢の画面かどうかと選択肢の数を出力させたい
def get_event_title_image(rect):
    width = rect[2]-rect[0]
    height = rect[3]-rect[1]

    left = rect[0] + width*0.16
    right = rect[2] - width*0.35
    top = rect[1] + height*0.21
    bottom = rect[3] - height*0.76

    new_rect = [left,top,right,bottom]
    return ImageGrab.grab(new_rect)



def enhance_image(img):
    #グレースケール
    img = img.convert('L')
    #ネガポジ反転
    img = ImageOps.invert(img)

    img = ImageEnhance.Brightness(img).enhance(2)
    img = ImageEnhance.Sharpness(img).enhance(2)
    return img


def OCR(tesseract, img):
    builder = pyocr.builders.TextBuilder()
    return tesseract.image_to_string(img, lang="jpn", builder=builder)


def get_event():
    tesseract = tesseract_init()
    rect = get_window_position()

    img = get_event_title_image(rect)
    img = enhance_image(img)

    result = OCR(tesseract, img)

    print(result)
    pyperclip.copy(result.split(' ',1)[0])

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


def main():
    get_event ()
    #eventsearch(get_event ())


if __name__ == '__main__':
    main()
