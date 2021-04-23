import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plotData():

    data = []

    pbminmax = []
    pbAlphaBeta = []
    pbBLuff = []

    pbMinMax_vs_pbBluff = []
    pbAlphaBeta_vs_pbBluff = []
    pbMinMax_vs_pbAlphaBeta = []

    file = open('data.txt', 'r')
    
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
                    print('whatever')
            data.append(datahelper)
            print(data)
            n += 1

    plt.scatter(x = 150, y = data[0])
    plt.show()

def main():
    plotData()

main()