from tkinter import N, S, E, W, Tk, StringVar, TclError, Frame, Button
from tkinter import ttk as tk
from RGB_effects import *
from gui import GUI_variables, draw_GUI
from audio_functions import list_available_audio_devices

gvars = GUI_variables(list_available_audio_devices)
rgb_effects = RGBEffects(gvars)

root = draw_GUI(rgb_effects)

# actual GUI loop
root.mainloop()
