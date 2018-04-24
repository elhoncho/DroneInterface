import time
from dronekit import connect, VehicleMode

# Connect to the Vehicle.
vehicle = connect("/dev/serial0", baud=57600, wait_ready=True)

while True:
    print " GPS: %s" % vehicle.location.global_frame
    time.sleep(5)
# Close vehicle object before exiting script
vehicle.close()