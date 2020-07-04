from . import util
if not util.BUILDING_RTD:
    import cv2
    import numpy as np


class ObjectRecognizer:
    """ |yolov3| coco 物品识别器，能识别 |80种物品|

    .. |yolov3| raw:: html

       <a href='https://pjreddie.com/darknet/yolo/' target='blank'>yolov3</a>

    .. |80种物品| raw:: html

       <a href='https://github.com/pjreddie/darknet/blob/master/data/coco.names' target='blank'>80种物品</a>

    .. |cv2.dnn.NMSBoxes| raw:: html

       <a href='https://docs.opencv.org/master/d6/d0f/group__dnn.html#ga9d118d70a1659af729d01b10233213ee' target='blank'>cv2.dnn.NMSBoxes</a>

    :param confidence_threshold: 默认是 `0.5`，用于 |cv2.dnn.NMSBoxes| 的参数
    :type confidence_threshold: float, optional
    :param nms_threshold: 默认是 `0.3`，用于 |cv2.dnn.NMSBoxes| 的参数
    :type nms_threshold: float, optional
    :param use_bgr: 要识别的图片是否是“BGR”色彩模式，默认是 `True` ，“BGR”是opencv默认的模式，设为 `False` 则表示使用“RGB”模式
    :type use_bgr: bool, optional
    """
    def __init__(self, *, confidence_threshold=.5, nms_threshold=.3, use_bgr=True):

        self._use_bgr = use_bgr
        self._confidence_threshold = confidence_threshold
        self._nms_threshold = nms_threshold

        labels = util.resource('yolov3/coco.names')
        config = util.resource('yolov3/yolov3-coco.cfg')
        weights = util.resource('yolov3/yolov3-coco.weights')

        with open(labels) as label_file:
            self._labels = label_file.read().strip().split('\n')
        self._net = cv2.dnn.readNetFromDarknet(config, weights)
        self._net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        # self._net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)

        self._layer_names = self._net.getLayerNames()
        self._layer_names = [self._layer_names[i[0] - 1] for i in self._net.getUnconnectedOutLayers()]

    def recognize(self, img):
        """从图像中识别物体

        :param img: 用来识别的图像
        :type img: numpy.ndarray
        :return: 返回识别到的物品的位置数组和对应的物品名字数组

            位置数组中的每个元素是一个 `tuple` ，包含物品中心的坐标和物品的宽和高： `(centerX, centerY, width, height)`
        :rtype: tuple
        """
        h, w = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (320, 320), swapRB=self._use_bgr, crop=False)
        self._net.setInput(blob)
        outs = self._net.forward(self._layer_names)
        boxes = []
        confidences = []
        class_ids = []
        for output in outs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > self._confidence_threshold:
                    box = detection[0:4] * np.array([w, h, w, h])
                    (centerX, centerY, width, height) = box.astype(int)
                    boxes.append((centerX, centerY, width, height))
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        ret_boxes = []
        ret_confidences = []
        ret_labels = []
        nms_boxes = cv2.dnn.NMSBoxes(boxes, confidences, self._confidence_threshold, self._nms_threshold)
        if len(nms_boxes):
            for i in nms_boxes.flatten():
                ret_boxes.append(boxes[i])
                ret_labels.append(self._labels[class_ids[i]])
                # ret_confidences.append(confidences[i])
        # return ret_boxes, ret_labels, ret_confidences
        return ret_boxes, ret_labels

    def draw_labels(self, img, locations, names=None, color=(0,0,180), text_color=(255,255,255)):
        """在图像中框出识别到的物品，并标记上对应的品名

        :param img: 要标记的图像，应该是被 :func:`recognize` 识别过的同一个图像
        :type img: numpy.ndarray
        :param locations: 物品的位置数组
        :type locations: list
        :param names: 与位置数组对应的品名数组，默认是 `None` ，表示不标注品名
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
        if names:
            for (x, y, w, h), name in zip(locations, names):
                x, y = x-w//2, y-h//2
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 1)
                cv2.rectangle(img, (x, y), (x+len(name)*9, y+20), color, cv2.FILLED)
                cv2.putText(img, name, (x, y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)
        else:
            for (x, y, w, h) in locations:
                x, y = x-w//2, y-h//2
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 1)





