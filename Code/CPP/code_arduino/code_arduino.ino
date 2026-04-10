#include <Arduino_BMI270_BMM150.h>
#include <ReefwingAHRS.h>

ReefwingAHRS ahrs;
SensorData data;

int loopFrequency = 0;
const long displayPeriod = 1000;
unsigned long previousMillis = 0;

float ledvalue;

// SENSORS
const int pinPouce = A0;
const int pinIndex = A1;
const int pinMajeur = A2;

int valeurPouce = 0;
int valeurIndex = 0;
int valeurMajeur = 0;

int positionPouce = 0;
int positionIndex = 0;
int positionMajeur = 0;

// CALIBRATIONS
const int seuilBas = 100;  
const int seuilHaut = 230;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);

  //  Initialise the AHRS
  //  Use default fusion algo and parameters
  ahrs.begin();
  
  ahrs.setFusionAlgorithm(SensorFusion::MADGWICK);
  ahrs.setDeclination(2.433);                      //  Declination of Montpellier

  //  Start Serial and wait for connection
  Serial.begin(115200);
  while (!Serial);

  Serial.print("Detected Board - ");
  Serial.println(ahrs.getBoardTypeString());

  if (IMU.begin() && ahrs.getBoardType() == BoardType::NANO33BLE_SENSE_R2) {
    Serial.println("BMI270 & BMM150 IMUs Connected."); 
    Serial.print("Gyroscope sample rate = ");
    Serial.print(IMU.gyroscopeSampleRate());
    Serial.println(" Hz");
    Serial.println();
    Serial.println("Gyroscope in degrees/second");
    Serial.print("Accelerometer sample rate = ");
    Serial.print(IMU.accelerationSampleRate());
    Serial.println(" Hz");
    Serial.println();
    Serial.println("Acceleration in G's");
    Serial.print("Magnetic field sample rate = ");
    Serial.print(IMU.magneticFieldSampleRate());
    Serial.println(" Hz");
    Serial.println();
    Serial.println("Magnetic Field in uT");
  } 
  else {
    Serial.println("BMI270 & BMM150 IMUs Not Detected.");
    while(1);
  }
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
      
      //SENSORS

      int lecturePouce = analogRead(pinPouce);
      int lectureIndex = analogRead(pinIndex);
      int lectureMajeur = analogRead(pinMajeur);

      valeurPouce = (valeurPouce + lecturePouce) / 2;
      valeurIndex = (valeurIndex + lectureIndex) / 2;
      valeurMajeur = (valeurMajeur + lectureMajeur) / 2;

      Serial.print("{\"flex\":["); Serial.print(valeurPouce); Serial.print(","); Serial.print(valeurIndex); Serial.print(","); Serial.print(valeurMajeur); Serial.println("]}");


      //IMU

      if (IMU.gyroscopeAvailable()) {  IMU.readGyroscope(data.gx, data.gy, data.gz);  }
      if (IMU.accelerationAvailable()) {  IMU.readAcceleration(data.ax, data.ay, data.az);  }
      if (IMU.magneticFieldAvailable()) {  IMU.readMagneticField(data.mx, data.my, data.mz);  }

      if (millis() - previousMillis >= displayPeriod) {
        //  Display sensor data every displayPeriod, non-blocking.
        /*Serial.print("--> Roll: ");
        Serial.print(ahrs.angles.roll, 2);
        Serial.print("\tPitch: ");
        Serial.print(ahrs.angles.pitch, 2);
        Serial.print("\tYaw: ");
        Serial.print(ahrs.angles.yaw, 2);
        Serial.print("\tHeading: ");
        Serial.print(ahrs.angles.heading, 2);
        Serial.print("\tLoop Frequency: ");
        Serial.print(loopFrequency);
        Serial.println(" Hz");*/

        Serial.print("{\"acc\":["); Serial.print(data.ax); Serial.print(", "); Serial.print(data.ay); Serial.print(", "); Serial.print(data.az); Serial.print(", "); Serial.println("]}");
        Serial.print("{\"gyro\":["); Serial.print(data.gx); Serial.print(", "); Serial.print(data.gy); Serial.print(", "); Serial.print(data.gz); Serial.print(", "); Serial.println("]}");
        Serial.print("{\"magneto\":["); Serial.print(data.mx); Serial.print(", "); Serial.print(data.my); Serial.print(", "); Serial.print(data.mz); Serial.print(", "); Serial.println("]}");
        Serial.print("{\"roll\":"); Serial.print(ahrs.angles.roll); Serial.println("]}");
        Serial.print("{\"pitch\":"); Serial.print(ahrs.angles.pitch); Serial.println("]}");
        Serial.print("{\"yaw\":"); Serial.print(ahrs.angles.yaw); Serial.println("]}");
        Serial.print("{\"heading\":"); Serial.print(ahrs.angles.heading); Serial.println("]}");
        

        loopFrequency = 0;
        previousMillis = millis();
      }

      loopFrequency++;

    }
  }
}


