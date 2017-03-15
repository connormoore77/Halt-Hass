import numpy as np
#import pyqtgraph as pg
import serial,glob,math
#import pyqtgraph.exporters
import time,threading,sys,os,fnmatch,shutil
#filename=raw_input("filename:  ")
filename="gfile.txt"



def fWrite(filename,y):
	#try :f = open(filename, 'w', os.O_NONBLOCK);f.flush();f.write(y+'\n');f.close()
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
        	ACMport  = glob.glob('COM12')
        	for i in range(0,len(ACMport)):
                	if ACMport[i]==exclude:	ACMport[i]=0
                	try   :	info=serial.Serial(ACMport[i]);address=ACMport[i]
	                except: print ''
	print '%s = %s'%(boardName,address);print info
	return info,address

class SerialReader(threading.Thread):
	def __init__(self, portR, M, N, ch, toG):
        	threading.Thread.__init__(self)
		self.portR 	= portR         
		#self.portW 	= portW                      
        	self.M     	= M           
		self.N     	= N                         
		self.ch    	= ch 
		self.toG   	= toG                       
        	self.ptr   	= 0             
		self.sp    	= 0.0                       
        	self.buffer    	= np.zeros((N*M,ch),dtype=np.float)
        	self.buff_rms  	= np.zeros((  M,ch),dtype=np.float)
        	self.buff_gt  	= np.zeros((  M   ),dtype=np.float)
        	self.exitFlag  	= False
        	self.exitMutex 	= threading.Lock()
        	self.dataMutex 	= threading.Lock()
    	def run(self):
        	exitMutex      	= self.exitMutex
        	dataMutex      	= self.dataMutex
        	buffer         	= self.buffer
        	buff_rms       	= self.buff_rms
        	buff_gt       	= self.buff_gt
        	t1             	= time.time()
        	portR      	= self.portR         
		#portW     	= self.portW
        	M	   	= self.M    
		N	       	= self.N
		ch	   	= self.ch
		toG       	= self.toG
		count      	= 0	
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
			gAMP 	= np.array([(R[:,i]-avg[i])/toG for i in range(0,ch)]).reshape(M,ch)
			#Write gRMS to MEGA
			gRMS 	= np.array([rms(gAMP[:,i])      for i in range(0,ch)])
			gt 	= np.sqrt(gRMS[0]**2+gRMS[1]**2+gRMS[2]**2)
			fWrite(filename,str(gt))
			#portW.flush()              
			#portW.write(str(gt))
			#print gRMS ; 
			print gt
			#print (self.ptr/M)%N 
			count  += self.M
			t2	= time.time()
			difft 	= t2-t1
        	    	if difft > 1.0:
				if sp is None : sp = count / difft
        	    		else          : sp = sp * 0.9 + (count / difft) * 0.1
        	    		count = 0 
				t1 = t2
        	    	with dataMutex:                    
        	    		buffer  [ self.ptr : self.ptr + M ] = gAMP
        	    		buff_rms[          (self.ptr/M)%N ] = gRMS
				buff_gt [          (self.ptr/M)%N ] = gt
				self.ptr = (self.ptr + self.M) % (N*M)
        	    		if sp is not None : self.sp = sp
	def get(self,M):
       		with self.dataMutex:
        		ptr = self.ptr
			M   = self.M
			if ptr==0 : data = self.buffer[ptr-M :   ]
        	    	else      : data = self.buffer[ptr-M :ptr].copy()
			rate = self.sp
        		return data , self.buff_rms[(ptr/M)%N],self.buff_gt[(ptr/M)%N]
	def exit(self):
    		with self.exitMutex : self.exitFlag = True

########################################################################################
ArduinoRead = serial.Serial('COM12',9600)
#ArduinoWrite, address_write = findArduino('Arduino_write',address_read)

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
#case	    = input( 'Grms plot   (1(y)/0(n))    : ')
#DataLogging = input( 'DataLogging (1(y)/0(n))	 : ')
#if DataLogging ==1 : DataInfo = raw_input('Description     : ')

########################################################################################

"""
c=[(255,0,0),(255,255,0),(0,255,0),(0,0,255),(165,42,42),(128,0,128)]
app     = pg.mkQApp()        
win     = pg.GraphicsWindow(title='SAMPLING RATE = %d [kHz]'%sps)
win.resize(1000,400)
plt	= win.addPlot(title="ADXL001-500z")
plt.setLabels(left=('Acceleration','[g]'),bottom=('Time','[s]'))
plt.setYRange(-ymax,  ymax)
plt.setXRange(    0, t_avg)
plt.showGrid(x=True,y=True)
plt.addLegend()
if DataLogging ==1 : exporter = pg.exporters.CSVExporter(plt)

A0=plt.plot(pen=c[0],name='A0')
"""
"""
A1=plt.plot(pen=[1],name='A1');A2=plt.plot(pen=[2],name='A2')
A3=plt.plot(pen=c[3],name='A3');A4=plt.plot(pen=[4],name='A4');A5=plt.plot(pen=[5],name='A5')
"""
"""
if case==1 :
	win.nextRow()
        pl = win.addPlot(title='grms')
        #G0=pl.plot(pen=c[0]);G1=pl.plot(pen=c[1]);G2=pl.plot(pen=c[2])
        #G3=pl.plot(pen=c[3]);G4=pl.plot(pen=c[4]);G5=pl.plot(pen=c[5])
        #Gt=pl.plot(pen='w',symbolBrush='w',symbolPen='w')
        Gt=pl.plot(pen='w')
"""


########################################################################################
#thread = SerialReader(ArduinoRead,ArduinoWrite,M,N,ch,toG)
thread = SerialReader(ArduinoRead,M,N,ch,toG)
thread.start()
########################################################################################
"""
#GT=[]
#r=0
def update():                
	global ArduinoRead,ArduinoWrite,thread
	#global plt,A0,A1,A2,A3,A4,A5,GT
	#global pl ,G0,G1,G2,G3,G4,G5,Gt
	global plt,A0,pl,Gt
	
	data,grms,gt = thread.get(M)
	GT.append(gt*(1+r))
	pl.setLabels(left='%0.1f'%gt)
	A0.setData(t_data,data[:,0])
	
	A1.setData(t_data,data[:,1]);A2.setData(t_data,data[:,2])
	A3.setData(t_data,data[:,3]);A4.setData(t_data,data[:,4]);A5.setData(t_data,data[:,5])
	
	Gt.setData(GT[:r])
	if DataLogging==1:
		timestamp=time.time()
		now=int(round(timestamp))
		if (now%t_logging)==0:
			localDATE=time.strftime('%y%m%d'  ,time.localtime(timestamp))
			localTIME=time.strftime('%H:%M:%S',time.localtime(timestamp))
			filename='accData_'+localDATE+'_%s_'%DataInfo + localTIME+'.csv'
			exporter.export(filename)
	if not plt.isVisible():
		thread.exit()
		timer.stop()
		ArduinoRead.close() ; ArduinoRead.delete()
		ArduinoWrite.close(); ArduinoWrite.delete()
	r+=1
"""
"""
timer = pg.QtCore.QTimer()                    
timer.timeout.connect(update)
timer.start(0)
if sys.flags.interactive == 0 : app.exec_()
"""
