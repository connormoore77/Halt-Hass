classdef Arduino
    %MATLAB
    %UNTITLED2 Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        comm;
    end
    
    methods (Access = public)
        function  obj = Arduino(port)
         
            obj.comm = serial(port,'Baudrate',9600,'Terminator','CR');
            obj.connect(port);
            
        end
        function r = connect(obj,port)
            % chamber = serial(port,'Baudrate',9600,'Terminator','CR');
            get(obj.comm);
            fopen(obj.comm); 
            set(obj.comm,'ReadAsyncMode','manual');
            readasync(obj.comm);
        end
         function r = close(obj)
            fclose(obj.comm);
         end
         function NTCTemp = readNTC(obj)
             
              NTCTemp = str2double(fgetl(obj.comm));
         end
    end
    
end

