from os import path, listdir, environ

BUILDING_RTD = environ.get("RCUTE_AI_RTD") == "1"
if not BUILDING_RTD:
    from PIL import Image, ImageFont, ImageDraw
    import numpy as np
    import math

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
        char_per_line = min(w//15, len(text))
        lines = min(math.floor(h/20), math.ceil(len(text)/char_per_line))
    else:
        char_per_line = len(text)
        lines = 1
    img = Image.new('RGB', (15*char_per_line, 20*lines), 'black')
    draw = ImageDraw.Draw(img)
    ind = 0
    for i in range(lines):
        draw.text((0,20*i), text[ind:ind+char_per_line], font=_font, textColor=(255,255,255))
        ind += char_per_line
    return np.asarray(img)/255
