import time
import sys
from dronekit import connect, VehicleMode

# Connect to the Vehicle.
vehicle = connect("/dev/serial0", baud=57600, wait_ready=True)

while True:
    output = " GPS: %s" % vehicle.location.global_frame
    sys.stdout.write(output)
    print("\r\n")
    time.sleep(5)
# Close vehicle object before exiting script
vehicle.close()