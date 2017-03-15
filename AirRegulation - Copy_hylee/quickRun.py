

import Vibration
import time

print "START"
test = Vibration.VibrationCycling('COM2','COM10')
test.cycle(5,1,5, frequency=20)
