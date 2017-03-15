clc;%clean slate

%Here is the global paramters, min,max and N can be adjusted as desired
%------------------------------------------------------
min=-40;%minimum value of profile
max=60;%max value of profile
N=1;%number of discrete steps
cycles=252;%number of up and down cycles
acceptance=11.5;%the range of accepted values for step completion
step = (max-min)/N;%calculate the value of each step 
soakTime = 1;%wait between steps in 10 second intervals (weird scheme I know)
display(step);
display(N);
display(max);
display(min);
display(cycles);
display(acceptance);
display(soakTime*10);
%------------------------------------------------------


%Open log file and create/open serial connection with tenney
%-------------------------------------------------------------------------
log = fopen('tempLog.txt','wt');%text file for temp log
tenney = serial('COM4','BaudRate',9600,'Terminator','CR');%create serial object
get(tenney);%get some diagnostics for good measure
fopen(tenney);%initiate serial connection
pause(10);%pause for 10 seconds to let SYN ACK 
arduino = serial('COM5','BaudRate',9600,'Terminator','CR');
fopen(arduino);
set(arduino,'ReadAsyncMode','manual');
readasync(arduino);
%-----------------------------------------------------------------------

%------------write paramters to log--------------------------------
fprintf(log, 'step size = %d\n',step);
fprintf(log, 'Number of steps = %d\n',N);
fprintf(log, 'min temp = %d\n',min);
fprintf(log, 'max temp = %d\n',max);
fprintf(log, 'number of cycles = %d\n',cycles);
fprintf(log, 'step acceptance = %d\n',acceptance);



%-------------This is a good diagnostic tool for troubleshooting--
%for i=1:6
%    fprintf(tenney,'? CSP\n');%ask what the current set point is
%    CSP = fscanf(tenney);%scan for an answer and store it into variable CSP
%    display(CSP);%write to screen value of CSP
%    display(i);%display the iterations number
%    pause(1);%pause a second to let the dust settle
%    fprintf(log,'T %s\n V %s\n', char(datetime('now')), CSP);%record readings to log file
%end
%-----------------------------------------------------------------

for j=1:cycles% total overall number of cycles loop
%-------------Main loop for ramping UP---------------------------
for i=0:N
    
    SP = min+i*step;%lets do N intervals starting at min  
    display(SP);%display the current setpoint
    fprintf(log,'Setpoint = %d\n',SP);%log the setpoint
    fprintf(tenney,'= SP1 %d\n',SP);%change the set point 
    pause(5);%give the tenney time to change
    fprintf(tenney,'? C1\n');%ask what the current temp point is
    pause(2);%give it time to think
    display(j);
    
    
    %-----------this next part gets confusing--------------------------
    currentTemp = fgetl(tenney);   %scan for an answer and store it into variable 
    dummyArray = size(currentTemp);%the tenny sends information in 2 arrays, we want the length of both of them. the first is trivially 1 and the second index is the real size
    maxIndex = dummyArray(2);      %here we extract the real size of the character aarry which is encoded in the second element of the dummyArray
                                   %The size of the string will be our max
                                   %index for data formatting
    
    x=1;%to extract the lower index needed for formatting we need to look for the first non-control-protocol element
    while double(currentTemp(x)) < 20 %the control protocols are all ascii < 20 so we loop over the control protocols to get rid of them
        x = x+1;
    end %once we know where the first non-protocol element in the character array we have the lower bound for formatting
    
    numericalTemp = str2double(currentTemp(x:maxIndex));%finally caste the currentTemp into a double datatype
    display(currentTemp);%these lines are just for real time monitering
    display(numericalTemp);
    %display(i);%display the iterations number
       
    BoxTemp = fgetl(arduino);
    while str2double(BoxTemp) > (SP+acceptance) || str2double(BoxTemp) < (SP-acceptance) %get stuck in a loop until we reach the setpoint
        pause(10);
        fprintf(tenney,'? C1\n');%ask what the current temp point is
        pause(2);%give it time to think
        currentTemp = fgetl(tenney);%scan for an answer and store it into variable Val
    dummyArray = size(currentTemp);
    maxIndex = dummyArray(2);
    
    %---------------you will see repeated versions of what we have done
    %above. This strange step is a clumsy way to solve a simple problem
    %that can probably be solved a better way. I have tried many many
    %things and this seems to be the most ROBUST solution-------------
    if(str2double(BoxTemp)<-200)%failsafe in case something comes undone
       fprintf(tenney,'= SP1 %d\n',20); 
    end
    
    x=1;
    while double(currentTemp(x)) < 20
        x = x+1;
    end
    
    numericalTemp = str2double(currentTemp(x:maxIndex));
    display(currentTemp);
    display(numericalTemp);
    BoxTemp = fgetl(arduino);
    display(BoxTemp);
    display('the current cycle is j');
         display(j);
        fprintf(log,'T %s\n V %s\n B %s\n', char(datetime('now')), currentTemp, BoxTemp);%record readings to log file
        

    end
    display('SETPOINT REACHED');
    
    %here is where we can soak each individual step
    for s=1:soakTime
         pause(10);
        fprintf(tenney,'? C1\n');%ask what the current temp point is
        pause(2);%give it time to think
        currentTemp = fgetl(tenney);%scan for an answer and store it into variable Val
        display(currentTemp);%write to screen value of currentTemp
     
         BoxTemp = fgetl(arduino);
         display(BoxTemp);
        fprintf(log,'T %s\n V %s\n B %s\n', char(datetime('now')), currentTemp, BoxTemp);%record readings to log file
        display(j);
    end
    
