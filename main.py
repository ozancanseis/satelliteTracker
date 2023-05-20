# =========== Imports =========== #
import satellite as st
import planet as pt
from declination import calculate_declination
from .servo_mover import ServoMover
# from magnetic_field_calculator import MagneticFieldCalculator

# =========== GLOBAL VARIABLES =========== #

BOARD_PORT = ""
VERTICAL_SERVO_PIN = 9
HORIZONTAL_SERVO_PIN = 10

# =========== SERVO MOVERS =========== #

vertical_servo   = ServoMover(BOARD_PORT, VERTICAL_SERVO_PIN)
horizontal_servo = ServoMover(BOARD_PORT, HORIZONTAL_SERVO_PIN)

# =========== MAIN =========== #
def send_results(alt, az):
    alt, az = alt.degrees, az.degrees
    print("calculated alt:", alt)
    print("calculated az:", az)
    if az >= 0 and az <= 360:
        if alt >= 0:
            if alt <= 70:
                vertical_servo.rotate_servo(alt)
                horizontal_servo.rotate_servo(az)
            else:
                print("Altitude too high -", alt)
        else:
            print("Altitude too low -", alt)
    else:
        print("Invalid Azimuth -", az)


def decdeg2dms(dd): #DMS to Degree Transformation
    is_positive = dd >= 0
    dd = abs(dd)
    minutes,seconds = divmod(dd*3600,60)
    degrees,minutes = divmod(minutes,60)
    degrees = degrees if is_positive else -degrees
    return (degrees,minutes,seconds)

#altitude = 0
#azimuth = calculate_declination()
#degree, minutes, seconds = decdeg2dms(azimuth)
#azimuth = degree + minutes/60 + seconds/3600
#print("azimuth: ", azimuth)

def fnc1():
    print("triggerarduino")
    

def main():
    if __name__ == "__main__":
        track_input = 0
        while track_input != 1 and track_input != 2:
            track_input = int(input("Press 1 to track a sattelite / a known spacecraft\nPress 2 to track a planet.\n"))

        # Tracking known spacecraft
        if track_input == 1:
            print("Track Satellite / Known Aircraft")
            list_tle_input = 0
            while list_tle_input != 1 and list_tle_input != 2:
                list_tle_input = int(input("Press 1 to track an item from the list\nPress 2 to enter TLE information.\n"))

            # Tracking from list
            if list_tle_input == 1:
                satellites = st.print_stations()
                spacecraft_id = int(input("Enter ID from the list: "))
                satellite = st.print_satellite(satellites, spacecraft_id)
                st.track_satellite(satellite)
            # Tracking by TLE input
            elif list_tle_input == 2:
                st.get_satellite_from_tle()

        # Tracking Planet
        elif track_input == 2:
            pt.planet()

main()
