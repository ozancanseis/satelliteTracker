import pyfirmata
import time

# Set up the connection to the Arduino using the specified port
board = pyfirmata.Arduino('COM3')

# Define the pin that the servo is connected to
servo_pin = 9

# Set up the servo on the specified pin
servo = board.get_pin('d:{}:s'.format(servo_pin))

# Define the minimum and maximum angles for the servo
min_angle = 0
max_angle = 180

def set_angle(angle, ramp_time=0.5):
    # Convert the angle to a value between 0 and 1
    value = (angle - min_angle) / (max_angle - min_angle)

    # Get the current position of the servo
    current_value = servo.read()

    # Determine the difference between the current position and the target position
    delta = value - current_value

    # Divide the difference by the ramp time to get the step size
    step_size = delta / (ramp_time / 0.01)

    # Set the servo position gradually, one step at a time
    for i in range(int(ramp_time / 0.01)):
        current_value += step_size
        servo.write(current_value)
        time.sleep(0.01)

    # Set the final servo position to the desired value
    servo.write(value)

# Example usage: Move the servo to 90 degrees over 1 second
set_angle(90, ramp_time=1.0)

# Clean up the connection to the Arduino
board.exit()