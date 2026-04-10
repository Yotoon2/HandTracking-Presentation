import serial # type: ignore
import time
import json

class ArduinoBoard:
    def __init__(self, port, baud=115200):
        self.ser = serial.Serial(port, baud, timeout=0.1)

    def led_on(self):
        self.ser.write(b"LED_ON\n")

    def led_off(self):
        self.ser.write(b"LED_OFF\n")

    def hors_champs(self):
        self.ser.write(b"HORS_CHAMPS\n")

    def read(self):
        if self.ser.in_waiting:
            line = self.ser.readline().decode().strip()
            try:
                data = json.loads(line)
                return data
            except:
                return None
            
        return None