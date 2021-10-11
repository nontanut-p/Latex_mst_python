from serial import Serial
import statistics
import sys
import keyboard
import time
import numpy as np
import math
import matplotlib.pyplot as plt

### SETUP VARIABLE ###
short = 30  # short moving Average period
long = 150  # long moving Average period
macdThreshold = 1.25
## LOADCELL & LASER VARIABLE#
laserRawData = []
loadcellRawData = []
#############################
## MACD VARIABLE ########
## MST TIME     ########
#############################
#############################

laserShortMA = []
loadShortMA = []
laserLongMA = []
loadLongMA = []
laserMACD = []
laserMACD_MA = []
loadMACD = []
loadMACD_MA = []
laserMST = []
loadMST = []


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


def macD(maShort, maLong, lenght):
    return maShort[lenght] - maLong[lenght]
#############################


waittime = 100
laserMSTcount = 0
loadcellMSTcount = 0


def realtimePlot(lenght):
    global short, long, macdThreshold, laserRawData, loadcellRawData, laserMSTcount, loadcellMSTcount
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
# fix program ??  add macd loadcell and edit plotting time moving average by append zeros until long
        print(lenght, 'lenght')

        if len(loadMACD_MA) > 0:

            mylenght = len(loadMACD_MA) - 1
            #print(mylenght, 'test')
            #print(loadMACD_MA[mylenght], 'yeahh')
            print("mylenght=" + str(mylenght) +
                  ", len(loadMACD_MA)=" + str(len(loadMACD_MA)))
            if laserMACD_MA[mylenght] >= macdThreshold and laserMSTcount == waittime:
                ax[1].axvline(x=(lenght - short - long),
                              color='darkred', lw=2)
                laserMSTcount = 0
            if laserMACD_MA[mylenght] >= macdThreshold and laserMSTcount < waittime:
                laserMSTcount = laserMSTcount + 1
                print(laserMSTcount, 'MST COUNT')
            if laserMACD_MA[mylenght] < macdThreshold:
                laserMSTcount = 0

            if loadMACD_MA[mylenght] >= macdThreshold and loadcellMSTcount == waittime:
                ax[2].axvline(x=(lenght - short - long),
                              color='darkgreen', lw=2)
                loadcellMSTcount = 0
            if loadMACD_MA[mylenght] < macdThreshold:
                loadcellMSTcount = 0
            if loadMACD_MA[mylenght] >= macdThreshold and loadcellMSTcount < waittime:
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


def main():
    global short, long, laserRawData, loadcellRawData
    # แก้ Serial Port , Baudrate 
    ser = Serial('COM4', 57600, timeout=0)
    serialString = ''

    f = open("raw_data.txt", 'w')
    f.writelines("START : 0000")
    f.close()

    while True:
        if keyboard.is_pressed('Esc'):
            #
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
                    while True:
                        if not dataSplit[1][-1].isdigit():
                            dataSplit[1] = dataSplit[1][:-1]
                        else:
                            break
                    #print(dataSplit[1])
                    laserRawData.append(float(dataSplit[0])) # Data ชุดหน้า 
                    loadcellRawData.append(float(dataSplit[1])) # Data ชุดหลัง
                    if len(loadcellRawData) != len(laserRawData):
                        print('ERROR!!')
                        break    
                    lenght = len(loadcellRawData)
                    if len(laserRawData) <= long:  # 10
                        ax[0].plot(loadcellRawData, color='green')
                        ax[0].plot(laserRawData, color='red')
                        print('laser', laserRawData)
                        print('load', loadcellRawData)
                        # here append loadcell macd
                        loadMACD_MA.append(0)
                        laserMACD_MA.append(0)
                        ax[2].plot(loadMACD_MA, color='lime')
                        fig.canvas.draw()
                        plt.pause(0.001)
                        debug.writelines('< long')
                    if len(laserRawData) > long:  # 10
                        debug.writelines('> long')
                        realtimePlot(lenght)
            debug.close()
    f.close()


if __name__ == '__main__':
    main()
