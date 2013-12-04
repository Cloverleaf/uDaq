#calculates the slow down of data sampling using the pyD2.py script

import pandas as pd
import matplotlib.pyplot as plt


def performanceArray(file):
    data = pd.read_csv(file, delimiter = '\t')
    data.columns = ['int', 'time', 'val1','val2','val3']

    startTime = data.time[0].split(':')
    currentMinute = int(startTime[1])
    currentHour = int(startTime[0])
    currentSecond = int(startTime[2])

    endTime = data.time[len(data.time)-1].split(':')
    endHour = int(endTime[0])
    endMinute = int(endTime[1])
    endSecond = int(endTime[2])



    hRecord = endHour - currentHour
    mRecord = hRecord*60 + (endMinute - currentMinute)
    sRecord = mRecord*60 + (endSecond - currentSecond)

    minutesSampled = 0

    Array = [] #save the values for samples per second

    while minutesSampled <= (mRecord-1):
        cmString = str(currentHour) + ":" + str(currentMinute) + ":" + str(currentSecond)
        cmValues = data[data.time == cmString]
        Array.append(len(cmValues))
        currentMinute += 1
        minutesSampled += 1
        if currentMinute > 59:
            currentHour += 1
            currentMinute = 0
    return Array
perf0 = performanceArray('lp_5')                
perf1 = performanceArray('Ubuntu')
perf2 = performanceArray('lp_3')
perf3 = performanceArray('lp_4')
perf4 = performanceArray('mp_1')
    

plt.figure()
plt.plot(perf1)
plt.plot(perf2)
plt.plot(perf0)
plt.plot(perf3)
plt.plot(perf4)
#plt.axis([0, max(len(perf1), len(perf2), len(perf0)), 0, max(max(perf1),max(perf2))+2])
plt.show()
print "Array 1:" 
print perf0 
print "Array 2:" 
print perf1
print "Array 3:"
print perf2
print "Array 4:"
print perf3
print "Array 5:" 
print perf4