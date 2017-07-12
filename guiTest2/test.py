#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import mtTkinter as Tkinter#TKinter is not thread safe, mtTkinter fixes this.
import time
import threading
#import logging,Queue
import datetime
import thermalControl
import vibrationControl
import cyclingControl
import os
from sys import executable
from subprocess import Popen, CREATE_NEW_CONSOLE

#Notes
#add vacuum chuck status
#add checks to see if entered a value or entered the right type of value

class HALTHASS(Tkinter.Tk):
    #If something is not right, kill everything.
    #add checks for vacuum chuck, temperature out of range, grms out of range, etc.
    if(1==2):
        os.sysytem("kill.cmd")

    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        
###########################    Manual components    ##############################################        
        #initialize frequency gui components
        self.labelManual = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelManual,anchor="w",fg="white",bg="black")
        label.grid(column=0,row=1,columnspan=3,sticky='EW')
        self.labelManual.set(u"MANUAL CONTROLS")

        #Box to input new frequency
        self.enterFrequency = Tkinter.StringVar()
        self.entryF = Tkinter.Entry(self,textvariable=self.enterFrequency)
        self.entryF.grid(column=0,row=2,sticky='EW')
        #self.entry.bind("<Return>", self.OnPressEnter)
        #self.enterFrequency.set(u"Enter Frequency (Hz)")#Initial text in Frequency box
        #Update frequency button
        self.buttonFrequency = Tkinter.Button(self,text=u"Update Frequency",width = 22,command=self.OnButtonClickFrequency)
        self.buttonFrequency.grid(column=1,row=2)
        #display current frequency
        self.labelFrequency = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelFrequency,anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=3,columnspan=2,sticky='EW')
        self.labelFrequency.set(u"Enter Frequency (Hz)")
        #Box to input new pressure
        self.enterPressure = Tkinter.StringVar()
        self.entryP = Tkinter.Entry(self,textvariable=self.enterPressure)
        self.entryP.grid(column=0,row=4,sticky='EW')
        #self.enterPressure.set(u"Enter Pressure (Psi)")#Initial text in Pressure box
        #Update pressure button
        self.buttonPressure = Tkinter.Button(self,text=u"Update Pressure",width = 22,command=self.OnButtonClickPressure)
        self.buttonPressure.grid(column=1,row=4)
        #display current Pressure
        self.labelPressure = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelPressure,anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=5,columnspan=2,sticky='EW')
        self.labelPressure.set(u"Enter Pressure (Psi)")
        #Box to input new temperature
        self.enterTemperature = Tkinter.StringVar()
        self.entryT = Tkinter.Entry(self,textvariable=self.enterTemperature)
        self.entryT.grid(column=0,row=7,sticky='EW')
        #self.enterTemperature.set(u"Enter Temperature (C)")#Initial text in temperature box
        #Update temperature button
        self.buttonTemperature = Tkinter.Button(self,text=u"Update Temperature",width = 22,command=self.OnButtonClickTemperature)
        self.buttonTemperature.grid(column=1,row=7)
        #display current temperature
        self.labelTemperature = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelTemperature,anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=8,columnspan=2,sticky='EW')
        self.labelTemperature.set(u"Enter Temperature (C)")

        #Control Setting 
        self.radioCycle = Tkinter.Radiobutton(self,text = 'Cycle',value=0,command = self.setCycle)
        self.radioCycle.grid(column=1,row=0)
        self.radioManual = Tkinter.Radiobutton(self,text = 'Manual',value=1,command = self.setManual)
        self.radioManual.grid(column=0,row=0)

        ######################    Cycle Components    #####################################################
        ##########################    Thermal settings    #################################################
        self.labelCycle = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelCycle,anchor="w",fg="white",bg="black")
        label.grid(column=0,row=12,columnspan=3,sticky='EW')
        self.labelCycle.set(u"CYCLE CONTROLS")
        self.labelThermal = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelThermal,anchor="w",fg="white",bg="black")
        label.grid(column=0,row=13,columnspan=3,sticky='EW')
        self.labelThermal.set(u"Thermal Chamber Cycle Settings")
        #set start temperature
        self.enterStartTemperature = Tkinter.StringVar()
        self.entryThermST = Tkinter.Entry(self,textvariable=self.enterStartTemperature,state='disable')
        self.entryThermST.grid(column=0,row=14,sticky='EW')
        #display start temperature set point
        self.labelStartTemperature = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelStartTemperature,anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=14,columnspan=2,sticky='EW')
        self.labelStartTemperature.set(u"Enter Start Temperature (C)")
        #set number of steps between low and high temperatures 
        self.enterSteps = Tkinter.StringVar()
        self.entryS = Tkinter.Entry(self,textvariable=self.enterSteps,state='disable')
        self.entryS.grid(column=0,row=15,sticky='EW')
        #self.enterSteps.set(u"Enter Number of Steps")
        #display number of steps between temperatures
        self.labelSteps = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelSteps,anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=15,columnspan=2,sticky='EW')
        self.labelSteps.set(u"Enter Number of Steps")
        #set step size
        self.enterThermStepSize = Tkinter.StringVar()
        self.entryThermSS = Tkinter.Entry(self,textvariable=self.enterThermStepSize,state='disable')
        self.entryThermSS.grid(column=0,row=16,sticky='EW')
        #display thermal chamber step size
        self.labelThermStepSize = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelThermStepSize,anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=16,columnspan=2,sticky='EW')
        self.labelThermStepSize.set(u"Enter Step Size (C)")
        #set time to sit at each temp
        self.enterSetTime = Tkinter.StringVar()
        self.entryST = Tkinter.Entry(self,textvariable=self.enterSetTime,state='disable')
        self.entryST.grid(column=0,row=17,sticky='EW')
        #self.enterSetTime.set(u"Enter Time to Sit at Each Step")
        #display set time
        self.labelSetTime = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelSetTime,anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=17,columnspan=2,sticky='EW')
        self.labelSetTime.set(u"Enter Set Time (min)")
        #set number of cycles
        self.enterNumCycles = Tkinter.StringVar()
        self.entryNC = Tkinter.Entry(self,textvariable=self.enterNumCycles,state='disable')
        self.entryNC.grid(column=0,row=18,sticky='EW')
        #self.enterNumCycles.set(u"Enter Time to Sit at Each Step")
        #display set time
        self.labelNumCycles = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelNumCycles,anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=18,columnspan=2,sticky='EW')
        self.labelNumCycles.set(u"Enter Number of Cycles")        

        #################    Vibration settings    ##############################################################
        self.labelVibration = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVibration,anchor="w",fg="white",bg="black")
        label.grid(column=0,row=19,columnspan=3,sticky='EW')
        self.labelVibration.set(u"Vibration Cycle Settings")
        #set start grms
        self.enterVibStartGrms = Tkinter.StringVar()
        self.entryVSG = Tkinter.Entry(self,textvariable=self.enterVibStartGrms,state='disable')
        self.entryVSG.grid(column=0,row=20,sticky='EW')
        #display start grms
        self.labelStartGrms = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelStartGrms,anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=20,columnspan=2,sticky='EW')
        self.labelStartGrms.set(u"Enter Start Grms")
        #set number of steps
        self.enterVibNumberOfSteps = Tkinter.StringVar()
        self.entryVNS = Tkinter.Entry(self,textvariable=self.enterVibNumberOfSteps,state='disable')
        self.entryVNS.grid(column=0,row=21,sticky='EW')
        #display number of steps
        self.labelVibNumberOfSteps = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVibNumberOfSteps,anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=21,columnspan=2,sticky='EW')
        self.labelVibNumberOfSteps.set(u"Enter Number of Steps")
        #set vibration step size
        self.enterVibStepSize = Tkinter.StringVar()
        self.entryVSS = Tkinter.Entry(self,textvariable=self.enterVibStepSize,state='disable')
        self.entryVSS.grid(column=0,row=22,sticky='EW')        
        #display vibration step size
        self.labelVibStepSize = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVibStepSize,anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=22,columnspan=2,sticky='EW')
        self.labelVibStepSize.set(u"Enter Step Size (Psi)")
        #set time to wait
        self.enterVibStepLength = Tkinter.StringVar()
        self.entryVSL = Tkinter.Entry(self,textvariable=self.enterVibStepLength,state='disable')
        self.entryVSL.grid(column=0,row=23,sticky='EW')
        #display time to wait
        self.labelVibStepLength = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVibStepLength,anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=23,columnspan=2,sticky='EW')
        self.labelVibStepLength.set(u"Enter time to wait at each step")
        #set number of cycles
        self.enterVibNumberOfCycles = Tkinter.StringVar()
        self.entryVNC = Tkinter.Entry(self,textvariable=self.enterVibNumberOfCycles,state='disable')
        self.entryVNC.grid(column=0,row=24,sticky='EW')
        #display number of steps
        self.labelVibNumberOfCycles = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVibNumberOfCycles,anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=24,columnspan=2,sticky='EW')
        self.labelVibNumberOfCycles.set(u"Enter Number of Cycles")
        #set frequency
        self.enterVibFrequency = Tkinter.StringVar()
        self.entryVF = Tkinter.Entry(self,textvariable=self.enterVibFrequency,state='disable')
        self.entryVF.grid(column=0,row=25,sticky='EW')
        #display frequency
        self.labelVibFrequency = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVibFrequency, anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=25,columnspan=2,sticky='EW')
        self.labelVibFrequency.set(u"Enter Frequency (Hz)")

