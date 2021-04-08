import json
import os
from collections import OrderedDict

import settings as st

import numpy as np
import pyocr
import pyocr.builders
import pyperclip
if not st.DEBUG_IMAGE_PATH:
    import win32gui
from PIL import Image, ImageEnhance, ImageGrab, ImageOps

def tesseract_init():
    # 1.インストール済みのTesseractのパスを通す
    if st.TESSERACT_PATH not in os.environ["PATH"].split(os.pathsep):
        os.environ["PATH"] += os.pathsep + st.TESSERACT_PATH

    # 2.OCRエンジンの取得
    tools = pyocr.get_available_tools()
    return tools[0]


def get_window_image():
    handle = win32gui.FindWindow(None, st.TARGET_NAME)
    rect = win32gui.GetWindowRect(handle)
    ImageGrab.grab(rect)
    return image


#TODO get_event_title_image, get_event_choices_image の中でenhanceまでやる？
#TODO get_event_choices_image の呼び出し回数に応じて上に移動するか判断

def crop_event_title_image(img):
    width,height = img.size

    left = width*0.16
    right = width*0.7
    top = height*0.21
    bottom = height*0.24

    return img.crop((left,top,right,bottom))


def enhance_image(img):
    #グレースケール
    img = img.convert('L')
    #ネガポジ反転
    img = ImageOps.invert(img)

    img = ImageEnhance.Brightness(img).enhance(2)
    img = ImageEnhance.Sharpness(img).enhance(2)
    return img


def OCR(tesseract, img):
    #TODO builderをinitで作成し渡す
    builder = pyocr.builders.TextBuilder()
    return tesseract.image_to_string(img, lang="jpn", builder=builder)

#関数名はよしなに
def is_event_display():
    pass 


def get_event():
    tesseract = tesseract_init()

    #TODO 選択肢が出ているかどうかを判定するループ

    """
    while(1):
        ans = is_event_display()
        if ans == 0:
            continue
        else:
            if ans == 2:
                #OCR
                break
    """

    img = None
    if not st.DEBUG_IMAGE_PATH:
        img = get_window_image()
    else:
        img = Image.open(st.DEBUG_IMAGE_PATH)
    img = crop_event_title_image(img)
    img = enhance_image(img)

    result = OCR(tesseract, img)

    #test code
    print(result)
    pyperclip.copy(result.split(' ',1)[0])

    #TODO イベント名と選択肢を含む配列をリターンする
    return result.split(' ',1)[0]