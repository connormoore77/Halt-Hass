#!/usr/bin/python
import sys

argList = []
for arg in sys.argv:
    argList.append(arg)

outputText = open(argList[1], "r")
listPressure = [line.split() for line in outputText if "function pressure is" in line]
outputText = open(argList[1], "r")
listGrms = [line.split() for line in outputText if "Current grms is" in line]

tempP = []
pressure = []
for i in range(0, len(listPressure)):
    tempP = listPressure[i]
    temp = tempP[3]
    pressure.append(temp)
print pressure

tempG = []
grms = []
for i in range(0, len(listGrms)):
    tempG = listGrms[i]
    temp = tempG[3]
    grms.append(temp)
print grms