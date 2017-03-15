import pyqtgraph as pg
import pyqtgraph.exporters
import time
import time, threading, sys
import serial
import numpy as np
import glob
"""
Hyoyeon Lee 2016.08.03
[Reference] http://forum.arduino.cc/index.php?topic=137635.15;wap2
[Hardware ] arduino_DUE(loaded with "accDue_6channels_tag.ino")
	    accelerometer_ADXL001-500g with Power=3.3V (no low-pass filter :C2=22[nF],R1=0[Ohm])
[Summary  ] Find a connected Serial '/dev/ttyA*'(arduinoDUE-USB port(Not a programming port!!)
            Read T=dt*M[sec] of data where T=<1[sec], dt=20E-6[sec], M=T/dt
            (Type of data is uint16, 0~4095 : upper4bits=channelID, lower12bits=data)
	    (T is used to get rms so it should be long enough to sample the wave pattern)  
	    Read the channel ID of the first data and store them into a buffer 
	    (such that the column index match the channelID,DUEpin-channel[A0-CH7,A1-CH6...A5-CH0])
	    Convert data into [g] and calculate grms
	    Fetch data from buffer and create a real-time plot of t_range=T*n[sec]<5[sec]
*** 
[README]
1. Before running this, unplug the usb and reconnect it.
2. M can go upto 50000 the minimum sampling(M) should be long enough to include at least one period of the peak.
3. t_range (plot range) can go upto ~
"""	       


#____________________Find a port connected to Arduino________________________#
print '	Connect the Arduino (USB port)Cable to PC.'
print '	If already connected, UNPLUG and then Reconnect it.'

a = raw_input( ' tab [Enter] key if you connect the port ')
if a is not None:
	print 'Finding the address of the port'
ACMport  = glob.glob('/dev/tty*')
for item in ACMport:
	try:    due = serial.Serial(item)
	except: print ''
print 'The Arduino is Connected :'
print due

#_________________________Set Variables from user_________________________#
#T       = input('Sampling Time (T) with T <= 1[sec]) :  ')
#t_range = input('Plot Range (t_range)  with %f[sec] <= t_range < 5[sec]:  ' %(T))
#ymax    = input('Y max [g]:  ')
T=1
t_range=1
ymax=500
ch      = 6
dt      = 20E-6 		# Data are sent at 50[kHz]
M = int(T/dt)  		        
n = int(t_range/T)
N = int(50*n)
scaling  = 2.7 		# [digits/g] for ADXL001-500z with Power=3.3V

#_________________________Threading_______________________________________#
class SerialReader(threading.Thread):
#_________________________________________________________________#	
	def __init__(self, port, M, N):
        	threading.Thread.__init__(self)
        	self.buffer    = np.zeros((N*M,ch),dtype=np.float)
        	self.buff_digit= np.zeros((N*M,ch),dtype=np.uint16)
		self.buff_rms  = np.zeros((N  ,ch),dtype=np.float)
		self.N         = N                         
        	self.M         = M                         
        	self.ptr       = 0                         
		self.port      = port                      
        	self.sps       = 0.0                       
        	self.exitFlag  = False
        	self.exitMutex = threading.Lock()
        	self.dataMutex = threading.Lock()
#_________________________________________________________________#	
    	def run(self):
        	exitMutex      = self.exitMutex
        	dataMutex      = self.dataMutex
        	buffer         = self.buffer
		buff_digit     = self.buff_digit
		buff_rms       = self.buff_rms
        	port           = self.port
        	count          = 0
        	sps            = None
        	t1             = pg.ptime.time()
        	while True:
			with exitMutex:                    
        	        	if self.exitFlag:
        	            		break
        	    	port.flush()
			mod4   = np.empty((M,ch),dtype=np.uint16)
			org    = port.read(5000*2*ch)		#eliminate incorrect data reading that occurs 0.1s    
			org    = port.read(self.M*2*ch)			#read data from Due    
        	    	mod1   = np.fromstring(org,dtype=np.uint16)     #convert string to integer
			leading= mod1[0]>>12			        #check the channel ID of the first data
			mod2   = mod1&4095				#remove channel ID and get only acceleration values
			mod3   = mod2.reshape(self.M,ch)		
			for i in range (0,ch):				#distribute data so that col# match the channelID
				mod4[:,(leading-2+i)%6] = mod3[:,i]	#mod4=raw data
			mean   = [np.average(mod4[:,i])             for i in range(0,ch)]#mean=mean of rawdata for T
			scaled = [(mod4[:,i]-mean[i])/scaling 	    for i in range(0,ch)]#scaled=converted into [g]
			rms    = [np.sqrt(sum(scaled[i]**2)/self.M) for i in range(0,ch)]#rms=grms
			count += self.M                    
        	    	t2     = pg.ptime.time()
        	    	difft     = t2-t1
        	    	if difft > 1.0:
        	    	    if sps is None:                
        	    	        sps = count / difft
        	    	    else:
        	    	        sps = sps * 0.9 + (count / difft) * 0.1
        	    	    count = 0
        	    	    t1    = t2
        	    	with dataMutex:                    
        	    	    buffer    [ self.ptr : self.ptr+self.M ] = np.transpose(scaled)
			    buff_digit[ self.ptr : self.ptr+self.M ] = mod4
			    buff_rms  [self.ptr/M]                   = rms
        	    	    self.ptr = (self.ptr + self.M) % (N*M)
        	    	    if sps is not None:
        	    	        self.sps = sps
