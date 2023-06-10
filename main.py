# =========== Imports =========== #
#libraries
import satellite as st
import planet as pt
#from declination import calculate_declination
import serial
import time


# =========== UNIT TRANSFORMER =========== #
#transform units into degrees

# def decdeg2dms(dd): #DMS to Degree Transformation
#     is_positive = dd >= 0
#     dd = abs(dd)
#     minutes,seconds = divmod(dd*3600,60)
#     degrees,minutes = divmod(minutes,60)
#     degrees = degrees if is_positive else -degrees
#     return (degrees,minutes,seconds)ß

# =========== MAIN =========== #

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

#run main() in infinite loop
while True: 
    
    main()
