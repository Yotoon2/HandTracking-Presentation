# IMPORTS

import numpy as np
import cv2 as cv
import mediapipe as mp
import time
from mediapipe.tasks.python.vision import GestureRecognizer, GestureRecognizerOptions
from pynput import keyboard
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# CLASS ARDUINO
import serial

from Code.arduino.arduino import ArduinoBoard
arduino = ArduinoBoard(port='/dev/ttyACM0')
serial_port = serial.Serial(port='/dev/ttyACM0', timeout=0.1)

# useless pour l'instant ?

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

controller = keyboard.Controller()
mp_hands = mp.tasks.vision.HandLandmarksConnections
mp_drawing = mp.tasks.vision.drawing_utils
mp_drawing_styles = mp.tasks.vision.drawing_styles

# Constantes (pixels)

MARGIN = 10
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # Couleur du texte sens de la main à la caméra
GESTURE_TEXT_COLOR = (25, 25, 112)  # Nom du geste

NB_FRAME = 10
global frame_actuelle
frame_actuelle = NB_FRAME


def draw_landmarks_on_image(rgb_image, detection_result):
    """Fonction Google"""
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(rgb_image)

    # Loop through the detected hands to visualize.
    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]
        handedness = handedness_list[idx]

        # Draw the hand landmarks.
        mp_drawing.draw_landmarks(
            annotated_image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style()
        )

        # Get the top left corner of the detected hand's bounding bow.
        height, width, _ = annotated_image.shape
        x_coordinates = [landmark.x for landmark in hand_landmarks]
        y_coordinates = [landmark.y for landmark in hand_landmarks]
        text_x = int(min(x_coordinates) * width)
        text_y = int(min(y_coordinates) * height) - MARGIN

        # Draw handedness (left or right hand) on the image.
        cv.putText(annotated_image, f"{handedness[0].category_name}",
                   (text_x, text_y), cv.FONT_HERSHEY_DUPLEX,
                   FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv.LINE_AA)

        # A nous

        gesture_name = None
        if hasattr(detection_result, "gestures"):
            hand_gestures = detection_result.gestures[idx]
            if hand_gestures:
                gesture_name = hand_gestures[0].category_name  # [0] car le geste le plus probable est au début

        if gesture_name:
            cv.putText(annotated_image, f"Gesture : {gesture_name}",
                       (text_x, text_y - 20), cv.FONT_HERSHEY_DUPLEX,
                       FONT_SIZE, GESTURE_TEXT_COLOR, FONT_THICKNESS, cv.LINE_AA)

    return annotated_image

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode
latest_result = None
latest_gesture_result = None


# AFFICHAGES CONSOLE

def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    #print("Hand landmarker result : {}".format(result))
    global latest_result
    latest_result = result

last_imu_request = 0
IMU_INTERVAL = 0.2  # secondes
last_led_state = None

def print_gesture_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):

    global last_imu_request, last_led_state

    if result.gestures == []: # QUAND LA MAIN EST HORS-CHAMP -> capteurs prennent le relai
        if last_led_state != "ON":
            arduino.led_on()
            last_led_state = "ON"


        now = time.time()
        if now - last_imu_request > IMU_INTERVAL:
            arduino.hors_champs()
            last_imu_request = now

        if serial_port.in_waiting:
            line = serial_port.readline().decode(errors="ignore").strip()
            print(line)

            if "," in line:
                sock.sendto(line.encode(), ("127.0.0.1", 5005))

    else:
        if last_led_state != "OFF":
            arduino.led_off()
            last_led_state = "OFF"

    for hand_gestures in result.gestures:
        
        if hand_gestures:
            top_gesture = hand_gestures[0]  # = le plus probable des gestes
            #print("Geste détecté :", top_gesture.category_name)
            
        else:
            pass
            #print("Geste détecté : inconnu")
            
        global frame_actuelle

        if frame_actuelle == NB_FRAME and top_gesture.category_name == "Thumb_Up":
            controller.press(keyboard.Key.right)
            controller.release(keyboard.Key.right)
            frame_actuelle = 0
        elif frame_actuelle != NB_FRAME:
            frame_actuelle += 1
            
    global latest_gesture_result
    latest_gesture_result = result


# FIN AFFICHAGES CONSOLE

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="./hand_landmarker.task"),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=2,  # Nombre de mains max à détecter
    result_callback=print_result)

gesture_options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path="./gesture_recognizer.task"),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=2,
    result_callback=print_gesture_result)

gesture_recognizer = GestureRecognizer.create_from_options(gesture_options)

# CAMERA ?

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("IMPOSSIBLE D'OUVRIR LA CAMERA")
    exit()

# FIN CAMERA

with HandLandmarker.create_from_options(options) as landmarker:
    frame_actuelle = 0
    while True:
        ret, frame = cap.read()
        #print("\n\n")
        timestamp_ms = int(time.time() * 1000)
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        )

        landmarker.detect_async(mp_image, timestamp_ms=timestamp_ms)
        gesture_recognizer.recognize_async(mp_image, timestamp_ms=timestamp_ms)

        if latest_result is not None:
            annotated_image = draw_landmarks_on_image(mp_image.numpy_view(),
                                                      latest_result)  # Pour main droite ou main gauche
            if latest_gesture_result is not None:
                annotated_image = draw_landmarks_on_image(mp_image.numpy_view(), latest_gesture_result)  # Pour le geste
            cv.imshow("Hands + Gesture",
                      cv.cvtColor(annotated_image, cv.COLOR_RGB2BGR))  # Création fenêtre de la caméra


        if cv.waitKey(1) & 0xFF == 27:  # Gestion touche Echap pour quitter
            break