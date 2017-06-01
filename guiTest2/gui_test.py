#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter
import time
import threading,Queue
import logging
import datetime
import tenney
import vibration
import os
#import Writing

#Notes
#Add kill button and stop button
#add additional fields for cycle functions
#add vacuum chuck status
#add threaded moduals, changeFreq, changePressure, changeTemp, setGrms
#Add plotting 
#Save data and plots
#add checks to see if entered a value or entered the right type of value
#add a way to exit loops
#add updating fields to gui

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

class HALTHASS(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

#Frequesncy, pressure, temperature##############################################        
                        
        #initialize frequency gui components
        self.labelManual = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelManual,
                              anchor="w",fg="white",bg="black")
        label.grid(column=0,row=1,columnspan=3,sticky='EW')
        self.labelManual.set(u"MANUAL CONTROLS")

        #Box to input new frequency
        self.enterFrequency = Tkinter.StringVar()
        self.entryF = Tkinter.Entry(self,textvariable=self.enterFrequency)
        self.entryF.grid(column=0,row=2,sticky='EW')
        #self.entry.bind("<Return>", self.OnPressEnter)
        #self.enterFrequency.set(u"Enter Frequency (Hz)")#Initial text in Frequency box

        #Update frequency button
        self.buttonFrequency = Tkinter.Button(self,text=u"Update Frequency",
                                command=self.OnButtonClickFrequency)
        self.buttonFrequency.grid(column=1,row=2)

        #display current frequency
        self.labelFrequency = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelFrequency,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=3,columnspan=2,sticky='EW')
        self.labelFrequency.set(u"Enter Frequency (Hz)")

        #initialize pressure gui components
        #Box to input new pressure
        self.enterPressure = Tkinter.StringVar()
        self.entryP = Tkinter.Entry(self,textvariable=self.enterPressure)
        self.entryP.grid(column=0,row=4,sticky='EW')
        #self.enterPressure.set(u"Enter Pressure (Psi)")#Initial text in Pressure box

        #Update pressure button
        self.buttonPressure = Tkinter.Button(self,text=u"Update Pressure",
                                command=self.OnButtonClickPressure)
        self.buttonPressure.grid(column=1,row=4)

        #display current Pressure
        self.labelPressure = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelPressure,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=5,columnspan=2,sticky='EW')
        self.labelPressure.set(u"Enter Pressure (Psi)")

        #initialize temperature gui components
        #Box to input new temperature
        self.enterTemperature = Tkinter.StringVar()
        self.entryT = Tkinter.Entry(self,textvariable=self.enterTemperature)
        self.entryT.grid(column=0,row=7,sticky='EW')
        #self.enterTemperature.set(u"Enter Temperature (C)")#Initial text in temperature box

        #Update temperature button
        self.buttonTemperature = Tkinter.Button(self,text=u"Update Temperature",
                                command=self.OnButtonClickTemperature)
        self.buttonTemperature.grid(column=1,row=7)

        #display current temperature
        self.labelTemperature = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelTemperature,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=8,columnspan=2,sticky='EW')
        self.labelTemperature.set(u"Enter Temperature (C)")

        #Control Setting 
        self.radioCycle = Tkinter.Radiobutton(self,text = 'Cycle',value=0,command = self.setCycle)
        self.radioCycle.grid(column=1,row=0)
        self.radioManual = Tkinter.Radiobutton(self,text = 'Manual',value=1,command = self.setManual)
        self.radioManual.grid(column=0,row=0)

###################Grms#########################################################

        #Box to input new grms
        self.enterGrms = Tkinter.StringVar()
        self.entryG = Tkinter.Entry(self,textvariable=self.enterGrms)
        self.entryG.grid(column=0,row=10,sticky='EW')
        #self.enterGrms.set(u"Enter Grms")#Initial text in temperature box

        #Update grms button
        self.buttonGrms = Tkinter.Button(self,text=u"Update Grms",
                                command=self.OnButtonClickGrms,state='active')
        self.buttonGrms.grid(column=1,row=10)
                        
        self.labelGrms = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelGrms,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=11
        ,columnspan=2,sticky='EW')
        self.labelGrms.set(u"Enter Grms")

