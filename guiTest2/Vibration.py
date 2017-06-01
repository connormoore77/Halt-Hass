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
        
        def setGrms(self, Grms, length):
                self.Grms = Grms
                self.length = t
                
                pressure = 1                    
                t_end = time.time() + (60 * t)
                while time.time() < t_end:
                        x = g.getGrms(rmsFile)
                        if (( x < (Grms - 1)) and (x > (Grms - 3))):
                                pressure = pressure +1
                                if pressure > 80:
                                        pressure = 80
                                self.setPressure(pressure)
                                time.sleep(1)
                        elif ((x > (Grms + 1)) and (x < (Grms + 3))):
                                pressure = pressure - 1
                                if pressure < 1:
                                        pressure = 1
                                self.setPressure(pressure)
                                time.sleep(1)
                        elif ((x > (Grms + 3))):
                                pressure = pressure -3
                                if pressure < 1:
                                        pressure = 1
                                self.setPressure(pressure)
                                time.sleep(1)
                        elif ((x < (Grms - 3))):
                                pressure = pressure + 3
                                if pressure > 80:
                                        pressure = 80
                                self.setPressure(pressure)
                                time.sleep(1)
                        elif ((x >= (Grms - 1)) and (X <= (Grms + 1))):
                                time.sleep(1)
                                x = read.readGrms(grmsLog)
                                print x
                                
        def calibrationCycle(self, frequency):
                self.setFreq(frequency)
                
                for n in range(1,70):
                        if n < 2:
                                self.setPressure(0 + (n*.5))
                                time.sleep(60)
                        elif n >= 2: 
                                self.setPressure(n - 1)
                                time.sleep(60)
                self.setPressure(0)
                print 'Calibration cycle is complete.'
                
                        

        def grmsCycling(self, startGrms,numberOfSteps,stepSize,timeToWaitAtStep,numberOfCycles, frequency):
                self.setFreq(frequency)
                pressure = 1

                Shift1d = .005
                Shift2d = .02
                Shift3d = .04
                Shift1u = .006
                Shift2u = .023
                Shift3u =  .05
                for cycle in range(1,numberOfCycles+1):
                        timetoEnd = time.time() + (60 * timeToWaitAtStep)#convert to minutes
                        while time.time() < timeToEnd:
                                x = read.readGrms(grmsLog)
                                print x
                                Buffer1d = (cycle*stepSize - .2)
                                Buffer2d = (cycle*stepSize - .5)
                                Buffer3d = (cycle*stepSize - 1)
                                Buffer1u = (cycle*stepSize + .2)
                                Buffer2u = (cycle*stepSize + .5)
                                Buffer3u = (cycle*stepSize + 1)
                                
                                                                
                                if(x < (startGrms + Buffer3d)):
                                        #print 'd1'
                                        pressure = pressure + Shift3d
                                        if pressure > 80:
                                                pressure = 80
                                        self.setPressure(pressure)
                                        time.sleep(1)
                                elif((x < (startGrms + Buffer2d)) and (x > (startGrms + Buffer3d))):
                                        #print 'd2'
                                        pressure = pressure + Shift2d
                                        if pressure > 80:
                                                pressure = 80
                                        self.setPressure(pressure)
                                        time.sleep(1)
                                elif((x >= (startGrms + Buffer2d)) and (x <= (startGrms + Buffer1d))):
                                        #print 'd3'
                                        pressure = pressure + Shift1d
                                        if pressure > 80:
                                                pressure = 80
                                        self.setPressure(pressure)
                                        time.sleep(1)
                                elif ((x >= (startGrms + Buffer1d)) and (x <= (startGrms + Buffer1u))):
                                        #print 'd4'
                                        time.sleep(1)
                                        #x = read.getGrms(grmsLog)
                                        #print x
                                elif((x <= (startGrms + Buffer2u)) and (x >= (startGrms + Buffer1u ))):
                                        #print 'd5'
                                        pressure = pressure - Shift1u
                                        if pressure < 1:
                                                pressure = 1
                                        self.setPressure(pressure)
                                        time.sleep(1)                     
                                elif((x > (startGrms + Buffer2u))  and (x < (startGrms + Buffer3u))):
                                        #print 'd6'
                                        pressure = pressure - Shift2u
                                        if pressure < 1:
                                                pressure=1 
                                        self.setPressure(pressure)
                                        time.sleep(1)
                                elif(x > (startGrms + Buffer3u)):
                                        #print 'd7'
                                        pressure = pressure - Shift3u
                                        if pressure < 1:
                                                pressure=1  
                                        self.setPressure(pressure)
                                        time.sleep(1)
                        print 'Cycle ' + str(i) + ' of ' + str(cycle) + ' is complete.'
                print 'Finished Grms Cycling. Setting pressure to 0 Psi.'
                self.setPressure(0)