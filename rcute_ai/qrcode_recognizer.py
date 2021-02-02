from . import util
import cv2
import numpy as np

class QRCodeRecognizer(cv2.QRCodeDetector):
    """二维码识别类

    :param use_bgr: 要识别的图片是否是“BGR”色彩模式，默认是 `True` ，“BGR”是opencv默认的模式，设为 `False` 则表示使用“RGB”模式
    :type use_bgr: bool, optional
    """
    def __init__(self, use_bgr=True):
        self._use_bgr = use_bgr
        cv2.QRCodeDetector.__init__(self)

    def angle_between(self, v1, v2):
        return np.arccos(np.clip(np.dot(v1, v2)/np.linalg.norm(v1)/np.linalg.norm(v2), -1, 1))

    def edges(self, pts):
        return [np.linalg.norm(pts[i]-pts[(i+1)%4]) for i in range(4)]

    def is_square(self, pts):
        # pts should be in clock or counterclock wise ordered
        if pts is None:
            return False
        edges = self.edges(pts)
        return (.8 < min(edges) / max(edges) < 1.2) and (.9 < self.angle_between(pts[0]-pts[1], pts[0]-pts[3])*2/np.pi < 1.1)

    def order4points(self, pts):
        xSorted = pts[np.argsort(pts[:, 0]), :]
        leftMost = xSorted[:2, :]
        rightMost = xSorted[2:, :]
        tl, bl = leftMost[np.argsort(leftMost[:, 1]), :]
        tr, br = rightMost[np.argsort(rightMost[:, 1]), :]
        return tr, br, bl, tl

    def recognize(self, img):
        """从图像中识别物体

        :param img: 用来识别的图像
        :type img: numpy.ndarray
        :return: 返回识别到的二维码的位置数组和对应的二维码信息

            位置数组中的每个元素是一个 `numpy.ndarray` ，包含二维码四个顶点的位置坐标

            如果没有识别到二维码，则返回 `(None, None)`
        :rtype: tuple
        """
        try:
            text, points = self.detectAndDecode(img)[:2]
            points = points is not None and points.reshape(-1, 2).astype(int)
            return (points, text) if self.is_square(points) else (None, '')
        except Exception:
            return None, ''

    def draw_labels(self, img, points, text, color=(0,0,180), text_color=(255,255,255)):
        """在图像中标记出识别到的二维码

        :param img: 要标记的图像，应该是被 :func:`recognize` 识别过的同一个图像
        :type img: numpy.ndarray
        :param points: 二维码的四个顶点
        :type points: numpy.ndarray
        :param text: 二维码的信息
        :type text: str
        :param color: 方框的颜色，默认是BGR= `(0,0,180)` 的红色
        :type color: tuple, optional
        :param text_color: 名字的颜色，默认是白色 `(255,255,255)`
        :type text_color: tuple, optional
        """
        if points is not None:
            if not self._use_bgr:
                color = color[::-1]
                text_color = text_color[::-1]
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