######################Cycle#####################################################
        self.labelCycle = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelCycle,
                              anchor="w",fg="white",bg="black")
        label.grid(column=0,row=12,columnspan=3,sticky='EW')
        self.labelCycle.set(u"CYCLE CONTROLS")

        self.labelThermal = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelThermal,
                              anchor="w",fg="white",bg="black")
        label.grid(column=0,row=13,columnspan=3,sticky='EW')
        self.labelThermal.set(u"Thermal Chamber Cycle Settings")

        #set low temperature
        self.enterLowTemp = Tkinter.StringVar()
        self.entryLT = Tkinter.Entry(self,textvariable=self.enterLowTemp,state='disable')
        self.entryLT.grid(column=0,row=14,sticky='EW')
        #self.enterLowTemp.set(u"Enter Low Temperature")

        #display low temperature set point
        self.labelLowTemperature = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelLowTemperature,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=14,columnspan=2,sticky='EW')
        self.labelLowTemperature.set(u"Enter Low Temperature (C)")

        #set high temperature
        self.enterHighTemp = Tkinter.StringVar()
        self.entryHT = Tkinter.Entry(self,textvariable=self.enterHighTemp,state='disable')
        self.entryHT.grid(column=0,row=15,sticky='EW')
        #self.enterHighTemp.set(u"Enter High Temperature")

        #display high temperature set point
        self.labelHighTemperature = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelHighTemperature,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=15,columnspan=2,sticky='EW')
        self.labelHighTemperature.set(u"Enter High Temperature (C)")
              
        #set number of steps between low and high temperatures 
        self.enterSteps = Tkinter.StringVar()
        self.entryS = Tkinter.Entry(self,textvariable=self.enterSteps,state='disable')
        self.entryS.grid(column=0,row=16,sticky='EW')
        #self.enterSteps.set(u"Enter Number of Steps")

        #display number of steps between temperatures
        self.labelSteps = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelSteps,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=16,columnspan=2,sticky='EW')
        self.labelSteps.set(u"Enter Number of Steps")
        
        #set time to sit at each temp
        self.enterSetTime = Tkinter.StringVar()
        self.entryST = Tkinter.Entry(self,textvariable=self.enterSetTime,state='disable')
        self.entryST.grid(column=0,row=17,sticky='EW')
        #self.enterSetTime.set(u"Enter Time to Sit at Each Step")

        #display set time
        self.labelSetTime = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelSetTime,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=17,columnspan=2,sticky='EW')
        self.labelSetTime.set(u"Enter Set Time (min)")

        #set number of cycles
        self.enterNumCycles = Tkinter.StringVar()
        self.entryNC = Tkinter.Entry(self,textvariable=self.enterNumCycles,state='disable')
        self.entryNC.grid(column=0,row=18,sticky='EW')
        #self.enterNumCycles.set(u"Enter Time to Sit at Each Step")

        #display set time
        self.labelNumCycles = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelNumCycles,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=18,columnspan=2,sticky='EW')
        self.labelNumCycles.set(u"Enter Number of Cycles")        

        self.labelVibration = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVibration,
                              anchor="w",fg="white",bg="black")
        label.grid(column=0,row=19,columnspan=3,sticky='EW')
        self.labelVibration.set(u"Vibration Cycle Settings")

        #set vibration step size
        self.enterVibStepSize = Tkinter.StringVar()
        self.entryVSS = Tkinter.Entry(self,textvariable=self.enterVibStepSize,state='disable')
        self.entryVSS.grid(column=0,row=20,sticky='EW')        

        #display vibration step size
        self.labelVibStepSize = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVibStepSize,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=20,columnspan=2,sticky='EW')
        self.labelVibStepSize.set(u"Enter Step Size")

        #set start grms
        self.enterVibStartGrms = Tkinter.StringVar()
        self.entryVSG = Tkinter.Entry(self,textvariable=self.enterVibStartGrms,state='disable')
        self.entryVSG.grid(column=0,row=21,sticky='EW')

        #display start grms
        self.labelStartGrms = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelStartGrms,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=21,columnspan=2,sticky='EW')
        self.labelStartGrms.set(u"Enter Start Grms")
              
        #set step length
        self.enterVibStepLength = Tkinter.StringVar()
        self.entryVSL = Tkinter.Entry(self,textvariable=self.enterVibStepLength,state='disable')
        self.entryVSL.grid(column=0,row=22,sticky='EW')

        #display step length
        self.labelVibStepLength = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVibStepLength,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=22,columnspan=2,sticky='EW')
        self.labelVibStepLength.set(u"Enter Step Length")
        
        #set number of steps
        self.enterVibNumberOfSteps = Tkinter.StringVar()
        self.entryVNS = Tkinter.Entry(self,textvariable=self.enterVibNumberOfSteps,state='disable')
        self.entryVNS.grid(column=0,row=23,sticky='EW')

        #display number of steps
        self.labelVibNumberOfSteps = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVibNumberOfSteps,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=23,columnspan=2,sticky='EW')
        self.labelVibNumberOfSteps.set(u"Enter Number of Steps")

        #set frequency
        self.enterVibFrequency = Tkinter.StringVar()
        self.entryVF = Tkinter.Entry(self,textvariable=self.enterVibFrequency,state='disable')
        self.entryVF.grid(column=0,row=24,sticky='EW')

        #display frequency
        self.labelVibFrequency = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVibFrequency,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=1,row=24,columnspan=2,sticky='EW')
        self.labelVibFrequency.set(u"Enter Frequency (Hz)")

