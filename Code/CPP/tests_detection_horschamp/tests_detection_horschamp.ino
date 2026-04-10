#include <Arduino_BMI270_BMM150.h>

float angle_x = 0, angle_y = 0, angle_z = 0;
unsigned long previousTime;

int degreesX = 0;
int degreesY = 0;

int plusThreshold = 30;
int minusTreshold = -30;

float ax, ay, az;
float gx, gy, gz;
float mx, my, mz;

float ledvalue;

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);

  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("IMU FAILED");
    while (true);
  }
  Serial.println("IMU OK");


  unsigned long previousTime = millis();
}

void loop() {
  if (Serial.available()) { 
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "LED_ON") {
      digitalWrite(LED_BUILTIN, HIGH);
    } else if (cmd == "LED_OFF") {
      digitalWrite(LED_BUILTIN, LOW);
    } 

    if (cmd == "HORS_CHAMPS") {

      
      unsigned long currentTime = millis();
      float dt = (currentTime - previousTime) / 1000.0;
      previousTime = currentTime;

      if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(ax, ay, az);
        
        if ((ax < 0.1) && (ax > -0.1) && (ay < 0.1) && (ay > -0.1)){
          //Serial.println("STABLE");
        }

        if (ax > 0.1){
          ax = 100*ax;
          degreesX = map(ax, 0, 97, 0, 90);
          //Serial.print("Up");
          //Serial.print(degreesX);
          //Serial.println(" degrés");

        }

        if (ax < -0.1){
          ax = 100*ax;
          degreesX = map(ax, 0, -100, 0, 90);
          //Serial.print("Down");
          //Serial.print(degreesX);
          //Serial.println(" degrés");

        }

        if (ay > 0.1){
          ay = 100*ay;
          degreesY = map(ay, 0, 97, 0, 90);
          //Serial.print("Left");
          //Serial.print(degreesY);
          //Serial.println(" degrés");

        }

        if (ay < -0.1){
          ay = 100*ay;
          degreesY = map(ay, 0, -100, 0, 90);
          //Serial.print("Right");
          //Serial.print(degreesY);
          //Serial.println(" degrés");

        }
      } 

      if (IMU.gyroscopeAvailable()){
        IMU.readGyroscope(gx, gy, gz);

        if (gy > plusThreshold){
          Serial.println("GYRO Front");
         
        }

        if (gy < minusTreshold){
          Serial.println("GYRO Back");
        }

        if (gx < minusTreshold){
          Serial.println("GYRO Right");
        }

        if (gx > plusThreshold){
          Serial.println("GYRO Left");
        }
      }
      
      IMU.readMagneticField(mx, my, mz);
      if (mx<0){
        ledvalue = -(mx);
      }
      else {
        ledvalue = mx;
      }

      analogWrite(LED_BUILTIN, ledvalue);

      delay(10);
    }
  }
}
