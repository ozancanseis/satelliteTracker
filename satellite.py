# =========== SATELLITE =========== #

import time
import geocoder
from skyfield.api import load, wgs84
from skyfield.api import EarthSatellite
from main import send_results

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

        if alt.degrees < 0:
            print('The Object is below the horizon')

        print('Altitude:', alt)
        print('Azimuth:', az)
        print('Distance: {:.1f} km'.format(distance.km))

        send_results(alt, az)
        end_time = time.time()
        time.sleep(30 - (end_time - start_time))

