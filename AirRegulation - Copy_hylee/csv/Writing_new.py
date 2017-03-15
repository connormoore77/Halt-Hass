import numpy as np
import serial,glob,math
import time,threading,sys,os,fnmatch,shutil

ArduinoRead = serial.Serial('COM12',9600)
t_log = 10
filename = "gfile.txt"

t_start = time.time()
localDATE = time.strftime('%y%m%d'  ,time.localtime(t_start))
localTIME = time.strftime('%Hh_%Mm_%Ss',time.localtime(t_start))
fgrmsName = localDATE+'_grms_'+'start_at_'+ localTIME+'.csv'
fgrmsComponentsName = localDATE+'_grmsComponents_'+'start_at_'+ localTIME+'.csv'

def facc_Write(y,t):
	localDATE = time.strftime('%y%m%d'  ,time.localtime(t))
	localTIME = time.strftime('%Hh_%Mm_%Ss',time.localtime(t))
	faccName = localDATE+'_acc_'+localTIME+'.csv'
	facc = open(faccName,'w')
	for i in range(0,len(y)):
		facc.write(str(0.00002*i)+','+','.join(map(str,y[i]))+' \n')
	facc.close()


def fgrms_Write(fgrmsName,y,t0,t):
	str_t  = str(int(t-t0))
	str_g  = str(round(y,1))
	fgrms = open(fgrmsName,'a')
        fgrms.write(str_t+','+str_g+'\n');fgrms.close()


def fgrmsComponents_Write(fgrmsComponentsName,ycomp,t0,t):
	str_t  = str(int(t-t0))
	gcomp=np.array([round(item,1) for item in ycomp])
	fgrms = open(fgrmsComponentsName,'a')
	fgrms.write(str_t+','+','.join(map(str,gcomp))+' \n')
	fgrms.close()

def fWrite(filename,y):
	try :f = open(filename, 'w');f.flush();f.write(y+'\n');f.close()
	except:print ''
	

def rms(y):
        sum_squares = 0
        for i in range(0,len(y)):
                sum_squares = sum_squares+y[i]*y[i]
        return math.sqrt(sum_squares/float(len(y)))

def findArduino(boardName,exclude):
	a = raw_input('Connect %s and press Enter'%boardName)
	if a is not None:
        	ACMport  = glob.glob('/dev/ttyA*')
        	for i in range(0,len(ACMport)):
                	if ACMport[i]==exclude:	ACMport[i]=0
                	try   :	info=serial.Serial(ACMport[i]);address=ACMport[i]
	                except: print ''
	print '%s = %s'%(boardName,address);print info
	return info,address


sps      = 50
dt       = 0.00002 
ymax     = 600
t_logging= 10
t_avg    = 1.0
M        = int(round(t_avg/dt))	           
N        = 50			   
ch       = 6
toG      = 2.7365 		  
t_data   = [i*dt for i in range(0,M) ]
class SerialReader(threading.Thread):
	def __init__(self, portR,M,N,ch,toG):
        	threading.Thread.__init__(self)
		self.portR 	= portR         
		self.t_now      = time.time()
		self.gAMP	= []
        	self.ptr   	= 0             
		self.sp    	= 0.0                       
        	self.exitFlag  	= False
        	self.exitMutex 	= threading.Lock()
        	self.dataMutex 	= threading.Lock()
    	def run(self):
        	exitMutex      	= self.exitMutex
        	dataMutex      	= self.dataMutex
        	t1             	= time.time()
        	portR      	= self.portR         
		self.count      = 0	
		sp        	= None
        	while True:
			with exitMutex:                    
        	        	if self.exitFlag:break
			#Read gAMP from DUE
			temp   	= np.empty((M,ch),dtype=np.uint16)
        	    	portR.flush()
			portR.read(int(0.1*M*2*ch))	    
			R      	= portR.read(M*2*ch)
			R      	= np.fromstring(R,dtype=np.uint16) 
			leading	= R[0]>>12           
			leading	= leading-100/sps
			R      	= R&4095	            
			R      	= R.reshape(M,ch)		
			for i in range (0,ch) : temp[:,(leading+i)%ch] =    R[:,     i]	
			for i in range (0,ch) : R[:,i]                 = temp[:,ch-1-i]		
			avg  	= np.array([np.average(R[:,i])  for i in range(0,ch)]) 
			self.t_now=time.time()
			self.gAMP= np.array([(R[:,i]-avg[i])/toG for i in range(0,ch)]).reshape(M,ch)
			gRMS 	= np.array([rms(self.gAMP[:,i])      for i in range(0,ch)])
			gt 	= np.sqrt(gRMS[0]**2+gRMS[1]**2+gRMS[2]**2)
			print str(round(gt,1))
			fWrite(filename,str(gt))
			fgrms_Write(fgrmsName,gt,t_start,self.t_now)
			fgrmsComponents_Write(fgrmsComponentsName,gRMS,t_start,self.t_now)
			self.count  += M
			t2	= time.time()
			difft 	= t2-t1
        	    	if difft > 1.0:
				if sp is None : sp = self.count / difft
        	    		else          : sp = sp * 0.9 + (self.count / difft) * 0.1
				t1 = t2
        	    	with dataMutex:                    
				self.ptr = (self.ptr + M) % (N*M)
        	    		if sp is not None : self.sp = sp
	def exit(self):
    		with self.exitMutex : self.exitFlag = True

########################################################################################

class Csvfiles(threading.Thread):
	def __init__(self,mainTH):
		self.mainTH=mainTH
        	threading.Thread.__init__(self)
	def run(self):
		mainTH=self.mainTH
		i=0
        	while True:
			if i==0:print ""
				
			else:
				if mainTH.count%(M*30)==0:
					facc_Write(mainTH.gAMP,mainTH.t_now)
					
			i=1
#ArduinoRead, address_read=findArduino('Arduino_read','0')
thread = SerialReader(ArduinoRead,M,N,ch,toG)
thread.start()
thread2 = Csvfiles(thread)
thread2.start()
#######################################################################################

