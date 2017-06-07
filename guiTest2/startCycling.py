import time
import datetime
import thermalControl 
import vibrationControl
import cyclingControl
 
startCycling(VibStartGrms,VibNumberOfSteps,VibStepSize,VibStepLength,StartTemperature,
            enterSteps,ThermStepSize,NumCycles, VibFrequency):    
    cycleObject = cyclingControl.cycleAll('COM4','COM5','COM7','COM3')
    cycleObject.cycleAll(VibStartGrms,VibNumberOfSteps,VibStepSize,VibStepLength,StartTemperature,
            enterSteps,ThermStepSize,NumCycles, VibFrequency])