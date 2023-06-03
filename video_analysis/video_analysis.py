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
from mutils import convert, offset, Preprocessor

MODEL_NAME = "Score"
FPS = 10
TIMESTAMPS = 16

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

clock = pygame.time.Clock()

MODEL = tf.keras.models.load_model(os.path.join("model", MODEL_NAME))
input_buffer = []

cap = cv2.VideoCapture(0)

preprocessor = Preprocessor()

def process(pose_model, image):
    results = pose_model.process(image)
    if results.pose_landmarks is not None:
        converted_landmarks = convert(results.pose_world_landmarks.landmark)
        if previous_landmarks is None:
            previous_landmarks = converted_landmarks
        else:
            offset_landmarks = offset(converted_landmarks, previous_landmarks)
            previous_landmarks = converted_landmarks
            input_buffer.append(offset_landmarks)
            if len(input_buffer) >= TIMESTAMPS:
                inputs = np.array([preprocessor.transform(np.array(input_buffer))])
                outputs = MODEL.predict(inputs, verbose=0)
                print(outputs)
                # print([LABELS[next(filter(lambda x: x[1]==max(output), enumerate(output)))[0]] for output in outputs])
                input_buffer.clear()
        landmark = results.pose_landmarks.landmark
        # Draw the pose annotation on the image.