import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import serial as sr

baudrates = [110, 300, 600, 1200, 2400, 4800, 9600,
             14400, 19200, 38400, 57600, 115200, 128000, 256000]
# ----------- Global Variable
myPort = ''
baudrate = 115200  # Default
data_front = []
data_back = []


def connect():
    global s
    s = sr.Serial(myPort, baudrate)
    s.reset_input_buffer()
    print(myPort, baudrate)


def plot_data():
    global cond
    if cond == True:
        a = s.readline()
        a.decode('Ascii')

# https://thepoorengineer.com/en/python-gui/


def serial_ports():
    return serial.tools.list_ports.comports()


# Every time after user click on the start button the program will automatically create an emtpy file for record log
# Name of the file is a current datetime
serialString = ''
status = True


def start_program(root):
    if status == True:
        try:
            s = sr.Serial(myPort, baudrate)
            s.reset_input_buffer()
        except:
            pass

        global serialString

        a = s.read().decode()
        serialString = serialString + a
        print(serialString)
        '''
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
                # print(dataSplit[1])
                data_front.append(float(dataSplit[0]))  # Data ชุดหน้า
                data_back.append(float(dataSplit[1]))  # Data ชุดหลัง

        '''
        root.after(10, start_program(root))


def reload_port(root):
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    cb = ttk.Combobox(root, values=serial_ports())
    cb.grid(row=1, column=1, ipadx="100")


def stop_plotting():
    global status
    if status == True:
        status = False
    else:
        status = True
    print(status)


def on_select(event=None):
    # get selection from event
    global myPort
    portName = event.widget.get()
    st = portName.find('(')
    ed = portName.find(')')
    myPort = portName[st+1:ed]
    print("change port to: ", myPort)


def on_select_bb(event=None):

    # get selection from event
    global baudrate
    baudrate = event.widget.get()
    print(event.widget.get())
    print("change baudrate to : ", baudrate)


def main():

    root = tk.Tk()
    root.title('--- LATEX MST ---')
    root.configure(background='ivory2')
    root.geometry("1200x700")

    cond = 0

    # Parameter Plot Selection : 1) DATA FRONT, BACK 2 ) RAW DATA 3) FILTER FOR RAW 4) SMA FOR SHORT 5) SMA FOR LONG 6) MACD 7) TIME FOR START DETECTION   ,
    fig = Figure()
    ax = fig.add_subplot(111)

    ax.set_title('LATEX Mechanical Stability Time Detection')
    ax.set_xlabel('TIME (s)')
    ax.set_ylabel('Distance (mm)')
    ax.set_ylim(0, 60)
    lines = ax.plot([], [])[0]

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().place(x=1, y=20, width=800, height=500)
    canvas.draw()

    serialString = ''

    connect = 0

    # Button
    root.update()
    start = tk.Button(root, text='START', command=lambda: start_program(root))
    start.place(x=300, y=600)
    root.update()
    stop = tk.Button(root, text='RESET', command=lambda: stop_plotting())
    stop.place(x=400, y=600)

    reload = tk.Button(root, text='Reload', command=lambda:  reload_port(root)).grid(
        row=1, column=3, ipadx="10")

    # TEXT

    cb = ttk.Combobox(root, values=serial_ports())
    cb_br = ttk.Combobox(root, values=baudrates)
    cb.grid(row=1, column=1, ipadx="100")
    cb_br.grid(row=1, column=2, ipadx="100")

    # assign function to combobox
    cb.bind('<<ComboboxSelected>>', on_select)
    cb_br.bind('<<ComboboxSelected>>', on_select_bb)

    root.mainloop()


if __name__ == '__main__':
    main()
