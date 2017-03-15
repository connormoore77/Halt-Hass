import grms
from sys import argv

script , input = argv

while 1:
	rowNum = raw_input("which row of the csv file would you like to read?(0-5)")
	y = grms.read_data(input,int(rowNum))
	mean = grms.rms(y)
	print "grms = ", mean
	plotname = raw_input("Give name you want to save the plot as (foo.png)")
	x = grms.plotf(y,mean,plotname)
	end = raw_input("End? (y/n)")
	if end=='y' or end == 'Y':
		break
#grms.Integrate(x,10000,50000)


