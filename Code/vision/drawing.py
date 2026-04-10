# IMPORTS

import mediapipe as mp
import numpy as np
import cv2 as cv

mp_hands = mp.tasks.vision.HandLandmarksConnections
mp_drawing = mp.tasks.vision.drawing_utils
mp_drawing_styles = mp.tasks.vision.drawing_styles

# Constantes (pixels)

MARGIN = 10
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # Couleur du texte sens de la main à la caméra
GESTURE_TEXT_COLOR = (25, 25, 112)  # Nom du geste

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