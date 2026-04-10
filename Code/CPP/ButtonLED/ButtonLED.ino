#include <ArduinoBLE.h>

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
}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connecté à : ");
    Serial.println(central.address());

    while (central.connected()) {
      String msg = "Valeur:" + String(compteur);
      testChar.writeValue(msg);

      Serial.println(msg);
      compteur++;

      delay(1000);
    }

    Serial.println("Déconnecté");
  }
}