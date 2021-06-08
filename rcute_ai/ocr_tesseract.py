import pytesseract
import cv2
from . import util

class OCR:
    lang_map = {'zh': 'chi_sim', 'cn': 'chi_sim'}

    def __init__(self, lang='zh'):
        self._lang = lang

    @property
    def lang(self):
        """default language"""
        return self._lang

    @lang.setter
    def lang(self, lang):
        self._lang = lang

    @classmethod
    def get_lang_list(cl):
        """get all supported languages"""
        return pytesseract.get_languages(config='')

    @staticmethod
    def filter(detected):
        strings, locations = [], []
        text, left,top,width,height,conf = detected['text'], detected['left'],detected['top'],detected['width'],detected['height'],detected['confidence']
        for i in range(len(text)):
            if int(conf[i]) <0 or not text[i].strip():
                continue
            strings.append(text[i])
            locations.append((left[i]+w[i]//2,top[i]+h[i]//2,w[i],h[i]))
        return locations, strings

    def detect(self, img, *, lang=None, annotate=False):
        """detect and recognize text in image

        :param img: image in which to recognize text
        :type img: numpy.ndarray
        :param lang: language, default is None so the default language is used
        :type lang: str
        :param annotate: whether or not to annotate detected results on image
        :type annotate: bool
        :return: location list and string list, each element in location list is a tuple of `(centerX, centerY, width, height)`
        :rtype: tuple
        """
        lang = lang or OCR.lang_map.get(self._lang, self._lang)
        res = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang=lang)
        locations, strings = OCR.filter(res)
        annotate and self.annotate(img, locations, strings)
        return locations, strings

    def annotate(self, img, locations, strings=None, color='red'):
        """draw boxes around detected text on image"""
        color = util.bgr(color)
        for x,y,w,h in locations:
            x,y = x-w//2, y-h//2
        cv2.rectangle(img, (x,y), (x + w, y + h), color, 1)
