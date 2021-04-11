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
import cv2

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

def crop_event_choices_img(img):
    width,height = img.size

    left = width*0.03
    right = width*0.97
    top = height*0.3
    bottom = height*0.7

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


def count_event_display(img):
    choices_img = crop_event_choices_img(img)
    choices_img = np.array(choices_img, dtype=np.uint8)
    img_gray = cv2.cvtColor(choices_img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5,5), 0) 
    img_th = cv2.threshold(img_blur, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    contours,hierarchy = cv2.findContours(cv2.bitwise_not(img_th), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    img = cv2.drawContours(cv2.cvtColor(np.array(choices_img, dtype=np.uint8), cv2.COLOR_RGB2BGR), contours, -1, (0,255,0), 3)
    cv2.imshow('debug',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return len(contours)


def get_event():
    tesseract = tesseract_init()

    base_img = None
    if not st.DEBUG_IMAGE_PATH:
        while(1):
            base_img = get_window_image()
            ans = count_event_display(base_img)
            if ans==0:
                continue
            else:
                break
    else:
        base_img = Image.open(st.DEBUG_IMAGE_PATH)
        ans = count_event_display(base_img)

    img = crop_event_title_image(base_img)
    img = enhance_image(img)

    

    result = OCR(tesseract, img)

    #test code
    print(result)
    pyperclip.copy(result.split(' ',1)[0])

    #TODO イベント名と選択肢を含む配列をリターンする
    return result.split(' ',1)[0]
