import serial
import time
import smtplib
class Arduino(object):
    s = 0
    x = 0
    
    import serial
    comm = 0
    
    def __init__(self,port):
        self.comm = serial.Serial(port,9600,timeout=0)  
        
    def readNTC(self):
        time.sleep(4)
        try :
            s = self.comm.read(10000)
        except:
            return -273
        float_a=-273.1
        a = "-273"
        #print s
        
        if (len(s)<3):
            print "NO NUM ERROR"
        for i in range(1,len(s)-2):
            
            if s[len(s)-2-i] == '\n':
                x = int(len(s)-i-2)
                
                #print x    
                a =  s[(x+1):-2]
                
                break
            elif len(s) < 10:
                a =  s[:-2]
                break
            else:
                a = -273.1
        try:
            float_a = float(a)
        except ValueError as e:
            print "Bad DataPoint Retrying"
            print e            
            return -272
        except UnboundLocalError as e:           
            print "Bad DataPoint Reconnecting"
            print e
            self.comm.close()
            print "Port closed for reboot"
            time.sleep(3)
            try :
                self.comm.open()
                print "Port reopen"
            except:
                return -273                        
    
        return float_a
       
            
             
            
            
        
        
        
        #return float(s[x+1:len(s)-2])  
            
            
            
                

    def close(self):
        self.comm.close()

    def open(self):
        self.comm.open()
    
    def s(self):
         print self.readNTC()
         
         print self.readNTC()
         
         print self.readNTC()
         
         print self.readNTC()
         
         print self.readNTC()
         
         print self.readNTC()
         
