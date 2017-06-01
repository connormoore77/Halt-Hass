import serial
from ArduinoClass import Arduino
import decimal
import time

#add data logging

class tenney(object):
    #initialize class to control thermal chamber
    def __init__(self,com,ardport):
        #chamber appears to be serial port for thermal chamber
        self.chamber = serial.Serial(com,baudrate=9600,timeout=1)
        self.arduino = Arduino(ardport)
    
    def close(self):
        self.chamber.close()
        self.arduino.comm.close()

    def open(self):
        self.chamber.open()
        self.arduino.comm.open()

    def waitInPlace(self,seconds):
        waitTime = int(seconds/3)#why is this divided by 3?
        for x in range(1,waitTime):
            time.sleep(1)#in seconds
            currentTemperature = self.arduino.readTemperature()#temperature read from thermistor
            print 'Maintaining temperature at %r degrees C' % (ntcTemp) 
            print currentTemperature
        time.sleep(1)

    def setTemperature(self,setTemperature):
        self.setTemperature = setTemperature
        decimal.getcontext().prec = 1 #keeps values to 1 decimal place
        chamberInput = "= SP1 " + str(decimal.Decimal(setTemperature)) + "\n"
        try:
            self.chamber.write(chamberInput)
        except:
            print "Missed setTemperature Handshake"
            self.close()
            time.sleep(1)
            self.open()

    def theramlChamberError(self):
        self.arduino.comm.close()
        time.sleep(1)
        try:
            self.arduino.comm.open()
        except:
            print "Thermal chamber error. Shutdown."
            self.setTemperature(23)
            self.arduino.comm.close()
            time.sleep(1)
            self.arduino.comm.open()
            print self.arduino.comm
            self.arduino.readTemperature()
        #self.close()


    def thermalCycling(self,startTemperature,numberOfSteps,stepSize,timeToWaitAtStep,numberOfCycles):
        if round(numberOfCycles,1) != round(numberOfCycles,0)+0.0:
            raise RuntimeError('Use only integer values for Number of Cycles.') 
        #startTime = time.time()
        timeToWait = timeToWaitInPlace*60 #convert to minutes
        temperatureAcceptance = 5
        stopTemperature = startTemperature + stepSize*numberOfSteps

        #begin thermal cycling
        for cycle in range(1,numberOfCycles+1):            
            for step in range(0, numberOfSteps):
                setTemperature = startTemperature + step*stepSize
                print 'Adjusting Temperature to ' + str(setTemperature)
                self.setTemperature(setTemperature)
                time.sleep(1)
                currentTemperature = self.arduino.readTemperature()
                if (currentTemperature < -272):
                    self.theramlChamberError()                
                print currentTemperature
                while (abs(currentTemperature - setTemperature) > temperatureAcceptance):
                    time.sleep(1)
                    print 'Adjusting Setpoint to ' + str(setTemperature)
                    self.setTemperature(setTemperature)
                    currentTemperature = self.arduino.readTemperature()
                    if (currentTemperature < -272):
                        self.theramlChamberError()
                    print currentTemperature                
                print 'Set Temperature Reached'
                self.soak(timeToWaitAtStep)                                
            print 'Cycle ' + str(i) + ' of ' + str(cycle) + ' is complete.'
        print 'Finished thermal cycling. Setting tmeperature to 23 degrees C.'
        self.setTemperature(23)