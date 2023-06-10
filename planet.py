# =========== PLANET =========== #

# Create a timescale and ask the current time.
import time
import geocoder
from skyfield.api import N, W, load, wgs84
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


def planet():
    g = geocoder.ip('me') #take observer position to calculate topocraphic values
    print('Observer location:', g.latlng)

    # Load the JPL ephemeris DE421 (covers 1900-2050).
    planets = load('de421.bsp')
    print(planets, '\n')
    earth = planets['earth']
    observer = earth + wgs84.latlon(g.latlng[0], g.latlng[1])
    print('OB',observer)

    observant_name = input('Planet To Observe: ')
    try:
        observant = planets[observant_name]
    except:
        print('Planet not found.')
        quit()

    while True:

        ts = load.timescale()
        t = ts.now()

        # What's the position of Mars, viewed from Earth?
        astrometric = observer.at(t).observe(observant)
        alt, az, distance = astrometric.apparent().altaz()
        print("alt: ", alt._degrees)
        print("az: ", az._degrees)

        servo_angle(alt._degrees, "a")
        servo_angle(az._degrees, "b")

        time.sleep(30)