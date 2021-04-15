import cv2
import mediapipe as mp
import time


class PoseDetector():

    def __init__(self, mode=False, up_body_only=False, smooth=True,
                 detect_conf=0.5, track_conf=0.5):
        self.mode = mode
        self.up_body_only = up_body_only
        self.smooth = smooth
        self.detect_conf = detect_conf
        self.track_conf = track_conf

        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(self.mode, self.up_body_only, self.smooth,
                                      self.detect_conf,  self.track_conf)
        self.mp_draw = mp.solutions.drawing_utils


    def find_pose(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)

        if self.results.pose_landmarks:
            if draw:
                self.mp_draw.draw_landmarks(img, self.results.pose_landmarks,
                                            self.mp_pose.POSE_CONNECTIONS)

        return img


    def find_position(self, img, draw=True):
        landmark_list = []

        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmark_list.append([id, cx, cy])

                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        return landmark_list



def main():
    cap = cv2.VideoCapture("videos/4.mp4")
    # cap = cv2.VideoCapture(0)

    previous_time = 0
    detector = PoseDetector()
    while True:
        success, img = cap.read()
        img = detector.find_pose(img)
        landmark_list = detector.find_position(img, draw=False)
        # if len(landmark_list) != 0:
            # print(landmark_list)
            # cv2.circle(img, (landmark_list[0][1], landmark_list[0][2]), 5, (255, 0, 0), cv2.FILLED)

        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time
        cv2.putText(img, f'FPS: {int(fps)}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()