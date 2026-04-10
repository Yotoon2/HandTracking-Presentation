"""
FICHIER decoupe_video.py

Ce script python permet de transformer une vidéo en images (frames).
A été utilisé pour train le gesture recognizer.
"""

import cv2
import os

VIDEO_PATH = "gesture.mp4"
OUTPUT_DIR = "dataset"

os.makedirs(OUTPUT_DIR, exist_ok=True)

cap = cv2.VideoCapture(VIDEO_PATH)
count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if count % 3 == 0:  # 1 frame sur 3
        cv2.imwrite(f"{OUTPUT_DIR}/img_{count}.jpg", frame)
    count += 1

cap.release()