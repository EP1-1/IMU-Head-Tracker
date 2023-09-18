#include <Arduino_LSM9DS1.h>
#include <MadgwickAHRS.h>

Madgwick filter;
unsigned long frequency, microsPrevious;
int samplerate = 200;

void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!IMU.begin()){
    Serial.println("Failed to initialize IMU!");
  }
  // start the IMU and filter
  filter.begin(samplerate);

  
  frequency = 25000; //sets a 25 microsecond frequency for the measurement
  microsPrevious = micros();
}

void loop() {
  float aix, aiy, aiz;
  float gix, giy, giz;
  float magX, magY, magZ;
  float ax, ay, az;
  float gx, gy, gz;
  float roll, pitch, yaw;
  unsigned long microsNow;

  // check if it's time to read data and update the filter
  microsNow = micros();
  if (microsNow - microsPrevious >= frequency) {

  
    if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
      IMU.readAcceleration(ax, ay, az);
      IMU.readGyroscope(gx, gy, gz);
      IMU.readMagneticField(magX, magY, magZ);

      // update the filter, which computes orientation
      filter.update(gx, gy, gz, ax, ay, az, magX, magY, magZ);

      // print the heading, pitch and roll
      roll = filter.getRoll();
      pitch = filter.getPitch();
      yaw = filter.getYaw();
      Serial.print("[");
      Serial.print(pitch);
      Serial.print(",");
      Serial.print(roll);
      Serial.print(",");
      Serial.print(yaw);
      Serial.print("]");
      Serial.println();

      microsPrevious = microsPrevious + frequency;
    }
  }
}
