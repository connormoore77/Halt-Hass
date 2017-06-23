import serial
from ArduinoClass import Arduino
import decimal
import time
import minimalmodbus
import Reading as read
#import thermalControl, vibrationControl

#need to check if everything works.

class Cylinders(object):
    def __init__(self, Cport):
        self.ard = serial.Serial(Cport, 9600)

    def setFrequency(self, frequency):
        if frequency > 50:
            print "Choose a frequency less than 50."
            return
        deltaT = 500/frequency
        time.sleep(1)
        self.ard.flush()
        self.ard.write(str(deltaT))
        print 'Frequency Set.'

    def close(self):
        self.ard.close()


class PropAir(object):
    def __init__(self, PAport, grmsArduinoPort='none'):
        self.ins = minimalmodbus.Instrument(PAport, 247)
        self.ins.serial.parity = 'E'
        self.ins.serial.timeout = .160
        self.ins.serial.baudrate = 19200

    def setPressure(self, pressure):
        val = pressure*655 #pressure is scaled by a fixed value to map to presure regulator
        self.ins.write_register(49, val)

    def readPressure(self):
        return self.ins.read_register(49)/655

    #def guessPressure(self,targetGrms):
        #the equation below was determined by fitting grms vs pressure.
        #returns approximate required pressure to get a target grms
        #return .0002*targetGrms*targetGrms*targetGrms*targetGrms - .0084*targetGrms*targetGrms*targetGrms + .1839*targetGrms*targetGrms  - 1.0125*targetGrms + 9.7998
        #return .0005*targetGrms**4-.0252*targetGrms**3+.4538*targetGrms**2-2.5732*targetGrms+12.62
        #return .0004*targetGrms**4-.0293*targetGrms**3+.7402*targetGrms**2-6.3215*targetGrms+24.129#three hammers test 1
        #return .00002*targetGrms**4-.0016*targetGrms**3+.0527*targetGrms**2+0.109*targetGrms+7.4121#three hammers test 2
        #return -.0002*targetGrms**4+.0085*targetGrms**3-.1106*targetGrms**2+1.069*targetGrms+6.366#three hammers test 3
        

    def setGrms(self, currentGrms, desiredGrms):
        #will need to be called in a loop with time.sleep()
        Shift1d = .005
        Shift2d = .02
        Shift3d = .04
        Shift4d = .1
        Shift5d = .2
        Shift1u = .006
        Shift2u = .023
        Shift3u =  .05
        Shift4u =  .1
        Shift5u =  .2

        smallDifference = .2
        mediumDifference = .5
        largeDifference = 1.0

        grmsDifference = desiredGrms - currentGrms
        if grmsDifference > 3 and desiredGrms > 10:   
            print '-1'
            self.pressure = self.pressure + Shift5d
            if self.pressure > 80:
                self.pressure = 80
            self.setPressure(self.pressure)
        elif grmsDifference > 2 and desiredGrms > 10:   
            print '0'
            self.pressure = self.pressure + Shift4d
            if self.pressure > 80:
                self.pressure = 80
            self.setPressure(self.pressure)
        elif grmsDifference > largeDifference:#large positive difference   
            print '1'
            self.pressure = self.pressure + Shift3d
            if self.pressure > 80:
                self.pressure = 80
            self.setPressure(self.pressure)
        elif grmsDifference > mediumDifference:#medium positive difference
            print '2'
            self.pressure = self.pressure + Shift2d
            if self.pressure > 80:
                self.pressure = 80
            self.setPressure(self.pressure)
        elif grmsDifference > smallDifference:#small positive difference   
            print '3'
            self.pressure = self.pressure + Shift1d
            if self.pressure > 80:
                self.pressure = 80
            self.setPressure(self.pressure)         
        elif grmsDifference < -1*3:
            self.pressure = self.pressure - Shift5u
            if self.pressure < 1:
                self.pressure = 1
            self.setPressure(self.pressure)
        elif grmsDifference < -1*2:
            print '7'
            self.pressure = self.pressure - Shift4u
            if self.pressure < 1:
                self.pressure = 1
            self.setPressure(self.pressure)
        elif grmsDifference < -1*largeDifference:#large negative difference 
            print '6'
            self.pressure = self.pressure - Shift3u
            if self.pressure < 1:
                self.pressure = 1
            self.setPressure(self.pressure) 
        elif grmsDifference < -1*mediumDifference:#medium negative difference 
            print '5'
            self.pressure = self.pressure - Shift2u
            if self.pressure < 1:
                self.pressure = 1
            self.setPressure(self.pressure)
        elif grmsDifference < -1*smallDifference:#small negative difference
            print '4'
            self.pressure = self.pressure - Shift1u
            if self.pressure < 1:
                self.pressure = 1.0
            self.setPressure(self.pressure)
        #print 'function pressure is ' +str(self.pressure) +'. Current Grms is ' + str(currentGrms)
                
class tenney(object):
    #initialize class to control thermal chamber
    def __init__(self, com, ardport):
        #chamber appears to be serial port for thermal chamber
        self.chamber = serial.Serial(com, baudrate=9600, timeout=1)
        self.arduino = Arduino(ardport)

    def close(self):
        self.chamber.close()
        self.arduino.comm.close()

    def open(self):
        self.chamber.open()
        self.arduino.comm.open()

    def waitInPlace(self, seconds):
        waitTime = int(seconds/3)#why is this divided by 3?
        for x in range(1, waitTime):
            time.sleep(1)#in seconds
            currentTemperature = self.arduino.readTemperature()#temperature read from thermistor
            print 'Maintaining temperature. Current temperature is %r degrees C' % (currentTemperature)
        time.sleep(1)



