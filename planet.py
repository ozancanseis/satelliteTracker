# =========== PLANET =========== #

# Create a timescale and ask the current time.
import time
import geocoder
from main import send_results
from skyfield.api import N, W, load, wgs84

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

        #print('Altitude:', alt)
        #print('Azimuth:', az)
        #print('Distance: {:.1f} km'.format(distance.km))

        send_results(alt, az)

        time.sleep(30)
