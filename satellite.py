# =========== SATELLITE =========== #

import time
import geocoder
from skyfield.api import load, wgs84
from skyfield.api import EarthSatellite
import serial
import time

# =========== GLOBAL VARIABLES =========== #

#serial communication start (Port should be changed to the correct value)
arduino = serial.Serial(port='/dev/cu.usbserial-14120', baudrate=115200, timeout=.1) #baudrate should be same with Arduino

upper_limit1 = 360 #upper limit angle value for servoMotorA
lower_limit1 = 0  #lower limit angle value for servoMotorB

upper_limit2 = 360 #upper limit angle value for servoMotorA
lower_limit2 = 0 #lower limit angle value for servoMotorB

# =========== SERVO MOVERS =========== #
#servo angle set function
def servo_angle(x,y):

    #first upper and lower limit

    if(int(x)>upper_limit1 and str(y)=="a"):
        print("Upper limit reached")
        return -1
    
    if(int(x)<lower_limit1 and str(y)=="a"):
        print("Lower Limit reached")
        return -1
    
    #second upper and lower limit

    if(int(x)>upper_limit2 and str(y)=="b"):
        print("Upper limit reached")
        return -1
    
    if(int(x)<lower_limit2 and str(y)=="b"):
        print("Lower Limit reached")
        return -1
    

        #bytes are written
    #str(x) = degrees in string
    #str(y) = which servo motor in string
    arduino.write(bytes(str(x)+str(y)+",", 'utf-8'))
    
    #test clause
    print(str(x)+str(y)+",")

    #time sleep for 0.05 seconds to read serial_communication data
    time.sleep(0.05)
    data = arduino.readline()
    
    #returns serial_communication data
    return data


def print_stations():
    stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'
    satellites = load.tle_file(stations_url, reload=True)
    print('Loaded', len(satellites), 'satellites')

    #Ask Input and Find a satellite from lsit by:
    print("\nID    \tName")
    for satellite in satellites:
        target = str(satellite.target)
        print('#' + target[2:], "\t", satellite.name)
    return satellites


def print_satellite(satellites: list, id: int):
    by_number = {sat.model.satnum: sat for sat in satellites}
    satellite = by_number[id]
    print(satellite)
    return satellite

def get_satellite_from_tle():
    input_toggle = 0
    while input_toggle != 1 and input_toggle != 2:
        input_toggle = int(input("\nPress 1 to enter TLE information manually.\nPress 2 to read TLE information from tle.txt\n"))
    if input_toggle == 1:
        print("Enter TLE.")
        print("Example TLE format:\n1 25544U 98067A   14020.93268519  .00009878  00000-0  18200-3 0  5082\n2 25544  51.6498 109.4756 0003572  55.9686 274.8005 15.49815350868473\n")
        line1 = input("Line 1: ")
        line2 = input("Line 2: ")
    else:
        with open("tle.txt", "r", encoding="utf-8") as tle_conf:
            line1 = tle_conf.readline()
            line2 = tle_conf.readline()
    ts =  load.timescale()
    satellite = EarthSatellite(line1, line2, "GivenTLE", ts)
    print(satellite)
    track_satellite(satellite)

def track_satellite(satellite):
    # Get observer location
    g = geocoder.ip('me')
    print("Observer location:", g.latlng)
    observer = wgs84.latlon(g.latlng[0], g.latlng[1])

    while True:
        start_time = time.time()
        # Generate a satellite position
        ts = load.timescale()
        t = ts.now()
        geocentric = satellite.at(t)

        difference = satellite - observer

        topocentric = difference.at(t)
        alt, az, distance = topocentric.altaz()
        print("alt: ", alt._degrees)
        print("az: ", az._degrees)

        servo_angle(alt._degrees, "a")
        servo_angle(az._degrees, "b")

        time.sleep(30)

