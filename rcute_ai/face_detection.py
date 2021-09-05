from . import util
import face_recognition
import cv2
import numpy as np


def resize_320x240(img):
    h, w, c = img.shape
    fx, fy = 320/w, 240/h
    if fx <= fy <= 1:
        return cv2.resize(img, (0,0), fx=fx, fy=fx), 1/fx
    elif fy <= fx <=1:
        return cv2.resize(img, (0,0), fx=fy, fy=fy), 1/fy
    return img, 1

class FaceDetector:
    """人脸识别类，是对 |face_recognition| 的简单封装，可以从图像中检测人脸的位置并与已知的人脸对比识别他/她们是谁

    .. |face_recognition| raw:: html

       <a href='https://pypi.org/project/face-recognition/' target='blank'>face_recognition</a>


    :param use_bgr: 要识别的图片是否是“BGR”色彩模式，默认是 `True` ，“BGR”是opencv默认的模式，设为 `False` 则表示使用“RGB”模式
    :type use_bgr: bool, optional
    """

    def __init__(self, use_bgr=True):
        self._face_encodings = []
        self._face_names = []
        self._name_images = []
        self._use_bgr = use_bgr
        self._unknown_name_image = util.create_text_image("Unknown")

    def memorize(self, name, image):
        """记住某一个人的脸，若在后续的识别中看到这个人脸，就能得到他/她的名字

        :param name: 要记住的人的名字
        :type name: str
        :param file_or_img: 要记住的人脸的样子，可以是图像文件的路径，也可以是图像数据本身（numpy三维数组）
        :type file_or_img: str / numpy.ndarray
        :raises RuntimeError: 如果提供的图像中检测不到人脸，则抛出异常
        :raises AssertionError: 不能再次记住同一个人，否则抛出异常。若要“更新记忆”，先要“忘记”这个人，再从新“记住”

        """
        file_or_img, resize_factor = resize_320x240(image)
        assert name not in self._face_names, f'{name} is already in memory'
        if isinstance(file_or_img, str):
            file_or_img = face_recognition.load_image_file(file_or_img)
        elif self._use_bgr:
            file_or_img = file_or_img[:, :, ::-1]
        locations = face_recognition.face_locations(file_or_img)
        encodings = face_recognition.face_encodings(file_or_img, locations)
        if not encodings:
            raise RuntimeError('No face found in image')
        self._face_encodings.append(encodings[0])
        self._face_names.append(name)
        self._name_images.append(util.create_text_image(name))

    def forget(self, name):
        """忘记某一个人的脸，即从记忆中删除对应的人脸信息

        :param name: 要忘记的人的名字
        :type name: str
        :raises ValueError: 当记忆中本没有这个名字时抛出异常
        """
        i = self._face_names.index(name)
        del self._face_names[i]
        del self._face_encodings[i]
        del self._name_images[i]

    @property
    def memory(self):
        """已经记住的所有人的名字的数组"""
        return list(self._face_names)

    def detect(self, image, *, annotate=False):
        """从图像中识别人脸

        :param image: 用来识别的图像
        :type image: numpy.ndarray
        :param annotate: whether or not to annotate detected results on image
        :type annotate: bool
        :return: 返回识别到的人脸的位置数组和对应的名字数组

            位置数组中的每个元素是一个 `tuple` ，包含人脸中心的坐标和人脸的宽和高： `(x, y, w, h)`
        :rtype: tuple
        """
        img, resize_factor = resize_320x240(image)
        if self._use_bgr:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(img)
        ret_locations = [(left, top, right-left, bottom-top) for top, right, bottom, left in locations]
        ret_locations = [tuple(int(a*resize_factor) for a in p) for p in ret_locations]
        if not self._face_encodings:
            annotate and self.annotate(image, ret_locations)
            return ret_locations, [None]*len(ret_locations)
        names = []
        for encoding in face_recognition.face_encodings(img, locations):
            matches = face_recognition.compare_faces(self._face_encodings, encoding)
            face_distances = face_recognition.face_distance(self._face_encodings, encoding)
            if face_distances is not None:
                best_match_index = np.argmin(face_distances)
                name = self._face_names[best_match_index] if matches[best_match_index] else None
            else:
                name = None
            names.append(name)
        annotate and self.annotate(image, ret_locations, names)
        return ret_locations, names

    def annotate(self, img, boxes, names=None, color='red', text_color='white'):
        """在图像中框出人脸，并标记上对应的名字

        :param img: 要标记的图像，应该是被 :func:`recognize` 识别过的同一个图像
        :type img: numpy.ndarray
        :param boxes: 人脸的位置数组
        :type boxes: list
        :param names: 与位置数组对应的名字数组，默认是 `None` ，表示不标注名字
        :type names: list, optional
        :param color: 方框的颜色，默认是红色
        :type color: tuple, optional
        :param text_color: 名字的颜色，默认是白色
        :type text_color: tuple, optional
        """
        color = util.bgr(color)
        text_color = util.bgr(text_color)
        if not self._use_bgr:
            color = color[::-1]
            text_color = text_color[::-1]
        H, W = img.shape[:2]
        if names:
            for (x, y, w, h), name in zip(boxes, names):
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 1)
                try:
                    index = self._face_names.index(name)
                except ValueError:
                    name_image = self._unknown_name_image
                else:
                    name_image = self._name_images[index]
                nh, nw = name_image.shape[:2]
                sy, sy1, sx, sx1 = min(H, y+h-nh), min(H, y+h), min(W, x), min(W, x+nw)
                cv2.rectangle(img, (x, sy), (sx1, sy1), color, cv2.FILLED)
                # font = cv2.FONT_HERSHEY_DUPLEX
                # cv2.putText(img, name if name else 'Unknown', (x+6, y1-6), font, 0.5, (255, 255, 255), 1)
                # img[sy:sy1, sx:sx1] = cv2.bitwise_or(img[sy:sy1, sx:sx1], name_image)
                img[sy:sy1, sx:sx1] = (img[sy:sy1, sx:sx1]*(1-name_image)+name_image*text_color).astype(np.uint8)
        else:
            for x, y, w, h in boxes:
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 1)









