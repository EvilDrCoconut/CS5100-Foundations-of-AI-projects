import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plotData():

    data = []

    x = []

    pop = 1
    while pop < 101:
        x.append(pop)
        pop += 1

    pbminmax = []
    pbAlphaBeta = []
    pbBLuff = []

    pbMinMax_vs_pbBluff = []
    pbAlphaBeta_vs_pbBluff = []
    pbMinMax_vs_pbAlphaBeta = []

    # issue parsing csv file, copied to text and parsed from there
    file = open('data2.txt', 'r')
    
    n = 0
    while n < 6:

        for line in file.readlines():
            helper = line.split('=')
            #print(helper)
            datahelper = []
            for item in helper:
                item = item.replace('[', '')
                item = item.replace(']', '')
                try:
                    datahelper.append(int(item))
                except:
                    pass
            data.append(datahelper)
            #print(data)
        n += 1
    data[0].sort()
    print(len(x), len(data[0]))
    plt.scatter(x, data[0])
    plt.show()

def main():
    plotData()

main()