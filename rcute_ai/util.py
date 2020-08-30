from os import path, listdir, environ

BUILDING_RTD = environ.get("RCUTE_AI_RTD") == "1"
if not BUILDING_RTD:
    from PIL import Image, ImageFont, ImageDraw
    import numpy as np
    import math
    import cv2

RESOURCES = path.join(path.dirname(__file__), '../resources')
def resource(file):
    return path.join(RESOURCES, file)

def hotword_model_list_snowboy():
    return listdir(resource('snowboy/hotword_models'))

def hotword_list_snowboy():
    return [w.split('/')[-1].split('.')[0] for w in hotword_model_list()]

import logging
logger = logging.getLogger('rcute-ai')

if not BUILDING_RTD:
    _font = ImageFont.truetype(resource("msyh.ttc"), 15)

def create_text_image(text, area=None):
    if area:
        w, h = area
        char_per_line = min(w//9, len(text))
        lines = max(1, min(math.floor(h/20), math.ceil(len(text)/char_per_line)))
    else:
        char_per_line = len(text)
        lines = 1
    img = Image.new('RGB', (9*char_per_line, 20*lines), 'black')
    draw = ImageDraw.Draw(img)
    ind = 0
    for i in range(lines):
        draw.text((0,20*i), text[ind:ind+char_per_line], font=_font, textColor=(255,255,255))
        ind += char_per_line
    return np.divide(np.asarray(img), 255)

def imshow(img, win='', wait=1):
    """显示图像

    .. code:: python

        rcute_ai.imshow(img)

    等同于：

    .. code:: python

        cv2.imshow('', img)
        cv2.waitKey(1)


    :param img: 要显示的图像
    :type img: numpy.ndarray
    :param win: 图像窗口的名字
    :type win: str
    :param wait: `cv2.waitKey()`的参数，默认是 `1`
    :type wait: int
    """
    cv2.imshow(win, img)
    cv2.waitKey(wait)

def imclose(win=None):
    '''关闭图像窗口

    :param win: 要关闭的图像窗口的名字，默认是 `None`，表示关闭所有图形窗口
    :type win: str
    '''
    cv2.destroyWindow(win) if win else cv2.destroyAllWindows()


