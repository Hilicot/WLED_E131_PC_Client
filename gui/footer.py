from tkinter import E, StringVar, Frame
from tkinter import ttk as tk


def draw_footer(rgb_effects, root, row=0):
    gvars = rgb_effects.gvars

    footer_frame = Frame(master=root)
    footer_frame.grid(row=row, column=0, padx=(10, 10))

    # console
    gvars.console_output = StringVar(footer_frame, '')
    console = tk.Label(footer_frame, width=50)
    console['textvariable'] = gvars.console_output
    console.grid(row=row, column=0)

    # exit button
    tk.Button(footer_frame, text="Exit", command=root.destroy).grid(row=row, column=5, sticky=E)
