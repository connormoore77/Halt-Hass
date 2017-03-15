import math
import csv
import matplotlib.pyplot as plt
from scipy import fft

import numpy as np

def rms(readings):
	
	sum_squares=0
	for i in range(0,len(readings)):
		sum_squares = sum_squares+readings[i]*readings[i]
	return math.sqrt(sum_squares/len(readings))
	
def read_data(input_file,rowNum):
    list = []
    with open(input_file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            try :
                list.append(float(row[rowNum]))
            except ValueError:
                print("Bad Point")
#        print(row[0])
#        print(row[0],row[1],row[2],)
    return list

def plot(list):

    plt.plot(list)
    plt.show()

def power_spectrum(list,grms):
    
    
    
    for i in range(0,len(list)):
        list[i]=list[i]/len(list)
    plt.subplot(3,1,3)
    plt.plot(grms*list)
    plt.show()


def plotf(y,grms,plotname):
    
   	   # sampling rate
    Ts = 1.0/len(y)       # sampling interval
    t = np.arange(0,1,Ts)      # time vector
    ff = 5
    #y = np.arange(0,len(y))# frequency of the signaly = np.sin(2 * np.pi * ff * t)
        
    plt.subplot(2,1,1)
    plt.plot(t,y,'k-')
    plt.xlabel('time')
    plt.ylabel('amplitude')
        
    plt.subplot(2,1,2)
    n = len(y)                       # length of the signal
    k = np.arange(n)
    T = n/len(y)
    frq = k/T # two sides frequency range
    freq = frq[range(n/2)]           # one side frequency range
        
    Y = np.fft.fft(y)/n              # fft computing and normalization
    Y = Y[range(n/2)]                #Normalization
    
    sum=0
    for i in range(0,len(Y)):
        sum=sum+abs(Y[i])
    
    print(sum)
#   renormalization
    Y=Y/sum
    Y=Y*grms
    
    plt.plot(freq,abs(Y), 'r-')
    plt.xlabel('freq (Hz)')
    plt.ylabel('|Y(freq)|')
    print "total integral = " , Integrate(Y,0,len(Y))
    print "0-5000 integral = " , Integrate(Y,0,5000)
    print "5000-10000 integral = " ,Integrate(Y,5000,10000)
    print "10000-15000 integral = " , Integrate(Y,10000,15000)
    print "15000-20000 integral = " , Integrate(Y,15000,20000)
#print(freq)
    plt.savefig(plotname)
    return Y

def Integrate(list,min,max):

	sum=0
	for i in range(min,max):
		sum = sum+abs(list[i])
    
	return sum

















