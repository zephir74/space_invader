#!/usr/bin/env python3

from tkinter import *
import os

def launch():
    os.system("python3 space_invader.py")

controls = r"""-- Controls --
Left / right : arrows
Shoot : space"""

window = Tk()

window.title('Space Invaders')
window.geometry("900x638")

background = PhotoImage(file = "resources/gui_background.png") 
bg = Label(window, image = background) 
bg.place(x = 0, y = 0) 

text = Label(window, text=controls)
text.configure(bg="light green")
text.place(x=750, y=0)

button = Button(window, text='Start playing', width=25, command=launch)
button.place(x=340, y=600)

window.mainloop()