from tkinter import W
from tkinter import ttk as tk


def draw_tab_screen_mirroring(rgb_effects, tab, row=0):
    gvars = rgb_effects.gvars

    tk.Checkbutton(tab, text='Active', variable=gvars.mode, onvalue="screen_mirroring", offvalue="off",
                   command=lambda: rgb_effects.display_mode(gvars.mode.get())).grid(row=row, column=0)
