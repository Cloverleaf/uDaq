#This is used to query a JENCO 6230N pH meter
#The command to query this pH meter is "S00"
#The meter will respond with the a structured string of data
#uD3 is the ubuntu version of the uDaq script 

#known issues:
#Sensors limit the sampling rate to 30 hZ
#The script slows down after ~1330 measurements.  This occurs with or without graphing.  The source of this bug is unclear.

import serial
import io
from datetime import datetime
import time
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.pylab import subplots, close
filename = raw_input("Save pH data as: ")
#Serial port names
#MacOS '/dev/tty.usbserial'
#Ubuntu '/dev/ttyUSB0'

#USB port names (force transducer)
#MacOS '/dev/tty.usbmodem621'
#Ubuntu '/dev/ttyACM1'
phPORT = '/dev/ttyUSB1'
forcePORT = '/dev/ttyACM1'
plotLength = 20
BAUD = 9600
COLLECTION_RATE = 100
COLLECTION_SECONDS = 60*8 #change to 60*8 when done debugging

class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
	
    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000
        if self.verbose:
            print 'elapsed time: %f ms' %self.msecs

#may not need a function here until the demands get more complicated
#def readMeter():

#serial port information for the force transducer
with Timer() as t:
    ForceSer = serial.Serial(port=forcePORT, baudrate=BAUD)
    ForceSio = io.TextIOWrapper(io.BufferedRWPair(ForceSer,ForceSer))
print "=> elapsed ForceSer+ForceSio: %s s" %t.secs

#serial port information for the ph meter
with Timer() as t:
    phSer = serial.Serial(port=phPORT, baudrate=BAUD)
    phSio = io.TextIOWrapper(io.BufferedRWPair(phSer,phSer))
print "=> elapsed pHSer+pHSio: %s s" %t.secs


numDataPoints = COLLECTION_RATE*COLLECTION_SECONDS
output = open(filename, 'w')
counter = 0

def getTime():
    timeTemp = time.localtime()
    timeTuple = timeTemp[3:6]
    timeList = list(timeTuple)
    timeStr = ""
    temp = []
    for i in timeList:
        temp.append(str(i))

    timeStr=":".join(temp)
    return timeStr



#Plotting not ready yet
#Jenco data is parsed now
#Need handling for error strings from JENCO6230N
#Currently commented out the plot2 containing pH information; this is lower value than force 
#Testing performance gains

#pltCount = 0
#y=[0]
#x=[0]
#phX=[0]
#phY=[0]
#forceX=[0]
#forceY=[0]
#fig, ax = subplots(1,1)
#ax.set_xlim(0,numDataPoints)
#ax.set_ylim(0, 1400)
#ax.hold(True)
#plt.ion()
#plt.show(block=False)
#plot = ax.plot(forceX,forceY, lw=0.5)[0]
#plot2 = ax.plot(phX, phY, lw=0.5)[0]
#tic = time.time()

#x = [0]
#y = [0]

#write the header for the file
output.write("Int" + "\t" + "Time" + "\t" + "Force" + "\t" + "pH" + "\t" + "mV" + "\n")

while counter <= (numDataPoints):
    with Timer() as t:
        time.sleep(1/COLLECTION_RATE)
    print "=> sleep: %s s" %t.secs
    with Timer() as t:
        phSer.write('S00')
    print "=> pHser.write: %s s" %t.secs
    with Timer() as t:
        ForceSer.write(unicode('1'))
    print "=> ForceSer.write(): %s s" %t.secs
    with Timer() as t:
        current_time = getTime()
    print "=> current_time: %s s" %t.secs
    countStr = str(counter)
    with Timer() as t:
        line = phSer.readline()
    print "=> phSer.readline(): %s s" %t.secs
    milivoltVal = line[4:10] #the output from the JENCO6230N has fixed width so slicing works
    phVal= float(line[12:17])
    #ForceSer.write(unicode('1'))
    with Timer() as t:
        line = ForceSer.readline()
    print "=> ForceSer.readline(): %s s" %t.secs
    forceVal = (1023-int(line))
#    forceY.append(forceVal)
#    forceX.append(counter)
#    phX.append(counter)
#    phY.append(phVal*100) #phY is the graphed value of the pH meter reading, multiply by 100 to have it fit on the same scale as the force measurements
#    pltCount+=1
 #   if pltCount >= 10:
 #       if len(forceX) < plotLength:
#        	plot.set_data(forceX,forceY)
#                plot2.set_data(phX, phY)
#	else:
#		plot.set_data(forceX[(len(forceX)-plotLength):], forceY[(len(forceY)-plotLength):])
#                plot2.set_data(phX[(len(phX)-plotLength):], phY[(len(phY)-plotLength):])
#        ax.draw_artist(plot)
#        ax.draw_artist(plot2)
#        fig.canvas.blit(ax.bbox)
#        pltCount = 0	
    with Timer() as t:
        data = countStr + "\t" + current_time + "\t" + str(forceVal) + "\t" + str(phVal) + "\t" + milivoltVal + "\n"
    print "=> data string formatting: %s s" %t.secs
#    with Timer() as t:
#        print data
#    print "=> print data: %s s" %t.secs
    with Timer() as t:
        output.write(data)
    print "=> output.write(data): %s s" %t.secs
    counter += 1
    if phSer.isOpen()==False:
        break
output.close()
