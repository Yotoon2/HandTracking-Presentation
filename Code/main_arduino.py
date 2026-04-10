import cv2 as cv # type: ignore
import serial # type: ignore
import socket
import time
import mediapipe as mp # type: ignore
from mediapipe.tasks.python import vision # type: ignore

from arduino.arduino import ArduinoBoard
from arduino.parser import Parser
from vision.mediapipe_handler import MediapipeHandler
from vision.drawing import draw_landmarks_on_image
from gestures.gesture_logic import detect_gesture

PORT = '/dev/ttyACM0'

arduino = ArduinoBoard(port=PORT)
parser = Parser()
serial_port = serial.Serial(port=PORT, timeout=0.1)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mediapipe_handler = MediapipeHandler(arduino=arduino, serial_port=serial_port, sock=sock)

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("IMPOSSIBLE D'OUVRIR LA CAMERA")
    exit()

while True:
    ret, frame = cap.read()
    timestamp_ms = int(time.time() * 1000)
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    )

    result, gesture_result = mediapipe_handler.process_frame(mp_image, timestamp_ms)

    if result is not None:
        annotated_image = draw_landmarks_on_image(mp_image.numpy_view(),
                                                      result)  # Pour main droite ou main gauche
        if gesture_result is not None:
            annotated_image = draw_landmarks_on_image(mp_image.numpy_view(), gesture_result)  # Pour le geste
        cv.imshow("Hands + Gesture",
                cv.cvtColor(annotated_image, cv.COLOR_RGB2BGR))  # Création fenêtre de la caméra

    line = arduino.read()
    if line:
        parser.update(line)
        #print("Flex :", parser.flex)
        geste = detect_gesture(parser.flex)
        print(geste)

    if cv.waitKey(1) & 0xFF == 27:  # Gestion touche Echap pour quitter
        break