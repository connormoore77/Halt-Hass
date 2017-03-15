import matplotlib.pyplot as plt

f = open("tenney_datalog.csv","r")
temps = []
times = []
for line in f:
    foundComma = False
    tempString =""
    timeString =""
    for char in line:
        if(char!= ',' and foundComma==False and (char!=' ' or char !='\n')):
            tempString = tempString + char
        elif(char!=',' and foundComma==True and (char!=' ' or char!='\n')):
            timeString = timeString +char
        elif(char==','):
            foundComma=True
            continue
    try:
        temps.append(float(tempString))
        times.append(float(timeString))
    except ValueError:
        continue
    
plt.plot(times,temps)
plt.show()
    
