import serial

class freqShift(object):
	
	def __init__(self,port,baud):
		self.ard = serial.Serial(port,baud)
	def changeFreq(self,f):
		if (f>50):
			print "TOFAST"
			return

		deltaT = 500/f
		self.ard.write(str(deltaT))
	def close(self):
		self.ard.close()

