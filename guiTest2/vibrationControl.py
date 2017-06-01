import serial 
import minimalmodbus
import time
import Reading as read

rmsFile = "grmsLog.txt"
        
class Cylinders(object):
    def __init__(self,Cport):
        self.arduino = serial.Serial(Cport,9600)
        
    def setFrequency(self,frequency):
        if (frequency>50):
            print "Choose a frequency less than 50."
            return                

        deltaT = 500/frequency
        print deltaT
        time.sleep(1)
        self.arduino.flush()
        self.arduino.write(str(deltaT))
        
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
                
                        
class VibrationCycling(PropAir, Cylinders):
    def __init__(self, PAport, Cport, grmsPort='none'):
        PropAir.__init__(self, PAport, grmsArduinoPort=grmsPort)
        Cylinders.__init__(self, Cport)
        
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
                        
                        

    def grmsCycling(self, startGrms,numberOfSteps,stepSize,timeToWaitAtStep,numberOfCycles, frequency):
        if round(numberOfCycles,1) != round(numberOfCycles,0)+0.0:
            raise RuntimeError('Use only integer values for Number of Cycles.') 
        #startTime = time.time()
        self.setFreq(frequency)
        self.setPressure(1)#have the pressure start low
        grmsAcceptance = .2        
        timeToWait = timeToWaitInPlace*60 #convert to minutes
        temperatureAcceptance = 5
        stopTemperature = startTemperature + stepSize*numberOfSteps
        
        #begin vibration cycling cycling
        for cycle in range(1,numberOfCycles+1):            
            for step in range(0, numberOfSteps):
                setGrms = startGrms + step*stepSize
                print 'Adjusting Grms to ' + str(setGrms)
                self.setGrms(setGrms)
                time.sleep(1)
                currentGrms = read.readGrms(grmsLog)               
                while (abs(currentGrms - setGrms) > grmsAcceptance):                    
                    print 'Current grms is ' + currentGrms +'. Adjusting Setpoint to ' + str(setTemperature)
                    self.setGrms(setGrms)
                    currentTemperature = self.arduino.readTemperature()               
                    time.sleep(1)
                print 'Set Grms Reached'
                timeToEnd = time.time() + timeToWait
                #Keep grms at certain level
                while time.time() < timeToEnd:
                    currentGrms = read.readGrms(grmsLog)
                    print 'Current grms is ' + currentGrms + '.' 
                    if(abs(currentGrms - setGrms) > grmsAcceptance):#keep calling to maintian grms
                        self.setGrms(setGrms)
                    time.sleep(1)                               
            print 'Cycle ' + str(i) + ' of ' + str(cycle) + ' is complete.'
        print 'Finished vibration cycling. Setting Pressure 0 Psi.'
        self.setPressure(0)