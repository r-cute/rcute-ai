import cv2

class QRCodeDetector(cv2.QRCodeDetector):
    def __init__(self, use_gbr=True):
        self._use_gbr = use_gbr
        cv2.QRCodeDetector.__init__(self)

    def detect(self, img):
        text, points = self.detectAndDecode(img)[:2]
        return text, (points if points is None else points.reshape(-1, 2).astype(int))

    def draw(self, img, text, points, color=(0,0,180)):
        if points is not None:
            if not self._use_gbr:
                r, g, b = color
                color = b, g, r
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, text, tuple(points[0]), font, 0.5, color, 1)
            cv2.polylines(img, [points.reshape(-1, 1, 2)], 1, color)