############    start stop cycle buttons    ############################################
        #Start cycle with given values 
        self.buttonStartCycle = Tkinter.Button(self,text=u"Start Cycle",command=self.OnButtonClickStartCycle, state='disable')
        self.buttonStartCycle.grid(column=0,row=26)
        #Stop cycle 
        self.buttonStopCycle = Tkinter.Button(self,text=u"Kill All",command=self.OnButtonClickStopCycle, state='disable')
        self.buttonStopCycle.grid(column=1,row=26)

##############    Define what buttons do    ############################################
    #Update frequency button definition 
    #def OnPressEnter(self,event):
    #  self.labelVariable.set( self.entryVariable.get())#+" (You pressed ENTER)" )
    #  self.entry.focus_set()
    #  self.entry.selection_range(0, Tkinter.END)
    def OnButtonClickFrequency(self):
        #self.labelFrequency.set("Current frequency: " + self.enterFrequency.get() + " Hz")
        self.entryF.focus_set()
        self.entryF.selection_range(0, Tkinter.END)
        try:
            vib = vibrationControl.vibrationCycling('COM4','COM5')
            vib.setFrequency(float(self.enterFrequency.get()))
        except:
            print 'ERROR: Unable to set frequency.'
    #Update Pressure button definition
    def OnButtonClickPressure(self):
        #self.labelPressure.set("Current Pressure: " + self.enterPressure.get() + " Psi")
        self.entryP.focus_set()
        self.entryP.selection_range(0, Tkinter.END)
        try:
            vib = vibrationControl.vibrationCycling('COM4','COM5')
            vib.setPressure(float(self.enterPressure.get()))
        except:
            print 'ERROR: Unable to set pressure.'
    #Update temperature button definition        
    def OnButtonClickTemperature(self):
        #self.labelTemperature.set("Current Temperature: " + self.enterTemperature.get() + " C")
        self.entryT.focus_set()
        self.entryT.selection_range(0, Tkinter.END)
        try:
            oven = thermalControl.tenney('COM7','COM3')
            oven.setTemperature(float(self.enterTemperature.get()))
        except:
            print 'ERROR: Unable to set temperature. Try again.'

    #Put control in manual        
    def setManual(self):
        self.buttonFrequency.config(state='normal')
        self.buttonPressure.config(state='normal')
        self.buttonTemperature.config(state='normal')   
        self.entryP.config(state='normal')
        self.entryF.config(state='normal')
        self.entryT.config(state='normal')
        self.entryNC.config(state='disable')
        self.entryThermSS.config(state='disable')
        self.entryThermST.config(state='disable')
        self.entryS.config(state='disable')
        self.entryST.config(state='disable')
        self.entryVF.config(state='disable')
        self.entryVNC.config(state='disable')
        self.entryVNS.config(state='disable')
        self.entryVSG.config(state='disable')
        self.entryVSL.config(state='disable')
        self.entryVSS.config(state='disable')
        self.buttonStartCycle.config(state='disable')
    #Put control in cycle        
    def setCycle(self):
        self.entryF.config(state='disable')
        self.buttonFrequency.config(state='disable')
        self.buttonPressure.config(state='disable')
        self.buttonTemperature.config(state='disable')        
        self.entryP.config(state='disable')
        self.entryT.config(state='disable')
        self.buttonStartCycle.config(state='normal')
        self.entryNC.config(state='normal')
        self.entryNC.config(state='normal')
        self.entryThermSS.config(state='normal')
        self.entryThermST.config(state='normal')
        self.entryS.config(state='normal')
        self.entryST.config(state='normal')
        self.entryVF.config(state='normal')
        self.entryVNC.config(state='normal')
        self.entryVNS.config(state='normal')
        self.entryVSG.config(state='normal')
        self.entryVSL.config(state='normal')
        self.entryVSS.config(state='normal')

    #Stop cycle button definition        
    def OnButtonClickStopCycle(self):
        os.sysytem("kill.cmd")#kills everything

    #Start cycle button definition        
    def OnButtonClickStartCycle(self):      
        self.buttonStartCycle.config(state='disable')
        self.entryNC.config(state='disable')
        self.entryNC.config(state='disable')
        self.entryThermSS.config(state='disable')
        self.entryThermST.config(state='disable')
        self.entryS.config(state='disable')
        self.entryST.config(state='disable')
        self.entryVF.config(state='disable')
        self.entryVNC.config(state='disable')
        self.entryVNS.config(state='disable')
        self.entryVSG.config(state='disable')
        self.entryVSL.config(state='disable')
        self.entryVSS.config(state='disable')  
        #vib = vibrationControl.vibrationCycling('COM4','COM5')
        #thread = threading.Thread(target=vib.grmsCycling, args=[10,5,10,2,2,7])
        #thread = threading.Thread(target=oven.thermalCycling, args=[40,3,2,1,2])
        #oven = thermalControl.thermalCycling('COM7','COM3')
        #thread = threading.Thread(target=vib.grmsCycling, args=[int(self.enterVibStartGrms.get()),int(self.enterVibNumberOfSteps.get()),int(self.enterVibStepSize.get()),int(self.enterVibStepLength.get()),int(self.enterVibNumberOfCycles.get()),int(self.enterVibFrequency.get())])
        #thread = threading.Thread(target=oven.cycle, args=[float(self.enterStartTemperature.get()),float(self.enterSteps.get()),int(self.enterThermStepSize.get()),int(self.enterSetTime.get()),int(self.enterNumCycles.get())])
        Popen([executable, 'Writing.py'], creationflags=CREATE_NEW_CONSOLE)
        cycleObject = cyclingControl.cycleAll('COM4','COM5','COM7','COM3') 
        #thread = threading.Thread(target=cycleObject.grmsCycling, args=[5,1,25,1,21,0,1,1,2])
        #startGrms, numberOfGrmsSteps, grmsStepSize, timeToWaitAtGrmsStep, 
        #startTemperature, numberOfTemperatureSteps, temperatureStepSize, numberOfCycles, frequency
        thread = threading.Thread(target=cycleObject.grmsCycling, args=[25,0,5,30,-40,18,5,1,2])

        thread.start()

                     
                                                                                                
########################    MAIN    ####################################################
if __name__ == "__main__":
    app = HALTHASS(None)
    app.title('HALT/HASS Controls')
    app.mainloop()
    