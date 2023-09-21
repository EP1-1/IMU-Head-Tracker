# IMU-Head-Tracker
Using an Arduino Nano 33 BLE, I wanted to translate the movements recorded by the IMU into my pilot's head in DCS World real time.

# Background:
Using an Arduino Nano 33 BLE (LSM9DS1), I wanted to try to translate the movements of my head to my pilot's head in [DCS World](https://www.digitalcombatsimulator.com/en/).

I chose the Arduino Nano 33 BLE for this project because it fit multiple criteria I was looking for:

First, it has bluetooth - meaning that I could make this cordless. 

Second, it has a decent 9 degrees of freedom IMU (Inertial Measurement Unit) - the LSM9DS1. An [IMU](https://en.wikipedia.org/wiki/Inertial_measurement_unit) is a device that can measure rotational rate, acceleration, and (for mine) the Earth's magenetic field. 

The IMU does this using 3 sensors - gyroscope, accelerometer, and magnetometer, each with 3 degrees of freedom (commonly abbreviated as "DoF").

A gyroscope is a device that measures angular velocity - the "rotational force" of the Arduino. For example, if you take a ball and roll it around in your hands, a gyroscope (or "gyro" for short) would be used to measure the rate of rotation of the ball.
The gyro has 3 Degrees of freedom - x, y, z. Gyros, however, have a huge problem - they are SUPER drifty. The raw readings given off by the gyro change many times per second, even when the device is stationary, making the data unuseable.

An accelerometer measures acceleration with relation to gravity. More specifically, it can be used to measure the device's current "cartesian angle." If you have a graph, the accelerometer measures the x and y axis of movement on the graph. Pitch (y-axis) on the accerometer can be thought of as the steepness of the device's current upward angle. The roll measures the rotation around the cartesian x-axis (the rocking side to side). Think of it like a plane - the pitch is the nose of the plane moving up and down, and the roll is the plane's wings rocking back and forth around the x-axis. 

A magnetometer measures Earth's magnetic field with 3 DoF. A magnetometer makes it easier to find an absolute heading/orientation (beceause Earth's magnetic field is constant). A magnetometer could be used to make a simple compass. Magnetometers also have a large issue - Earth's magnetic field isn't very strong relative to other sources of electromagnetic interference (EMI) and is easily overpowered. During my testing, being anywhere near my PC would cause the magnetomter to drift. Even calibrating this out is difficult due to the strength of the EMI (and because the magnetometer in the LSM9DS1 isn't very sophisticated - relatively speaking). 


# Sensor Fusion:

In order to supress the weakneses present in all 3 sensors, sensor fusion is required. [Sensor Fusion](https://en.wikipedia.org/wiki/Sensor_fusion) is the process of merging the data from all 3 sensors to reduce the weaknesses present in one of the sensors.
There are many different types of sensor fusion algorithms. The most commonly used algorithm for these applications are the Madgwick Filter, Mahoney Filter, and Kalman Filter. I tried all 3 of these filters and found most success in the Madgwick Filter, so I mainly focused on that. Also, the Madgwick filter is the most commonly used for these types of applications. The [Kalman Filter](https://en.wikipedia.org/wiki/Kalman_filter) is used in many different scenarios and its strength is predicting a future state based on measurements taken over time. But, that was not a requirement for this application, so this algorithm was not used. The [Mahoney Filter](https://ahrs.readthedocs.io/en/latest/filters/mahony.html), is similar to the Madgwick, but not as good at obtaining heading orientation. I found this to be true during my testing.

Arduino already has a library for the Madgwick Filter, so I didn't have to actually rebuild the entire algorithm, I just had to implement it. The library is called [MadgwickAHRS](https://github.com/arduino-libraries/MadgwickAHRS). The "AHRS" part stands for Atitude Heading Reference System and refers to finding absolute heading of the device. Digital Combat Simulator's pilot's head movement requires an absolute orientation, so relative movements (measuring only the changes in movement instead of measuring exactly where the device is pointed relative to where it started) will not work because the pilots head would reset to point (0,0) each time no movement is detected. These absolute measurements are called [Euler Angles](https://en.wikipedia.org/wiki/Euler_angles).

Measuring pitch and roll angle is super easy - the accelerometer can take care of that inherently. The hard part - and the reason sensor fusion is needed - is because of measuring yaw (heading). Yaw is the twisting side-to-side motion (z-axis). In this case, its the user turning their head side to side. Getting an accurate heading is very difficult due to drift and because it requires advanced computation (a filter). This is where 99% of the difficulties with this project emerged. 

# How it Works:

First, the IMU collects the raw acceleration, magnetic field, and gyroscopic information (3 degrees each). 

Second, the Madgwick filter takes all 9 Dof and estimates 3 Euler angles - pitch, roll, and yaw (heading). The data is then sent over serial to a virtual game controller created by the python script which recieved the data and emulates a virtual joystick. This is what makes the data accessable/readable by apps such as DCS or opentrack (which see it as "Xbox 360 controller").

Fourth, the emulated joystick input data is sent to an app called [opentrack](https://github.com/opentrack/opentrack) which communicates with DCS using the [FreeTrack](https://en.wikipedia.org/wiki/FreeTrack) protocol. Opentrack also smooths the input data a little more and shows me some analytics on what the axis are currently doing.





# Difficulties/Findings:

Since my Arduino operates very close to my PC, I found that there is a considerably large amount of EMI to work around and there is no easy solution. The head-tracker works initially decently accurately at first. Some of the inaccuracies can be mitigated by smoothing the data - basically just creating a data buffer (of 10 in my case) - then just computing the average value of that buffer to use for the final value sent out to the joystick output. 

Unfortunately, after a while, the drift problem starts to set in. The best way to describe this phenomenon is that the device gets "lost" after moving it around too much. It temporarily cannot find its accurate/actual position. When this happens, I found that letting it sit stationary for a few seconds allows it to find the right orientation again. 

This problem is what makes an intertial head tracker not practical - at least in my case. Working out the drift problem is way too difficult, especially on a $25 Arduino Nano.

I even tried using another application called [HeadTracker](https://github.com/dlktdr/HeadTracker) made by dlkrdr to solve the issue, or to at least give me some ideas. The app comes with is own custom Arduino firmware, a really nice UI, magnetometer calibration, gyro and acceletomter calibration, etc. 

Using this app didn't fix the issue I was trying to solve, and the Arduino was still too drifty. I contacted the developer (who was very helpful) and tried my own methods to remedy the issue, with no luck. 

Disabling the magnetometer sort of helps temporarily, but eventually the drift will completely take over a just a few seconds to minutes later.

# Conclusion:

Honestly, I wanted to try this project just because I wanted to see if I could do it. I was able to make a working prototype, but the complexities associated with the weaknesses of this Arduino's IMU made is undoable in the amount of time I was willing to spend - which was already a lot (and assuming that producing a stable headtracker that you would actually want to use can actually be done with a $25 Arduino board, which remains a question). This was a super interesting project for me because I learned so much about IMU's, sensor fusion algorithms, using Github and downloading open source programs, and just more experience with an Arduino. This project required me to code both in C++ (for Arduino) and Python for the gamepad emulation. Also, this project required me to really brainstorm around several large issues:

First, the accurate heading problem - being able to calculate the devices absolute heading relative to an initial point (Euler angles). 

Second, was actually figuring out a method of communicating the information to DCS. Emulating a virtual joystick was a good solution. I found that many other pieces of hardware (specifcally DIY devices for DCS) use this method to communicate with the game. For example, one really cool DIY project - one that I am working on right now - is a flight panel (basically a fancy button box that makes interacting with my cockpit on the F18 more tangible/immersive). Without going into too much detail, some commerical devices do the same thing mine does - emulating a game controller and each button press corresponds to a button on the virtual gamepad. I found this interesting, and I hadn't (at the time) seen another device do this for my specific (or related) application when I came up with the idea. 

Third, researching and choosing the correct sensor fusion filter. It might seem obvious to use the Madgwick - seeing as it was made specifcally for this purpose - but I wanted to try the other 2 (Kalman and Mahoney) just to see and learn more.

Fourth, the drift problem. Even though I didn't fully overcome this problem, I was able to diagnose the problem and attempt to remedy it. Talking to one of the engineers at the engineering company I interned at over the summer 2023 - where I did electrical and electronics engineering work - IMUs can be very difficult to work with. Many times, production-level equipment doesn't just use intertial tracking to find orientation - because it would encounter the exact the same issues as my device. Some of the equipment suppliments the intertial data with GPS reference so that the drift problem is mostly eliminated. This seems to be the best way - from my research - of fixing this issue (using GPS). 

In conclusion, even though I couldn't get the Arduino to the core of the stable headtracker (within a reasonable amount of time) that I wanted to build, I was able to demonstrate a working proof-of-concept. I learned a ton about filters and their various strengths/weaknesses, and the process and variables that an engineer must consider when bringing projects to life.

