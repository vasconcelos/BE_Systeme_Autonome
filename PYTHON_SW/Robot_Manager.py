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
        self.comm = SerialComm(9600,2)
        self.comm.findPort()
        s1.acquire()
        self.running = True
        s1.release()
        print "Thread " + self.threadID + " ready\n"
        #app.text.insert(END, "Thread1 is ready")
        return

    def run(self):
        print "Thread " + self.threadID + " starting\n"
        #app.text.insert(END, "Starting" + self.threadID)
        j = 0
        while j < 5:
            j += 1
            x = self.comm.read()
            convert = ":".join("{0:x}".format(ord(c)) for c in x)
            print(self.comm.inWaiting())
            s.release()
            s1.acquire()
            if self.running == False:
                j = 10
            s1.release()
        self.comm.close()
        print "End of thread: " + self.threadID
        #app.text.insert((END, "End of thread1"), self.threadID) 
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
        if self.isOpen():
            self.close()
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
        print "Serial port found :" + self.name
        #app.text.insert(END, "Serial port found: " + self.name)
        #app.text.insert(END, "Serial COM openned? " + self.isOpen())
        return
    

## Control robot manager (Thread)
class RobotControl(threading.Thread):
    def __init__(self, threadID): ##redefine Thread constructor
        threading.Thread.__init__(self) ## call parent constructor
        self.threadID = threadID
        s1.acquire()
        self.running = True
        s1.release()
        print "Thread " + self.threadID + " ready\n"
        #app.text.insert(END,"Thread " + self.threadID + "ready")
        s.acquire()
        return
    
    def run(self):
        print "Thread " + self.threadID + " starting\n"
        #app.text.insert(END, "Starting" + self.threadID)
        k = 0
        while k < 2:
            k += 1
            if self.running == False:
                k = 10
                s1.release()
            else:
                s.acquire()
                print "Read value: ", convert
                app.text.insert(END, "Converted value: %i\n"  %convert)
        #app.text.insert(END, "End of " + self.threadID + "thread")
        print "End of thread: " + self.threadID
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
        #self.initSystem()
        return

    def initializeGUI(self):
        f1 = Frame(self)
        f1.pack(side=LEFT,padx=5)
        self.START = Button(f1,text="START", bg = "green")#, command = self.start)
        self.START.pack(side=TOP,expand=YES,fill=BOTH)

        self.STOP = Button(f1,text="STOP", bg = "red")#, command = self.stop)
        self.STOP.pack(side=TOP,expand=YES,fill=BOTH)

        self.QUIT = Button(f1,text="QUIT")#, command = self.stop)       
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
        self.capt4 = self.can.create_oval(x,y+60,x+dia,y+dia+60, fill='dark olive green',width=2)
        self.capt3 = self.can.create_rectangle(x-70,y,x+dia-70,y+dia, fill='red',width=2)
        self.capt2 = self.can.create_rectangle(x+70,y,x+dia+70,y+dia, fill='red',width=2)
        self.capt1 = self.can.create_rectangle(x,y,x+dia,y+dia,fill='red',width=2)
        return


    def initSystem(self):
        pass
    
    def start(self):
        self.thread1.start()
        self.thread2.start()


## main app
convert = 0
s = threading.Semaphore()
s1 = threading.Semaphore()
# Create new thread
thread1 = ManagerCommThread("CommWatcher")
thread2 = RobotControl("ControlRobot")
thread1.start()
thread2.start()
mainWindow = Tk()
mainWindow.title("BE Systèmes Autonomes")
app = Interface(master = mainWindow)
app.mainloop()
#app.destroy()
thread1.stop()
thread2.stop()

print("End of main app")