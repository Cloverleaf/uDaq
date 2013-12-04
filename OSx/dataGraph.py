#a quick and dirty script for pulling the pH data and graphing it
#requires tab delimited data with labeled columns

import pandas as ultimate_lab_sidekick_army
import matplotlib.pyplot as plt

plt.figure()
def makeGraphs():    
    filename = raw_input("Data file to graph: ")
    data = ultimate_lab_sidekick_army.read_csv(filename, delimiter="\t")
    plt.plot(data.pH)
    
    if raw_input("Another graph? Y or N: ") == "Y":
        makeGraphs()
    else:
        return "Graphs completed"


print makeGraphs()

plt.show()