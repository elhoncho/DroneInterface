import subprocess
import time
from dronekit import connect, VehicleMode

vehicle = connect("/dev/serial0", baud=57600, wait_ready=True)
gpsData = "%s\n" % vehicle.location.global_frame

p = subprocess.Popen(['../RaspberryPiDrone'],
                     stdin=subprocess.PIPE)
p.stdin.write(gpsData)

print("Basic pre-arm checks")
while not vehicle.is_armable:
    print(" Waiting for vehicle to initialise...")
    time.sleep(1)

print("Arming Motors")
vehicle.mode = VehicleMode("GUIDED")
vehicle.armed = True

while not vehicle.armed:
    print("Waiting for arming...")
    time.sleep(1)

print("Taking off!")
vehicle.simple_takeoff(10) # Take off to target altitude

vehicle.close()
p.kill()