import pyqtgraph as pg
import time, threading, sys
import serial
import numpy as np
import glob
"""
Hyoyeon Lee 
Created 2016.08.03
Revised 2016.08.10
	T/dt=1[s]/20E-6[s] does not give 50000 in python2.#
		>>>>>>>changed M=int(T/dt) to M=int((T*1E6)/(dt*1E6))
	time array for the plot has the same division problem
		>>>>>>>used [i*dt for i in range(0,#)] instead of np.linspace()
	Colors of the graph correspond to the those of wires.
		>>>>>>> A0(x1,Red), A1(y1,Yellow)...A5(z2,Purple)
	Choose Enabled Axes, types of graph	

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
ACMport  = glob.glob('/dev/ttyA*')
for item in ACMport:
	try:    due = serial.Serial(item)
	except: print ''
print 'The Arduino is Connected :'
print due

#_________________________Set Variables from user_________________________#
#T       = input('Sampling Time (T) with T <= 1[sec]) :  ')
#t_range = input('Plot Range (t_range)  with %f[sec] <= t_range < 5[sec]:  ' %(T))
ymax    = input('Y max [g]:  ')
T=1
t_range=1
#ymax=500
ch      = 6
dt      = 20E-6  		# in [seconds] Data are sent at 50[kHz]
M = int((T*1E6)/(dt*1E6))	# each reading        
n = int(t_range/T)		# plot range
N = int(50*n)			# buffer length
scaling  = 2.7365 		# [digits/g] for ADXL001-500z with Power=3.3V

#____________Enable channels and choose plot type_________________________#
#nCH = input('Number of Accelerometers connected to Arduino (1~6) :  ')
nCH=6
plot_rms = input( 'need to plot RMS?press 1(y)/0(n) : ')
plot_lr  = input( 'need to plot ZoomIn?   1(y)/0(n) : ')

case=(plot_lr<<1)+plot_rms     #case 0-nn/ 1-rms/ 2-lr/ 3-rms&lr 


#_________________________Threading_______________________________________#
class SerialReader(threading.Thread):
#_________________________________________________________________#	
	def __init__(self, port, M, N):
        	threading.Thread.__init__(self)
        	self.buffer    = np.zeros((N*M,nCH),dtype=np.float)
        	self.buff_digit= np.zeros((N*M,nCH),dtype=np.uint16)
		self.buff_rms  = np.zeros((N  ,nCH),dtype=np.float)
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
			rawdata= np.empty((M,nCH),dtype=np.uint16)
			mod4   = np.empty((M, ch),dtype=np.uint16)
			dump   = port.read(5000*2*ch)			#eliminate incorrect data reading that occurs 0.1s    
			org    = port.read(self.M*2*ch)			#read data from Due    
        	    	mod1   = np.fromstring(org,dtype=np.uint16)     #convert string to integer
			leading= mod1[0]>>12			        #check the channel ID of the first data
			mod2   = mod1&4095				#remove channel ID and get only acceleration values
			mod3   = mod2.reshape(self.M,ch)		
			for i in range (0,ch):				# column index =  channelID-2 (ch2~ch7)
				mod4[:,(leading-2+i)%6] = mod3[:,i]	
			for i in range (0,nCH):				# column index =  pin number  ( A0~ A5)
				rawdata[:,i]=mod4[:,5-i]		# ONLY store data of enabled pins
			mean   = [np.average(rawdata[:,i])          for i in range(0,ch)]	#mean=mean of rawdata for T
			scaled = [(rawdata[:,i]-mean[i])/scaling    for i in range(0,ch)]	#scaled=converted into [g]
			rms    = [np.sqrt(sum(scaled[i]**2)/self.M) for i in range(0,ch)]	#rms=grms
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
			    buff_digit[ self.ptr : self.ptr+self.M ] = rawdata
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
        	        	data   = np.empty((num,nCH),dtype=np.float)
        	        	data [       :num-ptr] = self.buffer    [ptr-num:   ]
        	        	data [num-ptr:       ] = self.buffer    [       :ptr]
        	        	digit  = np.empty((num,nCH),dtype=np.uint16)
				digit[       :num-ptr] = self.buff_digit[ptr-num:   ]
        	        	digit[num-ptr:       ] = self.buff_digit[       :ptr]
				grms   = np.empty((10*n,nCH),dtype=np.float)
				grms [       :10*n-ptr/M] = self.buff_rms  [ptr/M-10*n:     ]
				grms [10*n-ptr/M:       ] = self.buff_rms  [       :ptr/M]
        	    	else:
        	    	    data  = self.buffer      [self.ptr-num :self.ptr  ].copy()
        	    	    digit = self.buff_digit  [self.ptr-num :self.ptr  ].copy()
			    grms  = self.buff_rms    [self.ptr/M-10*n :self.ptr/M].copy()
        	    	rate = self.sps
        		return data,digit,grms
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
plt1.setYRange(-ymax,ymax)
plt1.setXRange(0 ,t_range)
plt1.showGrid(x=True,y=True)
plt1.addLegend()
x1=plt1.plot(pen=(255,  0,  0),name='x1(PinA0)') #the same color of the wire 
y1=plt1.plot(pen=(255,255,  0),name='y1(PinA1)')
z1=plt1.plot(pen=(  0,255,  0),name='z1(PinA2)')
x2=plt1.plot(pen=(  0,  0,255),name='x2(PinA3)')
y2=plt1.plot(pen=(165, 42, 42),name='y2(PinA4)')
z2=plt1.plot(pen=(128,  0,128),name='z2(PinA5)')

if case==2  or case==3:
	#Linear Region slowers the data aquisition.
	#If needed, activate this with the last def UpdatePlot, etc.
	#_______________plot2____________________________________

	plt1.addItem(lr)
	plt2=win.addPlot(title='Linear Region')
	plt2.setYRange(-ymax,ymax)
	rx1=plt2.plot(pen=(255,  0,  0))
	ry1=plt2.plot(pen=(255,255,  0))
	rz1=plt2.plot(pen=(  0,255,  0))
	rx2=plt2.plot(pen=(  0,  0,255))
	ry2=plt2.plot(pen=(165, 42, 42))
	rz2=plt2.plot(pen=(128,  0,128))
	
	def updatePlot():
        	plt2.setXRange(*lr.getRegion(),padding=0)
	def updateRegion():
        	lr.setRegion(plt2.getViewBox().viewRange()[0])

if case==1 or case==3:
	#_______________plot3____________________________________

	plt3=win.addPlot(title='grms')
	plt3.setYRange(0,ymax)
	gx1=plt3.plot(pen=(255,  0,  0))
	gy1=plt3.plot(pen=(255,255,  0))
	gz1=plt3.plot(pen=(  0,255,  0))
	gx2=plt3.plot(pen=(  0,  0,255))
	gy2=plt3.plot(pen=(165, 42, 42))
	gz2=plt3.plot(pen=(128,  0,128))

t_data = [i*dt for i in range(0,n*M) ]
t_grms = [i*T  for i in range(1,10*n+1)]
#Start Program
thread = SerialReader(due,M,N)
thread.start()
#___________________________________________________________________#
def update():                
	global due,thread,lr
	global plt1,   x1, y1, z1, x2, y2, z2
	global plt2,  rx1,ry1,rz1,rx2,ry2,rz2
	global plt3,  gx1,gy1,gz1,gx2,gy2,gz2
	
	data,digit,grms = thread.get(M,n)
	

	x1.setData(t_data,data[:,0])
	"""
	y1.setData(t_data,data[:,1])
	z1.setData(t_data,data[:,2])
	x2.setData(t_data,data[:,3])
	y2.setData(t_data,data[:,4])
	z2.setData(t_data,data[:,5])
	"""
	if case==2 or case==3:
		rx1.setData(t_data,data[:,5])
		"""
		ry1.setData(t_data,data[:,4])
		rz1.setData(t_data,data[:,3])
		rx2.setData(t_data,data[:,2])
		ry2.setData(t_data,data[:,1])
		rz2.setData(t_data,data[:,0])
		"""
	if case==1 or case==3:
		gx1.setData(t_grms,grms[:,5])
		"""
		gy1.setData(t_grms,grms[:,4])
		gz1.setData(t_grms,grms[:,3])
		gx2.setData(t_grms,grms[:,2])
		gy2.setData(t_grms,grms[:,1])
		gz2.setData(t_grms,grms[:,0])
		"""
	if not plt1.isVisible():
		thread.exit()
	        timer.stop()
		due.close()
		due.delete()
#___________________________________________________________________#
timer = pg.QtCore.QTimer()                    
timer.timeout.connect(update)


#___________________________________________________________________#


if case==2 or case==3:

	lr.sigRegionChanged.connect(updatePlot)
	plt2.sigXRangeChanged.connect(updateRegion)
	updatePlot()

timer.start(0)
if sys.flags.interactive == 0:                  
    app.exec_()
