from tkinter import W, Frame, LabelFrame, N, W, BooleanVar, StringVar
from tkinter import ttk as tk
from .GUI_variables import IntVarSafe, update_widgets, WidgetSubdomain, GUI_variables


def draw_tab_screen_mirroring(rgb_effects, tab, row=0):
    gvars: GUI_variables = rgb_effects.gvars

    tk.Checkbutton(tab, text='Active', variable=gvars.mode, onvalue="screen_mirroring", offvalue="off",
                   command=lambda: update_widgets(gvars, gvars.root,
                                                  starting_function=lambda: rgb_effects.display_mode(gvars.mode.get()))) \
        .grid(row=row, column=0, sticky=(W, N))
    row += 1

    screen_frame = Frame(master=tab)
    screen_frame.grid(row=row, column=0, sticky=(W, N), padx=(5, 10))
    gvars.widget_subdomains[screen_frame] = WidgetSubdomain(gvars.mode, "screen_mirroring")
    row += 1

    gvars.screen_mode = StringVar(screen_frame, "Average")
    tk.OptionMenu(screen_frame, gvars.screen_mode, "Average", *["Average","Squared Average","Fast"]).grid(row=0, column=0, sticky=W)
    row += 1
    """
                area size
    """
    size_frame = LabelFrame(master=screen_frame, text="Capture area size")
    size_frame.grid(row=row, column=0, sticky=(W, N), padx=5, pady=10)
    size_frame['borderwidth'] = 1
    size_frame['relief'] = 'groove'

    # get screen resolution
    screen_width = gvars.root.winfo_screenwidth()
    screen_height = gvars.root.winfo_screenheight()

    gvars.fullscreen = BooleanVar(size_frame, True)
    tk.Checkbutton(size_frame, text='Fullscreen', variable=gvars.fullscreen, onvalue=True, offvalue=False,
                   command=lambda: update_widgets(gvars, man_size_frame)).grid(row=row, column=0, sticky=(W, N))
    row += 1

    man_size_frame = Frame(master=size_frame)
    man_size_frame.grid(row=row, column=0, sticky=(W, N), padx=(5, 10))
    gvars.widget_subdomains[man_size_frame] = WidgetSubdomain(gvars.fullscreen, False)

    # set default values
    gvars.capture_width = IntVarSafe(man_size_frame, int(screen_width/2))
    gvars.capture_height = IntVarSafe(man_size_frame, int(screen_height/2))
    gvars.capture_x_offset = IntVarSafe(man_size_frame, int(screen_width/4))
    gvars.capture_y_offset = IntVarSafe(man_size_frame, int(screen_height/4))

    # create GUI entries
    tk.Label(man_size_frame, text="Width").grid(row=row, column=0, sticky=W, padx=5, pady=2)
    tk.Entry(master=man_size_frame, text=gvars.capture_width, width=10).grid(row=row, column=1, sticky=W, padx=5, pady=2)
    tk.Label(man_size_frame, text=" ", width=10).grid(row=row, column=3, sticky=W)
    tk.Label(man_size_frame, text="Height").grid(row=row, column=5, sticky=W, padx=5, pady=2)
    tk.Entry(master=man_size_frame, text=gvars.capture_height, width=10).grid(row=row, column=6, sticky=W, padx=5, pady=2)
    row += 1

    tk.Label(man_size_frame, text="X offset").grid(row=row, column=0, sticky=W, padx=5, pady=2)
    tk.Entry(master=man_size_frame, text=gvars.capture_x_offset, width=10).grid(row=row, column=1, sticky=W, padx=5, pady=2)
    tk.Label(man_size_frame, text="Yoffset").grid(row=row, column=5, sticky=W, padx=5, pady=2)
    tk.Entry(master=man_size_frame, text=gvars.capture_y_offset, width=10).grid(row=row, column=6, sticky=W, padx=5, pady=2)


