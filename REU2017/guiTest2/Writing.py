import numpy as np
import serial,glob,math
import time,threading,sys,os,fnmatch,shutil
import ROOT

print ""
portDUE=raw_input("Port of DUE ? (COM##)   : ")
ArduinoRead = serial.Serial(portDUE,9600)
t_log = 10
filename = "grmsLog.txt"
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
		#print i
	facc.close()
def fgrms_Write(fgrmsName,y,t0,t):
	str_t  = str(int(t-t0))
	str_g  = str(round(y,1))
	fgrms = open(fgrmsName,'a')
        fgrms.write(str_t+','+str_g+'\n');fgrms.close()
def fgrmsComponents_Write(fgrmsComponentsName,y,t0,t):
	n=len(y);str_t   = str(int(t-t0))
	fgrms = open(fgrmsComponentsName,'a')
	print str(y[n-1])+'    ('+str(y[0])+','+str(y[1])+','+str(y[2])+')'
	fgrms.write(str_t+','+','.join(map(str,y))+' \n')
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
ymax     = 100
t_avg    = 1.0
M        = int(round(t_avg/dt))	           
N        = 50			   
n	 = 1
ch       = 6
toG      = 2.7365 		  
t_data   = [i*dt for i in range(0,M) ]
class SerialReader(threading.Thread):
	def __init__(self, port,M,N,ch,toG):
        	threading.Thread.__init__(self)
		self.buffer    = np.zeros((N*M,ch),dtype=np.float)
                self.buff_rms  = np.zeros((N,ch+1),dtype=np.float)
		self.ptr   	= 0             
		self.port 	= port         
		self.t_now      = time.time()
		self.gAMP	= []
		self.sp    	= 0.0                       
        	self.exitFlag  	= False
        	self.exitMutex 	= threading.Lock()
        	self.dataMutex 	= threading.Lock()
    	def run(self):
        	exitMutex      	= self.exitMutex
        	dataMutex      	= self.dataMutex
        	buffer         = self.buffer
                buff_rms       = self.buff_rms
        	port      	= self.port         
		self.count      = 0	
		sp        	= None
		t1             	= time.time()
        	while True:
			with exitMutex:                    
        	        	if self.exitFlag:break
			#Read gAMP from DUE
			m4   	= np.empty((M,ch),dtype=np.uint16)
			raw   	= np.empty((M,ch),dtype=np.uint16)
        	    	port.flush()
			port.read(int(0.1*M*2*ch))	    
			org   	= port.read(M*2*ch)
			m1     	= np.fromstring(org,dtype=np.uint16) 
			leading	= m1[0]>>12           
			leading	= leading-100/sps
			m2     	= m1&4095	            
			m3     	= m2.reshape(M,ch)		
			for i in range (0,ch) : m4[:,(leading+i)%ch] = m3[:,i]	
			for i in range (0,ch) : raw[:,i] = m4[:,ch-1-i]		
			avg  	= [np.average(raw[:,i])       for i in range(0,ch)]
			self.t_now=time.time()
			scaled = [(raw[:,i]-avg[i])/toG for i in range(0,ch)]
			#self.gAMP= np.array([(R[:,i]-avg[i])/toG for i in range(0,ch)]).reshape(M,ch)
			rmsComp= [rms(scaled[i]) for i in range(0,ch)]
                        rmsVec = np.sqrt(rmsComp[0]**2+rmsComp[1]**2+rmsComp[2]**2)
                        rmsComp.append(rmsVec);n=len(rmsComp)-1 #idx of vector sum in a rmsComp array
                        rmsComp=np.array([round(item,1) for item in rmsComp])
                        


			#print rmsComp[n]
		
			fWrite(filename,str(rmsComp[n]))
			fgrms_Write(fgrmsName,rmsComp[n],t_start,self.t_now)
			fgrmsComponents_Write(fgrmsComponentsName,rmsComp,t_start,self.t_now)
			self.count  += M
			t2	= time.time()
			difft 	= t2-t1
        	    	if difft > 1.0:
				if sp is None : sp = self.count / difft
        	    		else          : sp = sp * 0.9 + (self.count / difft) * 0.1
				
				t1 = t2
        	    	with dataMutex:     
				buffer    [ self.ptr : self.ptr+M ] = np.transpose(scaled)
                            	buff_rms  [self.ptr/M] = rmsComp
				self.ptr = (self.ptr + M) % (N*M)
        	    		if sp is not None : self.sp = sp
	def get(self, M,n):
                with self.dataMutex:
                        num = M*n
                        ptr = self.ptr
                        if ptr-num < 0:
                                data   = np.empty((num,ch),dtype=np.float)
                                data [       :num-ptr] = self.buffer    [ptr-num:   ]
                                data [num-ptr:       ] = self.buffer    [       :ptr]
                        else:
                                data  = self.buffer      [self.ptr-num :self.ptr  ].copy()
                        rms=self.buff_rms[ptr/M]
                        rate = self.sp
                        return data,rms,self.t_now

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
				if mainTH.count%(M*t_log)==0:
					print "------------------------------------[CSV file out]  %d [sec]"%(mainTH.count/M)
					data,rms,t_now=mainTH.get(M,n)
					facc_Write(data,t_now)
					time.sleep(1)
			i=i+1
#ArduinoRead, address_read=findArduino('Arduino_read','0')
thread = SerialReader(ArduinoRead,M,N,ch,toG)
thread.start()
thread2 = Csvfiles(thread)
thread2.start()
#######################################################################################
