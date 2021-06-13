import serial
import statistics
import sys
import keyboard
import time
import numpy as np
import math
import matplotlib.pyplot as plt

#
#
ser = serial.Serial('COM4', 57600, timeout=0)
### SETUP VARIABLE ###
short = 3  # short moving Average period
long = 15  # long moving Average period
macdThreshold = 1.25
## LOADCELL & LASER VARIABLE#
laserRawData = []
loadcellRawData = []
laserShortMA = []
loadShortMA = []
laserLongMA = []
loadLongMA = []
#############################
## MACD VARIABLE ########
laserMACD = []
laserMACD_MA = []
loadMACD = []
loadMACD_MA = []
## MST TIME     ########
laserMST = []
loadMST = []
laserMSTcount = 50
loadcellMSTcount = 50
#############################
serialString = ''
#############################


def macD(maShort, maLong, lenght):
    return maShort[lenght] - maLong[lenght]
#############################


def plot():
    # fig, ax = plt.subplots(3)
    # plt.show()
    plt.pause(0.01)


plot()
fig, ax = plt.subplots(3)
fig.set_size_inches(12, 6)
ax[0].set_ylim(0, 70)

ax[1].set_ylim(-2, 3)
ax[2].set_ylim(-2, 3)
ax[1].axhline(y=1, color='r', linestyle='-')
ax[1].axhline(y=0, color='b', linestyle='-')
ax[2].axhline(y=1, color='r', linestyle='-')
ax[2].axhline(y=0, color='b', linestyle='-')


def realtimePlot(lenght):
    try:
        global laserMSTcount, loadcellMSTcount
        # 11
        # FOR SHORT
        laserShortMA.append(statistics.mean(
            laserRawData[lenght - short: lenght]))
        loadShortMA.append(statistics.mean(
            loadcellRawData[lenght - short: lenght]))
        # FOR LONG
        laserLongMA.append(statistics.mean(
            laserRawData[lenght - long: lenght]))
        loadLongMA.append(statistics.mean(
            loadcellRawData[lenght - long: lenght]))
        # FIND MACD

        macdlenght = len(laserLongMA)
        laserMACD.append(
            laserShortMA[macdlenght - 1] - laserLongMA[macdlenght - 1])
        loadMACD.append(loadShortMA[macdlenght - 1] -
                        loadLongMA[macdlenght - 1])
        if len(loadLongMA) > short:
            lenlenght = len(loadLongMA)
            laserMACD_MA.append(statistics.mean(
                laserMACD[lenlenght - short: lenlenght]))
            loadMACD_MA.append(statistics.mean(
                loadMACD[lenlenght - short: lenlenght]))

            print(lenght, 'lenght')
            if len(loadMACD_MA) > 0:

                mylenght = len(loadMACD_MA) - 1
                print(mylenght, 'test')
                print(loadMACD_MA[mylenght], 'yeahh')
                if laserMACD_MA[mylenght] >= macdThreshold and laserMSTcount == 50:
                    ax[1].axvline(x=(lenght - short - long),
                                  color='darkred', lw=2)
                    laserMSTcount = 0
                if laserMSTcount < 50:
                    laserMSTcount = laserMSTcount + 1

                if loadMACD_MA[mylenght] >= macdThreshold and loadcellMSTcount == 50:
                    ax[2].axvline(x=(lenght - short - long),
                                  color='darkgreen', lw=2)
                    loadcellMSTcount = 0
                if loadcellMSTcount < 50:
                    loadcellMSTcount = loadcellMSTcount + 1
                ## CHECKED MST ##
                # plot Graph
                # fig, ax = plt.subplots(3)
                # plot AX[0] MA30 MA150 RAWDATA

        ax[0].plot(laserRawData, color='red', lw=0.5)
        ax[0].plot(laserShortMA, color='deeppink', lw=0.5)
        ax[0].plot(laserLongMA, color='darkred', lw=0.5)

        ax[0].plot(loadcellRawData, color='green', lw=0.5)
        ax[0].plot(loadShortMA, color='lime', lw=0.5)
        ax[0].plot(loadLongMA, color='darkgreen', lw=0.5)

        ax[0].legend(["LASER",  "LASER: : MA " + str(short), "LASER :  MA " + str(long), "LOADCELL",
                     "LOADCELL: : MA " + str(short), "LOADCELL :  MA " + str(long)], loc="lower right")
        # plot AX[1] Laser MACD
        ax[1].plot(laserMACD_MA, color='red')
        ax[1].legend(['LASER MACD'], loc="lower right")
        print(loadMACD_MA)
        # plot AX[2] LOAD CELL MACD
        ax[2].plot(loadMACD_MA, color='lime')
        ax[2].legend(['LOADCELL MACD'], loc="lower right")
        fig.canvas.draw()

        plt.pause(0.01)
    except:
        print('error')


f = open("raw_data.txt", 'w')
f.writelines("START : 0000")
f.close()
while True:
    try:
        if keyboard.is_pressed('Esc'):
            fig.savefig('figure.png', dpi=400)
            plt.close()
            break
        if ser.in_waiting > 0:
            tmp = ser.read().decode("Ascii")
            serialString = serialString + tmp
            f = open("raw_data.txt", 'a')
            debug = open('debug.txt', 'a')

            f.writelines(tmp)
            f.close()
            start = serialString.find("START")
            if(start != -1):
                end = serialString[start:].find("STOP")
                if(end != -1):
                    rawData = serialString[start+11:end]
                    serialString = ''
                    dataSplit = rawData.split('+')
                    laserRawData.append(float(dataSplit[0]))
                    loadcellRawData.append(float(dataSplit[1]))
                    print(loadcellRawData)
                    print(laserRawData)
                    if len(loadcellRawData) != len(laserRawData):
                        print('ERROR!!')
                        break
                    print(rawData)
                    lenght = len(loadcellRawData)
                    print(lenght)
                    if len(loadcellRawData) and len(laserRawData) <= long:  # 10
                        ax[0].plot(loadcellRawData, color='green')
                        ax[0].plot(laserRawData, color='red')
                        print('laser', laserRawData)
                        print('load', loadcellRawData)
                        fig.canvas.draw()
                        plt.pause(0.001)
                        debug.writelines('< long')
                    if len(loadcellRawData) and len(laserRawData) > long:  # 10
                        debug.writelines('> long')
                        realtimePlot(lenght)
            debug.close()
    except:
        print('something error!!')
        pass
f.close()
