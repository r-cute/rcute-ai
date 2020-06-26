import cv2
import numpy as np

class ObjectDetector:
    def __init__(self,*, confidence_threshold=.5, nms_threshold=.3, use_bgr=True,
        labels='../resources/coco.names',
        config='../resources/yolov3-coco.cfg',
        weights='../resources/yolov3-coco.weights'):

        self._use_bgr = use_bgr
        self._confidence_threshold = confidence_threshold
        self._nms_threshold = nms_threshold

        with open(labels) as label_file:
            self._labels = label_file.read().strip().split('\n')

        self._net = cv2.dnn.readNetFromDarknet(config, weights)
        self._net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        # self._net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)

        self._layer_names = self._net.getLayerNames()
        self._layer_names = [self._layer_names[i[0] - 1] for i in self._net.getUnconnectedOutLayers()]

    def detect(self, img):
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
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        ret_boxes = []
        ret_confidences = []
        ret_labels = []
        nms_boxes = cv2.dnn.NMSBoxes(boxes, confidences, self._confidence_threshold, self._nms_threshold)
        if len(nms_boxes):
            for i in nms_boxes.flatten():
                x, y, w, h = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]
                ret_boxes.append((x, y, w, h))
                ret_labels.append(self._labels[class_ids[i]])
                ret_confidences.append(confidences[i])
        return ret_boxes, ret_labels, ret_confidences

    def draw(self, img, *, labels=None, boxes=None, confidences=None, color=(0,0,180)):
        if not self._use_bgr:
            r, g, b = color
            color = b, g, r
        if boxes is not None:
            for i, (x, y, w, h) in enumerate(boxes):
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 1)
                text = ((labels[i]+": ") if labels is not None else '') + ("{:.2f}".format(confidences[i]) if confidences is not None else '')
                if text:
                    cv2.rectangle(img, (x, y), (x+len(text)*9, y+20), color, cv2.FILLED)
                    cv2.putText(img, text, (x, y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)





