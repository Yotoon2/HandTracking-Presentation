import time
import mediapipe as mp # type: ignore
from mediapipe.tasks.python.vision import GestureRecognizer, GestureRecognizerOptions # type: ignore
from pynput import keyboard # type: ignore

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
        self.NB_FRAME = 10
        self.frame_actuelle = self.NB_FRAME
        self.PATH = "../Modèles/"

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
        """if result.gestures == []: # QUAND LA MAIN EST HORS-CHAMP -> capteurs prennent le relai
            if self.last_led_state != "ON":
                self.arduino.led_on()
                self.last_led_state = "ON"


            now = time.time()
            if now - self.last_imu_request > self.IMU_INTERVAL:
                self.arduino.hors_champs()
                self.last_imu_request = now

            if self.serial_port.in_waiting:
                line = self.serial_port.readline().decode(errors="ignore").strip()
                print(line)

                if "," in line:
                    self.sock.sendto(line.encode(), ("127.0.0.1", 5005))

        else:
            if self.last_led_state != "OFF":
                self.arduino.led_off()
                self.last_led_state = 'OFF'"""

        for hand_gestures in result.gestures:
            
            if hand_gestures:
                top_gesture = hand_gestures[0]  # = le plus probable des gestes
                #print("Geste détecté :", top_gesture.category_name)
                
            else:
                continue
                #print("Geste détecté : inconnu")

            if self.frame_actuelle == self.NB_FRAME and top_gesture.category_name == "Thumb_Up":
                controller = keyboard.Controller()
                controller.press(keyboard.Key.right)
                controller.release(keyboard.Key.right)
                self.frame_actuelle = 0
            elif self.frame_actuelle != self.NB_FRAME:
                self.frame_actuelle += 1
                
        self.latest_gesture_result = result

    
    def process_frame(self, mp_image, timestamp_ms):
        self.landmarker.detect_async(mp_image, timestamp_ms=timestamp_ms)
        self.gesture_recognizer.recognize_async(mp_image, timestamp_ms=timestamp_ms)
        return self.latest_result, self.latest_gesture_result