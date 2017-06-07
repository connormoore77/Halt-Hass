import serial
from ArduinoClass import Arduino
import decimal
import time
import minimalmodbus
import Reading as read

#need to check if everything works.
#may need to delete everything that is found in thermalControl and vibrationControl
#add check to see if we are at a safe temperature and a safe grms

"""
class Cylinders(object):
    def __init__(self,Cport):
        self.arduino = serial.Serial(Cport,9600)
        
    def setFrequency(self,frequency):
        if (frequency>50):
            print "Choose a frequency less than 50."
            return                

        deltaT = 500/frequency
        time.sleep(1)
        self.arduino.flush()
        self.arduino.write(str(deltaT))
        print 'Frequency Set.'
        
    def close(self):
        self.arduino.close()


class PropAir(object):
    def __init__(self,PAport,grmsArduinoPort='none'):
        self.ins = minimalmodbus.Instrument(PAport,247)
        self.ins.serial.parity = 'E'
        self.ins.serial.timeout = .160
        self.ins.serial.baudrate = 19200
        #Lines added by Dylan for the grms read
        if grmsArduinoPort != 'none' :
            self.grmsReader = serial.Serial(grmsArduinoPort,9600)
            self.grmsReader.timeout = 2

    def setPressure(self,pressure):
        val = pressure*655 #pressure is scaled by a fixed value to map to presure regulator
        self.ins.write_register(49,val)
                        
    def readPressure(self):
        return self.ins.read_register(49)/655
                
    def readGrms(self):
        try:
            dum = float(self.grmsReader.readline().strip())
        except ValueError:
            print("Data Fragment Dropped")
        try:
            val = float(self.grmsReader.readline().strip())
        except ValueError:
            print("Format Error")
            self.grmsReader.reset_input_buffer()
            val = readGrms()
        self.grmsReader.reset_input_buffer()
        return val
                
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
"""

rmsFile = "grmsLog.txt"

class cycleAll(PropAir, Cylinders, tenney):
    def __init__(self, PAport, Cport, grmsPort='none'):
        PropAir.__init__(self, PAport, grmsArduinoPort=grmsPort)
        Cylinders.__init__(self, Cport)
        tenney.__init__(self, ardport)
