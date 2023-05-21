# import time
# import serial
# arduino = serial.Serial('COM10', 9600)
#
# def send_to_arduino(message, start, end):
#     message = start + message + end
#     arduino.write(message.encode('utf-8'))
# i = 1
# while True:
#     for angle in range(180):
#         send_to_arduino(str(angle), '!', '?')
#         time.sleep(.1)
#         send_to_arduino(str(angle), '+', '-')
#         # send_to_arduino(message=str(angle))
#         print("sent")
#         time.sleep(1)
#     for angle in range(180, 0, -1):
#         send_to_arduino(str(angle), '!', '?')
#         time.sleep(.1)
#         send_to_arduino(str(angle), '+', '-')
#         # send_to_arduino(message=str(angle))
#         print("sent")
#         time.sleep(1)


# import time
# from servo_mover import ServoMover

# port = '/dev/cu.usbserial-14120'
# pin = 9

# servo = ServoMover(port, pin)

# servo.reset_position()
# i = 1
# while True:
#     angle = 45 * (i % 4)
#     print(angle)
#     i += 1
#     servo.rotate_servo(angle)
#     time.sleep(1)
import time
from pyfirmata import Arduino, SERVO

port = "COM10"
pin = 9

board = Arduino(port)

board.digital[pin].mode = SERVO

def rotate_servo(angle, pin):
    board.digital[pin].write(angle)
    time.sleep(.015)

while True:
    for i in range(180):
        rotate_servo(i, pin)