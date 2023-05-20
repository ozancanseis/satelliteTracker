from pyfirmata import Arduino, SERVO
from time import sleep

class ServoMover:
    port = str()
    pin = int()

    def __init__(self, port, pin):

        if not isinstance(port, str):
            raise TypeError(f"Port must be a string, not {type(port)}")
        if not isinstance(pin, int):
            raise TypeError(f"Pin value must be an integer, not {type(pin)}")

        self.port = port
        self.pin = pin
        self.board = Arduino(port)
        self.board.digital[self.pin].mode = SERVO

    def rotate_servo(self, angle):
        if isinstance(angle, float):
            angle = round(angle)
        elif not isinstance(angle, int):
            raise TypeError(f"Angle value must be integer or float, not {type(angle)}")
        self.board.digital[self.pin].write(angle)
        sleep(.015)

    def current_position(self):
        return self.board.digital[self.pin].read()
    
    def reset_position(self):
        self.rotate_servo(0)