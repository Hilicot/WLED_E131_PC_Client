from tkinter import TclError, IntVar
from tkinter.colorchooser import askcolor
import numpy as np


class IntVarSafe(IntVar):
    """Variant of IntVar which never throws errors, but silently sets itself to zero"""

    def get(self):
        try:
            return super().get()
        except TclError:
            return 0


class GUI_variables:
    # General tab variables
    root = None
    mode = None
    color_generator_name = None
    console_output = None
    num_leds = None
    speed = None
    audio_device = None
    color = np.array([255, 0, 0])
    color_hex = "#ff0000"
    hue = 0
    speaker1 = speaker2 = None
    brightness = None
    ip = [None, None, None, None]

    # screen tab variables
    fullscreen = None
    capture_width = None
    capture_height = None
    capture_x_offset = None
    capture_y_offset = None


    def __init__(self, list_available_audio_devices_function):
        self.list_available_audio_devices = list_available_audio_devices_function

    def choose_color(self, button):
        color_tuple = askcolor(title="Choose color")
        self.color = np.array(color_tuple[0])
        self.color_hex = color_tuple[1]
        self.hue = rgb2hsv(self.color[0], self.color[1], self.color[2])[0]
        button['bg'] = self.color_hex

    def print_console(self, message:str):
        self.console_output.set(message)