end
    %---------soak for 3 minutes with readings every 30 seconds--------
   %{
    pause(10);
        fprintf(tenney,'? C1\n');%ask what the current temp point is
        pause(2);%give it time to think
        currentTemp = fgetl(tenney);%scan for an answer and store it into variable Val
        display(currentTemp);%write to screen value of currentTemp
        fprintf(log,'T %s\n V %s\n', char(datetime('now')), currentTemp);%record readings to log file
    pause(10);
        fprintf(tenney,'? C1\n');%ask what the current temp point is
        pause(2);%give it time to think
        currentTemp = fgetl(tenney);%scan for an answer and store it into variable Val
        display(currentTemp);%write to screen value of currentTemp
        fprintf(log,'T %s\n V %s\n', char(datetime('now')), currentTemp);%record readings to log file 
    pause(10);
        fprintf(tenney,'? C1\n');%ask what the current temp point is
        pause(2);%give it time to think
        currentTemp = fgetl(tenney);%scan for an answer and store it into variable Val
        display(currentTemp);%write to screen value of currentTemp
        fprintf(log,'T %s\n V %s\n', char(datetime('now')), currentTemp);%record readings to log file
    pause(10);
        fprintf(tenney,'? C1\n');%ask what the current temp point is
        pause(2);%give it time to think
        currentTemp = fgetl(tenney);%scan for an answer and store it into variable Val
        display(currentTemp);%write to screen value of currentTemp
        fprintf(log,'T %s\n V %s\n', char(datetime('now')), currentTemp);%record readings to log file
    %-------------------------------------------------------------------
%}



%-------------Main loop for ramping DOWN---------------------------
for i=0:N
    
    SP = max-i*step;%lets do N intervals starting at min  
    display(SP);%display the current setpoint
    fprintf(log,'Setpoint = %d\n',SP);%log the setpoint
    fprintf(tenney,'= SP1 %d\n',SP);%change the set point 
    pause(5);%give the tenney time to change
    fprintf(tenney,'? C1\n');%ask what the current temp point is
    pause(2);%give it time to think
    currentTemp = fgetl(tenney);%scan for an answer and store it into variable 
    dummyArray = size(currentTemp);
    maxIndex = dummyArray(2);
    
    x=1;
    while double(currentTemp(x)) < 20
        x = x+1;
    end
    
    numericalTemp = str2double(currentTemp(x:maxIndex));
    display(currentTemp);
    display(numericalTemp);
    %display(anotherthing);
    %display(i);%display the iterations number
       
    BoxTemp = fgetl(arduino);
    while str2double(BoxTemp) > (SP+acceptance) || str2double(BoxTemp) < (SP-acceptance) %get stuck in a loop until we reach the setpoint
        pause(10);
        fprintf(tenney,'? C1\n');%ask what the current temp point is
        pause(2);%give it time to think
        currentTemp = fgetl(tenney);%scan for an answer and store it into variable Val
    dummyArray = size(currentTemp);
    maxIndex = dummyArray(2);
    
    if(str2double(BoxTemp)<-200)%failsafe in case something comes undone
       fprintf(tenney,'= SP1 %d\n',20); 
    end
    
    x=1;
    while double(currentTemp(x)) < 20
        x = x+1;
    end
    
    numericalTemp = str2double(currentTemp(x:maxIndex));
    display(currentTemp);
    display(numericalTemp);
         BoxTemp = fgetl(arduino);
         display(BoxTemp);
         display('the current cycle is j');
         display(j);
        fprintf(log,'T %s\n V %s\n B %s\n', char(datetime('now')), currentTemp, BoxTemp);%record readings to log file
        

    end
    display('SETPOINT REACHED');
    %here is where you would soak each individual step
       for s=1:soakTime
         pause(10);
        fprintf(tenney,'? C1\n');%ask what the current temp point is
        pause(2);%give it time to think
        currentTemp = fgetl(tenney);%scan for an answer and store it into variable Val
        display(currentTemp);%write to screen value of currentTemp
        
         BoxTemp = fgetl(arduino);
         display(BoxTemp);
        fprintf(log,'T %s\n V %s\n B %s\n', char(datetime('now')), currentTemp, BoxTemp);%record readings to log file
        display(j);
    end
