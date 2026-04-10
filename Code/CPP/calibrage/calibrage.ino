#include <Arduino_BMI270_BMM150.h>

float mx, my, mz;
float minX=9999, minY=9999, minZ=9999;
float maxX=-9999, maxY=-9999, maxZ=-9999;

void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("IMU fail");
    while (1);
  }

  Serial.println("=== MAG CALIBRATION ===");
  Serial.println("Bouge la carte dans TOUS les sens pendant 20s");
}

void loop() {

  if (IMU.magneticFieldAvailable()) {
    IMU.readMagneticField(mx, my, mz);

    minX = min(minX, mx);
    minY = min(minY, my);
    minZ = min(minZ, mz);

    maxX = max(maxX, mx);
    maxY = max(maxY, my);
    maxZ = max(maxZ, mz);
  }

  static unsigned long start = millis();
  if (millis() - start > 20000) {

    Serial.println("\n=== RESULTATS ===");

    Serial.print("Offset X: "); Serial.println((maxX+minX)/2);
    Serial.print("Offset Y: "); Serial.println((maxY+minY)/2);
    Serial.print("Offset Z: "); Serial.println((maxZ+minZ)/2);

    Serial.print("Scale X: "); Serial.println((maxX-minX)/2);
    Serial.print("Scale Y: "); Serial.println((maxY-minY)/2);
    Serial.print("Scale Z: "); Serial.println((maxZ-minZ)/2);

    while(1);
  }
}