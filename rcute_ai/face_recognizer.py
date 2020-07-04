from . import util

if not util.BUILDING_RTD:
    import face_recognition
    import cv2
    from PIL import Image, ImageFont, ImageDraw
    import numpy as np


def resize_320x240(img):
    h, w, c = img.shape
    fx, fy = 320/w, 240/h
    if fx <= fy <= 1:
        return cv2.resize(img, (0,0), fx=fx, fy=fx), 1/fx
    elif fy <= fx <=1:
        return cv2.resize(img, (0,0), fx=fy, fy=fy), 1/fy
    return img, 1

class FaceRecognizer:
    """人脸识别器，是对 |face_recognition| 的简单封装，可以从图像中检测人脸的位置并与已知的人脸对比识别他/她们是谁

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
        self._font = ImageFont.truetype(util.resource("msyh.ttc"), 15)
        self._unknown_name_image = self._create_name_image("陌生人")

    def _create_name_image(self, name):
        img = Image.new('RGB', (15*len(name), 20), 'black')
        draw = ImageDraw.Draw(img)
        draw.text((0,0), name, font=self._font, textColor=(255,255,255))
        return np.asarray(img)/255

    def memorize(self, name, file_or_img):
        """记住某一个人的脸，若在后续的识别中看到这个人脸，就能得到他/她的名字

        :param name: 要记住的人的名字
        :type name: str
        :param file_or_img: 要记住的人脸的样子，可以是图像文件的路径，也可以是图像数据本身（numpy三维数组）
        :type file_or_img: Union[str, numpy.ndarray]
        :raises AssertionError: 不能再次记住同一个人，否则抛出异常。若要“更新记忆”，先要“忘记”这个人，再从新“记住”
        """
        assert self._face_names.get(name) == None, f'{name} is already in memory'
        if isinstance(file_or_img, str):
            file_or_img = face_recognition.load_image_file(file_or_img)
        elif self._use_bgr:
            file_or_img = file_or_img[:, :, ::-1]
        self._face_encodings.append(face_recognition.face_encodings(file_or_img)[0])
        self._face_names.append(name)
        self._name_images.append(self._create_name_image(name))

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

    def recognize(self, img):
        """从图像中识别人脸

        :param img: 用来识别的图像
        :type img: numpy.ndarray
        :return: 返回识别到的人脸的位置数组和对应的名字数组

            位置数组中的每个元素是一个 `tuple` ，包含人脸中心的坐标和人脸的宽和高： `(centerX, centerY, width, height)`
        :rtype: tuple
        """
        img, resize_factor = resize_320x240(img)
        if self._use_bgr:
            img = img[:, :, ::-1]
        locations = face_recognition.face_locations(img)
        ret_locations = [((left+right)/2, (top+bottom)/2, right-left, bottom-top) for top, right, bottom, left in locations]
        ret_locations = [(int(a*resize_factor) for a in p) for p in ret_locations]
        names = []
        for encoding in face_recognition.face_encodings(img, locations):
            matches = face_recognition.compare_faces(self._face_encodings, encoding)
            face_distances = face_recognition.face_distance(self._face_encodings, encoding)
            if face_distances:
                best_match_index = np.argmin(face_distances)
                name = self._face_names[best_match_index] if matches[best_match_index] else None
            else:
                name = None
            names.append(name)
        return ret_locations, names

    def draw_labels(self, img, locations, names=None, color=(0,0,180), text_color=(255,255,255)):
        """在图像中框出人脸，并标记上对应的名字

        :param img: 要标记的图像，应该是被 :func:`recognize` 识别过的同一个图像
        :type img: numpy.ndarray
        :param locations: 人脸的位置数组
        :type locations: list
        :param names: 与位置数组对应的名字数组，默认是 `None` ，表示不标注名字
        :type names: list, optional
        :param color: 方框的颜色，默认是BGR= `(0,0,180)` 的红色
        :type color: tuple, optional
        :param text_color: 名字的颜色，默认是白色 `(255,255,255)`
        :type text_color: tuple, optional
        """
        if not self._use_bgr:
            r, g, b = color
            color = b, g, r
            r, g, b = text_color
            text_color = b, g, r
        H, W = img.shape[:2]
        if names:
            for (x, y, w, h), name in zip(locations, names):
                x, y = x-w//2, y-h//w
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 1)
                try:
                    index = self._face_names.index(name)
                except ValueError:
                    name_image = self._unknown_name_image
                else:
                    name_image = self._name_images[index]
                nh, nw = name_image.shape[:2]
                sy, sy1, sx, sx1 = min(H, y), min(H, y+20), min(W, x), min(W, x+nw)
                cv2.rectangle(img, (x, sy), (sx1, sy1), color, cv2.FILLED)
                # font = cv2.FONT_HERSHEY_DUPLEX
                # cv2.putText(img, name if name else 'Unknown', (x+6, y1-6), font, 0.5, (255, 255, 255), 1)
                # img[sy:sy1, sx:sx1] = cv2.bitwise_or(img[sy:sy1, sx:sx1], name_image)
                img[sy:sy1, sx:sx1] = (img[sy:sy1, sx:sx1]*(1-name_image)+name_image*text_color).astype(np.uint8)
        else:
            for x, y, w, h in self.face_locations:
                x, y = x-w//2, y-h//w
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 1)









