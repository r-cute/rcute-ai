import face_recognition
import cv2
from PIL import Image, ImageFont, ImageDraw
import numpy as np
from . import util

def resize_320x240(img):
    h, w, c = img.shape
    fx, fy = 320/w, 240/h
    if fx <= fy <= 1:
        return cv2.resize(img, (0,0), fx=fx, fy=fx), 1/fx
    elif fy <= fx <=1:
        return cv2.resize(img, (0,0), fx=fy, fy=fy), 1/fy
    return img, 1

class FaceRecognizer:
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
        if isinstance(file_or_img, str):
            file_or_img = face_recognition.load_image_file(file_or_img)
        elif self._use_bgr:
            file_or_img = file_or_img[:, :, ::-1]
        self._face_encodings.append(face_recognition.face_encodings(file_or_img)[0])
        self._face_names.append(name)
        self._name_images.append(self._create_name_image(name))

    def forget(self, name):
        i = self._face_names.index(name)
        del self._face_names[i]
        del self._face_encodings[i]
        del self._name_images[i]

    def recognize(self, img):
        img, resize_factor = resize_320x240(img)
        if self._use_bgr:
            img = img[:, :, ::-1]
        locations = face_recognition.face_locations(img)
        ret_locations = [(left, top, right-left, bottom-top) for top, right, bottom, left in locations]
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
        if not self._use_bgr:
            r, g, b = color
            color = b, g, r
            r, g, b = text_color
            text_color = b, g, r
        H, W = img.shape[:2]
        if names:
            for (x, y, w, h), name in zip(locations, names):
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
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 1)