############start stop cycle buttons############################################
        
        #Start cycle with given values 
        self.buttonStartCycle = Tkinter.Button(self,text=u"Start Cycle",
                                command=self.OnButtonClickStartCycle, state='disable')
        self.buttonStartCycle.grid(column=0,row=25)
        
        #Stop cycle 
        self.buttonStopCycle = Tkinter.Button(self,text=u"Stop Cycle",
                                command=self.OnButtonClickStopCycle, state='disable')
        self.buttonStopCycle.grid(column=1,row=25)


##############Pane resize settings##############################################
        self.grid_columnconfigure(0,weight=1)
        #self.grid_columnconfigure(1,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())       
        #self.entryF.focus_set()
        #self.entryF.selection_range(0, Tkinter.END)

    
##############Define what buttons do############################################

    #Update frequency button definition 
    def OnButtonClickFrequency(self):
        self.labelFrequency.set("Current frequency: " + self.enterFrequency.get() + " Hz")
        self.entryF.focus_set()
        self.entryF.selection_range(0, Tkinter.END)
        vib = vibration.VibrationCycling('COM4','COM5')
        vib.changeFreq(int(self.enterFrequency.get()))

    #def OnPressEnter(self,event):
     #   self.labelVariable.set( self.entryVariable.get())#+" (You pressed ENTER)" )
      #  self.entry.focus_set()
       # self.entry.selection_range(0, Tkinter.END)

    #Update Pressure button definition
    def OnButtonClickPressure(self):
        self.labelPressure.set("Current Pressure: " + self.enterPressure.get() + " Psi")
        self.entryP.focus_set()
        self.entryP.selection_range(0, Tkinter.END)
        vib = vibration.VibrationCycling('COM4','COM5')
        vib.setPressure(int(self.enterPressure.get()))

    #Update temperature button definition        
    def OnButtonClickTemperature(self):
        self.labelTemperature.set("Current Temperature: " + self.enterTemperature.get() + " C")
        self.entryT.focus_set()
        self.entryT.selection_range(0, Tkinter.END)
        oven = tenney.Tenney('COM7','COM3')
        oven.setPoint(float(self.enterTemperature.get()))

    #Update grms button definition        
    def OnButtonClickGrms(self):
        self.labelGrms.set("Current Grms: " + self.enterGrms.get())
        self.entryG.focus_set()
        self.entryG.selection_range(0, Tkinter.END)

    #Put control in manual        
    def setManual(self):
        self.buttonFrequency.config(state='normal')
        self.buttonPressure.config(state='normal')
        self.buttonTemperature.config(state='normal')
        self.buttonGrms.config(state='normal')        
        self.entryP.config(state='normal')
        self.entryF.config(state='normal')
        self.entryT.config(state='normal')
        self.entryG.config(state='normal')
        self.entryNC.config(state='disable')
        self.entryLT.config(state='disable')
        self.entryHT.config(state='disable')
        self.entryS.config(state='disable')
        self.entryST.config(state='disable')
        self.buttonStartCycle.config(state='disable')
        self.entryVF.config(state='disable')
        self.entryVNS.config(state='disable')
        self.entryVSG.config(state='disable')
        self.entryVSL.config(state='disable')
        self.entryVSS.config(state='disable')
                
    #Put control in cycle        
    def setCycle(self):
        self.entryF.config(state='disable')
        self.buttonFrequency.config(state='disable')
        self.buttonPressure.config(state='disable')
        self.buttonTemperature.config(state='disable')
        self.buttonGrms.config(state='disable')        
        self.entryP.config(state='disable')
        self.entryT.config(state='disable')
        self.entryG.config(state='disable')
        self.buttonStartCycle.config(state='normal')
        self.entryNC.config(state='normal')
        self.entryLT.config(state='normal')
        self.entryHT.config(state='normal')
        self.entryS.config(state='normal')
        self.entryST.config(state='normal')
        self.entryVF.config(state='normal')
        self.entryVNS.config(state='normal')
        self.entryVSG.config(state='normal')
        self.entryVSL.config(state='normal')
        self.entryVSS.config(state='normal')

    #Start cycle button definition        
    def OnButtonClickStartCycle(self):        
        self.entryNC.config(state='disable')
        self.entryLT.config(state='disable')
        self.entryHT.config(state='disable')
        self.entryS.config(state='disable')
        self.entryST.config(state='disable')
        self.radioCycle.config(state='disable')
        self.radioManual.config(state='disable')
        self.buttonStopCycle.config(state='normal')
        self.buttonStartCycle.config(state='disable')
        #vib = vibration.VibrationCycling('COM4','COM5')
        oven = tenney.Tenney('COM7','COM3')
        #thread1 = threading.Thread(target=vib.cycle, args=[self.enterVibStepSize,self.enterVibStartGrms,self.enterVibStepLength,self.enterVibNumberOfSteps,self.enterVibFrequency])
        thread2 = threading.Thread(target=oven.cycle, args=[float(self.enterHighTemp.get()),float(self.enterLowTemp.get()),int(self.enterSteps.get()),int(self.enterSetTime.get()),int(self.enterNumCycles.get())])
        #thread3 = threading.Thread(target=os.system('python Writing.py'))
        #thread1.start()
        thread2.start()
        #thread3.start()

    #Stop cycle button definition        
    def OnButtonClickStopCycle(self):
        #self.entryNC.config(state='normal')
        #self.entryLT.config(state='normal')
        #self.entryHT.config(state='normal')
        #self.entryS.config(state='normal')
        #self.entryST.config(state='normal')
        #self.radioCycle.config(state='normal')
        #self.radioManual.config(state='normal')
        #self.buttonStartCycle.config(state='normal')
        self.buttonStopCycle.config(state='disable')     
        #thread1.stop()
        #thread2.stop()                   
                                                
                                                                                                
########################main####################################################

if __name__ == "__main__":
    app = HALTHASS(None)
    app.title('HALT/HASS Controls')
    app.mainloop()
    