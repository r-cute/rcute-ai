from . import util
import cv2
import numpy as np

class QRCodeRecognizer(cv2.QRCodeDetector):
    """二维码识别器

    :param use_bgr: 要识别的图片是否是“BGR”色彩模式，默认是 `True` ，“BGR”是opencv默认的模式，设为 `False` 则表示使用“RGB”模式
    :type use_bgr: bool, optional
    """
    def __init__(self, use_gbr=True):
        self._use_gbr = use_gbr
        cv2.QRCodeDetector.__init__(self)

    def recognize(self, img):
        """从图像中识别物体

        :param img: 用来识别的图像
        :type img: numpy.ndarray
        :return: 返回识别到的二维码的位置数组和对应的二维码信息

            位置数组中的每个元素是一个 `numpy.ndarray` ，包含二维码四个顶点的位置坐标

            如果没有识别到二维码，则返回 `(None, None)`
        :rtype: tuple
        """
        text, points = self.detectAndDecode(img)[:2]
        return (None, None) if points is None else (points.reshape(-1, 2).astype(int), text)

    def draw_labels(self, img, points, text, color=(0,0,180), text_color=(255,255,255)):
        if points is not None:
            if not self._use_gbr:
                r, g, b = color
                color = b, g, r
                r, g, b = text_color
                text_color = b, g, r
            # font = cv2.FONT_HERSHEY_DUPLEX
            # cv2.putText(img, text, tuple(points[0]), font, 0.5, color, 1)
            cv2.polylines(img, [points.reshape(-1, 1, 2)], 1, color)
            if text:
                bx, by, bw, bh=cv2.boundingRect(points)
                text_image = util.create_text_image(text, (bw, by))
                centerX, centerY = bx+bw//2, by+bh//2
                h, w = text_image.shape[:2]
                x, y = centerX-w//2, centerY-h//2
                x1, y1 = x+w, y+h
                img[y:y1, x:x1] = (color*(1-text_image)+text_image*text_color).astype(np.uint8)