"""
    def setGrms(self, desiredGrms):
        #will need to be called in a loop with time.sleep()
        Shift1d = .005
        Shift2d = .02
        Shift3d = .04
        Shift1u = .006
        Shift2u = .023
        Shift3u =  .05

        smallDifference= .2
        mediumDifference = .5
        largeDifference = 1        

        grmsDifference = currentGrms - desiredGrms                                               
        if(grmsDifference > largeDifference):#large positive difference           
            pressure = pressure + Shift3d
            if pressure > 80:
                pressure = 80
            self.setPressure(pressure)
        elif(grmsDifference > mediumDifference):#medium positive difference
            pressure = pressure + Shift2d
            if pressure > 80:
                pressure = 80
            self.setPressure(pressure)
        elif(grmsDifference > smallDifference):#small positive difference               
            pressure = pressure + Shift1d
            if pressure > 80:
                pressure = 80
            self.setPressure(pressure)          
        elif(grmsDifference < smallDifference):#small negative difference
            pressure = pressure - Shift1u
            if pressure < 1:
                pressure = 1
            self.setPressure(pressure)                    
        elif(grmsDifference < mediumDifference):#medium negative difference                          
            pressure = pressure - Shift2u
            if pressure < 1:
                pressure=1 
            self.setPressure(pressure)
        elif(grmsDifference < largeDifference):#large negative difference                                        
            pressure = pressure - Shift3u
            if pressure < 1:
                pressure=1  
            self.setPressure(pressure)

    def waitInPlace(self,seconds):
        waitTime = int(seconds/3)#why is this divided by 3?
        for x in range(1,waitTime):
            time.sleep(1)#in seconds
            currentTemperature = self.arduino.readTemperature()#temperature read from thermistor
            print 'Maintaining temperature. Current temperature is %r degrees C' % (currentTemperature) 
        time.sleep(1)
"""

    def setTemperature(self,setTemperature):
        #self.setTemperature = setTemperature
        decimal.getcontext().prec = 1 #keeps values to 1 decimal place
        chamberInput = "= SP1 " + str(decimal.Decimal(setTemperature)) + "\n"
        try:
            self.chamber.write(chamberInput)
        except:
            print "Missed setTemperature Handshake"
            self.close()
            time.sleep(1)
            self.open()

    def grmsCycling(self, startGrms,numberOfGrmsSteps,grmsStepSize, timeToWaitAtGrmsStep, startTemperature, numberOfTemperatureSteps, temperatureStepSize,numberOfCycles, frequency):
        if round(numberOfCycles,1) != round(numberOfCycles,0)+0.0:
            raise RuntimeError('Use only integer values for Number of Cycles.') 
        #startTime = time.time()
        self.setFreq(frequency)
        self.setPressure(1)#have the pressure start low
        grmsAcceptance = .2
        temperatureAcceptance = 5        
        timeToWait = timeToWaitAtGrmsStep*60 #convert to minutes
        stopGrms = startGrms + grmsStepSize*numberOfGrmsSteps
        stopTemperature = startTemperature + temperatureStepSize*numberOfTemperatureSteps
        #begin cycling
        for cycle in range(1,numberOfCycles+1):              
            for tempStep in range(0, numberOfTemperatureSteps+1):
                setTemperature = startTemperature + tempStep*temperatureStepSize
                currentTemperature = self.arduino.readTemperature()
                while (abs(currentTemperature - setTemperature) > temperatureAcceptance):
                    print 'Adjusting Temperature to ' + str(setTemperature) + '. Currently ' + str(currentTemperature)
                    self.setTemperature(setTemperature)
                    currentTemperature = self.arduino.readTemperature()
                    if (currentTemperature < -272):
                        self.theramlChamberError()
                    time.sleep(1)
                    #print currentTemperature
                print 'Set Temperature Reached'
                for grmsStep in range(0,numberOfGrmsSteps+1):
                    setGrms = startGrms + grmsStep*GrmsStepSize
                    print 'Adjusting Grms to ' + str(setGrms)
                    self.setGrms(setGrms)
                    time.sleep(1)
                    currentGrms = read.readGrms(grmsLog)               
                    while (abs(currentGrms - setGrms) > grmsAcceptance:                                
                        print 'Current grms is ' + currentGrms +'. Adjusting Setpoint to ' + str(setTemperature)
                        self.setGrms(setGrms)                            
                        time.sleep(1)
                    print 'Set Grms Reached'
                    timeToEnd = time.time() + timeToWait
                    #Keep grms at certain level
                    while time.time() < timeToEnd:
                        currentGrms = read.readGrms(grmsLog)
                        print 'Current grms is ' + currentGrms + '. Current temperature is ' + str(self.arduino.readTemperature()) + '.' 
                        if(abs(currentGrms - setGrms) > grmsAcceptance):#keep calling to maintian grms
                            self.setGrms(setGrms)
                        if(abs(currentTemperature - setTemperature) > temperatureAcceptance):
                            print 'Adjusting Temperature to ' + str(setTemperature) + '. Currently ' + str(currentTemperature)
                            self.setTemperature(setTemperature)
                            currentTemperature = self.arduino.readTemperature()
                            if (currentTemperature < -272):
                                self.theramlChamberError()
                        time.sleep(1)
                print 'Finished grms step ' + str(grmsStep) + ' out of ' + str(numberOfGrmsSteps) + '.'                   
            print 'Cycle ' + str(i) + ' of ' + str(cycle) + ' is complete.'
        print 'Finished cycling. Setting Pressure 0 Psi.'
        self.setPressure(0)
        print 'Setting frequency to 1 Hz.'
        self.setFreq(1)
        print 'Setting temperature to 20 degrees C.'
        self.setTemperature(20)
        self.close()