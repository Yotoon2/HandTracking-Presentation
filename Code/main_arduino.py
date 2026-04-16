import cv2 as cv  # type: ignore
import serial  # type: ignore
import socket
import time
import mediapipe as mp  # type: ignore
from mediapipe.tasks.python import vision  # type: ignore
import asyncio

from arduino.parser import Parser
from vision.mediapipe_handler import MediapipeHandler
from vision.drawing import draw_landmarks_on_image
from gestures.gesture_logic import detect_pos_flex, detect_gesture, handle_pince, handle_swipe_droit, \
    handle_swipe_gauche
from bluetooth.bluetooth_handler import BluetoothHandler
from pynput import keyboard
from pynput.mouse import Button, Controller

parser = Parser()
mediapipe_handler = MediapipeHandler()
m = Controller()  # Pour controller la souris
controller = keyboard.Controller()  # Pour contrôller le clavier

NB_FRAME = 20  # Tout les combiens de tick les effets peuvent s'activer
frame_actuelle = NB_FRAME

# DEBUG
DEBUG = False
if DEBUG:
    PORT = '/dev/ttyACM0'  # pour debug en usb sur pc (hors bluetooth)
    arduino = ArduinoBoard(port=PORT)
    serial_port = serial.Serial(port=PORT, timeout=0.1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mediapipe_handler = MediapipeHandler(arduino=arduino, serial_port=serial_port, sock=sock)

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("IMPOSSIBLE D'OUVRIR LA CAMERA")
    exit()
    
TEST = True
async def main():
    bl = BluetoothHandler()
    bl.run()
    global frame_actuelle
    last_send = 0
    while True:
        now = time.time()
        await asyncio.sleep(0.001)  # obligatoire sinon ça bug jsp pourquoi

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

        if ((mediapipe_handler.hors_champ) and (now - last_send > 0.1)):
            await bl.send_command("HORS_CHAMP")
            last_send = now
            
            data = bl.get_data()
            if (data != None):
                parser.update(data)

                geste = detect_gesture(None, parser.gyro, None, detect_pos_flex(parser.flex))
                if frame_actuelle == NB_FRAME and geste == "swipe_gauche":
                    print("GAUCHE")
                    handle_swipe_gauche()
                    frame_actuelle = 0

                # Passe à la diapo suivante
                elif frame_actuelle == NB_FRAME and geste == "swipe_droit":
                    print("DROIT")
                    handle_swipe_droit()
                    frame_actuelle = 0

                elif frame_actuelle != NB_FRAME:
                    frame_actuelle += 1

        if DEBUG:
            line = arduino.read()
            if line:
                parser.update(line)
                geste = detect_pos_flex(parser.flex)
                print(geste)

        if cv.waitKey(1) & 0xFF == 27:  # Gestion touche Echap pour quitter
            break


asyncio.run(main())
