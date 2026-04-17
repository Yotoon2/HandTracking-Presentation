import time
import mediapipe as mp # type: ignore
from mediapipe.tasks.python.vision import GestureRecognizer, GestureRecognizerOptions # type: ignore
from pynput import keyboard # type: ignore
from gestures.gesture_logic_demo import get_thumb_direction
import tkinter
root = tkinter.Tk()
root.withdraw()
longueur, largeur = root.winfo_screenwidth(), root.winfo_screenheight()

class MediapipeHandler:
    def __init__(self, arduino=None, serial_port=None, sock=None):
        self.latest_result = None
        self.latest_gesture_result = None
        self.last_imu_request = 0
        self.IMU_INTERVAL = 0.2
        self.last_led_state = None
        self.arduino = arduino
        self.serial_port = serial_port
        self.sock = sock
        self.NB_FRAME = 20
        self.frame_actuelle = self.NB_FRAME
        self.PATH = "../Modeles/"
        self.pointer = True
        self.hors_champ = False

        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=self.PATH + "hand_landmarker.task"),
            running_mode=VisionRunningMode.LIVE_STREAM,
            num_hands=2,  # Nombre de mains max à détecter
            result_callback=self.print_result)

        self.landmarker = HandLandmarker.create_from_options(options)

        gesture_options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=self.PATH + "gesture_recognizer.task"),
            running_mode=VisionRunningMode.LIVE_STREAM,
            num_hands=2,
            result_callback=self.print_gesture_result)

        self.gesture_recognizer = GestureRecognizer.create_from_options(gesture_options)

    def print_result(self, result, output_image: mp.Image, timestamp_ms: int):
        #print("Hand landmarker result : {}".format(result))
        self.latest_result = result

    def print_gesture_result(self, result, output_image: mp.Image, timestamp_ms: int):
        #Gère tout les gestes que l'on a définit au préalable
        if result.gestures == []: # MAIN HORS CHAMP
            self.hors_champ = True
        else:
            self.hors_champ = False

        for idx, hand_gestures in enumerate(result.gestures): #Affiche dans la console les gestes détectés sur l'image
            if hand_gestures:
                top_gesture = hand_gestures[0]  # = le plus probable des gestes

                if top_gesture.category_name == "thumb":
                    landmarks = self.latest_result.hand_landmarks[idx]

                    top_gesture.category_name = get_thumb_direction(landmarks)
                    
                #print("Geste détecté :", top_gesture.category_name)
                
            else:
                pass

        self.latest_gesture_result = result

    
    def process_frame(self, mp_image, timestamp_ms):
        self.landmarker.detect_async(mp_image, timestamp_ms=timestamp_ms)
        self.gesture_recognizer.recognize_async(mp_image, timestamp_ms=timestamp_ms)
        return self.latest_result, self.latest_gesture_result