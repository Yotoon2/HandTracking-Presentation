#include <ArduinoBLE.h>
#include <ReefwingAHRS.h>
#include <Arduino_BMI270_BMM150.h>

ReefwingAHRS ahrs;
SensorData data;

//  Display and Loop Frequency
int loopFrequency = 0;
const long displayPeriod = 1000;
unsigned long previousMillis = 0;


BLEService testService("12345678-1234-1234-1234-1234567890ab");

BLEStringCharacteristic testChar(
  "abcdefab-1234-1234-1234-abcdefabcdef",
  BLERead | BLENotify,
  50
);

int compteur = 0;

void setup() {
  Serial.begin(115200);
  delay(1500);

  if (!BLE.begin()) {
    Serial.println("BLE impossible à démarrer");
    while (1);
  }

  BLE.setLocalName("NanoBLE_Math");
  BLE.setAdvertisedService(testService);

  testService.addCharacteristic(testChar);
  BLE.addService(testService);

  testChar.writeValue("Début");

  BLE.advertise();

  Serial.println("Arduino prête, BLE actif");
  Serial.println("Nom Bluetooth : NanoBLE_Math");

  //  Initialise the AHRS
  //  Use default fusion algo and parameters
  ahrs.begin();
  
  ahrs.setFusionAlgorithm(SensorFusion::MADGWICK);
  ahrs.setDeclination(12.717);

  //  Start Serial and wait for connection

  Serial.print("Detected Board - ");
  Serial.println(ahrs.getBoardTypeString());

  if (IMU.begin() && ahrs.getBoardType() == BoardType::NANO33BLE_SENSE_R2) {
    Serial.println("BMI270 & BMM150 IMUs Connected."); 
  } 
  else {
    Serial.println("BMI270 & BMM150 IMUs Not Detected.");
    while(1);
  }

}

void loop() {
  BLEDevice central = BLE.central();
  

  if (central) {
    Serial.print("Connecté à : ");
    Serial.println(central.address());

    while (central.connected()) {
      BLE.poll();
      if (IMU.gyroscopeAvailable()) {  IMU.readGyroscope(data.gx, data.gy, data.gz);  }
      if (IMU.accelerationAvailable()) {  IMU.readAcceleration(data.ax, data.ay, data.az);  }
      if (IMU.magneticFieldAvailable()) {  IMU.readMagneticField(data.mx, data.my, data.mz);  }

      ahrs.setData(data);
      ahrs.update();
      String msg = "NO DATA";
      if (millis() - previousMillis >= displayPeriod) {
        //  Display sensor data every displayPeriod, non-blocking.
        //Serial.print(ahrs.angles.roll, 2);Serial.print(",");Serial.print(ahrs.angles.pitch, 2);Serial.print(",");Serial.print(ahrs.angles.yaw, 2);Serial.print(",");Serial.println(ahrs.angles.heading, 2);
        previousMillis = millis();
        msg = String(ahrs.angles.roll) + "," + String(ahrs.angles.pitch) + "," + String(ahrs.angles.yaw) + "," + String(ahrs.angles.heading);
      }
      testChar.writeValue(msg);

      Serial.println(msg);

      delay(1000);
    }

    Serial.println("Déconnecté");
  }
}

