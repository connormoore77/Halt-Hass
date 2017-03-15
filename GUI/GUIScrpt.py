from Tkinter import *
import ttk
import Vibration

class GUI:

   

    

    def  __init__(self,master):
        
        
        self.v = StringVar()
        self.x = StringVar()
        self.Grms = StringVar()
        
        
        
        
        self.frame = ttk.LabelFrame(master, text = 'Oven Controls', relief = SUNKEN)
        self.frame.grid(row=0,column=0,columnspan=2)
        self.entry1 = ttk.Entry(self.frame,width=15, state = 'disable')
        self.entry1.grid(row = 0, column = 1)
        self.label1 = ttk.Label(self.frame,text = 'Oven Setpoint', state = 'disable')
        self.label1.grid(row = 0, column = 0)
        self.button1 = ttk.Button(self.frame,text = 'Set Temp',state = 'disable')
        self.button1.grid(row = 1, column = 0, columnspan = 2)
        

        self.frame2 = ttk.LabelFrame(master, text = 'Pressure Controls', relief = SUNKEN)
        self.frame2.grid(row=5, column=0,columnspan=2)
        self.rb1 = ttk.Radiobutton(self.frame2,text = 'PSI',state = 'disable', variable = self.x, value = 1, command = self.psi)
        self.rb1.grid(row = 0,column  = 0)
        self.rb2 = ttk.Radiobutton(self.frame2, text = 'GRMS',state = 'disable', variable = self.x, value = 2,command = self.grms)
        self.rb2.grid(row = 0,column = 1)
        self.entry2 = ttk.Entry(self.frame2,width=15,state = 'disable')
        self.entry2.grid(row = 1, column =1)
        self.label2 = ttk.Label(self.frame2,text = 'Pressure Setpoint',state = 'disable')
        self.label2.grid(row = 1,column = 0)
        self.entry3 = ttk.Entry(self.frame2,width=15,state='disable')
        self.entry3.grid(row = 2, column = 1)
        self.label3 = ttk.Label(self.frame2,text = 'GRMS Setpoint',state = 'disable')
        self.label3.grid(row = 2, column = 0)
        self.button2 = ttk.Button(self.frame2,text = 'Set Pressure',state = 'disable')
        self.button2.grid(row=3,column = 0,columnspan=2)
        #if grms > n*stepsize +3:
        self.message = Message(self.frame2, text= '(+)', fg = 'Red').grid(row=4, column = 0, columnspan = 2)
        #if grms < n*stepsize -3:
        #        self.message = Message(self.frame2, textvariable= Grms +'(-)', fg = 'Red').grid(row=4, column = 0, columnspan = 2)
        #if grms > n*stepsize - 3 && grms < stepsize*n +3:
        #        self.message = Message(self.frame2, textvariable= Grms, fg = 'Green').grid(row=4, column = 0, columnspan = 2)

        
        self.frame3 = ttk.Frame(master,relief=GROOVE, borderwidth=4)
        self.frame3.grid(row=6,column=0,columnspan=2)
        ttk.Radiobutton(self.frame3,text = 'Oven Control',variable=self.v,value=1,command = self.ovenradio).pack(side=LEFT)
        ttk.Radiobutton(self.frame3,text = 'Pressure Control', variable = self.v, value=2, command = self.pressureradio).pack(side=LEFT)
        ttk.Radiobutton(self.frame3,text = 'Cycle Control',variable = self.v, value=3, command = self.cycleradio).pack(side=LEFT)
        ttk.Radiobutton(self.frame3,text = "General Setpoint",variable = self.v, value=4,command = self.setpointradio).pack(side = LEFT)



        self.frame4 = ttk.LabelFrame(master, text = 'Cycle Control', relief = SUNKEN)
        self.frame4.grid(row=7,column=0,columnspan=2)
        self.entry4 = ttk.Entry(self.frame4,width=15,state='disable')
        self.entry4.grid(row = 0, column =1)
        self.label4 = ttk.Label(self.frame4,text = 'Step size',state = 'disable')
        self.label4.grid(row = 0,column = 0)
        self.entry5 = ttk.Entry(self.frame4,width=15,state='disable')
        self.entry5.grid(row = 1, column = 1)
        self.label5 = ttk.Label(self.frame4,text = 'Step length',state = 'disable')
        self.label5.grid(row = 1, column = 0)
        self.entry6 = ttk.Entry(self.frame4,width=15,state='disable')
        self.entry6.grid(row = 2, column = 1)
        self.label6 = ttk.Label(self.frame4,text = 'Number of Steps',state = 'disable')
        self.label6.grid(row = 2, column = 0)
        self.entry7 = ttk.Entry(self.frame4,width=15,state='disable')
        self.entry7.grid(row = 3, column = 1)
        self.label7 = ttk.Label(self.frame4,text = 'Number of Steps',state = 'disable')
        self.label7.grid(row = 3, column = 0)
        self.entry8 = ttk.Entry(self.frame4,width=15,state='disable')
        self.entry8.grid(row = 3, column = 1)
        self.label8 = ttk.Label(self.frame4,text = 'Frequency of Hammer',state = 'disable')
        self.label8.grid(row = 3, column = 0)
        self.button4 = ttk.Button(self.frame4, text = 'Cycle Pressure', state = 'disable')
        self.button4.grid(row = 5, column = 0,  columnspan = 2)

        
        
    def ovenradio(self):
        for child in self.frame.winfo_children():
            child.configure(state = 'enable')
        for child in self.frame2.winfo_children():
            child.configure(state = 'disable')
        for child in self.frame4.winfo_children():
            child.configure(state = 'disable')
        self.x.set(0)
        
    def pressureradio(self):
        self.rb1.configure(state = 'enable')
        self.rb2.configure(state = 'enable')
        for child in self.frame.winfo_children():
            child.configure(state = 'disable')
        for child in self.frame4.winfo_children():
            child.configure(state = 'disable')
        self.button2.configure(state = 'enable')
        self.x.set(0)
        
    def cycleradio(self):
        for child in self.frame4.winfo_children():
            child.configure(state = 'enable')
        for child in self.frame.winfo_children():
            child.configure(state = 'disable')
        for child in self.frame2.winfo_children():
            child.configure(state = 'disable')
        self.x.set(0)
        
    def setpointradio(self):
        for child in self.frame.winfo_children():
            child.configure(state = 'enable')
        self.rb1.configure(state = 'enable')
        self.rb2.configure(state = 'enable')
        self.button2.configure(state = 'enable')
        for child in self.frame4.winfo_children():
            child.configure(state = 'disable')
        self.x.set(0)
        
    def grms(self):
        self.entry2.configure(state='disabled')
        self.entry3.configure(state = 'enabled')
        self.label3.configure(state='enable')
        self.label2.configure(state='disable')

    def psi(self):
        self.entry2.configure(state='enabled')
        self.entry3.configure(state = 'disabled')
        self.label2.configure(state='enable')
        self.label3.configure(state='disable')
        

    
    
    
    
def main():
    root = Tk()
    app = GUI(root)
    root.mainloop()


if __name__ == "__main__":main()
