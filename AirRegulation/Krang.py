# HALT/HASS GUI
import Tkinter
import Vibration
top = Tk()

L1 = Label(top, text="Step Size")
L1.pack(side = LEFT)
E1 = Entry(top, bd =5, )
L2 = Label(top, text="Step Length")
L2.pack( side = LEFT)
E2 = Entry(top, bd =5)
L3 = Label(top, text="Number of Steps")
L3.pack( side = LEFT)
E3 = Entry(top, bd =5)
L4 = Label(top, text="Frequency")
L4.pack( side = LEFT)
E4 = Entry(top, bd =5)


Cycle = Tkinter.Button(top, text = "Start Pressure Cycle", command = VibrationCycling.cycle(step_size, step_length, number_of_steps, frequency=5)

                       
                       
top.mainloop()