grmsLog = "grmsLog.txt"

class cycleAll(PropAir, Cylinders, tenney):
    def __init__(self, PAport, Cport, com, ardport):
        PropAir.__init__(self, PAport)
        Cylinders.__init__(self, Cport)
        tenney.__init__(self, com, ardport)

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

    def setTemperature(self, setTemperature):
        decimal.getcontext().prec = 1 #keeps values to 1 decimal place
        chamberInput = "= SP1 " + str(decimal.Decimal(setTemperature)) + "\n"
        try:
            self.chamber.write(chamberInput)
        except:
            print "Missed setTemperature Handshake"
            self.close()
            time.sleep(1)
            self.open()

    def grmsCycling(self, startGrms, numberOfGrmsSteps, grmsStepSize, timeToWaitAtGrmsStep, startTemperature, numberOfTemperatureSteps, temperatureStepSize, numberOfCycles, frequency):
        if round(numberOfCycles, 1) != round(numberOfCycles, 0)+0.0:
            raise RuntimeError('Use only integer values for Number of Cycles.')
        #startTime = time.time()
        self.setFrequency(frequency)
        self.pressure = 5.0
        #self.pressure = guessPressure(startGrms)#sets pressure to pressure given approximate equation
        self.setPressure(self.pressure)#start at a low pressure while temperatuer is adjusting
        grmsAcceptance = .2
        temperatureAcceptance = 50
        timeToWait = timeToWaitAtGrmsStep*60 #convert to minutes
        #stopGrms = startGrms + grmsStepSize*numberOfGrmsSteps#can be used to make the program cycle in revearse.
        #stopTemperature = startTemperature + temperatureStepSize*numberOfTemperatureSteps
        #begin cycling
        for cycle in range(1, numberOfCycles+1):
            for tempStep in range(0, numberOfTemperatureSteps+1):
                setTemperature = startTemperature + tempStep*temperatureStepSize
                currentTemperature = self.arduino.readTemperature()
                while abs(currentTemperature - setTemperature) > temperatureAcceptance:
                    print 'Adjusting Temperature to ' + str(setTemperature) + '. Currently ' + str(currentTemperature)
                    self.setTemperature(setTemperature)
                    currentTemperature = self.arduino.readTemperature()
                    if (currentTemperature < -272):
                        self.theramlChamberError()
                    time.sleep(2)
                    #print currentTemperature
                print 'Set Temperature Reached'
                for grmsStep in range(0, numberOfGrmsSteps+1):
                    setGrms = startGrms + grmsStep*grmsStepSize
                    #setGrms = stopGrms - grmsStep*grmsStepSize
                    print 'Adjusting Grms to ' + str(setGrms)
                    #self.pressure = self.guessPressure(setGrms)#sets pressure to pressure given approximate equation
                    #self.setPressure(self.pressure)
                    #time.sleep(2)
                    currentGrms = read.readGrms(grmsLog)
                    twice = False
                    while abs(currentGrms - setGrms) > grmsAcceptance or not twice:
                        print str(twice)
                        print 'Current grms is ' + str(currentGrms) +' Adjusting Setpoint to ' + str(setGrms)
                        print 'Current Pressure is ' +str(self.pressure) + ' Current temperature is ' + str(self.arduino.readTemperature())
                        self.setGrms(currentGrms, setGrms)
                        if abs(currentTemperature - setTemperature) > temperatureAcceptance:
                            print 'Adjusting Temperature to ' + str(setTemperature) + '. Currently ' + str(currentTemperature)
                            self.setTemperature(setTemperature)
                            currentTemperature = self.arduino.readTemperature()
                            if currentTemperature < -272:
                                self.theramlChamberError()
                        if abs(currentGrms - setGrms) < grmsAcceptance + .2:
                            twice = True
                        else:
                            twice = False
                        time.sleep(2)
                        currentGrms = read.readGrms(grmsLog)
                    print 'Set Grms Reached'
                    timeToEnd = time.time() + timeToWait
                    #Keep grms at certain level
                    while time.time() < timeToEnd:
                        currentGrms = read.readGrms(grmsLog)
                        print 'Current grms is ' + str(currentGrms)
                        print 'Current Pressure is ' +str(self.pressure) + ' Current temperature is ' + str(self.arduino.readTemperature())
                        if abs(currentGrms - setGrms) > grmsAcceptance + .1:#keep calling to maintian grms
                            self.setGrms(currentGrms, setGrms)
                        if abs(currentTemperature - setTemperature) > temperatureAcceptance:
                            print 'Adjusting Temperature to ' + str(setTemperature) + '. Currently ' + str(currentTemperature)
                            self.setTemperature(setTemperature)
                            currentTemperature = self.arduino.readTemperature()
                            if currentTemperature < -272:
                                self.theramlChamberError()
                        time.sleep(2)
                print 'Finished grms step ' + str(grmsStep) + ' out of ' + str(numberOfGrmsSteps) + '.'
            print 'Cycle ' + str(cycle) + ' of ' + str(cycle) + ' is complete.'
        print 'Finished cycling. Setting Pressure 0 Psi.'
        self.setPressure(0)
        print 'Setting frequency to 1 Hz.'
        self.setFrequency(1)
        print 'Setting temperature to 20 degrees C.'
        self.setTemperature(20)
        self.close()