import os,time

def getGrms(filename):
	while 1:
		try:f = open(filename, 'r');val= f.readline();f.close();return float(val)
		except:print 'BAD'


