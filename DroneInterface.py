import time
import sys
from dronekit import connect, VehicleMode
from subprocess import PIPE, Popen
from threading  import Thread
from collections import deque
from functools import reduce
import numpy as np

newCmd = 0
command = ""

role = "server"

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

ON_POSIX = 'posix' in sys.builtin_module_names

role = "server"
outputBuffer = deque([])

def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in range(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines)

def checksum256(st):
    return reduce(lambda x,y:x+y, map(ord, st)) % 256

def SetupConnection():
    seqNum = np.uint16(0)
    ackNum = np.uint16(0)
    flags = np.uint8(0)
    txData = ""
    TxPacket(seqNum, ackNum, flags, txData)
    #Expect a return packet with the prev seq number plus the amout of data (data len + 2 for ack + 2 for seq + 1 for flags
    expSeqNum = np.uint16(0)
    expAckNum = np.uint16(1)
    if(WaitForAck(expSeqNum, expAckNum, np.uint8(18)) == False):
        TxPacket(seqNum, ackNum, flags, txData)
    seqNum = np.uint16(1)
    ackNum = np.uint16(1)
    flags = np.uint8(16)
    TxPacket(seqNum, ackNum, flags, txData)
    flags = np.uint8(18)
    if(WaitForAck(expSeqNum, expAckNum, flags) == False):
        SetupConnection()
    print("Connection Established")

def CloseConnection(seqNum, ackNum):
    flags = np.uint8(1)
    TxPacket(seqNum, ackNum, flags, "")
    #Expect a return packet with the prev seq number plus the amout of data (data len + 2 for ack + 2 for seq + 1 for flags
    expSeqNum = np.uint16(0)
    expAckNum = np.uint16(1)
    if(WaitForAck(expSeqNum, expAckNum, np.uint8(17)) == False):
        TxPacket(seqNum, ackNum, flags, txData)
    print("Connection closed")


def SendData(data):
    maxFrameSize = 64
    maxPacket = maxFrameSize - 6  
    lenSent = 0
    flags = np.uint8(0)
    seqNum = np.uint16(1)
    ackNum = np.uint16(1)
    SetupConnection()
    while lenSent < len(data):
        if(lenSent+maxPacket >= len(data)):
            txData = data[lenSent:]
            lenSent = len(data)
            #Turn on the push to denote the end of the transfer
            flags = np.uint8(np.bitwise_or(flags, 8))
        else:
            txData = data[lenSent:lenSent+maxPacket]
            lenSent = lenSent + maxPacket
        flags = np.uint8(np.bitwise_or(flags, 2))
        TxPacket(seqNum, ackNum, flags, txData)
        #Expect a return packet with the prev seq number plus the amout of data
        expAckNum = seqNum+len(txData)
        expSeqNum = ackNum
        #function to wait for the ack
        if(WaitForAck(expSeqNum, expAckNum, np.uint8(18)) == False):
            TxPacket(seqNum, ackNum, flags, txData)
    CloseConnection(seqNum, ackNum)

def TxPacket(seqNum, ackNum, flags, txData):
    flagsStr = flags.tobytes().decode("ASCII")
    seqNumStr = seqNum.byteswap().tobytes().decode("ASCII")
    ackNumStr = ackNum.byteswap().tobytes().decode("ASCII")
    if(txData != ""):
        crc = checksum256(txData)
    else:
        crc = 0
    txData = seqNumStr+ackNumStr+flagsStr+txData
    txData = txData+chr(crc)
    print(hexdump(txData))
    p.stdin.write(txData) 

def WaitForAck(expSeqNum, expAckNum, flags):
    #print("Exp seq: "+str(expSeqNum))
    #print("Exp ack: "+str(expAckNum))
    #print("Exp flags: "+str(flags))
    return True

def enqueue_output(out, queue):
    #for line in iter(lambda: out.read(1), b''):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def ReadRadioInput():
    global newCmd
    global command

    print("Reading Inputs")
    p.stdin.write("\r\nThump thump"+str(time.time())+"\r\n")
    while True:
        try:
            line = q.get_nowait() # or q.get(timeout=.1)
        except Empty:
            break
        else:
            print("Got: "+line)
            newCmd = 1
            command = line.strip()

p = Popen(['../RaspberryPiDrone'], stdin=PIPE, stdout=PIPE, bufsize=1, close_fds=ON_POSIX)
#sys.stdout = p.stdin
q = Queue()
t = Thread(target=enqueue_output, args=(p.stdout, q))
t.daemon = True # thread dies with the program
t.start()

try:
    vehicle = connect("/dev/serial0", baud=57600, wait_ready=True)
except:
    print("Error Connecting")
    exit()

print("Basic pre-arm checks")
while not vehicle.is_armable:
    print(" Waiting for vehicle to initialise...")
    time.sleep(1)
print("Basic pre-are checks complete")

#gpsData = "%s\n" % vehicle.location.global_frame
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
	print("Executing: ("+command+")")
        outputBuffer.append("\r\nExecuting :"+command+"\r\n")
        try:
            exec(command)
        except:
            print("Bad Command")
            outputBuffer.append("\r\nBad Command\r\n")
            continue
        outputBuffer.append("\r\n%s\r\n" % vehicle.location.global_frame)
    while(len(outputBuffer)):
        SendData(outputBuffer.popleft())
vehicle.close()
p.kill()
