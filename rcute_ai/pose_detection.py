import cv2
import mediapipe
mp_drawing = mediapipe.solutions.drawing_utils
mp_pose = mediapipe.solutions.pose

PoseLandmark = mp_pose.PoseLandmark

class PoseDetector(mp_pose.Pose):

    def __del__(self):
        self.close()

    def detect(self, img, *, annotate=False):
        """detect body landmarks and recognizable pose

        :param annotate: whether or not to annotate detected results on image
        :type annotate: bool

        """
        # convert the BGR image to RGB.
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        rgb.flags.writeable = False
        skeleton = self.process(rgb)
        pose = self.pose(skeleton)
        annotate and self.annotate(img, skeleton, pose)
        return skeleton, pose

    def annotate(self, img, skeleton, pose=None):
        """Draw the hand annotations on the image."""
        img.flags.writeable = True
        mp_drawing.draw_landmarks(img, skeleton.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        pose and cv2.putText(img, pose, (30,30), cv2.FONT_HERSHEY_SIMPLEX, .8, (0,0,255), 1, cv2.LINE_AA)

    def pose(self, skeleton):
        raise NotImplementedError
