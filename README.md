# IMU-Head-Tracker
I wanted to try using an IMU to track the movements of my head, and translate them into DCS World.

# Background:
Using an Arduino Nano 33 BLE (LSM9DS1), I wanted to try to translate the movements of my head, to my pilots head in game - DCS World (https://www.digitalcombatsimulator.com/en/).

I chose the Arduino Nano 33 BLE for this project because it fit multiple criteria I was looking for. 

First, it has a decent 9 degrees of freedom IMU (Inertial Measurement Unit) - the LSM9DS1. An IMU is a device that can measure rotational rate, acceleration, and (for mine) Earth's magenetic field https://en.wikipedia.org/wiki/Inertial_measurement_unit.

The IMU does this using 3 sensors - gyroscope, accelerometer, and magnetometer, each with 3 degrees of freedom (commonly abbreviated as "DoF").

A gyroscope is a device that measures angular velocity - the "rotational force" of the arduino. For example, if you take a ball and roll it around in your hands, a gyroscope would be used to measure the rate of rotation of the ball.
The gyro has 3 Degrees of freedom - x, y, z. Gyros have a huge problem - they are SUPER drifty. The readings given off by the gyro change many times per second, even when the device is stationary.

An accelerometer measures acceleration with relation to gravity. More specifically, it can be used to measure the device's current "cartesian angle." If you have a graph, the accelerometer measures the x and y axis of movement on the graph. Pitch (y-axis) on the accerometer can be thought of as the steepness of the device. The roll axis (x) measures the rotation around the cartesian x-axis (the rocking side to side). Think of it like a plane - the pitch is the nose of the plane moving up and down, and the roll is the planes rocking back and forth axis. 


# The Project:


