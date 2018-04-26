import time
import sys
from dronekit import connect, VehicleMode
from subprocess import PIPE, Popen
from threading  import Thread

newCmd = 0
command = ""

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(out, queue):
    #for line in iter(lambda: out.read(1), b''):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def ReadRadioInput():
    global newCmd
    global command

    while True:
        try:
            line = q.get_nowait() # or q.get(timeout=.1)
        except Empty:
            break
        else:
            #print("Got: "+line)
            newCmd = 1
            command = line.strip()

p = Popen(['../RaspberryPiDrone'], stdin=PIPE, stdout=PIPE, bufsize=1, close_fds=ON_POSIX)
sys.stdout = p.stdin
q = Queue()
t = Thread(target=enqueue_output, args=(p.stdout, q))
t.daemon = True # thread dies with the program
t.start()

vehicle = connect("/dev/serial0", baud=57600, wait_ready=True)
gpsData = "%s\n" % vehicle.location.global_frame

print("Basic pre-arm checks")
while not vehicle.is_armable:
    print(" Waiting for vehicle to initialise...")
    time.sleep(1)

# vehicle.armed = True
# vehicle.mode = VehicleMode("GUIDED")
# vehicle.simple_takeoff(10)
# vehicle.mode = VehicleMode("LAND")
# 
# print "Global Location: %s" % vehicle.location.global_frame
# print "%s" % vehicle.mode
# print "%s" % vehicle.armed

while True:
    ReadRadioInput()
    time.sleep(1)
    if newCmd == 1:
        newCmd = 0
	print("Executing: "+command)
        exec(command)

vehicle.close()
p.kill()
