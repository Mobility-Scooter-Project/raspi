import os
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import pygame
import collections
# import sys
# sys.path.append(
#     os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
# )
from mutils import convert

MODEL_NAME = "trained_with_20_files"
FPS = 10
TIMESTAMPS = 16
WINDOW_NAME = "Motion Analysis"

'''
* store fixed number of items 
* trigger callback with the max capacity
* clear them after callback
'''
class ItemBuffer:
    def __init__(self, limit, callback):
        self.buffer = []
        self.limit = limit
        self.callback = callback
    
    def add(self, item):
        self.buffer.append(item)
        if self.limit == len(self.buffer):
            self.callback(self.buffer)
            self.buffer.clear()

'''
display image with extra drawing functions
'''
class ImageDisplay:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_pose = mp.solutions.pose
        self.image = None
        self.points = collections.deque(10*[0], 10)

    def set(self, image):
        self.image = image
        return self

    def show(self):
        cv2.imshow(WINDOW_NAME, self.draw_info_text(cv2.flip(self.image, 1)))
        cv2.waitKey(1)
    
    # takes POSE.process(...).pose_landmarks
    def draw_landmark(self, landmarks):
        self.mp_drawing.draw_landmarks(
            self.image,
            landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style(),
        )
        return self

    # custom curve on the image
    def draw_curve(self):
        pts = np.array([(i*30+100, v*1000) for i, v in enumerate(reversed(self.points)) if v>0], np.int32)
        cv2.polylines(self.image,[pts],False,(0,255,255),2, cv2.LINE_AA)
        return self

    def add_point(self, value):
        self.points.append(value)

    def draw_info_text(self, image):
        w = len(image[0])
        image = cv2.putText(image, 'Stable', (w-100,32), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        return cv2.putText(image, 'Unstable', (w-100,64), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)

def main():
    display = ImageDisplay()
    cap = cv2.VideoCapture(0)

    model = tf.keras.models.load_model(os.path.join("model", MODEL_NAME, "model.h5"))
    def process_poses(poses):
        # outputs = model.predict(np.array([poses]), verbose=0)
        mae_loss = model.evaluate(np.array([poses]), np.array([poses]),verbose=0)[0]
        display.add_point(mae_loss)

    pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    buffer = ItemBuffer(TIMESTAMPS, process_poses)
    def process_image(image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        if results.pose_landmarks is not None:
            converted_landmarks = convert(results.pose_world_landmarks.landmark)
            buffer.add(converted_landmarks)
        return results.pose_landmarks

    try:
        clock = pygame.time.Clock()
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            pose_landmarks = process_image(image)
            display.set(image).draw_landmark(pose_landmarks).draw_curve().show()
            delta_time = clock.tick(FPS)
            if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
                break
    except Exception as e:
        print(e)

    cap.release()
    pose.close()


if __name__=='__main__':
    main()