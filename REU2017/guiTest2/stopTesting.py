#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import thermalControl 
import vibrationControl
import os
#from sys import executable

#make sure that the COMs listed here are correct before running.
vib = vibrationControl.vibrationCycling('COM4','COM5')
oven = thermalControl.tenney('COM7','COM3')

print 'Stopping all processes... '
print 'Setting pressure to 0 Psi.'
vib.setPressure(0)
print 'Setting frequency to 1 Hz.'
vib.setFrequency(1)
print 'Setting thermal chamber to 20 degrees C.'
oven.setTemperature(20)