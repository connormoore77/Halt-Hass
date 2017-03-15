classdef Tenney < handle
    %Tenney This is a class that will control HALT operation with the
    %Tenney thermal chamber at OU 2016
    %   Detailed explanation goes here
    
    properties
        Temperature_Acceptance=3;
        chamber;
        ard;
        data ;
        time ;
        
    end
    
    methods (Access = public)
     
        function  obj = Tenney(com,ardport)
            
            
            obj.chamber = serial(com,'Baudrate',9600,'Terminator','CR');
            obj.ard = Arduino(ardport);
            fopen(obj.chamber);
            get(obj.chamber);
            tic;
        end
            
        
        function r = close(obj)
            fclose(obj.chamber);
            obj.ard.close();
        end
        
        function r = setPoint(obj,setpoint)
            fprintf(obj.chamber,'= SP1 %d\n',setpoint);
            pause(1);
        end
        
        function temp = readTemp(obj)
            fprintf(obj.chamber,'? C1\n');
            pause(1);
            currentTemp = fgetl(obj.chamber);   
            dummyArray = size(currentTemp);
            maxIndex = dummyArray(2); %extract the max index
            x=1;
            while double(currentTemp(x)) < 20 %This is a bitMask loop
            x = x+1;
            end%extract the min index
            temp = str2double(currentTemp(x:maxIndex));
        end
        
        function  stepUp(obj,start,stop,N,T)
            step = (stop-start)/N;
            stepSoak=T*60;
            tic;
            
            for i = 0:N
                SP = start+i*step;
                obj.setPoint(SP);
                ntcTemp = obj.readArduino();
                
                while ntcTemp > (SP+obj.Temperature_Acceptance) || ntcTemp < (SP-obj.Temperature_Acceptance)
                    pause(1)
                    ntcTemp=obj.readArduino();
                    lap=toc;
                    display(lap);
                    %datalog
                    dummyData = [obj.data,ntcTemp];
                    obj.data = dummyData;
                    dummyTime = [obj.time,lap];
                    obj.time=dummyTime;
                    
                    
                end
                display('SETPOINT REACHED');
                 obj.soak(stepSoak);
            end
            
        end
        function stepDown(obj,start,stop,N,T)
            step = (start-stop)/N;
            stepSoak=T*60;
            tic;
            
            for i = 0:N
                SP = start-i*step;
                obj.setPoint(SP);
                ntcTemp = obj.readArduino();
                
                while ntcTemp > (SP+obj.Temperature_Acceptance) || ntcTemp < (SP-obj.Temperature_Acceptance)
                    pause(1)
                    ntcTemp=obj.readArduino();
                   lap=toc;
                   display(lap);
                    %datalog
                    dummyData = [obj.data,ntcTemp];
                    obj.data = dummyData;
                    dummyTime = [obj.time,lap];
                    obj.time=dummyTime;
                    
                end
                display('SETPOINT REACHED');
                 obj.soak(stepSoak);
            end
            
        end
        function ntc = readArduino(obj)
                ntc = obj.ard.readNTC();
                display(ntc);
            end
            
        function  soak(obj,time)
                deltaT = time/3;
                for deltaT= 1:deltaT
                    pause(1);
                    display('SOAKING');
                    ntcTemp = obj.readArduino();
                     lap=toc;
                   display(lap);
                    %datalog
                    dummyData = [obj.data,ntcTemp];
                    obj.data = dummyData;
                    dummyTime = [obj.time,lap];
                    obj.time=dummyTime;
                    
                end
        end
        
        function r = cycle(obj,min,max,num_steps,soaktime,cycles)
            for i = 1:cycles
                obj.stepUp(min,max,num_steps,soaktime);
                obj.stepDown(max,min,num_steps,soaktime);
            end
        end
        function data = getData(obj)
            data = obj.data;
        end
        function timeData = getTimeData(obj)
            timeData=obj.time;
        end
    end
   
        
        
    end
    


