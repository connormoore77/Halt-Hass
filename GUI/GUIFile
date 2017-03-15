from Tkinter import *
import ttk

class GUI:

    

    def  __init__(self,master):

                
        v = StringVar()
        x = StringVar()
        
        self.frame = ttk.LabelFrame(master, text = 'Oven Controls', relief = SUNKEN)
        self.frame.grid(row=0,column=0,columnspan=2)
        self.entry1 = ttk.Entry(self.frame,width=15, state = 'disable')
        self.entry1.grid(row = 0, column = 1)
        self.label1 = ttk.Label(self.frame,text = 'Oven Setpoint', state = 'disable')
        self.label1.grid(row = 0, column = 0)
        self.button1 = ttk.Button(self.frame,text = 'Set Temp',state = 'disable')
        self.button1.grid(row = 1, column = 0, columnspan = 2)
        

        self.frame2 = ttk.LabelFrame(master, text = 'Pressure Controls', relief = SUNKEN)
        self.frame2.grid(row=2, column=0,columnspan=2)
        self.entry2 = ttk.Entry(self.frame2,width=15,state='disable')
        self.entry2.grid(row = 0, column =1)
        self.label2 = ttk.Label(self.frame2,text = 'Pressure Setpoint',state = 'disable')
        self.label2.grid(row = 0,column = 0)
        self.entry3 = ttk.Entry(self.frame2,width=15,state='disable')
        self.entry3.grid(row = 1, column = 1)
        self.label3 = ttk.Label(self.frame2,text = 'GRMS Setpoint',state = 'disable')
        self.label3.grid(row = 1, column = 0)
        ttk.Button(self.frame2,text = 'Set Pressure',state = 'disable').grid(row=2,column = 0,columnspan=2)
        self.rb1 = ttk.Radiobutton(self.frame2,text = 'PSI',state = 'disable', variable = x, value = 1, command = self.psi)
        self.rb1.grid(row = 3,column  = 0)
        self.rb2 = ttk.Radiobutton(self.frame2, text = 'GRMS',state = 'disable', variable = x, value = 2,command = self.grms)
        self.rb2.grid(row = 3,column = 1)

        

        
        self.frame3 = ttk.Frame(master,relief=GROOVE, borderwidth=4)
        self.frame3.grid(row=6,column=0,columnspan=2)
        ttk.Radiobutton(self.frame3,text = 'Oven Control',variable=v,value=1,command=self.ovenradio).pack(side=LEFT)
        ttk.Radiobutton(self.frame3,text = 'Pressure Control', variable = v, value=2,command = self.pressureradio).pack(side=LEFT)
        ttk.Radiobutton(self.frame3,text = 'Cycle Control',variable = v, value=3,command = self.cycleradio).pack(side=LEFT)
        ttk.Radiobutton(self.frame3,text = "General Setpoint",variable = v, value=4, command = self.setpointradio).pack(side = LEFT)



        self.frame4 = ttk.LabelFrame(master, text = 'Cycle Control', relief = SUNKEN)
        self.frame4.grid(row=8,column=0,columnspan=2)
        

        
        
    def ovenradio(self):
        for child in self.frame.winfo_children():
            child.configure(state = 'enable')
        for child in self.frame2.winfo_children():
            child.configure(state = 'disable')
        for child in self.frame4.winfo_children():
            child.configure(state = 'disable')

    def pressureradio(self):
        for child in self.frame2.winfo_children():
            child.configure(state = 'enable')
        for child in self.frame.winfo_children():
            child.configure(state = 'disable')
        for child in self.frame4.winfo_children():
            child.configure(state = 'disable')

    def cycleradio(self):
        for child in self.frame4.winfo_children():
            child.configure(state = 'enable')
        for child in self.frame.winfo_children():
            child.configure(state = 'disable')
        for child in self.frame2.winfo_children():
            child.configure(state = 'disable')

    def setpointradio(self):
        for child in self.frame.winfo_children():
            child.configure(state = 'enable')
        for child in self.frame2.winfo_children():
            child.configure(state = 'enable')
        for child in self.frame4.winfo_children():
            child.configure(state = 'disable')

    def grms(self):
        self.entry2.config(state='disabled')
        self.entry3.config(state = 'enabled')

    def psi(self):
        self.entry2.config(state='enabled')
        self.entry3.config(state = 'disabled')

    
    
    
    
def main():
    root = Tk()
    app = GUI(root)
    root.mainloop()


if __name__ == "__main__":main()
