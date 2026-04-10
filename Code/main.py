# IMPORTS

import numpy as np
import cv2 as cv
import mediapipe as mp
import time
from mediapipe.tasks.python.vision import GestureRecognizer, GestureRecognizerOptions
from pynput import keyboard
from pynput.mouse import Button, Controller
import tkinter

# useless pour l'instant ?
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
root = tkinter.Tk()
root.withdraw()
longueur, largeur = root.winfo_screenwidth(), root.winfo_screenheight() #Récupère la résolution de l'écran
print(longueur, largeur)
m = Controller() #Pour controller la souris
PATH = "../Modèles/"
controller = keyboard.Controller() #Pour contrôller le clavier
mp_hands = mp.tasks.vision.HandLandmarksConnections
mp_drawing = mp.tasks.vision.drawing_utils
mp_drawing_styles = mp.tasks.vision.drawing_styles
run = True

# Constantes (pixels)
pointer = True
MARGIN = 10
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # Couleur du texte sens de la main à la caméra
GESTURE_TEXT_COLOR = (25, 25, 112)  # Nom du geste

NB_FRAME = 10 #Tout les combiens de tick les effets peuvent s'activer
frame_actuelle = NB_FRAME

def draw_landmarks_on_image(rgb_image, detection_result): #Dessine les points de la mains de part la détection par le modèle google
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

def get_thumb_direction(landmarks):
    """
    Fonction afin de savoir la direction du pouce lorsque qu'un geste "pouce à l'horizontal" est détecté.
    Le modèle hésite trop à faire lui-même la différence entre gauche/droite donc on se sert des landmarks (points sur les doigts)
    """

    thumb_x = landmarks[4].x
    index_x = landmarks[5].x

    if thumb_x > index_x:
        return "thumb_left"
    else:
        return "thumb_right"


def print_gesture_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    #Gère tout les gestes que l'on a définit au préalable
    global latest_result

    for idx, hand_gestures in enumerate(result.gestures): #Affiche dans la console les gestes détectés sur l'image
        if hand_gestures:
            top_gesture = hand_gestures[0]  # = le plus probable des gestes

            if top_gesture.category_name == "thumb":
                landmarks = latest_result.hand_landmarks[idx]

                top_gesture.category_name = get_thumb_direction(landmarks)
                
            print("Geste détecté :", top_gesture.category_name)
            
        else:
            
            print("Geste détecté : inconnu")
            
        global frame_actuelle

        #Permet de dessiner sur le tableau grace au geste pince
        if frame_actuelle == NB_FRAME and top_gesture.category_name == "pince":
            x = result.hand_landmarks[0][4].x*longueur #Calcul la futur position de la souris sur l'écran via les données du lanmark 4
            y = result.hand_landmarks[0][4].y*largeur  #Calcul la futur position de la souris sur l'écran via les données du lanmark 4
            m.press(Button.left)                       #Appuie sur le clic gauche pour commencer le mouvement du dessin
            m.position = (x, y)                        #Déplace la souris à la position calculée
            m.release(Button.left)                     #Relache le clic gauche

        #Fais le changement entre le mode dessin et le mode pointeur laser via le geste "tableau"
        elif frame_actuelle == NB_FRAME and top_gesture.category_name == "tableau":
            global pointer
            if pointer == True:
                #Execute le raccourcis clavier pour se mettre en mode dessin
                controller.press(keyboard.Key.cmd)
                controller.press('p')
                controller.release(keyboard.Key.cmd)
                controller.release('p')
                pointer = False
            else:
                #Execute le clavier pour se mettre en mode pointeur laser
                pointer = True
                controller.press(keyboard.Key.cmd)
                controller.press('l')
                controller.release(keyboard.Key.cmd)
                controller.release('l')
            frame_actuelle = 0

        #Passe à la diapositive précédente
        elif frame_actuelle == NB_FRAME and top_gesture.category_name == "thumb_left":
            controller.press(keyboard.Key.left)
            controller.release(keyboard.Key.left)
            frame_actuelle = 0

        #Passe à la diapo suivante
        elif frame_actuelle == NB_FRAME and top_gesture.category_name == "thumb_right":
            controller.press(keyboard.Key.right)
            controller.release(keyboard.Key.right)
            frame_actuelle = 0

        #Ferme le diapo et arrête le programme si on utilise notre majeur
        elif frame_actuelle == NB_FRAME and top_gesture.category_name == "majeur":
            controller.press(keyboard.Key.cmd)
            controller.press('q')
            controller.release(keyboard.Key.cmd)
            controller.release('q')
            frame_actuelle = 0
            global run
            run = False
        elif frame_actuelle != NB_FRAME:
            frame_actuelle += 1

    global latest_gesture_result
    latest_gesture_result = result


# FIN AFFICHAGES CONSOLE




options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=f"{PATH}hand_landmarker.task"),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=2,  # Nombre de mains max à détecter
    result_callback=print_result)

gesture_options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=f"{PATH}gesture_recognizer.task"),
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
    while run:
        ret, frame = cap.read()
        print("\n\n")
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
