#include <ArduinoBLE.h>
#include <ReefwingAHRS.h>
#include <Arduino_BMI270_BMM150.h>

int loopFrequency = 0;
unsigned long previousMillis = 0;

float gx, gy, gz;

// FLEX SENSORS
const int pinPouce = A5;
const int pinIndex = A7;
const int pinMajeur = A6;

int valeurPouce = 0;
int valeurIndex = 0;
int valeurMajeur = 0;

BLEService testService("12345678-1234-1234-1234-1234567890ab");

BLEStringCharacteristic testChar(
  "abcdefab-1234-1234-1234-abcdefabcdef",
  BLERead | BLENotify,
  150 // NOMBRE MAX DE BYTES "ENVOYABLES" !!!important
);

BLEStringCharacteristic cmdChar(
  "beb5483e-36e1-4688-b7f5-ea07361b26a8",
  BLERead | BLEWrite | BLENotify,
  150 // NOMBRE MAX DE BYTES "ENVOYABLES" !!!important
);

void setup() {
  Serial.begin(115200);
  delay(1500);

  if (!BLE.begin()) {
    Serial.println("[*] BLE impossible à démarrer");
    while (1);
  }

  BLE.setLocalName("NanoBLE_Math");
  BLE.setAdvertisedService(testService);

  testService.addCharacteristic(testChar);
  testService.addCharacteristic(cmdChar);
  BLE.addService(testService);

  testChar.writeValue("[*] Début");

  BLE.advertise();

  Serial.println("[*] Arduino prête, BLE actif");
  Serial.println("[*] Nom Bluetooth : NanoBLE_Math");

  Serial.print("[*] Detected Board - ");

  if (IMU.begin()) {
    Serial.println("[*] BMI270 & BMM150 IMUs Connected."); 
  } 
  else {
    Serial.println("[*] BMI270 & BMM150 IMUs Not Detected.");
    while(1);
  }

}

void loop() {
  BLEDevice central = BLE.central();
  
  if (central) {
    while (central.connected()) {
      BLE.poll();
      bool actif = false;
      if (cmdChar.written()){
        String cmd = cmdChar.value();
        cmd.trim();

        if (cmd == "HORS_CHAMP"){
          actif = true;
        }
      }
      int lecturePouce = analogRead(pinPouce);
      int lectureIndex = analogRead(pinIndex);
      int lectureMajeur = analogRead(pinMajeur);

      valeurPouce = (valeurPouce + lecturePouce)/2; // pseudo moyenne
      valeurIndex = (valeurIndex + lectureIndex)/2;
      valeurMajeur = (valeurMajeur + lectureMajeur)/2; 

      if (actif && (millis() - previousMillis >= 100)) { 
        previousMillis = millis();
        if (IMU.gyroscopeAvailable()) { 
          IMU.readGyroscope(gx, gy, gz);
          char buffer[120];

          sprintf(buffer, "{\"gyro\":[%.2f,%.2f,%.2f], \"flex\":[%d,%d,%d]}", gx, gy, gz, valeurPouce, valeurIndex, valeurMajeur); // plus stable que concat de str

          testChar.writeValue(buffer);
          Serial.println(buffer);
          delay(2);
        }

      }
    }
  }
}
