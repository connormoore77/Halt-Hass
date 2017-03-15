function varargout = GUI(varargin)
% GUI MATLAB code for GUI.fig
%      GUI, by itself, creates a new GUI or raises the existing
%      singleton*.
%
%      H = GUI returns the handle to a new GUI or the handle to
%      the existing singleton*.
%
%      GUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in GUI.M with the given input arguments.
%
%      GUI('Property','Value',...) creates a new GUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before GUI_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to GUI_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help GUI

% Last Modified by GUIDE v2.5 29-Jun-2016 16:35:54

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @GUI_OpeningFcn, ...
                   'gui_OutputFcn',  @GUI_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before GUI is made visible.
function GUI_OpeningFcn(obj, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to GUI (see VARARGIN)

% Choose default command line output for GUI
handles.output = obj;


% Update handles structure
guidata(obj, handles);
global handle
handle = Tenney('COM4','COM5');




   

% UIWAIT makes GUI wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = GUI_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

% --- Executes on button press in close_button.
function close_button_Callback(hObject, eventdata, handles)
% hObject    handle to close_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global handle
handle.close();
close GUI;
GUI;

% --- Executes on button press in readarduino_button.
function readarduino_button_Callback(hObject, eventdata, handles)
% hObject    handle to readarduino_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global handle
handle.readArduino();

% --- Executes on button press in cycleset_button.
function cycleset_button_Callback(hObject, eventdata, handles)
% hObject    handle to cycleset_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global handle
global cmi
global cma
global ste
global st
global cyc
handle.cycle(cmi,cma,ste,st,cyc);
handle.getData();
h = figure('Name','Cycle Data','NumberTitle','off')
plot(ans)
uisave({'ans','h'},'Trial Data')


function mintemp_entry_Callback(hObject, eventdata, handles)
% hObject    handle to mintemp_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of mintemp_entry as text
%        str2double(get(hObject,'String')) returns contents of mintemp_entry as a double
global cmi
cmi = str2double(get(hObject,'String'));

% --- Executes during object creation, after setting all properties.
function mintemp_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to mintemp_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function maxtemp_entry_Callback(hObject, eventdata, handles)
% hObject    handle to maxtemp_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of maxtemp_entry as text
%        str2double(get(hObject,'String')) returns contents of maxtemp_entry as a double
global cma
cma = str2double(get(hObject,'String'));

% --- Executes during object creation, after setting all properties.
function maxtemp_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to maxtemp_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function steps_entry_Callback(hObject, eventdata, handles)
% hObject    handle to steps_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of steps_entry as text
%        str2double(get(hObject,'String')) returns contents of steps_entry as a double
global ste
 ste = str2double(get(hObject,'String'));



% --- Executes during object creation, after setting all properties.
function steps_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to steps_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function soaktime_entry_Callback(hObject, eventdata, handles)
% hObject    handle to soaktime_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of soaktime_entry as text
%        str2double(get(hObject,'String')) returns contents of soaktime_entry as a double
global st
st = str2double(get(hObject,'String'));

% --- Executes during object creation, after setting all properties.
function soaktime_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to soaktime_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function cycles_entry_Callback(hObject, eventdata, handles)
% hObject    handle to cycles_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of cycles_entry as text
%        str2double(get(hObject,'String')) returns contents of cycles_entry as a double
global cyc
cyc = str2double(get(hObject,'String'));


% --- Executes during object creation, after setting all properties.
function cycles_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to cycles_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in setpoint_button.
function setpoint_button_Callback(hObject, eventdata, handles)
% hObject    handle to setpoint_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global handle
global tem
handle.setPoint(tem);


function setpoint_entry_Callback(hObject, eventdata, handles)
% hObject    handle to setpoint_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of setpoint_entry as text
%        str2double(get(hObject,'String')) returns contents of setpoint_entry as a double
global tem
tem = str2double(get(hObject,'String'));

% --- Executes during object creation, after setting all properties.
function setpoint_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to setpoint_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in stepupset_button.
function stepupset_button_Callback(hObject, eventdata, handles)
% hObject    handle to stepupset_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global handle
global sumi
global suma
global sus
global sut
handle.stepUp(sumi,suma,sus,sut);


function stepupmintemp_entry_Callback(hObject, eventdata, handles)
% hObject    handle to stepupmintemp_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of stepupmintemp_entry as text
%        str2double(get(hObject,'String')) returns contents of stepupmintemp_entry as a double
global sumi
sumi = str2double(get(hObject,'String'));

% --- Executes during object creation, after setting all properties.
function stepupmintemp_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to stepupmintemp_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function stepupmaxtemp_entry_Callback(hObject, eventdata, handles)
% hObject    handle to stepupmaxtemp_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of stepupmaxtemp_entry as text
%        str2double(get(hObject,'String')) returns contents of stepupmaxtemp_entry as a double
global suma
suma = str2double(get(hObject,'String'));

% --- Executes during object creation, after setting all properties.
function stepupmaxtemp_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to stepupmaxtemp_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function stepupsteps_entry_Callback(hObject, eventdata, handles)
% hObject    handle to stepupsteps_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of stepupsteps_entry as text
%        str2double(get(hObject,'String')) returns contents of stepupsteps_entry as a double
global sus
sus = str2double(get(hObject,'String'));


% --- Executes during object creation, after setting all properties.
function stepupsteps_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to stepupsteps_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function stepuptime_entry_Callback(hObject, eventdata, handles)
% hObject    handle to stepuptime_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of stepuptime_entry as text
%        str2double(get(hObject,'String')) returns contents of stepuptime_entry as a double
global sut
sut = str2double(get(hObject,'String'));

% --- Executes during object creation, after setting all properties.
function stepuptime_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to stepuptime_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in stepdownset_button.
function stepdownset_button_Callback(hObject, eventdata, handles)
% hObject    handle to stepdownset_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global handle
global sdmi
global sdma
global sds
global sdt

enableDisableFig       
handle.stepDown(sdma,sdmi,sds,sdt);
enableDisableFig
    
    


function stepdownmintemp_entry_Callback(hObject, eventdata, handles)
% hObject    handle to stepdownmintemp_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of stepdownmintemp_entry as text
%        str2double(get(hObject,'String')) returns contents of stepdownmintemp_entry as a double
global sdmi
sdmi = str2double(get(hObject,'String'));

% --- Executes during object creation, after setting all properties.
function stepdownmintemp_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to stepdownmintemp_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function stepdownmaxtemp_entry_Callback(hObject, eventdata, handles)
% hObject    handle to stepdownmaxtemp_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of stepdownmaxtemp_entry as text
%        str2double(get(hObject,'String')) returns contents of stepdownmaxtemp_entry as a double
global sdma
sdma = str2double(get(hObject,'String'));

% --- Executes during object creation, after setting all properties.
function stepdownmaxtemp_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to stepdownmaxtemp_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function stepdownsteps_entry_Callback(hObject, eventdata, handles)
% hObject    handle to stepdownsteps_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of stepdownsteps_entry as text
%        str2double(get(hObject,'String')) returns contents of stepdownsteps_entry as a double
global sds
sds = str2double(get(hObject,'String'));

% --- Executes during object creation, after setting all properties.
function stepdownsteps_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to stepdownsteps_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function stepdowntime_entry_Callback(hObject, eventdata, handles)
% hObject    handle to stepdowntime_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of stepdowntime_entry as text
%        str2double(get(hObject,'String')) returns contents of stepdowntime_entry as a double
global sdt
sdt = str2double(get(hObject,'String'));

% --- Executes during object creation, after setting all properties.
function stepdowntime_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to stepdowntime_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in tempaccept_setbutton.
function tempaccept_setbutton_Callback(hObject, eventdata, handles)
% hObject    handle to tempaccept_setbutton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global donald_trump
handle.Temperature_Acceptance = donald_trump


function tempaccept_edit_Callback(hObject, eventdata, handles)
% hObject    handle to tempaccept_edit (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of tempaccept_edit as text
%        str2double(get(hObject,'String')) returns contents of tempaccept_edit as a double
global donald_trump
donald_trump = str2double(get(hObject,'String'));

% --- Executes during object creation, after setting all properties.
function tempaccept_edit_CreateFcn(hObject, eventdata, handles)
% hObject    handle to tempaccept_edit (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

  


% --- Executes when user attempts to close figure1.
function figure1_CloseRequestFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: delete(hObject) closes the figure
global handle
handle.close();
close GUI
