import cv2, math
from . import util
import mediapipe
mp_drawing = mediapipe.solutions.drawing_utils
mp_hands = mediapipe.solutions.hands

HandLandmark = mp_hands.HandLandmark

class HandDetector(mp_hands.Hands):
    def __init__(self):#, *args, **kw):
        """ only detect on hand"""
        # if kw.get('max_num_hands') == None and len(args) < 2:
        #     kw['max_num_hands'] = 1
        super().__init__(max_num_hands=1)#(*args, **kw)

    def __del__(self):
        self.close()

    def detect(self, img, *, annotate=False):
        """detect hand landmarks (only one hand) and recognizable guesture"""
        # convert the BGR image to RGB.
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        rgb.flags.writeable = False
        hands = self.process(rgb)
        if hands.multi_hand_landmarks:
            marks = hands.multi_hand_landmarks[0]
            h, w = img.shape[:2]
            pt = util.norm_to_pixel(w, h, marks.landmark)
            guesture = self.guesture(pt)
            annotate and self.annotate(img, pt, guesture)
            return pt, guesture
        return None, None



    def annotate(self, img, keypoints, guesture=None):
        """Draw the hand annotations on the image."""
        # img.flags.writeable = True # must
        # if normalized:
        #     mp_drawing.draw_landmarks(img, keypoints, mp_hands.HAND_CONNECTIONS)
        # else:
        util.draw_landmarks(img, keypoints, mp_hands.HAND_CONNECTIONS)
        guesture and cv2.putText(img, guesture, (30,30), cv2.FONT_HERSHEY_SIMPLEX, .8, (0,0,255), 1, cv2.LINE_AA)

    _joints = [[6,8],[10,12],[14,16],[18,20]]
    def guesture(self, pt): # only recognize one hand
        """recognize guesture based on key points

        :param pt: one hand key points
        :type pt: list
        :return: guesture name
        :rtype: str
        """
        pt0 = pt[0]
        finger_stretched = [math.dist(pt[17], pt[4])> math.dist(pt[17], pt[2])] # if thumb is stretched
        for j1, j2 in HandDetector._joints: # for the other 4 fingers
            finger_stretched.append(math.dist(pt[j1], pt0) < math.dist(pt[j2], pt0))
        if not finger_stretched[0] and finger_stretched[2:]== [False, False, False]:
            a, b, c=math.dist(pt[8], pt[10]), math.dist(pt[12], pt[8]), math.dist(pt[10], pt[6])
            if a> c and finger_stretched[1]:
                return '1'
            return 'fist' if a> b else '9'
        if finger_stretched == [True, False, False, False, False]:
            return 'thumbs-up' if pt[4][1]< pt0[1] else 'thumbs-down'
        if finger_stretched == [False, False, True, False, False]:
            return 'middle finger'
        if finger_stretched == [False, False, False, False, True]:
            return 'little finger'
        if finger_stretched == [False, True, True, False, False]:
            return '2'
        if finger_stretched == [False, True, True, True, False]:
            return '3'
        if finger_stretched == [True, True, True, False, False]:
            return 'german 3'
        if finger_stretched == [False, True, True, True, True]:
            return '4'
        if finger_stretched == [True, True, True, True, True]:
            return '5' if math.dist(pt[12], pt[8])*2 > math.dist(pt[12], pt[16]) else 'long live and prosper'
        if finger_stretched == [True, False, False, False, True]:
            return '666'
        if finger_stretched == [True, True, False, False, True]:
            return 'love'
        if finger_stretched == [False, True, False, False, True]:
            return 'rock'
        pinch = self.thumb_and_index_finger_pinch(pt)
        if finger_stretched[2:] == [True, True, True] and pinch:
            return 'ok'
        if finger_stretched[2:] == [False, False, False]:
            return 'heart' if pinch else 'gun'

    def thumb_and_index_finger_pinch(self, pt):
        return math.dist(pt[4], pt[8])< math.dist(pt[2], pt[5])
