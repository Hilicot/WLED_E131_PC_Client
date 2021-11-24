from tkinter import Tk
from tkinter import ttk as tk

from .tab_general import draw_tab_general
from .tab_screen_mirroring import draw_tab_screen_mirroring
from .footer import draw_footer


def draw_GUI(rgb_effects):
    root = Tk()
    root.title("E131 RGB controller")
    rgb_effects.gvars.root = root
    tabControl = tk.Notebook(root)

    tab1 = tk.Frame(tabControl)
    tabControl.add(tab1, text='General')
    draw_tab_general(rgb_effects, tab1)

    tab2 = tk.Frame(tabControl)
    tabControl.add(tab2, text='Screen Mirroring')
    draw_tab_screen_mirroring(rgb_effects, tab2)

    tabControl.grid(row=0, column=0)

    draw_footer(rgb_effects, root, 1)

    """function to run at startup after the gui is defined"""
    rgb_effects.set_ip()
    rgb_effects.gvars.print_console("Ready")

    return root
