from collections.abc import Callable, Iterable, Mapping
import tkinter as tk
from tkinter import ttk
from typing import Any
from ttkthemes import ThemedTk
import threading
import time
import queue
import serial

# Create a thread to manage pulling rx-ed serial data into a buffer
class SerialThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    #Open a serial port and pipe data to queue
    def run(self, portPath, baudrate):
        sp = serial.Serial(portPath, baudrate=baudrate)
        #sp.write("")
        time.sleep(1) #Give things a bit of time to settle
        while True:
            if sp.in_waiting():
                line = sp.readline(sp.in_waiting())
                self.queue.put(line)

# Create a ui
class App:
    def __init__(self, root):
        root.title("Debug Tool")
        width = 600
        height = 480
        #align the created window to the center of the string, and bring to the front
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        align = '%dx%d+%d+%d' % (width, height, (screenWidth - width) / 2, (screenHeight - height) / 2)
        root.geometry(align)
        #root.resizeable(width=False,height=False)
        root.lift()

        #Start Creating the window features
        tabCtrl = ttk.Notebook(root)

        #Notebook tabs - Note: They must have features to render
        tab1 = ttk.Frame(tabCtrl)
        tabCtrl.add(tab1, text="tab1")
        tab2 = ttk.Frame(tabCtrl)
        tabCtrl.add(tab2, text="tab2")
        SerCom = ttk.Frame(tabCtrl)
        tabCtrl.add(SerCom, text="Serial Connection")

        tabCtrl.pack(expand=1, fill="both")

        #Tab1 Features
        ttk.Label(tab1, text="tab1").grid(column=0, row=0, padx=5, pady=5)

        #Tab2 Features
        ttk.Label(tab2, text="tab2").grid(column=0, row=0, padx=5, pady=5)

        #Serial Comm Features
        connButton = ttk.Button(SerCom, text="Connect",command=self.ConnectButton)
        connButton.place(x=520,y=10,width=70,height=30)

        portEntry = ttk.Entry(SerCom, text="Enter Serial Port")

    def ConnectButton(self):
        pass


if __name__ == "__main__":
    root = ThemedTk(theme="adapta")
    app = App(root)
    root.mainloop()
