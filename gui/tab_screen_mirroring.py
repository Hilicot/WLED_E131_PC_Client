from tkinter import W, Frame, N, W
from tkinter import ttk as tk
from .GUI_variables import IntVarSafe


def draw_tab_screen_mirroring(rgb_effects, tab, row=0):
    gvars = rgb_effects.gvars

    tk.Checkbutton(tab, text='Active', variable=gvars.mode, onvalue="screen_mirroring", offvalue="off",
                   command=lambda: rgb_effects.display_mode(gvars.mode.get())).grid(row=row, column=0,sticky=(W, N))
    row += 1

    options_frame = Frame(master=tab)
    options_frame.grid(row=row, column=0, sticky=(W, N), padx=(5, 10))

    """
                Capture area size
    """
    # get screen resolution
    screen_width = gvars.root.winfo_screenwidth()
    screen_height = gvars.root.winfo_screenheight()
    print(screen_height)
    # set default values
    gvars.capture_width = IntVarSafe(options_frame, int(screen_width/2))
    gvars.capture_height = IntVarSafe(options_frame, int(screen_height/2))
    gvars.capture_x_offset = IntVarSafe(options_frame, int(screen_width/4))
    gvars.capture_y_offset = IntVarSafe(options_frame, int(screen_height/4))

    # create GUI entries
    tk.Label(options_frame, text="Width").grid(row=row, column=0, sticky=W)
    tk.Entry(master=options_frame, text=gvars.capture_width, width=10).grid(row=row, column=1, sticky=W)
    tk.Label(options_frame, text=" ", width=10).grid(row=row, column=3, sticky=W)
    tk.Label(options_frame, text="height").grid(row=row, column=5, sticky=W)
    tk.Entry(master=options_frame, text=gvars.capture_height, width=10).grid(row=row, column=6, sticky=W)
    row += 1

    tk.Label(options_frame, text="X offset").grid(row=row, column=0, sticky=W)
    tk.Entry(master=options_frame, text=gvars.capture_x_offset, width=10).grid(row=row, column=1, sticky=W)
    tk.Label(options_frame, text="Y offset").grid(row=row, column=5, sticky=W)
    tk.Entry(master=options_frame, text=gvars.capture_y_offset, width=10).grid(row=row, column=6, sticky=W)
