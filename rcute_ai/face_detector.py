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

class FaceDetector:
    def __init__(self, use_bgr=True):
        self._face_encodings = []
        self._face_names = []
        self._name_images = []
        self._use_bgr = use_bgr
        self._font = ImageFont.truetype("../resources/msyh.ttc", 15)
        self._unknown_name_image = self.create_name_image("陌生人")

    def create_name_image(self, name):
        img = Image.new('RGB', (15*len(name), 20), 'black')
        draw = ImageDraw.Draw(img)
        draw.text((0,0), name, font=self._font, textColor=(255,255,255))
        return np.asarray(img)[:,:,::-1]

    def memorize(self, name, file_or_img):
        if isinstance(file_or_img, str):
            file_or_img = face_recognition.load_image_file(file_or_img)
        elif self._use_bgr:
            file_or_img = file_or_img[:, :, ::-1]
        self._face_encodings.append(face_recognition.face_encodings(file_or_img)[0])
        self._face_names.append(name)
        self._name_images.append(self.create_name_image(name))

    def forget(self, name):
        i = self._face_names.index(name)
        del self._face_names[i]
        del self._face_encodings[i]
        del self._name_images[i]

    def detect(self, img):
        self._current_image, self._resize_factor = resize_320x240(img)
        if self._use_bgr:
            self._current_image = self._current_image[:, :, ::-1]
        self._face_locations = face_recognition.face_locations(self._current_image)
        self._detected_faces = self._recognized_faces = self._face_landmarks_list = None

    @property
    def detected_faces(self):
        if self._detected_faces is None:
            self._detected_faces = [(left, top, right, bottom) for top, right, bottom, left in self._face_locations]
            self._detected_faces = [(int(a*self._resize_factor) for a in p) for p in self._detected_faces]
        return self._detected_faces

    @property
    def recognized_faces(self):
        if self._recognized_faces is None:
            self._current_encodings = face_recognition.face_encodings(self._current_image, self._face_locations)
            self._recognized_faces = []
            for encoding in self._current_encodings:
                matches = face_recognition.compare_faces(self._face_encodings, encoding)
                face_distances = face_recognition.face_distance(self._face_encodings, encoding)
                if face_distances:
                    best_match_index = np.argmin(face_distances)
                    name = self._face_names[best_match_index] if matches[best_match_index] else None
                else:
                    name = None
                self._recognized_faces.append(name)
        return self._recognized_faces

    @property
    def detected_face_landmarks(self):
        if self._face_landmarks_list is None:
            self._face_landmarks_list = []
            for landmarks in face_recognition.face_landmarks(self._current_image):
                ret_landmarks = {}
                for facial_feature in landmarks.keys():
                    ret_landmarks[facial_feature] = [(x*self._resize_factor, y*self._resize_factor) for x, y in landmarks[facial_feature]]
                self._face_landmarks_list.append(ret_landmarks)
        return self._face_landmarks_list

    def draw(self, img, *, boxes=None, names=None, landmarks=None, color=(0,0,180)):
        if not self._use_bgr:
            r, g, b = color
            color = b, g, r
        h, w = img.shape[:2]
        if boxes and names:
            for (x, y, x1, y1), name in zip(boxes, names):
                cv2.rectangle(img, (x, y), (x1, y1), color, 1)
                try:
                    index = self._face_names.index(name)
                except ValueError:
                    name_image = self._unknown_name_image
                else:
                    name_image = self._name_images[index]
                nh, nw = name_image.shape[:2]
                sy, sy1, sx, sx1 = min(h, y), min(h, y+20), min(w, x), min(w, x+nw)
                cv2.rectangle(img, (x, sy), (sx1, sy1), color, cv2.FILLED)
                # font = cv2.FONT_HERSHEY_DUPLEX
                # cv2.putText(img, name if name else 'Unknown', (x+6, y1-6), font, 0.5, (255, 255, 255), 1)
                img[sy:sy1, sx:sx1] = cv2.bitwise_or(img[sy:sy1, sx:sx1], name_image)
        elif boxes:
            for x, y, x1, y1 in boxes:
                cv2.rectangle(img, (x, y), (x1, y1), color, 1)
        if landmarks:
            for lm in landmarks:
                cv2.polylines(img, [np.array(points, np.int32).reshape(-1,1,2) for points in lm.values()], 1, color)









