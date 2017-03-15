import pyqtgraph as pg
import time, threading, sys
import serial
import numpy as np
import glob
"""
[README]
0. Let A0~A5 pins be grounded when not used
1. Before running this, unplug the usb and reconnect it.
"""


"""
Hyoyeon Lee 
Created 2016.08.03
Revised 2016.08.11

[Reference] http://forum.arduino.cc/index.php?topic=137635.15;wap2
[Hardware ] arduino_DUE(loaded with "accDue_user_ch_sps.ino")
	    accelerometer_ADXL001-500g with Power=3.3V (no low-pass filter :C2=22[nF],R1=0[Ohm])
[Summary  ] Find a connected Serial '/dev/ttyA*'(arduinoDUE-USB port(Not a programming port!!)
            Read data(16bits) every T[s]
            	 >>>upper( 4 bits) : channelID ( ID2~ID7 corresponds to A5~A0)
		 >>>lower(12 bits) : data with conversion rate 3.3[V]/4095[digits] 
	    Convert to [g] by dividing scaling = 2.2E-3[V/g]*4095[digits]/3.2922[V]
	    Plot data,grms,and zoomed-in 
"""	       


#____________________Find a port connected to Arduino________________________#
print '	Connect the Arduino (USB port)Cable to PC.'
print '	If already connected, UNPLUG and then Reconnect it.'

a = raw_input( ' tab [Enter] key if you connect the port ')
if a is not None:
	print 'Finding the address of the port'
ACMport  = glob.glob('/dev/tty.usb*')
for item in ACMport:
	try:    due = serial.Serial(item)
	except: print ''
print 'The Arduino is Connected :'
print due


#[USER]_______________________user_ch_sps_dt
"""
while True:
	sps=input('Sampling rate of DUE board in [kHz]? (50 or 100?)')
	#print("deBUG")
	if sps not in [50,100]:
		print 'Not 50 or 100 [kHz]'
	else:
		print("50-100 Please")
		break
"""
sps=50
user_ch_sps_dt =[[6,20E-6],[7,10E-6]]
ch = user_ch_sps_dt[sps/50-1][0]
dt = user_ch_sps_dt[sps/50-1][1]

print 'Sampling Rate = %d [kHz], dt = %f [sec]' %(sps,dt)


 
#[USER]_______________________plot_type
plot_rms = input( 'need to plot RMS?press 1(y)/0(n) : ')
if sps==50:
	plot_lr  = input( 'need to plot ZoomIn?   1(y)/0(n) : ')
else:
	print 'ZoomIn plot is not recommended for sps=%d [kHz]' %sps 
	plot_lr  = input( 'still need to plot ZoomIn?   1(y)/0(n) : ')
ymax     = input('Y max [g]:  ')
t_range  = input('Plot Range in [sec] ? 1~5[sec]:  ')
#T        = input('Sampling Time (T) with T <= 1[sec]) :  ')
#nCH      = input('Number of Accelerometers connected to Arduino (1~6) :  ')

T      =1
nCH    = 6

case=(plot_lr<<1)+plot_rms      # case 0-none/ 1-rms/ 2-lr/ 3-rms&lr 
ndump = int((0.1*1E6)/(dt*1E6)) # dump first 0.1[s] data
M     = int((T*1E6)/(dt*1E6))	# each reading        
n     = int(t_range/T)		# plot range
N     = int(50*n)			# buffer length
scaling  = 2.7365 		# [digits/g] for ADXL001-500z with Power=3.3V



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
        	self.sp        = 0.0                       
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
        	sp             = None
        	t1             = pg.ptime.time()
        	while True:
			with exitMutex:                    
        	        	if self.exitFlag:
        	            		break
			mod4   = np.empty((M, ch),dtype=np.uint16)
			rawdata= np.empty((M,nCH),dtype=np.uint16)

        	    	port.flush()
			dump   = port.read(ndump*2*ch)			#dump incorrect reading    
			org    = port.read(self.M*2*ch)			#read data from Due    
        	    	mod1   = np.fromstring(org,dtype=np.uint16)     #convert string to integer
			leading= mod1[0]>>12			        #check the channel ID of the first data
			leading= leading-100/sps
			mod2   = mod1&4095				#remove channel ID and get only acceleration values
			mod3   = mod2.reshape(self.M,ch)		
			for i in range (0,ch):				# column index =  channelID-2 (ch2~ch7)
				mod4[:,(leading+i)%ch] = mod3[:,i]	
			for i in range (0,nCH):				# column index =  pin number  ( A0~ A5)
				rawdata[:,i]=mod4[:,ch-1-i]		# ONLY store data of enabled pins
			mean   = [np.average(rawdata[:,i])          for i in range(0,nCH)]	#mean=mean of rawdata for T
			scaled = [(rawdata[:,i]-mean[i])/scaling    for i in range(0,nCH)]	#scaled=converted into [g]
			rms    = [np.sqrt(sum(scaled[i]**2)/self.M) for i in range(0,nCH)]	#rms=grms
			count += self.M                    
        	    	t2     = pg.ptime.time()
        	    	difft     = t2-t1
        	    	if difft > 1.0:
        	    	    if sp is None:                
        	    	        sp = count / difft
        	    	    else:
        	    	        sp = sp * 0.9 + (count / difft) * 0.1
        	    	    count = 0
        	    	    t1    = t2
        	    	with dataMutex:                    
        	    	    buffer    [ self.ptr : self.ptr+self.M ] = np.transpose(scaled)
			    buff_digit[ self.ptr : self.ptr+self.M ] = rawdata
			    buff_rms  [self.ptr/M]                   = rms
        	    	    self.ptr = (self.ptr + self.M) % (N*M)
        	    	    if sp is not None:
        	    	        self.sp = sp
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
        	    	rate = self.sp
        		return data,digit,grms
#_________________________________________________________________#	
	def exit(self):
    		with self.exitMutex:                   
    	        	self.exitFlag = True
##################################################################


app     = pg.mkQApp()        
win	= pg.GraphicsWindow(title=' ************ SAMPLING RATE = %d [kHz]*************'%sps)     
win.resize(1000,400)
lr=pg.LinearRegionItem([0.01,0.05])
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
		rx1.setData(t_data,data[:,0])
		"""
		ry1.setData(t_data,data[:,1])
		rz1.setData(t_data,data[:,2])
		rx2.setData(t_data,data[:,3])
		ry2.setData(t_data,data[:,4])
		rz2.setData(t_data,data[:,5])
		"""
	if case==1 or case==3:
		gx1.setData(t_grms,grms[:,0])
		"""
		gy1.setData(t_grms,grms[:,1])
		gz1.setData(t_grms,grms[:,2])
		gx2.setData(t_grms,grms[:,3])
		gy2.setData(t_grms,grms[:,4])
		gz2.setData(t_grms,grms[:,5])
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