#_________________________________________________________________#	
	def get(self, M,n):
       		with self.dataMutex:
			num = M*n                    
        		ptr = self.ptr
			if ptr-num < 0:
        	        	data   = np.empty((num,ch),dtype=np.float)
        	        	data [       :num-ptr] = self.buffer    [ptr-num:   ]
        	        	data [num-ptr:       ] = self.buffer    [       :ptr]
        	        	digit  = np.empty((num,ch),dtype=np.uint16)
				digit[       :num-ptr] = self.buff_digit[ptr-num:   ]
        	        	digit[num-ptr:       ] = self.buff_digit[       :ptr]
				grms   = np.empty((10*n,ch),dtype=np.float)
				grms [       :10*n-ptr/M] = self.buff_rms  [ptr/M-10*n:     ]
				grms [10*n-ptr/M:       ] = self.buff_rms  [       :ptr/M]
        	    	else:
        	    	    data  = self.buffer      [self.ptr-num :self.ptr  ].copy()
        	    	    digit = self.buff_digit  [self.ptr-num :self.ptr  ].copy()
			    grms  = self.buff_rms    [self.ptr/M-10*n :self.ptr/M].copy()
        	    	rate = self.sps
 
        		return np.linspace(0,t_range,num),data,digit,np.linspace(0,t_range,10*n),grms
#_________________________________________________________________#	
	def exit(self):
    		with self.exitMutex:                   
    	        	self.exitFlag = True
##################################################################


app     = pg.mkQApp()        
win	= pg.GraphicsWindow(title='ADXL001-500z')     
win.resize(1000,400)
lr=pg.LinearRegionItem([0.1,0.15])
lr.setZValue(-10)
#_______________plot1____________________________________
plt1	= win.addPlot(title="Accelerometer#1")
plt1.setLabels(left=('Acceleration','g'),bottom=('Time','s'))
#plt1.setYRange(-ymax,ymax)
plt1.setYRange(-510,510)
plt1.setXRange(0 ,t_range)
plt1.showGrid(x=True,y=True)
plt1.addLegend()
plt1.addItem(lr)
x1=plt1.plot(pen=(255,  0,  0),name='x1(PinA0)')
y1=plt1.plot(pen=(  0,255,  0),name='y1(PinA1)')
z1=plt1.plot(pen=(  0,  0,255),name='z1(PinA2)')
x2=plt1.plot(pen=(200,200,  0),name='x2(PinA3)')
y2=plt1.plot(pen=(  0,200,200),name='y2(PinA4)')
z2=plt1.plot(pen=(200,  0,200),name='z2(PinA5)')
exporter = pg.exporters.CSVExporter(plt1)#here is the exporter object

"""
#Linear Region slowers the data aquisition.
#If needed, activate this with the last def UpdatePlot, etc.
#_______________plot2____________________________________
plt2=win.addPlot(title='Linear Region')
plt2.setYRange(-ymax,ymax)
rx1=plt2.plot(pen=(255,  0,  0))
ry1=plt2.plot(pen=(  0,255,  0))
rz1=plt2.plot(pen=(  0,  0,255))
rx2=plt2.plot(pen=(200,200,  0))
ry2=plt2.plot(pen=(  0,200,200))
rz2=plt2.plot(pen=(200,  0,200))
"""
#_______________plot3____________________________________

plt3=win.addPlot(title='grms')
plt3.setYRange(-510,510)
gx1=plt3.plot(pen=(255,  0,  0))
gy1=plt3.plot(pen=(  0,255,  0))
gz1=plt3.plot(pen=(  0,  0,255))
gx2=plt3.plot(pen=(200,200,  0))
gy2=plt3.plot(pen=(  0,200,200))
gz2=plt3.plot(pen=(200,  0,200))

#Start Program
thread = SerialReader(due,M,N)
thread.start()
#___________________________________________________________________#
def update():
	
	global due,thread,lr
	global plt1,   x1, y1, z1, x2, y2, z2
	global plt2,  rx1,ry1,rz1,rx2,ry2,rz2
	global plt3,  gx1,gy1,gz1,gx2,gy2,gz2
	
	t,data,digit,tgrms,grms = thread.get(M,n)
	
	
	x1.setData(t,data[:,5])
	y1.setData(t,data[:,4])
	z1.setData(t,data[:,3])
	x2.setData(t,data[:,2])
	y2.setData(t,data[:,1])
	z2.setData(t,data[:,0])
	"""
	rx1.setData(t,data[:,5])
	ry1.setData(t,data[:,4])
	rz1.setData(t,data[:,3])
	rx2.setData(t,data[:,2])
	ry2.setData(t,data[:,1])
	rz2.setData(t,data[:,0])
	"""
	gx1.setData(tgrms,grms[:,5])
	gy1.setData(tgrms,grms[:,4])
	gz1.setData(tgrms,grms[:,3])
	gx2.setData(tgrms,grms[:,2])
	gy2.setData(tgrms,grms[:,1])
	gz2.setData(tgrms,grms[:,0])
	now = int(round(time.time()))

	if (now % 60)==0:
		filename = "accelerometerData_%d.csv" % now
		exporter.export(filename)

	if not plt1.isVisible():
		thread.exit()
	        timer.stop()
		due.close()
		due.delete()
#___________________________________________________________________#
timer = pg.QtCore.QTimer()                    
timer.timeout.connect(update)

#___________________________________________________________________#
"""
def updatePlot():
	plt2.setXRange(*lr.getRegion(),padding=0)
def updateRegion():
	lr.setRegion(plt2.getViewBox().viewRange()[0])
lr.sigRegionChanged.connect(updatePlot)
plt2.sigXRangeChanged.connect(updateRegion)
updatePlot()
"""


timer.start(0)
if sys.flags.interactive == 0:                  
    app.exec_()
