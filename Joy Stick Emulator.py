import vgamepad as vg
import serial
import string
import ast
import numpy as np


#This code takes data from the Arduino being sent over serial - the pitch, roll, and yaw - and emulates a virtual joystick.
#The pitch is the y-axis of the joystick, and the yaw is the x-axis of the joystick.

#initialize serial port
dataport = serial.Serial("COM7", 115200, timeout=3)

#initialize the Virtual gamepad (need the joystick function)
gamepad = vg.VX360Gamepad()


#create a buffer of 10 values for both pitch and yaw - used to average the values (smooth them).
buffer_size = 10
yaw_buffer = np.zeros(buffer_size)
pitch_buffer = np.zeros(buffer_size)


#Remap numbers within user operable range to -1.0 and +1.0 for the joystick
def reMap(value, low_in, high_in, low_out, high_out):
    # Clamp the value to the input range
    value = np.clip(value, low_in, high_in)

    # Calculate the normalized position of the value within the input range
    normalized = (value - low_in) / (high_in - low_in)

    # Remap the normalized value to the output range
    return low_out + normalized * (high_out - low_out)


try:
    while True:
        read_data = dataport.readlines(1)
        decode_serialtostring = read_data[0].decode()
        data_inlist = ast.literal_eval(decode_serialtostring)
        pitch = data_inlist[1]
        yaw = data_inlist[2] 

        pitch_buffer = np.roll(pitch_buffer, -1)#roll pitch array to next value
        yaw_buffer = np.roll(yaw_buffer, -1)#roll yaw array to next value
        yaw_buffer[-1] = yaw 
        pitch_buffer[-1] = pitch
            
            
        smoothed_pitch = np.mean(pitch_buffer)
        smoothed_yaw = np.mean(yaw_buffer)
        

        remap_pitch = reMap(smoothed_pitch, -90, 90, -1.0, 1.0)
        remap_yaw = reMap(smoothed_yaw, 90, 120, -1.0, 1.0)
        gamepad.right_joystick_float(x_value_float=remap_yaw, y_value_float=remap_pitch)
        gamepad.update() 
        print(yaw)
        
except KeyboardInterrupt: 
    exit()

