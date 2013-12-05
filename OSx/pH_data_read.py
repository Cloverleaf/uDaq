import pandas as pd
import numpy as np
#filename = "fatigue_6"

#dataFiles = pd.read_csv("dataList", delimiter ='\t')

outputFile = "pH_recording_data.txt"
output = open(outputFile, 'w')
#structure should be:
#[Filename,   baselineStart,   baselineEnd, finalStart,  finalEnd]
#fatigued animals
fatigue_3 = ['fatigue_3', 5600, 7200, 22500, 23700]
fatigue_4 = ['fatigue_4', 4000, 6000, 21500, 23000]
fatigue_5 = ['fatigue_5', 9500, 11000, 26500, 28000]
fatigue_6 = ['fatigue_6', 1600, 3100, 20000, 21500]
fatigue_7 = ['fatigue_7', 3800, 5300, 20300, 21800]

#control animals with normal blood flow
ctrl_6 = ['ctrl_6', 2000, 3500, 24500, 26000]
ctrl_7 = ['ctrl_7', 5000, 6500, 21500, 23000]
ctrl_8 = ['ctrl_8', 4000, 5500, 22500, 24000]
ctrl_9 = ['ctrl_9', 1600, 3100, 15100, 16600]

#control animals with ischemia due to clamps
ctrl_2 = ['ctrl_2', 100, 1600, 10733, 10806]
ctrl_3 = ['ctrl_3', 2000, 2739, 13000, 14000]
ctrl_4 = ['ctrl_4', 2500, 4000,20000, 20750]
ctrl_5 = ['ctrl_5', 4500, 6000, 4000+23760, 5500+23760]

def readData(args):
    filename = args[0]
    baselineStart = args[1]
    baselineEnd = args[2]
    finalStart = args[3]
    finalEnd = args[4]
    file = pd.read_csv(filename, delimiter='\t')


    baseline = file.pH[baselineStart:baselineEnd]
    final = file.pH[finalStart:finalEnd]

#because some files are saving the floats as string
    bsl =[float(x) for x in baseline]
    fnl = [float(x) for x in final]

    print np.mean(bsl)
    print np.mean(fnl)
    return "%r\t%r\t%r\n" %(filename,np.mean(bsl), np.mean(fnl))
    

output.write("Animal\tBaseline\tFinal\n")
output.write(readData(fatigue_3))
output.write(readData(fatigue_4))
output.write(readData(fatigue_5))
output.write(readData(fatigue_6))
output.write(readData(fatigue_7))
output.write('\n')
output.write(readData(ctrl_6))
output.write(readData(ctrl_7))
output.write(readData(ctrl_8))
output.write(readData(ctrl_9))
output.write('\n')
output.write(readData(ctrl_2))
output.write(readData(ctrl_3))
output.write(readData(ctrl_4))
output.write(readData(ctrl_5))


