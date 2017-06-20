@ECHO OFF

taskkill /IM python.exe
:: change this to the location of the mentioned python script if this is called from a different folder. 
:: cd C:\Users\Josep\OneDrive\Documents\GitHub\Halt-Hass\guiTest2
pyhton stopTesting.py