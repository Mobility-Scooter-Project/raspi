import os
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import pygame
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
from mutils import convert

MODEL_NAME = "Score"
FPS = 10
TIMESTAMPS = 16

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

    def set(self, image):
        self.image = image
        return self

    def show(self):
        cv2.imshow("Motion Analysis", cv2.flip(self.image, 1))
        cv2.waitKey(1)
    
    # takes POSE.process(...).pose_landmarks
    def draw_landmark(self, landmarks):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        self.mp_drawing.draw_landmarks(
            image,
            landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style(),
        )
        return self

    # custom curve on the image
    def draw_curve(self):
        pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(self.image,[pts],False,(0,255,255))
        return self


def main():
    model = tf.keras.models.load_model(os.path.join("model", MODEL_NAME))
    def process_poses(poses):
        outputs = model.predict(np.array([poses]), verbose=0)
        print(outputs)

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

    display = ImageDisplay()
    clock = pygame.time.Clock()
    cap = cv2.VideoCapture(0)
    try:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            pose_landmarks = process_image(image)
            display.set(image).draw_landmark(pose_landmarks).draw_curve().show()
            delta_time = clock.tick(FPS)
    except:
        pass
        
    cap.release()
    pose.close()