end
    %---------soak for 3 minutes with readings every 30 seconds--------
   %{
    pause(10);
        fprintf(tenney,'? C1\n');%ask what the current temp point is
        pause(2);%give it time to think
        currentTemp = fgetl(tenney);%scan for an answer and store it into variable Val
        display(currentTemp);%write to screen value of currentTemp
        fprintf(log,'T %s\n V %s\n', char(datetime('now')), currentTemp);%record readings to log file
    pause(10);
        fprintf(tenney,'? C1\n');%ask what the current temp point is
        pause(2);%give it time to think
        currentTemp = fgetl(tenney);%scan for an answer and store it into variable Val
        display(currentTemp);%write to screen value of currentTemp
        fprintf(log,'T %s\n V %s\n', char(datetime('now')), currentTemp);%record readings to log file 
    pause(10);
        fprintf(tenney,'? C1\n');%ask what the current temp point is
        pause(2);%give it time to think
        currentTemp = fgetl(tenney);%scan for an answer and store it into variable Val
        display(currentTemp);%write to screen value of currentTemp
        fprintf(log,'T %s\n V %s\n', char(datetime('now')), currentTemp);%record readings to log file
    pause(10);
        fprintf(tenney,'? C1\n');%ask what the current temp point is
        pause(2);%give it time to think
        currentTemp = fgetl(tenney);%scan for an answer and store it into variable Val
        display(currentTemp);%write to screen value of currentTemp
        fprintf(log,'T %s\n V %s\n', char(datetime('now')), currentTemp);%record readings to log file
    pause(10);
        fprintf(tenney,'? C1\n');%ask what the current temp point is
        pause(2);%give it time to think
        currentTemp = fgetl(tenney);%scan for an answer and store it into variable Val
        display(currentTemp);%write to screen value of currentTemp
        fprintf(log,'T %s\n V %s\n', char(datetime('now')), currentTemp);%record readings to log file
    pause(10);
        fprintf(tenney,'? C1\n');%ask what the current temp point is
        pause(2);%give it time to think
        currentTemp = fgetl(tenney);%scan for an answer and store it into variable Val
        display(currentTemp);%write to screen value of currentTemp
        fprintf(log,'T %s\n V %s\n', char(datetime('now')), currentTemp);%record readings to log file
            pause(10);
        fprintf(tenney,'? C1\n');%ask what the current temp point is
        pause(2);%give it time to think
        currentTemp = fgetl(tenney);%scan for an answer and store it into variable Val
        display(currentTemp);%write to screen value of currentTemp
        fprintf(log,'T %s\n V %s\n', char(datetime('now')), currentTemp);%record readings to log file
    pause(10);
        fprintf(tenney,'? C1\n');%ask what the current temp point is
        pause(2);%give it time to think
        currentTemp = fgetl(tenney);%scan for an answer and store it into variable Val
        display(currentTemp);%write to screen value of currentTemp
        fprintf(log,'T %s\n V %s\n', char(datetime('now')), currentTemp);%record readings to log file
    pause(10);
        fprintf(tenney,'? C1\n');%ask what the current temp point is
        pause(2);%give it time to think
        currentTemp = fgetl(tenney);%scan for an answer and store it into variable Val
        display(currentTemp);%write to screen value of currentTemp
        fprintf(log,'T %s\n V %s\n', char(datetime('now')), currentTemp);%record readings to log file
    pause(10);
        fprintf(tenney,'? C1\n');%ask what the current temp point is
        pause(2);%give it time to think
        currentTemp = fgetl(tenney);%scan for an answer and store it into variable Val
        display(currentTemp);%write to screen value of currentTemp
        fprintf(log,'T %s\n V %s\n', char(datetime('now')),
        currentTemp);%record readings to log file
    %}
        %-------------------------------------------------------------------
end

%everywhere there is a datalog I would like to have a GUI plot
%look into using plot([x,y]) with currentTemp and a time scalar
%I need to build a stopwatch

fclose(tenney);%close the serial communication
delete(tenney);%clean house
display('everything is closed and clean: Job Success');%let the user know everything is succesful