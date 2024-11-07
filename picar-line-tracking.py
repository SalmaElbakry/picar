#  ___   ___  ___  _   _  ___   ___   ____ ___  ____  
# / _ \ /___)/ _ \| | | |/ _ \ / _ \ / ___) _ \|    \ 
#| |_| |___ | |_| | |_| | |_| | |_| ( (__| |_| | | | |
# \___/(___/ \___/ \__  |\___/ \___(_)____)___/|_|_|_|
#                  (____/ 
# Osoyoo Raspberry Pi Robot Car Line Tracking auto driving
# tutorial url: https://osoyoo.com/?p=32082

import time
import RPi.GPIO as GPIO
# Import the PCA9685 module.
# Import the PCA9685 module.
from board import SCL, SDA
import busio
# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685
from controller import Robot, Camera, Motor
# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pwm =  PCA9685(i2c_bus)

# Initialization
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Set up the camera and motors
camera = robot.getDevice("camera")
camera.enable(timestep)
width = camera.getWidth()
height = camera.getHeight()

left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")

# Set motors to velocity mode
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

# Base speed setting
base_speed = 3.0
turn_speed = 1.5

# Main control loop
while robot.step(timestep) != -1:
    # Get the image
    image = camera.getImage()
    # Extract gray values of the middle row
    mid_line_gray_values = [camera.imageGetGray(image, width, x, int(height / 2)) for x in range(width)]

    # Calculate the average gray value for the left and right halves of the image
    left_gray = sum(mid_line_gray_values[:width // 2]) / (width // 2)
    right_gray = sum(mid_line_gray_values[width // 2:]) / (width // 2)

    # Line-following control logic
    if left_gray < right_gray:  # Line is more on the left side
        left_motor.setVelocity(base_speed - turn_speed)
        right_motor.setVelocity(base_speed + turn_speed)
    elif right_gray < left_gray:  # Line is more on the right side
        left_motor.setVelocity(base_speed + turn_speed)
        right_motor.setVelocity(base_speed - turn_speed)
    else:  # Line is centered
        left_motor.setVelocity(base_speed)
        right_motor.setVelocity(base_speed)
