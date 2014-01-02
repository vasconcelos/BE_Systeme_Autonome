import threading, sys, os, time, math
import serial
from Tkinter import*
import Tkinter
import tkMessageBox
from ScrolledText import *

#### Serial communication class (Thread)
class ManagerCommThread(threading.Thread):
    def __init__(self, threadID): ##redefine Thread constructor
        threading.Thread.__init__(self) ## call parent constructor
        self.threadID = threadID
        self.comm = SerialComm(9600,0.05)
        self.comm.findPort()
        s1.acquire()
        self.running = False
        s1.release()
        return

    def run(self):
        s1.acquire()
        self.running = True
        s1.release()
        app.text.insert(END, "Starting thread: " + self.threadID + "\n")
        j = 0
        while j < 1:
            x = self.comm.read()
            convert = ":".join("{0:x}".format(ord(c)) for c in x)
            s.release()
            s1.acquire()
            if self.running == False:
                j = 2
            s1.release()
        app.text.insert(END, "End of " + self.threadID + " thread\n")
        s1.acquire()
        app.threadsRunning = 0
        s1.release()
        del self
        return

    def stop(self):
        s1.acquire()
        self.running = False
        s1.release()


#### Serial communication configuration class
class SerialComm(serial.Serial):
    def __init__(self, baudrate, timeout):
        serial.Serial.__init__(self)
        self.baudrate = baudrate
        self.timeout= timeout
        self.port = 0
        return
    
    def findPort(self):
        port_founded = 0
        i = 0
        while port_founded < 1:
            i += 1
            try:
                self.open()
                port_founded = 2
            except:
                self.port = i
        return
    

## Control robot manager (Thread)
class RobotControl(threading.Thread):
    def __init__(self, threadID): ##redefine Thread constructor
        threading.Thread.__init__(self) ## call parent constructor
        self.threadID = threadID
        s1.acquire()
        self.running = False
        s1.release()
        s.acquire()
        return
    
    def run(self):
        s1.acquire()
        self.running = True
        s1.release()
        app.text.insert(END, "Starting thread: " + self.threadID + "\n")
        k = 0
        while k < 1:
            s1.acquire()
            if self.running == False:
                k = 2
                s1.release()
            else:
                s1.release()
                s.acquire()
                app.text.insert(END, "Converted value: %i\n"  %convert)
            if(convert == 0):
                app.can.itemconfigure(app.capt1,fill='black')
                app.can.itemconfigure(app.capt2,fill='black')
                app.can.itemconfigure(app.capt3,fill='black')
                app.can.itemconfigure(app.capt4,fill='black')
                
        app.text.insert(END, "End of " + self.threadID + " thread\n")
        s1.acquire()
        app.threadsRunning = 0
        s1.release()
        s.release()
        del self
        return

    def stop(self):
        s1.acquire()
        self.running = False
        s1.release()

## GUI configurations class
class Interface(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.pack()
        self.initializeGUI()
        self.threadsRunning = 0
        return

    def initializeGUI(self):
        f1 = Frame(self)
        f1.pack(side=LEFT,padx=5)
        self.START = Button(f1,text="START", bg = "green", command = self.start)
        self.START.pack(side=TOP,expand=YES,fill=BOTH)

        self.STOP = Button(f1,text="STOP", bg = "red", command = self.stop)
        self.STOP.pack(side=TOP,expand=YES,fill=BOTH)

        self.QUIT = Button(f1,text="QUIT", command = self.quit)       
        self.QUIT.pack(side=TOP,expand=YES,fill=BOTH)

        f2 = Frame(self)
        f2.pack(side = RIGHT,padx=5)
        
        self.label= Label(f2,text="STATUS OF THE SENSORS",font=('Helvetica',12,'italic bold'),foreground='blue')
        self.label.grid(row=0,column=1)
        #define and design the interface window(height,width,colour, etc.) 
        self.can = Canvas( f2, width=500, height=130,relief=SUNKEN, bd=2)
        self.can.grid(row=1,column=1)
        
        self.label = Label(f2,text="Message Box",font=('Helvetica',12,'italic bold'),foreground='blue')
        self.label.grid(row=2,column=1)
        self.text = ScrolledText(f2, width=80, height=15,background='white',spacing1=1, spacing2=1, tabs='24')
        self.text.grid(row=3,column=1)
        self.myLabel = Label(f2,text = "Software created and edited by Joao VASCONCELOS")
        self.myLabel.grid(row=4,column=1)
        self.myLabel1 = Label(f2,text = "Squares = IR sensors")
        self.myLabel1.grid(row=0,column=0)
        self.myLabel2 = Label(f2,text = "Cercle = Ultra son sensors")
        self.myLabel2.grid(row=1,column=0)
        
        # position of the sensors
        x = 250; y = 20
        dia= 20

        #create rectangles for the infra-red sensores along with circle for ultrasonic sensor
        self.capt4 = self.can.create_oval(x,y+60,x+dia,y+dia+60, fill='red',width=2)
        self.capt3 = self.can.create_rectangle(x-70,y,x+dia-70,y+dia, fill='red',width=2)
        self.capt2 = self.can.create_rectangle(x+70,y,x+dia+70,y+dia, fill='red',width=2)
        self.capt1 = self.can.create_rectangle(x,y,x+dia,y+dia,fill='red',width=2)
        return


    def initSystem(self):
        # Create new thread
        global thread1
        global thread2
        thread1 = ManagerCommThread("CommWatcher")
        thread2 = RobotControl("ControlRobot")
        self.threadsRunning = 1
    
    def start(self):
        s1.acquire()
        if self.threadsRunning == 0:
            s1.release()
            self.initSystem()
            thread1.start()
            thread2.start()
            app.text.insert(END, "Serial port found: " + thread1.comm.name + "\n")
            app.text.insert(END, "Thread " + thread1.threadID + " is ready\n")
            app.text.insert(END, "Thread " + thread2.threadID + " is ready\n")
        else:
            s1.release()
            self.text.insert(END, "All threads are already running\n")
        return

    def stop(self):
        s1.acquire()
        if self.threadsRunning == 1:
            s1.release()
            app.text.insert(END, "Stopping threads\n")
            thread1.stop()
            thread2.stop()
            thread1.comm.close()
        else:
            s1.release()
            self.text.insert(END, "All threads are already stopped\n")
        return

    def quit(self):
        s1.acquire()
        if app.threadsRunning == 1:
            s1.release()
            self.stop()
            time.sleep(2)

        s1.release()
        mainWindow.destroy()
        #app.destroy()
        return


## main app
convert = 0
s = threading.Semaphore()
s1 = threading.Semaphore()
mainWindow = Tk()
mainWindow.title("BE Systèmes Autonomes")
app = Interface(master = mainWindow)
app.text.insert(END, "Main app thread is ready\n")
app.mainloop()
if app.threadsRunning == 1:
    thread1.stop()
    thread2.stop()

#app.text.insert(END, "End of main app\n")
#app.destroy()